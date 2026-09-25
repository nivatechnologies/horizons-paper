"""KS E3 evaluation helpers (post-freeze extension): tokenizers, exact bound, decode-and-integrate, persistence.

Output contract (Amendment 1 A2, ext_freeze.yaml ks.output_contract): the scored field is real-space u on the N grid;
decoded states (patch concatenation, whole-state prototype, residual-VQ sum) are scored as is. The decode-and-
integrate reference integrates the decoded current state; the integrator projects its initial condition onto the
retained modes 1..M (this projection applies only to the reference trajectory). At t = 0 the reference output is the
decoded state as is.

Bound (Amendment 1 A1; ks_fix_1): th/patchvq.certified_bound_crossings on the true frames 1..F (shifted by one), so
the future-frame bound is the first crossing at j >= 1 even when frame 0 already crosses; the from-t0 score is 0 where
the exact d_C(x_0) > eps*sigma_A, otherwise the future score; p_0 from the same exact d_C(x_0).
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import torch
from scipy.spatial import cKDTree

from . import config
from . import ks as K
from .patchvq import certified_bound_crossings, code_neighbours, exact_nn, to_patches_1d

CACHE = config.CACHE / "ext_ks"
CB = config.RUNS / "ext" / "ks" / "codebooks"
EPS = (0.1, 0.3, 0.5)


# ------------------------------------------------------------------------------------------------ tokenizers
class Tok:
    """family in {whole, patch, rvq}. For whole and patch: P patches (whole: P = 1) and codebook C (K, N/P)."""

    def __init__(self, name):
        self.name = name
        z = np.load(CB / f"{name}.npz")
        self.meta = json.loads(str(z["meta"]))
        parts = name.split("_")
        self.system = parts[0]
        self.family = parts[1]
        if self.family == "whole":
            self.P, self.b = 1, int(parts[2][1:])
            self.C = z["C"]
            self.bits = self.b
        elif self.family == "patch":
            self.P, self.b = int(parts[2][1:]), int(parts[3][1:])
            self.C = z["C"]
            self.bits = self.P * self.b
        else:  # rvq: stages 1..s
            self.stages = int(parts[2][1:])
            self.Cs = [np.load(CB / f"{self.system}_rvq_s{s}.npz")["C"] for s in range(1, self.stages + 1)]
            self.P, self.b, self.bits = None, 8, 8 * self.stages
        self.has_bound = self.family in ("whole", "patch")

    def device_codes(self, device):
        Ct = torch.as_tensor(self.C, dtype=torch.float32, device=device)
        return dict(C64=np.asarray(self.C, float), C32=Ct, cn=(Ct * Ct).sum(1))

    def decode_nearest(self, U, device):
        """Exact nearest decoding of states U (n, N). Returns decoded (n, N) and, for whole/patch, exact d_C (n,)."""
        if self.family == "rvq":
            R = U.copy()
            out = np.zeros_like(U)
            for C in self.Cs:
                _, lab = cKDTree(C).query(R, workers=16)
                out += C[lab]
                R -= C[lab]
            return out, None
        Xp = to_patches_1d(U, self.P)
        n, P, d = Xp.shape
        idx, d2, _ = exact_nn(Xp.reshape(-1, d), self.device_codes(device), device)
        dec = self.C[idx].reshape(n, P * d)
        return dec, np.sqrt(d2.reshape(n, P).sum(1))


# ------------------------------------------------------------------------------------------------ data
def panel(system, block, delta):
    """(traj (n, frames, N) memmap, pre index) for one frame grid."""
    s = K.ks_spec(system)
    pres = np.load(CACHE / f"panel_{block}_{system}_pre.npy")
    i = [float(d) for d in s["frame_intervals"]].index(float(delta))
    arr = np.load(CACHE / f"panel_{block}_{system}_d{delta:g}.npy", mmap_mode="r")
    return arr, int(pres[i])


def lam(system):
    return float(K.ks_spec(system)["lyapunov"]["lam_max"])


def W():
    return float(config.freeze()["scoring"]["window_lyapunov_times"])


def n_future(system, delta):
    return int(math.ceil(W() / lam(system) / delta - 1e-9))


def sigma_A(system):
    return float(json.loads((config.RESULTS / "ext" / "ks" / "data_blocks.json").read_text())[system]["sigma_A"])


# ------------------------------------------------------------------------------------------------ scoring
def h_from_first(first, lam_, delta, F):
    """Mirror of th/score.horizon for a first-crossing frame index (F + 1 = never within the F future frames)."""
    Wl = W()
    j = np.where(first <= F, first, F + 1)
    H = np.minimum(lam_ * j * delta, Wl)
    crossed = (first <= F) & (lam_ * j * delta < Wl)
    return H, crossed


def survival(H, crossed, taus=(1.0, 3.0, 10.0)):
    """Amendment 2 B4: S(tau) = P(lambda T_out > tau); censored states survive for tau <= W."""
    return {f"S{tau:g}": float(np.mean(~crossed | (H > tau))) for tau in taus if tau <= W()}


def bound(tok, system, block, delta, sA, device, n=None):
    """Exact output-support bound on a panel. Returns dict eps -> dict(future H, crossed, from_t0 H, crossed), dC0."""
    arr, pre = panel(system, block, delta)
    F = n_future(system, delta)
    assert pre + F < arr.shape[1], "panel too short"
    nn = arr.shape[0] if n is None else n
    fut = np.asarray(arr[:nn, pre: pre + F + 1])                       # frames 0..F
    x0p = to_patches_1d(fut[:, 0], tok.P)
    _, d20, _ = exact_nn(x0p.reshape(-1, x0p.shape[-1]), tok.device_codes(device), device)
    dC0 = np.sqrt(d20.reshape(nn, tok.P).sum(1))
    nbr = code_neighbours(tok.C, device=device)
    thr = [e * sA for e in EPS]
    first, _, cnt = certified_bound_crossings(lambda j: to_patches_1d(fut[:, j + 1], tok.P), F - 1, tok.C, thr,
                                              nbr=nbr, device=device)
    # first[:, k] in 0..F-1 means crossing at frame first+1; F means none in frames 1..F
    lam_ = lam(system)
    out = {}
    for k, e in enumerate(EPS):
        fj = np.where(first[:, k] <= F - 1, first[:, k] + 1, F + 1)
        Hf, cf = h_from_first(fj, lam_, delta, F)
        p0 = dC0 > e * sA
        H0 = np.where(p0, 0.0, Hf)
        c0 = np.where(p0, True, cf)
        out[e] = dict(future=(Hf, cf), from_t0=(H0, c0), p0=p0)
    return out, dC0, cnt


def horizons_from_err(err, lam_, delta):
    """err (F+1, n) from t = 0. Returns eps -> dict(future, from_t0) of (H, crossed) via th/score.horizon."""
    from .score import horizon
    out = {}
    for e in EPS:
        out[e] = dict(future=horizon(err, lam_, delta, W(), e, 1), from_t0=horizon(err, lam_, delta, W(), e, 0))
    return out


# ------------------------------------------------------------------------------------------------ decode-and-integrate
def _di_job(args):
    system, dec0, plan = args
    s = K.ks_spec(system)
    ks = K.KS(s["L"], s["N"], s["dt"])
    v = ks.to_spec(dec0)                                    # projection onto modes 1..M (reference trajectory only)
    n_steps = max(int(ix[-1]) for ix in plan.values())
    out, _ = K.integrate_record(ks, v, n_steps, plan)
    return out


def di_trajectories(system, dec0, pool, nproc):
    """Integrate decoded states dec0 (n, N); frames on every frame grid for j = 0..F (frame 0 replaced by dec0 as is)."""
    s = K.ks_spec(system)
    plan = {}
    for d in s["frame_intervals"]:
        sub = K.steps(d, s["dt"])
        plan[f"{d:g}"] = sub * np.arange(0, n_future(system, d) + 1)
    chunks = np.array_split(np.arange(len(dec0)), nproc)
    parts = list(pool.map(_di_job, [(system, dec0[c], plan) for c in chunks]))
    out = {k: np.concatenate([p[k] for p in parts], 0) for k in plan}
    for k in out:
        out[k][:, 0] = dec0
    return out
