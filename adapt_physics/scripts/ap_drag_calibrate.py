"""Calibrate the truth's linear drag alpha at Re 40 so that drag carries 15% of the total enstrophy dissipation
(ap_freeze.yaml drag): share(alpha) = alpha <omega^2> / (alpha <omega^2> + (1/Re) <|grad omega|^2>), time- and
ensemble-averaged. Calibration block, stream 0: 64 random initial conditions, burn-in 300 tu, average over 300 tu
sampled every 1 tu. Secant iteration on share(alpha) - 0.15 to |error| < 0.002 (at most 8 evaluations).
Writes results/drag_calibration.json.

Usage: python scripts/ap_drag_calibrate.py <device>
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ap import config  # noqa: E402
from ap.solver import KolmoDrag  # noqa: E402

TARGET, B, BURN, AVG = 0.15, 64, 300.0, 300.0


def share(alpha, device):
    m = KolmoDrag(np.full(B, 40.0), alpha=alpha, device=device)
    wh = m.random_ic(np.random.default_rng(config.seed("calibration", 0)), B)
    wh = m.flow(wh, int(BURN / m.dt))
    v = d = 0.0
    for _ in range(int(AVG)):
        wh = m.flow(wh, 100)
        a, b = m.budget(wh)
        v += float(a.mean())
        d += float(b.mean())
    return d / (v + d), v / AVG, d / AVG


def main(device):
    t0 = time.time()
    hist = []
    a0, a1 = 0.0, 0.05
    s0 = share(a0, device)[0]
    hist.append(dict(alpha=a0, share=s0))
    for it in range(8):
        s1, v, d = share(a1, device)
        hist.append(dict(alpha=a1, share=s1, viscous=v, drag=d))
        print(hist[-1], round(time.time() - t0), flush=True)
        if abs(s1 - TARGET) < 0.002:
            break
        a0, a1, s0 = a1, max(1e-4, a1 + (TARGET - s1) * (a1 - a0) / (s1 - s0)), s1
    out = dict(alpha=hist[-1]["alpha"], share=hist[-1]["share"], target=TARGET, iterations=hist, B=B, burn=BURN,
               avg=AVG, seed=config.seed("calibration", 0), seconds=time.time() - t0, git_sha=config.git_sha(),
               definition="drag share of enstrophy dissipation alpha<w^2>/(alpha<w^2> + <|grad w|^2>/Re) at Re 40")
    config.RESULTS.mkdir(parents=True, exist_ok=True)
    (config.RESULTS / "drag_calibration.json").write_text(json.dumps(out, indent=1))
    print("alpha", out["alpha"], "share", out["share"])


if __name__ == "__main__":
    torch.set_num_threads(8)
    main(sys.argv[1])
