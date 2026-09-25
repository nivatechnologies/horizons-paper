"""Post-freeze extension E2: large codebooks, patch product codebooks and their exact output-support bound.

Patch product codebook. The state x (a field on a 1D or 2D grid) is split into P non-overlapping patches x_1..x_P
of equal shape; one shared codebook C = {c_j} of 2^b codes is fitted by k-means on patches from calibration states;
each patch is encoded to its nearest code and decoded independently. The representable set is the product C^P.

Exact bound. For any y in C^P, ||x - y||^2 = sum_p ||x_p - y_p||^2 >= sum_p min_j ||x_p - c_j||^2, with equality at
y_p = argmin_j ||x_p - c_j||, which is in C^P. Hence d_C(x) = sqrt(sum_p min_j ||x_p - c_j||^2) exactly, and it is
attained by patch-wise nearest decoding.

k-means runs on the GPU in float32 with float64 accumulation of centroids (Lloyd iterations; init by a seeded sample
of distinct data points; empty clusters re-seeded from the points farthest from their centroid, and counted).
Distances for the bound are exact (Amendment 1, A1): brute force over all codes, float32 ranking certified by a
rigorous rounding margin with float64 re-scoring, else float64 brute force (exact_nn). Code-neighbour candidate sets
serve only to certify NON-crossing through an upper bound (d_C^2 <= UB <= T^2); a crossing is declared only from an
exact d_C (certified_bound_crossings).
"""
from __future__ import annotations

import json
import time

import numpy as np
import torch
from scipy.spatial import cKDTree


