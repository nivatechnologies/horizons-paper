"""Training, checkpoint selection (validation loss only) and closed-loop rollout for the learned arms."""
from __future__ import annotations

import hashlib
import json
import time

import numpy as np
import torch
import torch.nn.functional as F

from . import config, data
from .models import ArmModel, Probe, cosine_lr, train_flops
from .tokenize import kmeans_codebook

TOKEN_ARMS = ("A", "B", "D")


def model_seed(*parts):
    h = hashlib.sha256("|".join(map(str, parts)).encode()).hexdigest()
    return int(h[:8], 16)


class Standardizer:
    def __init__(self, system):
        X, _ = data.calibration(system)
        self.mu, self.sd = X.mean(0), X.std(0)

    def fwd(self, x):
        return (x - self.mu) / self.sd

    def inv(self, z):
        return z * self.sd + self.mu


def ctx_frames(delta):
    return int(config.freeze()["learned"]["context_frames"][str(delta)])


def windows(T, delta, L, n, rng):
    """Random windows of L+1 frames at interval delta from trajectories T (N, steps+1, d)."""
    sub = int(round(delta / data.DT))
    span = L * sub
    N, S, _ = T.shape
    ti = rng.integers(0, N, n)
    s0 = rng.integers(0, S - span, n)
    idx = s0[:, None] + sub * np.arange(L + 1)[None]
    return T[ti[:, None], idx]


