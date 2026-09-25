"""Kuramoto-Sivashinsky system (post-freeze extension, part 2 pilot). float64 throughout.

    u_t = -u u_x - u_xx - u_xxxx   on [0, L), periodic, zero mean.

Discretization
--------------
* Pseudo-spectral Fourier Galerkin on N equispaced grid points x_j = j L / N. The tokenized and scored state is the
  real-space field u(x_j), shape (..., N).
* Dealiasing: Orszag 2/3 rule. Only modes 1 <= m <= M with M = floor((N - 1) / 3) are retained (mode 0 is zero by
  the zero-mean constraint; modes M < m <= N/2, including Nyquist, are identically zero in the state AND in the
  nonlinear term). With N >= 3M + 1 the quadratic product u^2 computed on the N-point grid is alias-free for all
  retained modes, so the scheme integrates the exact Galerkin truncation to 2M real degrees of freedom.
* Time stepping: ETDRK4 (Cox & Matthews 2002) with the contour-integral evaluation of the phi-function coefficients
  of Kassam & Trefethen (2005, SIAM J. Sci. Comput. 26:1214), 64 points on a unit circle around each h*L_m.
* Nonlinear term in Fourier space: N(v) = -(i k / 2) FFT(u^2) (since u u_x = (u^2/2)_x), masked to retained modes.

Tangent dynamics
----------------
`step_tangent` is the exact derivative of the discrete ETDRK4 map (every stage linearized), so Benettin/QR gives the
Lyapunov exponents of the map that generates the trajectories. The nonlinear term's Jacobian is traceless on
zero-mean fields (its diagonal Galerkin entries are proportional to v_0 = 0), so the full 2M-exponent spectrum of the
continuous Galerkin system sums to the trace of the linear operator, 2 * sum_{m=1..M} (k_m^2 - k_m^4), k_m = 2 pi m/L.

Tangent vectors are carried as complex rfft coefficients and orthonormalized in real coordinates
r = sqrt(2/N) [Re v_1..v_M, Im v_1..v_M], for which ||r|| equals the Euclidean norm of the real-space field.

Blocks and panels mirror th/data.py (independent burned-in trajectories per block, disjoint seeds, panels with
pre-history and future, frames subsampled from the stored grid with no interpolation). The confirmation block is
refused until the extension freeze part 2 (ext_freeze.yaml key `ks`) exists.
"""
from __future__ import annotations

import math

import numpy as np
import scipy.fft as sfft
import yaml

from . import config

WORKERS = 1   # scipy.fft workers per call; parallelism is normally across processes


