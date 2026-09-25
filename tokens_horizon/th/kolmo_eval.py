"""Kolmogorov flow E3 helpers (post-freeze extension; ext_freeze.yaml `kolmogorov`, Amendments 1-2, ks_fix_1).

Storage (runs/cache/ext_kolmo/, not in git):
  calib_fit.npy (204800, 64, 64) float64 grid vorticity, calib_fit_traj.npy; calib_heldout.npy, calib_heldout_traj.npy
  panel_confirmation.npy (3731, 1000, 43, 22) complex128, frame-major: the exact retained Fourier coefficients of the
  integrator state (|kx|, |ky| <= 21, rfft2 layout) every 0.07 tu from t = -46.2 (unit 0) to t = +214.9; t = 0 is unit
  PRE_UNITS = 660. Grids are reconstructed by numpy irfft2 in float64 (this grid is the scored true state).

Output contract (Amendment 1 A2; kolmogorov.output_contract): the scored field is vorticity on the 64 x 64 grid, norm
= Euclidean over the 4,096 values; decoded states (patch concatenation or residual-VQ sum) are scored as is. The
decode-and-integrate reference integrates the decoded current state; the integrator's Galerkin projection (dealias
mask, mean removal) acts on its initial condition, which applies to the reference trajectory only. At t = 0 the
reference output is the decoded state as is.

Bound (A1; ks_fix_1 future-frame convention): th/patchvq.certified_bound_crossings on true frames 1..F (shifted by one);
from-t0 = 0 where the exact d_C(x_0) > eps sigma_A, else the future score; p_0 from the exact d_C(x_0).
"""
from __future__ import annotations

import json
import math

import numpy as np
import torch
import yaml

from . import config
from . import kolmogorov as KM
from .patchvq import certified_bound_crossings, code_neighbours, exact_nn, from_patches_2d, to_patches_2d

CACHE = config.CACHE / "ext_kolmo"
RUNS = config.RUNS / "ext" / "kolmo"
CB = RUNS / "codebooks"
RES = config.RESULTS / "ext" / "kolmo"
EPS = (0.1, 0.3, 0.5)
N = 64
KM_ = 21                                 # retained |k| <= 21
KY_IDX = np.r_[0:KM_ + 1, N - KM_:N]     # 43 rows of the rfft2 array
UNIT = 0.07


def spec():
    return yaml.safe_load((config.PKG / "ext_freeze.yaml").read_text())["kolmogorov"]


def lam():
    return float(spec()["lyapunov"]["lam_max"])


def W():
    return float(config.freeze()["scoring"]["window_lyapunov_times"])


def units(t):
    u = t / UNIT
    assert abs(u - round(u)) < 1e-9, t
    return int(round(u))


def pre_units():
    return units(float(spec()["pre_history_time"]))


def n_future(delta):
    return int(math.ceil(W() / lam() / delta - 1e-9))


def sigma_A():
    return float(json.loads((RES / "data_blocks.json").read_text())["sigma_A"])


def seed(block, stream):
    return KM.seed(block, stream)


# ------------------------------------------------------------------------------------------------ storage
def pack(wh):
    """(B, 64, 33) complex spectral state -> (B, 43, 22) retained coefficients (numpy complex128)."""
    if isinstance(wh, torch.Tensor):
        wh = wh.detach().cpu().numpy()
    return np.ascontiguousarray(wh[:, KY_IDX, :KM_ + 1]).astype(np.complex128)


