"""Train one learned arm (ap_freeze.yaml learned): L0, L0big (nominal Re 40 data), L_range, L_param (Re ~ U[34, 46]).

Samples: a trajectory and a start k uniformly; inputs = frames k .. k+n_in-1 (+2% sigma_A(Re 40) white noise per
frame, as the observations), targets = the next 4 clean frames. Fields scaled by 64 / sigma_A(Re 40).
Loss = one-step MSE + mean over a 4-step unrolled rollout (predictions fed back) of the per-step MSE.
AdamW lr 1e-3, weight decay 1e-4, cosine decay to 0, no warm-up, gradient-norm clip 1.0, batch 32, seed 0
(stage 2: seeds 1 and 2 via the seed argument; seed s sets torch.manual_seed(s) and the sampling generator).
Validation every 1,000 steps on 512 fixed validation windows (fixed noise); checkpoint = minimum validation loss.
A run directory that already holds a run is never reused.

Usage: python scripts/ap_train.py <arm> <device> [steps|-] [seed]
"""
import json
import math
import sys
import time
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ap import config  # noqa: E402
from ap.fno import ARMS, build  # noqa: E402

OUT = config.RUNS / "train"
BATCH, UNROLL, VAL_EVERY = 32, 4, 1000
STEPS = {"L0": 30000, "L0big": 60000, "L_range": 30000, "L_param": 30000, "L_range_wide": 30000}


def scale(world="D"):
    if world == "C":     # pivot World C: its own sigma_A(Re 40)
        return 64.0 / json.loads((config.PKG / "pivot" / "results" / "chaos_gate_C.json").read_text())["Re40"]["sigma_A"]
    return 64.0 / json.loads((config.RESULTS / "chaos_gate.json").read_text())["Re40"]["sigma_A"]


def windows(X, re, idx_traj, k0, n_in, noise, sc, device):
    fr = np.stack([np.asarray(X[i, k:k + n_in + UNROLL]) for i, k in zip(idx_traj, k0)]).astype(np.float32) * sc
    x = torch.from_numpy(fr[:, :n_in] + noise).to(device)
    y = torch.from_numpy(fr[:, n_in:]).to(device)
    return x, y, torch.as_tensor(re[idx_traj], device=device)


def loss_fn(model, x, y, r):
    losses = []
    h = x
    for k in range(UNROLL):
        p = model(h, r)
        losses.append(((p - y[:, k]) ** 2).mean())
        h = torch.cat([h[:, 1:], p[:, None]], 1)
    return losses[0] + sum(losses) / UNROLL


def main(arm, device, steps=None, seed=0):
    base, world = (arm[:-2], "C") if arm.endswith("_C") else (arm, "D")      # pivot: <arm>_C = World C data
    steps = steps or STEPS[base]
    n_in, _, _, data = ARMS[base]
    data = data + ("_C" if world == "C" else "")
    d = OUT / (arm if seed == 0 else f"{arm}_s{seed}")          # stage 2: seeds 1, 2 in <arm>_s<seed>
    if (d / "info.json").exists() or (d / "running").exists():
        raise FileExistsError(f"{d} already holds a run")
    d.mkdir(parents=True, exist_ok=True)
    (d / "running").write_text(f"{time.time()}\n")
    torch.manual_seed(seed)
    rng = np.random.default_rng(seed)
    sc = scale(world)
    X = np.load(config.CACHE / f"train_{data}.npy", mmap_mode="r")
    R = np.load(config.CACHE / f"train_{data}_re.npy")
    V = np.load(config.CACHE / f"val_{data}.npy", mmap_mode="r")
    RV = np.load(config.CACHE / f"val_{data}_re.npy")
    nt, nf = X.shape[:2]
    vr = np.random.default_rng(1)
    vt = vr.integers(0, V.shape[0], 512)
    vk = vr.integers(0, V.shape[1] - n_in - UNROLL + 1, 512)
    vnoise = (vr.standard_normal((512, n_in, 64, 64)) * 0.02).astype(np.float32)
    model = build(base).to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: 0.5 * (1 + math.cos(math.pi * min(s, steps) / steps)))
    logf = open(d / "train.log", "a")
    best, best_step, curve, t0, run = float("inf"), None, [], time.time(), 0.0
    for step in range(1, steps + 1):
        it = rng.integers(0, nt, BATCH)
        k0 = rng.integers(0, nf - n_in - UNROLL + 1, BATCH)
        noise = (rng.standard_normal((BATCH, n_in, 64, 64)) * 0.02).astype(np.float32)
        x, y, r = windows(X, R, it, k0, n_in, noise, sc, device)
        loss = loss_fn(model, x, y, r)
        if not torch.isfinite(loss):
            logf.write(f"non-finite loss at step {step}\n")
            break
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        sched.step()
        run += float(loss.detach())
        if step % VAL_EVERY == 0 or step == steps:
            model.eval()
            vl = 0.0
            with torch.no_grad():
                for i in range(0, 512, 64):
                    x, y, r = windows(V, RV, vt[i:i + 64], vk[i:i + 64], n_in, vnoise[i:i + 64], sc, device)
                    vl += float(loss_fn(model, x, y, r)) * len(x)
            model.train()
            vl /= 512
            curve.append(dict(step=step, train_loss=run / VAL_EVERY, val_loss=vl, seconds=time.time() - t0))
            run = 0.0
            if vl < best:
                best, best_step = vl, step
                torch.save(model.state_dict(), d / "best.pt")
            logf.write(json.dumps(curve[-1]) + "\n")
            logf.flush()
    info = dict(arm=arm, n_in=n_in, width=ARMS[base][1], re_channel=ARMS[base][2], data=data, world=world, params=model.n_params(),
                steps=steps, batch=BATCH, unroll=UNROLL, train_seconds=time.time() - t0, best_val=best,
                best_step=best_step, gradient_steps=steps, curve=curve, seed=seed, git_sha=config.git_sha())
    (d / "info.json").write_text(json.dumps(info, indent=1))
    (d / "running").unlink()
    print(arm, "done", round(time.time() - t0), "best", best, "at", best_step, flush=True)


if __name__ == "__main__":
    torch.set_num_threads(8)
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3] != "-" else None,
         int(sys.argv[4]) if len(sys.argv) > 4 else 0)
