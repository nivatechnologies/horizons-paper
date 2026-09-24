"""Systems, integrators and Lyapunov estimation for the preliminary check."""
import numpy as np

DT = 0.01


def lorenz_f(rho, sigma=10.0, beta=8.0 / 3.0):
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

    return f, jac, 3


def l96_f(d, F=8.0):
    def f(x):
        return (np.roll(x, -1, -1) - np.roll(x, 2, -1)) * np.roll(x, 1, -1) - x + F

    def jac(x):
        n = x.shape[:-1]
        J = np.zeros(n + (d, d))
        for i in range(d):
            J[..., i, (i + 1) % d] += x[..., (i - 1) % d]
            J[..., i, (i - 2) % d] += -x[..., (i - 1) % d]
            J[..., i, (i - 1) % d] += x[..., (i + 1) % d] - x[..., (i - 2) % d]
            J[..., i, i] += -1.0
        return J

    return f, jac, d


def rk4(f, x, dt=DT):
    k1 = f(x)
    k2 = f(x + 0.5 * dt * k1)
    k3 = f(x + 0.5 * dt * k2)
    k4 = f(x + dt * k3)
    return x + dt / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)


def rk4_tangent(f, jac, x, Q, dt=DT):
    """RK4 for state plus tangent vectors (columns of Q)."""
    def g(x, Q):
        return f(x), jac(x) @ Q
    k1x, k1Q = g(x, Q)
    k2x, k2Q = g(x + 0.5 * dt * k1x, Q + 0.5 * dt * k1Q)
    k3x, k3Q = g(x + 0.5 * dt * k2x, Q + 0.5 * dt * k2Q)
    k4x, k4Q = g(x + dt * k3x, Q + dt * k3Q)
    return (x + dt / 6 * (k1x + 2 * k2x + 2 * k3x + k4x),
            Q + dt / 6 * (k1Q + 2 * k2Q + 2 * k3Q + k4Q))


def sample_attractor(f, d, n_traj, n_keep, stride, burn=5000, seed=0, x0_scale=1.0, offset=0.0):
    rng = np.random.default_rng(seed)
    x = offset + x0_scale * rng.standard_normal((n_traj, d))
    for _ in range(burn):
        x = rk4(f, x)
    out = np.empty((n_keep, n_traj, d))
    for k in range(n_keep):
        for _ in range(stride):
            x = rk4(f, x)
        out[k] = x
    return out.reshape(-1, d)


def lyapunov_spectrum(f, jac, x0, n_exp, t_total=500.0, renorm_every=10, burn=2000):
    """Benettin/QR on a batch of initial points; returns mean and per-trajectory spectra."""
    x = x0.copy()
    for _ in range(burn):
        x = rk4(f, x)
    B, d = x.shape
    Q = np.tile(np.eye(d)[:, :n_exp], (B, 1, 1))
    sums = np.zeros((B, n_exp))
    n_steps = int(round(t_total / DT))
    for s in range(1, n_steps + 1):
        x, Q = rk4_tangent(f, jac, x, Q)
        if s % renorm_every == 0:
            Q, R = np.linalg.qr(Q)
            diag = np.abs(np.diagonal(R, axis1=-2, axis2=-1))
            sums += np.log(diag)
    spec = sums / (n_steps * DT)
    return spec.mean(0), spec
