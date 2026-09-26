"""Pivot figures (greyscale; every arm distinguished by marker shape AND line style, plus direct labels). From
pivot/results/pv_rows.csv, pv_detector.csv, pv_cost.csv, pv_training.csv. Each writes SVG, PNG and a CSV with SHA.

  PV1_retention   retention (arm horizon / O) against test Re, w = 11, eps 0.1; panels World D, World C
  PV2_detector    identified Re against window w for H, P1, P1x (median over states), each test Re; panels D, C
  PV3_cost        (a) horizon at Re 50 and 56 against training conditions; (b) against online seconds per state
                  (w = 11, eps 0.1, both worlds)
"""
import csv
import sys
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from ap import config  # noqa: E402

RES = config.PKG / "pivot" / "results"
FIG = config.PKG / "pivot" / "figures"
STYLE = {
    "O": ("*", "-", "0.0", True, "O oracle"),
    "H": ("o", "-", "0.0", True, "H hybrid, Re identified"),
    "H_true": ("o", (0, (1, 1)), "0.45", False, "H + true Re (diag.)"),
    "P1x": ("s", (0, (1, 1)), "0.35", False, "P1x true family, Re identified (diag.)"),
    "L_range": ("^", (0, (5, 2)), "0.0", False, "L_range history FNO, Re 34-46"),
    "L0": ("D", (0, (3, 1, 1, 1)), "0.55", True, "L0 frozen nominal FNO"),
    "L0big": ("D", (0, (5, 2)), "0.55", False, "L0-big (5.9x)"),
    "P1": ("P", (0, (3, 1, 1, 1)), "0.0", False, "P1 no-drag physics, Re identified"),
    "persistence": ("x", (0, (1, 3)), "0.35", False, "persistence"),
}


def rd(name):
    return list(csv.DictReader(l for l in open(RES / name) if not l.startswith("#")))


def save(fig, name, pts):
    FIG.mkdir(parents=True, exist_ok=True)
    out = FIG / name
    fig.savefig(out.with_suffix(".svg"))
    fig.savefig(out.with_suffix(".png"), dpi=200)
    with open(out.with_suffix(".csv"), "w", newline="") as fh:
        fh.write(f"# git_sha={config.git_sha()}; Adapt the Physics pivot {name}\n")
        w = csv.DictWriter(fh, fieldnames=list(pts[0].keys()))
        w.writeheader()
        w.writerows(pts)
    print("wrote", out, len(pts))


def st(arm):
    m, ls, g, fill, lab = STYLE[arm]
    return dict(marker=m, ls=ls, color=g, mfc=g if fill else "white", mec=g, ms=5, lw=1.1, label=lab)


