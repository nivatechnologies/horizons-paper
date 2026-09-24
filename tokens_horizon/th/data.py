"""Trajectory blocks. Four independent blocks per system from disjoint seed ranges.

calibration   codebooks, D_eff, calibration map h      150,000 states, every 0.1 tu
training      learned models                            trajectories stored every dt
validation    checkpoint selection (and the pre-freeze stall check panel)
confirmation  all final evaluation                      independent panel trajectories

A panel trajectory is one burned-in trajectory per test state: `pre` steps of history
before t = 0 and `post` steps after, stored every integrator step so every frame
interval is a subsample of the same physical trajectory (no interpolation).
"""
from __future__ import annotations

import hashlib
import math

import numpy as np

from . import config
from .systems import DT, flow, get_system, trajectory


def _cache(name):
    config.ensure_dirs()
    return config.CACHE / f"{name}.npz"


def _hash(a):
    return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()[:16]


def burned_starts(system, block, n, stream=0):
    fz = config.freeze()
    sysm = get_system(system)
    rng = np.random.default_rng(config.seed(block, system, stream))
    x = sysm.gaussian_starts(rng, n)
    return flow(sysm.f, x, fz["integration"]["burn_in_steps"])


def calibration(system):
    """(states (150000, d), traj_id (150000,))"""
    p = _cache(f"calib_{system}")
    if p.exists():
        z = np.load(p)
        return z["X"], z["traj"]
    c = config.freeze()["blocks"]["calibration"]
    sysm = get_system(system)
    x = burned_starts(system, "calibration", c["n_traj"])
    tr = trajectory(sysm.f, x, c["samples_per_traj"], stride=c["sample_every_steps"])[1:]  # (S, n, d)
    X = tr.transpose(1, 0, 2).reshape(-1, sysm.d)
    traj = np.repeat(np.arange(c["n_traj"]), c["samples_per_traj"])
    np.savez(p, X=X, traj=traj)
    return X, traj


def sigma_A(system):
    X, _ = calibration(system)
    return float(np.sqrt(((X - X.mean(0)) ** 2).sum(1).mean()))


def train_trajectories(system, block="training", n_traj=None):
    """(n_traj, steps+1, d) stored every dt. Training uses the first 100 of the 1,000 data-axis trajectories."""
    b = config.freeze()["blocks"][block]
    n_all = b.get("n_traj_data_axis", b["n_traj"])
    p = _cache(f"{block}_{system}")
    if p.exists():
        T = np.load(p)["T"]
    else:
        sysm = get_system(system)
        x = burned_starts(system, block, n_all)
        steps = int(round(b["traj_time"] / DT))
        T = trajectory(sysm.f, x, steps).transpose(1, 0, 2).astype(np.float64)
        np.savez(p, T=T)
    return T[: (n_traj or b["n_traj"])]


def panel(system, block="confirmation", n=None, dt=DT, post_time=None, stream=0, tag=""):
    """Panel trajectories. Returns dict(traj (n, pre+post+1, d), pre (index of t = 0), dt).

    The panel is generated once for the full 1,000 states; the 300-state history panel is its first 300,
    so every history-reference comparison uses states that are also in the bound panel.
    """
    fz = config.freeze()
    b = fz["blocks"][block]
    n_all = b["panel_states"]
    pre_time = fz["blocks"]["confirmation"]["pre_history_time"]
    if post_time is None:
        post_time = config.window_time(system) + 0.2
    name = f"panel_{block}_{system}_dt{dt:g}_s{stream}{tag}"
    p = _cache(name)
    if p.exists():
        z = np.load(p)
        out = dict(traj=z["traj"], pre=int(z["pre"]), dt=float(z["dt"]))
    else:
        sysm = get_system(system)
        x = burned_starts(system, block, n_all, stream=stream)
        pre = int(round(pre_time / dt))
        post = int(math.ceil(post_time / dt))
        tr = trajectory(sysm.f, x, pre + post, dt=dt).transpose(1, 0, 2)
        np.savez(p, traj=tr, pre=pre, dt=dt)
        out = dict(traj=tr, pre=pre, dt=dt)
    if n is not None:
        out = dict(out, traj=out["traj"][:n])
    out["sha"] = _hash(out["traj"][:, out["pre"]])
    return out


def frames(pnl, delta, n_before=None, n_after=None):
    """Subsample a panel on the frame grid. Returns (hist (L+1, n, d) ending at t = 0, fut (F+1, n, d) from t = 0)."""
    sub = delta / pnl["dt"]
    if abs(sub - round(sub)) > 1e-9:
        raise ValueError(f"frame interval {delta} is not a multiple of dt {pnl['dt']}; no interpolation allowed")
    sub = int(round(sub))
    tr, pre = pnl["traj"], pnl["pre"]
    max_before = pre // sub
    L = max_before if n_before is None else n_before
    if L > max_before:
        raise ValueError("not enough history in panel")
    hist = tr[:, pre - L * sub: pre + 1: sub].transpose(1, 0, 2)
    max_after = (tr.shape[1] - 1 - pre) // sub
    F = max_after if n_after is None else n_after
    fut = tr[:, pre: pre + F * sub + 1: sub].transpose(1, 0, 2)
    return hist, fut


def n_future_frames(system, delta):
    return int(math.ceil(config.window_time(system) / delta - 1e-9))
