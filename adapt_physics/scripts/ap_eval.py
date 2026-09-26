"""Evaluate every arm on one test panel (after the freeze). For each window w in {3, 6, 11, 23}: the forecast starts from
the noisy observation at k = w; errors e_j = ||x_hat(w + j) - x(w + j)|| / sigma_A(test Re) for j = 0..F (row 0 = the
start frame), F = ceil(10 / (lambda_test * 0.35)). Integration / rollout stops once every state has exceeded 0.3 at
some j >= 1 (all first crossings at eps <= 0.3 fixed); later rows are +inf.

Online cost per arm and w: wall-clock seconds per state, solver integrator steps per state (identification + forecast)
or gradient steps per state. Writes runs/eval/Re<Re>/<arm>_w<w>.npz and results/eval/Re<Re>.json.

Usage: python scripts/ap_eval.py <Re> <device> [arm ...]
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ap import config  # noqa: E402
from ap.arms import finetune, identify, solver_errors  # noqa: E402
from ap.fno import ARMS, build  # noqa: E402

PRE, WS = 10, (3, 6, 11, 23)
ALL = ["persistence", "O", "P0", "P1", "P1x", "L0", "L0big", "L_range", "L_param_P1", "L_param_true", "L_ft"]
N_FT = 100
EPS_STOP = 0.3


class Truth:
    def __init__(self, T, w, F, idx=slice(None)):
        self.T, self.w, self.F, self.idx = T, w, F, idx

    def __call__(self, j):
        return np.asarray(self.T[PRE + self.w + j, self.idx], dtype=np.float64)


def load_model(arm, device):
    m = build(arm).to(device)
    m.load_state_dict(torch.load(config.RUNS / "train" / arm / "best.pt", map_location=device))
    return m.eval()


@torch.no_grad()
def rollout_errors(model, ctx, truth, sc, sA, re=None, bs=300):
    F = truth.F
    n = ctx.shape[0]
    dev = next(model.parameters()).device
    err = np.full((F + 1, n), np.inf)
    err[0] = np.sqrt(((ctx[:, -1] - truth(0)) ** 2).sum((-2, -1))) / sA
    h = torch.as_tensor(ctx * sc, dtype=torch.float32, device=dev)
    r = None if re is None else torch.as_tensor(re, device=dev)
    done = np.zeros(n, bool)
    for j in range(1, F + 1):
        p = torch.cat([model(h[i:i + bs], None if r is None else r[i:i + bs]) for i in range(0, n, bs)])
        e = np.sqrt(((p.double().cpu().numpy() / sc - truth(j)) ** 2).sum((-2, -1))) / sA
        err[j] = e
        done |= e > EPS_STOP
        if done.all():
            break
        h = torch.cat([h[:, 1:], p[:, None]], 1)
    return err


def main(Re, device, arms):
    Re = int(Re)
    fz = config.freeze()
    alpha = float(fz["drag"]["alpha"])
    info = json.loads((config.RESULTS / "test_panels.json").read_text())[f"Re{Re}"]
    sA, F = info["sigma_A"], info["F"]
    sc = 64.0 / json.loads((config.RESULTS / "chaos_gate.json").read_text())["Re40"]["sigma_A"]
    T = np.load(config.CACHE / f"test_Re{Re}.npy", mmap_mode="r")
    Y = np.load(config.CACHE / f"test_Re{Re}_obs.npy", mmap_mode="r")
    n = T.shape[1]
    out = config.RUNS / "eval" / f"Re{Re}"
    out.mkdir(parents=True, exist_ok=True)
    resf = config.RESULTS / "eval" / f"Re{Re}.json"
    resf.parent.mkdir(parents=True, exist_ok=True)
    meta = json.loads(resf.read_text()) if resf.exists() else {}
    models = {}
    for w in WS:
        tr = Truth(T, w, F)
        y0 = np.asarray(Y[PRE + w], dtype=np.float64)
        rehat = {}
        for arm in arms:
            f = out / f"{arm}_w{w}.npz"
            if f.exists():
                if arm in ("P1", "P1x"):
                    rehat[arm] = np.load(f)["re_hat"]
                continue
            t0 = time.time()
            extra, cost = {}, {}
            if arm == "persistence":
                err = np.stack([np.sqrt(((y0 - tr(j)) ** 2).sum((-2, -1))) / sA for j in range(F + 1)])
                cost = dict(solver_steps=0, gradient_steps=0)
            elif arm in ("O", "P0"):
                err, st = solver_errors(y0, tr, np.full(n, float(Re) if arm == "O" else 40.0),
                                        alpha if arm == "O" else 0.0, sA, device, EPS_STOP)
                cost = dict(solver_steps=0, gradient_steps=0, forecast_steps=st)
            elif arm in ("P1", "P1x"):
                a = alpha if arm == "P1x" else 0.0
                rh, ev, st_id = identify(np.asarray(Y[PRE + 1:PRE + w + 1]), w, a, sA, device)
                t_id = time.time() - t0
                rehat[arm] = rh
                err, st = solver_errors(y0, tr, rh, a, sA, device, EPS_STOP)
                extra = dict(re_hat=rh)
                cost = dict(solver_steps=st_id, objective_evals=ev, gradient_steps=0, forecast_steps=st,
                            identify_seconds_per_state=t_id / n)
            elif arm in ("L0", "L0big", "L_range", "L_param_P1", "L_param_true"):
                key = "L_param" if arm.startswith("L_param") else arm
                if key not in models:
                    models[key] = load_model(key, device)
                n_in = ARMS[key][0]
                ctx = np.asarray(Y[PRE + w - n_in + 1:PRE + w + 1], dtype=np.float64).transpose(1, 0, 2, 3)
                re = None
                if arm == "L_param_P1":
                    if "P1" not in rehat:
                        rehat["P1"] = np.load(out / f"P1_w{w}.npz")["re_hat"]
                    re = rehat["P1"]
                elif arm == "L_param_true":
                    re = np.full(n, float(Re))
                err = rollout_errors(models[key], ctx, tr, sc, sA, re)
                cost = dict(solver_steps=0, gradient_steps=0)
                if arm == "L_param_P1":
                    cost.update(solver_steps=30 * (w - 1) * 35, note="plus P1 identification")
            elif arm == "L_ft":
                if "L0" not in models:
                    models["L0"] = load_model("L0", device)
                errs = []
                for i in range(N_FT):
                    ks = range(1, w + 1)
                    px = np.stack([np.asarray(Y[PRE + k - 4:PRE + k, i]) for k in ks])
                    py = np.stack([np.asarray(Y[PRE + k, i]) for k in ks])
                    m = finetune(models["L0"], px, py, sc)
                    ctx = np.asarray(Y[PRE + w - 3:PRE + w + 1, i], dtype=np.float64)[None]
                    errs.append(rollout_errors(m, ctx, Truth(T, w, F, idx=slice(i, i + 1)), sc, sA)[:, 0])
                    del m
                err = np.stack(errs, 1)
                cost = dict(solver_steps=0, gradient_steps=200, pairs=w, n_states=N_FT)
            sec = time.time() - t0
            cost["wall_seconds_per_state"] = sec / err.shape[1]
            np.savez(f, err=err.astype(np.float32), **extra)
            meta[f"{arm}_w{w}"] = dict(arm=arm, w=w, n=int(err.shape[1]), seconds=sec, **cost)
            resf.write_text(json.dumps(dict(meta, Re=Re, sigma_A=sA, F=F, lam=info["lam"], git_sha=config.git_sha()),
                                       indent=1, default=float))
            print(f"Re{Re} {arm} w{w} {sec:.0f}s", flush=True)


if __name__ == "__main__":
    torch.set_num_threads(8)
    main(sys.argv[1], sys.argv[2], sys.argv[3:] or ALL)
