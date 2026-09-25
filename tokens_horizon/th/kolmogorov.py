"""2D Kolmogorov flow (post-freeze extension, Phase A pilot module).

Equations (Chandler & Kerswell 2013, J. Fluid Mech. 722, 554-595, section 2):
    u_t + u.grad u + grad p = (1/Re) lap u + sin(n y) e_x,   div u = 0,   (x, y) in [0, 2 pi)^2,
taking the curl (omega = v_x - u_y):
    omega_t + u.grad omega = (1/Re) lap omega - n cos(n y),
with n = 4, Re = 40 (their regime). Streamfunction: lap psi = -omega, u = psi_y, v = -psi_x.
The laminar solution is u = (Re/n^2) sin(n y), omega = -(Re/n) cos(n y).

THE STATE is the vorticity field omega on the N x N collocation grid (array axis -2 = y, -1 = x), zero mean.
This is the object that is tokenized and scored (e_j = ||omega_hat_j - omega_j|| / sigma_A, Euclidean norm
over the N^2 grid values). Velocity is derived from it and is not part of the state.

Numerics: Fourier pseudo-spectral, 2/3-rule dealiasing (modes with |kx| or |ky| > N/3 are zeroed; the
state is kept in the dealiased subspace), integrating-factor RK4 (IFRK4) with the exact factor
exp(-|k|^2 dt / Re) on the diagonal viscous term. IFRK4 is used rather than ETDRK4 because the linear
operator is diagonal and only mildly stiff at this Re and resolution (max |k|^2 dt / Re ~ 0.1 at
N = 64, dt = 0.01), so the integrating factor is exact for viscosity with none of ETDRK4's contour-
integral coefficient evaluation; accuracy is checked by dt halving.

Batched: states (B, N, N). Torch backend (CPU or CUDA, float64 by default).
"""
from __future__ import annotations

import math

import numpy as np
import torch

from . import config

# ---- defaults (pilot proposal; frozen values go in ext_freeze.yaml part 2) ----
RE = 40.0
N_FORCE = 4
N_GRID = 64
DT = 0.01
SYSTEM = "kolmo40"
SYSTEM_INDEX = 8          # proposed; 6, 7 left for the KS systems
BURN_TIME = 500.0         # proposed burn-in from random initial conditions (time units)


def seed(block: str, stream: int = 0) -> int:
    """Seed = block base + 100 * system index + stream, as freeze.yaml seeds."""
    base = config.freeze()["seeds"]["block_base"][block]
    return int(base + 100 * SYSTEM_INDEX + stream)


