"""Stage-2 evaluation (stage2/s2_freeze.yaml). Stage-1/pivot conventions: the forecast starts from the noisy observation
at the window's last frame, errors on future frames, integration stops once every state has exceeded 0.3.

Usage: python stage2/scripts/s2_eval.py <panel> <device> <arm> <seed> <variant>
  panel    s2_test_Re<Re>_<world> | s2_test2p_<case>
  arm      O | P1 | P1x | persistence | H | H_Re_only | L0 | L_range | L0big | L_range_wide
  seed     model seed (0, 1, 2; 0 for single-seed arms)
  variant  std (w in 3, 6, 11: window frames 1..w) | straddle (11-frame windows ending at k = 8, 5, 2) |
           noise5 (5% observations, w = 11) | 2p (two-parameter panel, w = 11; H identifies (Re, amp) by Nelder-Mead)
Writes runs/s2_eval/<panel>/<arm>_s<seed>_<variant>_<k>.npz (k = w, or the window end e for straddle) and
stage2/results/eval_<panel>.json (online cost).
"""
import fcntl
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "pivot"))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from ap import config  # noqa: E402
from ap.arms import identify, solver_errors  # noqa: E402
from ap.fno import ARMS, build  # noqa: E402
from ap.solver import KolmoDrag, STEPS_PER_OBS  # noqa: E402
from ap_eval import Truth, rollout_errors  # noqa: E402
from hybrid import Correction, HybridSolver  # noqa: E402

PRE, EPS_STOP = 10, 0.3
RES = config.PKG / "stage2" / "results"
PR = config.PKG / "pivot" / "results"


def sigma40(world):
    if world == "D":
        return json.loads((config.RESULTS / "chaos_gate.json").read_text())["Re40"]["sigma_A"]
    return json.loads((PR / "chaos_gate_C.json").read_text())["Re40"]["sigma_A"]


def model_dir(arm, world, seed):
    base = f"H_{world}" if arm == "H" else arm + ("" if world == "D" else "_C")
    return config.RUNS / "train" / (base if seed == 0 else f"{base}_s{seed}")


def nm_gen(x0, steps, lo, hi):
    """Nelder-Mead in 2-D as a generator: yields points, receives objective values (s2_freeze item 3)."""
    clip = lambda x: np.minimum(np.maximum(x, lo), hi)  # noqa: E731
    S = [clip(np.array(x0, float)), clip(np.array(x0, float) + [steps[0], 0.0]), clip(np.array(x0, float) + [0.0, steps[1]])]
    F = []
    for x in S:
        F.append((yield x))
    while True:
        o = np.argsort(F)
        S, F = [S[i] for i in o], [F[i] for i in o]
        c = 0.5 * (S[0] + S[1])
        xr = clip(c + (c - S[2]))
        fr = yield xr
        if fr < F[0]:
            xe = clip(c + 2.0 * (c - S[2]))
            fe = yield xe
            S[2], F[2] = (xe, fe) if fe < fr else (xr, fr)
        elif fr < F[1]:
            S[2], F[2] = xr, fr
        else:
            xc = clip(c + 0.5 * (xr - c)) if fr < F[2] else clip(c + 0.5 * (S[2] - c))
            fc = yield xc
            if fc < min(fr, F[2]):
                S[2], F[2] = xc, fc
            else:
                S[1] = S[0] + 0.5 * (S[1] - S[0])
                F[1] = yield S[1]
                S[2] = S[0] + 0.5 * (S[2] - S[0])
                F[2] = yield S[2]


def nelder_mead_batched(obj, n, x0, steps, lo, hi, n_eval=60):
    gens = [nm_gen(x0, steps, lo, hi) for _ in range(n)]
    pts = np.stack([next(g) for g in gens])
    best_x, best_f = pts.copy(), np.full(n, np.inf)
    for k in range(n_eval):
        f = obj(pts)
        better = f < best_f
        best_f[better], best_x[better] = f[better], pts[better]
        if k == n_eval - 1:
            break
        pts = np.stack([g.send(float(fi)) for g, fi in zip(gens, f)])
    return best_x, best_f


