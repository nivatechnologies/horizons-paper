"""Hybrid H (pivot WO): the no-drag physics right-hand side plus a learned continuous-time correction g_theta(omega)
inside the right-hand side (the solver is differentiable in torch, so the WO's continuous-time option applies).

    d omega / dt = N_phys(omega; Re) + (1/Re) lap omega  +  g_theta(omega)

integrated by the same integrating-factor RK4 (dt 0.01) as the truth, with the correction evaluated at every RK stage and
projected by the 2/3 dealias mask. g_theta is a small FNO (ap.fno.FNO2d machinery): 1 input frame (omega scaled by
64 / sigma_A(Re 40)) + coordinate channels, width 32, 12 x 12 modes, 4 Fourier layers, non-residual output multiplied by
OUT_SCALE / scale (tendency units); the last projection is zero-initialized so training starts from pure physics.
Re is not an input to g_theta. Float32 (complex64) in training and at test.
"""
from __future__ import annotations

import sys
from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.checkpoint import checkpoint

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ap.fno import FNO2d  # noqa: E402
from ap.solver import KolmoDrag  # noqa: E402

OUT_SCALE = 1.0


class Correction(nn.Module):
    def __init__(self, scale, width=32, modes=12, layers=4):
        super().__init__()
        self.net = FNO2d(1, modes=modes, width=width, layers=layers)
        nn.init.zeros_(self.net.proj2.weight)
        nn.init.zeros_(self.net.proj2.bias)
        self.scale = float(scale)

    def forward(self, w):
        """w (B, 64, 64) physical vorticity -> tendency (B, 64, 64)."""
        x = (w * self.scale)[:, None]
        B = x.shape[0]
        h = self.net.lift(torch.cat([x, self.net.coords.expand(B, -1, -1, -1)], 1))
        for k, (s, p) in enumerate(zip(self.net.spec, self.net.pw)):
            h = s(h) + p(h)
            if k < len(self.net.spec) - 1:
                h = torch.nn.functional.gelu(h)
        out = self.net.proj2(torch.nn.functional.gelu(self.net.proj1(h)))[:, 0]
        return out * (OUT_SCALE / self.scale)

    def n_params(self):
        return self.net.n_params()


class HybridSolver(KolmoDrag):
    """No-drag family (alpha = 0, beta = 0) with the learned correction in the right-hand side."""

    def __init__(self, Re, g: Correction, device="cpu", dtype=torch.float32, ckpt=False):
        super().__init__(Re, alpha=0.0, device=device, dtype=dtype)
        self.g = g
        self.ckpt = ckpt

    def rhs(self, wh):
        r = super().rhs(wh)
        corr = self.g(self.to_phys(wh).to(torch.float32))
        return r + torch.fft.rfft2(corr.to(self.dtype)) * self.mask

    def flow(self, wh, nsteps):
        for _ in range(int(nsteps)):
            wh = checkpoint(self.step, wh, use_reentrant=False) if self.ckpt else self.step(wh)
        return wh
