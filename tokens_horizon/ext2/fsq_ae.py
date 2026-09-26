"""EXT2 FSQ autoencoder (ext2_freeze.yaml `tokenizer`): VQGAN-style convolutional encoder/decoder with residual blocks,
circular padding (periodic domain), finite scalar quantization (Mentzer et al. 2023, arXiv:2309.15505, sec. 3 and
appendix A.1 code; Table 1 level sets). No attention, no adversarial or perceptual loss.

Input/output: vorticity grids (B, 64, 64) in units of sigma_A / 64, so that mean over the 4,096 grid values of the
squared difference equals ||x - x_hat||^2 / sigma_A^2, the scored relative squared error.

Encoder: conv3x3(1 -> ch*m0); for each resolution level i < n_down: n_res ResBlocks at ch*m_i, stride-2 conv3x3
(-> ch*m_{i+1}); bottom: n_res ResBlocks at ch*m_last; GroupNorm, SiLU, conv3x3 -> d = len(levels); FSQ.
Decoder mirrors it with nearest-neighbour x2 upsampling followed by conv3x3. All 3x3 convolutions use circular
padding. ResBlock: GN(32)-SiLU-conv3x3-GN(32)-SiLU-conv3x3 plus identity (1x1 conv when channels change).
Channel multipliers: 8x8 latent (3 downsamplings) (1, 2, 2, 4); 16x16 latent (2 downsamplings) (1, 2, 4); ch = 64.
"""
from __future__ import annotations

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

CH = 64
N_RES = 2
MULTS = {8: (1, 2, 2, 4), 16: (1, 2, 4)}


def conv3(i, o, stride=1):
    return nn.Conv2d(i, o, 3, stride=stride, padding=1, padding_mode="circular")


def gn(c):
    return nn.GroupNorm(32, c, eps=1e-6)


class ResBlock(nn.Module):
    def __init__(self, i, o):
        super().__init__()
        self.n1, self.c1, self.n2, self.c2 = gn(i), conv3(i, o), gn(o), conv3(o, o)
        self.skip = nn.Conv2d(i, o, 1) if i != o else nn.Identity()

    def forward(self, x):
        h = self.c1(F.silu(self.n1(x)))
        h = self.c2(F.silu(self.n2(h)))
        return self.skip(x) + h


class FSQ(nn.Module):
    """Finite scalar quantization on the channel axis. bound(): tanh with the offset for even levels (the paper's
    appendix listing writes tan(offset / half_l); the reference implementation uses arctanh, used here)."""

    def __init__(self, levels):
        super().__init__()
        L = torch.tensor(levels, dtype=torch.float32)
        self.register_buffer("L", L)
        self.register_buffer("basis", torch.tensor(np.concatenate([[1], np.cumprod(levels[:-1])]), dtype=torch.float64))
        self.levels = list(levels)
        self.d = len(levels)
        self.n_codes = int(np.prod(levels))

    def _shape(self, t):
        return t.view(1, -1, 1, 1)

    def bound(self, z):
        eps = 1e-3
        half_l = self._shape((self.L - 1) * (1 - eps) / 2)
        offset = self._shape(torch.where(self.L % 2 == 1, 0.0, 0.5))
        shift = torch.atanh(offset / half_l)
        return torch.tanh(z + shift) * half_l - offset

    def forward(self, z):
        b = self.bound(z)
        q = b + (torch.round(b) - b).detach()
        return q / self._shape(torch.div(self.L, 2, rounding_mode="floor"))

    def level_index(self, zq):
        """Normalized codes (B, d, h, w) -> integer level per dimension in 0..L-1."""
        hw = self._shape(torch.div(self.L, 2, rounding_mode="floor"))
        return torch.round(zq * hw + hw).long()

    def code_index(self, zq):
        lv = self.level_index(zq).double()
        return (lv * self._shape(self.basis)).sum(1).long()


class FSQAE(nn.Module):
    def __init__(self, latent_side, levels, ch=CH, n_res=N_RES):
        super().__init__()
        mults = MULTS[latent_side]
        n_down = len(mults) - 1
        assert 64 // 2 ** n_down == latent_side
        chs = [ch * m for m in mults]
        enc = [conv3(1, chs[0])]
        for i in range(n_down):
            enc += [ResBlock(chs[i], chs[i]) for _ in range(n_res)]
            enc += [conv3(chs[i], chs[i + 1], stride=2)]
        enc += [ResBlock(chs[-1], chs[-1]) for _ in range(n_res)]
        enc += [gn(chs[-1]), nn.SiLU(), conv3(chs[-1], len(levels))]
        self.encoder = nn.Sequential(*enc)
        self.quant = FSQ(levels)
        dec = [conv3(len(levels), chs[-1])]
        dec += [ResBlock(chs[-1], chs[-1]) for _ in range(n_res)]
        for i in reversed(range(n_down)):
            dec += [nn.Upsample(scale_factor=2, mode="nearest"), conv3(chs[i + 1], chs[i])]
            dec += [ResBlock(chs[i], chs[i]) for _ in range(n_res)]
        dec += [gn(chs[0]), nn.SiLU(), conv3(chs[0], 1)]
        self.decoder = nn.Sequential(*dec)
        self.latent_side = latent_side

    def encode(self, x):
        return self.quant(self.encoder(x[:, None]))

    def decode(self, zq):
        return self.decoder(zq)[:, 0]

    def forward(self, x):
        zq = self.encode(x)
        return self.decode(zq), zq

    def param_counts(self):
        c = lambda m: int(sum(p.numel() for p in m.parameters()))
        return dict(encoder=c(self.encoder), decoder=c(self.decoder), quantizer=0, total=c(self))


CONFIGS = {
    "L8-b10": (8, [8, 5, 5, 5]),
    "L8-b12": (8, [7, 5, 5, 5, 5]),
    "L8-b16": (8, [8, 8, 8, 5, 5, 5]),
    "L16-b10": (16, [8, 5, 5, 5]),
    "L16-b12": (16, [7, 5, 5, 5, 5]),
}


def build(name):
    side, levels = CONFIGS[name]
    return FSQAE(side, levels)
