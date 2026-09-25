"""Post-freeze extension E4: learned arms on patch-tokenized frames (ext_freeze.yaml ks.e4; Amendments 1 A7, 2 B3).

Input contract. A context of F frames, each of P patch tokens, is flattened frame-major into F*P positions. Each
position carries a token embedding (A, B: shared embedding of the patch's code id; C: linear adapter of the patch
values) plus a learned patch-position embedding (P, width) and a learned frame (time) embedding (F, width).

Masking contract (B3). Attention is block-causal in time: a position in frame f attends to every position of frames
<= f (full attention within an observed frame) and to nothing in frames > f. The output at patch p of frame t
predicts patch p of frame t+1; targets are shifted by one whole frame. Hence every prediction for frame t+1 depends
only on frames <= t; tests/ext/test_prefix_invariance.py checks this bitwise for A, B and C.

Heads (A7). A: one shared categorical head over the K codes for all patch positions. B: one shared linear head to the
patch values, residual on the current patch's prototype. C: shared linear head, residual on the current patch values.
Backbone as the original freeze: pre-LN encoder layers, GELU, no dropout, final LayerNorm.
"""
from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


def block_causal_mask(frames, P, device=None):
    """(F*P, F*P) float mask: 0 where key frame <= query frame, -inf otherwise."""
    fr = torch.arange(frames, device=device).repeat_interleave(P)
    allowed = fr[None, :] <= fr[:, None]
    m = torch.zeros(allowed.shape, device=device)
    m[~allowed] = float("-inf")
    return m


class PatchSeqModel(nn.Module):
    def __init__(self, arm, frames, P, d_patch, K=0, protos_std=None, width=128, layers=4, heads=4, ff=512):
        super().__init__()
        assert arm in ("A", "B", "C")
        self.arm, self.frames, self.P, self.d_patch, self.K = arm, frames, P, d_patch, K
        if arm in ("A", "B"):
            self.adapter = nn.Embedding(K, width)
        else:
            self.adapter = nn.Linear(d_patch, width)
        self.pos_patch = nn.Parameter(torch.zeros(P, width))
        self.pos_time = nn.Parameter(torch.zeros(frames, width))
        nn.init.normal_(self.pos_patch, std=0.02)
        nn.init.normal_(self.pos_time, std=0.02)
        layer = nn.TransformerEncoderLayer(width, heads, ff, dropout=0.0, activation="gelu", batch_first=True,
                                           norm_first=True)
        self.enc = nn.TransformerEncoder(layer, layers, enable_nested_tensor=False)
        self.norm = nn.LayerNorm(width)
        self.head = nn.Linear(width, K if arm == "A" else d_patch)
        if protos_std is not None:
            self.register_buffer("protos", torch.as_tensor(protos_std, dtype=torch.float32))
        else:
            self.protos = None
        self.register_buffer("mask", block_causal_mask(frames, P), persistent=False)

    def hidden(self, x):
        """x: token ids (B, T, P) for A/B, or patch values (B, T, P, d_patch) for C; T <= frames. -> (B, T, P, width)"""
        B, T = x.shape[:2]
        h = self.adapter(x)                                               # (B, T, P, width)
        h = h + self.pos_patch[None, None] + self.pos_time[None, :T, None]
        h = h.reshape(B, T * self.P, -1)
        n = T * self.P
        h = self.enc(h, mask=self.mask[:n, :n])
        return self.norm(h).reshape(B, T, self.P, -1)

    def forward(self, x):
        """Predictions for frames 1..T from frames 0..T-1: logits (B, T, P, K) for A; patch values (B, T, P, d) for B, C."""
        h = self.hidden(x)
        out = self.head(h)
        if self.arm == "A":
            return out
        base = self.protos[x] if self.arm == "B" else x
        return base + out

    def param_counts(self):
        tot = sum(p.numel() for p in self.parameters())
        return dict(total=tot, adapter=sum(p.numel() for p in self.adapter.parameters()),
                    embeddings=self.pos_patch.numel() + self.pos_time.numel(),
                    backbone=sum(p.numel() for p in self.enc.parameters()) + sum(p.numel() for p in self.norm.parameters()),
                    head=sum(p.numel() for p in self.head.parameters()))

    def loss(self, x_in, target):
        out = self(x_in)
        if self.arm == "A":
            return F.cross_entropy(out.reshape(-1, out.shape[-1]), target.reshape(-1))
        return F.mse_loss(out, target)


def train_flops(model: PatchSeqModel, steps, batch):
    """6 * dense params * tokens + attention (score and value products, forward and backward)."""
    n_tok = model.frames * model.P
    dense = model.param_counts()["total"] - (model.adapter.weight.numel() if model.arm in ("A", "B") else 0)
    width = model.pos_patch.shape[1]
    L = len(model.enc.layers)
    attn = 3 * steps * batch * L * 2 * 2 * n_tok * n_tok * width / 2
    return float(6 * dense * steps * batch * n_tok + attn)
