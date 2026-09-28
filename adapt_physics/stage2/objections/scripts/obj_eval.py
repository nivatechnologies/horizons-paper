"""Objections WO evaluations (obj_freeze.yaml). Stage-2 conventions (stage2/scripts/s2_eval.py): forecast from the noisy
observation at the window's last frame k = w, window frames 1..w, errors on future frames, stop once every state has
exceeded 0.3.

Usage: python stage2/objections/scripts/obj_eval.py <panel> <device> <arm> <seed> <windows>
  panel    obj_V_Re50 (World V) | s2_test_Re<Re>_<D|C> (Part A fresh panels)
  arm      O_V | P1x_V | H | H_true | L_range_V | L0 | FNO_Re_true | FNO_Re_id | FNOw_Re_true | FNOw_Re_id | L_ft
           (FNOw: post-freeze request, the L_param recipe trained on Re ~ U[30, 60] data, World D, seed 0)
  windows  comma list of w (e.g. 3,6,11,23)
Part 2 identification through the network (FNO_Re_id): golden-section on Re in [25, 80], exactly 30 evaluations (the
same routine as ap/arms.identify); misfit = mean over scored frames of ||x_hat - y||^2 / sigma_A^2 where x_hat is the
network's autoregressive rollout at the candidate Re.
  - w >= n_in + 1 (= 5): inputs = window frames 1..4; scored frames 5..w.
  - w <  n_in + 1: inputs = the 4 observed frames ending at frame 1 (frames -2..1, pre-change frames included);
    scored frames 2..w.
Writes runs/obj_eval/<panel>/<arm>_s<seed>_<w>.npz and stage2/objections/results/eval_<panel>.json.
"""
import fcntl
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

HERE = Path(__file__).resolve()
PKG = HERE.parents[3]
sys.path.insert(0, str(PKG))
sys.path.insert(0, str(PKG / "pivot"))
sys.path.insert(0, str(PKG / "scripts"))
from ap import config  # noqa: E402
from ap.arms import GOLD, finetune, identify, solver_errors  # noqa: E402
from ap.fno import ARMS, build  # noqa: E402
from ap.solver import KolmoDrag  # noqa: E402
from ap_eval import Truth, rollout_errors  # noqa: E402
from hybrid import Correction, HybridSolver  # noqa: E402

PRE, EPS_STOP, N_IN_P = 10, 0.3, 4
RES = config.PKG / "stage2" / "objections" / "results"
S2R = config.PKG / "stage2" / "results"


def sigma40(world):
    if world in ("D", "V"):
        return json.loads((config.RESULTS / "chaos_gate.json").read_text())["Re40"]["sigma_A"]
    return json.loads((config.PKG / "pivot" / "results" / "chaos_gate_C.json").read_text())["Re40"]["sigma_A"]


def model_dir(name, seed):
    return config.RUNS / "train" / (name if seed == 0 else f"{name}_s{seed}")


def gss(obj, n, lo=25.0, hi=80.0, n_eval=30):
    """The golden-section routine of ap/arms.identify, for an arbitrary per-state objective obj(re (n,)) -> (n,)."""
    a, b = np.full(n, lo), np.full(n, hi)
    c, d = b - GOLD * (b - a), a + GOLD * (b - a)
    fc, fd = obj(c), obj(d)
    ev = 2
    while ev < n_eval:
        left = fc < fd
        b = np.where(left, d, b)
        a = np.where(left, a, c)
        c_new = np.where(left, b - GOLD * (b - a), d)
        d_new = np.where(left, c, a + GOLD * (b - a))
        f_new = obj(np.where(left, c_new, d_new))
        fc, fd = np.where(left, f_new, fd), np.where(left, fc, f_new)
        c, d = c_new, d_new
        ev += 1
    return 0.5 * (a + b), ev


@torch.no_grad()
def fno_misfit(model, Y, w, re, sc, sA, bs=300):
    """Y: observations indexed Y[PRE + k] (k from -10). Pinned rule in the module docstring."""
    dev = next(model.parameters()).device
    if w >= N_IN_P + 1:
        k_in, scored = list(range(1, N_IN_P + 1)), list(range(N_IN_P + 1, w + 1))
    else:
        k_in, scored = list(range(2 - N_IN_P, 2)), list(range(2, w + 1))
    n = Y.shape[1]
    tot = np.zeros(n)
    for i in range(0, n, bs):
        h = torch.as_tensor(np.stack([Y[PRE + k, i:i + bs] for k in k_in], 1) * sc, dtype=torch.float32, device=dev)
        r = torch.as_tensor(re[i:i + bs], device=dev)
        for k in range(k_in[-1] + 1, scored[-1] + 1):
            p = model(h, r)
            if k in scored:
                tot[i:i + bs] += (((p.double().cpu().numpy() / sc - Y[PRE + k, i:i + bs]) ** 2).sum((-2, -1)))
            h = torch.cat([h[:, 1:], p[:, None]], 1)
    return tot / len(scored) / sA ** 2


