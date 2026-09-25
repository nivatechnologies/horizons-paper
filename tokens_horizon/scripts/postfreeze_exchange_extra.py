"""POST-FREEZE (requested by Todd, 2026-09-25; not pre-registered). Reported in NUMBERS.md section P.

(1) Exchange-law predictions recomputed two further ways, next to the frozen RMS prediction h(delta_hat_RMS):
    per-state   pred = mean_i h(e_i), e_i = each confirmation-panel state's own initial (decode) error / sigma_A
                at rate R (the same 1,000 states and errors the measured decode-and-integrate horizon uses);
                h is the frozen fresh-orientation calibration curve, linear in ln delta; errors outside the
                calibrated range [1e-4, 10^-0.5] sigma_A are clamped to the range end, and the clamped fraction is reported.
    geometric   pred = h(exp(mean_i ln e_i)) on the same states (nan if outside the calibrated range).
    Intervals: bootstrap resampling the 1,000 h states and the 1,000 panel states jointly (2,000 reps).
    Criterion outcomes are NOT recomputed: the frozen outcomes stand. Errors and the frozen tolerance are
    shown for information only.
(3) Least-squares decode-and-integrate slope, Lyapunov times per bit, every system: H_DI(R) restricted means
    on the 1,000-state confirmation panel (Delta 0.02, future frames, eps 0.3) against R. Primary fit over R = 4..12;
    also over the frozen fit rates {6, 8, 10, 12}. 95% interval: bootstrap over panel states, paired across rates.
(b) Every per-state and geometric-mean prediction carries the share of panel states whose initial error lies
    outside the calibrated h range (clamped share). Cells with a clamped share above 25% are marked uninformative.
(a) slope x D_eff per system for both fit ranges, with a 95% interval propagated from both: the slope bootstrap
    (panel states) and the D_eff bootstrap (150 calibration trajectories, the frozen system-table method) are
    independent, so each replicate multiplies one draw of each. Implied r = ln 2 / (slope x D_eff), interval from the
    same replicates. Shown beside section R's local r (fresh orientation, central differences) at codebook scales,
    i.e. the h-grid points between the 12-bit and 4-bit calibration distortions. Also whether the calibration
    distortion ever falls below the 0.3 sigma_A tolerance within 4-12 bits.
Labels: predictions and slopes are estimates; measured horizons are references.
"""
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np  # noqa: E402

from th import config  # noqa: E402

FZ = config.freeze()
EL = FZ["exchange_law"]
RUNS = config.RUNS / "exchange_law"
OUT = config.RESULTS / "postfreeze"
RATES = list(range(4, 13))
ALL_SYSTEMS = ["lorenz28", "lorenz45", "l96_5", "l96_6", "l96_10", "l96_20"]
REPS = FZ["seeds"]["bootstrap_reps"]


def h_interp(x_ln, y, t_ln):
    """x_ln increasing ln delta grid, y matching H values; clamp outside."""
    return np.interp(t_ln, x_ln, y)


def frozen_rows():
    p = config.RESULTS / "exchange_law" / "predicted_vs_measured.csv"
    rows = list(csv.DictReader(l for l in open(p) if not l.startswith("#")))
    return {(r["system"], int(r["rate_bits"])): r for r in rows}


def tol_of(meas):
    c = EL["criterion"]
    return c["relative"] * meas if meas >= c["split_at"] else c["absolute_below_half"]


