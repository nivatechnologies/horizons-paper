"""Pivot evaluation (pivot/pv_freeze.yaml arms) on one world and test Re; stage-1 conventions (scripts/ap_eval.py):
forecast from the noisy observation at k = w, errors on future frames, integration/rollout stops once every state has
exceeded 0.3. World D at Re 36/40/44/50 reuses the stage-1 panels and the stage-1 evaluations of O, P1, P1x,
persistence, L0, L_range and L0-big (identical computations); only H and H_true run here. World D Re 56 and World C
run every arm.

Arms: persistence; O (truth family: drag, plus beta in World C; true Re); P1 (no-drag family, golden-section on [25, 70],
30 evaluations, as stage 1); P1x (truth family with Re identified, as P1); H (hybrid, Re identified on the hybrid by the
same search widened to [25, 80]); H_true (hybrid at the true Re); L0, L_range (World C: retrained L0_C, L_range_C);
L0big (World D only). Writes runs/pivot_eval/<world>/Re<Re>/<arm>_w<w>.npz and pivot/results/eval_<world>_Re<Re>.json.

Usage: python pivot/scripts/pv_eval.py <D|C> <Re> <device> [arm ...]
"""
import fcntl
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from ap import config  # noqa: E402
from ap.arms import identify, solver_errors  # noqa: E402
from ap.fno import ARMS, build  # noqa: E402
from ap_eval import Truth, rollout_errors  # noqa: E402
from hybrid import Correction, HybridSolver  # noqa: E402

PRE, WS, EPS_STOP = 10, (3, 6, 11, 23), 0.3
RES = config.PKG / "pivot" / "results"
ALL = ["persistence", "O", "P1", "P1x", "H", "H_true", "L0", "L_range", "L0big"]


def sigma40(world):
    if world == "D":
        return json.loads((config.RESULTS / "chaos_gate.json").read_text())["Re40"]["sigma_A"]
    return json.loads((RES / "chaos_gate_C.json").read_text())["Re40"]["sigma_A"]


def main(world, Re, device, arms):
    Re = int(Re)
    sfx = "" if world == "D" else "_C"
    alpha = float(config.freeze()["drag"]["alpha"])
    beta = 0.0 if world == "D" else float(json.loads((RES / "beta_calibration.json").read_text())["beta"])
    if world == "D" and Re != 56:
        info = json.loads((config.RESULTS / "test_panels.json").read_text())[f"Re{Re}"]
    else:
        info = json.loads((RES / f"test_panels_{world}.json").read_text())[f"Re{Re}"]
    sA, F = info["sigma_A"], info["F"]
    s40 = sigma40(world)
    sc = 64.0 / s40
    T = np.load(config.CACHE / f"test_Re{Re}{sfx}.npy", mmap_mode="r")
    Y = np.load(config.CACHE / f"test_Re{Re}{sfx}_obs.npy", mmap_mode="r")
    n = T.shape[1]
    out = config.RUNS / "pivot_eval" / world / f"Re{Re}"
    out.mkdir(parents=True, exist_ok=True)
    resf = RES / f"eval_{world}_Re{Re}.json"
    g = None
    models = {}
    for w in WS:
        tr = Truth(T, w, F)
        y0 = np.asarray(Y[PRE + w], dtype=np.float64)
        for arm in arms:
            f = out / f"{arm}_w{w}.npz"
            if f.exists():
                continue
            t0 = time.time()
            extra, cost = {}, {}
            if arm == "persistence":
                err = np.stack([np.sqrt(((y0 - tr(j)) ** 2).sum((-2, -1))) / sA for j in range(F + 1)])
                cost = dict(solver_steps=0, gradient_steps=0)
            elif arm == "O":
                err, st = solver_errors(y0, tr, np.full(n, float(Re)), alpha, sA, device, EPS_STOP, beta=beta)
                cost = dict(solver_steps=0, forecast_steps=st, gradient_steps=0)
            elif arm in ("P1", "P1x"):
                a, b = (alpha, beta) if arm == "P1x" else (0.0, 0.0)
                rh, ev, st_id = identify(np.asarray(Y[PRE + 1:PRE + w + 1]), w, a, sA, device, beta=b)
                ti = time.time() - t0
                err, st = solver_errors(y0, tr, rh, a, sA, device, EPS_STOP, beta=b)
                extra = dict(re_hat=rh)
                cost = dict(solver_steps=st_id, objective_evals=ev, forecast_steps=st, gradient_steps=0,
                            identify_seconds_per_state=ti / n)
            elif arm in ("H", "H_true"):
                if g is None:
                    g = Correction(sc).to(device)
                    g.load_state_dict(torch.load(config.RUNS / "train" / f"H_{world}" / "best.pt", map_location=device))
                    g.eval()
                make = lambda re: HybridSolver(re, g, device=device)   # noqa: E731
                if arm == "H":
                    with torch.no_grad():
                        rh, ev, st_id = identify(np.asarray(Y[PRE + 1:PRE + w + 1]), w, 0.0, sA, device, lo=25.0, hi=80.0,
                                                 make=make)
                    ti = time.time() - t0
                    extra = dict(re_hat=rh)
                    cost = dict(solver_steps=st_id, objective_evals=ev, identify_seconds_per_state=ti / n)
                else:
                    rh = np.full(n, float(Re))
                with torch.no_grad():
                    err, st = solver_errors(y0, tr, rh, 0.0, sA, device, EPS_STOP, make=make)
                cost.update(forecast_steps=st, gradient_steps=0)
            elif arm in ("L0", "L_range", "L0big"):
                key = arm + sfx
                if key not in models:
                    m = build(arm).to(device)
                    m.load_state_dict(torch.load(config.RUNS / "train" / key / "best.pt", map_location=device))
                    models[key] = m.eval()
                n_in = ARMS[arm][0]
                ctx = np.asarray(Y[PRE + w - n_in + 1:PRE + w + 1], dtype=np.float64).transpose(1, 0, 2, 3)
                err = rollout_errors(models[key], ctx, tr, sc, sA)
                cost = dict(solver_steps=0, gradient_steps=0)
            sec = time.time() - t0
            cost["wall_seconds_per_state"] = sec / err.shape[1]
            np.savez(f, err=err.astype(np.float32), **extra)
            with open(RES / f".eval_{world}_Re{Re}.lock", "w") as lk:
                fcntl.flock(lk, fcntl.LOCK_EX)
                meta = json.loads(resf.read_text()) if resf.exists() else {}
                meta[f"{arm}_w{w}"] = dict(arm=arm, w=w, n=int(err.shape[1]), seconds=sec, **cost)
                resf.write_text(json.dumps(dict(meta, world=world, Re=Re, sigma_A=sA, F=F, lam=info["lam"], beta=beta,
                                                git_sha=config.git_sha()), indent=1, default=float))
            print(f"{world} Re{Re} {arm} w{w} {sec:.0f}s", flush=True)


if __name__ == "__main__":
    torch.set_num_threads(8)
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:] or ALL)
