"""Part 3 edge timing (obj_freeze.yaml part3): the same code, weights and settings as the datacenter runs, FP32 solver
arms as in the datacenter (O float64, hybrid float32), batch 1, no TensorRT. World D, Re 50, w = 11; states 0..22 of the
Part A fresh panel (a slice file made by `slice` mode): states 0-2 warm-up, 3-22 timed.

Per arm and state: wall time (CUDA-synchronized), forecast frames and throughput, torch peak memory; H and FNO_Re_id
time identification and forecast separately; L_ft times fine-tuning (200 steps) and forecast. Board power: tegrastats
(--interval 100) read by a thread that timestamps every line; mean VDD_IN over each arm's timed interval and energy per
state = mean power x mean wall time. Horizons (eps 0.1, future frames) are saved per state for the correctness check.

Usage: python edge_time.py slice                       (datacenter: write runs/cache/edge_slice.npz)
       python edge_time.py run <device> <out.json> [arms] [fixed]   (Orin or datacenter)
With `fixed`, early stopping is disabled and every arm forecasts the same fixed number of frames: the full scoring window
F (111 frames at Re 50 = 10 Lyapunov times), so wall time and frames per second are comparable across arms.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path

import numpy as np
import torch

HERE = Path(__file__).resolve()
PKG = HERE.parents[3]
sys.path.insert(0, str(PKG))
sys.path.insert(0, str(PKG / "pivot"))
sys.path.insert(0, str(PKG / "scripts"))
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(PKG.parent / "tokens_horizon"))
from ap import config  # noqa: E402
from ap.arms import finetune, identify, solver_errors  # noqa: E402
from ap.fno import build  # noqa: E402
from ap.solver import KolmoDrag  # noqa: E402
from hybrid import Correction, HybridSolver  # noqa: E402
from th import score  # noqa: E402

PRE, W, WARM, NT = 10, 11, 3, 23
ARMS = ["H", "H_true", "O", "L0", "L_range", "L0big", "FNO_Re_id", "L_ft"]
SLICE = config.CACHE / "edge_slice.npz"


class Truth1:
    def __init__(self, T, F):
        self.T, self.F = T, F

    def __call__(self, j):
        return self.T[PRE + W + j][None]


def make_slice():
    tp = json.loads((PKG / "stage2" / "results" / "test_panels.json").read_text())["s2_test_Re50_D"]
    T = np.load(config.CACHE / "s2_test_Re50_D.npy", mmap_mode="r")
    Y = np.load(config.CACHE / "s2_test_Re50_D_obs.npy", mmap_mode="r")
    np.savez(SLICE, T=np.asarray(T[:, :NT]), Y=np.asarray(Y[:, :NT]), sigma_A=tp["sigma_A"], F=tp["F"], lam=tp["lam"],
             sigma40=json.loads((config.RESULTS / "chaos_gate.json").read_text())["Re40"]["sigma_A"],
             alpha=float(config.freeze()["drag"]["alpha"]))
    print("slice", SLICE, T.shape)


class Power:
    def __init__(self):
        self.lines, self.proc = [], None
        if shutil.which("tegrastats"):
            self.proc = subprocess.Popen(["tegrastats", "--interval", "100"], stdout=subprocess.PIPE, text=True)
            threading.Thread(target=self._read, daemon=True).start()

    def _read(self):
        for l in self.proc.stdout:
            m = re.search(r"VDD_IN (\d+)mW", l)
            r = re.search(r"RAM (\d+)/(\d+)MB", l)
            self.lines.append((time.time(), int(m.group(1)) if m else None, int(r.group(1)) if r else None))

    def window(self, t0, t1):
        v = [p for t, p, _ in self.lines if t0 <= t <= t1 and p is not None]
        ram = [x for t, _, x in self.lines if t0 <= t <= t1 and x is not None]
        return (float(np.mean(v)) if v else None, int(max(ram)) if ram else None, len(v))

    def stop(self):
        if self.proc:
            self.proc.terminate()


def sync(dev):
    if dev.startswith("cuda"):
        torch.cuda.synchronize(dev)


def run(device, outf, arms, fixed=False):
    import ap_eval
    stop = float("inf") if fixed else 0.3
    ap_eval.EPS_STOP = stop                   # rollout_errors reads this module constant
    z = np.load(SLICE)
    T, Y, sA, F, lam, s40, alpha = z["T"], z["Y"], float(z["sigma_A"]), int(z["F"]), float(z["lam"]), float(z["sigma40"]), float(z["alpha"])
    sc = 64.0 / s40
    Re = 50.0
    W_ = config.RUNS / "train"
    pw = Power()
    host = dict(hostname=os.uname().nodename, torch=torch.__version__, cuda=torch.version.cuda,
                device=torch.cuda.get_device_name(0) if device.startswith("cuda") else "cpu")
    for f in ("/etc/nv_tegra_release",):
        if Path(f).exists():
            host["l4t"] = Path(f).read_text().splitlines()[0]
    for cmd in (["nvpmodel", "-q"],):
        if shutil.which(cmd[0]):
            host["nvpmodel"] = subprocess.run(cmd, capture_output=True, text=True).stdout.strip().replace("\n", " | ")
    res = dict(host=host, arms={}, fixed_frames=F if fixed else None, early_stop=None if fixed else 0.3)
    for arm in arms:
        rec = dict(states=[], errors=[])
        try:
            if arm in ("H", "H_true"):
                g = Correction(sc).to(device)
                g.load_state_dict(torch.load(W_ / "H_D" / "best.pt", map_location=device))
                g.eval()
                make = lambda r: HybridSolver(r, g, device=device)  # noqa: E731
            elif arm in ("L0", "L_range", "L0big", "L_ft"):
                net = build("L0" if arm == "L_ft" else arm).to(device)
                net.load_state_dict(torch.load(W_ / ("L0" if arm == "L_ft" else arm) / "best.pt", map_location=device))
                net.eval()
            elif arm == "FNO_Re_id":
                net = build("L_param").to(device)
                net.load_state_dict(torch.load(W_ / "L_param" / "best.pt", map_location=device))
                net.eval()
                from obj_eval import fno_misfit, gss
        except torch.cuda.OutOfMemoryError as e:
            res["arms"][arm] = dict(result="does not fit in memory", error=str(e)[:300])
            continue
        from ap_eval import rollout_errors
        if device.startswith("cuda"):
            torch.cuda.reset_peak_memory_stats(device)
        t_arm0 = time.time()
        for i in range(NT):
            tr = Truth1(T[:, i], F)
            y0 = Y[PRE + W, i][None].astype(np.float64)
            Yw = Y[PRE + 1:PRE + W + 1, i:i + 1]
            sync(device)
            t0 = time.time()
            t_id = None
            try:
                if arm in ("H", "H_true"):
                    with torch.no_grad():
                        if arm == "H":
                            rh, _, _ = identify(Yw, W, 0.0, sA, device, lo=25.0, hi=80.0, make=make)
                            sync(device)
                            t_id = time.time() - t0
                        else:
                            rh = np.array([Re])
                        t1 = time.time()
                        err, st = solver_errors(y0, tr, rh, 0.0, sA, device, stop, make=make)
                elif arm == "O":
                    t1 = t0
                    err, st = solver_errors(y0, tr, np.array([Re]), alpha, sA, device, stop)
                elif arm in ("L0", "L_range", "L0big"):
                    t1 = t0
                    n_in = 8 if arm == "L_range" else 4
                    ctx = Y[PRE + W - n_in + 1:PRE + W + 1, i][None].astype(np.float64)
                    err = rollout_errors(net, ctx, tr, sc, sA)
                elif arm == "FNO_Re_id":
                    rh, _ = gss(lambda r: fno_misfit(net, Y[:, i:i + 1], W, r, sc, sA), 1)
                    sync(device)
                    t_id = time.time() - t0
                    t1 = time.time()
                    ctx = Y[PRE + W - 3:PRE + W + 1, i][None].astype(np.float64)
                    err = rollout_errors(net, ctx, tr, sc, sA, re=rh)
                elif arm == "L_ft":
                    px = np.stack([Y[PRE + k - 4:PRE + k, i] for k in range(1, W + 1)])
                    py = np.stack([Y[PRE + k, i] for k in range(1, W + 1)])
                    m = finetune(net, px, py, sc)
                    sync(device)
                    t_id = time.time() - t0
                    t1 = time.time()
                    ctx = Y[PRE + W - 3:PRE + W + 1, i][None].astype(np.float64)
                    err = rollout_errors(m, ctx, tr, sc, sA)
                sync(device)
                t2 = time.time()
            except torch.cuda.OutOfMemoryError as e:
                rec["errors"].append(f"state {i}: OOM {str(e)[:200]}")
                res["arms"][arm] = dict(result="does not fit in memory", error=str(e)[:300])
                break
            frames = int(np.isfinite(err[1:, 0]).sum())
            h = float(score.horizon(err.astype(float), lam, 0.35, 10.0, 0.1, 1)[0][0])
            rec["states"].append(dict(state=i, warmup=i < WARM, wall=t2 - t0, identify_or_adapt=t_id, forecast=t2 - t1,
                                      frames=frames, t_start=t0, t_end=t2, horizon=h))
        if arm in res["arms"]:
            continue
        timed = [s for s in rec["states"] if not s["warmup"]]
        wall = np.array([s["wall"] for s in timed])
        fc = np.array([s["forecast"] for s in timed])
        fr = np.array([s["frames"] for s in timed])
        p, ram, npw = pw.window(timed[0]["t_start"], timed[-1]["t_end"]) if timed else (None, None, 0)
        ida = [s["identify_or_adapt"] for s in timed if s["identify_or_adapt"] is not None]
        rec.update(n_timed=len(timed), wall_median=float(np.median(wall)), wall_p90=float(np.quantile(wall, 0.9)),
                   identify_or_adapt_median=float(np.median(ida)) if ida else None,
                   identify_or_adapt_p90=float(np.quantile(ida, 0.9)) if ida else None,
                   forecast_median=float(np.median(fc)), forecast_fps=float(fr.sum() / fc.sum()),
                   peak_torch_mem_MB=(torch.cuda.max_memory_allocated(device) / 2 ** 20) if device.startswith("cuda") else None,
                   tegrastats_ram_peak_MB=ram, vdd_in_mean_mW=p, power_samples=npw,
                   energy_per_state_J=(p / 1000 * float(wall.mean())) if p else None, arm_seconds=time.time() - t_arm0)
        res["arms"][arm] = rec
        Path(outf).write_text(json.dumps(res, indent=1, default=float))
        print(arm, {k: rec[k] for k in ("wall_median", "wall_p90", "forecast_fps", "peak_torch_mem_MB", "vdd_in_mean_mW")}, flush=True)
    pw.stop()
    Path(outf).write_text(json.dumps(res, indent=1, default=float))


if __name__ == "__main__":
    torch.set_num_threads(8)
    if sys.argv[1] == "slice":
        make_slice()
    else:
        run(sys.argv[2], sys.argv[3], sys.argv[4].split(",") if len(sys.argv) > 4 else ARMS,
            fixed=len(sys.argv) > 5 and sys.argv[5] == "fixed")
