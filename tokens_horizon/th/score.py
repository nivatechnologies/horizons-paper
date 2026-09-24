"""Horizon scoring on the frame grid, restricted means, paired bootstrap and the frozen margins.

Error at frame j: e_j = ||xhat_j - x_j|| / sigma_A. Horizon T = first frame time j*Delta (j >= start)
with e_j > eps. Score lambda*T, restricted to the window W: H = min(lambda*T, W). States that do not
cross within W score W and are counted as non-crossing.
"""
from __future__ import annotations

import numpy as np

from . import config


def err_rel(xhat, x, sA):
    return np.linalg.norm(xhat - x, axis=-1) / sA


def horizon(err, lam, delta, W, eps=None, start=1):
    """err (F+1, n) indexed from t = 0. Returns (H (n,), crossed (n,) bool)."""
    if eps is None:
        eps = config.freeze()["scoring"]["eps_primary"]
    e = err[start:] > eps
    any_ = e.any(0)
    j = np.where(any_, e.argmax(0) + start, err.shape[0])
    H = np.minimum(lam * j * delta, W)
    crossed = any_ & (lam * j * delta < W)
    return H, crossed


def horizon_all(err, lam, delta, W):
    """Primary and secondary scores at every frozen eps. Returns nested dict of per-state arrays."""
    sc = config.freeze()["scoring"]
    out = {}
    for eps in [sc["eps_primary"]] + sc["eps_secondary"]:
        for tag, start in (("future", sc["primary_start_frame"]), ("from_t0", sc["secondary_start_frame"])):
            H, c = horizon(err, lam, delta, W, eps, start)
            out[f"eps{eps}_{tag}"] = dict(H=H, crossed=c)
    return out


def summary(H, crossed):
    return dict(restricted_mean=float(np.mean(H)), frac_no_cross=float(1 - np.mean(crossed)), n=int(len(H)),
                median=float(np.median(H)))


def _rng():
    return np.random.default_rng(config.freeze()["seeds"]["bootstrap_seed"])


def bootstrap_mean(H, reps=None, ci=0.95, seeds_axis=False):
    """H (n,) or (S, n) for S model seeds. Resamples whole trajectories (states) and seeds."""
    reps = reps or config.freeze()["seeds"]["bootstrap_reps"]
    rng = _rng()
    H = np.atleast_2d(H)
    S, n = H.shape
    stats = np.empty(reps)
    for r in range(reps):
        si = rng.integers(0, S, S) if S > 1 else np.zeros(1, int)
        ni = rng.integers(0, n, n)
        stats[r] = H[np.ix_(si, ni)].mean()
    a = (1 - ci) / 2
    return float(H.mean()), float(np.quantile(stats, a)), float(np.quantile(stats, 1 - a))


def paired_diff(Ha, Hb, reps=None):
    """Paired bootstrap of mean(Ha) - mean(Hb) on the same states.

    Ha, Hb: (n,) or (Sa, n) / (Sb, n). Seeds are resampled independently per arm (different models),
    states jointly (same states). Returns point estimate and the 90% and 95% intervals.
    """
    reps = reps or config.freeze()["seeds"]["bootstrap_reps"]
    rng = _rng()
    Ha, Hb = np.atleast_2d(Ha), np.atleast_2d(Hb)
    n = Ha.shape[1]
    assert Hb.shape[1] == n, "paired comparison needs the same states"
    d = np.empty(reps)
    for r in range(reps):
        ni = rng.integers(0, n, n)
        sa = rng.integers(0, Ha.shape[0], Ha.shape[0])
        sb = rng.integers(0, Hb.shape[0], Hb.shape[0])
        d[r] = Ha[np.ix_(sa, ni)].mean() - Hb[np.ix_(sb, ni)].mean()
    pt = float(Ha.mean() - Hb.mean())
    return dict(diff=pt, ci90=(float(np.quantile(d, 0.05)), float(np.quantile(d, 0.95))),
                ci95=(float(np.quantile(d, 0.025)), float(np.quantile(d, 0.975))))


def reading(pd):
    """Frozen margin reading of a paired difference (a - b). Section 2.8 only; no other words."""
    m = config.freeze()["margins"]
    lo90, hi90 = pd["ci90"]
    lo95, hi95 = pd["ci95"]
    tags = []
    if lo90 >= -m["approx_equal"]["half_width"] and hi90 <= m["approx_equal"]["half_width"]:
        tags.append("approximately equal")
    if -pd["diff"] >= m["well_below"]["min_diff"] and hi95 < 0:
        tags.append("a well below b")
    if pd["diff"] >= m["well_below"]["min_diff"] and lo95 > 0:
        tags.append("b well below a")
    return tags or ["no frozen reading applies (a non-significant difference is not equivalence)"]


def near(pd_ref_minus_model):
    """Model near a bound/reference: upper 95% limit of (reference - model) within 0.15."""
    return pd_ref_minus_model["ci95"][1] <= config.freeze()["margins"]["near"]["upper_limit"]


def outlast(H_forecaster, H_bound):
    """Per-state strict outlast fraction and tie fraction (forecaster vs bound, same states)."""
    Ha, Hb = np.atleast_2d(H_forecaster), np.asarray(H_bound)
    return dict(outlast=float((Ha > Hb[None]).mean()), ties=float((Ha == Hb[None]).mean()))
