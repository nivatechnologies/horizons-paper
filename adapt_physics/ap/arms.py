"""Forecast arms (ap_freeze.yaml arms). Every arm receives the same noisy observations; forecasts start from the last
observed frame k = w and are compared with the true frames k = w + j, j = 1..F.

Solver arms (O, P0, P1, P1x): the noisy frame is projected by the integrator (2/3 dealias mask, mean removal).
  O   truth family (drag alpha) at the true test Re            P0  no-drag family at Re 40
  P1  no-drag family at Re fitted by golden-section search      P1x drag family (alpha known) at Re fitted likewise
Identification (P1, P1x): deterministic golden-section search on Re in [25, 70], exactly 30 objective evaluations; the
objective is the mean over window frames k = 2..w of ||x_model(k) - y_k||^2 / sigma_A^2, with the model started from
the projected first window frame y_1; the estimate is the midpoint of the final bracket.
Learned arms: autoregressive rollouts of an FNO from the last n_in observed frames (earlier frames are pre-change
observations when w < n_in).
"""
from __future__ import annotations

import copy
import math
import time

import numpy as np
import torch

from .solver import KolmoDrag, STEPS_PER_OBS

GOLD = (math.sqrt(5) - 1) / 2


def solver_errors(y0, truth_frames, re, alpha, sA, device, eps_stop=0.3, chunk=600, beta=0.0, make=None):
    """y0 (n, 64, 64) start grids; truth_frames(j) -> (n, 64, 64) truth at j = 1..F (callable, F = its .F);
    re (n,) per-state Re. Returns err (F+1, n) (row 0 = start error), with +inf after the integration stops (every
    state has crossed eps_stop at some j >= 1). Also the number of integrator steps."""
    F = truth_frames.F
    n = len(y0)
    err = np.full((F + 1, n), np.inf)
    err[0] = np.sqrt(((y0 - truth_frames(0)) ** 2).sum((-2, -1))) / sA
    m = make(re) if make else KolmoDrag(re, alpha=alpha, beta=beta, device=device)
    wh = m.to_spec(torch.as_tensor(y0))
    done = np.zeros(n, bool)
    steps = 0
    for j in range(1, F + 1):
        with torch.no_grad():
            wh = m.flow(wh, STEPS_PER_OBS)
        steps += STEPS_PER_OBS
        e = np.sqrt(((m.to_phys(wh).double().cpu().numpy() - truth_frames(j)) ** 2).sum((-2, -1))) / sA
        err[j] = e
        done |= e > eps_stop
        if done.all():
            break
    return err, steps


def identify(Y, w, alpha, sA, device, lo=25.0, hi=70.0, n_eval=30, beta=0.0, make=None):
    """Golden-section search for Re per state. Y (w, n, 64, 64): window frames k = 1..w (noisy).
    Returns (Re_hat (n,), objective evaluations per state, integrator steps per state)."""
    n = Y.shape[1]
    Yt = torch.as_tensor(np.asarray(Y), device=device)

    def obj(re):
        m = make(re) if make else KolmoDrag(re, alpha=alpha, beta=beta, device=device)
        wh = m.to_spec(Yt[0])
        tot = torch.zeros(n, dtype=torch.float64, device=device)
        for k in range(1, w):
            with torch.no_grad():
                wh = m.flow(wh, STEPS_PER_OBS)
            tot += ((m.to_phys(wh).double() - Yt[k]) ** 2).sum((-2, -1))
        return (tot / max(w - 1, 1) / sA ** 2).cpu().numpy()

    a = np.full(n, lo)
    b = np.full(n, hi)
    c = b - GOLD * (b - a)
    d = a + GOLD * (b - a)
    fc, fd = obj(c), obj(d)
    evals = 2
    while evals < n_eval:
        left = fc < fd                       # minimum in [a, d]
        b = np.where(left, d, b)
        a = np.where(left, a, c)
        c_new = np.where(left, b - GOLD * (b - a), d)
        d_new = np.where(left, c, a + GOLD * (b - a))
        f_new = obj(np.where(left, c_new, d_new))
        fc, fd = np.where(left, f_new, fd), np.where(left, fc, f_new)
        c, d = c_new, d_new
        evals += 1
    return 0.5 * (a + b), evals, evals * (w - 1) * STEPS_PER_OBS


@torch.no_grad()
def rollout(model, ctx, F, sc, re=None, bs=150):
    """ctx (n, n_in, 64, 64) raw observed frames; returns forecasts (F, n, 64, 64) raw units (float64 numpy)."""
    dev = next(model.parameters()).device
    n = ctx.shape[0]
    out = np.empty((F, n, 64, 64))
    for i in range(0, n, bs):
        h = torch.as_tensor(ctx[i:i + bs] * sc, dtype=torch.float32, device=dev)
        r = None if re is None else torch.as_tensor(re[i:i + bs], device=dev)
        for j in range(F):
            p = model(h, r)
            out[j, i:i + bs] = p.double().cpu().numpy() / sc
            h = torch.cat([h[:, 1:], p[:, None]], 1)
    return out


def finetune(base, pairs_x, pairs_y, sc, steps=200, lr=1e-4):
    """Copy of `base` fine-tuned on one state's window pairs (inputs (P, n_in, 64, 64), targets (P, 64, 64); raw units,
    noisy observations): AdamW (lr 1e-4, weight decay 0), full batch, one-step MSE, `steps` steps."""
    m = copy.deepcopy(base)
    m.train()
    dev = next(m.parameters()).device
    x = torch.as_tensor(pairs_x * sc, dtype=torch.float32, device=dev)
    y = torch.as_tensor(pairs_y * sc, dtype=torch.float32, device=dev)
    opt = torch.optim.AdamW(m.parameters(), lr=lr, weight_decay=0.0)
    for _ in range(steps):
        loss = ((m(x) - y) ** 2).mean()
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
    m.eval()
    return m
