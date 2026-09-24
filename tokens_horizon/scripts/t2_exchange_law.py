"""Task 2.4: exchange law H_W(R) = h(delta_hat(R)), per-rate criterion, second-author comparator, r by orientation, FSLE.

Stages (each skip-if-done, per-state arrays in runs/exchange_law/):
  h_<sys>_<orient>.npz   H_W (15 deltas x 1,000 calibration states) for orientation fresh | aligned | isotropic
                         | aligned_endpoint  (Delta = 0.02, future frames, eps = 0.3, W = 27)
  di_<sys>_R<R>.npz      decode-and-integrate reference with the rate-R k-means codebook, 1,000-state
                         confirmation panel (R = 4..12, all six systems; the non-exchange systems feed Task 2.5)
  fsle_<sys>.npz         first-passage times through doubling levels from 1e-9 sigma_A (codebook direction)

Orientations (same 1,000 calibration states, same deltas):
  fresh      unit (c(x) - x) of the 10-bit codebook at x (this is the h curve)
  aligned    a random unit tangent vector evolved (RK4 tangent, renormalised every 10 steps) for 10 tu along the
             stored calibration trajectory that ENDS at x; the start is the calibration state 1,000 steps earlier
             (stored sample, or regenerated from the frozen Gaussian start through the burn-in); random sign
  isotropic  random unit vector
  aligned_endpoint  (supplementary) x integrated 10 tu forward with a random tangent vector; the endpoint state and
             its evolved tangent are used (different states from the other three)
Labels: h, predictions, r, FSLE, comparator = estimate; decode-and-integrate horizons = reference.
"""
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("TH_KDTREE_WORKERS", "1")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np  # noqa: E402

from th import config, data, score  # noqa: E402
from th import exchange as ex  # noqa: E402
from th.tokenize import kmeans_codebook  # noqa: E402

ALL_SYSTEMS = ["lorenz28", "lorenz45", "l96_5", "l96_6", "l96_10", "l96_20"]
FZ = config.freeze()
EL = FZ["exchange_law"]
SYSTEMS = EL["systems"]
RATES = list(range(4, 13))
ORIENTS = ["fresh", "aligned", "isotropic", "aligned_endpoint"]
RUNS = config.RUNS / "exchange_law"
OUT = config.RESULTS / "exchange_law"
DELTA = 0.02
N_WORKERS = int(os.environ.get("T2_WORKERS", "20"))


def rel_deltas():
    g = EL["delta_grid"]
    return np.logspace(g["log10_start"], g["log10_stop"], g["n"])


def codebook(system, bits):
    p = config.CACHE / f"kmeans_{system}_{bits}.npz"
    while not p.exists():          # never fit k-means here; wait for the cache process
        print(f"waiting for {p.name}", flush=True)
        time.sleep(60)
    return kmeans_codebook(system, bits)


def directions(system, orient):
    idx, X, _ = ex.h_states(system)
    sA = data.sigma_A(system)
    info = {}
    if orient == "fresh":
        q, _ = ex.nearest(codebook(system, EL["calibration_codebook_bits"]), X)
        U = q - X
        U /= np.linalg.norm(U, axis=1, keepdims=True)
        return X, U, info
    if orient == "isotropic":
        rng = np.random.default_rng(config.seed("calibration", system, 8))
        U = rng.standard_normal(X.shape)
        U /= np.linalg.norm(U, axis=1, keepdims=True)
        return X, U, info
    steps = int(round(EL["aligned_tangent_time"] / data.DT))
    if orient == "aligned":
        rng = np.random.default_rng(config.seed("calibration", system, 9))
        X0 = ex.state_back_in_time(system, idx, steps)
        Xe, U = ex.evolve_tangent(system, X0, steps, rng)
        dev = np.linalg.norm(Xe - X, axis=1) / sA
        info = dict(endpoint_dev_max_rel=float(dev.max()), endpoint_dev_median_rel=float(np.median(dev)))
        U *= rng.choice([-1.0, 1.0], size=(len(U), 1))
        return X, U, info
    if orient == "aligned_endpoint":
        rng = np.random.default_rng(config.seed("calibration", system, 10))
        Xe, U = ex.evolve_tangent(system, X, steps, rng)
        U *= rng.choice([-1.0, 1.0], size=(len(U), 1))
        return Xe, U, info
    raise ValueError(orient)


