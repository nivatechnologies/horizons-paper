"""Task 2.2: headline bound and references on lorenz28 (bits 4/6/8 x Delta 0.02/0.05/0.1), with the
particle-count sensitivity (3,000 particles at 4 and 8 bits, Delta = 0.05) and step-halving (dt = 0.005).

Labels
  bound      output-support bound d_C(x_j)/sigma_A on the true future (exact inequality evaluated on data)
  reference  decode-and-integrate, particle-filter history reference (true dynamics);
             persistence and climatology are reference (null)
  estimate   bootstrap intervals of population quantities

Usage
  t2_headline.py run  [--bits 4 6 8] [--deltas 0.02 0.05 0.1] [--dts 0.01 0.005] [--particles 1500]
                      [--n STATES] [--workers 48] [--out runs/headline] [--force]
  t2_headline.py sens [--workers 48]                  3,000-particle sensitivity (frozen bits/Delta)
  t2_headline.py summarize [--out runs/headline] [--res results/headline]
  t2_headline.py all                                  run + stop-condition reruns + sens + summarize

Each setting writes runs/headline/<setting>.npz; finished settings are skipped unless --force.
"""
import argparse
import csv
import json
import math
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np  # noqa: E402

from th import config, data, score  # noqa: E402
from th.pf import particle_filter  # noqa: E402
from th.systems import flow, get_system  # noqa: E402
from th.tokenize import kmeans_codebook, kmeans_labels  # noqa: E402

SYSTEM = "lorenz28"
FZ = config.freeze()
PF = FZ["references"]["particle_filter"]
EPS = [FZ["scoring"]["eps_primary"]] + FZ["scoring"]["eps_secondary"]
TAGS = ("future", "from_t0")
W = FZ["scoring"]["window_lyapunov_times"]
N_HIST = FZ["blocks"]["confirmation"]["history_panel_states"]
PF_CHUNK = 7          # states per worker job (300 states -> 43 jobs on <= 48 workers); part of the seed layout


def setting_name(bits, delta, dt, M):
    return f"{SYSTEM}_b{bits}_D{delta:g}_dt{dt:g}_M{M}"


