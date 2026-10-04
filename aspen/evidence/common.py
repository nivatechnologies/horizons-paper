"""Frozen AEA numerics, streams, state queries and outcome definitions."""
from pathlib import Path
import hashlib
import json
import math
import subprocess
import sys
import time

import numpy as np
import torch

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
sys.path.insert(0, str(REPO / "adapt_physics"))
from ap.solver import KolmoDrag

CENTRE = np.array([40., 1., .07733])
RANGE = np.array([6., .1, .2 * .07733])
QUERY_NAMES = ["forcing_power", "viscous_energy", "drag_energy", "viscous_enstrophy"]
SEEDS = {name: 7100000 + 100000 * i for i, name in enumerate([
    "training", "validation", "sensitivity", "attractor", "test", "identification",
    "chaos", "noise", "bootstrap", "optimizer", "qa"])}
RESULTS = ROOT / "results"
RUNS = ROOT / "runs"


def rng(name, index=0):
    if not 0 <= index < 100000:
        raise ValueError("substream outside reserved block")
    return np.random.default_rng(SEEDS[name] + index)


def sha():
    snapshot = REPO / "SOURCE_COMMIT"
    if snapshot.exists():
        value = snapshot.read_text().strip()
        if len(value) != 40 or any(c not in "0123456789abcdef" for c in value):
            raise ValueError("invalid source snapshot SHA")
        return value
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip()


def write_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    obj = dict(obj, git_sha=sha())
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, allow_nan=False) + "\n")
    tmp.replace(path)


class World(KolmoDrag):
    """Same World D IFRK4, with all three parameters batched and optional CUDA graphs."""
    def __init__(self, theta, device="cuda", graphs=True):
        theta = np.atleast_2d(np.asarray(theta, dtype=np.float64))
        super().__init__(theta[:, 0], alpha=0., device=device, amp=theta[:, 1])
        self.theta = theta.copy()
        self._alpha = torch.as_tensor(theta[:, 2], device=self.device, dtype=self.dtype)
        self._re = torch.as_tensor(theta[:, 0], device=self.device, dtype=self.dtype)
        self.graphs = graphs and self.device.type == "cuda"
        self._graphs = {}
        self.set_dt(.01)

    def set_dt(self, dt):
        if not hasattr(self, "theta"):
            return super().set_dt(dt)
        self.dt = float(dt)
        L = -self.K2[None] / self._re[:, None, None] - self._alpha[:, None, None]
        self.E = torch.exp(L * self.dt / 2).to(self.cdtype)
        self.E2 = self.E * self.E
        self._graphs = {}

    @torch.no_grad()
    def flow(self, wh, nsteps):
        if not self.graphs or nsteps < 5:
            return super().flow(wh, nsteps)
        key = tuple(wh.shape)
        if key not in self._graphs:
            # All captured coefficients are immutable for this World instance.
            work = wh.clone()
            stream = torch.cuda.Stream()
            stream.wait_stream(torch.cuda.current_stream())
            with torch.cuda.stream(stream):
                for _ in range(3):
                    super().flow(work, 5)
            torch.cuda.current_stream().wait_stream(stream)
            graph = torch.cuda.CUDAGraph()
            with torch.cuda.graph(graph):
                out = super().flow(work, 5)
            self._graphs[key] = work, out, graph
        work, out, graph = self._graphs[key]
        work.copy_(wh)
        for _ in range(nsteps // 5):
            graph.replay()
            work.copy_(out)
        return super().flow(work.clone(), nsteps % 5)

    def advance(self, wh, duration):
        n = int(math.floor((duration + 1e-11) / .01))
        wh = self.flow(wh, n)
        remainder = duration - n * .01
        if remainder > 1e-10:
            old = self.dt
            self.set_dt(remainder)
            wh = super().flow(wh, 1)
            self.set_dt(old)
        return wh


def queries(model, wh, theta=None):
    """Final clarified queries; theta sets the common physical query being evaluated."""
    theta = model.theta if theta is None else np.atleast_2d(theta)
    t = torch.as_tensor(theta, device=wh.device, dtype=torch.float64)
    velocity = model.velocity_hat(wh)
    energy2 = sum(model._mean_sq(v) for v in velocity)
    omega2 = model._mean_sq(wh)
    power = t[:, 1] * model.energy_input(wh)
    return torch.stack([power, omega2 / t[:, 0], t[:, 2] * energy2,
                        model.grad_sq(wh) / t[:, 0]], -1)


def ratio(e0, e90):
    if e0 is None or e90 is None or e0 == 0 or e90 == 0 or not np.isfinite([e0,e90]).all():
        return None
    value=e0/e90
    return value if np.isfinite(value) and value>0 else None


def spearman(x, y):
    from scipy.stats import spearmanr
    x, y = np.asarray(x), np.asarray(y)
    if len(x) < 2 or not np.isfinite(x).all() or not np.isfinite(y).all() or np.ptp(x) == 0 or np.ptp(y) == 0:
        return None
    value = float(spearmanr(x, y).statistic)
    return value if np.isfinite(value) else None


def classify(ratios, correlations, law_ratios, n_evaluable):
    if n_evaluable < 3:
        return "otherwise"
    arms = ["L_range-3", "FNO-theta"]
    near = {a: sum(r is not None and max(r, 1/r) <= 1.3 for r in ratios[a]) >= 3 for a in arms}
    gaps = {a: all(v is not None for v in correlations[a]) and
            abs(correlations[a][0] - correlations[a][1]) < .15 for a in arms}
    if all(near.values()) or all(gaps.values()):
        return "KILL"
    law_ok = sum(r is not None and r <= 1.3 for r in law_ratios) >= 3
    for a in arms:
        g, p = correlations[a]
        if law_ok and sum(r is not None and r >= 2 for r in ratios[a]) >= 3 and g is not None and p is not None and g >= .6 and p <= .3:
            return "PASS"
    return "otherwise"


def geometry(g):
    norm = np.linalg.norm(g)
    if not np.isfinite(norm) or norm < 1e-8:
        return None
    gh = g / norm
    j = int(np.argmin(np.abs(gh)))
    e = np.eye(3)[j]
    perp = e - gh[j] * gh
    perp /= np.linalg.norm(perp)
    if perp[j] < 0:
        perp = -perp
    out = {}
    for label, direction in [("0", gh), ("90", perp)]:
        lo, hi = 0., 2.
        def distance(s):
            u = s * direction
            return np.linalg.norm(u - np.clip(u, -1, 1))
        while distance(hi) < 1:
            hi *= 2
        for _ in range(80):
            mid = (lo + hi) / 2
            if distance(mid) < 1:
                lo = mid
            else:
                hi = mid
        u = (lo + hi) / 2 * direction
        d = u - np.clip(u, -1, 1)
        out[label] = dict(u=u.tolist(), theta=(CENTRE + RANGE*u).tolist(),
                          D_g=float(abs(gh@d)), D_perp=float(np.linalg.norm(d - gh*(gh@d))),
                          distance=float(np.linalg.norm(d)), ray=direction.tolist())
    return out
