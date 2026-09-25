"""Figure F8 (post-freeze extension): reviewer controls on Lorenz-63. No learned KS cell exists (E4: no tested
configuration satisfying the size requirements had a validation restricted-mean support horizon below one Lyapunov
time), so F8 shows the controls only.

(a) Probe control (E5.1): horizon of the MLP probe on trained A, on untrained A (same initial weights), and a
    token-history MLP. Pooled seeds, 95% intervals.
(b) Ties with the output-support bound at 4 bits (Amendment 2 B4): P(VPT = T_out | Delta < T_out <= W) for A,
    snapped B, persistence and a random-code forecaster.
(c) B, B snapped to its nearest prototype (A8.1) and the bound at 4 bits.
(d) Larger and longer model (E5.3) against the frozen size, Delta = 0.05.
Greyscale-safe: categories by marker shape, fill and hatching; direct legends. Primary score (eps 0.3, future frames).
"""
import csv
import sys
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from th import config  # noqa: E402

R = config.RESULTS / "ext"
OUT = config.FIGS / "F8_controls"


def rd(name):
    return list(csv.DictReader(l for l in open(R / name) if not l.startswith("#")))


def main():
    plt.rcParams.update({"font.size": 8, "axes.linewidth": 0.6, "font.family": "DejaVu Sans"})
    fig, ax = plt.subplots(2, 2, figsize=(7.2, 6.0), constrained_layout=True)
    out = []
    # (a) probe control
    pc = [r for r in rd("e5_probe_control.csv") if r["kind"] == "pooled"]
    cells = ["b4_D0.02", "b4_D0.05", "b4_D0.1", "b6_D0.02"]
    styles = [("trained_mlp", "o", "k", "trained-A MLP probe"), ("untrained_mlp", "o", "white", "untrained-A MLP probe"),
              ("tokhist", "s", "k", "token-history MLP")]
    a = ax[0, 0]
    for i, (f, m, fc, lab) in enumerate(styles):
        ys, lo, hi = [], [], []
        for c in cells:
            r = [x for x in pc if x["cell"] == c and x["forecaster"] == f][0]
            ys.append(float(r["H_restricted_mean"]))
            lo.append(float(r["ci95_lo"]))
            hi.append(float(r["ci95_hi"]))
            out.append(dict(panel="a", cell=c, series=f, value=ys[-1], ci95_lo=lo[-1], ci95_hi=hi[-1], label="learned"))
        x = np.arange(len(cells)) + (i - 1) * 0.18
        ys, lo, hi = map(np.array, (ys, lo, hi))
        a.errorbar(x, ys, yerr=[ys - lo, hi - ys], marker=m, ls="none", color="k", mfc=fc, ms=5, capsize=2, label=lab)
    a.set_xticks(range(len(cells)))
    a.set_xticklabels([c.replace("_D", ", Δ ").replace("b", "") + "" for c in cells], fontsize=6)
    a.set_xlabel("bits, Δ")
    a.set_ylabel("restricted mean horizon (Lyapunov times)")
    a.set_title("(a) probe control", fontsize=8)
    a.legend(fontsize=6, frameon=False)
    # (b) ties at 4 bits
    tb = rd("e5_tie_baselines.csv")
    deltas = ["b4_D0.02", "b4_D0.05", "b4_D0.1"]
    sn = [r for r in rd("e5_b_snapped.csv") if r["score"] == "eps0.3_future" and r["row"] == "B_snapped"]
    b = ax[0, 1]
    series = [("A", "0-2 pooled", "^", "k", "A (seeds pooled)"), ("persistence", "", "x", "k", "persistence"),
              ("random_code", "draws 0-4 averaged", "v", "white", "random-code")]
    for f, seed, m, fc, lab in series:
        ys, lo, hi = [], [], []
        for c in deltas:
            r = [x for x in tb if x["cell"] == c and x["forecaster"] == f and x["seed"] == seed][0]
            ys.append(float(r["tie_given_obs_failure"]))
            lo.append(float(r["tie_ci95_lo"]))
            hi.append(float(r["tie_ci95_hi"]))
            out.append(dict(panel="b", cell=c, series=f, value=ys[-1], ci95_lo=lo[-1], ci95_hi=hi[-1], label="estimate"))
        ys, lo, hi = map(np.array, (ys, lo, hi))
        b.errorbar(range(3), ys, yerr=[ys - lo, hi - ys], marker=m, ls="-", color="k", mfc=fc, ms=5, capsize=2, lw=0.8,
                   label=lab)
    ys = np.array([float([x for x in sn if x["cell"] == c][0]["tie_given_obs_failure"]) for c in deltas])
    lo = np.array([float([x for x in sn if x["cell"] == c][0]["tie_ci95_lo"]) for c in deltas])
    hi = np.array([float([x for x in sn if x["cell"] == c][0]["tie_ci95_hi"]) for c in deltas])
    b.errorbar(range(3), ys, yerr=[ys - lo, hi - ys], marker="D", ls=(0, (3, 2)), color="k", mfc="white", ms=5, capsize=2,
               lw=0.8, label="B snapped")
    out += [dict(panel="b", cell=c, series="B_snapped", value=v, ci95_lo=l_, ci95_hi=h_, label="estimate")
            for c, v, l_, h_ in zip(deltas, ys, lo, hi)]
    b.set_xticks(range(3))
    b.set_xticklabels(["Δ 0.02", "Δ 0.05", "Δ 0.1"])
    b.set_ylim(0, 1)
    b.set_ylabel("P(VPT = T_out | Δ < T_out ≤ W)")
    b.set_title("(b) ties with the bound, 4 bits", fontsize=8)
    b.legend(fontsize=6, frameon=False)
    # (c) B, snapped B, bound at 4 bits
    c_ = ax[1, 0]
    for rowname, m, fc, ls, lab in (("B", "D", "k", "-", "B (continuous output)"), ("B_snapped", "D", "white", (0, (3, 2)),
                                                                                       "B snapped to nearest prototype"),
                                    ("bound", "_", "k", "-", "output-support bound")):
        rr = [r for r in rd("e5_b_snapped.csv") if r["score"] == "eps0.3_future" and r["row"] == rowname and r["cell"] in deltas]
        rr.sort(key=lambda r: deltas.index(r["cell"]))
        ys = np.array([float(r["value"]) for r in rr])
        lo = np.array([float(r["ci95_lo"]) if r["ci95_lo"] else float(r["value"]) for r in rr])
        hi = np.array([float(r["ci95_hi"]) if r["ci95_hi"] else float(r["value"]) for r in rr])
        c_.errorbar(range(3), ys, yerr=[ys - lo, hi - ys], marker=m, ls=ls, color="k", mfc=fc, ms=6,
                    lw=2.2 if rowname == "bound" else 1.0, capsize=2, label=lab)
        out += [dict(panel="c", cell=r["cell"], series=rowname, value=v, ci95_lo=l_, ci95_hi=h_,
                     label="bound" if rowname == "bound" else "learned") for r, v, l_, h_ in zip(rr, ys, lo, hi)]
    c_.set_yscale("log")
    c_.set_xticks(range(3))
    c_.set_xticklabels(["Δ 0.02", "Δ 0.05", "Δ 0.1"])
    c_.set_ylabel("restricted mean horizon (Lyapunov times)")
    c_.set_title("(c) B scored after snapping, 4 bits", fontsize=8)
    c_.legend(fontsize=6, frameon=False)
    # (d) E5.3
    d = ax[1, 1]
    e = rd("e53_larger_model.csv")
    labs = [f"{r['arm']}{'' if r['arm'] == 'C' else ' ' + r['bits'] + ' b'}" for r in e]
    for j, (col, ci_col, fc, lab) in enumerate((("H_frozen_size", "H_frozen_ci95", "white", "frozen size (128 x 4, 10k steps)"),
                                                ("H_large", "H_large_ci95", "k", "larger (256 x 6, 40k steps)"))):
        ys = np.array([float(r[col]) for r in e])
        ci = np.array([[float(v) for v in r[ci_col].strip("[]").split(",")] for r in e])
        d.errorbar(np.arange(len(e)) + (j - 0.5) * 0.25, ys, yerr=[ys - ci[:, 0], ci[:, 1] - ys], marker="o", ls="none",
                   color="k", mfc=fc, ms=5, capsize=2, label=lab)
        out += [dict(panel="d", cell=l_, series=col, value=v, ci95_lo=a_, ci95_hi=b_, label="learned")
                for l_, v, (a_, b_) in zip(labs, ys, ci)]
    d.set_xticks(range(len(e)))
    d.set_xticklabels(labs, fontsize=7)
    d.set_ylabel("restricted mean horizon (Lyapunov times)")
    d.set_title("(d) larger and longer model, Δ = 0.05", fontsize=8)
    d.legend(fontsize=6, frameon=False)
    fig.suptitle("Post-freeze extension: reviewer controls on Lorenz-63 (ε = 0.3, future frames). No learned KS cell "
                 "qualified (E4).", fontsize=7)
    fig.savefig(OUT.with_suffix(".svg"))
    fig.savefig(OUT.with_suffix(".png"), dpi=200)
    with open(OUT.with_suffix(".csv"), "w", newline="") as fh:
        fh.write(f"# git_sha={config.git_sha()}; POST-FREEZE EXTENSION F8\n")
        w = csv.DictWriter(fh, fieldnames=["panel", "cell", "series", "value", "ci95_lo", "ci95_hi", "label"])
        w.writeheader()
        w.writerows(out)
    print("wrote", OUT, len(out))


if __name__ == "__main__":
    main()