class KS:
    def __init__(self, L: float, N: int, dt: float, n_contour: int = 64):
        assert N % 2 == 0
        self.L, self.N, self.dt = float(L), int(N), float(dt)
        self.M = (N - 1) // 3                               # 2/3 rule: retained modes 1..M
        self.K = N // 2 + 1                                 # rfft length
        m = np.arange(self.K)
        self.k = 2.0 * np.pi * m / self.L
        self.mask = ((m >= 1) & (m <= self.M)).astype(float)
        self.lin = (self.k ** 2 - self.k ** 4) * self.mask
        self.g = -0.5j * self.k * self.mask                 # N(v) = g * FFT(u^2)
        h = self.dt
        hL = h * self.lin
        self.E = np.exp(hL)
        self.E2 = np.exp(hL / 2)
        r = np.exp(1j * np.pi * (np.arange(1, n_contour + 1) - 0.5) / n_contour)
        LR = hL[:, None] + r[None, :]
        self.Q = h * np.real(np.mean((np.exp(LR / 2) - 1) / LR, axis=1))
        self.f1 = h * np.real(np.mean((-4 - LR + np.exp(LR) * (4 - 3 * LR + LR ** 2)) / LR ** 3, axis=1))
        self.f2 = h * np.real(np.mean((2 + LR + np.exp(LR) * (-2 + LR)) / LR ** 3, axis=1))
        self.f3 = h * np.real(np.mean((-4 - 3 * LR - LR ** 2 + np.exp(LR) * (4 - LR)) / LR ** 3, axis=1))
        self.dim = 2 * self.M
        self.trace = float(2.0 * np.sum(self.lin[1:self.M + 1]))

    # ------------------------------------------------------------------ transforms
    def to_real(self, v):
        return sfft.irfft(v, n=self.N, axis=-1, workers=WORKERS)

    def to_spec(self, u):
        return sfft.rfft(u, axis=-1, workers=WORKERS) * self.mask

    def spec_to_coords(self, v):
        s = math.sqrt(2.0 / self.N)
        return s * np.concatenate([v[..., 1:self.M + 1].real, v[..., 1:self.M + 1].imag], axis=-1)

    def coords_to_spec(self, r):
        s = math.sqrt(2.0 / self.N)
        v = np.zeros(r.shape[:-1] + (self.K,), complex)
        v[..., 1:self.M + 1] = (r[..., :self.M] + 1j * r[..., self.M:]) / s
        return v

    # ------------------------------------------------------------------ dynamics
    def nl(self, v):
        u = self.to_real(v)
        return self.g * sfft.rfft(u * u, axis=-1, workers=WORKERS)

    def step(self, v):
        """One ETDRK4 step on spectral states (..., K)."""
        E2, Q = self.E2, self.Q
        Nv = self.nl(v)
        a = E2 * v + Q * Nv
        Na = self.nl(a)
        b = E2 * v + Q * Na
        Nb = self.nl(b)
        c = E2 * a + Q * (2 * Nb - Nv)
        Nc = self.nl(c)
        return self.E * v + Nv * self.f1 + 2 * (Na + Nb) * self.f2 + Nc * self.f3

    def flow(self, v, n):
        for _ in range(n):
            v = self.step(v)
        return v

    def step_tangent(self, v, w):
        """ETDRK4 step and its exact derivative. v (B, K), w (B, p, K) tangent vectors (spectral)."""
        E2, Q, g = self.E2, self.Q, self.g

        def nl_lin(v_, w_):
            u = self.to_real(v_)
            om = self.to_real(w_)
            Nv_ = g * sfft.rfft(u * u, axis=-1, workers=WORKERS)
            dN_ = g * sfft.rfft(2.0 * u[:, None, :] * om, axis=-1, workers=WORKERS)
            return Nv_, dN_

        Nv, dNv = nl_lin(v, w)
        a = E2 * v + Q * Nv
        da = E2 * w + Q * dNv
        Na, dNa = nl_lin(a, da)
        b = E2 * v + Q * Na
        db = E2 * w + Q * dNa
        Nb, dNb = nl_lin(b, db)
        c = E2 * a + Q * (2 * Nb - Nv)
        dc = E2 * da + Q * (2 * dNb - dNv)
        Nc, dNc = nl_lin(c, dc)
        v1 = self.E * v + Nv * self.f1 + 2 * (Na + Nb) * self.f2 + Nc * self.f3
        w1 = self.E * w + dNv * self.f1 + 2 * (dNa + dNb) * self.f2 + dNc * self.f3
        return v1, w1

    # ------------------------------------------------------------------ starts and trajectories
    def small_random_start(self, rng, n, amp=1e-2):
        """Small random initial conditions: amp * N(0, 1) per grid point, projected on the retained zero-mean modes."""
        return self.to_spec(amp * rng.standard_normal((n, self.N)))

    def burned_starts(self, rng, n, burn_time):
        v = self.small_random_start(rng, n)
        return self.flow(v, steps(burn_time, self.dt))

    def trajectory(self, v, n_samples, stride):
        """Real-space states after every `stride` steps, n_samples + 1 of them starting with v: (n, n_samples+1, N)."""
        out = np.empty((v.shape[0], n_samples + 1, self.N))
        out[:, 0] = self.to_real(v)
        for s in range(1, n_samples + 1):
            v = self.flow(v, stride)
            out[:, s] = self.to_real(v)
        return out, v

    # ------------------------------------------------------------------ Lyapunov
    def benettin(self, v0, t_total, n_exp, renorm_every=1, burn_time=0.0, rng=None, return_series=False):
        """Leading n_exp exponents by Benettin/QR on the discrete-map tangent. v0 (B, K) spectral starts.

        Returns per-start spectra (B, n_exp); with return_series also the running estimates of lambda_1 per start
        at each renormalization (for convergence checks)."""
        rng = rng or np.random.default_rng(0)
        v = self.flow(v0.copy(), steps(burn_time, self.dt))
        B = v.shape[0]
        Qr, _ = np.linalg.qr(rng.standard_normal((B, self.dim, n_exp)))
        w = self.coords_to_spec(np.swapaxes(Qr, 1, 2))          # (B, p, K)
        sums = np.zeros((B, n_exp))
        n_steps = steps(t_total, self.dt)
        series = []
        for s in range(1, n_steps + 1):
            v, w = self.step_tangent(v, w)
            if s % renorm_every == 0 or s == n_steps:
                R_in = np.swapaxes(self.spec_to_coords(w), 1, 2)   # (B, dim, p)
                Qr, R = np.linalg.qr(R_in)
                d = np.diagonal(R, axis1=-2, axis2=-1)
                sums += np.log(np.abs(d))
                w = self.coords_to_spec(np.swapaxes(Qr, 1, 2))
                if return_series:
                    series.append(sums[:, 0] / (s * self.dt))
        spec = sums / (n_steps * self.dt)
        if return_series:
            return spec, np.array(series)
        return spec