def main():
    plt.rcParams.update({"font.size": 8, "axes.linewidth": 0.6, "font.family": "DejaVu Sans"})
    rows = rd("pv_rows.csv")
    # PV1
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 4.4), constrained_layout=True, sharey=True)
    pts = []
    for ax, wd in zip(axes, ("D", "C")):
        for arm in STYLE:
            rr = sorted([r for r in rows if r["world"] == wd and r["arm"] == arm and r["w"] == "11" and r["eps"] == "0.1"
                         and r["retention"]], key=lambda r: int(r["Re"]))
            if not rr:
                continue
            x = [int(r["Re"]) for r in rr]
            y = [float(r["retention"]) for r in rr]
            ax.plot(x, y, **st(arm))
            pts += [dict(figure="PV1", world=wd, arm=arm, Re=a, retention=b, restricted_mean=r["restricted_mean"],
                         label=r["label"]) for a, b, r in zip(x, y, rr)]
        ax.axhspan(0, 0, color="k")
        for yv, lab in ((0.85, "0.85"), (0.70, "0.70")):
            ax.axhline(yv, color="k", lw=0.5, ls=(0, (1, 2)))
            ax.text(56.4, yv, lab, fontsize=6, va="center")
        ax.axvspan(34, 46, color="0.9", zorder=0)
        ax.set_xticks([36, 40, 44, 50, 56])
        ax.set_ylim(0, 1.1)
        ax.set_xlabel("test Re (grey: L_range training range 34-46)")
        ax.set_title(f"World {wd}: {'drag' if wd == 'D' else 'drag + Codex topographic beta'}", fontsize=8)
    axes[0].set_ylabel("retention: horizon / oracle horizon (w = 11, ε = 0.1σ_A)")
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="outside lower center", ncol=3, fontsize=6, frameon=False)
    fig.suptitle("Retention against drift (dotted lines: PASS thresholds 0.85 in D, 0.70 in C)", fontsize=8)
    save(fig, "PV1_retention", pts)
    # PV2 detector
    det = rd("pv_detector.csv")
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 4.4), constrained_layout=True, sharey=True)
    pts = []
    greys = {36: "0.65", 40: "0.5", 44: "0.35", 50: "0.2", 56: "0.0"}
    for ax, wd in zip(axes, ("D", "C")):
        for d in det:
            if d["world"] != wd:
                continue
            ws = [int(x) for x in d["w_tested"].split(",")]
            y = [float(d[f"re_hat_w{w}"]) for w in ws]
            Re = int(d["Re"])
            m, ls, _, fill, _ = STYLE[d["arm"]]
            ax.plot(ws, y, marker=m, ls=ls, color=greys[Re], mfc=greys[Re] if fill else "white", mec=greys[Re], ms=4, lw=1,
                    label=f"{d['arm']}" if Re == 50 else None)
            ax.annotate(f"{d['arm']} Re {Re}", (ws[-1], y[-1]), xytext=(3, 0), textcoords="offset points", fontsize=5,
                        color="0.3", va="center")
            pts += [dict(figure="PV2", world=wd, arm=d["arm"], Re=Re, w=a, re_hat_mean=b, slope_per_frame=d["slope_per_frame"],
                         label=d["label"]) for a, b in zip(ws, y)]
        for Re in greys:
            ax.axhline(Re, color="k", lw=0.4, ls=(0, (1, 3)))
        ax.set_xscale("log")
        ax.set_xticks([3, 6, 11, 23])
        ax.set_xticklabels(["3", "6", "11", "23"])
        ax.set_xlabel("window w (frames)")
        ax.set_title(f"World {wd}", fontsize=8)
    axes[0].set_ylabel("identified Re (mean over 300 states); dotted = true Re")
    axes[0].legend(fontsize=6, frameon=False, title="marker/line = arm; grey level = test Re", title_fontsize=6)
    fig.suptitle("Window-drift detector: identified Re against window (reported only)", fontsize=8)
    save(fig, "PV2_detector", pts)
    # PV3 cost
    tr = {t["model"]: t for t in rd("pv_training.csv")}
    cost = rd("pv_cost.csv")
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 4.0), constrained_layout=True, sharey=True)
    pts = []
    model_of = {("H", "D"): "H_D", ("H", "C"): "H_C", ("L_range", "D"): "L_range", ("L_range", "C"): "L_range_C",
                ("L0", "D"): "L0", ("L0", "C"): "L0_C", ("L0big", "D"): "L0big"}
    for wd, fill_world in (("D", True), ("C", False)):
        for Re in (50, 56):
            for arm in ("H", "L_range", "L0", "L0big", "O", "P1x"):
                r = [x for x in rows if x["world"] == wd and x["Re"] == str(Re) and x["arm"] == arm and x["w"] == "11"
                     and x["eps"] == "0.1"]
                if not r:
                    continue
                y = float(r[0]["restricted_mean"])
                m, ls, g, fill, lab = STYLE[arm]
                kw = dict(marker=m, color=g, mfc=g if fill_world else "white", mec=g, ms=6 if Re == 56 else 4, ls="none")
                mod = model_of.get((arm, wd))
                if mod and mod in tr:
                    x = int(tr[mod]["training_conditions"])
                    axes[0].plot([x * (1.15 if Re == 56 else 1.0)], [y], **kw)
                    axes[0].annotate(f"{arm} {wd} {Re}", (x, y), xytext=(4, 0), textcoords="offset points", fontsize=5)
                c = [x for x in cost if x["world"] == wd and x["Re"] == str(Re) and x["arm"] == arm and x["w"] == "11"]
                if c and c[0]["wall_seconds_per_state"]:
                    xc = float(c[0]["wall_seconds_per_state"])
                    axes[1].plot([xc], [y], **kw)
                    axes[1].annotate(f"{arm} {wd} {Re}", (xc, y), xytext=(4, 0), textcoords="offset points", fontsize=5)
                    pts.append(dict(figure="PV3", world=wd, Re=Re, arm=arm, horizon=y,
                                    training_conditions=tr[mod]["training_conditions"] if mod in tr else "",
                                    training_states=tr[mod]["training_states"] if mod in tr else "",
                                    online_seconds_per_state=xc, label=r[0]["label"]))
    axes[0].set_xscale("log")
    axes[0].set_xlabel("training conditions (distinct Re in training data)")
    axes[1].set_xscale("log")
    axes[1].set_xlabel("online wall-clock seconds per state")
    axes[0].set_ylabel("horizon at w = 11, ε = 0.1σ_A (Lyapunov times)")
    axes[0].set_title("(a) against training conditions", fontsize=8)
    axes[1].set_title("(b) against online cost", fontsize=8)
    fig.suptitle("Filled = World D, hollow = World C; large = Re 56, small = Re 50; marker = arm (as PV1)", fontsize=7)
    save(fig, "PV3_cost", pts)


if __name__ == "__main__":
    main()
