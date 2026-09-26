"""Adapt the Physics stage-1 figures (greyscale; every arm distinguished by marker shape AND line style, plus a direct
label), from results/ap_rows.csv and results/ap_cost.csv. Each figure writes SVG, PNG and a CSV of the plotted points
with the producing SHA.

  AP1_drift      restricted-mean horizon (Lyapunov times of the test system) against test Re, w = 11; panels eps 0.1, 0.3
  AP2_recovery   horizon against window w (frames; top axis Lyapunov times at Re 44), Re 44 and Re 50, eps 0.1
  AP3_cost       horizon against online adaptation wall-clock seconds per state, Re 44, w = 11, eps 0.1
"""
import csv
import sys
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ap import config  # noqa: E402

STYLE = {  # arm: (marker, linestyle, grey, fill, label)
    "O": ("*", "-", "0.0", True, "O oracle (true family, true Re)"),
    "P1": ("o", "-", "0.0", True, "P1 identify Re, no-drag solver"),
    "L_param_P1": ("s", "-", "0.35", True, "L_param + P1 (hybrid)"),
    "P1x": ("o", (0, (1, 1)), "0.35", False, "P1x identify, drag known (diag.)"),
    "L_param_true": ("s", (0, (1, 1)), "0.55", False, "L_param + true Re (diag.)"),
    "L_range": ("^", (0, (5, 2)), "0.0", False, "L_range history FNO, Re 34-46"),
    "L_ft": ("v", (0, (5, 2)), "0.35", False, "L_ft fine-tuned FNO (n = 100)"),
    "L0big": ("D", (0, (5, 2)), "0.55", False, "L0-big (5.9x parameters)"),
    "L0": ("D", (0, (3, 1, 1, 1)), "0.55", True, "L0 frozen nominal FNO"),
    "P0": ("P", (0, (3, 1, 1, 1)), "0.0", False, "P0 nominal solver, Re 40"),
    "persistence": ("x", (0, (1, 3)), "0.35", False, "persistence"),
}


def rd(name):
    return list(csv.DictReader(l for l in open(config.RESULTS / name) if not l.startswith("#")))


def plot(ax, x, y, lo, hi, arm):
    m, ls, g, fill, lab = STYLE[arm]
    ax.errorbar(x, y, yerr=[np.array(y) - lo, np.array(hi) - y], marker=m, ls=ls, color=g, mfc=g if fill else "white",
                mec=g, ms=5, lw=1.1, capsize=1.5, elinewidth=0.5, label=lab)


def save(fig, name, pts):
    out = config.FIGS / name
    config.FIGS.mkdir(parents=True, exist_ok=True)
    fig.savefig(out.with_suffix(".svg"))
    fig.savefig(out.with_suffix(".png"), dpi=200)
    with open(out.with_suffix(".csv"), "w", newline="") as fh:
        fh.write(f"# git_sha={config.git_sha()}; Adapt the Physics stage 1 {name}\n")
        w = csv.DictWriter(fh, fieldnames=list(pts[0].keys()))
        w.writeheader()
        w.writerows(pts)
    print("wrote", out, len(pts))