def job_h(system, orient):
    p = RUNS / f"h_{system}_{orient}.npz"
    if p.exists():
        return p.name, "skip"
    t0 = time.time()
    sA = data.sigma_A(system)
    X, U, info = directions(system, orient)
    dl = rel_deltas()
    H, c = ex.perturbation_horizons(system, X, U, dl, sA, DELTA)
    np.savez(p, H=H, crossed=c, rel_deltas=dl, X=X, U=U, info=json.dumps(info), sha=config.git_sha())
    return p.name, f"{time.time() - t0:.0f}s {info}"


def job_di(system, R):
    p = RUNS / f"di_{system}_R{R}.npz"
    if p.exists():
        return p.name, "skip"
    t0 = time.time()
    cb = codebook(system, R)
    H, c, e0, psha = ex.decode_integrate(system, lambda X: ex.nearest(cb, X)[0], DELTA)
    np.savez(p, H=H, crossed=c, err0_rel=e0, panel_sha=psha, sha=config.git_sha())
    return p.name, f"{time.time() - t0:.0f}s meanH={H.mean():.3f}"


def job_fsle(system):
    p = RUNS / f"fsle_{system}.npz"
    if p.exists():
        return p.name, "skip"
    t0 = time.time()
    sA = data.sigma_A(system)
    X, U, _ = directions(system, "fresh")
    levels, first = ex.fsle(system, X, U, sA, start_rel=1e-9, top_rel=1.0)
    np.savez(p, levels=levels, first=first, sha=config.git_sha())
    return p.name, f"{time.time() - t0:.0f}s"


def run_job(j):
    kind, *a = j
    return {"h": job_h, "di": job_di, "fsle": job_fsle}[kind](*a)


# ------------------------------------------------------------------------------------------------ analysis
def boot_idx(n, reps, rng):
    return rng.integers(0, n, (reps, n))


def interp_h(dl, Hmean, target):
    """Linear interpolation of H_W in ln delta. Returns nan outside the calibrated range (no extrapolation)."""
    x = np.log(dl[::-1])
    y = Hmean[::-1]
    t = np.log(target)
    out = np.interp(t, x, y)
    return np.where((t < x[0] - 1e-12) | (t > x[-1] + 1e-12), np.nan, out)


def criterion(pred, meas):
    c = EL["criterion"]
    tol = c["relative"] * meas if meas >= c["split_at"] else c["absolute_below_half"]
    return tol, abs(pred - meas) <= tol