class Task:
    """Everything one learned-arm run needs, on one device."""

    def __init__(self, system, arm, bits, delta, seed, device, noise=0.0, n_traj=None, steps=None):
        fz = config.freeze()
        self.fz, self.system, self.arm, self.bits, self.delta, self.seed = fz, system, arm, bits, delta, seed
        self.noise, self.device = noise, device
        self.L = ctx_frames(delta)
        self.std = Standardizer(system)
        self.sA = data.sigma_A(system)
        self.cb = kmeans_codebook(system, bits) if bits else None
        self.protos = self.std.fwd(self.cb.C) if self.cb is not None else None
        self.Ttr = data.train_trajectories(system, "training", n_traj=n_traj)
        self.Tva = data.train_trajectories(system, "validation")
        self.steps = steps or fz["learned"]["steps"]
        self.d = self.Ttr.shape[-1]
        self._gpu = {}
        for name, T in (("tr", self.Ttr), ("va", self.Tva)):
            g = dict(Z=torch.as_tensor(self.std.fwd(T), dtype=torch.float32, device=device), shape=T.shape)
            if self.cb is not None:
                g["tok"] = torch.as_tensor(self.cb.encode(T), device=device)
            self._gpu[name] = g
        self.tag = f"{system}_{arm}_b{bits}_D{delta}_s{seed}" + (f"_n{noise}" if arm == "C" else "") + \
                   (f"_traj{n_traj}" if n_traj else "")

    def build(self):
        torch.manual_seed(model_seed(self.tag, "init"))
        m = ArmModel(self.arm, self.d, self.cb.K if self.cb else 0, self.L,
                     protos_std=self.protos, **{k: v for k, v in self.fz["learned"]["backbone"].items()
                                                if k in ("width", "layers", "heads", "ff")})
        return m.to(self.device)

    def batch_idx(self, which, n, rng, train=True):
        """GPU batch from precomputed standardized states / tokens. Same windows as `windows`."""
        g = self._gpu[which]
        N, S, _ = g["shape"]
        sub = int(round(self.delta / data.DT))
        ti = rng.integers(0, N, n)
        s0 = rng.integers(0, S - self.L * sub, n)
        idx = s0[:, None] + sub * np.arange(self.L + 1)[None]
        ti_t = torch.as_tensor(ti[:, None], device=self.device)
        idx_t = torch.as_tensor(idx, device=self.device)
        Z = g["Z"][ti_t, idx_t]
        if self.arm in TOKEN_ARMS:
            tok = g["tok"][ti_t, idx_t]
            inp = tok[:, :-1]
            tgt = tok[:, 1:] if self.arm == "A" else (Z[:, 1:] if self.arm == "B" else Z[:, :-1])
            return inp, tgt
        x_in = Z[:, :-1]
        if train and self.noise > 0:
            scale = torch.as_tensor(self.noise * self.sA / self.std.sd, dtype=torch.float32, device=self.device)
            x_in = x_in + scale * torch.as_tensor(rng.standard_normal(x_in.shape), dtype=torch.float32,
                                                  device=self.device)
        return x_in, Z[:, 1:]

    def batch_tensors(self, W, rng, train=True):
        """W (B, L+1, d) raw states -> (inp, target) tensors for this arm."""
        dev = self.device
        if self.arm in TOKEN_ARMS:
            tok = torch.as_tensor(self.cb.encode(W), device=dev)
            inp = tok[:, :-1]
            if self.arm == "A":
                tgt = tok[:, 1:]
            elif self.arm == "B":
                tgt = torch.as_tensor(self.std.fwd(W[:, 1:]), dtype=torch.float32, device=dev)
            else:  # D: current state
                tgt = torch.as_tensor(self.std.fwd(W[:, :-1]), dtype=torch.float32, device=dev)
            return inp, tgt
        Z = self.std.fwd(W)
        x_in = Z[:, :-1]
        if train and self.noise > 0:
            x_in = x_in + (self.noise * self.sA / self.std.sd) * rng.standard_normal(x_in.shape)
        return (torch.as_tensor(x_in, dtype=torch.float32, device=dev),
                torch.as_tensor(Z[:, 1:], dtype=torch.float32, device=dev))

    def loss(self, m, inp, tgt):
        out = m(inp)
        if self.arm == "A":
            return F.cross_entropy(out.reshape(-1, out.shape[-1]), tgt.reshape(-1))
        return F.mse_loss(out, tgt)

    def train(self, log_every=500, time_limit=None):
        opt_cfg = self.fz["learned"]["optimizer"]
        m = self.build()
        opt = torch.optim.AdamW(m.parameters(), lr=opt_cfg["lr"], weight_decay=opt_cfg["weight_decay"])
        rng = np.random.default_rng(model_seed(self.tag, "data"))
        vrng = np.random.default_rng(model_seed(self.system, self.delta, "val"))
        vbatches = [self.batch_idx("va", 256, vrng, train=False) for _ in range(8)]
        best, best_state, hist = float("inf"), None, []
        B = opt_cfg["batch"]
        t0 = time.time()
        val_every = self.fz["learned"]["val_every"]
        for step in range(1, self.steps + 1):
            for g in opt.param_groups:
                g["lr"] = cosine_lr(step - 1, self.steps, opt_cfg["lr"])
            inp, tgt = self.batch_idx("tr", B, rng)
            loss = self.loss(m, inp, tgt)
            opt.zero_grad(set_to_none=True)
            loss.backward()
            opt.step()
            if step % val_every == 0 or step == self.steps:
                m.eval()
                with torch.no_grad():
                    vl = float(np.mean([self.loss(m, i, t).item() for i, t in vbatches]))
                m.train()
                hist.append(dict(step=step, train=float(loss.item()), val=vl, secs=time.time() - t0))
                if vl < best:
                    best, best_state = vl, {k: v.detach().clone() for k, v in m.state_dict().items()}
            if time_limit and time.time() - t0 > time_limit:
                break
        m.load_state_dict(best_state)
        m.eval()
        info = dict(tag=self.tag, best_val=best, history=hist, secs=time.time() - t0, steps=self.steps,
                    params=m.param_counts(), train_flops=train_flops(m, self.steps, B, self.L))
        if self.arm == "E":
            info["temperature"] = float(m.temperature)
        return m, info

    # ---------------------------------------------------------------- rollout
    @torch.no_grad()
    def rollout(self, m, hist, n_future, eps_stop=None, fut=None, chunk=500):
        """Closed-loop forecast from the context ending at t = 0.

        hist (L_ctx_available+1, n, d) raw frames ending at t = 0. Returns dict of raw-state forecasts
        (F+1, n, d) with frame 0 the arm's current-frame output (secondary score), plus diagnostics.
        If `fut` and `eps_stop` are given, stops early once every state has exceeded eps_stop.
        """
        L = self.L
        ctx = hist[-L:]                       # (L, n, d)
        n = ctx.shape[1]
        outs = []
        for c0 in range(0, n, chunk):
            r = self._rollout_chunk(m, ctx[:, c0:c0 + chunk], n_future, eps_stop,
                                    None if fut is None else fut[:, c0:c0 + chunk])
            outs.append(r)
        res = {k: np.concatenate([o[k] for o in outs], axis=1) for k in ("pred", "diag") if k in outs[0]}
        res["steps_run"] = max(o["steps_run"] for o in outs)
        if "repeat" in outs[0]:
            w = [o["pred"].shape[1] for o in outs]
            res["repeat"] = float(np.average([o["repeat"] for o in outs], weights=w))
        return res

    def _rollout_chunk(self, m, ctx, n_future, eps_stop, fut):
        dev = self.device
        L, n, d = ctx.shape
        nan = np.full((n_future + 1, n, d), np.nan)
        preds = nan.copy()
        diag = nan.copy() if self.arm == "A" else None
        if self.arm in TOKEN_ARMS:
            seq = torch.as_tensor(self.cb.encode(ctx.transpose(1, 0, 2)), device=dev)      # (n, L)
            preds[0] = self.cb.C[seq[:, -1].cpu().numpy()]
            if self.arm == "A":
                diag[0] = preds[0]
        else:
            seq = torch.as_tensor(self.std.fwd(ctx.transpose(1, 0, 2)), dtype=torch.float32, device=dev)
            preds[0] = ctx[-1]                 # C, E observe the current state
        protos_t = torch.as_tensor(self.cb.C, dtype=torch.float32, device=dev) if self.cb else None
        repeats = 0
        dead = np.zeros(n, bool)
        dead_diag = np.zeros(n, bool) if self.arm == "A" else np.ones(n, bool)
        for j in range(1, n_future + 1):
            out = m(seq)[:, -1]
            if self.arm == "A":
                nxt = out.argmax(-1)
                repeats += int((nxt == seq[:, -1]).sum())
                preds[j] = self.cb.C[nxt.cpu().numpy()]
                p = torch.softmax(out.double(), -1)
                diag[j] = (p @ protos_t.double()).cpu().numpy()
                seq = torch.cat([seq[:, 1:], nxt[:, None]], 1)
            elif self.arm == "B":
                x = self.std.inv(out.double().cpu().numpy())
                preds[j] = x
                tok = torch.as_tensor(self.cb.encode(x), device=dev)
                seq = torch.cat([seq[:, 1:], tok[:, None]], 1)
            else:  # C, E
                preds[j] = self.std.inv(out.double().cpu().numpy())
                seq = torch.cat([seq[:, 1:], out[:, None].float()], 1)
            if fut is not None and eps_stop is not None:
                dead |= np.linalg.norm(preds[j] - fut[j], axis=-1) / self.sA > eps_stop
                if self.arm == "A":
                    dead_diag |= np.linalg.norm(diag[j] - fut[j], axis=-1) / self.sA > eps_stop
                if dead.all() and dead_diag.all():
                    break
        res = dict(pred=preds, steps_run=j)
        if self.arm == "A":
            res["diag"] = diag
            res["repeat"] = repeats / (n * j)
        return res

    @torch.no_grad()
    def reconstruct(self, m, hist):
        """D: reconstruction of the current (t = 0) state from the token context."""
        seq = torch.as_tensor(self.cb.encode(hist[-self.L:].transpose(1, 0, 2)), device=self.device)
        out = [m(seq[i:i + 500])[:, -1] for i in range(0, seq.shape[0], 500)]
        return self.std.inv(torch.cat(out).double().cpu().numpy())

    @torch.no_grad()
    def a_hidden(self, m, hist):
        seq = torch.as_tensor(self.cb.encode(hist[-self.L:].transpose(1, 0, 2)), device=self.device)
        return torch.cat([m.hidden(seq[i:i + 500])[:, -1] for i in range(0, seq.shape[0], 500)])


