"""Pivot analysis (pivot/pv_freeze.yaml measurements, outcomes). Writes pivot/results/:
  pv_rows.csv       restricted mean (Lyapunov, physical time) [95%], S(1), S(3), retention (share of O), ratio to L_range
  pv_paired.csv     paired differences a - b with 90/95% intervals and the frozen reading
  pv_outcome.csv    the pre-committed outcome (precedence KILL -> PASS -> MIDDLE -> otherwise) with every condition
  pv_conditions.csv each criterion's value, threshold and result
  pv_recovery.csv   time to 90% of the oracle (tested w)
  pv_detector.csv   window-drift detector: identified Re per w and the per-state least-squares slope of Re_hat on w
                    (mean with a 95% bootstrap interval over states); reported only
  pv_cost.csv       online cost; pv_training.csv training cost (conditions = distinct Re values; states)
Stage-1 World D evaluations (runs/eval) are used for the stage-1 arms at Re 36/40/44/50.
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

RES = config.PKG / "pivot" / "results"
WS, EPS, DELTA = (3, 6, 11, 23), (0.1, 0.3), 0.35
ARMS = ["O", "H", "H_true", "P1x", "L_range", "L0", "L0big", "P1", "persistence"]
LABEL = {"O": "reference", "P1": "reference", "P1x": "reference", "persistence": "reference", "H": "hybrid (learned correction)",
         "H_true": "hybrid (learned correction)", "L_range": "learned", "L0": "learned", "L0big": "learned"}
STAGE1 = {"O", "P1", "P1x", "persistence", "L0", "L_range", "L0big"}


def lam_of(world, Re):
    if world == "D" and Re != 56:
        return json.loads((config.RESULTS / "chaos_gate.json").read_text())[f"Re{Re}"]["lam"]
    return json.loads((RES / f"chaos_gate_{world}.json").read_text())[f"Re{Re}"]["lam"]


def path(world, Re, arm, w):
    if world == "D" and Re != 56 and arm in STAGE1:
        return config.RUNS / "eval" / f"Re{Re}" / f"{arm}_w{w}.npz"
    return config.RUNS / "pivot_eval" / world / f"Re{Re}" / f"{arm}_w{w}.npz"


def reading(pd):
    if pd["diff"] >= 0.25 and pd["ci95"][0] > 0:
        return "b well below a"
    if -pd["diff"] >= 0.25 and pd["ci95"][1] < 0:
        return "a well below b"
    if pd["ci90"][0] >= -0.10 and pd["ci90"][1] <= 0.10:
        return "approximately equal"
    return "no reading"


def write(name, rows, note):
    keys = []
    for r in rows:
        keys += [k for k in r if k not in keys]
    RES.mkdir(parents=True, exist_ok=True)
    with open(RES / name, "w", newline="") as fh:
        fh.write(f"# git_sha={config.git_sha()}; Adapt the Physics pivot; {note}\n")
        wr = csv.DictWriter(fh, fieldnames=keys)
        wr.writeheader()
        wr.writerows(rows)


def main():
    H, Z = {}, {}
    rows, paired, rec, det, cost = [], [], [], [], []
    worlds = {"D": [36, 40, 44, 50, 56], "C": [36, 40, 44, 50, 56]}
    for world, res in worlds.items():
        for Re in res:
            try:
                lam = lam_of(world, Re)
            except (KeyError, FileNotFoundError):
                continue
            for arm in ARMS:
                for w in WS:
                    f = path(world, Re, arm, w)
                    if not f.exists():
                        continue
                    z = np.load(f)
                    Z[(world, Re, arm, w)] = z
                    err = z["err"].astype(np.float64)
                    for e in EPS:
                        H[(world, Re, arm, w, e)] = score.horizon(err, lam, DELTA, 10.0, e, 1)
            for w in WS:
                for e in EPS:
                    O = H.get((world, Re, "O", w, e))
                    LR = H.get((world, Re, "L_range", w, e))
                    for arm in ARMS:
                        if (world, Re, arm, w, e) not in H:
                            continue
                        h, c = H[(world, Re, arm, w, e)]
                        m, lo, hi = score.bootstrap_mean(h)
                        rows.append(dict(world=world, Re=Re, arm=arm, w=w, eps=e, n=len(h), restricted_mean=m, ci95_lo=lo,
                                         ci95_hi=hi, phys_time=m / lam, S1=float(np.mean(~c | (h > 1))),
                                         S3=float(np.mean(~c | (h > 3))), retention=m / O[0].mean() if O else None,
                                         ratio_to_L_range=m / LR[0].mean() if LR else None, lam_test=lam, label=LABEL[arm]))
                    for a, b in (("H", "L_range"), ("H", "O"), ("H", "P1"), ("H_true", "H"), ("H", "L0"), ("H", "L0big"),
                                 ("H", "P1x"), ("L_range", "L0")):
                        if (world, Re, a, w, e) in H and (world, Re, b, w, e) in H:
                            ha, hb = H[(world, Re, a, w, e)][0], H[(world, Re, b, w, e)][0]
                            pd = score.paired_diff(ha, hb)
                            paired.append(dict(world=world, Re=Re, w=w, eps=e, a=a, b=b, n=len(ha), mean_a=float(ha.mean()),
                                               mean_b=float(hb.mean()), ratio=float(ha.mean() / hb.mean()), diff=pd["diff"],
                                               ci90_lo=pd["ci90"][0], ci90_hi=pd["ci90"][1], ci95_lo=pd["ci95"][0],
                                               ci95_hi=pd["ci95"][1], reading=reading(pd), label="estimate"))
            for e in EPS:
                for arm in ARMS:
                    ws = [w for w in WS if (world, Re, arm, w, e) in H and (world, Re, "O", w, e) in H]
                    hit = next((w for w in ws if H[(world, Re, arm, w, e)][0].mean() >= 0.9 * H[(world, Re, "O", w, e)][0].mean()), None)
                    if ws:
                        rec.append(dict(world=world, Re=Re, eps=e, arm=arm, w_tested=",".join(map(str, ws)),
                                        w_to_90pct_oracle=hit if hit is not None else "not reached", label="estimate"))
            for arm in ("H", "P1", "P1x"):
                ws = [w for w in WS if (world, Re, arm, w) in Z]
                if len(ws) < 2:
                    continue
                R = np.stack([Z[(world, Re, arm, w)]["re_hat"] for w in ws], 1)
                x = np.array(ws, float)
                xc = x - x.mean()
                slope = (R - R.mean(1, keepdims=True)) @ xc / (xc ** 2).sum()
                m, lo, hi = score.bootstrap_mean(slope)
                det.append(dict(world=world, Re=Re, arm=arm, w_tested=",".join(map(str, ws)),
                                **{f"re_hat_w{w}": float(R[:, i].mean()) for i, w in enumerate(ws)},
                                slope_per_frame=m, slope_ci95_lo=lo, slope_ci95_hi=hi,
                                slope_per_lyapunov_time=m / (DELTA * lam), label="estimate (reported only)"))
            meta = {}
            for mf in ([config.RESULTS / "eval" / f"Re{Re}.json"] if world == "D" and Re != 56 else []) + \
                    [RES / f"eval_{world}_Re{Re}.json"]:
                if mf.exists():
                    meta.update({k: v for k, v in json.loads(mf.read_text()).items() if isinstance(v, dict)})
            for k, v in meta.items():
                if v.get("arm") in ARMS:
                    cost.append(dict(world=world, Re=Re, arm=v["arm"], w=v["w"], n=v.get("n"),
                                     wall_seconds_per_state=v.get("wall_seconds_per_state"),
                                     solver_steps_identify=v.get("solver_steps"), objective_evals=v.get("objective_evals"),
                                     forecast_steps=v.get("forecast_steps"), gradient_steps=v.get("gradient_steps"),
                                     label="estimate"))
    # outcome at w 11, eps 0.1
    g = lambda wd, Re, arm: float(H[(wd, Re, arm, 11, 0.1)][0].mean()) if (wd, Re, arm, 11, 0.1) in H else None  # noqa: E731
    cond = []

    def add(name, wd, Re, value, thr, ok):
        cond.append(dict(criterion=name, world=wd, Re=Re, value=value, threshold=thr, holds=ok, label="estimate"))
        return ok

    def ratio(wd, Re, a, b):
        x, y = g(wd, Re, a), g(wd, Re, b)
        return None if x is None or y is None else x / y

    kill = []
    for wd in ("D", "C"):
        for Re in (50, 56):
            r = ratio(wd, Re, "H", "L_range")
            kill.append(add("KILL: H/L_range <= 1.0", wd, Re, r, 1.0, r is not None and r <= 1.0))
    r = ratio("D", 50, "H", "O")
    kill.append(add("KILL: H/O < 0.70 at Re 50 (D)", "D", 50, r, 0.70, r is not None and r < 0.70))
    ps = []
    for Re in (36, 44, 50, 56):
        r = ratio("D", Re, "H", "O")
        ps.append(add("PASS: H/O >= 0.85 (D)", "D", Re, r, 0.85, r is not None and r >= 0.85))
    for Re in (36, 50, 56):
        r = ratio("D", Re, "H", "L_range")
        ps.append(add("PASS: H/L_range >= 1.5 (D)", "D", Re, r, 1.5, r is not None and r >= 1.5))
    best = max([v for v in (g("D", 40, "L0"), g("D", 40, "L0big")) if v is not None], default=None)
    r = None if best is None or g("D", 40, "H") is None else g("D", 40, "H") / best
    ps.append(add("PASS: H/max(L0, L0big) >= 0.95 at Re 40 (D)", "D", 40, r, 0.95, r is not None and r >= 0.95))
    for Re in (50, 56):
        r = ratio("C", Re, "H", "O")
        ps.append(add("PASS: H/O >= 0.70 (C)", "C", Re, r, 0.70, r is not None and r >= 0.70))
        r = ratio("C", Re, "H", "L_range")
        ps.append(add("PASS: H/L_range >= 1.2 (C)", "C", Re, r, 1.2, r is not None and r >= 1.2))
    mid = []
    for wd in ("D", "C"):
        for Re in (50, 56):
            r = ratio(wd, Re, "H", "L_range")
            mid.append(add("MIDDLE: H/L_range >= 1.3", wd, Re, r, 1.3, r is not None and r >= 1.3))
    complete = all(c["value"] is not None for c in cond)
    outcome = ("KILL" if any(kill) else "PASS (headline A)" if all(ps) else "MIDDLE (headline B)" if all(mid)
               else "OTHERWISE (Todd decides)")
    if not complete:
        outcome += " [INCOMPLETE: some criteria missing]"
    write("pv_rows.csv", rows, "horizons")
    write("pv_paired.csv", paired, "paired differences a - b")
    write("pv_conditions.csv", cond, "pre-committed criteria at w 11, eps 0.1, 300 states")
    write("pv_outcome.csv", [dict(outcome=outcome, kill_any=any(kill), pass_all=all(ps), middle_all=all(mid),
                                  complete=complete, precedence="KILL -> PASS -> MIDDLE -> otherwise",
                                  label="estimate (frozen outcome rule)")], "outcome")
    write("pv_recovery.csv", rec, "time to 90% of O")
    if det:
        write("pv_detector.csv", det, "window-drift detector (reported only)")
    write("pv_cost.csv", cost, "online cost")
    tr = []
    for arm, conds, states in (("H_D", 1, 102400), ("H_C", 1, 102400), ("L0", 1, 102400), ("L0_C", 1, 102400),
                               ("L0big", 1, 102400), ("L_range", 1024, 204800), ("L_range_C", 1024, 204800)):
        f = config.RUNS / "train" / arm / "info.json"
        if f.exists():
            i = json.loads(f.read_text())
            tr.append(dict(model=arm, params=i["params"], steps=i["steps"], batch=i["batch"], train_seconds=i["train_seconds"],
                           best_step=i["best_step"], training_conditions=conds, training_states=states, label="learned"))
    write("pv_training.csv", tr, "training cost")
    print(outcome)
    for c in cond:
        print(c)


if __name__ == "__main__":
    main()
