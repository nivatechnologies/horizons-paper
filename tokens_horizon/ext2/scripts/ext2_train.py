"""EXT2 FSQ autoencoder training (ext2_freeze.yaml `training`).

Training pool: calibration fit (runs/cache/ext_kolmo/calib_fit.npy, 204,800 states) + training block (training.npy,
204,800 states); batches of 64 states drawn uniformly with replacement from the pool (numpy generator, seed 0).
Loss: mean over grid values of the squared error in units of sigma_A / 64 (= ||x - x_hat||^2 / sigma_A^2).
AdamW (lr 3e-4, betas 0.9/0.999, weight decay 0.01), cosine decay to 0 over the step budget, no warm-up, gradient
norm clipped at 1.0. Model seed 0. Validation (validation block, 6,400 states, checkpoint selection only) every
1,000 steps; the selected checkpoint minimizes validation loss. Divergence: a non-finite training loss, or a best
validation loss >= 1.0 (no better than predicting zero, the null); a diverged run is repeated once at lr 1e-4.

Usage: python ext2/scripts/ext2_train.py <config> <device> [steps] [lr] [tag]
"""
import json
import math
import sys
import time
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from fsq_ae import build, CONFIGS  # noqa: E402
from th import config  # noqa: E402
from th import kolmo_eval as E  # noqa: E402

OUT = config.RUNS / "ext2" / "train"
BATCH = 64
VAL_EVERY = 1000
AMP = None                # float32 throughout (timing pilot: bf16 autocast 15% faster; not used)


def pool():
    return [np.load(E.CACHE / "calib_fit.npy", mmap_mode="r").reshape(-1, 64, 64),
            np.load(E.CACHE / "training.npy", mmap_mode="r").reshape(-1, 64, 64)]


def batch_of(P, idx, scale):
    n0 = len(P[0])
    idx = np.sort(idx)
    a, b = idx[idx < n0], idx[idx >= n0] - n0
    x = np.concatenate([np.asarray(P[0][a], np.float32), np.asarray(P[1][b], np.float32)])
    return torch.from_numpy(x * scale)


def val_loss(model, V, device, scale):
    model.eval()
    tot = 0.0
    with torch.no_grad(), torch.autocast("cuda", dtype=AMP, enabled=AMP is not None):
        for i in range(0, len(V), 256):
            x = torch.from_numpy(np.asarray(V[i:i + 256], np.float32) * scale).to(device)
            y, _ = model(x)
            tot += float(((y.float() - x) ** 2).mean((1, 2)).sum())
    model.train()
    return tot / len(V)


def main(name, device, steps=30000, lr=3e-4, tag=""):
    assert name in CONFIGS
    torch.manual_seed(0)
    rng = np.random.default_rng(0)
    sA = E.sigma_A()
    scale = 64.0 / sA
    P = pool()
    n = sum(len(p) for p in P)
    V = np.load(E.CACHE / "validation.npy", mmap_mode="r").reshape(-1, 64, 64)
    model = build(name).to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=lr, betas=(0.9, 0.999), weight_decay=0.01)
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: 0.5 * (1 + math.cos(math.pi * min(s, steps) / steps)))
    d = OUT / f"{name}{tag}"
    if (d / "info.json").exists() or (d / "running").exists():
        raise FileExistsError(f"{d} already holds a run; use a fresh tag (frozen runs are never overwritten)")
    d.mkdir(parents=True, exist_ok=True)
    (d / "running").write_text(f"{time.time()}\n")
    logf = open(d / "train.log", "a")
    curve, best, best_step, diverged = [], float("inf"), None, False
    t0 = time.time()
    run_loss = 0.0
    for step in range(1, steps + 1):
        x = batch_of(P, rng.integers(0, n, BATCH), scale).to(device, non_blocking=True)
        with torch.autocast("cuda", dtype=AMP, enabled=AMP is not None):
            y, _ = model(x)
        loss = ((y.float() - x) ** 2).mean()
        if not torch.isfinite(loss):
            diverged = True
            logf.write(f"non-finite loss at step {step}\n")
            break
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        sched.step()
        run_loss += float(loss.detach())
        if step % VAL_EVERY == 0 or step == steps:
            vl = val_loss(model, V, device, scale)
            curve.append(dict(step=step, train_loss=run_loss / VAL_EVERY, val_loss=vl, seconds=time.time() - t0))
            run_loss = 0.0
            if vl < best:
                best, best_step = vl, step
                torch.save(model.state_dict(), d / "best.pt")
            logf.write(json.dumps(curve[-1]) + "\n")
            logf.flush()
    diverged = diverged or not best < 1.0
    info = dict(config=name, levels=CONFIGS[name][1], latent_side=CONFIGS[name][0], steps=steps, lr=lr, batch=BATCH,
                amp=str(AMP), params=model.param_counts(), train_seconds=time.time() - t0, best_val_loss=best,
                best_val_rel_rms=math.sqrt(best) if best < float("inf") else None, best_step=best_step,
                diverged=diverged, curve=curve, pool_states=n, git_sha=config.git_sha(),
                label="EXT2 learned-tokenizer kill test")
    (d / "info.json").write_text(json.dumps(info, indent=1))
    if not diverged:
        (d / "done").write_text("ok\n")
    (d / "running").unlink()
    print(name, "done", round(time.time() - t0), "s best val", best, "at", best_step, "diverged", diverged, flush=True)


if __name__ == "__main__":
    torch.set_num_threads(8)
    a = sys.argv
    main(a[1], a[2], int(a[3]) if len(a) > 3 else 30000, float(a[4]) if len(a) > 4 else 3e-4, a[5] if len(a) > 5 else "")