def pf_seed(bits, delta, M, dt):
    """Deterministic particle-filter seed from (bits, Delta, M, dt)."""
    return int(7_000_000 + 100_000 * bits + 1_000 * int(round(delta * 100)) + 10 * (M // 1500)
               + int(round(dt * 1000)))


def cb_path(bits):
    return config.CACHE / f"kmeans_{SYSTEM}_{bits}.npz"


def integrate_frames(f, x0, F, sub, dt):
    out = np.empty((F + 1,) + x0.shape)
    out[0] = x0
    x = x0.copy()
    for j in range(1, F + 1):
        x = flow(f, x, sub, dt)
        out[j] = x
    return out


def scores_of(err, lam, delta):
    return score.horizon_all(err, lam, delta, W)


def put(store, prefix, hs):
    for k, v in hs.items():
        eps_tag = k  # "eps0.3_future"
        store[f"H_{prefix}_{eps_tag}"] = v["H"]
        store[f"crossed_{prefix}_{eps_tag}"] = v["crossed"]


def run_setting(bits, delta, dt, M, n, workers, out, force=False):
    name = setting_name(bits, delta, dt, M) + (f"_n{n}" if n else "")
    p = out / f"{name}.npz"
    if p.exists() and not force:
        print(f"skip {name} (exists)", flush=True)
        return p
    if not cb_path(bits).exists():
        raise RuntimeError(f"codebook cache missing for bits {bits}; not fitting here")
    t0 = time.time()
    sysm = get_system(SYSTEM)
    lam = config.lam(SYSTEM)
    sA = data.sigma_A(SYSTEM)
    cb = kmeans_codebook(SYSTEM, bits)
    calib, _ = data.calibration(SYSTEM)
    labels = kmeans_labels(SYSTEM, bits)
    pnl = data.panel(SYSTEM, "confirmation", dt=dt)
    if n:
        pnl = dict(pnl, traj=pnl["traj"][:n])
    F = data.n_future_frames(SYSTEM, delta)
    sub = int(round(delta / dt))
    hist, fut = data.frames(pnl, delta, n_after=F)          # fut (F+1, N, d)
    N = fut.shape[1]
    nh = min(N_HIST, N)
    x0 = fut[0]
    tok0 = cb.encode(x0)
    proto0 = cb.C[tok0]
    store = dict(bits=bits, delta=delta, dt=dt, particles=M, n_states=N, n_hist=nh, lam=lam, sigma_A=sA, W=W,
                 n_future_frames=F, sub=sub, panel_sha=pnl["sha"], x0=x0, tok0=tok0)

    # 1. output-support bound
    dC = cb.dist(fut) / sA                                   # (F+1, N)
    put(store, "bound", scores_of(dC, lam, delta))
    store["dC0"] = dC[0]
    # 3. decode-and-integrate
    di = integrate_frames(sysm.f, proto0, F, sub, dt)
    put(store, "DI", scores_of(score.err_rel(di, fut, sA), lam, delta))
    # 4. persistence and climatology
    put(store, "persistence", scores_of(score.err_rel(proto0[None], fut, sA), lam, delta))
    clim = calib.mean(0)
    put(store, "climatology", scores_of(score.err_rel(np.broadcast_to(clim, fut.shape), fut, sA), lam, delta))

    # 5. history reference on the first nh states
    L = int(round(PF["context_time"] / delta))
    hist_h = hist[-(L + 1):, :nh]
    toks = cb.encode(hist_h)                                 # (L+1, nh)
    assert np.array_equal(toks[-1], tok0[:nh])
    seed = pf_seed(bits, delta, M, dt)
    tp = time.time()
    mean, sd, fb, rate = particle_filter(SYSTEM, cb, calib, labels, toks, M, sub, seed, dt=dt,
                                         jitter=PF["jitter_fraction_of_spread"], n_workers=workers,
                                         chunk=PF_CHUNK)
    t_pf = time.time() - tp
    pf_traj = integrate_frames(sysm.f, mean, F, sub, dt)
    put(store, "PF", scores_of(score.err_rel(pf_traj, fut[:, :nh], sA), lam, delta))
    store.update(PF_mean0=mean, PF_sd0=sd, PF_err0=score.err_rel(mean, x0[:nh], sA), PF_fallback_events=fb,
                 PF_fallback_rate=rate, PF_steps=nh * L, PF_seed=seed, PF_chunk=PF_CHUNK, PF_context_frames=L,
                 PF_jitter=PF["jitter_fraction_of_spread"], PF_workers=workers, PF_seconds=t_pf,
                 labels_vs_encode_mismatch=float((labels != cb.encode(calib)).mean()),
                 git_sha=config.git_sha(), seconds=time.time() - t0)
    out.mkdir(parents=True, exist_ok=True)
    tmp = out / f"{name}.tmp.npz"
    np.savez(tmp, **store)
    tmp.replace(p)
    print(f"done {name}: pf {t_pf:.0f}s total {time.time()-t0:.0f}s fallback {fb}/{nh*L} = {rate:.4f} "
          f"H0.3 bound {store['H_bound_eps0.3_future'].mean():.3f} PF {store['H_PF_eps0.3_future'].mean():.3f} "
          f"DI {store['H_DI_eps0.3_future'].mean():.3f}", flush=True)
    return p


# ------------------------------------------------------------------------------------------ summary

def _ci(H):
    m, lo, hi = score.bootstrap_mean(H)
    return m, lo, hi


def summarize_setting(z, ref1500=None, dt01=None):
    """One row. z: loaded npz of this setting."""
    lim = PF["fallback_rate_limit"]
    nh = int(z["n_hist"])
    row = dict(system=SYSTEM, bits=int(z["bits"]), delta=float(z["delta"]), dt=float(z["dt"]),
               particles=int(z["particles"]), n_states=int(z["n_states"]), n_hist=nh,
               pf_seed=int(z["PF_seed"]), pf_context_frames=int(z["PF_context_frames"]),
               pf_fallback_events=int(z["PF_fallback_events"]), pf_steps=int(z["PF_steps"]),
               pf_fallback_rate=float(z["PF_fallback_rate"]),
               labels_vs_encode_mismatch=float(z["labels_vs_encode_mismatch"]), panel_sha=str(z["panel_sha"]))
    row["history_ref_label"] = "reference" if row["pf_fallback_rate"] <= lim else "unreliable"
    for eps in EPS:
        row[f"p0_eps{eps}"] = float((z["dC0"] > eps).mean())
        row[f"p0_eps{eps}_hist"] = float((z["dC0"][:nh] > eps).mean())
    for eps in EPS:
        for tag in TAGS:
            k = f"eps{eps}_{tag}"
            for q in ("bound", "DI", "persistence", "climatology", "PF"):
                H, c = z[f"H_{q}_{k}"], z[f"crossed_{q}_{k}"]
                sets = [("", slice(None))] if q == "PF" else [("", slice(None)), ("_hist", slice(0, nh))]
                for suf, sl in sets:
                    m, lo, hi = _ci(H[sl])
                    row[f"{q}_{k}{suf}_mean"] = m
                    row[f"{q}_{k}{suf}_ci95"] = [lo, hi]
                    row[f"{q}_{k}{suf}_nocross"] = float(1 - c[sl].mean())
            Hb, Hd, Hp = z[f"H_bound_{k}"], z[f"H_DI_{k}"], z[f"H_PF_{k}"]
            o = score.outlast(Hp, Hb[:nh])
            row[f"outlast_PF_vs_bound_{k}"], row[f"ties_PF_vs_bound_{k}"] = o["outlast"], o["ties"]
            o = score.outlast(Hd, Hb)
            row[f"outlast_DI_vs_bound_{k}"], row[f"ties_DI_vs_bound_{k}"] = o["outlast"], o["ties"]
            o = score.outlast(Hd[:nh], Hb[:nh])
            row[f"outlast_DI_vs_bound_{k}_hist"], row[f"ties_DI_vs_bound_{k}_hist"] = o["outlast"], o["ties"]
            for nm, a, b in (("PF_minus_bound", Hp, Hb[:nh]), ("PF_minus_DI", Hp, Hd[:nh]),
                             ("DI_minus_bound", Hd, Hb)):
                pdf = score.paired_diff(a, b)
                row[f"diff_{nm}_{k}"] = pdf["diff"]
                row[f"diff_{nm}_{k}_ci90"] = list(pdf["ci90"])
                row[f"diff_{nm}_{k}_ci95"] = list(pdf["ci95"])
    if ref1500 is not None:      # sensitivity: 3,000 minus 1,500 particles, paired on the same states
        for eps in EPS:
            for tag in TAGS:
                k = f"eps{eps}_{tag}"
                pdf = score.paired_diff(z[f"H_PF_{k}"], ref1500[f"H_PF_{k}"])
                row[f"sens_PF_M{row['particles']}_minus_M1500_{k}"] = pdf["diff"]
                row[f"sens_PF_M{row['particles']}_minus_M1500_{k}_ci95"] = list(pdf["ci95"])
    if dt01 is not None:         # step-halving: dt 0.005 minus dt 0.01, same burned-in starts
        for eps in EPS:
            for tag in TAGS:
                k = f"eps{eps}_{tag}"
                for q in ("bound", "DI", "persistence", "climatology", "PF"):
                    pdf = score.paired_diff(z[f"H_{q}_{k}"], dt01[f"H_{q}_{k}"])
                    row[f"halving_{q}_minus_dt0.01_{k}"] = pdf["diff"]
                    row[f"halving_{q}_minus_dt0.01_{k}_ci95"] = list(pdf["ci95"])
    return row


def summarize(out, res):
    files = sorted(p for p in out.glob(f"{SYSTEM}_b*_M*.npz") if "_n" not in p.stem.split("_M")[-1]
                   and not p.stem.endswith(".tmp"))
    Z = {p.stem: dict(np.load(p)) for p in files}
    rows = []
    for name, z in Z.items():
        b, d, dt, M = int(z["bits"]), float(z["delta"]), float(z["dt"]), int(z["particles"])
        r1500 = Z.get(setting_name(b, d, dt, 1500)) if M != 1500 else None
        d01 = Z.get(setting_name(b, d, 0.01, M)) if dt != 0.01 else None
        rows.append(summarize_setting(z, r1500, d01))
    rows.sort(key=lambda r: (r["dt"] != 0.01, r["bits"], r["delta"], r["particles"]))
    # stop condition: a 1,500-particle setting above the limit is labelled by its 3,000-particle rerun
    lim = PF["fallback_rate_limit"]
    for r in rows:
        r["stop_condition"] = ""
        if r["particles"] == 1500 and r["pf_fallback_rate"] > lim:
            r3 = [q for q in rows if q["particles"] == 3000 and (q["bits"], q["delta"], q["dt"]) ==
                  (r["bits"], r["delta"], r["dt"])]
            if not r3:
                r["stop_condition"] = "fallback > 5%: 3,000-particle rerun pending"
            elif r3[0]["pf_fallback_rate"] > lim:
                r["stop_condition"] = "fallback > 5% at 1,500 and 3,000 particles: history reference unreliable"
                r["history_ref_label"] = r3[0]["history_ref_label"] = "unreliable"
            else:
                r["stop_condition"] = "fallback > 5% at 1,500: use the 3,000-particle row"
    sha = config.git_sha()
    for r in rows:
        r["git_sha"] = sha
    res.mkdir(parents=True, exist_ok=True)
    meta = dict(task="2.2 headline bound and references", system=SYSTEM, git_sha=sha,
                labels=dict(bound="bound", DI="reference", PF="reference (history; see history_ref_label)",
                            persistence="reference (null)", climatology="reference (null)",
                            ci="estimate", diff="estimate", outlast="estimate", p0="estimate"),
                window_lyapunov_times=W, eps=EPS, bootstrap=dict(reps=FZ["seeds"]["bootstrap_reps"],
                                                                 seed=FZ["seeds"]["bootstrap_seed"]),
                pf_chunk=PF_CHUNK, rows=rows)
    (res / "headline.json").write_text(json.dumps(meta, indent=1))
    keys = []
    for r in rows:
        for k in r:
            if k not in keys:
                keys.append(k)
    with open(res / "headline.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(keys)
        for r in rows:
            w.writerow([json.dumps(r[k]) if isinstance(r.get(k), list) else r.get(k, "") for k in keys])
    print(f"wrote {res/'headline.json'} and headline.csv ({len(rows)} rows)", flush=True)
    return rows


# ------------------------------------------------------------------------------------------ main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run", "sens", "summarize", "all"])
    ap.add_argument("--bits", type=int, nargs="+", default=[4, 6, 8])
    ap.add_argument("--deltas", type=float, nargs="+", default=FZ["scoring"]["frame_intervals"])
    ap.add_argument("--dts", type=float, nargs="+", default=[FZ["integration"]["dt"], FZ["integration"]["dt_half"]])
    ap.add_argument("--particles", type=int, default=PF["particles"])
    ap.add_argument("--n", type=int, default=None, help="test on the first n states (separate file)")
    ap.add_argument("--workers", type=int, default=48)
    ap.add_argument("--out", default=str(config.RUNS / "headline"))
    ap.add_argument("--res", default=str(config.RESULTS / "headline"))
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--system", default="lorenz28", help="subset systems (Task 4) reuse this script")
    a = ap.parse_args()
    global SYSTEM
    SYSTEM = a.system
    out, res = Path(a.out), Path(a.res)
    t0 = time.time()
    if a.cmd in ("run", "all"):
        for dt in a.dts:
            for b in a.bits:
                for d in a.deltas:
                    p = run_setting(b, d, dt, a.particles, a.n, a.workers, out, a.force)
                    # stop condition: fallback > 5% -> rerun with 3,000 particles
                    if a.particles == PF["particles"] and float(np.load(p)["PF_fallback_rate"]) > \
                            PF["fallback_rate_limit"]:
                        print(f"stop condition at b{b} D{d} dt{dt}: rerun with 3000 particles", flush=True)
                        run_setting(b, d, dt, PF["sensitivity"]["particles"], a.n, a.workers, out, a.force)
    if a.cmd in ("sens", "all"):
        s = PF["sensitivity"]
        for b in s["bits"]:
            run_setting(b, s["delta"], FZ["integration"]["dt"], s["particles"], a.n, a.workers, out, a.force)
    if a.cmd in ("summarize", "all") and not a.n:
        summarize(out, res)
    print(f"wall {time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