# ----------------------------------------------------------------------------------------------- patches
def to_patches_1d(U, P):
    """U (..., N) -> (..., P, N // P). N must be divisible by P."""
    N = U.shape[-1]
    assert N % P == 0, (N, P)
    return U.reshape(U.shape[:-1] + (P, N // P))


def from_patches_1d(X):
    return X.reshape(X.shape[:-2] + (-1,))


def to_patches_2d(W, pr, pc):
    """W (..., N, M) -> (..., pr*pc, (N//pr)*(M//pc)), patches in row-major patch order."""
    N, M = W.shape[-2:]
    assert N % pr == 0 and M % pc == 0
    a, b = N // pr, M // pc
    X = W.reshape(W.shape[:-2] + (pr, a, pc, b))
    nd = X.ndim
    X = np.moveaxis(X, nd - 3, nd - 2)          # (..., pr, pc, a, b)
    return X.reshape(W.shape[:-2] + (pr * pc, a * b))


def from_patches_2d(X, pr, pc, N, M):
    a, b = N // pr, M // pc
    Y = X.reshape(X.shape[:-2] + (pr, pc, a, b))
    nd = Y.ndim
    Y = np.moveaxis(Y, nd - 2, nd - 3)          # (..., pr, a, pc, b)
    return Y.reshape(X.shape[:-2] + (N, M))


# ----------------------------------------------------------------------------------------------- k-means
def gpu_kmeans(X, K, seed, device="cuda:0", max_iter=100, rtol=1e-6, chunk=4096, log=None):
    """Lloyd k-means. X (n, d) float64 numpy. Returns centers (K, d) float64 and a metadata dict."""
    rng = np.random.default_rng(seed)
    n, d = X.shape
    if K > n:
        raise ValueError(f"K={K} exceeds the number of training vectors n={n}")
    init = rng.choice(n, K, replace=False)
    C = torch.as_tensor(X[init], dtype=torch.float32, device=device)
    Xt = torch.as_tensor(X, dtype=torch.float32)                     # stays on CPU, streamed in chunks
    prev, reseeded_total, it = None, 0, 0
    t0 = time.time()
    for it in range(1, max_iter + 1):
        sums = torch.zeros((K, d), dtype=torch.float64, device=device)
        cnt = torch.zeros(K, dtype=torch.float64, device=device)
        inertia = 0.0
        far_d, far_i = [], []
        cn = (C * C).sum(1)
        for s in range(0, n, chunk):
            xb = Xt[s:s + chunk].to(device, non_blocking=True)
            d2 = (xb * xb).sum(1, keepdim=True) - 2 * xb @ C.T + cn[None]
            md, lab = d2.min(1)
            md = md.clamp_min(0)
            inertia += float(md.double().sum())
            sums.index_add_(0, lab, xb.double())
            cnt.index_add_(0, lab, torch.ones_like(md, dtype=torch.float64))
            k = min(64, len(md))
            v, i = md.topk(k)
            far_d.append(v.cpu())
            far_i.append(i.cpu() + s)
        empty = (cnt == 0).nonzero().flatten()
        newC = (sums / cnt.clamp_min(1)[:, None]).float()
        if len(empty):
            fd, fi = torch.cat(far_d), torch.cat(far_i)
            order = fd.argsort(descending=True)[:len(empty)]
            newC[empty] = Xt[fi[order]].to(device)
            reseeded_total += int(len(empty))
        C = newC
        if log:
            log(f"  it {it:3d} inertia {inertia:.6e} empty {len(empty)} ({time.time()-t0:.0f}s)")
        if prev is not None and abs(prev - inertia) <= rtol * prev and len(empty) == 0:
            break
        prev = inertia
    Cn = C.double().cpu().numpy()
    # final assignment statistics in float64 on CPU (exact)
    tree = cKDTree(Cn)
    dd, lab = tree.query(X, workers=16)
    counts = np.bincount(lab, minlength=K)
    uniq = len(np.unique(np.round(Cn, 12), axis=0))
    meta = dict(K=K, n_train=int(n), dim=int(d), iterations=it, converged=bool(it < max_iter),
                inertia=float((dd ** 2).sum()), mse=float((dd ** 2).mean()),
                empty_codes=int((counts == 0).sum()), empty_frac=float((counts == 0).mean()),
                duplicate_codes=int(K - uniq), duplicate_frac=float((K - uniq) / K),
                reseeded_during_fit=reseeded_total, seed=int(seed), seconds=time.time() - t0)
    return Cn, meta


class PatchCodebook:
    """Shared codebook over patches; exact product bound and patch-wise decode."""

    def __init__(self, C, meta=None):
        self.C = np.asarray(C, float)
        self.meta = meta or {}
        self.tree = cKDTree(self.C)

    def encode(self, Xp, workers=16):
        """Xp (..., P, d) -> token ids (..., P) and squared distances (..., P)."""
        shp = Xp.shape[:-1]
        dd, idx = self.tree.query(Xp.reshape(-1, Xp.shape[-1]), workers=workers)
        return idx.reshape(shp), (dd ** 2).reshape(shp)

    def decode(self, idx):
        return self.C[idx]

    def dist(self, Xp, workers=16):
        """Exact output-support distance d_C(x) = sqrt(sum_p min_j ||x_p - c_j||^2), shape (...)."""
        _, d2 = self.encode(Xp, workers)
        return np.sqrt(d2.sum(-1))

    def save(self, path):
        np.savez(path, C=self.C, meta=json.dumps(self.meta))

    @classmethod
    def load(cls, path):
        z = np.load(path, allow_pickle=False)
        return cls(z["C"], json.loads(str(z["meta"])))


# ----------------------------------------------------------------------------------------------- exact bound, fast
def code_neighbours(C, m=32, device="cuda:0", chunk=2048):
    """For each code, its m nearest codes (including itself), by exact float32 distances on the GPU."""
    K = len(C)
    m = min(m, K)
    Ct = torch.as_tensor(C, dtype=torch.float32, device=device)
    cn = (Ct * Ct).sum(1)
    out = np.empty((K, m), np.int64)
    for s in range(0, K, chunk):
        d2 = cn[s:s + chunk, None] - 2 * Ct[s:s + chunk] @ Ct.T + cn[None]
        out[s:s + chunk] = d2.topk(m, largest=False).indices.cpu().numpy()
    return out


def exact_nn(Xp, C_t, device="cuda:0", chunk=8192, k=8):
    """Exact nearest code (Amendment 1, A1): brute force over all codes.

    Float32 GPU distances rank all codes; the top-k candidates are re-scored in float64. The float64 winner is
    accepted only if its distance is below the (k+1)-th float32 distance minus a rigorous float32 rounding margin
    err = 4 (d + 2) u (||x|| + max_j ||c_j||)^2, u = 2^-24, which bounds |d2_float32 - d2_exact| for every code; then
    no code outside the candidate set can be nearer. Rows that fail the certificate are recomputed by float64 brute
    force over all codes on the CPU. Returns (idx (n,), d2 (n,) float64, n_fallback)."""
    C64 = C_t["C64"]
    Ct, cn = C_t["C32"], C_t["cn"]
    K, d = C64.shape
    kk = min(k + 1, K)
    cmax = float(np.sqrt((C64 ** 2).sum(1).max()))
    u = 2.0 ** -24
    n = len(Xp)
    idx = np.empty(n, np.int64)
    d2o = np.empty(n)
    n_fb = 0
    for s in range(0, n, chunk):
        xb64 = Xp[s:s + chunk]
        xb = torch.as_tensor(xb64, dtype=torch.float32, device=device)
        d2 = (xb * xb).sum(1, keepdim=True) - 2 * xb @ Ct.T + cn[None]
        vals, cand = d2.topk(kk, largest=False)
        vals, cand = vals.double().cpu().numpy(), cand.cpu().numpy()
        cand_k = cand[:, :min(k, K)]
        dd = ((xb64[:, None, :] - C64[cand_k]) ** 2).sum(-1)
        j = dd.argmin(1)
        best = dd[np.arange(len(j)), j]
        bi = cand_k[np.arange(len(j)), j]
        if kk > min(k, K):
            xn = np.sqrt((xb64 ** 2).sum(1))
            err = 4 * (d + 2) * u * (xn + cmax) ** 2
            ok = best < vals[:, -1] - err
        else:
            ok = np.ones(len(j), bool)               # every code was a candidate
        bad = np.flatnonzero(~ok)
        for r in bad:                                # float64 brute force over all codes
            full = ((C64 - xb64[r]) ** 2).sum(1)
            bi[r] = full.argmin()
            best[r] = full[bi[r]]
        n_fb += len(bad)
        idx[s:s + chunk] = bi
        d2o[s:s + chunk] = best
    return idx, d2o, n_fb


def certified_bound_crossings(frame_patches, n_frames, C, thresholds, nbr=None, device="cuda:0", log=None):
    """First frame index at which d_C(x_j) > threshold, for each state and threshold (in absolute units).

    frame_patches(j) -> (n, P, d) float64 patches of the true state at frame j (j = 0..n_frames).
    thresholds: increasing list of absolute distances (eps * sigma_A).
    Returns first (n, len(thresholds)) int array (n_frames + 1 where never crossed), d_C at frame 0 (exact, (n,)),
    and counters of exact and certified evaluations.

    Exactness: at every frame, for every state that has not yet crossed threshold T_k, either the upper bound
    UB = sum_p min_{j in S_p} ||x_p - c_j||^2 (S_p = code-graph neighbours of the patch's previous code) is <= T_k^2,
    which implies d_C^2 <= UB <= T_k^2 (certified not crossed), or d_C^2 is computed exactly. Decisions are never
    made from an approximation.
    """
    C64 = np.asarray(C, float)
    Ct = torch.as_tensor(C64, dtype=torch.float32, device=device)
    C_t = dict(C64=C64, C32=Ct, cn=(Ct * Ct).sum(1))
    if nbr is None:
        nbr = code_neighbours(C64, device=device)
    X0 = frame_patches(0)
    n, P, d = X0.shape
    T2 = np.asarray(thresholds, float) ** 2
    nT = len(T2)
    idx0, d20, fb0 = exact_nn(X0.reshape(-1, d), C_t, device)
    codes = idx0.reshape(n, P)
    dC0 = np.sqrt(d20.reshape(n, P).sum(1))
    first = np.full((n, nT), n_frames + 1, np.int64)
    for k in range(nT):
        first[dC0 ** 2 > T2[k], k] = np.minimum(first[dC0 ** 2 > T2[k], k], 0)
    n_exact, n_cert, n_fb = n * P, 0, fb0
    for j in range(1, n_frames + 1):
        alive = (first == n_frames + 1).any(1)                       # still needs some threshold
        if not alive.any():
            break
        Xj = frame_patches(j)[alive]                                 # (a, P, d)
        a = Xj.shape[0]
        cand = nbr[codes[alive]]                                     # (a, P, m)
        diff = Xj[:, :, None, :] - C64[cand]                         # (a, P, m, d)
        dd = (diff * diff).sum(-1)
        kbest = dd.argmin(-1)
        ub_p = np.take_along_axis(dd, kbest[..., None], -1)[..., 0]  # (a, P)
        ub = ub_p.sum(1)
        new_codes = np.take_along_axis(cand, kbest[..., None], -1)[..., 0]
        open_k = (first[alive] == n_frames + 1)                      # (a, nT) thresholds not yet crossed
        # the smallest open threshold decides whether an exact value is needed
        tmin = np.where(open_k, T2[None, :], np.inf).min(1)
        need = ub > tmin
        n_cert += int((~need).sum())
        d2 = ub.copy()
        if need.any():
            ex_idx, ex_d2, fb = exact_nn(Xj[need].reshape(-1, d), C_t, device)
            n_fb += fb
            n_exact += int(need.sum()) * P
            d2[need] = ex_d2.reshape(-1, P).sum(1)
            new_codes[need] = ex_idx.reshape(-1, P)
        crossed = need[:, None] & open_k & (d2[:, None] > T2[None, :])
        rows = np.flatnonzero(alive)
        sub = first[rows]
        sub[crossed] = j
        first[rows] = sub
        codes[alive] = new_codes
        if log and j % 200 == 0:
            log(f"  frame {j}/{n_frames}: alive {int(alive.sum())}, exact states so far {n_exact // P}, "
                f"certified {n_cert}")
    return first, dC0, dict(exact_patch_evals=n_exact, certified_state_frames=n_cert, float64_fallback_rows=n_fb)
