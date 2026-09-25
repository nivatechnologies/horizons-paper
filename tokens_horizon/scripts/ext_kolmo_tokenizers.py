"""Post-freeze extension, Kolmogorov tokenizers (ext_freeze.yaml kolmogorov.tokenizers). Codebooks ->
runs/ext/kolmo/codebooks/.

  patch : shared patch codebooks, layouts 4x4 / 8x8 / 16x16 (P = 16 / 64 / 256 patches of 16x16 / 8x8 / 4x4 points),
          b in {8,...,16}; th/patchvq.gpu_kmeans with the frozen settings (seed 1000 P + b, max_iter 300, rtol 1e-6),
          fitted on all patches of a seeded random subset of whole calibration fit states (seed = calibration stream 2,
          min(204,800, 3,276,800 // P) states). Halved refits (A5) at b = 14, 16 on the subset states from the first
          half of the fit trajectories (suffix _half).
  rvq   : residual VQ, 4 stages of 8 bits, whole-state (4,096-dim) gpu_kmeans on all calibration fit states, stage s on
          the residual of stages < s, seed 5000 + s.

Implementation note: gpu_kmeans ends with an exact float64 assignment for its reported statistics using scipy cKDTree.
In 256 dimensions with 2^16 codes that query takes hours of CPU (measured 3.2 ms per point at d = 256), so this script
substitutes th/patchvq.exact_nn (certified exact nearest code, Amendment 1 A1) for that final query only. Both are
exact; the Lloyd iterations are untouched. GPU chunk: 2^29 / K rows (as the KS script), RVQ capped at 16,384 rows.

Usage: python scripts/ext_kolmo_tokenizers.py patch <device> <side> [b ...]  |  rvq <device>
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
from th import patchvq   # noqa: E402

CAP = 3_276_800
LOGD = E.RUNS / "logs"
DEVICE = [None]


class ExactTree:
    """Drop-in for cKDTree(C).query(X, workers) used by gpu_kmeans' final statistics: exact nearest code (A1)."""

    def __init__(self, C):
        self.C = np.asarray(C, float)
        Ct = torch.as_tensor(self.C, dtype=torch.float32, device=DEVICE[0])
        self.ct = dict(C64=self.C, C32=Ct, cn=(Ct * Ct).sum(1))

    def query(self, X, workers=None):
        idx, d2, _ = patchvq.exact_nn(np.asarray(X, float), self.ct, DEVICE[0], chunk=max(256, min(2 ** 27 // len(self.C), 2 ** 25 // self.C.shape[1])))
        return np.sqrt(d2), idx


def logger(name):
    LOGD.mkdir(parents=True, exist_ok=True)
    f = open(LOGD / f"{name}.log", "a")
    f.write(f"=== start {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    def log(s):
        f.write(s + "\n")
        f.flush()
    return log


def save(name, C, meta):
    E.CB.mkdir(parents=True, exist_ok=True)
    meta = dict(meta, name=name, git_sha=config.git_sha(), label="post-freeze extension")
    np.savez(E.CB / f"{name}.npz", C=C, meta=json.dumps(meta))
    print(name, {k: meta[k] for k in ("K", "n_train", "iterations", "converged", "empty_frac", "duplicate_frac",
                                      "reseeded_during_fit", "seconds")}, flush=True)


def chunk_for(K):
    return int(min(262144, max(4096, 2 ** 29 // K)))


def fit_states():
    X = np.load(E.CACHE / "calib_fit.npy", mmap_mode="r").reshape(-1, 64, 64)
    tr = np.load(E.CACHE / "calib_fit_traj.npy")
    return X, tr


def patch(device, side, b_list):
    X, tr = fit_states()
    n_traj = int(tr.max()) + 1
    P = side * side
    m = min(len(X), CAP // P)
    rng = np.random.default_rng(KM.seed("calibration", 2))
    idx = np.sort(rng.choice(len(X), m, replace=False))
    for item in b_list:
        half = item.endswith("h")
        b = int(item.rstrip("h"))
        name = f"kolmo_patch_L{side}_b{b}" + ("_half" if half else "")
        if (E.CB / f"{name}.npz").exists():
            continue
        sel = idx[tr[idx] < n_traj // 2] if half else idx
        Xp = patchvq.to_patches_2d(np.asarray(X[sel]), side, side).reshape(-1, (64 // side) ** 2)
        t0 = time.time()
        C, meta = patchvq.gpu_kmeans(Xp, 2 ** b, seed=1000 * P + b, device=device, max_iter=300, rtol=1e-6,
                                     chunk=chunk_for(2 ** b), log=logger(name))
        meta.update(method="th/patchvq.gpu_kmeans (as frozen); final statistics by exact_nn", half=half, layout=f"{side}x{side}",
                    P=P, b=b, states_used=int(len(sel)), independent_trajectories=int(len(np.unique(tr[sel]))),
                    patches=int(len(Xp)), samples_per_code=len(Xp) / 2 ** b, wall_seconds=time.time() - t0)
        save(name, C, meta)
        del Xp


def rvq(device):
    X, tr = fit_states()
    R = np.asarray(X).reshape(len(X), -1).copy()
    for s in range(1, 5):
        name = f"kolmo_rvq_s{s}"
        path = E.CB / f"{name}.npz"
        if path.exists():
            C = np.load(path)["C"]
        else:
            C, meta = patchvq.gpu_kmeans(R, 256, seed=5000 + s, device=device, max_iter=300, rtol=1e-6,
                                         chunk=min(16384, chunk_for(256)), log=logger(name))
            meta.update(method="th/patchvq.gpu_kmeans (as frozen); final statistics by exact_nn", stage=s,
                        states_used=int(len(R)), independent_trajectories=int(len(np.unique(tr))))
            save(name, C, meta)
        lab = ExactTree(C).query(R)[1]
        R = R - C[lab]


if __name__ == "__main__":
    mode, device = sys.argv[1], sys.argv[2]
    DEVICE[0] = device
    patchvq.cKDTree = ExactTree
    t0 = time.time()
    if mode == "patch":
        patch(device, int(sys.argv[3]), sys.argv[4:] or ["8", "10", "12", "14", "16", "14h", "16h"])
    else:
        rvq(device)
    print("done", sys.argv[1:], round(time.time() - t0), "s", flush=True)
