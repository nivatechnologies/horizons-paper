"""Post-freeze extension, Kolmogorov data blocks (ext_freeze.yaml `kolmogorov.blocks`). Writes runs/cache/ext_kolmo/
and results/ext/kolmo/data_blocks.json (sigma_A on the calibration fit split).

Seeds: freeze.yaml block bases + 100 * 8 + stream (calibration fit 0 -> 10800, held-out 1 -> 10801, confirmation 0 ->
40800). As in th/data.py each block draws all its random initial conditions from one generator
(th/kolmogorov.Kolmogorov.random_ic), burns in 500 tu and integrates every state (IFRK4, dt 0.01, float64, 64^2).
Calibration: samples every 1.4 tu starting 1.4 tu after burn-in, stored as float64 grids.
Confirmation panel: t = -46.2 .. +214.9 every 0.07 tu, stored as the exact retained Fourier coefficients, frame-major.

Usage: python scripts/ext_kolmo_data.py calib <device>  |  panel <device>
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from th import config   # noqa: E402
from th import kolmogorov as KM   # noqa: E402
from th import kolmo_eval as E   # noqa: E402


def update_json(d):
    E.RES.mkdir(parents=True, exist_ok=True)
    fn = E.RES / "data_blocks.json"
    store = json.loads(fn.read_text()) if fn.exists() else {}
    store.update(d)
    store.update(git_sha=config.git_sha(), label="post-freeze extension")
    fn.write_text(json.dumps(store, indent=1))


def calib(device):
    s = E.spec()
    E.CACHE.mkdir(parents=True, exist_ok=True)
    info = {}
    for part, stream in (("fit", 0), ("heldout", 1)):
        c = s["blocks"]["calibration"][part]
        m = KM.Kolmogorov(device=device)
        sd = KM.seed("calibration", stream)
        t0 = time.time()
        wh = m.random_ic(np.random.default_rng(sd), c["n_traj"])
        wh = m.flow(wh, int(round(s["numerics"]["burn_in_time"] / m.dt)))
        every = int(round(c["sample_every"] / m.dt))
        S = c["samples_per_traj"]
        X = np.lib.format.open_memmap(E.CACHE / f"calib_{part}.npy", mode="w+", dtype=np.float64,
                                      shape=(c["n_traj"], S, 64, 64))
        for k in range(S):
            wh = m.flow(wh, every)
            X[:, k] = E.grid(E.pack(wh))
        X.flush()
        np.save(E.CACHE / f"calib_{part}_traj.npy", np.repeat(np.arange(c["n_traj"]), S))
        info[f"calibration_{part}"] = dict(c, seed=sd, states=c["n_traj"] * S, seconds=time.time() - t0)
        print(part, "done", round(time.time() - t0), flush=True)
        if part == "fit":
            Xf = np.load(E.CACHE / "calib_fit.npy", mmap_mode="r").reshape(-1, 4096)
            mu = np.zeros(4096)
            for i in range(0, len(Xf), 20000):
                mu += Xf[i:i + 20000].sum(0)
            mu /= len(Xf)
            d2 = np.concatenate([((Xf[i:i + 20000] - mu) ** 2).sum(1) for i in range(0, len(Xf), 20000)])
            per_traj = np.sqrt(d2.reshape(c["n_traj"], -1).mean(1))
            info.update(sigma_A=float(np.sqrt(d2.mean())),
                        sigma_A_note="RMS Euclidean distance (over the 4,096 grid values) of calibration fit states to their mean",
                        calibration_mean_norm=float(np.linalg.norm(mu)),
                        sigma_A_per_traj_sd=float(per_traj.std(ddof=1)),
                        sigma_A_per_traj_range=[float(per_traj.min()), float(per_traj.max())])
            print("sigma_A", info["sigma_A"], flush=True)
        update_json(info)


def panel(device):
    s = E.spec()
    E.CACHE.mkdir(parents=True, exist_ok=True)
    n = s["blocks"]["confirmation"]["panel_states"]
    m = KM.Kolmogorov(device=device)
    sd = KM.seed("confirmation", 0)
    t0 = time.time()
    wh = m.random_ic(np.random.default_rng(sd), n)
    wh = m.flow(wh, int(round(s["numerics"]["burn_in_time"] / m.dt)))
    pre = E.units(float(s["pre_history_time"]))
    post = E.units(float(s["post_time"]))
    spu = int(round(E.UNIT / m.dt))
    Z = np.lib.format.open_memmap(E.CACHE / "panel_confirmation.npy", mode="w+", dtype=np.complex128,
                                  shape=(pre + post + 1, n, 43, 22))
    Z[0] = E.pack(wh)
    for k in range(1, pre + post + 1):
        wh = m.flow(wh, spu)
        Z[k] = E.pack(wh)
        if k % 500 == 0:
            print("unit", k, round(time.time() - t0), flush=True)
    Z.flush()
    update_json(dict(panel_confirmation=dict(states=n, seed=sd, units=pre + post + 1, unit_time=E.UNIT,
                                             pre_units=pre, post_units=post, burn_in_time=s["numerics"]["burn_in_time"],
                                             storage="retained Fourier coefficients (43 x 22 complex128), frame-major",
                                             seconds=time.time() - t0)))
    print("panel done", round(time.time() - t0), flush=True)


if __name__ == "__main__":
    torch.set_num_threads(8)
    {"calib": calib, "panel": panel}[sys.argv[1]](sys.argv[2])
