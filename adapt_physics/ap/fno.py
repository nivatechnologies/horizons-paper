"""Fourier neural operator (Li et al. 2021, arXiv:2010.08895), 2D, for autoregressive vorticity forecasting at the
observation interval Delta = 0.35.

Input channels: n_in past frames (scaled by 64 / sigma_A(Re 40), oldest first) + 4 periodic coordinate channels
(sin x, cos x, sin y, cos y) + [optional] the Reynolds number channel (Re - 40) / 6 (L_param only).
Lift (1x1 conv) to `width`; `layers` Fourier layers: spectral convolution keeping `modes` x `modes` Fourier modes in
both ky half-planes (rfft2 layout) plus a 1x1 conv, GELU between layers (none after the last); projection
1x1 conv (width -> 128), GELU, 1x1 conv (128 -> 1). Output = last input frame + network output (residual).
"""
from __future__ import annotations

import math

import torch
import torch.nn as nn
import torch.nn.functional as F


class SpectralConv2d(nn.Module):
    def __init__(self, c_in, c_out, modes):
        super().__init__()
        self.modes = modes
        scale = 1.0 / (c_in * c_out)
        self.w1 = nn.Parameter(scale * torch.randn(c_in, c_out, modes, modes, dtype=torch.cfloat))
        self.w2 = nn.Parameter(scale * torch.randn(c_in, c_out, modes, modes, dtype=torch.cfloat))

    def forward(self, x):
        B, C, H, W = x.shape
        m = self.modes
        xf = torch.fft.rfft2(x)
        out = torch.zeros(B, self.w1.shape[1], H, W // 2 + 1, dtype=torch.cfloat, device=x.device)
        out[:, :, :m, :m] = torch.einsum("bixy,ioxy->boxy", xf[:, :, :m, :m], self.w1)
        out[:, :, -m:, :m] = torch.einsum("bixy,ioxy->boxy", xf[:, :, -m:, :m], self.w2)
        return torch.fft.irfft2(out, s=(H, W))


class FNO2d(nn.Module):
    def __init__(self, n_in, modes=16, width=64, layers=4, re_channel=False, N=64):
        super().__init__()
        self.n_in, self.re_channel = n_in, re_channel
        c_in = n_in + 4 + (1 if re_channel else 0)
        self.lift = nn.Conv2d(c_in, width, 1)
        self.spec = nn.ModuleList([SpectralConv2d(width, width, modes) for _ in range(layers)])
        self.pw = nn.ModuleList([nn.Conv2d(width, width, 1) for _ in range(layers)])
        self.proj1 = nn.Conv2d(width, 128, 1)
        self.proj2 = nn.Conv2d(128, 1, 1)
        g = torch.arange(N) * (2 * math.pi / N)
        Y, X = torch.meshgrid(g, g, indexing="ij")
        self.register_buffer("coords", torch.stack([X.sin(), X.cos(), Y.sin(), Y.cos()])[None].float())

    def forward(self, frames, re=None):
        """frames (B, n_in, 64, 64) scaled; re (B,) raw Reynolds numbers when re_channel. Returns (B, 64, 64)."""
        B = frames.shape[0]
        ch = [frames, self.coords.expand(B, -1, -1, -1)]
        if self.re_channel:
            ch.append(((re.float() - 40.0) / 6.0).view(B, 1, 1, 1).expand(B, 1, *frames.shape[-2:]))
        h = self.lift(torch.cat(ch, 1))
        for k, (s, p) in enumerate(zip(self.spec, self.pw)):
            h = s(h) + p(h)
            if k < len(self.spec) - 1:
                h = F.gelu(h)
        return frames[:, -1] + self.proj2(F.gelu(self.proj1(h)))[:, 0]

    def n_params(self):
        return int(sum(p.numel() * (2 if p.is_complex() else 1) for p in self.parameters()))


ARMS = {  # name: (n_in, width, re_channel, data)
    "L0": (4, 64, False, "nominal"),
    "L0big": (4, 156, False, "nominal"),
    "L_range": (8, 64, False, "range"),
    "L_param": (4, 64, True, "range"),
}


def build(arm):
    n_in, width, rc, _ = ARMS[arm]
    return FNO2d(n_in, width=width, re_channel=rc)
