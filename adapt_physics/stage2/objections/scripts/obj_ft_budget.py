"""L_ft at matched budgets (post-freeze request, Todd 2026-09-27; reported only, not a reading -> NUMBERS APFR-FTB).

World D Re 50 fresh panel (s2_test_Re50_D), first 100 states, w = 11. Base L0 seed 0. Per state: fine-tune on the
stage-1 pair rule (the w one-step pairs whose target is a window frame; inputs may be earlier observations; targets
are the noisy observations), AdamW weight decay 0, full batch, one-step MSE (ap/arms.finetune), for STEPS steps at
learning rate LR; then forecast from the 4 frames ending at k = w (stage-1 convention: stop once the state exceeds
0.3 sigma_A). Configurations: steps in {200, 1000, 7500} x lr in {1e-4, 1e-3}; every configuration reported (no
selection). Batch 1 by construction (one state at a time); wall time per state = fine-tuning + forecast, measured with
CUDA synchronization. Writes runs/obj_eval/ftb/L_ft_steps<S>_lr<LR>.npz and stage2/objections/results/ftb_<S>_<LR>.json.

Usage: python stage2/objections/scripts/obj_ft_budget.py <device> <steps> <lr>
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

HERE = Path(__file__).resolve()
PKG = HERE.parents[3]
sys.path.insert(0, str(PKG))
sys.path.insert(0, str(PKG / "scripts"))
from ap import config  # noqa: E402
from ap.arms import finetune  # noqa: E402
from ap.fno import build  # noqa: E402
from ap_eval import Truth, rollout_errors  # noqa: E402

PRE, W, N = 10, 11, 100
RES = PKG / "stage2" / "objections" / "results"
PANEL = "s2_test_Re50_D"


def main(device, steps, lr):
    steps, lr = int(steps), float(lr)
    tp = json.loads((PKG / "stage2" / "results" / "test_panels.json").read_text())[PANEL]
    sA, F = tp["sigma_A"], tp["F"]
    sc = 64.0 / json.loads((config.RESULTS / "chaos_gate.json").read_text())["Re40"]["sigma_A"]
    T = np.load(config.CACHE / f"{PANEL}.npy", mmap_mode="r")
    Y = np.load(config.CACHE / f"{PANEL}_obs.npy", mmap_mode="r")
    base = build("L0").to(device)
    base.load_state_dict(torch.load(config.RUNS / "train" / "L0" / "best.pt", map_location=device))
    base.eval()
    out = config.RUNS / "obj_eval" / "ftb"
    out.mkdir(parents=True, exist_ok=True)
    RES.mkdir(parents=True, exist_ok=True)
    errs, walls, fts, fcs = [], [], [], []
    sync = (lambda: torch.cuda.synchronize(device)) if device.startswith("cuda") else (lambda: None)
    for i in range(N):
        px = np.stack([np.asarray(Y[PRE + k - 4:PRE + k, i]) for k in range(1, W + 1)])
        py = np.stack([np.asarray(Y[PRE + k, i]) for k in range(1, W + 1)])
        sync()
        t0 = time.time()
        m = finetune(base, px, py, sc, steps=steps, lr=lr)
        sync()
        t1 = time.time()
        ctx = np.asarray(Y[PRE + W - 3:PRE + W + 1, i], dtype=np.float64)[None]
        errs.append(rollout_errors(m, ctx, Truth(T, W, F, idx=slice(i, i + 1)), sc, sA)[:, 0])
        sync()
        t2 = time.time()
        walls.append(t2 - t0)
        fts.append(t1 - t0)
        fcs.append(t2 - t1)
        del m
    err = np.stack(errs, 1)
    tag = f"steps{steps}_lr{lr:g}"
    np.savez(out / f"L_ft_{tag}.npz", err=err.astype(np.float32), wall=np.array(walls), finetune=np.array(fts), forecast=np.array(fcs))
    (RES / f"ftb_{tag}.json").write_text(json.dumps(dict(panel=PANEL, n=N, w=W, steps=steps, lr=lr, device=device,
                                                         wall_median=float(np.median(walls)), wall_p90=float(np.quantile(walls, 0.9)),
                                                         finetune_median=float(np.median(fts)), forecast_median=float(np.median(fcs)),
                                                         git_sha=config.git_sha()), indent=1))
    print(tag, "done; wall median", round(float(np.median(walls)), 2), flush=True)


if __name__ == "__main__":
    torch.set_num_threads(8)
    main(*sys.argv[1:4])
