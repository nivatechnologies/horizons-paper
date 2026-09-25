"""Lloyd k-means with exact float64 CPU assignment (EXT_FREEZE part 2a fix 1, ext_freeze.yaml `ks_fix_1`).

Used for the KS patch-product codebooks. Identical to th/patchvq.gpu_kmeans in
  * init: rng = default_rng(seed); init = rng.choice(n, K, replace=False) (seeded sample of distinct points);
  * float64 centroid accumulation (sums / counts);
  * empty clusters re-seeded from the points farthest from their assigned centroid (largest distances first), counted;
  * stop: |inertia_prev - inertia| <= rtol * inertia_prev with no empty cluster in that iteration, or max_iter;
  * the returned metadata (final exact float64 assignment statistics: inertia, mse, empty and duplicate codes, ...),
except that the assignment step is the exact float64 nearest code (scipy cKDTree) on the CPU, and the centroids are
kept in float64 (gpu_kmeans casts them to float32 for its float32 GPU assignment).

Farthest-point re-seeding: gpu_kmeans takes the global largest distances among per-chunk top-64 candidates, which
equals the global top-k whenever k <= 64 empty clusters; here the global top-k is taken directly.
"""
from __future__ import annotations

import time

import numpy as np
from scipy.spatial import cKDTree


def cpu_kmeans(X, K, seed, max_iter=300, rtol=1e-6, workers=40, log=None):
    """X (n, d) float64 numpy. Returns centers (K, d) float64 and a metadata dict (same keys as gpu_kmeans)."""
    rng = np.random.default_rng(seed)
    X = np.ascontiguousarray(X, dtype=np.float64)
    n, d = X.shape
    if K > n:
        raise ValueError(f"K={K} exceeds the number of training vectors n={n}")
    init = rng.choice(n, K, replace=False)
    C = X[init].copy()
    prev, reseeded_total, it = None, 0, 0
    t0 = time.time()
    for it in range(1, max_iter + 1):
        dist, lab = cKDTree(C).query(X, workers=workers)
        md = dist * dist
        inertia = float(md.sum())
        cnt = np.bincount(lab, minlength=K).astype(np.float64)
        sums = np.empty((K, d))
        for j in range(d):
            sums[:, j] = np.bincount(lab, weights=X[:, j], minlength=K)
        empty = np.flatnonzero(cnt == 0)
        newC = sums / np.maximum(cnt, 1)[:, None]
        if len(empty):
            far = np.argpartition(-md, len(empty) - 1)[:len(empty)]
            far = far[np.argsort(-md[far], kind="stable")]
            newC[empty] = X[far]
            reseeded_total += int(len(empty))
        C = newC
        if log:
            log(f"  it {it:3d} inertia {inertia:.6e} empty {len(empty)} ({time.time()-t0:.0f}s)")
        if prev is not None and abs(prev - inertia) <= rtol * prev and len(empty) == 0:
            break
        prev = inertia
    tree = cKDTree(C)
    dd, lab = tree.query(X, workers=workers)
    counts = np.bincount(lab, minlength=K)
    uniq = len(np.unique(np.round(C, 12), axis=0))
    meta = dict(K=K, n_train=int(n), dim=int(d), iterations=it, converged=bool(it < max_iter),
                inertia=float((dd ** 2).sum()), mse=float((dd ** 2).mean()),
                empty_codes=int((counts == 0).sum()), empty_frac=float((counts == 0).mean()),
                duplicate_codes=int(K - uniq), duplicate_frac=float((K - uniq) / K),
                reseeded_during_fit=reseeded_total, seed=int(seed), seconds=time.time() - t0,
                method="cpu_kmeans (ks_fix_1): exact float64 cKDTree assignment")
    return C, meta
