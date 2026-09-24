"""Task 0.4 timing pilot: one arm-A model at 6 bits, Delta = 0.02, 1,000 steps (training block only)."""
import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import torch  # noqa: E402

from th import config  # noqa: E402
from th.learn import Task  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--arm", default="A")
ap.add_argument("--bits", type=int, default=6)
ap.add_argument("--delta", type=float, default=0.02)
ap.add_argument("--steps", type=int, default=1000)
ap.add_argument("--device", default="cuda:0")
ap.add_argument("--tag", default="")
a = ap.parse_args()
torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True
t = Task("lorenz28", a.arm, a.bits if a.arm != "C" else 0, a.delta, 0, a.device, steps=a.steps)
t0 = time.time()
m, info = t.train()
info["wall"] = time.time() - t0
info["sec_per_step"] = info["secs"] / a.steps
out = config.RUNS / "pilot" / f"pilot_{a.arm}_b{a.bits}_D{a.delta}{a.tag}.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(info, indent=1))
print(json.dumps({k: info[k] for k in ("sec_per_step", "best_val", "params", "train_flops")}))