class Kolmogorov:
    """Pseudo-spectral IFRK4 stepper for vorticity; spectral state w_hat of shape (B, N, N//2+1)."""

    def __init__(self, N=N_GRID, Re=RE, n=N_FORCE, dt=DT, device="cpu", dtype=torch.float64):
        self.N, self.Re, self.n, self.dt = N, float(Re), int(n), float(dt)
        self.device, self.dtype = torch.device(device), dtype
        self.cdtype = torch.complex128 if dtype == torch.float64 else torch.complex64
        kx = torch.fft.rfftfreq(N, d=1.0 / N).to(self.device, dtype)          # 0 .. N/2
        ky = torch.fft.fftfreq(N, d=1.0 / N).to(self.device, dtype)           # 0 .. -1
        self.KY, self.KX = torch.meshgrid(ky, kx, indexing="ij")               # (N, N//2+1)
        self.K2 = self.KX ** 2 + self.KY ** 2
        self.K2inv = torch.where(self.K2 > 0, 1.0 / torch.where(self.K2 > 0, self.K2, 1.0), 0.0)
        kmax = N // 3
        self.mask = ((self.KX.abs() <= kmax) & (self.KY.abs() <= kmax) & (self.K2 > 0)).to(dtype)
        self.set_dt(dt)
        y = torch.arange(N, device=self.device, dtype=dtype) * (2 * math.pi / N)
        forcing = (-self.n * torch.cos(self.n * y))[:, None].expand(N, N)      # -n cos(n y)
        self.F_hat = torch.fft.rfft2(forcing) * self.mask
        self.siny = torch.sin(self.n * y)[:, None]

    def set_dt(self, dt):
        self.dt = float(dt)
        L = -self.K2 / self.Re
        self.E = torch.exp(L * self.dt / 2).to(self.cdtype)
        self.E2 = self.E * self.E

    # -- transforms --
    def to_spec(self, w):
        w = torch.as_tensor(w, device=self.device, dtype=self.dtype)
        return torch.fft.rfft2(w) * self.mask

    def to_phys(self, wh):
        return torch.fft.irfft2(wh, s=(self.N, self.N))

    def velocity_hat(self, wh):
        psi = wh * self.K2inv
        return 1j * self.KY * psi, -1j * self.KX * psi

    # -- dynamics --
    def rhs(self, wh):
        uh, vh = self.velocity_hat(wh)
        s = (self.N, self.N)
        u = torch.fft.irfft2(uh, s=s)
        v = torch.fft.irfft2(vh, s=s)
        wx = torch.fft.irfft2(1j * self.KX * wh, s=s)
        wy = torch.fft.irfft2(1j * self.KY * wh, s=s)
        return -torch.fft.rfft2(u * wx + v * wy) * self.mask + self.F_hat

    def step(self, wh):
        dt, E, E2 = self.dt, self.E, self.E2
        k1 = dt * self.rhs(wh)
        k2 = dt * self.rhs(E * (wh + 0.5 * k1))
        k3 = dt * self.rhs(E * wh + 0.5 * k2)
        k4 = dt * self.rhs(E2 * wh + E * k3)
        return E2 * wh + (E2 * k1 + 2.0 * E * (k2 + k3) + k4) / 6.0

    def flow(self, wh, nsteps):
        for _ in range(int(nsteps)):
            wh = self.step(wh)
        return wh

    # -- diagnostics (grid means) --
    def _mean_sq(self, fh):
        """<f^2> over the grid from rfft2 coefficients (Parseval)."""
        w = torch.full_like(self.K2, 2.0)
        w[:, 0] = 1.0
        if self.N % 2 == 0:
            w[:, -1] = 1.0
        return (w * fh.abs() ** 2).sum((-2, -1)) / self.N ** 4

    def energy(self, wh):
        uh, vh = self.velocity_hat(wh)
        return 0.5 * (self._mean_sq(uh) + self._mean_sq(vh))

    def enstrophy(self, wh):
        return 0.5 * self._mean_sq(wh)

    def dissipation(self, wh):
        return 2.0 * self.enstrophy(wh) / self.Re

    def energy_input(self, wh):
        uh, _ = self.velocity_hat(wh)
        u = torch.fft.irfft2(uh, s=(self.N, self.N))
        return (u * self.siny).mean((-2, -1))

    def diagnostics(self, wh):
        return dict(E=self.energy(wh), Z=self.enstrophy(wh), I=self.energy_input(wh), D=self.dissipation(wh))

    # -- initial conditions --
    def random_ic(self, rng: np.random.Generator, B: int, kmax_ic: int = 8, rms: float = 5.0):
        """Random vorticity on modes 0 < |k| <= kmax_ic (independent of N, so the same seed gives the same
        field on every grid), Gaussian coefficients, rescaled to grid-RMS `rms`. Returns spectral state."""
        M = 2 * kmax_ic + 1
        coef = rng.standard_normal((B, M, M)) + 1j * rng.standard_normal((B, M, M))
        wh = torch.zeros((B, self.N, self.N // 2 + 1), dtype=self.cdtype, device=self.device)
        ks = np.arange(-kmax_ic, kmax_ic + 1)
        for a, ky in enumerate(ks):
            for b, kx in enumerate(ks):
                if kx < 0 or (kx == 0 and ky <= 0) or kx * kx + ky * ky > kmax_ic ** 2:
                    continue
                wh[:, ky % self.N, kx] = torch.as_tensor(coef[:, a, b], dtype=self.cdtype, device=self.device)
        wh[:, :, 0] = _hermitian_col0(wh[:, :, 0], self.N)
        w = self.to_phys(wh * self.mask)
        w = w / w.pow(2).mean((-2, -1), keepdim=True).sqrt() * rms
        return self.to_spec(w)


def _hermitian_col0(col, N):
    """Make the kx = 0 column Hermitian (c[-ky] = conj c[ky]) using the ky > 0 half."""
    out = col.clone()
    for ky in range(1, N // 2):
        out[:, (-ky) % N] = torch.conj(col[:, ky])
    out[:, 0] = 0
    return out


# ---------------------------------------------------------------------------------------------
# Trajectory blocks and panels in the conventions of th/data.py (seeds by block; no interpolation).

def burned_starts(model: Kolmogorov, block: str, n: int, stream: int = 0, burn_time: float = BURN_TIME):
    """n burned-in spectral states from random initial conditions of the given seed block/stream."""
    rng = np.random.default_rng(seed(block, stream))
    wh = model.random_ic(rng, n)
    return model.flow(wh, int(round(burn_time / model.dt)))


def trajectory(model: Kolmogorov, wh, n_samples: int, stride: int, out_dtype=np.float32):
    """Physical vorticity after every `stride` steps, n_samples samples, starting with the input state:
    numpy (B, n_samples + 1, N, N). Storage dtype float32 by default (integration dtype unchanged)."""
    B = wh.shape[0]
    out = np.empty((B, n_samples + 1, model.N, model.N), dtype=out_dtype)
    out[:, 0] = model.to_phys(wh).cpu().numpy()
    for k in range(1, n_samples + 1):
        wh = model.flow(wh, stride)
        out[:, k] = model.to_phys(wh).cpu().numpy()
    return out, wh


def panel(model: Kolmogorov, block: str, n: int, pre_time: float, post_time: float, store_every: int,
          stream: int = 0, burn_time: float = BURN_TIME, allow_confirmation: bool = False, chunk: int = 50):
    """Panel trajectories: one burned-in trajectory per test state, `pre_time` of history before t = 0 and
    `post_time` after, stored every `store_every` integrator steps (the frame unit; every frame interval must be
    a multiple of it). Returns dict(traj (n, S, N, N), pre, dt) compatible with th.data.frames, where
    dt = store_every * model.dt is the storage spacing. The confirmation panel needs allow_confirmation=True."""
    if block == "confirmation" and not allow_confirmation:
        raise RuntimeError("confirmation panel not generated in Phase A (pass allow_confirmation=True after part 2)")
    unit = store_every * model.dt
    pre = int(round(pre_time / unit))
    post = int(math.ceil(post_time / unit - 1e-9))
    rng = np.random.default_rng(seed(block, stream))
    wh0 = model.random_ic(rng, n)
    outs = []
    for i in range(0, n, chunk):
        wh = model.flow(wh0[i:i + chunk], int(round(burn_time / model.dt)))
        tr, _ = trajectory(model, wh, pre + post, store_every)
        outs.append(tr)
    return dict(traj=np.concatenate(outs), pre=pre, dt=unit)


# ---------------------------------------------------------------------------------------------
# Largest Lyapunov exponent: renormalized twin trajectories (Benettin with a finite perturbation).

def lyapunov_twin(model: Kolmogorov, wh, t_total: float, tau: float = 1.0, delta0: float = 1e-6,
                  t_transient: float = 20.0, rng: np.random.Generator | None = None, record_every=None):
    """lambda_1 per start. Twin = base + delta0 * ||base|| * random unit direction (grid-L2 norm of vorticity,
    in the dealiased subspace); every tau the separation is measured and rescaled back to delta0 * ||base||
    along its current direction. The first t_transient of log-growths (direction alignment) is discarded.
    Returns dict(lam (B,), local (B, n_renorm) log growth per tau, diagnostics time series)."""
    rng = rng or np.random.default_rng(0)
    B = wh.shape[0]
    n_tau = int(round(tau / model.dt))
    assert abs(n_tau * model.dt - tau) < 1e-9
    n_ren = int(round(t_total / tau))
    n_tr = int(round(t_transient / tau))

    def norm(x):
        return model._mean_sq(x).sqrt()

    pert = model.to_spec(torch.as_tensor(rng.standard_normal((B, model.N, model.N)), dtype=model.dtype))
    scale = (delta0 * norm(wh))
    pert = pert * (scale / norm(pert))[:, None, None]
    both = torch.cat([wh, wh + pert])
    logs = np.zeros((B, n_ren))
    diag = {k: [] for k in ("E", "Z", "I", "D")}
    for r in range(n_ren):
        both = model.flow(both, n_tau)
        base, twin = both[:B], both[B:]
        d = twin - base
        nd = norm(d)
        target = delta0 * norm(base)
        logs[:, r] = torch.log(nd / target).cpu().numpy()
        both = torch.cat([base, base + d * (target / nd)[:, None, None]])
        dg = model.diagnostics(base)
        for k in diag:
            diag[k].append(dg[k].cpu().numpy())
    use = logs[:, n_tr:]
    lam = use.sum(1) / (use.shape[1] * tau)
    return dict(lam=lam, local=logs, diag={k: np.stack(v, 1) for k, v in diag.items()}, t_used=use.shape[1] * tau)


def sigma_A(X):
    """RMS distance of states X (M, N, N) to their mean (grid Euclidean norm)."""
    X = np.asarray(X, np.float64).reshape(len(X), -1)
    return float(np.sqrt(((X - X.mean(0)) ** 2).sum(1).mean()))
