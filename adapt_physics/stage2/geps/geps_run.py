"""GEPS (Kassai Koupai et al., NeurIPS 2024; official code github.com/itsakk/geps, commit e9a8652, imported unmodified from a
clone - it carries no license file, so it is not vendored here) as a learned adaptive opponent (geps_freeze.yaml).

Fully data-driven variant (type_augment = ''): Forecaster('kolmo', ...) = NeuralODE whose derivative is the GEPS FNO2d
(10 x 10 modes, width 64, 4 layers, Swish) with low-rank context conditioning; integration as in the released code
(torchdiffeq, method hard-coded 'euler', one step per output time). Published Kolmogorov recipe (paper Table 12 +
train.py/adapt.py): context c = 4, width 64, depth 4, batch 4, epochs 20000 (capped at 8 h wall), Adam lr 1e-2 betas
(0.9, 0.999), ReduceLROnPlateau(factor 0.9, patience 350, threshold 0.01 rel, min_lr 1e-5) on the epoch train loss,
RelativeL2 loss on the rollout, no teacher forcing, orthogonal init (gain 1) of A, B, weight. Adaptation (adapt.py):
codes initialised to the mean training code, all weights frozen, Adam lr 1e-2 on the code only, ReduceLROnPlateau(0.9,
patience 50, 0.01 rel, min_lr 1e-5) on the epoch loss, MSE loss on the rollout, 500 epochs (published) or 5000 (10x).

Changes needed to read our data (all recorded in the freeze):
  * data: 64 x 64 vorticity scaled by 64 / sigma_A(Re 40, World D); frame interval Delta = 0.35 (t = 0.35 k);
  * environments: one per training trajectory (1,024; the code handles any number of codes);
  * training samples: one 20-frame window (the published trajectory length) per trajectory per epoch, random start;
    +2% sigma_A white noise on the initial frame (the rollout input), clean targets;
  * checkpoint: best RelativeL2 on the validation set (fixed 20-frame windows) every 50 epochs; the 8 h cap binds;
  * adaptation: one environment per test state; its data = the w = 11 noisy post-change observations as one
    trajectory (rollout from frame 1, the only use of the window the 1-frame-input model allows); states adapted in
    parallel with a per-state Adam + plateau schedule, exactly equivalent to adapting each state alone;
  * forecast: from the (noisy) frame 11 with the adapted code, F frames; errors against the truth grids.

Usage (on a Spark, cwd = ~/geps_work):
  python geps_run.py train <range|range_wide> <seed> <hours> [lr] [val_every (default 50)] [max_epochs] [stop_rule|-] [resume_epoch]
  python geps_run.py adapt <run> <panel> <steps|0> <nominal|batched> <i0> <i1>
        (states i0..i1-1 of the panel adapted in one batched pass; nominal = no-adaptation reference code fitted on Re-40 data)
  python geps_run.py pilot <run> <B> <steps>                   (batched adaptation throughput on training data)
  python geps_run.py time <run> <steps> [n_states (default 23: 3 warm-up + 20 timed)]                        (batch-1 timing, 20 states, fixed F frames)
"""
import json
import math
import os
import sys
import time
from functools import partial
from pathlib import Path

import numpy as np
import torch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "geps"))                  # the official clone
from geps.model.forecasters import Forecaster  # noqa: E402
from geps.utils import init_weights  # noqa: E402
from geps.losses import RelativeL2  # noqa: E402
import geps_fast  # noqa: E402

geps_fast.patch()                                        # equivalent low-rank reformulation (verified; see geps_fast.py)
torch.backends.cudnn.allow_tf32 = False                  # full FP32 (the released einsum path does not use TF32)
torch.backends.cuda.matmul.allow_tf32 = False

DATA = HERE / "data"
RUNS = HERE / "runs"
DELTA, T_WIN, PRE, W = 0.35, 20, 10, 11
CFG = dict(state_c=1, hidden_c=64, code_c=4, factor=1, is_complete=True, type_augment="", method="euler", options=None,
           batch=4, lr=1e-2, epochs=20000, sched=dict(factor=0.9, patience=350, threshold=0.01, min_lr=1e-5),
           adapt_lr=1e-2, adapt_sched=dict(factor=0.9, patience=50, threshold=0.01, min_lr=1e-5),
           init={"A": {"type": "orthogonal", "gain": 1}, "B": {"type": "orthogonal", "gain": 1},
                 "weight": {"type": "orthogonal", "gain": 1}})


