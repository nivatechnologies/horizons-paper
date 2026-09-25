"""Figure F6: history reference, one column per token rate (4 bits left, 6 bits right). Top row, (a) 4 bits and
(b) 6 bits: restricted-mean horizon vs context time per frame interval, with the output-support bound and
decode-and-integrate as reference bands (range over Delta). Bottom row, (c) 4 bits and (d) 6 bits: horizon vs frame
interval at tau = 3.2 for clean, timing-jitter and observation-noise tokens. Primary score (eps = 0.3, future frames).
Panel letters run in reading order; the CSV 'panel' column uses the same letters.

Greyscale-safe: categories are encoded by marker shape and dash pattern with direct labels; colour is not used.
Reads results/history/history.json; writes figures/F6_history.{svg,png,csv}.
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
from th import config  # noqa: E402

RES = config.RESULTS / "history" / "history.json"
OUT = config.FIGS / "F6_history"
TAU_SENS = float(config.freeze()["pins"]["sensitivity_context"])

DELTA_STYLE = {0.02: ("o", "-"), 0.035: ("s", (0, (6, 2))), 0.05: ("^", (0, (3, 2))),
               0.07: ("D", (0, (1, 1.5))), 0.1: ("v", (0, (6, 2, 1, 2)))}
VAR_STYLE = {"clean": ("o", "-", 1.8), "jitter": ("s", (0, (5, 2)), 1.4), "noise": ("^", (0, (1, 1.5)), 1.4)}
INK = "#000000"


def pick(rows, **kw):
    return [r for r in rows if all(r.get(k) == v for k, v in kw.items())]


def best_pf(rows, variant, bits, delta, tau):
    """Row at 1,500 particles unless a 3,000-particle rerun exists (then that row)."""
    rs = pick(rows, method="particle_filter", variant=variant, bits=bits, delta=delta, tau=tau)
    rs.sort(key=lambda r: r["particles"])
    return rs[-1] if rs else None


def main():
    J = json.load(open(RES))
    rows, meta = J["rows"], J["meta"]
    P = meta["primary"]
    sha = config.git_sha()
    bits_list = sorted({r["bits"] for r in rows})
    deltas = sorted({r["delta"] for r in rows})
    taus = sorted({r["tau"] for r in rows if r["method"] == "particle_filter" and r["variant"] == "clean"})
    csv_rows = []

    plt.rcParams.update({"font.size": 8, "axes.linewidth": 0.6, "font.family": "DejaVu Sans"})
    fig, axes = plt.subplots(2, len(bits_list), figsize=(7.2, 6.4), constrained_layout=True)
    letters = "abcdefghijklmnop"
    for c, bits in enumerate(bits_list):
        top, bot = letters[c], letters[len(bits_list) + c]      # reading order: top row, then bottom row
        ax = axes[0, c]
        for meth, lab, hatch in (("output_support_bound", "bound", None), ("decode_and_integrate", "decode-and-integrate", None)):
            rs = pick(rows, method=meth, bits=bits)
            if not rs:
                continue
            vals = [r[f"{P}_mean"] for r in rs]
            lo, hi = min(vals), max(vals)
            ax.axhspan(lo, hi if hi > lo else lo + 0.02, color="0.85", lw=0)
            ax.axhline(lo, color="0.45", lw=0.6)
            ax.axhline(hi, color="0.45", lw=0.6)
            ax.text(taus[-1], hi, f" {lab} ({lo:.2f}-{hi:.2f} over Δ)", va="bottom", ha="right", fontsize=6.5, color="0.2")
            for r in rs:
                csv_rows.append(dict(panel=top, label=r["label"], method=meth, variant="clean", bits=bits, delta=r["delta"],
                                     tau="", particles="", mean=r[f"{P}_mean"], lo95=r[f"{P}_lo95"], hi95=r[f"{P}_hi95"],
                                     no_cross=r[f"{P}_no_cross"], fallback_rate="", sha=sha))
        for d in deltas:
            mk, ls = DELTA_STYLE.get(d, ("x", "-"))
            xs, ys, los, his, unrel = [], [], [], [], []
            for t in taus:
                r = best_pf(rows, "clean", bits, d, t)
                if r is None:
                    continue
                xs.append(t); ys.append(r[f"{P}_mean"]); los.append(r[f"{P}_lo95"]); his.append(r[f"{P}_hi95"])
                unrel.append("unreliable" in r["label"])
                csv_rows.append(dict(panel=top, label=r["label"], method="particle_filter", variant="clean", bits=bits,
                                     delta=d, tau=t, particles=r["particles"], mean=r[f"{P}_mean"], lo95=r[f"{P}_lo95"],
                                     hi95=r[f"{P}_hi95"], no_cross=r[f"{P}_no_cross"], fallback_rate=r["fallback_rate"],
                                     sha=sha))
            if not xs:
                continue
            ax.plot(xs, ys, color=INK, ls=ls, lw=1.1, zorder=3)
            ax.errorbar(xs, ys, yerr=[[y - l for y, l in zip(ys, los)], [h - y for y, h in zip(ys, his)]], fmt="none",
                        ecolor=INK, elinewidth=0.6, capsize=1.5, zorder=3)
            for x, y, u in zip(xs, ys, unrel):
                ax.plot(x, y, marker=mk, ms=5, mfc="white" if u else INK, mec=INK, mew=0.8, ls="none", zorder=4)
            ax.plot([], [], color=INK, ls=ls, marker=mk, ms=5, lw=1.1, label=f"Δ = {d:g}")
        ax.set_title(f"({top}) {bits} bits: particle-filter reference vs context", fontsize=8, loc="left")
        ax.set_xscale("function", functions=(lambda x: np.sqrt(np.clip(x, 0, None)), lambda y: y ** 2))
        ax.set_xlabel("context time τ (tu, square-root axis)")
        ax.set_ylabel("restricted mean λ·VPT (ε = 0.3, future frames)")
        ax.set_xticks(taus)
        ax.set_xticklabels([f"{t:g}" for t in taus], fontsize=6.5)
        ax.set_ylim(bottom=0)
        top = ax.get_ylim()[1]
        pf_max = max(r[f"{P}_mean"] for r in pick(rows, method="particle_filter", variant="clean", bits=bits))
        if pf_max < 0.45 * top:      # empty band between the curves and a high reference band
            ax.legend(fontsize=6.5, frameon=False, loc="center right", bbox_to_anchor=(1.0, 0.55))
        else:
            ax.legend(fontsize=6.5, frameon=False, loc="lower right", bbox_to_anchor=(1.0, 0.18))

        ax = axes[1, c]
        for v, (mk, ls, lw) in VAR_STYLE.items():
            xs, ys, los, his, unrel = [], [], [], [], []
            for d in deltas:
                r = best_pf(rows, v, bits, d, TAU_SENS)
                if r is None:
                    continue
                xs.append(d); ys.append(r[f"{P}_mean"]); los.append(r[f"{P}_lo95"]); his.append(r[f"{P}_hi95"])
                unrel.append("unreliable" in r["label"])
                csv_rows.append(dict(panel=bot, label=r["label"], method="particle_filter", variant=v, bits=bits, delta=d,
                                     tau=TAU_SENS, particles=r["particles"], mean=r[f"{P}_mean"], lo95=r[f"{P}_lo95"],
                                     hi95=r[f"{P}_hi95"], no_cross=r[f"{P}_no_cross"],
                                     fallback_rate=r["fallback_rate"], sha=sha))
            if not xs:
                continue
            ax.plot(xs, ys, color=INK, ls=ls, lw=lw, zorder=3)
            ax.errorbar(xs, ys, yerr=[[y - l for y, l in zip(ys, los)], [h - y for y, h in zip(ys, his)]], fmt="none",
                        ecolor=INK, elinewidth=0.6, capsize=1.5, zorder=3)
            for x, y, u in zip(xs, ys, unrel):
                ax.plot(x, y, marker=mk, ms=5, mfc="white" if u else INK, mec=INK, mew=0.8, ls="none", zorder=4)
            ax.annotate(v, (xs[-1], ys[-1]), xytext=(4, 0), textcoords="offset points", fontsize=7, va="center")
        ax.set_title(f"({bot}) {bits} bits: τ = {TAU_SENS:g}, clean / timing jitter / obs. noise", fontsize=8, loc="left")
        ax.set_xlabel("frame interval Δ (tu)")
        ax.set_ylabel("restricted mean λ·VPT (ε = 0.3, future frames)")
        ax.set_xticks(deltas)
        ax.set_xticklabels([f"{d:g}" for d in deltas], fontsize=6.5)
        ax.set_xlim(deltas[0] - 0.008, deltas[-1] + 0.022)
        ax.set_ylim(bottom=0)
    fig.text(0.5, -0.01, "lorenz28, 300 states, dt = 0.005. Bars: bootstrap 95% intervals. Hollow markers: reference labelled "
             "unreliable (fallback > 5% at 3,000 particles).\nParticle filter and decode-and-integrate: reference; "
             f"output-support bound: bound. SHA {sha}", ha="center", va="top", fontsize=6)
    config.ensure_dirs()
    fig.savefig(f"{OUT}.svg", bbox_inches="tight")
    fig.savefig(f"{OUT}.png", dpi=200, bbox_inches="tight")
    with open(f"{OUT}.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(csv_rows[0].keys()))
        w.writeheader()
        w.writerows(csv_rows)
    print(f"wrote {OUT}.svg/.png/.csv ({len(csv_rows)} rows)")


if __name__ == "__main__":
    main()
