"""Tokenizers fitted on calibration states: k-means codebooks, scalar quantization, residual VQ."""
from __future__ import annotations

import json

import numpy as np
from scipy.spatial import cKDTree
from sklearn.cluster import KMeans

from . import config, data


class Codebook:
    def __init__(self, C, meta=None):
        self.C = np.asarray(C, float)
        self.meta = meta or {}
        self._tree = cKDTree(self.C)

    @property
    def K(self):
        return len(self.C)

    def encode(self, X):
        shp = X.shape[:-1]
        _, idx = self._tree.query(X.reshape(-1, X.shape[-1]), workers=-1)
        return idx.reshape(shp)

    def dist(self, X):
        """d_C(x) = min_j ||x - c_j||"""
        shp = X.shape[:-1]
        dd, _ = self._tree.query(X.reshape(-1, X.shape[-1]), workers=-1)
        return dd.reshape(shp)

    def decode(self, idx):
        return self.C[idx]

    def quantize(self, X):
        return self.C[self.encode(X)]


def kmeans_codebook(system, bits) -> Codebook:
    fz = config.freeze()["tokenizers"]["kmeans"]
    p = config.CACHE / f"kmeans_{system}_{bits}.npz"
    if p.exists():
        z = np.load(p, allow_pickle=False)
        return Codebook(z["C"], json.loads(str(z["meta"])))
    X, _ = data.calibration(system)
    km = KMeans(n_clusters=2 ** bits, n_init=fz["n_init"], max_iter=fz["max_iter"], tol=fz["tol"],
                random_state=bits).fit(X)
    meta = dict(n_iter=int(km.n_iter_), inertia=float(km.inertia_), bits=bits, system=system)
    np.savez(p, C=km.cluster_centers_, labels=km.labels_, meta=json.dumps(meta))
    return Codebook(km.cluster_centers_, meta)


def kmeans_labels(system, bits):
    kmeans_codebook(system, bits)
    return np.load(config.CACHE / f"kmeans_{system}_{bits}.npz")["labels"]


class ScalarQuantizer:
    """Uniform bins per coordinate over the calibration range, decoded to calibration cell means."""

    def __init__(self, system, levels):
        X, _ = data.calibration(system)
        self.d, self.n = X.shape[1], levels
        self.lo, self.hi = X.min(0), X.max(0)
        self.edges = [np.linspace(self.lo[j], self.hi[j], levels + 1)[1:-1] for j in range(self.d)]
        c = self.code(X)
        uniq, inv = np.unique(c, return_inverse=True)
        means = np.zeros((len(uniq), self.d))
        np.add.at(means, inv, X)
        means /= np.bincount(inv)[:, None]
        self.lookup = dict(zip(uniq.tolist(), range(len(uniq))))
        self.means = means
        self.rate_nominal = self.d * np.log2(levels)
        self.used = len(uniq)

    def code(self, X):
        idx = np.stack([np.searchsorted(self.edges[j], X[:, j]) for j in range(self.d)], 1)
        return np.ravel_multi_index(idx.T, (self.n,) * self.d)

    def quantize(self, X):
        shp = X.shape
        X = X.reshape(-1, self.d)
        c = self.code(X)
        out = np.empty_like(X)
        w = (self.hi - self.lo) / self.n
        for i, ci in enumerate(c):
            j = self.lookup.get(int(ci))
            if j is None:        # unseen cell: geometric centre
                out[i] = self.lo + (np.array(np.unravel_index(ci, (self.n,) * self.d)) + 0.5) * w
            else:
                out[i] = self.means[j]
        return out.reshape(shp)


class ResidualVQ:
    """Stages of 2^8-code k-means on successive calibration residuals."""

    def __init__(self, system, stages):
        tz = config.freeze()["tokenizers"]
        X, _ = data.calibration(system)
        self.books = []
        R = X.copy()
        for s in range(stages):
            p = config.CACHE / f"rvq_{system}_stage{s}.npz"
            if p.exists():
                C = np.load(p)["C"]
            else:
                km = KMeans(n_clusters=2 ** tz["rvq_bits_per_stage"], n_init=1, max_iter=tz["kmeans"]["max_iter"],
                            tol=tz["kmeans"]["tol"], random_state=tz["rvq_random_state_base"] + s).fit(R)
                C = km.cluster_centers_
                np.savez(p, C=C)
            cb = Codebook(C)
            self.books.append(cb)
            R = R - cb.quantize(R)
        self.bits = stages * tz["rvq_bits_per_stage"]

    def quantize(self, X):
        shp = X.shape
        R = X.reshape(-1, shp[-1]).copy()
        out = np.zeros_like(R)
        for cb in self.books:
            q = cb.quantize(R)
            out += q
            R -= q
        return out.reshape(shp)
