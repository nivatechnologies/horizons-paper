"""Exchange-law helpers (Task 2.4 / 2.5): quantization distortion, perturbation horizons, decode-and-integrate.

New module; it only composes the frozen library (config, data, score, systems, tokenize).
All horizons are scored with score.horizon on a frame grid of interval Delta (future frames, eps from the freeze,
W = 27 Lyapunov times), exactly like every other horizon in the package.
"""
from __future__ import annotations

import json
import os

import numpy as np

from . import config, data, score
from .systems import DT, flow, get_system, rk4, rk4_tangent

KDTREE_WORKERS = int(os.environ.get("TH_KDTREE_WORKERS", "4"))   # keep CPU use bounded (library default is all cores)


def nearest(cb, X, workers=None):
    """Exact nearest-prototype quantization with a bounded worker count. Returns (Xq, dist)."""
    shp = X.shape
    dd, idx = cb._tree.query(X.reshape(-1, shp[-1]), workers=workers or KDTREE_WORKERS)
    return cb.C[idx].reshape(shp), dd.reshape(shp[:-1])


def W():
    return float(config.freeze()["scoring"]["window_lyapunov_times"])


def eps0():
    return float(config.freeze()["scoring"]["eps_primary"])


def n_frames(system, delta):
    return data.n_future_frames(system, delta)


def integrate_pair_err(system, X_ref, X_pert, delta, sA):
    """Integrate reference states X_ref (n, d) and perturbed states X_pert (m*n, d) (m blocks, each aligned with
    X_ref) on the frame grid; return err (F+1, m*n) = ||x_pert - x_ref|| / sA at frames 0..F."""
    f = get_system(system).f
    sub = int(round(delta / DT))
    F = n_frames(system, delta)
    n = X_ref.shape[0]
    m = X_pert.shape[0] // n
    x = np.concatenate([X_ref, X_pert])
    err = np.empty((F + 1, m * n))
    err[0] = np.linalg.norm(x[n:].reshape(m, n, -1) - x[:n][None], axis=-1).ravel() / sA
    for j in range(1, F + 1):
        x = flow(f, x, sub)
        err[j] = np.linalg.norm(x[n:].reshape(m, n, -1) - x[:n][None], axis=-1).ravel() / sA
    return err


def perturbation_horizons(system, X, U, rel_deltas, sA, delta=0.02):
    """H_W for states X (n, d) perturbed by rel_delta * sA * U (U unit rows), for every rel_delta.
    Returns H (len(rel_deltas), n), crossed (same shape)."""
    lam = config.lam(system)
    Xp = np.concatenate([X + dl * sA * U for dl in rel_deltas])
    err = integrate_pair_err(system, X, Xp, delta, sA)
    H, c = score.horizon(err, lam, delta, W(), eps0(), start=config.freeze()["scoring"]["primary_start_frame"])
    return H.reshape(len(rel_deltas), -1), c.reshape(len(rel_deltas), -1)


def decode_integrate(system, quantize, delta=0.02, panel_block="confirmation"):
    """Decode-and-integrate reference: x_hat_0 = quantize(x_0) on the panel, integrated with the true system and
    scored against the panel's own future frames. Returns H (n,), crossed (n,), rel quantization error (n,)."""
    lam = config.lam(system)
    sA = data.sigma_A(system)
    pnl = data.panel(system, panel_block)
    _, fut = data.frames(pnl, delta)
    F = min(n_frames(system, delta), fut.shape[0] - 1)
    fut = fut[:F + 1]
    rec = quantize(fut[0])
    f = get_system(system).f
    sub = int(round(delta / DT))
    x = rec.copy()
    err = np.empty((F + 1, len(rec)))
    err[0] = score.err_rel(x, fut[0], sA)
    for j in range(1, F + 1):
        x = flow(f, x, sub)
        err[j] = score.err_rel(x, fut[j], sA)
    H, c = score.horizon(err, lam, delta, W(), eps0(), start=config.freeze()["scoring"]["primary_start_frame"])
    return H, c, err[0].copy(), pnl["sha"]


