"""Systems, RK4 integration and Lyapunov analysis (float64 throughout)."""
from __future__ import annotations

import numpy as np

DT = 0.01


class System:
    """A flow x' = f(x) with its Jacobian, for batched states of shape (..., d)."""

    def __init__(self, name, f, jac, d, divergence, offset, burn_scale=1.0):
        self.name, self.f, self.jac, self.d = name, f, jac, d
        self.divergence = divergence          # analytic trace of the Jacobian (constant here)
        self.offset = np.asarray(offset, float)
        self.burn_scale = burn_scale

    def gaussian_starts(self, rng, n):
        return self.offset + self.burn_scale * rng.standard_normal((n, self.d))


def lorenz63(rho, sigma=10.0, beta=8.0 / 3.0):
    def f(x):
        X, Y, Z = x[..., 0], x[..., 1], x[..., 2]
        return np.stack([sigma * (Y - X), X * (rho - Z) - Y, X * Y - beta * Z], axis=-1)

    def jac(x):
        X, Y, Z = x[..., 0], x[..., 1], x[..., 2]
        J = np.zeros(x.shape[:-1] + (3, 3))
        J[..., 0, 0] = -sigma
        J[..., 0, 1] = sigma
        J[..., 1, 0] = rho - Z
        J[..., 1, 1] = -1.0
        J[..., 1, 2] = -X
        J[..., 2, 0] = Y
        J[..., 2, 1] = X
        J[..., 2, 2] = -beta
        return J

    return System(f"lorenz{int(rho)}", f, jac, 3, -(sigma + 1.0 + beta), [1.0, 1.0, 20.0])


def lorenz96(d, F=8.0):
    ip1 = (np.arange(d) + 1) % d
    im1 = (np.arange(d) - 1) % d
    im2 = (np.arange(d) - 2) % d

    def f(x):
        return (x[..., ip1] - x[..., im2]) * x[..., im1] - x + F

    def jac(x):
        J = np.zeros(x.shape[:-1] + (d, d))
        for i in range(d):
            J[..., i, ip1[i]] += x[..., im1[i]]
            J[..., i, im2[i]] += -x[..., im1[i]]
            J[..., i, im1[i]] += x[..., ip1[i]] - x[..., im2[i]]
            J[..., i, i] += -1.0
        return J

    return System(f"l96_{d}", f, jac, d, -float(d), np.full(d, F))


SYSTEMS = {
    "lorenz28": lambda: lorenz63(28.0),
    "lorenz45": lambda: lorenz63(45.0),
    "l96_5": lambda: lorenz96(5),
    "l96_6": lambda: lorenz96(6),
    "l96_10": lambda: lorenz96(10),
    "l96_20": lambda: lorenz96(20),
}


def get_system(name) -> System:
    return SYSTEMS[name]()


def rk4(f, x, dt=DT):
    k1 = f(x)
    k2 = f(x + 0.5 * dt * k1)
    k3 = f(x + 0.5 * dt * k2)
    k4 = f(x + dt * k3)
    return x + dt / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)


def flow(f, x, n, dt=DT):
    for _ in range(n):
        x = rk4(f, x, dt)
    return x


def trajectory(f, x, n, stride=1, dt=DT):
    """States after every `stride` steps, n samples, starting with x itself: shape (n+1, ..., d)."""
    out = np.empty((n + 1,) + x.shape)
    out[0] = x
    for k in range(1, n + 1):
        x = flow(f, x, stride, dt)
        out[k] = x
    return out


def rk4_tangent(f, jac, x, Q, dt=DT):
    def g(x, Q):
        return f(x), jac(x) @ Q
    k1x, k1Q = g(x, Q)
    k2x, k2Q = g(x + 0.5 * dt * k1x, Q + 0.5 * dt * k1Q)
    k3x, k3Q = g(x + 0.5 * dt * k2x, Q + 0.5 * dt * k2Q)
    k4x, k4Q = g(x + dt * k3x, Q + dt * k3Q)
    return (x + dt / 6 * (k1x + 2 * k2x + 2 * k3x + k4x),
            Q + dt / 6 * (k1Q + 2 * k2Q + 2 * k3Q + k4Q))


def benettin(system: System, x0, t_total, renorm_every=10, burn=2000, dt=DT):
    """Full Lyapunov spectrum by Benettin/QR on a batch of starts. Returns per-start spectra (B, d)."""
    f, jac, d = system.f, system.jac, system.d
    x = flow(f, x0.copy(), burn, dt)
    B = x.shape[0]
    Q = np.tile(np.eye(d), (B, 1, 1))
    sums = np.zeros((B, d))
    n_steps = int(round(t_total / dt))
    for s in range(1, n_steps + 1):
        x, Q = rk4_tangent(f, jac, x, Q, dt)
        if s % renorm_every == 0 or s == n_steps:
            Q, R = np.linalg.qr(Q)
            sums += np.log(np.abs(np.diagonal(R, axis1=-2, axis2=-1)))
    return sums / (n_steps * dt)


def kaplan_yorke(spec):
    spec = np.sort(np.asarray(spec))[::-1]
    cs = np.cumsum(spec)
    if cs[0] < 0:
        return 0.0
    j = int(np.max(np.where(cs >= 0)[0])) + 1
    if j >= len(spec):
        return float(len(spec))
    return float(j + cs[j - 1] / abs(spec[j]))
