"""Post-freeze extension, KS tokenizers (ext_freeze.yaml ks.tokenizers, ks_fix_1). Codebooks -> runs/ext/ks/codebooks/.

  whole  : whole-state k-means, ks22, bits 4..16 on all 3.3M calibration fit states; th/patchvq.gpu_kmeans exactly as
           frozen (seed = bits, max_iter 300, rtol 1e-6). Halved refits (A5) at 15 and 16 bits on the first half of the
           fit trajectories (suffix _half).
  patch  : shared patch codebooks, P in {8,16,32}, b in {8,...,16}; fitted on all patches of a seeded subset of whole
           fit states (seed = calibration seed stream 2; 16,000,000 // P states, all if fewer), th/cpukmeans.cpu_kmeans
           (ks_fix_1), seed = 1000 P + b. Halved refits at b = 14, 16 on the subset states from the first half of the
           fit trajectories (suffix _half).
  rvq    : residual VQ, 4 stages of 8 bits on whole fit states (capped at 1,000,000: seeded subset, calibration seed
           stream 3); stage s fitted on the residual of stages < s with gpu_kmeans, seed 5000 + s.

Usage: python scripts/ext_ks_tokenizers.py whole cuda:2 16 15 ...   |   patch ks22 8 [b ...]   |   rvq cuda:0 ks22
"""
import os
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from th import config   # noqa: E402
from th import ks as K   # noqa: E402

CACHE = config.CACHE / "ext_ks"
CB = config.RUNS / "ext" / "ks" / "codebooks"
LOGD = config.RUNS / "ext" / "ks" / "logs"
PATCH_CAP = 16_000_000
RVQ_CAP = 1_000_000


def seed_of(system, block, stream):
    return K.block_seed(config.freeze()["seeds"]["block_base"][block], K.ks_spec(system)["system_index"], stream)


def fit_states(system):
    X = np.load(CACHE / f"calib_{system}_fit.npy", mmap_mode="r")
    tr = np.load(CACHE / f"calib_{system}_fit_traj.npy")
    return X, tr


def logger(name):
    LOGD.mkdir(parents=True, exist_ok=True)
    f = open(LOGD / f"{name}.log", "a")
    f.write(f"=== start {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    def log(s):
        f.write(s + "\n")
        f.flush()
    return log


def save(name, C, meta):
    CB.mkdir(parents=True, exist_ok=True)
    meta = dict(meta, name=name, git_sha=config.git_sha(), label="post-freeze extension")
    np.savez(CB / f"{name}.npz", C=C, meta=json.dumps(meta))
    print(name, {k: meta[k] for k in ("K", "n_train", "iterations", "converged", "empty_frac", "duplicate_frac",
                                      "reseeded_during_fit", "seconds")}, flush=True)


def chunk_for(K):
    """GPU chunk size (rows per distance block): 2^29 float32 entries per block, between 4,096 and 262,144 rows.
    The chunk only sets batching and the per-chunk top-64 farthest-point candidates of gpu_kmeans."""
    return int(min(262144, max(4096, 2 ** 29 // K)))


def whole(device, bits_list):
    from th.patchvq import gpu_kmeans
    X, tr = fit_states("ks22")
    n_traj = int(tr.max()) + 1
    for item in bits_list:
        half = item.endswith("h")
        b = int(item.rstrip("h"))
        name = f"ks22_whole_b{b}" + ("_half" if half else "")
        if (CB / f"{name}.npz").exists():
            continue
        Xf = np.asarray(X[tr < n_traj // 2]) if half else np.asarray(X)
        C, meta = gpu_kmeans(Xf, 2 ** b, seed=b, device=device, max_iter=300, rtol=1e-6, log=logger(name),
                             chunk=chunk_for(2 ** b))
        meta.update(method="th/patchvq.gpu_kmeans (as frozen)", half=half, n_traj_fit=(n_traj // 2 if half else n_traj))
        save(name, C, meta)


def patch_subset(system, P):
    X, tr = fit_states(system)
    n = len(X)
    m = min(n, PATCH_CAP // P)
    rng = np.random.default_rng(seed_of(system, "calibration", 2))
    idx = np.sort(rng.choice(n, m, replace=False))
    return idx, tr[idx]


def patch(system, P, b_list):
    from th.cpukmeans import cpu_kmeans
    from th.patchvq import to_patches_1d
    X, tr = fit_states(system)
    n_traj = int(tr.max()) + 1
    idx, tri = patch_subset(system, P)
    for item in b_list:
        half = item.endswith("h")
        b = int(item.rstrip("h"))
        name = f"{system}_patch_P{P}_b{b}" + ("_half" if half else "")
        if (CB / f"{name}.npz").exists():
            continue
        sel = idx[tri < n_traj // 2] if half else idx
        Xp = to_patches_1d(np.asarray(X[sel]), P).reshape(-1, X.shape[1] // P)
        C, meta = cpu_kmeans(Xp, 2 ** b, seed=1000 * P + b, max_iter=300, rtol=1e-6, workers=int(os.environ.get("KS_KMEANS_WORKERS", "40")), log=logger(name))
        meta.update(half=half, P=P, b=b, states_used=int(len(sel)),
                    independent_trajectories=int(len(np.unique(tr[sel]))), patches=int(len(Xp)))
        save(name, C, meta)
        del Xp


def rvq(device, system):
    from th.patchvq import gpu_kmeans
    X, tr = fit_states(system)
    n = len(X)
    m = min(n, RVQ_CAP)
    rng = np.random.default_rng(seed_of(system, "calibration", 3))
    idx = np.sort(rng.choice(n, m, replace=False))
    R = np.asarray(X[idx]).copy()
    from scipy.spatial import cKDTree
    for s in range(1, 5):
        name = f"{system}_rvq_s{s}"
        path = CB / f"{name}.npz"
        if path.exists():
            C = np.load(path)["C"]
        else:
            C, meta = gpu_kmeans(R, 256, seed=5000 + s, device=device, max_iter=300, rtol=1e-6, log=logger(name),
                                 chunk=chunk_for(256))
            meta.update(method="th/patchvq.gpu_kmeans (as frozen)", stage=s, states_used=int(m),
                        independent_trajectories=int(len(np.unique(tr[idx]))))
            save(name, C, meta)
        _, lab = cKDTree(C).query(R, workers=16)
        R = R - C[lab]


if __name__ == "__main__":
    mode = sys.argv[1]
    t0 = time.time()
    if mode == "whole":
        whole(sys.argv[2], sys.argv[3:])
    elif mode == "patch":
        patch(sys.argv[2], int(sys.argv[3]), sys.argv[4:] or ["8", "10", "12", "14", "16", "14h", "16h"])
    elif mode == "rvq":
        rvq(sys.argv[2], sys.argv[3])
    print("done", mode, sys.argv[2:], round(time.time() - t0), "s", flush=True)
