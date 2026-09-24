"""Learned arms on one backbone. Section 2.7 of the freeze.

Backbone (identical for every arm): causal pre-LN transformer, 4 layers, width 128, 4 heads,
feed-forward 512, GELU, no dropout, learned absolute positional embeddings over the context.

Arms differ only in the input adapter and the head:
  A   token IDs -> embedding            categorical head over codes, cross-entropy on the next token
  B   token IDs -> embedding            continuous head, MSE on the next state
  C   state coordinates -> linear       continuous head, MSE on the next state
  D   token IDs -> embedding            continuous head, MSE on the CURRENT state
  E   state coordinates -> linear       continuous head softly projected onto the prototypes (learned temperature)

Continuous heads are residual on the decoded current input frame, in standardized coordinates:
B and D add to the prototype of the current token, C and E add to the current state. This keeps
the B-versus-C comparison about what the input carries, not about the head parameterization.
"""
from __future__ import annotations

import math

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

TOKEN_ARMS = ("A", "B", "D")
STATE_ARMS = ("C", "E")


class Backbone(nn.Module):
    def __init__(self, ctx, width=128, layers=4, heads=4, ff=512):
        super().__init__()
        self.pos = nn.Parameter(torch.zeros(ctx, width))
        nn.init.normal_(self.pos, std=0.02)
        layer = nn.TransformerEncoderLayer(width, heads, ff, dropout=0.0, activation="gelu",
                                           batch_first=True, norm_first=True)
        self.enc = nn.TransformerEncoder(layer, layers, enable_nested_tensor=False)
        self.norm = nn.LayerNorm(width)
        self.register_buffer("mask", torch.triu(torch.full((ctx, ctx), float("-inf")), 1), persistent=False)

    def forward(self, h):
        T = h.shape[1]
        h = h + self.pos[:T]
        h = self.enc(h, mask=self.mask[:T, :T], is_causal=True)
        return self.norm(h)


class ArmModel(nn.Module):
    def __init__(self, arm, d, K, ctx, protos_std=None, width=128, layers=4, heads=4, ff=512):
        super().__init__()
        self.arm, self.d, self.K, self.ctx = arm, d, K, ctx
        if arm in TOKEN_ARMS:
            self.adapter = nn.Embedding(K, width)
        else:
            self.adapter = nn.Linear(d, width)
        self.backbone = Backbone(ctx, width, layers, heads, ff)
        self.head = nn.Linear(width, K if arm == "A" else d)
        if protos_std is not None:
            self.register_buffer("protos", torch.as_tensor(protos_std, dtype=torch.float32))
        else:
            self.protos = None
        if arm == "E":
            self.log_temp = nn.Parameter(torch.zeros(()))

    @property
    def temperature(self):
        return 1e-3 + F.softplus(self.log_temp)

    def hidden(self, inp):
        return self.backbone(self.adapter(inp))

    def forward(self, inp):
        """inp: token IDs (B, T) or standardized states (B, T, d). Returns logits or standardized states."""
        h = self.hidden(inp)
        out = self.head(h)
        if self.arm == "A":
            return out
        base = self.protos[inp] if self.arm in TOKEN_ARMS else inp
        y = base + out
        if self.arm == "E":
            d2 = ((y[..., None, :] - self.protos) ** 2).sum(-1)
            w = torch.softmax(-d2 / self.temperature, -1)
            y = w @ self.protos
        return y

    def param_counts(self):
        tot = sum(p.numel() for p in self.parameters())
        bb = sum(p.numel() for p in self.backbone.parameters())
        hd = sum(p.numel() for p in self.head.parameters())
        ad = sum(p.numel() for p in self.adapter.parameters())
        return dict(total=tot, backbone=bb, head=hd, adapter=ad)


def train_flops(model: ArmModel, steps, batch, ctx):
    """6 * params * tokens for the dense part plus the attention score/value products (forward x3)."""
    n = model.param_counts()["total"] - (model.adapter.weight.numel() if model.arm in TOKEN_ARMS else 0)
    tokens = steps * batch * ctx
    L = len(model.backbone.enc.layers)
    width = model.backbone.pos.shape[1]
    attn = 3 * steps * batch * L * 2 * 2 * ctx * ctx * width / 2
    return float(6 * n * tokens + attn)


class Probe(nn.Module):
    def __init__(self, kind, d, width=128, hidden=256):
        super().__init__()
        self.net = nn.Linear(width, d) if kind == "linear" else nn.Sequential(
            nn.Linear(width, hidden), nn.GELU(), nn.Linear(hidden, d))

    def forward(self, h):
        return self.net(h)


def cosine_lr(step, total, base):
    return base * 0.5 * (1 + math.cos(math.pi * min(step, total) / total))