def meta():
    return json.loads((DATA / "meta.json").read_text())


def build(n_env, device):
    m = Forecaster("kolmo", CFG["state_c"], CFG["hidden_c"], CFG["code_c"], CFG["factor"], n_env, CFG["is_complete"],
                   CFG["type_augment"], CFG["method"], CFG["options"]).to(device)
    return m


def to_states(x):
    """(B, T, 64, 64) -> GEPS layout (B, 1, 64, 64, T)."""
    return x.permute(0, 2, 3, 1).unsqueeze(1)


def train(data, seed, hours, lr=None, val_every=50, max_epochs=None, stop_rule=False, resume=None):
    """stop_rule (pre-registered deviation, Todd 2026-09-28): stop once validation improved by < 1% of the previous check at
    two consecutive checks; max_epochs caps the epochs (50). resume = <start_epoch>: continue the run in its directory from
    last.pt (weights) or state.pt (weights + Adam + scheduler + RNG, when saved), keeping the validation history and best."""
    seed, hours, val_every = int(seed), float(hours), int(val_every)
    max_epochs = CFG["epochs"] if max_epochs is None else int(max_epochs)
    lr = CFG["lr"] if lr is None else float(lr)                # deviation option (GEPS-wide: 1e-3 after divergence at 1e-2)
    torch.manual_seed(seed)
    np.random.seed(seed)
    rng = np.random.default_rng(seed)
    dev = torch.device("cuda")
    sc = 64.0 / meta()["sigma40"]
    X = np.load(DATA / f"train_{data}.npy", mmap_mode="r")
    V = np.load(DATA / f"val_{data}.npy", mmap_mode="r")
    n_env, nf = X.shape[:2]
    run = RUNS / (f"geps_{data}_s{seed}" + ("" if lr == CFG["lr"] else f"_lr{lr:g}"))
    run.mkdir(parents=True, exist_ok=True)
    model = build(n_env, dev)
    init_weights(model, init_config=CFG["init"])
    opt = torch.optim.Adam(model.parameters(), lr, betas=(0.9, 0.999))
    s = CFG["sched"]
    sched = torch.optim.lr_scheduler.ReduceLROnPlateau(opt, mode="min", factor=s["factor"], patience=s["patience"],
                                                       threshold=s["threshold"], threshold_mode="rel", cooldown=0,
                                                       min_lr=s["min_lr"], eps=1e-08)
    crit = RelativeL2()
    t = torch.arange(T_WIN, device=dev, dtype=torch.float32) * DELTA
    vr = np.random.default_rng(1)
    vi, vk = vr.integers(0, V.shape[0], 64), vr.integers(0, V.shape[1] - T_WIN + 1, 64)
    vx = torch.as_tensor(np.stack([V[i, k:k + T_WIN] for i, k in zip(vi, vk)]) * sc, dtype=torch.float32, device=dev)
    with torch.no_grad():                                          # no-change forecast on the same windows (collapse check)
        pv = to_states(vx)
        persist = float(crit(pv[..., :1].expand_as(pv).contiguous(), pv))
    t0 = time.time()
    log = open(run / "train.log", "a")
    log.write(json.dumps(dict(persistence_val_loss=persist, val_every=val_every, lr=lr)) + "\n")
    best, best_ep, ep, steps = float("inf"), -1, 0, 0
    hist = []
    resumed = None
    if resume is not None:
        ep = int(resume)
        prev = [json.loads(x) for x in (run / "train.log").read_text().splitlines() if x.startswith("{")]
        hist = [(x["epoch"], x["val_loss"]) for x in prev if "epoch" in x]
        best_ep, best = min(hist, key=lambda h: h[1])
        pinfo = json.loads((run / "info.json").read_text()) if (run / "info.json").exists() else {}
        steps = int(pinfo.get("steps", max(x.get("steps", 0) for x in prev if "epoch" in x)))
        if (run / "state.pt").exists():
            st = torch.load(run / "state.pt", map_location=dev, weights_only=False)
            model.load_state_dict(st["model"])
            opt.load_state_dict(st["opt"])
            sched.load_state_dict(st["sched"])
            rng.bit_generator.state = st["rng"]
            resumed = "state.pt (weights, Adam, scheduler, RNG)"
        else:
            model.load_state_dict(torch.load(run / "last.pt", map_location=dev))
            rng = np.random.default_rng([seed, ep])               # fresh window stream (the old one was not saved)
            resumed = "last.pt weights only; Adam moments, scheduler counters and RNG were not saved by the capped run: fresh"
        log.write(json.dumps(dict(resumed_at_epoch=ep, steps=steps, source=resumed, stop_rule=bool(stop_rule),
                                  max_epochs=max_epochs)) + "\n")
        log.flush()
    cap = hours * 3600
    stop_reason = None
    while ep < max_epochs and time.time() - t0 < cap:
        model.train()
        perm = rng.permutation(n_env)
        tot = 0.0
        for b in range(0, n_env, CFG["batch"]):
            env = perm[b:b + CFG["batch"]]
            k = rng.integers(0, nf - T_WIN + 1, len(env))
            x = torch.as_tensor(np.stack([X[e, kk:kk + T_WIN] for e, kk in zip(env, k)]) * sc, dtype=torch.float32, device=dev)
            y = to_states(x)
            yin = y.clone()
            yin[..., 0] += torch.randn_like(yin[..., 0]) * 0.02
            out = model(yin, t, torch.as_tensor(env, device=dev))
            loss = crit(out, y)
            loss.backward()
            opt.step()
            opt.zero_grad()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.)     # as released (after the step)
            tot += loss.item() * len(env)
            steps += 1
            if time.time() - t0 >= cap:
                break
        sched.step(tot / n_env)
        if ep % val_every == 0:
            model.eval()
            with torch.no_grad():
                # validation environments are unseen: evaluate with the mean training code (adaptation-free proxy)
                mc = model.derivative.codes.data.mean(0, keepdim=True)
                keep = model.derivative.codes.data.clone()
                model.derivative.codes.data[:1] = mc
                vl = float(crit(model(to_states(vx), t, torch.zeros(64, dtype=torch.long, device=dev)), to_states(vx)))
                model.derivative.codes.data.copy_(keep)
            rec = dict(epoch=ep, steps=steps, train_loss=tot / n_env, val_loss=vl, lr=opt.param_groups[0]["lr"],
                       seconds=time.time() - t0, persistence_val_loss=persist)
            log.write(json.dumps(rec) + "\n")
            log.flush()
            if vl < best:
                best, best_ep = vl, ep
                torch.save(model.state_dict(), run / "best.pt")
            hist.append((ep, vl))
            torch.save(dict(model=model.state_dict(), opt=opt.state_dict(), sched=sched.state_dict(), rng=rng.bit_generator.state,
                            epoch=ep, steps=steps), run / "state.pt.tmp")
            os.replace(run / "state.pt.tmp", run / "state.pt")
            if stop_rule and len(hist) >= 3 and all((hist[i - 1][1] - hist[i][1]) / hist[i - 1][1] < 0.01 for i in (-1, -2)):
                stop_reason = f"stopping rule: < 1% improvement at two consecutive checks (epochs {hist[-2][0]}, {hist[-1][0]})"
                log.write(json.dumps(dict(stopped=stop_reason)) + "\n")
                log.flush()
                ep += 1
                break
            if val_every < 50 and ep == 4 and abs(vl - persist) < 1e-4:     # Todd 2026-09-28: collapse stop at epoch 4
                (run / "COLLAPSED").write_text(json.dumps(dict(epoch=ep, val_loss=vl, persistence=persist)))
                log.write(json.dumps(dict(stopped="collapsed to persistence at epoch 4", val_loss=vl, persistence=persist)) + "\n")
                log.flush()
                break
        ep += 1
    torch.save(model.state_dict(), run / "last.pt")
    if stop_reason is None:
        stop_reason = f"max_epochs {max_epochs}" if ep >= max_epochs else "time cap"
    info = dict(data=data, seed=seed, lr=lr, epochs_done=ep, steps=steps, cap_hours=hours, cap_bound=stop_reason == "time cap",
                stopped_by=stop_reason, resumed=resumed, max_epochs=max_epochs, stop_rule=bool(stop_rule),
                best_val=best, best_epoch=best_ep, train_seconds=time.time() - t0, n_env=n_env, cfg={k: v for k, v in CFG.items()},
                params=int(sum(p.numel() for p in model.parameters())), torch=torch.__version__)
    (run / "info.json").write_text(json.dumps(info, indent=1, default=str))
    print("done", info["epochs_done"], "epochs", steps, "steps; best val", best, "at epoch", best_ep, flush=True)


