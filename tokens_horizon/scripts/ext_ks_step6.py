"""Post-freeze extension, KS step 6: D_eff, decode-and-integrate slopes, A3 thresholds with survival (ext_freeze.yaml
ks.e3.d_eff / di_slope / thresholds; Amendment 1 A3, A4; Amendment 2 B4).

D_eff = -1/slope of log2(delta) against the (total) rate, delta = RMS error of exact decoding on the held-out
calibration split; 95% interval by bootstrap over held-out trajectories (seed 777, 2,000 reps; per-trajectory mean
squared errors from scripts/ext_ks_adequacy.py). Whole-state ks22: rates {6,8,10,12} and {8,...,16} even. Patch:
per (system, P), total rate P*b over b in {8,...,16}; D_eff(P) estimates P * d_patch (never pooled over P).
DI slope: least squares of the decode-and-integrate restricted mean (primary Delta, eps 0.3, future) against total
bits, per system and family (patch: per P); 95% interval by bootstrap over panel states (same states at every rate).
Thresholds (A3): per family (system, family, P) and tau in {1, 3, 10} Lyapunov times, for the bound (whole and patch)
and, as references, decode-and-integrate and persistence: the smallest tested nominal rate whose restricted mean
reaches tau; monotone flag (every higher tested rate reaches it; exceptions listed); the smallest tested rate whose
lower 95% limit reaches tau; else 'not reached within the tested grid'. Bound rows carry S_out(1, 3, 10).
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from th import config   # noqa: E402
from th import ks as K   # noqa: E402

R = config.RUNS / "ext" / "ks"
OUTD = config.RESULTS / "ext" / "ks"
BOOT = dict(seed=777, reps=2000)


def write_csv(fn, rows):
    keys = []
    for r in rows:
        for k in r:
            if k not in keys:
                keys.append(k)
    with open(fn, "w", newline="") as fh:
        fh.write(f"# git_sha={config.git_sha()}; POST-FREEZE EXTENSION\n")
        w = csv.DictWriter(fh, keys)
        w.writeheader()
        w.writerows(rows)


def slope(x, y):
    A = np.stack([np.ones_like(x), x], 1)
    return np.linalg.lstsq(A, y, rcond=None)[0][1]


def deff(names, rates):
    e2 = np.stack([np.load(R / f"heldout_err2_{n}.npy") for n in names], 1)     # (n_traj, rates)
    x = np.asarray(rates, float)
    pt = -1.0 / slope(x, np.log2(np.sqrt(e2.mean(0))))
    rng = np.random.default_rng(BOOT["seed"])
    bs = []
    for _ in range(BOOT["reps"]):
        i = rng.integers(0, len(e2), len(e2))
        bs.append(-1.0 / slope(x, np.log2(np.sqrt(e2[i].mean(0)))))
    return dict(d_eff=float(pt), ci95_lo=float(np.quantile(bs, 0.025)), ci95_hi=float(np.quantile(bs, 0.975)),
                delta_heldout=[float(v) for v in np.sqrt(e2.mean(0))], n_heldout_traj=int(len(e2)))


def families():
    fam = {("ks22", "whole", 1): [(b, f"ks22_whole_b{b}") for b in range(4, 17)]}
    for s in ("ks22", "ks100"):
        for P in (8, 16, 32):
            fam[(s, "patch", P)] = [(P * b, f"{s}_patch_P{P}_b{b}") for b in (8, 10, 12, 14, 16)]
        fam[(s, "rvq", None)] = [(8 * k, f"{s}_rvq_s{k}") for k in (1, 2, 3, 4)]
    return fam


def e3_rows(name):
    f = R / "e3" / f"{name}.json"
    return json.loads(f.read_text())["rows"] if f.exists() else None


def main():
    out = dict(label="post-freeze extension", git_sha=config.git_sha())
    # ---------------- D_eff
    drows = []
    for key, sets in (("whole_6_12", [6, 8, 10, 12]), ("whole_8_16_even", [8, 10, 12, 14, 16])):
        r = deff([f"ks22_whole_b{b}" for b in sets], sets)
        drows.append(dict(system="ks22", family="whole", P=1, fit=key, rates=" ".join(map(str, sets)), **r))
    for s in ("ks22", "ks100"):
        for P in (8, 16, 32):
            bs = [8, 10, 12, 14, 16]
            r = deff([f"{s}_patch_P{P}_b{b}" for b in bs], [P * b for b in bs])
            dp = K.ks_spec(s)["N"] // P
            drows.append(dict(system=s, family="patch", P=P, fit="b_8_16_even", rates=" ".join(str(P * b) for b in bs),
                              d_patch=dp, P_times_d_patch=P * dp, **r))
    for r in drows:
        r["delta_heldout"] = " ".join(f"{v:.6g}" for v in r["delta_heldout"])
    write_csv(OUTD / "d_eff.csv", drows)
    out["d_eff"] = drows
    # ---------------- DI slopes and thresholds
    srows, trows = [], []
    rng = np.random.default_rng(BOOT["seed"])
    for (s, fam, P), members in families().items():
        d = float(K.ks_spec(s)["primary_delta"])
        present = [(rate, n) for rate, n in members if (R / "e3" / f"{n}.npz").exists()]
        if len(present) < len(members):
            print("missing", s, fam, P, [n for r_, n in members if (r_, n) not in present])
        # DI slope
        Hs, rates = [], []
        for rate, n in present:
            z = np.load(R / "e3" / f"{n}.npz")
            k = f"di_d{d:g}_eps0.3_future_H"
            if k in z.files:
                Hs.append(z[k])
                rates.append(rate)
        if len(rates) >= 2:
            Hm = np.stack(Hs, 0)
            x = np.asarray(rates, float)
            pt = slope(x, Hm.mean(1))
            n = Hm.shape[1]
            bs = [slope(x, Hm[:, rng.integers(0, n, n)].mean(1)) for _ in range(BOOT["reps"])]
            srows.append(dict(system=s, family=fam, P=P, delta=d, eps=0.3, start="future", rates=" ".join(map(str, rates)),
                              di_slope_per_bit=float(pt), ci95_lo=float(np.quantile(bs, 0.025)),
                              ci95_hi=float(np.quantile(bs, 0.975)), label="reference"))
        # thresholds
        for kind in ("bound", "decode_and_integrate", "persistence"):
            table = []
            for rate, n in present:
                rows = e3_rows(n)
                sel = [r for r in rows if r["kind"] == kind and r["delta"] == d and r["eps"] == 0.3 and r["start"] == "future"]
                if sel:
                    table.append((rate, sel[0]))
            if not table:
                continue
            table.sort(key=lambda t: t[0])
            for tau in (1.0, 3.0, 10.0):
                reach = [rate for rate, r in table if r["restricted_mean"] >= tau]
                reach_lo = [rate for rate, r in table if r["ci95_lo"] >= tau]
                row = dict(system=s, family=fam, P=P, kind=kind, label="bound" if kind == "bound" else "reference",
                           delta=d, eps=0.3, start="future", tau=tau, tested_rates=" ".join(str(t[0]) for t in table))
                if reach:
                    r0 = reach[0]
                    higher = [rate for rate, _ in table if rate > r0]
                    exc = [rate for rate in higher if rate not in reach]
                    rr = dict(table)[r0]
                    row.update(smallest_tested_rate=r0, restricted_mean_at_rate=rr["restricted_mean"],
                               ci95_lo_at_rate=rr["ci95_lo"], monotone=not exc, monotone_exceptions=" ".join(map(str, exc)))
                    if kind == "bound":
                        row.update(S1=rr.get("S1"), S3=rr.get("S3"), S10=rr.get("S10"), p0=rr.get("p0"))
                else:
                    row.update(smallest_tested_rate="not reached within the tested grid")
                row["smallest_tested_rate_lower95"] = reach_lo[0] if reach_lo else "not reached within the tested grid"
                trows.append(row)
    write_csv(OUTD / "di_slopes.csv", srows)
    write_csv(OUTD / "thresholds.csv", trows)
    out["di_slopes"] = srows
    out["thresholds"] = trows
    (OUTD / "step6.json").write_text(json.dumps(out, indent=1, default=str))
    print("d_eff", [(r["system"], r["family"], r["P"], r["fit"], round(r["d_eff"], 2)) for r in drows])


if __name__ == "__main__":
    main()