def main():
    rows = [r for r in rd("ap_rows.csv") if r["panel"] == "all"]
    plt.rcParams.update({"font.size": 8, "axes.linewidth": 0.6, "font.family": "DejaVu Sans"})
    res = sorted({int(r["Re"]) for r in rows})
    # AP1 drift
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 4.4), constrained_layout=True, sharey=True)
    pts = []
    for ax, eps in zip(axes, ("0.1", "0.3")):
        for arm in STYLE:
            rr = sorted([r for r in rows if r["arm"] == arm and r["w"] == "11" and r["eps"] == eps], key=lambda r: int(r["Re"]))
            if not rr:
                continue
            x = [int(r["Re"]) for r in rr]
            y = [float(r["restricted_mean"]) for r in rr]
            plot(ax, x, y, [float(r["ci95_lo"]) for r in rr], [float(r["ci95_hi"]) for r in rr], arm)
            pts += [dict(figure="AP1", eps=eps, arm=arm, Re=a, w=11, restricted_mean=b, n=r["n"], label=r["label"])
                    for a, b, r in zip(x, y, rr)]
        ax.axvline(40, color="k", lw=0.5, ls=(0, (1, 2)))
        ax.axvspan(34, 46, color="0.9", zorder=0)
        ax.set_xticks(res)
        ax.set_xlabel("test Re (grey band: L_range / L_param training range 34-46)")
        ax.set_yscale("log")
        ax.set_title(f"ε = {eps}σ_A(test), w = 11 frames", fontsize=8)
    axes[0].set_ylabel("restricted mean horizon (Lyapunov times of the test system)")
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="outside lower center", ncol=3, fontsize=6, frameon=False)
    fig.suptitle("Horizon against drift size (truth with drag; physics family without)", fontsize=8)
    save(fig, "AP1_drift", pts)
    # AP2 recovery
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 4.4), constrained_layout=True, sharey=True)
    pts = []
    for ax, Re in zip(axes, (44, 50)):
        for arm in STYLE:
            rr = sorted([r for r in rows if r["arm"] == arm and int(r["Re"]) == Re and r["eps"] == "0.1"], key=lambda r: int(r["w"]))
            if not rr:
                continue
            x = [int(r["w"]) for r in rr]
            y = [float(r["restricted_mean"]) for r in rr]
            plot(ax, x, y, [float(r["ci95_lo"]) for r in rr], [float(r["ci95_hi"]) for r in rr], arm)
            pts += [dict(figure="AP2", Re=Re, eps=0.1, arm=arm, w=a, restricted_mean=b, n=r["n"], label=r["label"])
                    for a, b, r in zip(x, y, rr)]
        lam = float([r for r in rows if int(r["Re"]) == Re][0]["lam_test"])
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xticks([3, 6, 11, 23])
        ax.set_xticklabels([f"{w}\n({w * 0.35 * lam:.2f} LT)" for w in (3, 6, 11, 23)])
        ax.set_xlabel("window w, frames after the change (Lyapunov times of the test system)")
        ax.set_title(f"Re {Re}, ε = 0.1σ_A", fontsize=8)
    axes[0].set_ylabel("restricted mean horizon (Lyapunov times)")
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="outside lower center", ncol=3, fontsize=6, frameon=False)
    fig.suptitle("Recovery curve: horizon against observation window", fontsize=8)
    save(fig, "AP2_recovery", pts)
    # AP3 cost
    cost = {(int(c["Re"]), c["arm"], int(c["w"])): c for c in rd("ap_cost.csv")}
    fig, ax = plt.subplots(figsize=(5.2, 4.2), constrained_layout=True)
    pts = []
    for arm in STYLE:
        r = [r for r in rows if r["arm"] == arm and r["Re"] == "44" and r["w"] == "11" and r["eps"] == "0.1"]
        c = cost.get((44, arm, 11))
        if not r or c is None or not c["wall_seconds_per_state"]:
            continue
        x = float(c["wall_seconds_per_state"])
        y = float(r[0]["restricted_mean"])
        plot(ax, [x], [y], [float(r[0]["ci95_lo"])], [float(r[0]["ci95_hi"])], arm)
        ax.annotate(arm, (x, y), xytext=(4, 3), textcoords="offset points", fontsize=6, color="0.25")
        pts.append(dict(figure="AP3", Re=44, w=11, eps=0.1, arm=arm, wall_seconds_per_state=x, restricted_mean=y,
                        gradient_steps=c["gradient_steps"], solver_steps_identify=c["solver_steps_identify"],
                        forecast_steps=c["forecast_steps"], label=r[0]["label"]))
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("online wall-clock seconds per state (identification or adaptation + forecast)")
    ax.set_ylabel("restricted mean horizon (Lyapunov times)")
    ax.set_title("Horizon against online cost, Re 44, w = 11, ε = 0.1σ_A", fontsize=8)
    ax.legend(fontsize=5.5, frameon=False, loc="best")
    save(fig, "AP3_cost", pts)


if __name__ == "__main__":
    main()