def train_probe(task: Task, a_model, kind, steps=3000, lr=1e-3):
    """Linear / two-layer MLP readout of the current state from frozen A's final hidden states."""
    dev = task.device
    torch.manual_seed(model_seed(task.tag, "probe", kind))
    pr = Probe(kind, task.d).to(dev)
    opt = torch.optim.AdamW(pr.parameters(), lr=lr, weight_decay=0.0)
    rng = np.random.default_rng(model_seed(task.tag, "probe-data", kind))
    vrng = np.random.default_rng(model_seed(task.system, task.delta, "probe-val"))
    Wv = windows(task.Tva, task.delta, task.L, 2048, vrng)

    def feats(W):
        tok = torch.as_tensor(task.cb.encode(W[:, :-1]), device=dev)
        with torch.no_grad():
            h = a_model.hidden(tok)
        y = torch.as_tensor(task.std.fwd(W[:, :-1]), dtype=torch.float32, device=dev)
        return h, y

    vb = [feats(Wv[i:i + 256]) for i in range(0, 2048, 256)]
    best, best_state = float("inf"), None
    for step in range(1, steps + 1):
        for g in opt.param_groups:
            g["lr"] = cosine_lr(step - 1, steps, lr)
        h, y = feats(windows(task.Ttr, task.delta, task.L, 256, rng))
        loss = F.mse_loss(pr(h), y)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        if step % 250 == 0 or step == steps:
            with torch.no_grad():
                vl = float(np.mean([F.mse_loss(pr(h), y).item() for h, y in vb]))
            if vl < best:
                best, best_state = vl, {k: v.detach().clone() for k, v in pr.state_dict().items()}
    pr.load_state_dict(best_state)
    pr.eval()
    return pr, dict(best_val=best, kind=kind)


def save_json(obj, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=1, default=float))
