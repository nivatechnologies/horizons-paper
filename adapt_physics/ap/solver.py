"""Kolmogorov flow with linear drag and a per-trajectory Reynolds number (Adapt the Physics, stage 1).

Extends tokens_horizon/th/kolmogorov.py (same equations, grid, 2/3 dealiasing, IFRK4, dt 0.01, float64):
    omega_t + u.grad omega = (1/Re) lap omega - alpha omega - n cos(n y),   n = 4, 64 x 64, [0, 2 pi)^2.
The truth has alpha > 0 (ap_freeze.yaml drag.alpha); the physics arms' model family has alpha = 0 (mismatch).
Re may differ per batch element (tensor of shape (B,)): the integrating factor exp((-|k|^2/Re_b - alpha) dt / 2)
is built per element. set_re() changes Re in place (the drift switch at t_c).

Pivot World C adds the blinded Codex term (pivot/CODEX_MISMATCH.md): topographic beta, +beta v on the left-hand side
(v = -psi_x), i.e. rhs - beta * v.

Enstrophy budget (Z = <omega^2>/2, grid means): viscous loss nu <|grad omega|^2>, drag loss alpha <omega^2>.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tokens_horizon"))
from th.kolmogorov import Kolmogorov  # noqa: E402

UNIT = 0.35          # observation interval Delta (time units)
STEPS_PER_OBS = 35   # dt = 0.01


class KolmoDrag(Kolmogorov):
    def __init__(self, Re, alpha=0.0, device="cpu", dtype=torch.float64, N=64, n=4, dt=0.01, beta=0.0, amp=None):
        self.alpha = float(alpha)
        self.beta = float(beta)          # topographic beta (pivot World C; pivot/CODEX_MISMATCH.md): RHS - beta * v
        self._re = None
        super().__init__(N=N, Re=40.0, n=n, dt=dt, device=device, dtype=dtype)
        self.F_hat0 = self.F_hat
        self.set_re(Re)
        if amp is not None:
            self.set_amp(amp)

    def set_amp(self, amp):
        """Forcing amplitude per element (stage 2 item 3): F_hat = amp_b * F_hat0; amp = 1 is the nominal forcing."""
        a = torch.as_tensor(np.atleast_1d(np.asarray(amp, dtype=np.float64)), device=self.device, dtype=self.dtype)
        self.F_hat = self.F_hat0[None] * a[:, None, None]

    def set_re(self, Re):
        re = torch.as_tensor(np.atleast_1d(np.asarray(Re, dtype=np.float64)), device=self.device, dtype=self.dtype)
        self._re = re
        L = -self.K2[None] / re[:, None, None] - self.alpha
        self.E = torch.exp(L * self.dt / 2).to(self.cdtype)
        self.E2 = self.E * self.E

    def set_dt(self, dt):
        self.dt = float(dt)
        if self._re is not None:
            self.set_re(self._re.cpu().numpy())

    def rhs(self, wh):
        r = super().rhs(wh)
        if self.beta:
            _, vh = self.velocity_hat(wh)
            r = r - self.beta * vh * self.mask
        return r

    # enstrophy budget terms per element
    def grad_sq(self, wh):
        return self._mean_sq(1j * self.KX * wh) + self._mean_sq(1j * self.KY * wh)

    def budget(self, wh):
        """(viscous enstrophy loss, drag enstrophy loss) per element."""
        return self.grad_sq(wh) / self._re, self.alpha * self._mean_sq(wh)


def obs_noise(rng: np.random.Generator, shape, sigma_A: float, rel: float = 0.02):
    """Additive white noise with Euclidean norm (over the 4,096 grid values) rel * sigma_A in RMS."""
    return rng.standard_normal(shape) * (rel * sigma_A / 64.0)


def lyapunov(model: KolmoDrag, wh, t_total, tau=1.0, delta0=1e-6, t_transient=20.0, rng=None):
    """Largest Lyapunov exponent per start by renormalized twins (as th.kolmogorov.lyapunov_twin)."""
    rng = rng or np.random.default_rng(0)
    B = wh.shape[0]
    n_tau = int(round(tau / model.dt))
    n_ren = int(round(t_total / tau))
    n_tr = int(round(t_transient / tau))
    re = model._re.cpu().numpy()
    model.set_re(np.concatenate([re, re]) if len(re) == B else np.full(2 * B, re[0]))

    def norm(x):
        return model._mean_sq(x).sqrt()

    pert = model.to_spec(torch.as_tensor(rng.standard_normal((B, model.N, model.N)), dtype=model.dtype))
    pert = pert * (delta0 * norm(wh) / norm(pert))[:, None, None]
    both = torch.cat([wh, wh + pert])
    logs = np.zeros((B, n_ren))
    for r in range(n_ren):
        both = model.flow(both, n_tau)
        base, twin = both[:B], both[B:]
        d = twin - base
        nd = norm(d)
        target = delta0 * norm(base)
        logs[:, r] = torch.log(nd / target).cpu().numpy()
        both = torch.cat([base, base + d * (target / nd)[:, None, None]])
    model.set_re(re)
    use = logs[:, n_tr:]
    return use.sum(1) / (use.shape[1] * tau)