def main(panel, device, arm, seed, variant):
    seed = int(seed)
    tp = json.loads((RES / "test_panels.json").read_text())[panel]
    world, Re, amp = tp["world"], int(tp["Re"]), float(tp["amp"])
    alpha = float(config.freeze()["drag"]["alpha"])
    beta = float(tp["beta"])
    sA, F = tp["sigma_A"], tp["F"]
    sc = 64.0 / sigma40(world)
    T = np.load(config.CACHE / f"{panel}.npy", mmap_mode="r")
    Y = np.load(config.CACHE / f"{panel}{'_obs5' if variant == 'noise5' else '_obs'}.npy", mmap_mode="r")
    n = T.shape[1]
    out = config.RUNS / "s2_eval" / panel
    out.mkdir(parents=True, exist_ok=True)
    resf = RES / f"eval_{panel}.json"
    if variant == "std":
        windows = [(w, 1, w) for w in (3, 6, 11)]            # (label, first frame, last frame)
    elif variant == "straddle":
        windows = [(e, e - 10, e) for e in (8, 5, 2)]
    else:
        windows = [(11, 1, 11)]
    g = None
    fno = None
    for lab, k0, k1 in windows:
        f = out / f"{arm}_s{seed}_{variant}_{lab}.npz"
        if f.exists():
            continue
        t0 = time.time()
        wlen = k1 - k0 + 1
        tr = Truth(T, k1, F)
        y0 = np.asarray(Y[PRE + k1], dtype=np.float64)
        Yw = np.asarray(Y[PRE + k0:PRE + k1 + 1])
        extra, cost = {}, {}
        if arm == "persistence":
            err = np.stack([np.sqrt(((y0 - tr(j)) ** 2).sum((-2, -1))) / sA for j in range(F + 1)])
        elif arm == "O":
            make = lambda re: KolmoDrag(re, alpha=alpha, beta=beta, device=device, amp=np.full(len(re), amp))  # noqa: E731
            err, st = solver_errors(y0, tr, np.full(n, float(Re)), 0.0, sA, device, EPS_STOP, make=make)
            cost = dict(forecast_steps=st)
        elif arm in ("P1", "P1x"):
            a, b = (alpha, beta) if arm == "P1x" else (0.0, 0.0)
            rh, ev, st_id = identify(Yw, wlen, a, sA, device, beta=b)
            ti = time.time() - t0
            err, st = solver_errors(y0, tr, rh, a, sA, device, EPS_STOP, beta=b)
            extra = dict(re_hat=rh)
            cost = dict(solver_steps=st_id, objective_evals=ev, forecast_steps=st, identify_seconds_per_state=ti / n)
        elif arm in ("H", "H_Re_only"):
            if g is None:
                g = Correction(sc).to(device)
                g.load_state_dict(torch.load(model_dir("H", world, seed) / "best.pt", map_location=device))
                g.eval()
            if variant == "2p" and arm == "H":
                Yt = torch.as_tensor(Yw, device=device)

                def obj(P):
                    m = HybridSolver(P[:, 0], g, device=device)
                    m.set_amp(P[:, 1])
                    with torch.no_grad():
                        wh = m.to_spec(Yt[0])
                        tot = torch.zeros(n, dtype=torch.float64, device=device)
                        for k in range(1, wlen):
                            wh = m.flow(wh, STEPS_PER_OBS)
                            tot += ((m.to_phys(wh).double() - Yt[k]) ** 2).sum((-2, -1))
                    return (tot / (wlen - 1) / sA ** 2).cpu().numpy()

                P, _ = nelder_mead_batched(obj, n, (40.0, 1.0), (5.0, 0.1), np.array([25.0, 0.5]), np.array([80.0, 1.5]))
                ti = time.time() - t0

                def make(re, P=P):
                    m = HybridSolver(re, g, device=device)
                    m.set_amp(P[:, 1])
                    return m
                with torch.no_grad():
                    err, st = solver_errors(y0, tr, P[:, 0], 0.0, sA, device, EPS_STOP, make=make)
                extra = dict(re_hat=P[:, 0], amp_hat=P[:, 1])
                cost = dict(objective_evals=60, solver_steps=60 * (wlen - 1) * STEPS_PER_OBS, forecast_steps=st,
                            identify_seconds_per_state=ti / n)
            else:
                make = lambda re: HybridSolver(re, g, device=device)  # noqa: E731
                with torch.no_grad():
                    rh, ev, st_id = identify(Yw, wlen, 0.0, sA, device, lo=25.0, hi=80.0, make=make)
                ti = time.time() - t0
                with torch.no_grad():
                    err, st = solver_errors(y0, tr, rh, 0.0, sA, device, EPS_STOP, make=make)
                extra = dict(re_hat=rh)
                cost = dict(solver_steps=st_id, objective_evals=ev, forecast_steps=st, identify_seconds_per_state=ti / n)
        else:   # FNO arms
            if fno is None:
                fno = build(arm).to(device)
                fno.load_state_dict(torch.load(model_dir(arm, world, seed) / "best.pt", map_location=device))
                fno.eval()
            n_in = ARMS[arm][0]
            ctx = np.asarray(Y[PRE + k1 - n_in + 1:PRE + k1 + 1], dtype=np.float64).transpose(1, 0, 2, 3)
            err = rollout_errors(fno, ctx, tr, sc, sA)
        sec = time.time() - t0
        cost["wall_seconds_per_state"] = sec / n
        np.savez(f, err=err.astype(np.float32), **extra)
        with open(RES / f".eval_{panel}.lock", "w") as lk:
            fcntl.flock(lk, fcntl.LOCK_EX)
            meta = json.loads(resf.read_text()) if resf.exists() else {}
            meta[f.stem] = dict(arm=arm, seed=seed, variant=variant, window=lab, first=k0, last=k1, n=n, seconds=sec, **cost)
            resf.write_text(json.dumps(dict(meta, panel=panel, git_sha=config.git_sha()), indent=1, default=float))
        print(f"{panel} {arm} s{seed} {variant} {lab} {sec:.0f}s", flush=True)


if __name__ == "__main__":
    torch.set_num_threads(8)
    main(*sys.argv[1:6])
