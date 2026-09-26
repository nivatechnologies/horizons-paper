"""Adapt the Physics stage-1 analysis (ap_freeze.yaml scoring, readings, kill_rule). Reads runs/eval/Re*/<arm>_w<w>.npz,
results/eval/Re*.json, results/chaos_gate.json, runs/train/*/info.json. Writes results/:
  ap_rows.csv       restricted mean (Lyapunov, physical time) with 95% intervals, S(1), S(3), per arm x Re x w x eps
                    (panel 'all' = every state the arm ran on; 'first100' = the kill-rule subset)
  ap_paired.csv     paired differences (a - b) per state with 90/95% intervals and the frozen reading
  ap_kill.csv       I*, A*, ratios per Re x w x eps on the first 100 states (+ 300-state ratio without L_ft); the
                    primary cell Re 44, eps 0.1, w 11; pass / kill / between; the no-drift flag
  ap_recovery.csv   time to 90% of the oracle per arm x Re x eps
  ap_identify.csv   P1 / P1x Re estimates (mean, SD, median absolute error) per Re x w
  ap_cost.csv       online cost per arm x Re x w; training cost per learned model
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tokens_horizon"))
from ap import config  # noqa: E402
from th import score  # noqa: E402

WS = (3, 6, 11, 23)
EPS = (0.1, 0.3)
DELTA = 0.35
ARMS = ["O", "P1", "P1x", "L_param_P1", "L_param_true", "L_range", "L_ft", "L0big", "L0", "P0", "persistence"]
LABEL = {"O": "reference", "P0": "reference", "P1": "reference", "P1x": "reference", "persistence": "reference",
         "L0": "learned", "L0big": "learned", "L_range": "learned", "L_param_P1": "learned", "L_param_true": "learned",
         "L_ft": "learned"}
ROLE = {"O": "oracle (upper reference)", "P0": "null (nominal solver)", "persistence": "null", "P1": "identification",
        "P1x": "identification diagnostic (drag known)", "L_param_P1": "identification (hybrid)",
        "L_param_true": "hybrid diagnostic (true Re)", "L_range": "opponent (context adaptation)",
        "L_ft": "opponent (fine-tuning)", "L0big": "opponent (scale)", "L0": "diagnostic (frozen nominal)"}
PAIRS = [("P1", "L_range"), ("P1", "L0big"), ("P1", "L_ft"), ("L_param_P1", "L_range"), ("L_param_P1", "L0big"),
         ("L_param_P1", "L_ft"), ("O", "P1"), ("O", "L_param_P1"), ("P1", "P0"), ("P1x", "P1"),
         ("L_param_true", "L_param_P1"), ("L_range", "L0"), ("L0big", "L0"), ("L_ft", "L0"), ("L_range", "L0big")]


def reading(pd):
    m = config.freeze()["readings"]
    lo90, hi90 = pd["ci90"]
    lo95, hi95 = pd["ci95"]
    if pd["diff"] >= 0.25 and lo95 > 0:
        return "b well below a"
    if -pd["diff"] >= 0.25 and hi95 < 0:
        return "a well below b"
    if lo90 >= -0.10 and hi90 <= 0.10:
        return "approximately equal"
    return "no reading"


def write(name, rows, note):
    keys = []
    for r in rows:
        keys += [k for k in r if k not in keys]
    config.RESULTS.mkdir(parents=True, exist_ok=True)
    with open(config.RESULTS / name, "w", newline="") as fh:
        fh.write(f"# git_sha={config.git_sha()}; Adapt the Physics stage 1; {note}\n")
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)


def main():
    cg = json.loads((config.RESULTS / "chaos_gate.json").read_text())
    res = sorted(int(p.name[2:]) for p in (config.RUNS / "eval").glob("Re*"))
    H = {}
    rows, paired, kill, rec, ident, cost = [], [], [], [], [], []
    for Re in res:
        lam = cg[f"Re{Re}"]["lam"]
        meta = json.loads((config.RESULTS / "eval" / f"Re{Re}.json").read_text())
        for arm in ARMS:
            for w in WS:
                f = config.RUNS / "eval" / f"Re{Re}" / f"{arm}_w{w}.npz"
                if not f.exists():
                    continue
                z = np.load(f)
                err = z["err"].astype(np.float64)
                for e in EPS:
                    h, c = score.horizon(err, lam, DELTA, 10.0, e, 1)
                    H[(Re, arm, w, e)] = (h, c)
                    for panel, sl in (("all", slice(None)), ("first100", slice(0, 100))):
                        hh, cc = h[sl], c[sl]
                        m, lo, hi = score.bootstrap_mean(hh)
                        rows.append(dict(Re=Re, arm=arm, role=ROLE[arm], w=w, eps=e, panel=panel, n=len(hh),
                                         restricted_mean=m, ci95_lo=lo, ci95_hi=hi, phys_time=m / lam,
                                         phys_ci95_lo=lo / lam, phys_ci95_hi=hi / lam,
                                         S1=float(np.mean(~cc | (hh > 1))), S3=float(np.mean(~cc | (hh > 3))),
                                         frac_no_cross=float(1 - cc.mean()), lam_test=lam, label=LABEL[arm]))
                mt = meta.get(f"{arm}_w{w}", {})
                cost.append(dict(Re=Re, arm=arm, w=w, n=mt.get("n"), wall_seconds_per_state=mt.get("wall_seconds_per_state"),
                                 identify_seconds_per_state=mt.get("identify_seconds_per_state"),
                                 solver_steps_identify=mt.get("solver_steps"), objective_evals=mt.get("objective_evals"),
                                 gradient_steps=mt.get("gradient_steps"), forecast_steps=mt.get("forecast_steps"),
                                 label="estimate"))
                if arm in ("P1", "P1x"):
                    rh = z["re_hat"]
                    ident.append(dict(Re=Re, arm=arm, w=w, n=len(rh), re_hat_mean=float(rh.mean()),
                                      re_hat_sd=float(rh.std(ddof=1)), re_hat_median=float(np.median(rh)),
                                      median_abs_error=float(np.median(np.abs(rh - Re))), frac_at_bounds=float(
                                          np.mean((rh < 25.5) | (rh > 69.5))), label="estimate"))
        for w in WS:
            for e in EPS:
                for a, b in PAIRS:
                    if (Re, a, w, e) not in H or (Re, b, w, e) not in H:
                        continue
                    ha, hb = H[(Re, a, w, e)][0], H[(Re, b, w, e)][0]
                    n = min(len(ha), len(hb))
                    pd = score.paired_diff(ha[:n], hb[:n])
                    paired.append(dict(Re=Re, w=w, eps=e, a=a, b=b, n=n, mean_a=float(ha[:n].mean()),
                                       mean_b=float(hb[:n].mean()), diff=pd["diff"], ci90_lo=pd["ci90"][0],
                                       ci90_hi=pd["ci90"][1], ci95_lo=pd["ci95"][0], ci95_hi=pd["ci95"][1],
                                       reading=reading(pd), label="estimate"))
                # kill quantities
                g = lambda arm, n=100: float(H[(Re, arm, w, e)][0][:n].mean()) if (Re, arm, w, e) in H else None
                ci = {k: g(k) for k in ("P1", "L_param_P1", "L_range", "L_ft", "L0big")}
                if None in (ci["P1"], ci["L_param_P1"], ci["L_range"]):
                    continue
                I = max(ci["P1"], ci["L_param_P1"])
                Iarm = "P1" if ci["P1"] >= ci["L_param_P1"] else "L_param_P1"
                opp = {k: v for k, v in ci.items() if k in ("L_range", "L_ft", "L0big") and v is not None}
                Aarm = max(opp, key=opp.get)
                A = opp[Aarm]
                i3 = max(g("P1", 300), g("L_param_P1", 300))
                o3 = {k: g(k, 300) for k in ("L_range", "L0big") if g(k, 300) is not None}
                kill.append(dict(Re=Re, w=w, eps=e, n=100, P1=ci["P1"], L_param_P1=ci["L_param_P1"],
                                 L_range=ci["L_range"], L_ft=ci["L_ft"], L0big=ci["L0big"], O=g("O"), I_star=I,
                                 I_arm=Iarm, A_star=A, A_arm=Aarm, ratio=I / A, opponents_present=",".join(sorted(opp)),
                                 ratio_300_without_Lft=i3 / max(o3.values()), label="estimate"))
        for e in EPS:
            for arm in ARMS:
                ws = [w for w in WS if (Re, arm, w, e) in H and (Re, "O", w, e) in H]
                hit = None
                for w in ws:
                    ha = H[(Re, arm, w, e)][0]
                    ho = H[(Re, "O", w, e)][0][:len(ha)]
                    if ha.mean() >= 0.9 * ho.mean():
                        hit = w
                        break
                if ws:
                    rec.append(dict(Re=Re, eps=e, arm=arm, w_tested=",".join(map(str, ws)),
                                    w_to_90pct_oracle=hit if hit is not None else "not reached", label="estimate"))
    # kill rule on the primary cell
    kp = {(k["Re"], k["w"], k["eps"]): k for k in kill}
    verdict = []
    if (44, 11, 0.1) in kp:
        k44 = kp[(44, 11, 0.1)]
        k50 = kp.get((50, 11, 0.1))
        k40 = kp.get((40, 11, 0.1))
        passed = k44["I_star"] >= 2 * k44["A_star"] and k50 is not None and k50["I_star"] >= 2 * k50["A_star"]
        killed = k44["A_star"] >= 0.75 * k44["I_star"]
        outcome = "KILL" if killed else ("PASS" if passed else "IN BETWEEN (Todd decides)")
        flag = k40 is not None and k40["ratio"] >= k44["ratio"]
        verdict.append(dict(cell="Re 44, eps 0.1, w 11, first 100 states", I_star=k44["I_star"], I_arm=k44["I_arm"],
                            A_star=k44["A_star"], A_arm=k44["A_arm"], ratio_44=k44["ratio"],
                            ratio_50=None if k50 is None else k50["ratio"], ratio_40=None if k40 is None else k40["ratio"],
                            pass_condition=passed, kill_condition=killed, outcome=outcome,
                            flag_no_drift_ratio_ge_drift=flag, opponents_present=k44["opponents_present"],
                            label="estimate (frozen kill rule)"))
    # training cost
    tr = []
    for d in sorted((config.RUNS / "train").glob("*/info.json")):
        i = json.loads(d.read_text())
        tr.append(dict(model=i["arm"], params=i["params"], steps=i["steps"], batch=i["batch"],
                       train_seconds=i["train_seconds"], best_step=i["best_step"], best_val=i["best_val"], label="learned"))
    write("ap_rows.csv", rows, "horizons")
    write("ap_paired.csv", paired, "paired differences a - b; frozen readings")
    write("ap_kill.csv", kill, "kill-rule quantities, first 100 states")
    if verdict:
        write("ap_kill_verdict.csv", verdict, "frozen kill rule on the primary cell")
    write("ap_recovery.csv", rec, "time to 90% of oracle")
    if ident:
        write("ap_identify.csv", ident, "identified Re")
    write("ap_cost.csv", cost, "online cost")
    if tr:
        write("ap_training.csv", tr, "training cost")
    for v in verdict:
        print(v)


if __name__ == "__main__":
    main()