def analyse(system, lyap_dky):
    reps = FZ["seeds"]["bootstrap_reps"]
    sA = data.sigma_A(system)
    lam = config.lam(system)
    dist = np.load(RUNS / f"distortion_{system}.npz")
    drates = list(dist["rates"])
    delta_hat = {int(R): float(np.sqrt(dist["sq_by_traj"][drates.index(R)].sum() / dist["count"].sum()) / sA)
                 for R in RATES}
    h = {o: np.load(RUNS / f"h_{system}_{o}.npz") for o in ORIENTS}
    dl = h["fresh"]["rel_deltas"]
    x = np.log(1 / dl)
    res = dict(system=system, lam=lam, sigma_A=sA, d_ky=lyap_dky, rel_deltas=dl.tolist(), delta_hat=delta_hat)
    # ---- h curve and saturation
    orient_out = {}
    for o in ORIENTS:
        H, c = h[o]["H"], h[o]["crossed"]
        Hm = H.mean(1)
        rng = np.random.default_rng(FZ["seeds"]["bootstrap_seed"])
        bi = boot_idx(H.shape[1], reps, rng)
        Hb = np.stack([H[:, b].mean(1) for b in bi])                     # (reps, 15)
        slope_cd = np.gradient(Hm, x)
        slope_cd_b = np.gradient(Hb, x, axis=1)
        ls = np.polyfit(x, Hm, 1)[0]
        ls_b = np.polyfit(x, Hb.T, 1)[0]
        orient_out[o] = dict(
            H_mean=Hm.tolist(), H_ci95=np.quantile(Hb, [0.025, 0.975], axis=0).T.tolist(),
            frac_no_cross=(1 - c.mean(1)).tolist(),
            r_central=(1 / slope_cd).tolist(),
            r_central_ci95=np.quantile(1 / slope_cd_b, [0.025, 0.975], axis=0).T.tolist(),
            r_ls=float(1 / ls), r_ls_ci95=np.quantile(1 / ls_b, [0.025, 0.975]).tolist(),
            info=json.loads(str(h[o]["info"])), label="estimate")
        if o == "fresh":
            Hb_fresh = Hb
    res["orientations"] = orient_out
    nc = np.array(orient_out["fresh"]["frac_no_cross"])
    in_range = (dl >= 1e-4 - 1e-15) & (dl <= 0.3)
    res["saturation"] = dict(max_frac_no_cross_in_range=float(nc[in_range].max()),
                             limit=EL["saturation_limit"], range_over_sigma_A=[1e-4, 0.3],
                             stop_condition_triggered=bool(nc[in_range].max() > EL["saturation_limit"]))
    # ---- predictions vs measured
    Hm = np.array(orient_out["fresh"]["H_mean"])
    rows = []
    meas = {}
    for R in RATES:
        z = np.load(RUNS / f"di_{system}_R{R}.npz")
        m, lo, hi = score.bootstrap_mean(z["H"])
        meas[R] = dict(mean=m, ci95=[lo, hi], frac_no_cross=float(1 - z["crossed"].mean()),
                       err0_rms_rel=float(np.sqrt((z["err0_rel"] ** 2).mean())))
    # second-author comparator: slope ln2/D_KY per bit, intercept by least squares on the fit rates
    b = np.log(2) / lyap_dky
    fit = EL["deff_fit_rates"]
    a = float(np.mean([meas[R]["mean"] - b * R for R in fit]))
    all_met = True
    for R in RATES:
        role = "heldout" if R in EL["heldout_rates"] else ("fit" if R in fit else "other")
        pred = float(interp_h(dl, Hm, delta_hat[R]))
        if np.isfinite(pred):
            pb = np.array([np.interp(np.log(delta_hat[R]), np.log(dl[::-1]), hb[::-1]) for hb in Hb_fresh])
            pci = np.quantile(pb, [0.025, 0.975]).tolist()
        else:
            pci = [None, None]
        mm = meas[R]["mean"]
        sa_pred = a + b * R
        row = dict(system=system, rate_bits=R, role=role, delta_hat_over_sigma_A=delta_hat[R],
                   pred=pred if np.isfinite(pred) else None, pred_ci95_lo=pci[0], pred_ci95_hi=pci[1],
                   pred_label="estimate", meas=mm, meas_ci95_lo=meas[R]["ci95"][0], meas_ci95_hi=meas[R]["ci95"][1],
                   meas_frac_no_cross=meas[R]["frac_no_cross"], meas_label="reference",
                   err=(pred - mm) if np.isfinite(pred) else None, tol=None, outcome=None,
                   second_author_pred=sa_pred, second_author_err=sa_pred - mm, second_author_label="estimate")
        tol, ok = criterion(pred, mm) if np.isfinite(pred) else (criterion(0.0, mm)[0], False)
        row["tol"] = tol
        if np.isfinite(pred):
            row["outcome"] = "criterion met" if ok else "criterion not met"
        else:
            row["outcome"] = "criterion not met (no prediction: delta_hat outside the frozen h range)"
        if role == "heldout":
            all_met &= bool(np.isfinite(pred) and ok)
        rows.append(row)
    res["rates"] = rows
    res["all_heldout_criterion_met"] = bool(all_met)
    res["second_author"] = dict(intercept=a, slope_per_bit=b, d_ky=lyap_dky, label="estimate",
                                note="fixed-slope comparator (pins.second_author_law), beside the WO criterion")
    # ---- FSLE
    fz = np.load(RUNS / f"fsle_{system}.npz")
    levels, first = fz["levels"], fz["first"]
    tau = np.diff(first, axis=0)
    rng = np.random.default_rng(FZ["seeds"]["bootstrap_seed"])
    fsle_rows = []
    for i in range(len(tau)):
        ok = np.isfinite(tau[i])
        if ok.sum() < 10:
            continue
        t = tau[i][ok]
        bs = np.array([np.log(2) / t[rng.integers(0, len(t), len(t))].mean() for _ in range(reps)]) / lam
        fsle_rows.append(dict(system=system, scale_rel=float(levels[i]), fsle_over_lambda=float(np.log(2) / t.mean() / lam),
                              ci95_lo=float(np.quantile(bs, 0.025)), ci95_hi=float(np.quantile(bs, 0.975)),
                              frac_reached=float(ok.mean()), label="estimate"))
    res["fsle"] = fsle_rows
    return res


