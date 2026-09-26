"""Figure F9 (EXT2 learned-tokenizer kill test; the WO's "F8" collides with figures/F8_controls): FSQ perfect
next-token prediction T_pt (reference, not a bound) and FSQ decode-and-integrate beside the k-means patch ceiling
(output-support bound) and k-means decode-and-integrate, against total bits per frame, Kolmogorov Re 40, Delta 0.35,
future frames; panels eps = 0.1 and eps = 0.3. Axes as F7.

Greyscale with two cues per distinction:
  family       k-means = black, thin line;       FSQ = grey, thick line
  quantity     ceiling / T_pt = solid, filled;   decode-and-integrate = dashed, hollow
  layout       8x8 = triangle, 16x16 = diamond (as F7), plus a direct text label at each series end
Reads results/ext2/k3_rows.csv and results/ext/kolmo/e3_rows.csv; writes figures/F9_learned_tokenizer.{svg,png,csv}.
"""
import csv
import sys
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from th import config  # noqa: E402

OUT = config.FIGS / "F9_learned_tokenizer"
MARK = {"8x8": "^", "16x16": "D"}
DELTA = 0.35


def rd(p):
    return list(csv.DictReader(l for l in open(p) if not l.startswith("#")))


def main():
    km = [r for r in rd(config.RESULTS / "ext" / "kolmo" / "e3_rows.csv") if r["family"] == "patch"
          and r["layout"] in MARK and abs(float(r["delta"]) - DELTA) < 1e-9 and r["start"] == "future"]
    fq = [r for r in rd(config.RESULTS / "ext2" / "k3_rows.csv") if abs(float(r["delta"]) - DELTA) < 1e-9
          and r["start"] == "future"]
    plt.rcParams.update({"font.size": 8, "axes.linewidth": 0.6, "font.family": "DejaVu Sans"})
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 4.2), constrained_layout=True, sharey=True)
    out = []
    for ax, eps in zip(axes, ("0.1", "0.3")):
        for lay in MARK:
            for kind, ls, fill, lab in (("bound", "-", True, "k-means ceiling (bound)"),
                                        ("decode_and_integrate", (0, (4, 2)), False, "k-means decode-and-integrate")):
                rr = sorted([r for r in km if r["layout"] == lay and r["eps"] == eps and r["kind"] == kind],
                            key=lambda r: float(r["total_bits"]))
                x = np.array([float(r["total_bits"]) for r in rr])
                y = np.array([float(r["restricted_mean"]) for r in rr])
                lo = np.array([float(r["ci95_lo"]) for r in rr])
                hi = np.array([float(r["ci95_hi"]) for r in rr])
                ax.errorbar(x, y, yerr=[y - lo, hi - y], marker=MARK[lay], ls=ls, lw=0.8, color="k",
                            mfc="k" if fill else "white", ms=4, capsize=1.5, elinewidth=0.5, label=f"{lab}, {lay}")
                out += [dict(eps=eps, family="kmeans", layout=lay, quantity=kind, total_bits=a, restricted_mean=b,
                             ci95_lo=c, ci95_hi=d, label="bound" if kind == "bound" else "reference")
                        for a, b, c, d in zip(x, y, lo, hi)]
            for kind, ls, fill, lab, short, dy in (
                    ("perfect_token", "-", True, "FSQ perfect next-token prediction (reference)", "T_pt", 6),
                    ("decode_and_integrate", (0, (4, 2)), False, "FSQ decode-and-integrate", "DI", -7)):
                ff = sorted([r for r in fq if r["latent"] == lay and r["eps"] == eps and r["kind"] == kind],
                            key=lambda r: float(r["bits_per_frame"]))
                if not ff:
                    continue
                x = np.array([float(r["bits_per_frame"]) for r in ff])
                y = np.array([float(r["restricted_mean"]) for r in ff])
                lo = np.array([float(r["ci95_lo"]) for r in ff])
                hi = np.array([float(r["ci95_hi"]) for r in ff])
                ax.errorbar(x, y, yerr=[y - lo, hi - y], marker=MARK[lay], ls=ls, lw=2.2, color="0.55",
                            mfc="0.55" if fill else "white", mec="0.35", ms=6, capsize=1.5, elinewidth=0.6,
                            label=f"{lab}, {lay}")
                ax.annotate(f"FSQ {lay} {short}", (x[0], y[0]), xytext=(-4, dy), textcoords="offset points",
                            fontsize=5.5, color="0.3", va="center", ha="right")
                out += [dict(eps=eps, family="fsq", layout=lay, quantity=kind, total_bits=a, restricted_mean=b, ci95_lo=c,
                             ci95_hi=d, label="reference (perfect next-token prediction)" if kind == "perfect_token"
                             else "reference") for a, b, c, d in zip(x, y, lo, hi)]
        for tau in (1, 3, 10):
            ax.axhline(tau, color="k", lw=0.5, ls=(0, (1, 2)))
        ax.axhline(27, color="k", lw=0.8, alpha=0.4)
        ax.set_xscale("log", base=2)
        ax.set_yscale("log")
        ax.set_xlabel("total bits per frame")
        ax.set_title(f"ε = {eps}σ_A, Δ = {DELTA:g}, future frames", fontsize=8)
    axes[0].set_ylabel("restricted mean horizon (Lyapunov times)")
    h, l = [], []
    for ax in axes:
        for hh, ll in zip(*ax.get_legend_handles_labels()):
            if ll not in l:
                h.append(hh)
                l.append(ll)
    fig.legend(h, l, loc="outside lower center", ncol=2, fontsize=5.5, frameon=False)
    fig.suptitle("Kolmogorov Re 40: learned FSQ tokenizer beside k-means patch codebooks. k-means black thin, FSQ grey "
                 "thick;\nsolid filled = ceiling (k-means, bound) or T_pt (FSQ, reference, not a bound); dashed hollow = "
                 "decode-and-integrate; dotted 1, 3, 10; grey W = 27", fontsize=6.5)
    fig.savefig(OUT.with_suffix(".svg"))
    fig.savefig(OUT.with_suffix(".png"), dpi=200)
    with open(OUT.with_suffix(".csv"), "w", newline="") as fh:
        fh.write(f"# git_sha={config.git_sha()}; EXT2 F9\n")
        w = csv.DictWriter(fh, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    print("wrote", OUT, len(out))


if __name__ == "__main__":
    main()
