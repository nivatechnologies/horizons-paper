"""Figure F7 (post-freeze extension): output-support bound and decode-and-integrate against total bits per frame,
per system and tokenizer family, primary frame interval, eps = 0.3, future frames; lines at 1, 3 and 10 Lyapunov
times and the window W = 27. Residual VQ has no bound (Amendment 1 A1): decode-and-integrate only.

Greyscale-safe: family by marker shape, bound = solid line with filled markers, decode-and-integrate = dashed line
with hollow markers; direct legend. Reads results/ext/{ks,kolmo}/e3_rows.csv; writes figures/F7_extension_bounds.*.
Nominal rates P*b (Amendment 1 A3). Patch family: spatially distributed tokenization at practical per-token
vocabulary sizes, with an exactly analyzable product decoder.
"""
import csv
import sys
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import yaml  # noqa: E402

from th import config  # noqa: E402

OUT = config.FIGS / "F7_extension_bounds"
MARK = {"whole": "o", "rvq": "x", "8": "s", "16": "^", "32": "D", "4x4": "s", "8x8": "^", "16x16": "D"}


def rows_of(path):
    return list(csv.DictReader(l for l in open(path) if not l.startswith("#")))


def fam_key(r):
    fam = r["family"]
    if fam in ("whole", "rvq"):
        return fam
    return r.get("layout") or r["P"]


def main():
    efz = yaml.safe_load((config.PKG / "ext_freeze.yaml").read_text())
    systems = []
    for name, spec in efz["ks"]["systems"].items():
        systems.append((name, config.RESULTS / "ext" / "ks" / "e3_rows.csv", spec["primary_delta"], f"KS L = {spec['L']:g}"))
    if "kolmogorov" in efz:
        systems.append(("kolmo40", config.RESULTS / "ext" / "kolmo" / "e3_rows.csv", efz["kolmogorov"]["primary_delta"],
                        "Kolmogorov Re = 40, 64²"))
    systems = [s for s in systems if s[1].exists()]
    plt.rcParams.update({"font.size": 8, "axes.linewidth": 0.6, "font.family": "DejaVu Sans"})
    fig, axes = plt.subplots(1, len(systems), figsize=(3.4 * len(systems) + 0.6, 4.0), constrained_layout=True,
                             squeeze=False)
    out_rows = []
    for ax, (name, path, delta, title) in zip(axes[0], systems):
        rows = [r for r in rows_of(path) if r["system"] == name and abs(float(r["delta"]) - delta) < 1e-9
                and r["eps"] == "0.3" and r["start"] == "future"]
        fams = sorted({fam_key(r) for r in rows}, key=lambda k: (k not in ("whole",), k == "rvq", k))
        for fam in fams:
            for kind, ls, fill in (("bound", "-", True), ("decode_and_integrate", (0, (4, 2)), False)):
                rr = sorted([r for r in rows if fam_key(r) == fam and r["kind"] == kind],
                            key=lambda r: float(r["total_bits"]))
                if not rr:
                    continue
                x = np.array([float(r["total_bits"]) for r in rr])
                y = np.array([float(r["restricted_mean"]) for r in rr])
                lo = np.array([float(r["ci95_lo"]) for r in rr])
                hi = np.array([float(r["ci95_hi"]) for r in rr])
                lab = {"whole": "whole-state k-means", "rvq": "residual VQ"}.get(fam, f"patches P = {fam}")
                ax.errorbar(x, y, yerr=[y - lo, hi - y], marker=MARK.get(fam, "o"), ls=ls, lw=1.0, color="k",
                            mfc="k" if fill else "white", ms=4, capsize=1.5, elinewidth=0.5,
                            label=f"{lab}: {'bound' if kind == 'bound' else 'decode-and-integrate'}")
                out_rows += [dict(system=name, family=fam, kind=kind, delta=delta, total_bits=a, restricted_mean=b,
                                  ci95_lo=c, ci95_hi=d, label="bound" if kind == "bound" else "reference")
                             for a, b, c, d in zip(x, y, lo, hi)]
        for tau in (1, 3, 10):
            ax.axhline(tau, color="k", lw=0.5, ls=(0, (1, 2)))
            ax.text(ax.get_xlim()[0] if False else 1.02, tau, f"{tau}", transform=ax.get_yaxis_transform(),
                    fontsize=6, va="center")
        ax.axhline(27, color="k", lw=0.8, ls="-", alpha=0.4)
        ax.set_xscale("log", base=2)
        ax.set_yscale("log")
        ax.set_xlabel("total bits per frame (nominal P·b)")
        ax.set_title(f"{title}, Δ = {delta:g}", fontsize=8)
    axes[0][0].set_ylabel("restricted mean horizon (Lyapunov times)")
    h, l = [], []
    for ax in axes[0]:
        for hh, ll in zip(*ax.get_legend_handles_labels()):
            if ll not in l:
                h.append(hh)
                l.append(ll)
    fig.legend(h, l, loc="outside lower center", ncol=2, fontsize=6, frameon=False)
    fig.suptitle("Post-freeze extension: output-support bound (solid, filled) and decode-and-integrate (dashed, hollow)\n"
                 "ε = 0.3, future frames; dotted lines at 1, 3, 10 Lyapunov times; grey line W = 27", fontsize=7)
    fig.savefig(OUT.with_suffix(".svg"))
    fig.savefig(OUT.with_suffix(".png"), dpi=200)
    with open(OUT.with_suffix(".csv"), "w", newline="") as fh:
        fh.write(f"# git_sha={config.git_sha()}; POST-FREEZE EXTENSION F7\n")
        w = csv.DictWriter(fh, fieldnames=list(out_rows[0].keys()))
        w.writeheader()
        w.writerows(out_rows)
    print("wrote", OUT, len(out_rows), "points")


if __name__ == "__main__":
    main()
