"""Post-freeze extension, Kolmogorov E3 summaries: main table, D_eff per layout, decode-and-integrate slope, A3
thresholds and the '>= 2^12 codes, >= 64 tokens' bound reading (descriptive). Reads runs/ext/kolmo/e3/*.json|npz,
results/ext/kolmo/calibration_adequacy.csv and runs/ext/kolmo/heldout_err2_*.npy.

  D_eff (per layout, never pooled): -1/slope(log2 delta against total rate P*b) over b in {8,...,16}, delta = RMS
    exact-decoding error on the held-out calibration split; 95% interval by bootstrap over the 64 held-out
    trajectories (seed 777, 2,000 reps). Residual VQ is reported as a supplementary family (rates 8..32).
  DI slope: least-squares decode-and-integrate restricted mean (eps 0.3, future frames) against total bits per frame,
    per family, at every Delta (primary 0.35); 95% interval by bootstrap over panel states (seed 777, 2,000 reps).
  Thresholds (Amendment 1 A3): per family, quantity (bound; DI and persistence as references), Delta and threshold
    tau in {1, 3, 10} Lyapunov times, eps 0.3 future: smallest tested nominal rate with restricted mean >= tau;
    monotone flag (exceptions listed); smallest tested rate whose lower 95% limit >= tau; else 'not reached within
    the tested grid'. These are the smallest tested rates for this tokenizer family, not minimum bit requirements.

Usage: python scripts/ext_kolmo_summary.py
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from th import config   # noqa: E402
from th import kolmo_eval as E   # noqa: E402

HDR = None


def write_csv(name, rows, keys):
    with open(E.RES / name, "w", newline="") as fh:
        fh.write(HDR)
        w = csv.DictWriter(fh, keys, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def read_csv(name):
    with open(E.RES / name) as fh:
        fh.readline()
        return list(csv.DictReader(fh))


def main():
    global HDR
    HDR = f"# git_sha={config.git_sha()}; POST-FREEZE EXTENSION\n"
    recs = {f.stem: json.loads(f.read_text()) for f in sorted((E.RUNS / "e3").glob("*.json"))}
    rows = [r for v in recs.values() for r in v["rows"]]
    adq = {r["codebook"]: r for r in read_csv("calibration_adequacy.csv")} if (E.RES / "calibration_adequacy.csv").exists() else {}
    deltas = [float(d) for d in E.spec()["frame_intervals"]]

    def fam(r):
        return r["layout"] if r["family"] == "patch" else "rvq"

    # ---------------- main table (eps 0.3, future frames)
    main_rows = []
    for name, v in recs.items():
        for d in deltas:
            sel = {r["kind"]: r for r in v["rows"] if r["delta"] == d and r["eps"] == 0.3 and r["start"] == "future"}
            any_ = next(iter(sel.values()))
            a = adq.get(name, {})
            o = dict(tokenizer=name, family=fam(any_), P=any_["P"], b=any_["b"], total_bits=any_["total_bits"], delta=d,
                     distortion_heldout_over_sigmaA=a.get("delta_heldout_over_sigmaA"),
                     distortion_fit_over_sigmaA=a.get("delta_fit_over_sigmaA"))
            for k, tag in (("bound", "bound"), ("decode_and_integrate", "di"), ("persistence", "persistence")):
                if k in sel:
                    r = sel[k]
                    o.update({f"{tag}_mean": r["restricted_mean"], f"{tag}_lo": r["ci95_lo"], f"{tag}_hi": r["ci95_hi"],
                              f"{tag}_no_cross": r["frac_no_cross"]})
                    if k == "bound":
                        o.update(p0=r["p0"], S1=r["S1"], S3=r["S3"], S10=r["S10"])
            main_rows.append(o)
    main_rows.sort(key=lambda o: (o["family"], o["total_bits"], o["delta"]))
    keys = ["tokenizer", "family", "P", "b", "total_bits", "delta", "distortion_heldout_over_sigmaA",
            "distortion_fit_over_sigmaA", "bound_mean", "bound_lo", "bound_hi", "bound_no_cross", "p0", "S1", "S3",
            "S10", "di_mean", "di_lo", "di_hi", "di_no_cross", "persistence_mean", "persistence_lo", "persistence_hi",
            "persistence_no_cross"]
    write_csv("e3_main_eps0.3_future.csv", main_rows, keys)

    # ---------------- D_eff per layout (held-out distortion, bootstrap over held-out trajectories)
    deff = []
    rng = np.random.default_rng(777)
    fams = {}
    for name in adq:
        if name.endswith("_half"):
            continue
        a = adq[name]
        f = a["layout"] if a["family"] == "patch" else "rvq"
        fams.setdefault(f, []).append((int(a["total_bits"]), name))
    for f, lst in sorted(fams.items()):
        lst.sort()
        R = np.array([x[0] for x in lst], float)
        E2 = np.stack([np.load(E.RUNS / f"heldout_err2_{x[1]}.npy") for x in lst])       # (rates, n_traj)
        y = np.log2(np.sqrt(E2.mean(1)))
        s = np.polyfit(R, y, 1)[0]
        nt = E2.shape[1]
        bs = []
        for _ in range(2000):
            i = rng.integers(0, nt, nt)
            bs.append(-1 / np.polyfit(R, np.log2(np.sqrt(E2[:, i].mean(1))), 1)[0])
        deff.append(dict(family=f, rates=" ".join(str(int(x)) for x in R), slope_log2delta_per_bit=float(s),
                         D_eff=float(-1 / s), ci95_lo=float(np.quantile(bs, 0.025)), ci95_hi=float(np.quantile(bs, 0.975)),
                         heldout_trajectories=int(nt),
                         note="D_eff(P) estimates P*d_patch-type dimension per layout; never pooled" if f != "rvq"
                         else "supplementary (residual VQ, whole-state)"))
    write_csv("d_eff.csv", deff, ["family", "rates", "slope_log2delta_per_bit", "D_eff", "ci95_lo", "ci95_hi",
                                  "heldout_trajectories", "note"])

    # ---------------- DI slope per family and Delta
    slopes = []
    byfam = {}
    for name, v in recs.items():
        r0 = v["rows"][0]
        byfam.setdefault(fam(r0), []).append((r0["total_bits"], name))
    for f, lst in sorted(byfam.items()):
        lst.sort()
        R = np.array([x[0] for x in lst], float)
        if len(R) < 2:
            continue
        for d in deltas:
            Hs = np.stack([np.load(E.RUNS / "e3" / f"{x[1]}.npz")[f"di_d{d:g}_eps0.3_future_H"] for x in lst])
            s = np.polyfit(R, Hs.mean(1), 1)
            n = Hs.shape[1]
            rng = np.random.default_rng(777)
            bs = [np.polyfit(R, Hs[:, i].mean(1), 1)[0] for i in (rng.integers(0, n, n) for _ in range(2000))]
            slopes.append(dict(family=f, delta=d, rates=" ".join(str(int(x)) for x in R),
                               slope_lyap_per_bit=float(s[0]), intercept=float(s[1]),
                               ci95_lo=float(np.quantile(bs, 0.025)), ci95_hi=float(np.quantile(bs, 0.975)), primary=d == 0.35))
    write_csv("di_slope.csv", slopes, ["family", "delta", "primary", "rates", "slope_lyap_per_bit", "intercept",
                                       "ci95_lo", "ci95_hi"])

    # ---------------- A3 thresholds
    th = []
    for f, lst in sorted(byfam.items()):
        lst.sort()
        for kind in ("bound", "decode_and_integrate", "persistence"):
            for d in deltas:
                pts = []
                for bits, name in lst:
                    r = [x for x in recs[name]["rows"] if x["kind"] == kind and x["delta"] == d and x["eps"] == 0.3
                         and x["start"] == "future"]
                    if r:
                        pts.append((bits, r[0]["restricted_mean"], r[0]["ci95_lo"]))
                if not pts:
                    continue
                for tau in (1.0, 3.0, 10.0):
                    reach = [p for p in pts if p[1] >= tau]
                    o = dict(family=f, quantity=kind, label="bound" if kind == "bound" else "reference", delta=d, eps=0.3,
                             start="future", tau=tau, tested_rates=" ".join(str(p[0]) for p in pts))
                    if reach:
                        r0 = reach[0][0]
                        exc = [p[0] for p in pts if p[0] > r0 and p[1] < tau]
                        o.update(smallest_tested_rate=r0, monotone=not exc, exceptions=" ".join(map(str, exc)))
                    else:
                        o.update(smallest_tested_rate="not reached within the tested grid", monotone="", exceptions="")
                    lo = [p for p in pts if p[2] >= tau]
                    o["smallest_rate_lower95"] = lo[0][0] if lo else "not reached within the tested grid"
                    th.append(o)
    write_csv("thresholds_a3.csv", th, ["family", "quantity", "label", "delta", "eps", "start", "tau", "tested_rates",
                                        "smallest_tested_rate", "monotone", "exceptions", "smallest_rate_lower95"])

    # ---------------- bound reading (descriptive): below 1 Lyapunov time at >= 2^12 codes and >= 64 tokens?
    cand = [o for o in main_rows if o["family"] in ("8x8", "16x16") and o["b"] >= 12 and o.get("bound_mean") is not None]
    below = [o for o in cand if o["bound_mean"] < 1.0]
    reading = dict(label="bound; descriptive only (EXT_FREEZE readings)", eps=0.3, start="future",
                   configurations_tested=[(o["tokenizer"], o["delta"], o["bound_mean"]) for o in cand],
                   below_one_lyapunov_time="yes" if below else ("no" if cand else "not determinable"),
                   configurations_below=[(o["tokenizer"], o["delta"], o["bound_mean"]) for o in below],
                   git_sha=config.git_sha())
    (E.RES / "bound_reading_2p12_64tokens.json").write_text(json.dumps(reading, indent=1))
    print("main rows", len(main_rows), "deff", len(deff), "slopes", len(slopes), "thresholds", len(th))


if __name__ == "__main__":
    main()