class PerStateAdam:
    """torch.optim.Adam (betas 0.9/0.999, eps 1e-8, no weight decay) + ReduceLROnPlateau(mode min, rel threshold,
    cooldown 0), applied independently to each row of a (n, c) parameter: identical to running one optimizer and one
    scheduler per state."""

    def __init__(self, p, lr, sched):
        self.p, self.n = p, p.shape[0]
        self.m = torch.zeros_like(p)
        self.v = torch.zeros_like(p)
        self.t = 0
        self.lr = torch.full((self.n, 1), float(lr), device=p.device, dtype=p.dtype)
        self.s = sched
        self.best = torch.full((self.n,), float("inf"), device=p.device, dtype=torch.float64)
        self.bad = torch.zeros(self.n, dtype=torch.long, device=p.device)

    @torch.no_grad()
    def step(self, g):
        self.t += 1
        self.m.mul_(0.9).add_(g, alpha=0.1)
        self.v.mul_(0.999).addcmul_(g, g, value=0.001)
        bc1, bc2 = 1 - 0.9 ** self.t, 1 - 0.999 ** self.t
        denom = (self.v.sqrt() / math.sqrt(bc2)).add_(1e-8)
        self.p.sub_(self.lr / bc1 * self.m / denom)            # torch.optim.Adam update, per-row learning rate

    @torch.no_grad()
    def sched_step(self, loss):
        loss = loss.double()
        better = loss < self.best * (1 - self.s["threshold"])
        self.best = torch.where(better, loss, self.best)
        self.bad = torch.where(better, torch.zeros_like(self.bad), self.bad + 1)
        red = self.bad > self.s["patience"]
        new = torch.clamp(self.lr * self.s["factor"], min=self.s["min_lr"])
        do = red[:, None] & ((self.lr - new) > 1e-8)
        self.lr = torch.where(do, new, self.lr)
        self.bad = torch.where(red, torch.zeros_like(self.bad), self.bad)