def h_states(system):
    """Fixed 1,000-state calibration subset (seed = calibration seed stream 7). Returns (idx, X, traj)."""
    fz = config.freeze()["exchange_law"]
    X, traj = data.calibration(system)
    rng = np.random.default_rng(config.seed("calibration", system, 7))
    idx = rng.choice(len(X), fz["calibration_states"], replace=False)
    return idx, X[idx], traj[idx]


def state_back_in_time(system, idx, steps_back):
    """Calibration state `steps_back` integrator steps before calibration state idx, on the same physical trajectory.

    Calibration sample i of trajectory k sits (i+1)*stride steps after the burned start, which itself is
    burn_in steps after the Gaussian start. States earlier than the first stored sample are regenerated from the
    Gaussian start with the same RK4 steps (per-row arithmetic is independent of batch composition)."""
    fz = config.freeze()
    c = fz["blocks"]["calibration"]
    stride, S = c["sample_every_steps"], c["samples_per_traj"]
    X, traj = data.calibration(system)
    sysm = get_system(system)
    rng = np.random.default_rng(config.seed("calibration", system, 0))
    g0 = sysm.gaussian_starts(rng, c["n_traj"])
    out = np.empty((len(idx), sysm.d))
    k = traj[idx]
    i = idx - k * S
    steps_from_gauss = fz["integration"]["burn_in_steps"] + (i + 1) * stride - steps_back
    # use a stored sample when the earlier state is itself a stored sample
    back_samples = steps_back // stride
    stored = (steps_back % stride == 0) & (i >= back_samples)
    out[stored] = X[idx[stored] - back_samples]
    todo = np.where(~stored)[0]
    if len(todo):
        order = todo[np.argsort(steps_from_gauss[todo])]
        x = g0[k[order]].copy()
        done = 0
        for j, o in enumerate(order):
            need = steps_from_gauss[o] - done
            if need > 0:
                x[j:] = flow(sysm.f, x[j:], int(need))
                done = steps_from_gauss[o]
            out[o] = x[j]
    return out


def evolve_tangent(system, X0, steps, rng, renorm_every=10):
    """Integrate states X0 with one random unit tangent vector each. Returns (X_end, unit tangent at end)."""
    sysm = get_system(system)
    x = X0.copy()
    v = rng.standard_normal(X0.shape)[..., None]
    v /= np.linalg.norm(v, axis=1, keepdims=True)
    for s in range(1, steps + 1):
        x, v = rk4_tangent(sysm.f, sysm.jac, x, v)
        if s % renorm_every == 0:
            v /= np.linalg.norm(v, axis=1, keepdims=True)
    u = v[..., 0] / np.linalg.norm(v[..., 0], axis=1, keepdims=True)
    return x, u


def fsle(system, X, U, sA, start_rel=1e-9, top_rel=1.0, t_max=None):
    """Classical FSLE by first-passage times through doubling levels (per dt step), no renormalisation.
    Returns levels (L,), first-passage times (L, n) (nan if not reached)."""
    f = get_system(system).f
    lam = config.lam(system)
    levels = start_rel * 2.0 ** np.arange(0, 64)
    levels = levels[levels <= top_rel]
    t_max = t_max or 45.0 / lam
    x, y = X.copy(), X + start_rel * sA * U
    first = np.full((len(levels), len(X)), np.nan)
    for s in range(1, int(round(t_max / DT)) + 1):
        x, y = rk4(f, x), rk4(f, y)
        e = np.linalg.norm(y - x, axis=1) / sA
        hit = np.isnan(first) & (e[None] > levels[:, None])
        first[hit] = s * DT
        if not np.isnan(first[-1]).any():
            break
    return levels, first


def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=1))


def write_csv(path, rows, header_comment=None):
    """rows: list of dicts with identical keys. First line is a '# sha=...' comment."""
    path.parent.mkdir(parents=True, exist_ok=True)
    keys = list(rows[0].keys())
    lines = [f"# git_sha={config.git_sha()}" + (f"; {header_comment}" if header_comment else "")]
    lines.append(",".join(keys))
    for r in rows:
        lines.append(",".join("" if r[k] is None else (f"{r[k]:.10g}" if isinstance(r[k], float) else str(r[k]))
                              for k in keys))
    path.write_text("\n".join(lines) + "\n")