def main():
    config.ensure_dirs()
    RUNS.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    for s in ALL_SYSTEMS:
        if not (RUNS / f"distortion_{s}.npz").exists():
            raise SystemExit("run scripts/t2_system_table.py first")
    jobs = [("h", s, o) for s in SYSTEMS for o in ORIENTS] + [("fsle", s) for s in SYSTEMS]
    jobs += [("di", s, R) for s in ALL_SYSTEMS for R in RATES]
    only = os.environ.get("T2_ONLY")
    if only:
        jobs = [j for j in jobs if j[1] == only]
    with ProcessPoolExecutor(min(N_WORKERS, 24)) as pool:
        for name, msg in pool.map(run_job, jobs):
            print(name, msg, flush=True)
    lyap = FZ["lyapunov"]
    sha = config.git_sha()
    allres, rate_rows, r_rows, fsle_rows = {}, [], [], []
    for s in (SYSTEMS if not only else [only] if only in SYSTEMS else []):
        r = analyse(s, float(lyap[s]["d_ky"]))
        allres[s] = r
        rate_rows += r["rates"]
        for o, v in r["orientations"].items():
            for i, dlt in enumerate(r["rel_deltas"]):
                r_rows.append(dict(system=s, orientation=o, delta_over_sigma_A=dlt, H_mean=v["H_mean"][i],
                                   H_ci95_lo=v["H_ci95"][i][0], H_ci95_hi=v["H_ci95"][i][1],
                                   frac_no_cross=v["frac_no_cross"][i], r_central=v["r_central"][i],
                                   r_central_ci95_lo=v["r_central_ci95"][i][0],
                                   r_central_ci95_hi=v["r_central_ci95"][i][1], r_ls_whole_range=v["r_ls"],
                                   label="estimate"))
        fsle_rows += r["fsle"]
        print(f"== {s}: saturation max {r['saturation']["max_frac_no_cross_in_range"]:.3f}  "
              f"all held-out met: {r['all_heldout_criterion_met']}")
        for row in r["rates"]:
            p = row["pred"]
            print(f"  R={row['rate_bits']:2d} {row['role']:7s} dhat={row['delta_hat_over_sigma_A']:.4f} "
                  f"pred={p if p is None else round(p, 3)} meas={row['meas']:.3f} "
                  f"[{row['meas_ci95_lo']:.3f},{row['meas_ci95_hi']:.3f}] {row['outcome']}  "
                  f"SA={row['second_author_pred']:.3f}")
        for o, v in r["orientations"].items():
            print(f"  {o:16s} r_ls={v['r_ls']:.3f} r_cd=" + " ".join(f"{q:.2f}" for q in v["r_central"]))
    if not allres:
        return
    ex.write_json(OUT / "exchange_law.json", dict(git_sha=sha, frame_interval=DELTA,
                                                  eps=FZ["scoring"]["eps_primary"], systems=allres))
    ex.write_csv(OUT / "predicted_vs_measured.csv", rate_rows,
                 "pred/second_author = estimate; meas = reference (decode-and-integrate)")
    ex.write_csv(OUT / "h_and_r_by_orientation.csv", r_rows, "all estimates")
    ex.write_csv(OUT / "fsle.csv", fsle_rows, "FSLE/lambda by doubling-time crossings; estimate")


if __name__ == "__main__":
    main()