def load_trained(run, n_env, dev):
    sd = torch.load(RUNS / run / "best.pt", map_location=dev)
    ctr = sd["derivative.codes"].mean(0)
    model = build(n_env, dev)
    sd = {k: v for k, v in sd.items() if "codes" not in k and "model_phy" not in k}
    missing = model.load_state_dict(sd, strict=False)
    with torch.no_grad():
        model.derivative.codes.data[:] = ctr                  # adapt.py: codes <- mean training code
    for name, p in model.named_parameters():
        p.requires_grad = "codes" in name
    return model, ctr


def adapt_codes(model, Yw, steps, dev, shared=False):
    """Yw (n, T, 64, 64) scaled observations. shared=False: one environment (code) per trajectory (per test state).
    shared=True: all n trajectories are one environment with one code (the no-adaptation Re-40 reference).
    Returns adapted codes, final per-environment losses."""
    n, T = Yw.shape[:2]
    t = torch.arange(T, device=dev, dtype=torch.float32) * DELTA
    y = to_states(Yw)
    code = model.derivative.codes
    opt = PerStateAdam(code.data, CFG["adapt_lr"], CFG["adapt_sched"])
    env = torch.zeros(n, dtype=torch.long, device=dev) if shared else torch.arange(n, device=dev)
    for _ in range(int(steps)):
        out = model(y, t, env)
        per = ((out - y) ** 2).flatten(1).mean(1)             # MSELoss per trajectory (adapt.py criterion)
        if shared:
            per = per.mean(0, keepdim=True)                     # MSELoss over the environment's trajectories
        g, = torch.autograd.grad(per.sum(), code)
        opt.step(g)
        opt.sched_step(per.detach())
    return code.data.clone(), per.detach()


