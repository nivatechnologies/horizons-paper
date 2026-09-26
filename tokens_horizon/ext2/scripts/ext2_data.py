"""EXT2 (learned-tokenizer kill test) Kolmogorov data blocks not produced by the extension: training and validation.

Seeds (freeze.yaml scheme, system index 8): training stream 0 -> 20800, validation stream 0 -> 30800. Generation as
scripts/ext_kolmo_data.py calib: all initial conditions of a block from one generator (Kolmogorov.random_ic), burn-in
500 tu, IFRK4 dt 0.01 float64 64^2; samples every 1.4 tu starting 1.4 tu after burn-in; grids stored as float32
(integration in float64). Sizes: ext2_freeze.yaml data.blocks.
Writes runs/cache/ext_kolmo/{training,validation}.npy (+ _traj.npy) and results/ext2/data_blocks.json.

Usage: python ext2/scripts/ext2_data.py <training|validation> <device>
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from th import config   # noqa: E402
from th import kolmogorov as KM   # noqa: E402
from th import kolmo_eval as E   # noqa: E402

SIZES = {"training": dict(n_traj=256, samples_per_traj=800, sample_every=1.4),
         "validation": dict(n_traj=64, samples_per_traj=100, sample_every=1.4)}
RES = config.RESULTS / "ext2"


def main(block, device):
    c = SIZES[block]
    m = KM.Kolmogorov(device=device)
    sd = KM.seed(block, 0)
    t0 = time.time()
    wh = m.random_ic(np.random.default_rng(sd), c["n_traj"])
    wh = m.flow(wh, int(round(E.spec()["numerics"]["burn_in_time"] / m.dt)))
    every = int(round(c["sample_every"] / m.dt))
    S = c["samples_per_traj"]
    X = np.lib.format.open_memmap(E.CACHE / f"{block}.npy", mode="w+", dtype=np.float32, shape=(c["n_traj"], S, 64, 64))
    for k in range(S):
        wh = m.flow(wh, every)
        X[:, k] = E.grid(E.pack(wh))
    X.flush()
    np.save(E.CACHE / f"{block}_traj.npy", np.repeat(np.arange(c["n_traj"]), S))
    RES.mkdir(parents=True, exist_ok=True)
    fn = RES / "data_blocks.json"
    store = json.loads(fn.read_text()) if fn.exists() else {}
    store[block] = dict(c, seed=sd, states=c["n_traj"] * S, seconds=time.time() - t0, storage="float32 grids",
                        burn_in_time=E.spec()["numerics"]["burn_in_time"])
    store.update(git_sha=config.git_sha(), label="EXT2 learned-tokenizer kill test")
    fn.write_text(json.dumps(store, indent=1))
    print(block, "done", round(time.time() - t0), flush=True)


if __name__ == "__main__":
    torch.set_num_threads(8)
    main(sys.argv[1], sys.argv[2])
