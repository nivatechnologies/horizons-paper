"""Post-freeze extension, KS data blocks (ext_freeze.yaml `ks.blocks`). Writes runs/cache/ext_ks/*.npy and
results/ext/ks/data_blocks.json (+ sigma_A on the calibration fit block).

Seeds: freeze.yaml block bases + 100 * system_index (ks22 = 6, ks100 = 7) + stream; calibration fit stream 0,
held-out stream 1, all others 0. As in th/data.py, each block draws all its small random starts from one generator
(so results do not depend on how the work is split across processes), then burns in and integrates each state.
As in th/data.py, the validation trajectories and the validation panel share the validation seed (stream 0).

Panels (validation 300, confirmation 1,000): one integration per state from t = -pre_time to post_time at the frozen
dt; stored as the three frame grids (t = 0 on every grid, frames k*Delta for k = -floor(pre/Delta) .. floor(post/Delta)).
Training/validation trajectories: stored on the three frame grids from t = 0 (after burn-in) to traj_time.

Usage: python scripts/ext_ks_data.py [ks22|ks100 ...]
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import json   # noqa: E402
import math   # noqa: E402
import sys    # noqa: E402
import time   # noqa: E402
from concurrent.futures import ProcessPoolExecutor   # noqa: E402
from pathlib import Path   # noqa: E402

import numpy as np   # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from th import config   # noqa: E402
from th import ks as K   # noqa: E402

NPROC = 64
CACHE = config.CACHE / "ext_ks"
OUTD = config.RESULTS / "ext" / "ks"


def spec(system):
    return K.ks_spec(system)


def seed_of(system, block, stream):
    base = config.freeze()["seeds"]["block_base"][block]
    return K.block_seed(base, spec(system)["system_index"], stream)


def fmt(d):
    return f"{d:g}"


def _job(args):
    system, v0, burn_steps, n_steps, record = args
    s = spec(system)
    ks = K.KS(s["L"], s["N"], s["dt"])
    v = ks.flow(v0, burn_steps)
    out, _ = K.integrate_record(ks, v, n_steps, record)
    return out


def run_block(system, seed, n, n_steps, record):
    """Draw n small random starts from one generator, split across processes, burn in, integrate, record."""
    s = spec(system)
    ks = K.KS(s["L"], s["N"], s["dt"])
    rng = np.random.default_rng(seed)
    v0 = ks.small_random_start(rng, n)
    burn = K.steps(s["burn_in_time"], s["dt"])
    chunks = np.array_split(np.arange(n), min(NPROC, n))
    with ProcessPoolExecutor(len(chunks)) as ex:
        parts = list(ex.map(_job, [(system, v0[c], burn, n_steps, record) for c in chunks]))
    return {k: np.concatenate([p[k] for p in parts], 0) for k in record}


def grid_record(s, t_start_steps, n_steps, deltas):
    """Step indices of the frame grids with t = 0 at step t_start_steps."""
    rec = {}
    for d in deltas:
        sub = K.steps(d, s["dt"])
        k0 = t_start_steps // sub
        k1 = (n_steps - t_start_steps) // sub
        rec[fmt(d)] = t_start_steps + sub * np.arange(-k0, k1 + 1)
    return rec


def save(name, arr):
    CACHE.mkdir(parents=True, exist_ok=True)
    np.save(CACHE / f"{name}.npy", arr)


def main(system):
    s = spec(system)
    ef = K.ext_freeze()["ks"]["blocks"]
    deltas = s["frame_intervals"]
    info = dict(system=system, dt=s["dt"], N=s["N"], L=s["L"], burn_in_time=s["burn_in_time"])
    t0 = time.time()

    # calibration fit and held-out
    for part, stream in (("fit", 0), ("heldout", 1)):
        c = ef["calibration"][system][part]
        sub = K.steps(c["sample_every"], s["dt"])
        n_steps = sub * c["samples_per_traj"]
        rec = {"x": sub * np.arange(1, c["samples_per_traj"] + 1)}
        seed = seed_of(system, "calibration", stream)
        X = run_block(system, seed, c["n_traj"], n_steps, rec)["x"]          # (n_traj, samples, N)
        save(f"calib_{system}_{part}", X.reshape(-1, s["N"]))
        save(f"calib_{system}_{part}_traj", np.repeat(np.arange(c["n_traj"]), c["samples_per_traj"]))
        info[f"calibration_{part}"] = dict(c, seed=seed, states=int(X.shape[0] * X.shape[1]))
        if part == "fit":
            Xf = X.reshape(-1, s["N"])
            mu = Xf.mean(0)
            d2 = ((Xf - mu) ** 2).sum(1)
            per_traj = np.sqrt(d2.reshape(c["n_traj"], -1).mean(1))
            info["sigma_A"] = float(np.sqrt(d2.mean()))
            info["sigma_A_note"] = "RMS Euclidean distance (over the N grid points) of calibration fit states to their mean"
            info["calibration_mean_norm"] = float(np.linalg.norm(mu))
            info["sigma_A_traj_spread"] = float(per_traj.std(ddof=1))
            del Xf
        del X
        print(system, "calibration", part, round(time.time() - t0), "s", flush=True)

    # training (data axis 1,000; the first n_traj are the base set) and validation trajectories
    for block, key in (("training", "training"), ("validation", "validation")):
        b = ef[key][system]
        n_all = 1000 if block == "training" else b["n_traj"]
        n_steps = K.steps(b["traj_time"], s["dt"]) if abs(b["traj_time"] / s["dt"] - round(b["traj_time"] / s["dt"])) < 1e-9 \
            else int(math.floor(b["traj_time"] / s["dt"]))
        rec = grid_record(s, 0, n_steps, deltas)
        seed = seed_of(system, block, 0)
        out = run_block(system, seed, n_all, n_steps, rec)
        for d, arr in out.items():
            save(f"{block}_{system}_d{d}", arr)
        info[block] = dict(b, n_traj_stored=n_all, seed=seed, frames={d: int(a.shape[1]) for d, a in out.items()})
        print(system, block, round(time.time() - t0), "s", flush=True)

    # panels: validation (300) and confirmation (1,000)
    pre_steps = K.steps(s["pre_history_time"], s["dt"])
    post_steps = int(math.ceil(s["post_time"] / s["dt"] - 1e-9))
    for block, n in (("validation", ef["validation"][system]["panel_states"]),
                     ("confirmation", ef["confirmation"]["panel_states"])):
        rec = grid_record(s, pre_steps, pre_steps + post_steps, deltas)
        seed = seed_of(system, block, 0)
        out = run_block(system, seed, n, pre_steps + post_steps, rec)
        pres = {}
        for d, arr in out.items():
            save(f"panel_{block}_{system}_d{d}", arr)
            pres[d] = int(pre_steps // K.steps(float(d), s["dt"]))
        np.save(CACHE / f"panel_{block}_{system}_pre.npy", np.array([pres[fmt(d)] for d in deltas]))
        info[f"panel_{block}"] = dict(states=n, seed=seed, pre_frames=pres,
                                      frames={d: int(a.shape[1]) for d, a in out.items()},
                                      pre_time=s["pre_history_time"], post_time=s["post_time"])
        print(system, "panel", block, round(time.time() - t0), "s", flush=True)
    info["seconds"] = time.time() - t0
    return info


if __name__ == "__main__":
    OUTD.mkdir(parents=True, exist_ok=True)
    fn = OUTD / "data_blocks.json"
    store = json.loads(fn.read_text()) if fn.exists() else {}
    for system in (sys.argv[1:] or ["ks22", "ks100"]):
        store[system] = main(system)
        store["git_sha"] = config.git_sha()
        store["label"] = "post-freeze extension"
        fn.write_text(json.dumps(store, indent=1))