def forecast_errors(model, y0, truth, F, sA_scaled, dev, chunk=40):
    """Integrate from y0 (n, 64, 64) for F frames; errors vs truth (F+1, n, 64, 64) scaled; returns (F+1, n)."""
    n = y0.shape[0]
    env = torch.arange(n, device=dev)
    err = np.empty((F + 1, n))
    err[0] = (np.sqrt(((y0.cpu().numpy() - truth[0]) ** 2).sum((-2, -1))) / sA_scaled)
    y = y0[:, None]
    j = 0
    with torch.no_grad():
        while j < F:
            k = min(chunk, F - j)
            t = torch.arange(k + 1, device=dev, dtype=torch.float32) * DELTA
            res = model.int_(partial(model.derivative, env=env), y0=y, t=t, method=model.method, options=model.options)
            for i in range(1, k + 1):
                err[j + i] = np.sqrt(((res[i][:, 0].cpu().numpy() - truth[j + i]) ** 2).sum((-2, -1))) / sA_scaled
            y = res[-1]
            j += k
    return err


def adapt(run, panel, steps, nominal=False, i0=0, i1=None):
    dev = torch.device("cuda")
    M = meta()
    sc = 64.0 / M["sigma40"]
    tp = M["panels"][panel]
    sA, F = tp["sigma_A"], tp["F"]
    T = np.load(DATA / f"{panel}.npy", mmap_mode="r")
    Y = np.load(DATA / f"{panel}_obs.npy", mmap_mode="r")
    i1 = T.shape[1] if i1 is None else int(i1)
    i0 = int(i0)
    sl = slice(i0, i1)
    n = i1 - i0
    out = RUNS / run / "eval"
    out.mkdir(parents=True, exist_ok=True)
    tag = ("noadapt" if nominal else f"adapt{steps}") + f"_states{i0}-{i1}"
    f = out / f"{panel}_{tag}.npz"
    if f.exists():
        return
    model, ctr = load_trained(run, n, dev)
    t0 = time.time()
    if nominal:
        Nm = np.load(DATA / "nominal32.npy")                     # 32 Re-40 trajectories x 11 frames
        m2, _ = load_trained(run, 1, dev)
        codes, _ = adapt_codes(m2, torch.as_tensor(Nm * sc, dtype=torch.float32, device=dev), 500, dev, shared=True)
        c40 = codes[0]
        with torch.no_grad():
            model.derivative.codes.data[:] = c40
        losses = None
    else:
        Yw = torch.as_tensor(np.asarray(Y[PRE + 1:PRE + W + 1, sl]).transpose(1, 0, 2, 3) * sc, dtype=torch.float32, device=dev)
        codes, losses = adapt_codes(model, Yw, steps, dev)
    ta = time.time() - t0
    y0 = torch.as_tensor(np.asarray(Y[PRE + W, sl]) * sc, dtype=torch.float32, device=dev)
    truth = np.asarray(T[PRE + W:PRE + W + F + 1, sl], dtype=np.float32) * sc
    err = forecast_errors(model, y0, truth, F, sA * sc, dev)
    np.savez(f, err=err.astype(np.float32), codes=model.derivative.codes.data.cpu().numpy(),
             adapt_loss=None if losses is None else losses.cpu().numpy())
    (out / f"{panel}_{tag}.json").write_text(json.dumps(dict(run=run, panel=panel, steps=0 if nominal else int(steps),
                                                             nominal=nominal, adapt_seconds_total=ta, n=n, i0=i0, i1=i1,
                                                             seconds_total=time.time() - t0), indent=1))
    print(panel, tag, "done", round(time.time() - t0), "s", flush=True)


