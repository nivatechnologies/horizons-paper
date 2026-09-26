"""Calibrate the Codex term's magnitude (pivot/CODEX_MISMATCH.md): starting at beta_T = +3.35, tune beta_T (same sign)
until |eta(beta)/eta(0) - 1| = 0.125 +- 0.005 at Re 40 with drag alpha, where eta = <nu |grad omega|^2> is averaged
over the ensemble and over time. Protocol as the stage-1 drag calibration: calibration block stream 0, 64 trajectories,
300-tu burn-in, 300-tu average sampled every 1 tu. Secant iteration on |r - 1| - 0.125 (at most 8 evaluations).
Writes pivot/results/beta_calibration.json.

Usage: python pivot/scripts/pv_beta_calibrate.py <device>
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from ap import config  # noqa: E402
from ap.solver import KolmoDrag  # noqa: E402

B, BURN, AVG, TARGET, TOL = 64, 300.0, 300.0, 0.125, 0.005
OUT = config.PKG / "pivot" / "results"


def eta(beta, alpha, device):
    m = KolmoDrag(np.full(B, 40.0), alpha=alpha, beta=beta, device=device)
    wh = m.random_ic(np.random.default_rng(config.seed("calibration", 0)), B)
    wh = m.flow(wh, int(BURN / m.dt))
    v = 0.0
    for _ in range(int(AVG)):
        wh = m.flow(wh, 100)
        v += float(m.budget(wh)[0].mean())
    return v / AVG


def main(device):
    alpha = float(config.freeze()["drag"]["alpha"])
    t0 = time.time()
    e0 = eta(0.0, alpha, device)
    hist = [dict(beta=0.0, eta=e0)]
    b0, f0 = 0.0, -TARGET
    b1 = 3.35
    for _ in range(8):
        e1 = eta(b1, alpha, device)
        f1 = abs(e1 / e0 - 1) - TARGET
        hist.append(dict(beta=b1, eta=e1, rel_change=e1 / e0 - 1))
        print(hist[-1], round(time.time() - t0), flush=True)
        if abs(f1) <= TOL:
            break
        b0, b1, f0 = b1, max(0.05, b1 - f1 * (b1 - b0) / (f1 - f0)), f1
    out = dict(beta=hist[-1]["beta"], rel_change=hist[-1]["rel_change"], eta0=e0, target=TARGET, tol=TOL, alpha=alpha,
               iterations=hist, start=3.35, B=B, burn=BURN, avg=AVG, seed=config.seed("calibration", 0),
               converged=abs(abs(hist[-1]["rel_change"]) - TARGET) <= TOL, seconds=time.time() - t0,
               git_sha=config.git_sha())
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "beta_calibration.json").write_text(json.dumps(out, indent=1))
    print("beta", out["beta"], "rel", out["rel_change"])


if __name__ == "__main__":
    torch.set_num_threads(8)
    main(sys.argv[1])