def unpack(c):
    out = np.zeros(c.shape[:-2] + (N, N // 2 + 1), np.complex128)
    out[..., KY_IDX, :KM_ + 1] = c
    return out


def grid(c):
    """Retained coefficients (..., 43, 22) -> float64 grid (..., 64, 64) (numpy irfft2)."""
    return np.fft.irfft2(unpack(c), s=(N, N))


class Panel:
    """Confirmation panel: frame(j, delta) -> (n, 64, 64) float64 truth at t = j*delta."""

    def __init__(self, n=None, block="confirmation"):
        self.Z = np.load(CACHE / f"panel_{block}.npy", mmap_mode="r")
        self.n = self.Z.shape[1] if n is None else n
        self.pre = pre_units()

    def unit(self, k):
        return grid(np.asarray(self.Z[self.pre + k, :self.n]))

    def frame(self, j, delta):
        return self.unit(j * units(delta))


# ------------------------------------------------------------------------------------------------ tokenizers
LAYOUTS = {"4x4": 4, "8x8": 8, "16x16": 16}       # patches per side; P = side^2 patches


class Tok:
    """name: kolmo_patch_L{side}_b{b}[_half]  or  kolmo_rvq_s{stages}."""

    def __init__(self, name, C=None):
        self.name = name
        parts = name.split("_")
        self.family = parts[1]
        if self.family == "patch":
            self.side = int(parts[2][1:])
            self.P = self.side ** 2
            self.b = int(parts[3][1:])
            self.bits = self.P * self.b
            z = np.load(CB / f"{name}.npz")
            self.C = z["C"] if C is None else C
            self.meta = json.loads(str(z["meta"]))
            self.layout = f"{self.side}x{self.side}"
        else:
            self.stages = int(parts[2][1:])
            self.Cs = [np.load(CB / f"kolmo_rvq_s{s}.npz")["C"] for s in range(1, self.stages + 1)]
            self.P, self.b, self.bits, self.layout = None, 8, 8 * self.stages, "whole"
            self.meta = json.loads(str(np.load(CB / f"kolmo_rvq_s{self.stages}.npz")["meta"]))
        self.has_bound = self.family == "patch"

    def patches(self, Wg):
        return to_patches_2d(Wg, self.side, self.side)

    def device_codes(self, C, device):
        Ct = torch.as_tensor(C, dtype=torch.float32, device=device)
        return dict(C64=np.asarray(C, float), C32=Ct, cn=(Ct * Ct).sum(1))

    def decode_nearest(self, Wg, device):
        """Exact nearest decoding of grids Wg (n, 64, 64). Returns decoded (n, 64, 64), exact d_C (n,) or None,
        and the code labels."""
        n = len(Wg)
        if self.family == "rvq":
            R = Wg.reshape(n, -1).copy()
            out = np.zeros_like(R)
            labs = []
            for C in self.Cs:
                idx, _, _ = exact_nn(R, self.device_codes(C, device), device)
                out += C[idx]
                R -= C[idx]
                labs.append(idx)
            return out.reshape(n, N, N), None, np.stack(labs, 1)
        Xp = self.patches(Wg)
        _, P, d = Xp.shape
        idx, d2, _ = exact_nn(Xp.reshape(-1, d), self.device_codes(self.C, device), device)
        dec = from_patches_2d(self.C[idx].reshape(n, P, d), self.side, self.side, N, N)
        return dec, np.sqrt(d2.reshape(n, P).sum(1)), idx.reshape(n, P)


# ------------------------------------------------------------------------------------------------ scoring
def h_from_first(first, delta, F):
    Wl, l = W(), lam()
    j = np.where(first <= F, first, F + 1)
    H = np.minimum(l * j * delta, Wl)
    crossed = (first <= F) & (l * j * delta < Wl)
    return H, crossed


def survival(H, crossed, taus=(1.0, 3.0, 10.0)):
    """Amendment 2 B4: S(tau) = P(lambda T_out > tau); censored states survive for tau <= W."""
    return {f"S{tau:g}": float(np.mean(~crossed | (H > tau))) for tau in taus if tau <= W()}


def bound(tok, pnl, delta, sA, device, C=None, log=None):
    """Exact output-support bound (future frames 1..F; from-t0 via exact d_C(x_0))."""
    C = tok.C if C is None else C
    F = n_future(delta)
    ct = tok.device_codes(C, device)
    x0p = tok.patches(pnl.frame(0, delta))
    n, P, d = x0p.shape
    _, d20, _ = exact_nn(x0p.reshape(-1, d), ct, device)
    dC0 = np.sqrt(d20.reshape(n, P).sum(1))
    nbr = code_neighbours(C, device=device)
    thr = [e * sA for e in EPS]
    first, _, cnt = certified_bound_crossings(lambda j: tok.patches(pnl.frame(j + 1, delta)), F - 1, C, thr,
                                              nbr=nbr, device=device, log=log)
    out = {}
    for k, e in enumerate(EPS):
        fj = np.where(first[:, k] <= F - 1, first[:, k] + 1, F + 1)
        Hf, cf = h_from_first(fj, delta, F)
        p0 = dC0 > e * sA
        out[e] = dict(future=(Hf, cf), from_t0=(np.where(p0, 0.0, Hf), np.where(p0, True, cf)), p0=p0)
    return out, dC0, cnt


def horizons_from_err(err, delta):
    from .score import horizon
    return {e: dict(future=horizon(err, lam(), delta, W(), e, 1), from_t0=horizon(err, lam(), delta, W(), e, 0))
            for e in EPS}


# ------------------------------------------------------------------------------------------------ references
def persistence_err(dec0, pnl, delta, sA):
    F = n_future(delta)
    err = np.empty((F + 1, len(dec0)))
    for j in range(F + 1):
        err[j] = np.sqrt(((pnl.frame(j, delta) - dec0) ** 2).sum((-2, -1))) / sA
    return err


def di_errors(dec0_list, pnl, sA, device, deltas, dtype=torch.float64, eps_stop=0.5, N_int=64, sub_eval=None,
              log=None):
    """Decode-and-integrate for several decoded initial states at once (list of (n, 64, 64)).

    The decoded grids are transformed (rfft2) and projected by the integrator (dealias mask incl. mean removal):
    reference trajectory only. Frame 0 output = decoded state as is. Errors on every frame grid in `deltas`; the
    integration stops once every state has err > eps_stop at some frame j >= 1 on every grid (all first crossings
    at eps <= eps_stop are then fixed); later frames are filled with +inf.
    N_int = 128: the decoded 64^2 field and nothing else is spectrally zero-padded (resolution check; errors are
    evaluated on the 64^2 collocation points, i.e. every other 128^2 point).
    Returns list of dicts delta -> err (F+1, n)."""
    T = len(dec0_list)
    n = len(dec0_list[0])
    m = KM.Kolmogorov(N=N_int, device=device, dtype=dtype)
    w0 = np.concatenate(dec0_list, 0)
    wh = zero_pad_spec(w0, N_int, m) if N_int != N else m.to_spec(torch.as_tensor(w0))
    subs = {d: units(d) for d in deltas}
    Fs = {d: n_future(d) for d in deltas}
    errs = [{d: np.full((Fs[d] + 1, n), np.inf) for d in deltas} for _ in range(T)]
    done = {d: np.zeros(T * n, bool) for d in deltas}
    steps_per_unit = int(round(UNIT / m.dt))
    k_max = max(Fs[d] * subs[d] for d in deltas)
    truth0 = pnl.unit(0)
    for t in range(T):
        e0 = np.sqrt(((dec0_list[t] - truth0) ** 2).sum((-2, -1))) / sA
        for d in deltas:
            errs[t][d][0] = e0
    for k in range(1, k_max + 1):
        wh = m.flow(wh, steps_per_unit)
        need = [d for d in deltas if k % subs[d] == 0 and k // subs[d] <= Fs[d]]
        if not need:
            continue
        g = m.to_phys(wh)
        if N_int != N:
            g = g[:, ::N_int // N, ::N_int // N]
        g = g.cpu().numpy()
        tr = pnl.unit(k)
        e = np.sqrt(((g.reshape(T, n, N, N) - tr[None]) ** 2).sum((-2, -1))) / sA     # (T, n)
        for d in need:
            j = k // subs[d]
            for t in range(T):
                errs[t][d][j] = e[t]
            done[d] |= e.reshape(-1) > eps_stop
        if all(done[d].all() for d in deltas):
            if log:
                log(f"  DI stop at unit {k} (t = {k * UNIT:.2f})")
            break
        if log and k % 500 == 0:
            log(f"  DI unit {k}/{k_max}, done " + ", ".join(f"{d:g}:{done[d].mean():.3f}" for d in deltas))
    return errs, k


def zero_pad_spec(w0, N_int, m):
    """64^2 grids -> spectral state on N_int^2 (exact trigonometric interpolation of the 64^2 field, Nyquist dropped),
    then the N_int integrator's mask."""
    c = np.fft.rfft2(w0)                                          # (n, 64, 33)
    out = np.zeros((len(w0), N_int, N_int // 2 + 1), np.complex128)
    h = N // 2
    ky_src = np.r_[0:h, h + 1:N]                                  # drop ky = -32 (Nyquist)
    ky_dst = np.r_[0:h, N_int - (h - 1):N_int]
    out[:, ky_dst, :h] = c[:, ky_src, :h]                         # drop kx = 32 (Nyquist)
    out *= (N_int / N) ** 2
    t = torch.as_tensor(out, device=m.device)
    return t * m.mask