def timing(run, steps, n_states=23):
    """Batch 1, one state at a time: states 3..22 of s2_test_Re50_D (states 0-2 warm-up); adaptation (steps) + a
    fixed-length forecast of F frames (no early stop); CUDA-synchronised wall clock."""
    dev = torch.device("cuda")
    M = meta()
    sc = 64.0 / M["sigma40"]
    tp = M["panels"]["s2_test_Re50_D"]
    sA, F = tp["sigma_A"], tp["F"]
    T = np.load(DATA / "s2_test_Re50_D.npy", mmap_mode="r")
    Y = np.load(DATA / "s2_test_Re50_D_obs.npy", mmap_mode="r")
    recs = []
    for i in range(int(n_states)):
        model, _ = load_trained(run, 1, dev)
        torch.cuda.synchronize()
        t0 = time.time()
        Yw = torch.as_tensor(np.asarray(Y[PRE + 1:PRE + W + 1, i:i + 1]).transpose(1, 0, 2, 3) * sc, dtype=torch.float32, device=dev)
        adapt_codes(model, Yw, steps, dev)
        torch.cuda.synchronize()
        t1 = time.time()
        y0 = torch.as_tensor(np.asarray(Y[PRE + W, i:i + 1]) * sc, dtype=torch.float32, device=dev)
        truth = np.asarray(T[PRE + W:PRE + W + F + 1, i:i + 1], dtype=np.float32) * sc
        forecast_errors(model, y0, truth, F, sA * sc, dev)
        torch.cuda.synchronize()
        t2 = time.time()
        recs.append(dict(state=i, warmup=i < 3, adapt=t1 - t0, forecast=t2 - t1, wall=t2 - t0, frames=F))
    timed = [r for r in recs if not r["warmup"]]
    res = dict(run=run, steps=int(steps), frames=F, n_timed=len(timed), wall_median=float(np.median([r["wall"] for r in timed])),
               wall_p90=float(np.quantile([r["wall"] for r in timed], 0.9)),
               adapt_median=float(np.median([r["adapt"] for r in timed])),
               forecast_median=float(np.median([r["forecast"] for r in timed])),
               forecast_fps=float(F * len(timed) / sum(r["forecast"] for r in timed)), states=recs,
               device=torch.cuda.get_device_name(0), torch=torch.__version__)
    (RUNS / run / f"timing_adapt{steps}.json").write_text(json.dumps(res, indent=1))
    print("timing", steps, res["wall_median"], flush=True)


def pilot(run, B, steps):
    """Batched adaptation throughput on TRAINING data (train_range windows), for choosing N before any test panel."""
    dev = torch.device("cuda")
    sc = 64.0 / meta()["sigma40"]
    X = np.load(DATA / ("train_range.npy" if (DATA / "train_range.npy").exists() else "train_range_wide.npy"), mmap_mode="r")
    B, steps = int(B), int(steps)
    Yw = torch.as_tensor(np.stack([X[i, 20:31] for i in range(B)]) * sc, dtype=torch.float32, device=dev)
    model, _ = load_trained(run, B, dev)
    adapt_codes(model, Yw, 2, dev)
    torch.cuda.synchronize()
    t0 = time.time()
    adapt_codes(model, Yw, steps, dev)
    torch.cuda.synchronize()
    dt = (time.time() - t0) / steps
    res = dict(run=run, B=B, steps=steps, seconds_per_step=dt, ms_per_state_step=1000 * dt / B,
               peak_mem_GB=torch.cuda.max_memory_allocated() / 1e9, device=torch.cuda.get_device_name(0))
    (RUNS / run / f"pilot_B{B}.json").write_text(json.dumps(res, indent=1))
    print(res, flush=True)


if __name__ == "__main__":
    torch.set_num_threads(8)
    c = sys.argv[1]
    if c == "train":
        a = sys.argv + [None] * 10
        train(a[2], a[3], a[4], a[5], a[6] or 50, a[7], a[8] == "stop_rule", a[9])
    elif c == "adapt":
        # adapt <run> <panel> <steps|0> <nominal|batched> <i0> <i1>
        adapt(sys.argv[2], sys.argv[3], int(sys.argv[4]), nominal=sys.argv[5] == "nominal", i0=sys.argv[6], i1=sys.argv[7])
    elif c == "pilot":
        pilot(sys.argv[2], sys.argv[3], sys.argv[4])
    elif c == "time":
        timing(sys.argv[2], int(sys.argv[3]), sys.argv[4] if len(sys.argv) > 4 else 23)