def steps(t, dt):
    n = t / dt
    if abs(n - round(n)) > 1e-9:
        raise ValueError(f"time {t} is not an integer multiple of dt {dt}")
    return int(round(n))


def kaplan_yorke(spec):
    spec = np.sort(np.asarray(spec))[::-1]
    cs = np.cumsum(spec)
    if cs[0] < 0:
        return 0.0
    j = int(np.max(np.where(cs >= 0)[0])) + 1
    if j >= len(spec):
        return float("nan")      # spectrum too short to close the sum
    return float(j + cs[j - 1] / abs(spec[j]))


# ---------------------------------------------------------------------- blocks and panels (freeze-conditional)
def ext_freeze() -> dict:
    return yaml.safe_load((config.PKG / "ext_freeze.yaml").read_text())


def ks_spec(system: str) -> dict:
    """The frozen KS settings for `system` (ext_freeze.yaml part 2 key `ks`)."""
    ef = ext_freeze()
    if "ks" not in ef or system not in ef["ks"].get("systems", {}):
        raise RuntimeError("KS settings are not frozen yet (ext_freeze.yaml part 2 missing)")
    return ef["ks"]["systems"][system]


def make(spec: dict, dt=None, N=None) -> KS:
    return KS(spec["L"], N or spec["N"], dt or spec["dt"])


def block_seed(block_base: int, system_index: int, stream: int = 0) -> int:
    """Same scheme as freeze.yaml: block base + 100 * system index + stream."""
    return int(block_base + 100 * system_index + stream)


def calibration_block(ks: KS, seed: int, n_traj: int, samples_per_traj: int, sample_every: float, burn_time: float):
    """(states (n_traj * samples, N), traj_id). States every `sample_every` time units after burn-in."""
    rng = np.random.default_rng(seed)
    v = ks.burned_starts(rng, n_traj, burn_time)
    tr, _ = ks.trajectory(v, samples_per_traj, steps(sample_every, ks.dt))
    X = tr[:, 1:].reshape(-1, ks.N)
    return X, np.repeat(np.arange(n_traj), samples_per_traj)


def train_block(ks: KS, seed: int, n_traj: int, traj_time: float, store_every: float, burn_time: float):
    """(n_traj, frames + 1, N) stored every `store_every` (an integer multiple of dt)."""
    rng = np.random.default_rng(seed)
    v = ks.burned_starts(rng, n_traj, burn_time)
    stride = steps(store_every, ks.dt)
    tr, _ = ks.trajectory(v, steps(traj_time, store_every), stride)
    return tr


def panel(ks: KS, seed: int, n: int, pre_time: float, post_time: float, store_every: float, burn_time: float,
          block: str = "validation"):
    """Panel trajectories: one independent burned-in trajectory per state, `pre_time` of history before t = 0 and at
    least `post_time` after, stored every `store_every`. Returns dict(traj (n, pre+post+1, N), pre, dt) as th/data.py.
    The confirmation panel is refused here until the extension freeze part 2 exists."""
    if block == "confirmation":
        if "ks" not in ext_freeze():
            raise RuntimeError("confirmation panel refused: KS not frozen (ext_freeze.yaml part 2 missing)")
    rng = np.random.default_rng(seed)
    v = ks.burned_starts(rng, n, burn_time)
    stride = steps(store_every, ks.dt)
    pre = steps(pre_time, store_every)
    post = int(math.ceil(post_time / store_every - 1e-9))
    tr, _ = ks.trajectory(v, pre + post, stride)
    return dict(traj=tr, pre=pre, dt=float(store_every))


def patch_len(N: int, P: int) -> int:
    assert N % P == 0, (N, P)
    return N // P


def integrate_record(ks: KS, v, n_steps: int, record: dict):
    """Integrate spectral states v (B, K) for n_steps steps and record real-space states at given step indices.

    record: name -> sorted int array of step indices in [0, n_steps] (0 = the initial state). Returns
    (dict name -> (B, len(idx), N) float64, final v). Frames are exact integrator states: no interpolation."""
    out = {k: np.empty((v.shape[0], len(ix), ks.N)) for k, ix in record.items()}
    ptr = {k: 0 for k in record}
    for s in range(0, n_steps + 1):
        if s > 0:
            v = ks.step(v)
        for k, ix in record.items():
            p = ptr[k]
            if p < len(ix) and ix[p] == s:
                out[k][:, p] = ks.to_real(v)
                ptr[k] = p + 1
    for k in record:
        assert ptr[k] == len(record[k]), k
    return out, v
