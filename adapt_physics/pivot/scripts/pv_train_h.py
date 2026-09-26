"""Train the hybrid's correction g_theta (pivot/pv_freeze.yaml hybrid) for one world on nominal Re 40 truth data only
(train_nominal[_C]: the data the frozen FNO L0 had), by matching short rollouts through the solver.

Sample: a trajectory and frame k uniformly; start = frame k + 2% sigma_A(Re 40) white noise (as the observations),
projected by the solver; roll the hybrid (no-drag physics at Re 40 + g_theta, IFRK4 dt 0.01, float32) for 1 frame
(35 steps, 0.35 tu) with gradient checkpointing per step; loss = mean ||x_hat - x_{k+1}||^2 / sigma_A(Re 40)^2.
AdamW lr 1e-3, weight decay 1e-4, cosine to 0, no warm-up, clip 1.0, batch 64, 2,000 steps, seed 0. Validation every
100 steps on 64 fixed windows of val_nominal[_C] (fixed noise), same loss; checkpoint = minimum validation loss;
step 0 (pure physics, zero-initialized output) is evaluated and recorded.

Usage: python pivot/scripts/pv_train_h.py <D|C> <device>
"""
import json
import math
import sys
import time
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ap import config  # noqa: E402
from hybrid import Correction, HybridSolver  # noqa: E402

STEPS, BATCH, VAL_EVERY, NVAL = 2000, 64, 100, 64


def sigma40(world):
    if world == "D":
        return json.loads((config.RESULTS / "chaos_gate.json").read_text())["Re40"]["sigma_A"]
    return json.loads((config.PKG / "pivot" / "results" / "chaos_gate_C.json").read_text())["Re40"]["sigma_A"]


def main(world, device):
    sfx = "" if world == "D" else "_C"
    d = config.RUNS / "train" / f"H_{world}"
    if (d / "info.json").exists() or (d / "running").exists():
        raise FileExistsError(d)
    d.mkdir(parents=True, exist_ok=True)
    (d / "running").write_text(f"{time.time()}\n")
    torch.manual_seed(0)
    rng = np.random.default_rng(0)
    sA = sigma40(world)
    X = np.load(config.CACHE / f"train_nominal{sfx}.npy", mmap_mode="r")
    V = np.load(config.CACHE / f"val_nominal{sfx}.npy", mmap_mode="r")
    g = Correction(64.0 / sA).to(device)
    m = HybridSolver(np.full(BATCH, 40.0), g, device=device, ckpt=True)
    mv = HybridSolver(np.full(NVAL, 40.0), g, device=device, ckpt=False)
    vr = np.random.default_rng(1)
    vt, vk = vr.integers(0, V.shape[0], NVAL), vr.integers(0, V.shape[1] - 1, NVAL)
    vx = torch.as_tensor(np.stack([V[i, k] for i, k in zip(vt, vk)]) + vr.standard_normal((NVAL, 64, 64)) * 0.02 * sA / 64,
                         dtype=torch.float32, device=device)
    vy = torch.as_tensor(np.stack([V[i, k + 1] for i, k in zip(vt, vk)]), dtype=torch.float32, device=device)
    opt = torch.optim.AdamW(g.parameters(), lr=1e-3, weight_decay=1e-4)
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: 0.5 * (1 + math.cos(math.pi * min(s, STEPS) / STEPS)))
    logf = open(d / "train.log", "a")

    def val():
        g.eval()
        with torch.no_grad():
            p = mv.to_phys(mv.flow(mv.to_spec(vx), 35))
            v = float((((p - vy) ** 2).sum((-2, -1)) / sA ** 2).mean())
        g.train()
        return v

    v0 = val()
    best, best_step, curve, t0, run = v0, 0, [dict(step=0, val_loss=v0)], time.time(), 0.0
    torch.save(g.state_dict(), d / "best.pt")
    for step in range(1, STEPS + 1):
        it, k = rng.integers(0, X.shape[0], BATCH), rng.integers(0, X.shape[1] - 1, BATCH)
        x = torch.as_tensor(np.stack([X[i, j] for i, j in zip(it, k)]) + rng.standard_normal((BATCH, 64, 64)) * 0.02 * sA / 64,
                            dtype=torch.float32, device=device)
        y = torch.as_tensor(np.stack([X[i, j + 1] for i, j in zip(it, k)]), dtype=torch.float32, device=device)
        p = m.to_phys(m.flow(m.to_spec(x), 35))
        loss = (((p - y) ** 2).sum((-2, -1)) / sA ** 2).mean()
        if not torch.isfinite(loss):
            logf.write(f"non-finite loss at step {step}\n")
            break
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(g.parameters(), 1.0)
        opt.step()
        sched.step()
        run += float(loss.detach())
        if step % VAL_EVERY == 0 or step == STEPS:
            v = val()
            curve.append(dict(step=step, train_loss=run / VAL_EVERY, val_loss=v, seconds=time.time() - t0))
            run = 0.0
            if v < best:
                best, best_step = v, step
                torch.save(g.state_dict(), d / "best.pt")
            logf.write(json.dumps(curve[-1]) + "\n")
            logf.flush()
    info = dict(arm=f"H_{world}", world=world, params=g.n_params(), steps=STEPS, batch=BATCH, rollout_frames=1,
                solver_steps_per_sample=35, train_seconds=time.time() - t0, val_loss_pure_physics=v0, best_val=best,
                best_step=best_step, curve=curve, training_conditions=1, training_states=int(X.shape[0] * X.shape[1]),
                git_sha=config.git_sha())
    (d / "info.json").write_text(json.dumps(info, indent=1))
    (d / "running").unlink()
    print("H", world, "done", round(time.time() - t0), "pure-physics val", v0, "best", best, "at", best_step, flush=True)


if __name__ == "__main__":
    torch.set_num_threads(8)
    main(sys.argv[1], sys.argv[2])
