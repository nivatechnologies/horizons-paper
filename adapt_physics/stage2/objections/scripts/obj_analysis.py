"""Objections WO analysis (obj_freeze.yaml). Seed-pooled estimator and bootstrap exactly as stage-2 part A
(stage2/scripts/s2_analysis.py: trajectories resampled, then seeds within each trajectory; 2,000 reps).
Writes stage2/objections/results/:
  obj_part1.csv            World V Re 50: every arm, w, eps (restricted mean [95%], S(1), S(3), per-seed), with the
                           Part A World D Re 50 value beside
  obj_part1_readings.csv   H/O, H/L_range_V (ratios [95%]), H_true - H (paired), outcome and detector readings
  obj_detector.csv         identified Re per w, slope [95%], bias from the true Re (H, P1x_V in V; FNO_Re_id in D)
  obj_part2.csv            FNO-Re (true Re, identified Re) and H on the fresh World D (and C) panels; paired H - FNO-Re
  obj_part2_reading.csv    the frozen claim reading at Re 50 and 56 (World D)
  obj_lft.csv              L_ft on fresh panels (Re 44, 50, 56): horizon, retention, H - L_ft, online seconds per state
  obj_edge.csv             Part 3: Orin NX and datacenter timing side by side; horizon agreement
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
PKG = HERE.parents[3]
sys.path.insert(0, str(PKG))
sys.path.insert(0, str(PKG / "stage2" / "scripts"))
sys.path.insert(0, str(PKG.parent / "tokens_horizon"))
from ap import config  # noqa: E402
from s2_analysis import boot_all, boot_idx, crossed_boot, q  # noqa: E402
from th import score  # noqa: E402

RES = PKG / "stage2" / "objections" / "results"
S2R = PKG / "stage2" / "results"
EV = config.RUNS / "obj_eval"
S2EV = config.RUNS / "s2_eval"
DELTA = 0.35


def write(name, rows, note):
    if not rows:
        return
    keys = []
    for r in rows:
        keys += [k for k in r if k not in keys]
    RES.mkdir(parents=True, exist_ok=True)
    with open(RES / name, "w", newline="") as fh:
        fh.write(f"# git_sha={config.git_sha()}; Adapt the Physics objections WO; {note}\n")
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)


def load(files, lam, e, start=1):
    Z = [np.load(f) for f in files if f.exists()]
    if not Z:
        return None, None, None
    H = np.stack([score.horizon(z["err"].astype(float), lam, DELTA, 10.0, e, start)[0] for z in Z])
    C = np.stack([score.horizon(z["err"].astype(float), lam, DELTA, 10.0, e, start)[1] for z in Z])
    R = np.stack([z["re_hat"] for z in Z]) if "re_hat" in Z[0] else None
    return H, C, R


rng = np.random.default_rng(779)
IDX = boot_idx(300)


def stats(H, C):
    """Primary interval: crossed bootstrap (trajectory rows and seed columns resampled independently; post-freeze, Todd
    2026-09-27). Also the interval conditional on the trained models and the frozen nested bootstrap."""
    b = boot_all(H, IDX, rng)
    lo, hi = q(b["crossed"])
    return dict(restricted_mean=float(H.mean()), ci95_lo=lo, ci95_hi=hi, cond_ci95_lo=q(b["cond"])[0], cond_ci95_hi=q(b["cond"])[1],
                nested_ci95_lo=q(b["nested"])[0], nested_ci95_hi=q(b["nested"])[1], seeds=H.shape[0],
                per_seed=" ".join(f"{v:.3f}" for v in H.mean(1)), seed_sd=float(H.mean(1).std(ddof=1)) if H.shape[0] > 1 else None,
                S1=float(np.mean(~C | (H > 1))), S3=float(np.mean(~C | (H > 3)))), b


def _per_seed(Ha, Hb, op):
    sa, sb = Ha.mean(1), Hb.mean(1)
    if len(sa) == 1 and len(sb) > 1:
        return [op(sa[0], x) for x in sb]
    return [op(sa[i], sb[i] if len(sb) == len(sa) else sb[0]) for i in range(len(sa))]


def ratio(ba, bb, Ha, Hb):
    ex = {f"{m}_ci95": "[%.4f, %.4f]" % q(ba[m] / bb[m]) for m in ("cond", "nested")}
    ex["per_seed"] = " ".join(f"{x:.3f}" for x in _per_seed(Ha, Hb, lambda a, b: a / b))
    lo, hi = q(ba["crossed"] / bb["crossed"])
    return float(Ha.mean() / Hb.mean()), lo, hi, ex


def diff(ba, bb, Ha, Hb):
    d = ba["crossed"] - bb["crossed"]
    ex = {}
    for m in ("cond", "nested"):
        ex[f"{m}_ci95_lo"], ex[f"{m}_ci95_hi"] = q(ba[m] - bb[m])
    ex["per_seed_diff"] = " ".join(f"{x:.3f}" for x in _per_seed(Ha, Hb, lambda a, b: a - b))
    return float(Ha.mean() - Hb.mean()), float(np.quantile(d, 0.025)), float(np.quantile(d, 0.975)), \
        float(np.quantile(d, 0.05)), float(np.quantile(d, 0.95)), ex


def slope_of(Rs, ws):
    """Rs (S, n, W) identified Re per seed, state, window. Per-seed per-state least-squares slopes; point = mean; interval
    crossed (states and seeds resampled independently), plus conditional (seed-averaged slopes, states resampled)."""
    x = np.array(ws, float)
    xc = x - x.mean()
    S = (Rs - Rs.mean(2, keepdims=True)) @ xc / (xc ** 2).sum()      # (S, n)
    lo, hi = q(crossed_boot(S, IDX, rng))
    clo, chi = q(S.mean(0)[IDX].mean(1))
    return float(S.mean()), lo, hi, clo, chi, " ".join(f"{v:.4f}" for v in S.mean(1))


def s2_value(arm, Re, e=0.1, w=11, world="D"):
    for r in csv.DictReader(l for l in open(S2R / "s2_rows.csv") if not l.startswith("#")):
        if r["world"] == world and r["Re"] == str(Re) and r["arm"] == arm and r["w"] == str(w) and r["eps"] == str(e) \
                and r["score"] == "future":
            return float(r["restricted_mean"])
    return None


def part1():
    tpf = RES / "test_panels.json"
    if not tpf.exists():
        return
    tp = json.loads(tpf.read_text())["obj_V_Re50"]
    lam = tp["lam"]
    P = EV / "obj_V_Re50"
    seeds = {"H": [0, 1, 2], "H_true": [0, 1, 2], "L0": [0, 1, 2], "L_range_V": [0, 1, 2], "O_V": [0], "P1x_V": [0]}
    rows, rd, det = [], [], []
    B, HH = {}, {}
    for arm, ss in seeds.items():
        for w in (3, 6, 11, 23):
            for e in (0.1, 0.3):
                H, C, R = load([P / f"{arm}_s{s}_{w}.npz" for s in ss], lam, e)
                if H is None:
                    continue
                st, b = stats(H, C)
                B[(arm, w, e)], HH[(arm, w, e)] = b, H
                partA = {"H": "H", "H_true": None, "L0": "L0", "L_range_V": "L_range", "O_V": "O", "P1x_V": "P1x"}[arm]
                rows.append(dict(world="V", Re=50, arm=arm, w=w, eps=e, n=H.shape[1], **st, phys_time=float(H.mean()) / lam,
                                 partA_worldD_Re50=s2_value(partA, 50, e, w) if partA else None,
                                 label="hybrid (learned correction)" if arm.startswith("H") else
                                 "learned" if arm.startswith("L") else "reference"))
    for e in (0.1, 0.3):
        k = lambda a: (a, 11, e)  # noqa: E731
        if all(k(a) in B for a in ("H", "O_V", "L_range_V")):
            hO = ratio(B[k("H")], B[k("O_V")], HH[k("H")], HH[k("O_V")])
            hL = ratio(B[k("H")], B[k("L_range_V")], HH[k("H")], HH[k("L_range_V")])
            outcome = "holds" if hO[0] >= 0.85 and hL[0] >= 1.5 else "degrades, still leads" if hL[0] >= 1.2 else "loses its lead"
            r = dict(eps=e, primary=e == 0.1, H_over_O=hO[0], H_over_O_ci95_lo=hO[1], H_over_O_ci95_hi=hO[2],
                     H_over_O_cond_ci95=hO[3]["cond_ci95"], H_over_O_nested_ci95=hO[3]["nested_ci95"], H_over_O_per_seed=hO[3]["per_seed"],
                     H_over_L_range_V=hL[0], H_over_L_range_V_ci95_lo=hL[1], H_over_L_range_V_ci95_hi=hL[2],
                     H_over_L_range_V_cond_ci95=hL[3]["cond_ci95"], H_over_L_range_V_nested_ci95=hL[3]["nested_ci95"],
                     H_over_L_range_V_per_seed=hL[3]["per_seed"],
                     outcome_reading=outcome, L_range_V_seeds=HH[k("L_range_V")].shape[0],
                     partA_D_Re50_H_over_O=(s2_value("H", 50, e) / s2_value("O", 50, e)) if s2_value("O", 50, e) else None,
                     partA_D_Re50_H_over_L_range=(s2_value("H", 50, e) / s2_value("L_range", 50, e)) if s2_value("L_range", 50, e) else None)
            if k("H_true") in B:
                d = diff(B[k("H_true")], B[k("H")], HH[k("H_true")], HH[k("H")])
                r.update(H_true_minus_H=d[0], H_true_minus_H_ci95_lo=d[1], H_true_minus_H_ci95_hi=d[2],
                         H_true_minus_H_cond_ci95="[%.4f, %.4f]" % (d[5]["cond_ci95_lo"], d[5]["cond_ci95_hi"]),
                         H_true_minus_H_nested_ci95="[%.4f, %.4f]" % (d[5]["nested_ci95_lo"], d[5]["nested_ci95_hi"]),
                         H_true_minus_H_per_seed=d[5]["per_seed_diff"])
            rd.append(dict(r, label="reading (reported, not criterion)"))
    for arm, ss in (("H", [0, 1, 2]), ("P1x_V", [0])):
        ws = [w for w in (3, 6, 11, 23) if all((P / f"{arm}_s{s}_{w}.npz").exists() for s in ss)]
        if len(ws) >= 2:
            Rs = np.stack([np.stack([np.load(P / f"{arm}_s{s}_{w}.npz")["re_hat"] for s in ss]) for w in ws], 2)   # (S, n, W)
            R = Rs.mean(0)
            sl = slope_of(Rs, ws)
            det.append(dict(world="V", Re=50, arm=arm, w_tested=",".join(map(str, ws)),
                            **{f"re_hat_w{w}": float(R[:, i].mean()) for i, w in enumerate(ws)},
                            mean_re_hat=float(R.mean()), bias_from_true=float(R.mean() - 50),
                            slope_per_frame=sl[0], slope_ci95_lo=sl[1], slope_ci95_hi=sl[2], slope_cond_ci95_lo=sl[3],
                            slope_cond_ci95_hi=sl[4], slope_per_seed=sl[5],
                            detector_reading=("flags" if (sl[1] > 0 or sl[2] < 0) else "silent") if arm == "H" else "",
                            label="estimate (reported only)"))
    return rows, rd, det


def part2():
    tp = json.loads((S2R / "test_panels.json").read_text())
    rows, reading, det, lft = [], [], [], []
    for world, arms_seeds in (("D", [0, 1, 2]), ("C", [0])):
        for Re in (36, 40, 44, 50, 56):
            panel = f"s2_test_Re{Re}_{world}"
            if panel not in tp:
                continue
            lam = tp[panel]["lam"]
            for e in (0.1, 0.3):
                Hh, Ch, _ = load([S2EV / panel / f"H_s{s}_std_11.npz" for s in (0, 1, 2)], lam, e)
                Ho, Co, _ = load([S2EV / panel / "O_s0_std_11.npz"], lam, e)
                if Hh is None or Ho is None:
                    continue
                sh, bh = stats(Hh, Ch)
                _, bo = stats(Ho, Co)
                for arm in ("FNO_Re_true", "FNO_Re_id", "FNOw_Re_true", "FNOw_Re_id"):
                    sds = [0] if arm.startswith("FNOw") else arms_seeds
                    Hf, Cf, _ = load([EV / panel / f"{arm}_s{s}_11.npz" for s in sds], lam, e)
                    if Hf is None:
                        continue
                    sf, bf = stats(Hf, Cf)
                    d = diff(bh, bf, Hh, Hf)
                    rows.append(dict(world=world, Re=Re, arm=arm, w=11, eps=e, n=Hf.shape[1], **sf,
                                     retention=float(Hf.mean() / Ho.mean()), H=float(Hh.mean()), H_retention=float(Hh.mean() / Ho.mean()),
                                     H_minus_arm=d[0], diff_ci95_lo=d[1], diff_ci95_hi=d[2], diff_ci90_lo=d[3], diff_ci90_hi=d[4],
                                     diff_cond_ci95_lo=d[5]["cond_ci95_lo"], diff_cond_ci95_hi=d[5]["cond_ci95_hi"],
                                     diff_nested_ci95_lo=d[5]["nested_ci95_lo"], diff_nested_ci95_hi=d[5]["nested_ci95_hi"],
                                     diff_per_seed=d[5]["per_seed_diff"],
                                     label="learned (Re-conditioned FNO, Re 30-60 data; post-freeze, reported only, no reading)"
                                     if arm.startswith("FNOw") else "learned (Re-conditioned FNO)"))
            if world == "D":
                for w in (3, 6, 11, 23):
                    pass
    for Re in (50, 56):
        r = [x for x in rows if x["world"] == "D" and x["Re"] == Re and x["arm"] == "FNO_Re_true" and x["eps"] == 0.1]
        if r:
            r = r[0]
            ok = r["H_minus_arm"] >= 0.25 and r["diff_ci95_lo"] > 0
            ok_c = r["H_minus_arm"] >= 0.25 and r["diff_cond_ci95_lo"] > 0
            ok_n = r["H_minus_arm"] >= 0.25 and r["diff_nested_ci95_lo"] > 0
            reading.append(dict(Re=Re, H_minus_FNO_Re_true=r["H_minus_arm"], ci95_lo=r["diff_ci95_lo"], ci95_hi=r["diff_ci95_hi"],
                                cond_ci95_lo=r["diff_cond_ci95_lo"], cond_ci95_hi=r["diff_cond_ci95_hi"],
                                nested_ci95_lo=r["diff_nested_ci95_lo"], nested_ci95_hi=r["diff_nested_ci95_hi"],
                                per_seed=r["diff_per_seed"], seeds=r["seeds"], holds_at_this_Re=ok, holds_cond=ok_c, holds_nested=ok_n,
                                label="reading component"))
    if len(reading) == 2:
        both = all(x["holds_at_this_Re"] for x in reading)
        reading.append(dict(Re="50 and 56", holds_at_this_Re=both,
                            claim="A network given the parameter does not extrapolate: " + ("STATED" if both else "REMOVED"),
                            label="frozen reading (decides the claim)"))
    # detector for FNO_Re_id (World D, seed-averaged)
    for Re in (36, 40, 44, 50, 56):
        panel = f"s2_test_Re{Re}_D"
        ws = [w for w in (3, 6, 11, 23) if all((EV / panel / f"FNO_Re_id_s{s}_{w}.npz").exists() for s in (0, 1, 2))]
        if len(ws) >= 2:
            Rs = np.stack([np.stack([np.load(EV / panel / f"FNO_Re_id_s{s}_{w}.npz")["re_hat"] for s in (0, 1, 2)])
                           for w in ws], 2)
            R = Rs.mean(0)
            sl = slope_of(Rs, ws)
            det.append(dict(world="D", Re=Re, arm="FNO_Re_id", w_tested=",".join(map(str, ws)),
                            **{f"re_hat_w{w}": float(R[:, i].mean()) for i, w in enumerate(ws)}, mean_re_hat=float(R.mean()),
                            bias_from_true=float(R.mean() - Re), slope_per_frame=sl[0], slope_ci95_lo=sl[1], slope_ci95_hi=sl[2],
                            slope_cond_ci95_lo=sl[3], slope_cond_ci95_hi=sl[4], slope_per_seed=sl[5],
                            label="estimate (reported only)"))
    # L_ft
    for Re in (44, 50, 56):
        panel = f"s2_test_Re{Re}_D"
        lam = tp[panel]["lam"]
        H1, C1, _ = load([EV / panel / "L_ft_s0_11.npz"], lam, 0.1)
        if H1 is None:
            continue
        Hh, _, _ = load([S2EV / panel / f"H_s{s}_std_11.npz" for s in (0, 1, 2)], lam, 0.1)
        Ho, _, _ = load([S2EV / panel / "O_s0_std_11.npz"], lam, 0.1)
        s1, b1 = stats(H1, C1)
        _, bh = stats(Hh, np.zeros_like(Hh, bool))
        d = diff(bh, b1, Hh, H1)
        meta = json.loads((RES / f"eval_{panel}.json").read_text()).get("L_ft_s0_11", {})
        lft.append(dict(world="D", Re=Re, w=11, eps=0.1, n=H1.shape[1], **s1, retention=float(H1.mean() / Ho.mean()),
                        H=float(Hh.mean()), H_minus_L_ft=d[0], diff_ci95_lo=d[1], diff_ci95_hi=d[2],
                        diff_cond_ci95_lo=d[5]["cond_ci95_lo"], diff_cond_ci95_hi=d[5]["cond_ci95_hi"],
                        diff_nested_ci95_lo=d[5]["nested_ci95_lo"], diff_nested_ci95_hi=d[5]["nested_ci95_hi"],
                        diff_per_seed=d[5]["per_seed_diff"],
                        online_seconds_per_state=meta.get("wall_seconds_per_state"), label="learned (reported, not a reading)"))
    return rows, reading, det, lft


def id_error():
    """Per-state |identified Re - true Re| at w = 11, pooled over states and seeds: median and 90th percentile."""
    rows = []
    tp = json.loads((S2R / "test_panels.json").read_text())
    specs = [("H", S2EV, "H_s{s}_std_11.npz", [0, 1, 2]), ("FNO_Re_id", EV, "FNO_Re_id_s{s}_11.npz", None),
             ("FNOw_Re_id", EV, "FNOw_Re_id_s{s}_11.npz", [0])]
    for world in ("D", "C"):
        for Re in (36, 40, 44, 50, 56):
            panel = f"s2_test_Re{Re}_{world}"
            if panel not in tp:
                continue
            for arm, base, pat, seeds in specs:
                ss = seeds if seeds is not None else ([0, 1, 2] if world == "D" else [0])
                fs = [base / panel / pat.format(s=s) for s in ss]
                fs = [f for f in fs if f.exists()]
                if not fs:
                    continue
                err = np.abs(np.concatenate([np.load(f)["re_hat"] for f in fs]) - Re)
                rows.append(dict(world=world, Re=Re, arm=arm, w=11, seeds=len(fs), n_values=len(err),
                                 abs_err_median=float(np.median(err)), abs_err_p90=float(np.quantile(err, 0.9)),
                                 abs_err_max=float(err.max()), label="estimate"))
    P = EV / "obj_V_Re50"
    fs = [P / f"H_s{s}_11.npz" for s in (0, 1, 2) if (P / f"H_s{s}_11.npz").exists()]
    if fs:
        err = np.abs(np.concatenate([np.load(f)["re_hat"] for f in fs]) - 50)
        rows.append(dict(world="V", Re=50, arm="H", w=11, seeds=len(fs), n_values=len(err), abs_err_median=float(np.median(err)),
                         abs_err_p90=float(np.quantile(err, 0.9)), abs_err_max=float(err.max()), label="estimate"))
    return rows


def edge():
    rows = []
    orin = RES / "edge_orin.json"
    dc = RES / "edge_datacenter.json"
    if not orin.exists():
        return rows
    O = json.loads(orin.read_text())
    D = json.loads(dc.read_text()) if dc.exists() else {"arms": {}}
    for arm, r in O["arms"].items():
        d = D["arms"].get(arm, {})
        row = dict(arm=arm, orin_result=r.get("result", "ok"))
        for k in ("wall_median", "wall_p90", "identify_or_adapt_median", "forecast_median", "forecast_fps", "peak_torch_mem_MB",
                  "tegrastats_ram_peak_MB", "vdd_in_mean_mW", "energy_per_state_J"):
            row[f"orin_{k}"] = r.get(k)
            row[f"dc_batch1_{k}"] = d.get(k)
        if "states" in r and "states" in d:
            ho = {s["state"]: s["horizon"] for s in r["states"] if not s["warmup"]}
            hd = {s["state"]: s["horizon"] for s in d["states"] if not s["warmup"]}
            common = sorted(set(ho) & set(hd))
            if common:
                diffs = [abs(ho[i] - hd[i]) for i in common]
                row.update(horizon_max_abs_diff=max(diffs), horizon_states_identical=sum(x == 0 for x in diffs), horizon_n=len(common))
        for tag, f in (("orin_fixed", RES / "edge_orin_fixed.json"), ("dc_fixed", RES / "edge_datacenter_fixed.json")):
            if f.exists():
                J = json.loads(f.read_text())
                rr = J["arms"].get(arm, {})
                row[f"{tag}_frames"] = J.get("fixed_frames")
                for k in ("wall_median", "wall_p90", "identify_or_adapt_median", "forecast_median", "forecast_fps",
                          "vdd_in_mean_mW", "energy_per_state_J", "peak_torch_mem_MB"):
                    row[f"{tag}_{k}"] = rr.get(k)
                if rr.get("states"):
                    row[f"{tag}_frames_per_state"] = sorted({s["frames"] for s in rr["states"] if not s["warmup"]})[0]
            else:                                           # run still in progress: explicit, so the NUMBERS checker resolves
                for k in ("frames", "wall_median", "wall_p90", "identify_or_adapt_median", "forecast_median", "forecast_fps",
                          "vdd_in_mean_mW", "energy_per_state_J", "peak_torch_mem_MB"):
                    row[f"{tag}_{k}"] = "pending"
        rows.append(dict(row, early_stop_note="early-stop columns (orin_*, dc_batch1_*): each arm forecasts until every state "
                                              "exceeds 0.3 sigma_A, so frame counts differ by arm; *_fixed_*: every arm forecasts "
                                              "the same fixed F frames",
                         orin_host=json.dumps(O["host"]), dc_host=json.dumps(D.get("host", {})), label="estimate (reported only)"))
    return rows


def main():
    p1 = part1()
    if p1:
        write("obj_part1.csv", p1[0], "Part 1 World V")
        write("obj_part1_readings.csv", p1[1], "Part 1 readings")
    p2 = part2()
    write("obj_part2.csv", p2[0], "Part 2 FNO-Re")
    write("obj_part2_reading.csv", p2[1], "Part 2 frozen reading")
    write("obj_detector.csv", (p1[2] if p1 else []) + p2[2], "detectors")
    write("obj_lft.csv", p2[3], "L_ft on fresh panels")
    write("obj_edge.csv", edge(), "Part 3 edge timing")
    write("obj_id_error.csv", id_error(), "per-state |identified Re - true Re| at w = 11")
    for r in (p1[1] if p1 else []) + p2[1]:
        print(r)


if __name__ == "__main__":
    main()
