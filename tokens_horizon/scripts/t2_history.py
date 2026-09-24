"""Task 2.6: history sweep of the particle-filter reference, with timing-jitter and observation-noise variants.

System lorenz28, bits {4, 6}, integration dt = 0.005 throughout (freeze pins: delta_035, history_sweep).
Truth: the dt = 0.005 confirmation panel, first 300 states. Particle propagation, jitter substeps and forecast
integration all use dt = 0.005.

Variants
  clean   tokens of the true states on the frame grid; all Delta x all context times.
  jitter  (tau = 3.2) observation k is the true state at t_k + u_k, u_k ~ U(-Delta/4, Delta/4) i.i.d., reached from the
          panel grid state at or before t_k + u_k by one RK4 substep of the remainder; the filter assumes t_k.
  noise   (tau = 3.2) N(0, (0.02 sigma_A)^2) per coordinate added to each observed state before tokenization.
In every variant the forecast is scored against the true, unperturbed future (target at t = 0 is the true state).

Labels: 'reference' (particle-filter history reference; decode-and-integrate), 'bound' (output-support bound),
'estimate' (population quantity with interval, e.g. paired differences). A reference whose fallback rate stays
above the frozen limit at 3,000 particles is labelled 'reference (unreliable)'.

Usage
  python scripts/t2_history.py                       # full sweep (skip-if-done per setting), then aggregate
  python scripts/t2_history.py --taus 0 0.8 3.2 6.4  # subset
  python scripts/t2_history.py --states 20 --outdir <scratch> --no-aggregate   # timing subset
  python scripts/t2_history.py --aggregate-only
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from th import config, data, score  # noqa: E402
from th.pf import particle_filter  # noqa: E402
from th.systems import flow, get_system, rk4  # noqa: E402
from th.tokenize import kmeans_codebook, kmeans_labels  # noqa: E402

SYSTEM = "lorenz28"
FZ = config.freeze()
PIN = FZ["pins"]["history_sweep"]
DT_H = float(PIN["dt"])                                   # 0.005
DELTAS = [float(x) for x in PIN["deltas"]]
TAUS = [float(x) for x in PIN["context_times"]]
RATES = [int(x) for x in PIN["rates"]]
N_STATES = int(PIN["states"])
M0 = int(PIN["particles"])
TAU_SENS = float(FZ["pins"]["sensitivity_context"])      # 3.2
PFZ = FZ["references"]["particle_filter"]
FB_LIMIT = float(PFZ["fallback_rate_limit"])
M_RERUN = int(PFZ["sensitivity"]["particles"])            # 3000
NOISE_REL = 0.02
CHUNK = 7                                                 # 300 states -> 43 filter jobs (<= 48 workers)
W = float(FZ["scoring"]["window_lyapunov_times"])
LAM = config.lam(SYSTEM)
SC = FZ["scoring"]
SCORE_KEYS = [f"eps{e}_{t}" for e in [SC["eps_primary"]] + SC["eps_secondary"] for t in ("future", "from_t0")]
PRIMARY = f"eps{SC['eps_primary']}_future"

RUNS = config.RUNS / "history"
RES = config.RESULTS / "history"


def derived_seed(*parts) -> int:
    h = hashlib.sha256("|".join(["t2_history"] + [str(p) for p in parts]).encode()).digest()
    return int.from_bytes(h[:8], "little") % (2 ** 63)


def fmt(x):
    return f"{x:g}"


def tag(variant, bits, delta, tau, M):
    return f"{variant}_b{bits}_D{fmt(delta)}_tau{fmt(tau)}_M{M}"


def integrate_frames(x0, sub, n_frames):
    f = get_system(SYSTEM).f
    out = np.empty((n_frames + 1,) + x0.shape)
    out[0] = x0
    x = x0.copy()
    for j in range(1, n_frames + 1):
        x = flow(f, x, sub, DT_H)
        out[j] = x
    return out


def horizons(pred, fut, delta, sA):
    err = score.err_rel(pred, fut, sA)
    return score.horizon_all(err, LAM, delta, W)


def sub_of(delta):
    s = delta / DT_H
    assert abs(s - round(s)) < 1e-9, delta
    return int(round(s))


class Ctx:
    def __init__(self, n_states):
        self.pnl = data.panel(SYSTEM, "confirmation", n=n_states, dt=DT_H)
        assert abs(self.pnl["dt"] - DT_H) < 1e-15
        self.traj, self.pre = self.pnl["traj"], self.pnl["pre"]
        self.n = self.traj.shape[0]
        self.sA = data.sigma_A(SYSTEM)
        self.calib, _ = data.calibration(SYSTEM)
        self.cbs = {b: kmeans_codebook(SYSTEM, b) for b in RATES}   # cache only (files exist)
        self.labels = {b: kmeans_labels(SYSTEM, b) for b in RATES}

    def frames(self, delta, L):
        F = data.n_future_frames(SYSTEM, delta)
        hist, fut = data.frames(self.pnl, delta, n_before=L, n_after=F)
        return hist, fut

    def observations(self, variant, delta, L, hist, draw_seed):
        """Observed states (L+1, n, d) for the variant, first context frame to t = 0."""
        if variant == "clean":
            return hist.copy(), {}
        rng = np.random.default_rng(draw_seed)
        if variant == "noise":
            eta = NOISE_REL * self.sA * rng.standard_normal(hist.shape)
            return hist + eta, dict(noise_sd_abs=NOISE_REL * self.sA,
                                    noise_rms_rel=float(np.sqrt((eta ** 2).sum(-1).mean()) / self.sA))
        if variant == "jitter":
            sub = sub_of(delta)
            idx = self.pre - (L - np.arange(L + 1)) * sub                     # grid index of t_k
            u = rng.uniform(-delta / 4, delta / 4, size=(L + 1, self.n))       # u_k per frame and state
            off = u / DT_H
            fl = np.floor(off)
            g = idx[:, None] + fl.astype(int)                                  # grid state at or before t_k + u_k
            rem = (off - fl) * DT_H                                            # remainder in [0, dt)
            assert g.min() >= 0 and g.max() < self.traj.shape[1]
            base = self.traj[np.arange(self.n)[None, :], g]                    # (L+1, n, d)
            obs = rk4(get_system(SYSTEM).f, base, rem[..., None])
            return obs, dict(u_abs_mean=float(np.abs(u).mean()),
                             obs_shift_rms_rel=float(np.sqrt(((obs - hist) ** 2).sum(-1).mean()) / self.sA))
        raise ValueError(variant)


def run_setting(ctx: Ctx, variant, bits, delta, tau, M, outdir: Path, workers):
    p = outdir / f"{tag(variant, bits, delta, tau, M)}.npz"
    if p.exists():
        z = np.load(p)
        print(f"skip {p.name} (fallback {float(z['fallback_rate']):.4f})", flush=True)
        return float(z["fallback_rate"])
    t0 = time.time()
    L = int(round(tau / delta))
    sub = sub_of(delta)
    hist, fut = ctx.frames(delta, L)
    F = fut.shape[0] - 1
    pf_seed = derived_seed("pf", SYSTEM, fmt(delta), fmt(tau), bits, variant, M)
    draw_seed = derived_seed("draw", SYSTEM, fmt(delta), fmt(tau), variant)   # same physical draws at every rate
    obs, obs_info = ctx.observations(variant, delta, L, hist, draw_seed)
    cb = ctx.cbs[bits]
    toks = cb.encode(obs)                                                        # (L+1, n)
    est, sd, fb, fb_rate = particle_filter(SYSTEM, cb, ctx.calib, ctx.labels[bits], toks, M, sub, pf_seed,
                                           dt=DT_H, n_workers=workers, chunk=CHUNK)
    t_pf = time.time() - t0
    pred = integrate_frames(est, sub, F)
    hz = horizons(pred, fut, delta, ctx.sA)
    x0 = fut[0]
    e0 = np.linalg.norm(est - x0, axis=-1) / ctx.sA
    arrays = dict(est=est, post_sd=sd, x0=x0, tokens=toks, err0_rel=e0,
                  tok_mismatch=(toks != cb.encode(hist)).astype(np.int8),
                  fallback_events=fb, fallback_rate=fb_rate, L=L, sub=sub, F=F, M=M, bits=bits, delta=delta, tau=tau,
                  pf_seed=np.uint64(pf_seed), draw_seed=np.uint64(draw_seed), chunk=CHUNK, dt=DT_H,
                  panel_sha=ctx.pnl["sha"], variant=variant, wall_pf=t_pf, wall_total=time.time() - t0,
                  obs_info=json.dumps(obs_info))
    for k, v in hz.items():
        arrays[f"H_{k}"] = v["H"]
        arrays[f"crossed_{k}"] = v["crossed"]
    np.savez(p, **arrays)
    print(f"done {p.name}: L={L} fallback={fb_rate:.4f} err0={np.sqrt((e0**2).mean()):.4f} "
          f"H={hz[PRIMARY]['H'].mean():.3f} pf {t_pf:.0f}s total {time.time()-t0:.0f}s", flush=True)
    return fb_rate


def run_refs(ctx: Ctx, bits, delta, outdir: Path):
    p = outdir / f"refs_b{bits}_D{fmt(delta)}.npz"
    if p.exists():
        return
    sub = sub_of(delta)
    _, fut = ctx.frames(delta, 0)
    F = fut.shape[0] - 1
    cb = ctx.cbs[bits]
    arrays = dict(bits=bits, delta=delta, sub=sub, F=F, panel_sha=ctx.pnl["sha"])
    b = score.horizon_all(cb.dist(fut) / ctx.sA, LAM, delta, W)          # output-support bound
    x0hat = cb.quantize(fut[0])
    d = horizons(integrate_frames(x0hat, sub, F), fut, delta, ctx.sA)    # decode-and-integrate
    for k in SCORE_KEYS:
        arrays[f"bound_H_{k}"] = b[k]["H"]
        arrays[f"bound_crossed_{k}"] = b[k]["crossed"]
        arrays[f"decode_H_{k}"] = d[k]["H"]
        arrays[f"decode_crossed_{k}"] = d[k]["crossed"]
    arrays["decode_err0_rel"] = np.linalg.norm(x0hat - fut[0], axis=-1) / ctx.sA
    np.savez(p, **arrays)
    print(f"refs {p.name}: bound {b[PRIMARY]['H'].mean():.3f} decode {d[PRIMARY]['H'].mean():.3f}", flush=True)


def settings(args):
    out = []
    for bits in args.bits:
        for delta in args.deltas:
            for variant in args.variants:
                taus = args.taus if variant == "clean" else [t for t in args.taus if abs(t - TAU_SENS) < 1e-12]
                for tau in taus:
                    out.append((variant, bits, delta, tau))
    # heaviest (small Delta, long tau) first so timing is visible early
    out.sort(key=lambda s: -(s[3] / s[2]) * (1 if s[3] > 0 else 0))
    return out


# ------------------------------------------------------------------------------------------ aggregation
def rms_ci(e0, reps, seed):
    rng = np.random.default_rng(seed)
    n = len(e0)
    st = np.array([np.sqrt((e0[rng.integers(0, n, n)] ** 2).mean()) for _ in range(reps)])
    return float(np.sqrt((e0 ** 2).mean())), float(np.quantile(st, 0.025)), float(np.quantile(st, 0.975))


def aggregate(outdir: Path, resdir: Path):
    resdir.mkdir(parents=True, exist_ok=True)
    sha = config.git_sha()
    reps = FZ["seeds"]["bootstrap_reps"]
    bseed = FZ["seeds"]["bootstrap_seed"]
    files = sorted(outdir.glob("*_M*.npz"))
    runs = {}
    for f in files:
        z = np.load(f)
        key = (str(z["variant"]), int(z["bits"]), float(z["delta"]), float(z["tau"]), int(z["M"]))
        runs[key] = z
    # reliability per (variant, bits, delta, tau): >limit at M0 -> look at M_RERUN
    status = {}
    for (v, b, d, t, M), z in runs.items():
        status.setdefault((v, b, d, t), {})[M] = float(z["fallback_rate"])
    rows = []

    def score_cols(prefix_H, prefix_c, z):
        c = {}
        for k in SCORE_KEYS:
            H = z[f"{prefix_H}{k}"]
            m, lo, hi = score.bootstrap_mean(H)
            c[f"{k}_mean"] = m
            c[f"{k}_lo95"] = lo
            c[f"{k}_hi95"] = hi
            c[f"{k}_no_cross"] = float(1 - z[f"{prefix_c}{k}"].mean())
        return c

    for (v, b, d, t, M), z in sorted(runs.items()):
        fbs = status[(v, b, d, t)]
        unreliable = all(r > FB_LIMIT for r in fbs.values()) and (M_RERUN in fbs)
        needs_rerun = fbs.get(M0, 0.0) > FB_LIMIT and M_RERUN not in fbs
        label = "reference (unreliable)" if unreliable else "reference"
        e = rms_ci(z["err0_rel"], reps, bseed)
        row = dict(label=label, method="particle_filter", variant=v, bits=b, delta=d, tau=t, L=int(z["L"]),
                   particles=M, n_states=len(z["err0_rel"]), fallback_rate=float(z["fallback_rate"]),
                   fallback_events=int(z["fallback_events"]), rerun_pending=needs_rerun,
                   canonical=(M == max(fbs)), err0_rms_rel=e[0], err0_lo95=e[1], err0_hi95=e[2],
                   err0_median_rel=float(np.median(z["err0_rel"])),
                   frac_err0_gt_0p3=float((z["err0_rel"] > 0.3).mean()),
                   token_mismatch_frac=float(z["tok_mismatch"].mean()),
                   pf_seed=int(z["pf_seed"]), draw_seed=int(z["draw_seed"]) if v != "clean" else None,
                   chunk=int(z["chunk"]), dt=float(z["dt"]), panel_sha=str(z["panel_sha"]),
                   wall_s=float(z["wall_total"]), obs_info=json.loads(str(z["obs_info"])), sha=sha)
        row.update(score_cols("H_", "crossed_", z))
        rows.append(row)
    for f in sorted(outdir.glob("refs_b*_D*.npz")):
        z = np.load(f)
        b, d = int(z["bits"]), float(z["delta"])
        for meth, lab in (("bound", "bound"), ("decode", "reference")):
            row = dict(label=lab, method="output_support_bound" if meth == "bound" else "decode_and_integrate",
                       variant="clean", bits=b, delta=d, tau=None, L=None, particles=None,
                       n_states=len(z[f"{meth}_H_{PRIMARY}"]), fallback_rate=None, sha=sha,
                       panel_sha=str(z["panel_sha"]), dt=DT_H)
            if meth == "decode":
                e = rms_ci(z["decode_err0_rel"], reps, bseed)
                row.update(err0_rms_rel=e[0], err0_lo95=e[1], err0_hi95=e[2])
            row.update(score_cols(f"{meth}_H_", f"{meth}_crossed_", z))
            rows.append(row)
    # paired differences (perturbed - clean) on the same states, same particle count, primary score
    paired = []
    for (v, b, d, t, M), z in sorted(runs.items()):
        if v == "clean":
            continue
        zc = runs.get(("clean", b, d, t, M)) or runs.get(("clean", b, d, t, M0))
        if zc is None:
            continue
        pdiff = score.paired_diff(z[f"H_{PRIMARY}"], zc[f"H_{PRIMARY}"])
        paired.append(dict(label="estimate", quantity=f"{v} minus clean, restricted mean, {PRIMARY}", variant=v,
                           bits=b, delta=d, tau=t, particles=M, clean_particles=int(zc["M"]),
                           perturbed_label=("reference (unreliable)" if all(r > FB_LIMIT for r in status[(v, b, d, t)].values())
                                            and M_RERUN in status[(v, b, d, t)] else "reference"), diff=pdiff["diff"], ci95=pdiff["ci95"],
                           ci90=pdiff["ci90"], sha=sha))
    meta = dict(system=SYSTEM, lam=LAM, W=W, dt=DT_H, primary=PRIMARY, fallback_limit=FB_LIMIT,
                bootstrap=dict(reps=reps, seed=bseed, ci=0.95), sha=sha,
                seeds="pf seed = sha256('t2_history|pf|lorenz28|Delta|tau|bits|variant|M')[:8] mod 2^63; "
                      "draw seed = sha256('t2_history|draw|lorenz28|Delta|tau|variant')[:8] mod 2^63 "
                      "(one physical perturbation realisation shared by both rates)")
    json.dump(dict(meta=meta, rows=rows, paired_vs_clean=paired), open(resdir / "history.json", "w"), indent=1)
    cols = []
    for r in rows:
        for k in r:
            if k not in cols and k != "obs_info":
                cols.append(k)
    with open(resdir / "history.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"aggregated {len(rows)} rows, {len(paired)} paired differences -> {resdir}", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bits", type=int, nargs="+", default=RATES)
    ap.add_argument("--deltas", type=float, nargs="+", default=DELTAS)
    ap.add_argument("--taus", type=float, nargs="+", default=TAUS)
    ap.add_argument("--variants", nargs="+", default=["clean", "jitter", "noise"])
    ap.add_argument("--states", type=int, default=N_STATES)
    ap.add_argument("--particles", type=int, default=M0)
    ap.add_argument("--workers", type=int, default=48)
    ap.add_argument("--outdir", default=str(RUNS))
    ap.add_argument("--resdir", default=str(RES))
    ap.add_argument("--no-rerun", action="store_true", help="do not rerun >5%% fallback settings with 3,000")
    ap.add_argument("--no-aggregate", action="store_true")
    ap.add_argument("--aggregate-only", action="store_true")
    args = ap.parse_args()
    assert args.workers <= 48
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    if not args.aggregate_only:
        T0 = time.time()
        ctx = Ctx(args.states)
        print(f"panel sha {ctx.pnl['sha']} n={ctx.n} sigma_A={ctx.sA:.5f} lam={LAM} W={W}", flush=True)
        for bits in args.bits:
            for delta in args.deltas:
                run_refs(ctx, bits, delta, outdir)
        for (v, b, d, t) in settings(args):
            fr = run_setting(ctx, v, b, d, t, args.particles, outdir, args.workers)
            if fr > FB_LIMIT and args.particles == M0 and not args.no_rerun:
                print(f"  fallback {fr:.4f} > {FB_LIMIT}: rerun with {M_RERUN}", flush=True)
                run_setting(ctx, v, b, d, t, M_RERUN, outdir, args.workers)
        print(f"sweep wall {time.time() - T0:.0f}s", flush=True)
    if not args.no_aggregate:
        aggregate(outdir, Path(args.resdir))


if __name__ == "__main__":
    main()