def exchange_variants():
    fr = frozen_rows()
    out = []
    for system in EL["systems"]:
        h = np.load(RUNS / f"h_{system}_fresh.npz")
        dl = h["rel_deltas"]                      # decreasing
        x = np.log(dl[::-1])                      # increasing ln delta
        Hs = h["H"][::-1]                         # (15, n_h) aligned with x
        Hm = Hs.mean(1)
        rng = np.random.default_rng(FZ["seeds"]["bootstrap_seed"])
        hb = rng.integers(0, Hs.shape[1], (REPS, Hs.shape[1]))
        Hb = np.stack([Hs[:, b].mean(1) for b in hb])            # (REPS, 15)
        for R in RATES:
            z = np.load(RUNS / f"di_{system}_R{R}.npz")
            e = z["err0_rel"]
            n = len(e)
            le = np.log(np.maximum(e, 1e-300))
            above, below = float((le > x[-1]).mean()), float((le < x[0]).mean())
            clamped = above + below
            uninf = "UNINFORMATIVE (clamped > 25%)" if clamped > 0.25 else ""
            per_state = float(h_interp(x, Hm, le).mean())
            gm = float(np.exp(le.mean()))
            geo = float(h_interp(x, Hm, np.log(gm))) if x[0] <= np.log(gm) <= x[-1] else float("nan")
            pb = rng.integers(0, n, (REPS, n))
            ps_b = np.array([np.interp(le[pb[r]], x, Hb[r]).mean() for r in range(REPS)])
            gm_b = np.exp(le[pb].mean(1))
            geo_b = np.array([np.interp(np.log(gm_b[r]), x, Hb[r]) for r in range(REPS)])
            f = fr[(system, R)]
            meas = float(f["meas"])
            frozen_pred = float(f["pred"]) if f["pred"] not in ("", "nan") else float("nan")
            tol = tol_of(meas)
            out.append(dict(
                system=system, rate_bits=R, role=f["role"], meas=meas, meas_label="reference",
                frozen_pred_rms=frozen_pred, frozen_delta_hat_rms=float(f["delta_hat_over_sigma_A"]),
                frozen_err=frozen_pred - meas if np.isfinite(frozen_pred) else float("nan"),
                frozen_outcome=f["outcome"],
                panel_rms_err0=float(np.sqrt((e ** 2).mean())),
                pred_per_state=per_state, pred_per_state_lo=float(np.quantile(ps_b, .025)),
                pred_per_state_hi=float(np.quantile(ps_b, .975)), err_per_state=per_state - meas,
                frac_err0_above_h_range=above, frac_err0_below_h_range=below,
                clamped_share_per_state=clamped, per_state_flag=uninf,
                geomean_err0=gm, pred_geomean=geo,
                pred_geomean_lo=float(np.quantile(geo_b, .025)) if np.isfinite(geo) else float("nan"),
                pred_geomean_hi=float(np.quantile(geo_b, .975)) if np.isfinite(geo) else float("nan"),
                err_geomean=geo - meas if np.isfinite(geo) else float("nan"),
                clamped_share_geomean_states=clamped,
                geomean_flag=("no prediction (geometric mean outside h range)" if not np.isfinite(geo) else uninf),
                frozen_tolerance_info_only=tol,
                label="post-freeze estimate (criterion outcomes stay as frozen)"))
    return out


SLOPE_BOOTS = {}


def di_slopes():
    out = []
    lam_rng = np.random.default_rng(FZ["seeds"]["bootstrap_seed"])
    for system in ALL_SYSTEMS:
        H = np.stack([np.load(RUNS / f"di_{system}_R{R}.npz")["H"] for R in RATES])     # (9, n)
        n = H.shape[1]
        idx = lam_rng.integers(0, n, (REPS, n))
        for name, rates in (("R4-12", RATES), ("fit_rates_6-12", EL["deff_fit_rates"])):
            sel = [RATES.index(r) for r in rates]
            y = H[sel].mean(1)
            s = float(np.polyfit(rates, y, 1)[0])
            yb = np.stack([H[sel][:, i].mean(1) for i in idx])                            # (REPS, k)
            sb = np.polyfit(rates, yb.T, 1)[0]
            SLOPE_BOOTS[(system, name)] = (s, sb)
            out.append(dict(system=system, fit=name, rates=" ".join(map(str, rates)),
                            slope_lyap_per_bit=s, ci95_lo=float(np.quantile(sb, .025)),
                            ci95_hi=float(np.quantile(sb, .975)),
                            H_by_rate=" ".join(f"{v:.4f}" for v in y),
                            label="post-freeze estimate (decode-and-integrate is a reference)"))
    return out


def deff_boots(system):
    """Replicates the frozen system-table D_eff bootstrap (same data, estimator, seed and reps)."""
    z = np.load(RUNS / f"distortion_{system}.npz")
    sq, count, rates = z["sq_by_traj"], z["count"], list(z["rates"])
    fit_idx = [rates.index(r) for r in EL["deff_fit_rates"]]

    def deff_from(sq_, cnt_):
        delta = np.sqrt(sq_[fit_idx].sum(1) / cnt_.sum())
        return -1.0 / np.polyfit(np.array(rates)[fit_idx], np.log2(delta), 1)[0]

    rng = np.random.default_rng(FZ["seeds"]["bootstrap_seed"])
    n = len(count)
    bs = np.empty(REPS)
    for r in range(REPS):
        k = rng.integers(0, n, n)
        bs[r] = deff_from(sq[:, k], count[k])
    return float(deff_from(sq, count)), bs


