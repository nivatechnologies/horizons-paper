"""Figure F1: headline on lorenz28. Top row, one panel per frame interval: restricted-mean horizon against
token rate for the output-support bound, the references, the learned arms and the A-probe. Bottom row:
per-state fraction of states on which each forecaster outlasts the output-support bound.
Primary score (eps = 0.3, future frames). 95% intervals.

Greyscale-safe: every series has its own marker shape and dash pattern and a direct label; no colour.
History reference: filled circles; hollow circles mark settings whose filter fallback rate exceeds 5% at
1,500 particles and again at 3,000 particles (unreliable; the 3,000-particle value is plotted).
Reads runs/headline/*.npz and results/learned/{cells,extra}.csv; writes figures/F1_headline.{svg,png,csv}.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from th import config, score  # noqa: E402

SYSTEM = "lorenz28"
P = "eps0.3_future"
BITS = [4, 6, 8, 10]
DELTAS = config.freeze()["scoring"]["frame_intervals"]
OUT = config.FIGS / "F1_headline"
# name: (marker, linestyle, linewidth, fill, label)
STY = {
    "bound": ("_", "-", 2.6, "full", "output-support bound"),
    "history ref": ("o", (0, (5, 2)), 1.4, "none", "history reference"),
    "decode-and-integrate": ("s", (0, (1, 1.5)), 1.2, "none", "decode-and-integrate"),
    "persistence": ("x", (0, (6, 2, 1, 2)), 0.8, "full", "persistence"),
    "A": ("^", "-", 1.2, "full", "A token model"),
    "B": ("D", "-", 1.0, "full", "B continuous output"),
    "D": ("v", (0, (3, 1)), 1.0, "full", "D reconstruction"),
    "A-probe": ("P", (0, (2, 2)), 1.0, "full", "A-probe (MLP)"),
}


def read_csv(p):
    with open(p) as fh:
        return list(csv.DictReader(l for l in fh if not l.startswith("#")))


FALLBACK_LIMIT = 0.05


def ref_series(bits, delta):
    """Reference series at 1,500 particles. Where the filter fallback rate exceeds 5%, the history reference
    (and its outlast fraction) is taken from the 3,000-particle rerun if one exists; the setting is marked
    unreliable when the rate of the file used still exceeds 5% (as history_ref_label in headline.csv)."""
    p = config.RUNS / "headline" / f"{SYSTEM}_b{bits}_D{delta:g}_dt0.01_M1500.npz"
    if not p.exists():
        return {}
    z = np.load(p)
    zpf = z
    if float(z["PF_fallback_rate"]) > FALLBACK_LIMIT:
        p3 = p.with_name(p.name.replace("_M1500", "_M3000"))
        if p3.exists():
            zpf = np.load(p3)
    out = {}
    for nm, key in (("bound", "bound"), ("decode-and-integrate", "DI"), ("persistence", "persistence")):
        out[nm] = score.bootstrap_mean(z[f"H_{key}_{P}"])
    out["history ref"] = score.bootstrap_mean(zpf[f"H_PF_{P}"])
    out["_history_reliable"] = float(zpf["PF_fallback_rate"]) <= FALLBACK_LIMIT
    out["_outlast_history"] = score.outlast(zpf[f"H_PF_{P}"], z[f"H_bound_{P}"][:len(zpf[f"H_PF_{P}"])])["outlast"]
    return out


def _probe_outlast(bits, delta):
    """Per-state outlast of the A-probe (MLP) over the bound, pooled over seeds; nan where no probe exists."""
    runs = sorted((config.RUNS / "learned" / "main").glob(f"{SYSTEM}_A_b{bits}_D{delta}_s*"))
    p = config.RUNS / "headline" / f"{SYSTEM}_b{bits}_D{delta:g}_dt0.01_M1500.npz"
    H = [np.load(r / "eval.npz")[f"Hprobe_mlp_{P}"] for r in runs if (r / "done").exists() and
         f"Hprobe_mlp_{P}" in np.load(r / "eval.npz").files]
    if not H or not p.exists():
        return np.nan
    return score.outlast(np.stack(H), np.load(p)[f"H_bound_{P}"])["outlast"]


def main():
    cells = read_csv(config.RESULTS / "learned" / "cells.csv")
    extra = read_csv(config.RESULTS / "learned" / "extra.csv")
    sha = config.git_sha()

    def cell(arm, bits, delta):
        for r in cells:
            if r["system"] == SYSTEM and r["arm"] == arm and int(r["bits"]) == bits and \
                    float(r["delta"]) == delta and float(r["noise"]) == 0.0 and int(r["n_traj"]) == 100:
                return r
        return None

    plt.rcParams.update({"font.size": 8, "axes.linewidth": 0.6, "font.family": "DejaVu Sans"})
    fig, axes = plt.subplots(2, len(DELTAS), figsize=(7.2, 5.6), constrained_layout=True,
                             gridspec_kw=dict(height_ratios=[1.6, 1]))
    rows = []
    for c, delta in enumerate(DELTAS):
        ax = axes[0, c]
        series = {k: [] for k in STY}
        reliable = {}
        for b in BITS:
            rs = ref_series(b, delta)
            reliable[b] = rs.get("_history_reliable", True)
            for nm in ("bound", "history ref", "decode-and-integrate", "persistence"):
                series[nm].append((b,) + rs[nm] if nm in rs else (b, np.nan, np.nan, np.nan))
            for nm in ("A", "B", "D"):
                r = cell(nm, b, delta)
                series[nm].append((b, float(r[f"H_{P}"]), float(r[f"H_{P}_lo"]), float(r[f"H_{P}_hi"]))
                                  if r else (b, np.nan, np.nan, np.nan))
            r = cell("A", b, delta)
            series["A-probe"].append((b, float(r["probe_mlp_H"]), float(r["probe_mlp_H_lo"]),
                                      float(r["probe_mlp_H_hi"])) if r and r.get("probe_mlp_H") else
                                     (b, np.nan, np.nan, np.nan))
        for nm, pts in series.items():
            m, ls, lw, fill, lab = STY[nm]
            pts = np.array(pts, float)
            ok = ~np.isnan(pts[:, 1])
            if not ok.any():
                continue
            x, y, lo, hi = pts[ok].T
            if nm == "history ref":
                # filled = reliable reference; hollow = fallback > 5% even at 3,000 particles (as in F6)
                ax.errorbar(x, y, yerr=[y - lo, hi - y], marker="none", ls=ls, lw=lw, color="k", capsize=2,
                            elinewidth=0.6)
                for xi, yi in zip(x, y):
                    ax.plot(xi, yi, marker=m, ms=5, ls="none", mec="k", mfc="k" if reliable[int(xi)] else "white",
                            zorder=4)
                ax.errorbar([], [], yerr=[[], []], marker=m, ls=ls, lw=lw, color="k", mfc="k", ms=5, capsize=2,
                            elinewidth=0.6, label="history reference (unreliable: hollow)")
            else:
                ax.errorbar(x, y, yerr=[y - lo, hi - y], marker=m, ls=ls, lw=lw, color="k",
                            mfc="k" if fill == "full" else "white", ms=5, capsize=2, elinewidth=0.6, label=lab)
            for xi, yi, l_, h_ in pts[ok]:
                rows.append(dict(delta=delta, bits=int(xi), series=nm, mean=yi, ci95_lo=l_, ci95_hi=h_,
                                 label={"bound": "bound", "A": "learned", "B": "learned", "D": "learned",
                                        "A-probe": "learned"}.get(nm, "reference"),
                                 reliable=reliable[int(xi)] if nm == "history ref" else ""))
        C0 = [r for r in cells if r["system"] == SYSTEM and r["arm"] == "C" and float(r["delta"]) == delta
              and float(r["noise"]) == 0.0]
        if C0:
            yc = float(C0[0][f"H_{P}"])
            ax.axhline(yc, color="k", lw=0.8, ls=(0, (8, 3)), label="C continuous input (σ=0)")
            rows.append(dict(delta=delta, bits=0, series="C(sigma=0)", mean=yc, ci95_lo=float(C0[0][f"H_{P}_lo"]),
                             ci95_hi=float(C0[0][f"H_{P}_hi"]), label="learned"))
        ax.set_yscale("log")
        ax.set_xticks(BITS)
        ax.set_xlabel("token rate (bits)")
        ax.set_title(f"Δ = {delta:g}")
        if c == 0:
            ax.set_ylabel("restricted mean horizon (Lyapunov times)")
        # bottom: outlast fractions
        ax2 = axes[1, c]
        arms = [("history ref", "o", "////"), ("A", "^", ""), ("B", "D", "...."), ("D", "v", "xxxx"),
                ("A-probe", "P", "\\\\")]
        w = 0.36
        for i, (nm, m, hatch) in enumerate(arms):
            vals = []
            for b in BITS:
                if nm == "history ref":
                    rs = ref_series(b, delta)
                    v = rs.get("_outlast_history", np.nan)
                elif nm == "A-probe":
                    v = _probe_outlast(b, delta)
                else:
                    e = [r for r in extra if r["kind"] == "outlast_vs_bound" and r["arm"] == nm and r["system"] == SYSTEM
                         and int(r["bits"]) == b and float(r["delta"]) == delta and r["score"] == P]
                    v = float(e[0]["outlast"]) if e else np.nan
                vals.append(v)
                rows.append(dict(delta=delta, bits=b, series=f"outlast_vs_bound:{nm}", mean=v, ci95_lo="", ci95_hi="",
                                 label="estimate", reliable=reliable[b] if nm == "history ref" else ""))
            xs = np.arange(len(BITS)) + (i - 2) * w / 2
            ax2.bar(xs, vals, width=w / 2, facecolor="white" if hatch else "black", edgecolor="k", hatch=hatch, lw=0.6,
                    label=nm)
        ax2.set_xticks(np.arange(len(BITS)))
        ax2.set_xticklabels(BITS)
        ax2.set_ylim(0, 1)
        ax2.set_xlabel("token rate (bits)")
        if c == 0:
            ax2.set_ylabel("fraction of states\noutlasting the bound")
        if c == len(DELTAS) - 1:
            ax2.legend(fontsize=6, frameon=False)
    h, l = axes[0, 0].get_legend_handles_labels()
    fig.legend(h, l, loc="outside lower center", ncol=5, fontsize=6, frameon=False)
    fig.suptitle("Lorenz-63 ρ = 28: output-support bound, references and learned arms (ε = 0.3, future frames)",
                 fontsize=8)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT.with_suffix(".svg"))
    fig.savefig(OUT.with_suffix(".png"), dpi=200)
    with open(OUT.with_suffix(".csv"), "w", newline="") as fh:
        fh.write(f"# git_sha={sha}\n")
        w_ = csv.DictWriter(fh, fieldnames=["delta", "bits", "series", "mean", "ci95_lo", "ci95_hi", "label",
                                            "reliable"], restval="")
        w_.writeheader()
        w_.writerows(rows)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
