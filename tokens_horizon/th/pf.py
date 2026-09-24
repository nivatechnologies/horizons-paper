"""History-conditioned reference: particle filter on token histories with the true dynamics.

Initialised from calibration states in the first observed cell (never from the true state).
Indicator likelihood on the observed cell. When no particle lies in the observed cell the weights
fall back to exp(-d^2 / delta_cell^2) in distance to the observed prototype; every fallback is counted.
Systematic resampling, then rejuvenation jitter of 5% of the cloud's per-coordinate spread.
"""
from __future__ import annotations

import os
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from .systems import DT, flow, get_system
from .tokenize import Codebook


def _run_chunk(args):
    (system, C, calib, labels, toks, M, sub, dt, seed, jitter, delta_cell) = args
    sysm = get_system(system)
    cb = Codebook(C)
    rng = np.random.default_rng(seed)
    L1, n = toks.shape
    d = C.shape[1]
    members = {}
    P = np.empty((n, M, d))
    for i in range(n):
        k = int(toks[0, i])
        if k not in members:
            members[k] = np.where(labels == k)[0]
        P[i] = calib[rng.choice(members[k], M)]
    fallbacks = 0
    rows = np.arange(n)[:, None]
    for j in range(1, L1):
        P = flow(sysm.f, P.reshape(-1, d), sub, dt).reshape(n, M, d)
        pk = cb.encode(P)
        inside = (pk == toks[j][:, None]).astype(float)
        none = inside.sum(1) == 0
        fallbacks += int(none.sum())
        w = inside
        if none.any():
            d2 = ((P[none] - C[toks[j][none]][:, None, :]) ** 2).sum(-1)
            w[none] = np.exp(-(d2 - d2.min(1, keepdims=True)) / delta_cell ** 2)
        w = w / w.sum(1, keepdims=True)
        cdf = np.cumsum(w, 1)
        cdf[:, -1] = 1.0
        u = (np.arange(M)[None, :] + rng.random((n, 1))) / M
        idx = np.empty((n, M), int)
        for i in range(n):
            idx[i] = np.searchsorted(cdf[i], u[i])
        idx = np.clip(idx, 0, M - 1)
        P = P[rows, idx]
        P = P + jitter * P.std(1, keepdims=True) * rng.standard_normal(P.shape)
    return P.mean(1), P.std(1), fallbacks


def particle_filter(system, cb: Codebook, calib, labels, toks, M, sub, seed, dt=DT, jitter=0.05,
                    n_workers=None, chunk=10):
    """toks (L+1, n): observed tokens from the first context frame to t = 0.

    Returns (posterior mean at t = 0 (n, d), posterior spread (n, d), fallback events, fallback rate).
    """
    L1, n = toks.shape
    delta_cell = float(np.sqrt(((calib - cb.C[labels]) ** 2).sum(1).mean()))
    n_workers = n_workers or min(64, os.cpu_count() or 1)
    ss = np.random.SeedSequence(seed).spawn((n + chunk - 1) // chunk)
    jobs = []
    for c0, s in zip(range(0, n, chunk), ss):
        jobs.append((system, cb.C, calib, labels, toks[:, c0:c0 + chunk], M, sub, dt,
                     s.generate_state(1)[0], jitter, delta_cell))
    means, sds, fb = [], [], 0
    with ProcessPoolExecutor(n_workers) as ex:
        for m, s, f in ex.map(_run_chunk, jobs):
            means.append(m)
            sds.append(s)
            fb += f
    steps = n * (L1 - 1)
    return np.concatenate(means), np.concatenate(sds), fb, fb / max(steps, 1)