def slope_times_deff():
    tol = FZ["scoring"]["eps_primary"]
    dist = list(csv.DictReader(l for l in open(config.RESULTS / "dimension" / "distortion_kmeans.csv")
                               if not l.startswith("#")))
    rrows = list(csv.DictReader(l for l in open(config.RESULTS / "exchange_law" / "h_and_r_by_orientation.csv")
                                if not l.startswith("#")))
    out = []
    for system in ALL_SYSTEMS:
        d0, db = deff_boots(system)
        dhat = {int(r["rate_bits"]): float(r["delta_over_sigma_A"]) for r in dist if r["system"] == system}
        below_tol = [R for R in RATES if dhat[R] < tol]
        fr = [r for r in rrows if r["system"] == system and r["orientation"] == "fresh"]
        lo_d, hi_d = dhat[max(RATES)], dhat[min(RATES)]
        rloc = [float(r["r_central"]) for r in fr if lo_d <= float(r["delta_over_sigma_A"]) <= hi_d]
        for name in ("R4-12", "fit_rates_6-12"):
            s0, sb = SLOPE_BOOTS[(system, name)]
            prod, prod_b = s0 * d0, sb * db
            r_impl = np.log(2) / prod if prod > 0 else float("nan")
            with np.errstate(divide="ignore"):
                rb = np.where(prod_b > 0, np.log(2) / prod_b, np.nan)
            note = ("" if below_tol else
                    "calibration distortion never falls below the 0.3 sigma_A tolerance within 4-12 bits "
                    f"(12-bit delta = {dhat[12]:.3f} sigma_A); slope and r not meaningful as an exchange rate")
            out.append(dict(system=system, fit=name, slope_lyap_per_bit=s0, d_eff=d0,
                            slope_x_deff=prod, slope_x_deff_lo=float(np.quantile(prod_b, .025)),
                            slope_x_deff_hi=float(np.quantile(prod_b, .975)),
                            implied_r=r_impl, implied_r_lo=float(np.nanquantile(rb, .025)),
                            implied_r_hi=float(np.nanquantile(rb, .975)),
                            local_r_codebook_scales_median=float(np.median(rloc)) if rloc else float("nan"),
                            local_r_codebook_scales_min=float(min(rloc)) if rloc else float("nan"),
                            local_r_codebook_scales_max=float(max(rloc)) if rloc else float("nan"),
                            local_r_scale_range=f"{lo_d:.4f}-{hi_d:.4f} sigma_A" if rloc else "no h curve (section R covers 4 systems)",
                            local_r_ls_whole_range=float(fr[0]["r_ls_whole_range"]) if fr else float("nan"),
                            rates_below_tolerance=" ".join(map(str, below_tol)) or "none", note=note,
                            label="post-freeze estimate"))
    return out


def write(name, rows, sha):
    with open(OUT / f"{name}.csv", "w", newline="") as fh:
        fh.write(f"# git_sha={sha}; POST-FREEZE (Todd 2026-09-25), not pre-registered\n")
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sha = config.git_sha()
    ex, sl = exchange_variants(), di_slopes()
    sd = slope_times_deff()
    write("exchange_law_variants", ex, sha)
    write("di_slope", sl, sha)
    write("slope_x_deff", sd, sha)
    (OUT / "exchange_extra.json").write_text(json.dumps(dict(git_sha=sha, note=__doc__, exchange_law_variants=ex,
                                                             di_slope=sl, slope_x_deff=sd), indent=1, default=float))
    for r in ex:
        if r["role"] == "heldout":
            print(f"{r['system']:9s} R{r['rate_bits']:2d} meas {r['meas']:.3f} | RMS {r['frozen_pred_rms']:.3f} "
                  f"({r['frozen_err']:+.3f}) | per-state {r['pred_per_state']:.3f} ({r['err_per_state']:+.3f}; "
                  f"clamped {r['frac_err0_above_h_range']:.2f}) | geo {r['pred_geomean']:.3f} ({r['err_geomean']:+.3f}) "
                  f"| tol {r['frozen_tolerance_info_only']:.3f} {r['per_state_flag']}")
    for r in sd:
        print(f"{r['system']:9s} {r['fit']:15s} s*Deff {r['slope_x_deff']:.4f} [{r['slope_x_deff_lo']:.4f}, "
              f"{r['slope_x_deff_hi']:.4f}] r_impl {r['implied_r']:.3f} [{r['implied_r_lo']:.3f}, {r['implied_r_hi']:.3f}] "
              f"| local r median {r['local_r_codebook_scales_median']:.3f} ({r['local_r_codebook_scales_min']:.2f}-"
              f"{r['local_r_codebook_scales_max']:.2f}) ls {r['local_r_ls_whole_range']:.3f} | below tol: {r['rates_below_tolerance']}")
    for r in sl:
        print(f"{r['system']:9s} {r['fit']:15s} {r['slope_lyap_per_bit']:.4f} [{r['ci95_lo']:.4f}, {r['ci95_hi']:.4f}]")


if __name__ == "__main__":
    main()