def main(panel, device, arm, seed, windows):
    seed = int(seed)
    tpf = RES / "test_panels.json" if panel.startswith("obj_") else S2R / "test_panels.json"
    tp = json.loads(tpf.read_text())[panel]
    world, Re = tp["world"], int(tp["Re"])
    a0 = float(config.freeze()["drag"]["alpha"])
    beta = float(tp.get("beta", 0.0))
    sA, F = tp["sigma_A"], tp["F"]
    sc = 64.0 / sigma40(world)
    T = np.load(config.CACHE / f"{panel}.npy", mmap_mode="r")
    Yall = np.load(config.CACHE / f"{panel}_obs.npy", mmap_mode="r")
    n = T.shape[1]
    out = config.RUNS / "obj_eval" / panel
    out.mkdir(parents=True, exist_ok=True)
    RES.mkdir(parents=True, exist_ok=True)
    resf = RES / f"eval_{panel}.json"
    g = fno = base_l0 = None
    for w in [int(x) for x in windows.split(",")]:
        f = out / f"{arm}_s{seed}_{w}.npz"
        if f.exists():
            continue
        t0 = time.time()
        tr = Truth(T, w, F)
        y0 = np.asarray(Yall[PRE + w], dtype=np.float64)
        Yw = np.asarray(Yall[PRE + 1:PRE + w + 1])
        extra, cost = {}, {}
        if arm == "O_V":
            make = lambda re: KolmoDrag(re, alpha=a0, alpha_ref_re=40.0, device=device)  # noqa: E731
            err, st = solver_errors(y0, tr, np.full(n, float(Re)), 0.0, sA, device, EPS_STOP, make=make)
            cost = dict(forecast_steps=st)
        elif arm == "P1x_V":
            make = lambda re: KolmoDrag(re, alpha=a0, alpha_ref_re=40.0, device=device)  # noqa: E731
            rh, ev, st_id = identify(Yw, w, 0.0, sA, device, make=make)
            ti = time.time() - t0
            err, st = solver_errors(y0, tr, rh, 0.0, sA, device, EPS_STOP, make=make)
            extra, cost = dict(re_hat=rh), dict(objective_evals=ev, solver_steps=st_id, forecast_steps=st,
                                                identify_seconds_per_state=ti / n)
        elif arm in ("H", "H_true"):
            if g is None:
                g = Correction(sc).to(device)
                g.load_state_dict(torch.load(model_dir("H_D", seed) / "best.pt", map_location=device))   # World D correction
                g.eval()
            make = lambda re: HybridSolver(re, g, device=device)  # noqa: E731
            if arm == "H":
                with torch.no_grad():
                    rh, ev, st_id = identify(Yw, w, 0.0, sA, device, lo=25.0, hi=80.0, make=make)
                extra, cost = dict(re_hat=rh), dict(objective_evals=ev, solver_steps=st_id,
                                                    identify_seconds_per_state=(time.time() - t0) / n)
            else:
                rh = np.full(n, float(Re))
            with torch.no_grad():
                err, st = solver_errors(y0, tr, rh, 0.0, sA, device, EPS_STOP, make=make)
            cost["forecast_steps"] = st
        elif arm in ("L_range_V", "L0"):
            if fno is None:
                name = arm if arm == "L_range_V" else ("L0" if world in ("D", "V") else "L0_C")
                fno = build("L_range" if arm == "L_range_V" else "L0").to(device)
                fno.load_state_dict(torch.load(model_dir(name, seed) / "best.pt", map_location=device))
                fno.eval()
            n_in = 8 if arm == "L_range_V" else 4
            ctx = np.asarray(Yall[PRE + w - n_in + 1:PRE + w + 1], dtype=np.float64).transpose(1, 0, 2, 3)
            err = rollout_errors(fno, ctx, tr, sc, sA)
        elif arm in ("FNO_Re_true", "FNO_Re_id", "FNOw_Re_true", "FNOw_Re_id"):
            if fno is None:
                name = "L_param_wide" if arm.startswith("FNOw") else ("L_param" if world == "D" else "L_param_C")
                fno = build("L_param").to(device)      # same architecture; FNOw = L_param recipe on Re 30-60 data
                fno.load_state_dict(torch.load(model_dir(name, seed) / "best.pt", map_location=device))
                fno.eval()
            if arm.endswith("_id"):
                rh, ev = gss(lambda re: fno_misfit(fno, Yall, w, re, sc, sA), n)
                extra, cost = dict(re_hat=rh), dict(objective_evals=ev, identify_seconds_per_state=(time.time() - t0) / n)
            else:
                rh = np.full(n, float(Re))
            ctx = np.asarray(Yall[PRE + w - 3:PRE + w + 1], dtype=np.float64).transpose(1, 0, 2, 3)
            err = rollout_errors(fno, ctx, tr, sc, sA, re=rh)
        elif arm == "L_ft":
            if base_l0 is None:
                base_l0 = build("L0").to(device)
                base_l0.load_state_dict(torch.load(model_dir("L0", 0) / "best.pt", map_location=device))
                base_l0.eval()
            errs = []
            for i in range(n):
                px = np.stack([np.asarray(Yall[PRE + k - 4:PRE + k, i]) for k in range(1, w + 1)])
                py = np.stack([np.asarray(Yall[PRE + k, i]) for k in range(1, w + 1)])
                m = finetune(base_l0, px, py, sc)
                ctx = np.asarray(Yall[PRE + w - 3:PRE + w + 1, i], dtype=np.float64)[None]
                errs.append(rollout_errors(m, ctx, Truth(T, w, F, idx=slice(i, i + 1)), sc, sA)[:, 0])
                del m
            err = np.stack(errs, 1)
            cost = dict(gradient_steps=200, pairs=w)
        sec = time.time() - t0
        cost["wall_seconds_per_state"] = sec / n
        np.savez(f, err=err.astype(np.float32), **extra)
        with open(RES / f".eval_{panel}.lock", "w") as lk:
            fcntl.flock(lk, fcntl.LOCK_EX)
            meta = json.loads(resf.read_text()) if resf.exists() else {}
            meta[f.stem] = dict(arm=arm, seed=seed, window=w, n=n, seconds=sec, **cost)
            resf.write_text(json.dumps(dict(meta, panel=panel, git_sha=config.git_sha()), indent=1, default=float))
        print(f"{panel} {arm} s{seed} w{w} {sec:.0f}s", flush=True)


if __name__ == "__main__":
    torch.set_num_threads(8)
    main(*sys.argv[1:6])
