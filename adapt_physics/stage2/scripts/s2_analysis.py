"""Stage-2 analysis (stage2/s2_freeze.yaml). Writes stage2/results/:
  s2_rows.csv          part A: per world, Re, arm, w, eps, score (future / from_t0): seed-pooled restricted mean [95%],
                       per-seed means, S(1), S(3), retention (share of O), ratio to L_range
  s2_conditions.csv    the pivot criteria on the fresh panels: point ratio, 95% interval, threshold, holds; screening value
  s2_outcome.csv       outcome (KILL -> PASS -> MIDDLE -> otherwise)
  s2_paired.csv        paired differences (seed-pooled, seeds resampled within trajectories) and frozen readings
  s2_recovery.csv      time to 90% of O on w in {3, 6, 11}
  s2_detector.csv      identified-Re slope (w 3, 6, 11) for H (seed-averaged) and P1; World C Spearman(slope, O - H)
  s2_partB.csv         items 1-4 (single seed where stated): horizon [95%], ratio to O and to L_range / L_range_wide
  s2_cost.csv, s2_training.csv
Bootstrap: 2,000 reps, seed 777; resample trajectories, then each arm's seeds within each resampled trajectory.
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tokens_horizon"))
from ap import config  # noqa: E402
from th import score  # noqa: E402

RES = config.PKG / "stage2" / "results"
EV = config.RUNS / "s2_eval"
REPS, DELTA = 2000, 0.35
SEEDED = {"H": [0, 1, 2], "L_range": [0, 1, 2], "L0": [0, 1, 2]}
ARMS_A = ["O", "H", "P1x", "L_range", "L_range_wide", "L0", "L0big", "P1", "persistence"]
LABEL = {"O": "reference", "P1": "reference", "P1x": "reference", "persistence": "reference", "H": "hybrid (learned correction)",
         "H_Re_only": "hybrid (learned correction)", "L_range": "learned", "L_range_wide": "learned", "L0": "learned",
         "L0big": "learned"}


def write(name, rows, note):
    if not rows:
        return
    keys = []
    for r in rows:
        keys += [k for k in r if k not in keys]
    RES.mkdir(parents=True, exist_ok=True)
    with open(RES / name, "w", newline="") as fh:
        fh.write(f"# git_sha={config.git_sha()}; Adapt the Physics stage 2; {note}\n")
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)


def boot_idx(n, reps=REPS, seed=777):
    return np.random.default_rng(seed).integers(0, n, (reps, n))


def pooled_boot(Hs, idx, rng):
    """Hs (S, n) per-seed per-state horizons -> (reps,) bootstrap means: states resampled by idx, seeds within state."""
    S, n = Hs.shape
    if S == 1:
        return Hs[0][idx].mean(1)
    sidx = rng.integers(0, S, (idx.shape[0], n, S))
    vals = Hs[sidx, idx[:, :, None]]                     # (reps, n, S): seed draws for each resampled state
    return vals.mean(2).mean(1)


def main():
    tp = json.loads((RES / "test_panels.json").read_text())
    rows, conds, paired, rec, det, partB, cost = [], [], [], [], [], [], []
    H = {}          # (world, Re, arm, w, eps, score) -> (S, n) horizons
    RH = {}         # (world, Re, arm, w) -> (S, n) identified Re
    for world in ("D", "C"):
        for Re in (36, 40, 44, 50, 56):
            panel = f"s2_test_Re{Re}_{world}"
            if panel not in tp:
                continue
            lam = tp[panel]["lam"]
            for arm in ARMS_A + ["H_Re_only"]:
                seeds = SEEDED.get(arm, [0])
                for w in (3, 6, 11):
                    fs = [EV / panel / f"{arm}_s{s}_std_{w}.npz" for s in seeds]
                    fs = [f for f in fs if f.exists()]
                    if not fs:
                        continue
                    Z = [np.load(f) for f in fs]
                    for e in (0.1, 0.3):
                        for sc, start in (("future", 1), ("from_t0", 0)):
                            H[(world, Re, arm, w, e, sc)] = np.stack([score.horizon(z["err"].astype(float), lam, DELTA, 10.0, e, start)[0]
                                                                      for z in Z])
                            H[(world, Re, arm, w, e, sc, "c")] = np.stack([score.horizon(z["err"].astype(float), lam, DELTA, 10.0, e, start)[1]
                                                                           for z in Z])
                    if "re_hat" in Z[0]:
                        RH[(world, Re, arm, w)] = np.stack([z["re_hat"] for z in Z])
    rng = np.random.default_rng(778)
    idx = boot_idx(300)
    B = {}

    def boot(key):
        if key not in B:
            B[key] = pooled_boot(H[key], idx, rng)
        return B[key]

    for key in [k for k in H if len(k) == 6]:
        world, Re, arm, w, e, sc = key
        Hs = H[key]
        c = H[key + ("c",)]
        m = float(Hs.mean())
        bs = boot(key)
        Okey = (world, Re, "O", w, e, sc)
        Lkey = (world, Re, "L_range", w, e, sc)
        lam = tp[f"s2_test_Re{Re}_{world}"]["lam"]
        rows.append(dict(world=world, Re=Re, arm=arm, w=w, eps=e, score=sc, seeds=Hs.shape[0], n=Hs.shape[1], restricted_mean=m,
                         ci95_lo=float(np.quantile(bs, 0.025)), ci95_hi=float(np.quantile(bs, 0.975)), phys_time=m / lam,
                         per_seed=" ".join(f"{v:.3f}" for v in Hs.mean(1)),
                         S1=float(np.mean(~c | (Hs > 1))), S3=float(np.mean(~c | (Hs > 3))),
                         retention=m / H[Okey].mean() if Okey in H else None,
                         ratio_to_L_range=m / H[Lkey].mean() if Lkey in H else None, label=LABEL[arm]))
    # paired differences (seed-pooled)
    for (world, Re, arm, w, e, sc) in [k for k in H if len(k) == 6]:
        if sc != "future" or arm not in ("H",):
            continue
        for b in ("O", "L_range", "L_range_wide", "P1", "L0", "L0big", "P1x"):
            kb = (world, Re, b, w, e, sc)
            if kb not in H:
                continue
            ka = (world, Re, arm, w, e, sc)
            da = boot(ka) - boot(kb)
            d = float(H[ka].mean() - H[kb].mean())
            lo90, hi90, lo95, hi95 = np.quantile(da, [0.05, 0.95, 0.025, 0.975])
            rd = ("b well below a" if d >= 0.25 and lo95 > 0 else "a well below b" if -d >= 0.25 and hi95 < 0
                  else "approximately equal" if lo90 >= -0.1 and hi90 <= 0.1 else "no reading")
            paired.append(dict(world=world, Re=Re, w=w, eps=e, a=arm, b=b, mean_a=float(H[ka].mean()), mean_b=float(H[kb].mean()),
                               ratio=float(H[ka].mean() / H[kb].mean()), diff=d, ci90_lo=lo90, ci90_hi=hi90, ci95_lo=lo95,
                               ci95_hi=hi95, reading=rd, label="estimate"))
    # criteria (pivot, unchanged) with intervals
    scr = {(c["criterion"], c["world"], c["Re"]): c["value"] for c in
           csv.DictReader(l for l in open(config.PKG / "pivot" / "results" / "pv_conditions.csv") if not l.startswith("#"))}

    def ratio(wd, Re, a, b):
        ka, kb = (wd, Re, a, 11, 0.1, "future"), (wd, Re, b, 11, 0.1, "future")
        if ka not in H or kb not in H:
            return None, None, None
        r = boot(ka) / boot(kb)
        return float(H[ka].mean() / H[kb].mean()), float(np.quantile(r, 0.025)), float(np.quantile(r, 0.975))

    def add(name, wd, Re, val, thr, test):
        v, lo, hi = val
        ok = v is not None and test(v)
        conds.append(dict(criterion=name, world=wd, Re=Re, value=v, ci95_lo=lo, ci95_hi=hi, threshold=thr, holds=ok,
                          screening_value=scr.get((name, wd, str(Re))), label="estimate"))
        return ok

    kill = [add("KILL: H/L_range <= 1.0", wd, Re, ratio(wd, Re, "H", "L_range"), 1.0, lambda v: v <= 1.0)
            for wd in ("D", "C") for Re in (50, 56)]
    kill.append(add("KILL: H/O < 0.70 at Re 50 (D)", "D", 50, ratio("D", 50, "H", "O"), 0.70, lambda v: v < 0.70))
    ps = [add("PASS: H/O >= 0.85 (D)", "D", Re, ratio("D", Re, "H", "O"), 0.85, lambda v: v >= 0.85) for Re in (36, 44, 50, 56)]
    ps += [add("PASS: H/L_range >= 1.5 (D)", "D", Re, ratio("D", Re, "H", "L_range"), 1.5, lambda v: v >= 1.5) for Re in (36, 50, 56)]
    kH, k0, kb = ("D", 40, "H", 11, 0.1, "future"), ("D", 40, "L0", 11, 0.1, "future"), ("D", 40, "L0big", 11, 0.1, "future")
    if all(k in H for k in (kH, k0, kb)):
        best = k0 if H[k0].mean() >= H[kb].mean() else kb
        rb = boot(kH) / boot(best)
        v40 = (float(H[kH].mean() / H[best].mean()), float(np.quantile(rb, 0.025)), float(np.quantile(rb, 0.975)))
    else:
        v40 = (None, None, None)
    ps.append(add("PASS: H/max(L0, L0big) >= 0.95 at Re 40 (D)", "D", 40, v40, 0.95, lambda v: v >= 0.95))
    for Re in (50, 56):
        ps.append(add("PASS: H/O >= 0.70 (C)", "C", Re, ratio("C", Re, "H", "O"), 0.70, lambda v: v >= 0.70))
        ps.append(add("PASS: H/L_range >= 1.2 (C)", "C", Re, ratio("C", Re, "H", "L_range"), 1.2, lambda v: v >= 1.2))
    mid = [add("MIDDLE: H/L_range >= 1.3", wd, Re, ratio(wd, Re, "H", "L_range"), 1.3, lambda v: v >= 1.3)
           for wd in ("D", "C") for Re in (50, 56)]
    complete = all(c["value"] is not None for c in conds)
    seeds_ok = all(H.get((wd, Re, a, 11, 0.1, "future"), np.zeros((0, 1))).shape[0] == 3 for wd in ("D", "C")
                   for Re in (36, 40, 44, 50, 56) for a in ("H", "L_range", "L0"))
    outcome = ("KILL" if any(kill) else "PASS (headline A)" if all(ps) else "MIDDLE (headline B)" if all(mid)
               else "OTHERWISE (Todd decides)")
    if not complete or not seeds_ok:
        outcome += " [INCOMPLETE: criteria or seeds missing]"
    # recovery
    for (world, Re, arm, w, e, sc) in [k for k in H if len(k) == 6 and k[3] == 3 and k[5] == "future"]:
        ws = [w2 for w2 in (3, 6, 11) if (world, Re, arm, w2, e, sc) in H and (world, Re, "O", w2, e, sc) in H]
        hit = next((w2 for w2 in ws if H[(world, Re, arm, w2, e, sc)].mean() >= 0.9 * H[(world, Re, "O", w2, e, sc)].mean()), None)
        rec.append(dict(world=world, Re=Re, eps=e, arm=arm, w_tested=",".join(map(str, ws)),
                        w_to_90pct_oracle=hit if hit is not None else "not reached", label="estimate"))
    # detector
    for world in ("D", "C"):
        for Re in (36, 40, 44, 50, 56):
            for arm in ("H", "P1", "P1x"):
                ws = [w for w in (3, 6, 11) if (world, Re, arm, w) in RH]
                if len(ws) < 3:
                    continue
                R = np.stack([RH[(world, Re, arm, w)].mean(0) for w in ws], 1)    # seed-averaged per state
                x = np.array(ws, float)
                xc = x - x.mean()
                slope = (R - R.mean(1, keepdims=True)) @ xc / (xc ** 2).sum()
                bs = slope[idx].mean(1)
                row = dict(world=world, Re=Re, arm=arm, **{f"re_hat_w{w}": float(R[:, i].mean()) for i, w in enumerate(ws)},
                           slope_per_frame=float(slope.mean()), slope_ci95_lo=float(np.quantile(bs, 0.025)),
                           slope_ci95_hi=float(np.quantile(bs, 0.975)), label="estimate (reported only)")
                kH, kO = (world, Re, "H", 11, 0.1, "future"), (world, Re, "O", 11, 0.1, "future")
                if arm == "H" and kH in H and kO in H:
                    short = H[kO][0] - H[kH].mean(0)
                    from scipy.stats import spearmanr
                    rho = spearmanr(slope, short).statistic
                    bsr = [spearmanr(slope[i], short[i]).statistic for i in idx[:500]]
                    row.update(spearman_slope_vs_shortfall=float(rho), spearman_ci95_lo=float(np.nanquantile(bsr, 0.025)),
                               spearman_ci95_hi=float(np.nanquantile(bsr, 0.975)))
                det.append(row)
    # part B
    def hz(panel, arm, seed, variant, lab, e=0.1, start=1):
        f = EV / panel / f"{arm}_s{seed}_{variant}_{lab}.npz"
        if not f.exists():
            return None
        lam = tp[panel]["lam"]
        return score.horizon(np.load(f)["err"].astype(float), lam, DELTA, 10.0, e, start)[0]

    def brow(item, panel, arm, variant, lab, ref=None, extra=None):
        h = hz(panel, arm, 0, variant, lab)
        if h is None:
            return
        m, lo, hi = score.bootstrap_mean(h)
        r = dict(item=item, panel=panel, arm=arm, variant=variant, window=lab, n=len(h), restricted_mean=m, ci95_lo=lo, ci95_hi=hi,
                 label=LABEL.get(arm, "learned") + " (single seed)" if arm in ("H", "L_range", "H_Re_only") else LABEL.get(arm, ""))
        if ref:
            for nm, (rp, ra, rv, rl) in ref.items():
                hr = hz(rp, ra, 0, rv, rl)
                if hr is not None:
                    r[f"ratio_to_{nm}"] = m / hr.mean()
        if extra:
            r.update(extra)
        partB.append(r)

    for world in ("D", "C"):
        for Re in (36, 40, 44, 50, 56):
            p = f"s2_test_Re{Re}_{world}"
            brow("1 train wider", p, "L_range_wide", "std", 11, ref={"O": (p, "O", "std", 11)})
    for world in ("D", "C"):
        for Re in (44, 50):
            p = f"s2_test_Re{Re}_{world}"
            for e_, off in ((8, 3), (5, 6), (2, 9)):
                for arm in ("H", "L_range"):
                    brow("2 straddle", p, arm, "straddle", e_, ref={"O_std": (p, "O", "std", 11)},
                         extra=dict(window_starts_before_tc=off, window_end_after_tc=e_))
            for arm in ("O", "H", "L_range"):
                brow("4 noise 5%", p, arm, "noise5", 11, ref={"O_noise5": (p, "O", "noise5", 11)})
    for case in ("Re44_A1.1", "Re50_A0.9"):
        p = f"s2_test2p_{case}"
        for arm in ("O", "H", "H_Re_only", "L_range"):
            f = EV / p / f"{arm}_s0_2p_11.npz"
            ex = {}
            if f.exists():
                z = np.load(f)
                if "re_hat" in z:
                    ex["re_hat_median"] = float(np.median(z["re_hat"]))
                if "amp_hat" in z:
                    ex["amp_hat_median"] = float(np.median(z["amp_hat"]))
            brow("3 two parameters", p, arm, "2p", 11, ref={"O": (p, "O", "2p", 11), "L_range": (p, "L_range", "2p", 11)}, extra=ex)
    # item 1 ratios H / L_range_wide
    for r in partB:
        if r["item"] == "1 train wider":
            wd, Re = r["panel"].split("_")[-1], int(r["panel"].split("Re")[1].split("_")[0])
            k = (wd, Re, "H", 11, 0.1, "future")
            if k in H:
                r["H_seed_pooled"] = float(H[k].mean())
                r["H_over_L_range_wide"] = float(H[k].mean() / r["restricted_mean"])
    # cost
    for f in sorted(RES.glob("eval_*.json")):
        for k, v in json.loads(f.read_text()).items():
            if isinstance(v, dict):
                cost.append(dict(panel=f.stem[5:], key=k, **{x: v.get(x) for x in ("arm", "seed", "variant", "window", "n",
                                 "wall_seconds_per_state", "solver_steps", "objective_evals", "forecast_steps")}, label="estimate"))
    tr = []
    for d in sorted((config.RUNS / "train").glob("*/info.json")):
        i = json.loads(d.read_text())
        name = d.parent.name
        data = i.get("data", "nominal")            # recorded training-data key (hybrids: nominal Re 40 data)
        ranged = data.startswith("range")
        conds_n, states = (1024, 204800) if ranged else (1, 102400)
        re_range = "30-60" if data.startswith("range_wide") else "34-46" if ranged else "40"
        tr.append(dict(model=name, params=i["params"], steps=i["steps"], batch=i["batch"], train_seconds=i["train_seconds"],
                       best_step=i["best_step"], seed=i.get("seed", 0), training_data=data, training_conditions=conds_n,
                       training_re_range=re_range, training_states=states, label="learned"))
    write("s2_rows.csv", rows, "part A horizons (seed-pooled)")
    write("s2_conditions.csv", conds, "pivot criteria on fresh panels")
    write("s2_outcome.csv", [dict(outcome=outcome, kill_any=any(kill), pass_all=all(ps), middle_all=all(mid), complete=complete,
                                  all_three_seeds=seeds_ok, precedence="KILL -> PASS -> MIDDLE -> otherwise",
                                  label="estimate (frozen outcome rule)")], "outcome")
    write("s2_paired.csv", paired, "paired differences (seed-pooled)")
    write("s2_recovery.csv", rec, "time to 90% of O")
    write("s2_detector.csv", det, "detector")
    write("s2_partB.csv", partB, "part B robustness (reported, not criteria)")
    write("s2_cost.csv", cost, "online cost")
    write("s2_training.csv", tr, "training cost")
    print(outcome)
    for c in conds:
        print(c["criterion"], c["world"], c["Re"], c["value"], c["ci95_lo"], c["ci95_hi"], c["holds"], "screening", c["screening_value"])


if __name__ == "__main__":
    main()
