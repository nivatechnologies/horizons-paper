"""Stage-2 paper figures (greyscale; every arm distinguished by marker AND line style, direct labels). From
stage2/results/s2_rows.csv, s2_partB.csv, s2_detector.csv, s2_training.csv. SVG + PNG + CSV with SHA each.

  S2F1_retention   retention (horizon / O) against test Re, fresh panels, seed-pooled, w = 11, eps 0.1; D and C
  S2F2_recovery    horizon against window w (3, 6, 11) at Re 50 and 56; D and C
  S2F3_conditions  horizon at Re 50 and 56 against training conditions (H: Re 40 only; L_range: 34-46; L_range-wide: 30-60)
  S2F4_detector    identified Re against w for H (seed-averaged) and P1; D and C
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

RES = config.PKG / "stage2" / "results"
FIG = config.PKG / "stage2" / "figures"
STYLE = {
    "O": ("*", "-", "0.0", True, "O oracle"),
    "H": ("o", "-", "0.0", True, "H hybrid (physics + correction), Re identified; trained at Re 40 only"),
    "P1x": ("s", (0, (1, 1)), "0.35", False, "P1x true family, Re identified (diag.)"),
    "L_range_wide": ("v", (0, (5, 2)), "0.45", True, "L_range-wide history FNO, Re 30-60"),
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
        fh.write(f"# git_sha={config.git_sha()}; Adapt the Physics stage 2 {name}\n")
        w = csv.DictWriter(fh, fieldnames=list(pts[0].keys()))
        w.writeheader()
        w.writerows(pts)
    print("wrote", out, len(pts))


def kw(arm, **o):
    m, ls, g, fill, lab = STYLE[arm]
    d = dict(marker=m, ls=ls, color=g, mfc=g if fill else "white", mec=g, ms=5, lw=1.1, label=lab)
    d.update(o)
    return d


def sel(rows, **k):
    return [r for r in rows if all(str(r[a]) == str(b) for a, b in k.items())]


def main():
    plt.rcParams.update({"font.size": 8, "axes.linewidth": 0.6, "font.family": "DejaVu Sans"})
    rows = rd("s2_rows.csv")
    # S2F1
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 4.5), constrained_layout=True, sharey=True)
    pts = []
    for ax, wd in zip(axes, ("D", "C")):
        for arm in STYLE:
            rr = sorted(sel(rows, world=wd, arm=arm, w=11, eps=0.1, score="future"), key=lambda r: int(r["Re"]))
            rr = [r for r in rr if r["retention"]]
            if not rr:
                continue
            x, y = [int(r["Re"]) for r in rr], [float(r["retention"]) for r in rr]
            ax.plot(x, y, **kw(arm))
            pts += [dict(figure="S2F1", world=wd, arm=arm, Re=a, retention=b, restricted_mean=r["restricted_mean"],
                         seeds=r["seeds"], label=r["label"]) for a, b, r in zip(x, y, rr)]
        for yv in (0.85, 0.70):
            ax.axhline(yv, color="k", lw=0.5, ls=(0, (1, 2)))
        ax.axvspan(34, 46, color="0.9", zorder=0)
        ax.axvspan(30, 60, color="0.96", zorder=-1)
        ax.set_xlim(34.5, 57.5)
        ax.set_xticks([36, 40, 44, 50, 56])
        ax.set_ylim(0, 1.08)
        ax.set_xlabel("test Re (dark band: 34-46; light: 30-60 training ranges)")
        ax.set_title(f"World {wd}: {'drag' if wd == 'D' else 'drag + topographic beta'} (fresh panels, 3 seeds)", fontsize=8)
    axes[0].set_ylabel("retention: horizon / oracle (w = 11, ε = 0.1σ_A)")
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="outside lower center", ncol=2, fontsize=6, frameon=False)
    save(fig, "S2F1_retention", pts)
    # S2F2
    fig, axes = plt.subplots(2, 2, figsize=(7.4, 6.4), constrained_layout=True, sharey=True)
    pts = []
    for i, wd in enumerate(("D", "C")):
        for j, Re in enumerate((50, 56)):
            ax = axes[i, j]
            for arm in STYLE:
                rr = sorted(sel(rows, world=wd, arm=arm, Re=Re, eps=0.1, score="future"), key=lambda r: int(r["w"]))
                if not rr:
                    continue
                x, y = [int(r["w"]) for r in rr], [float(r["restricted_mean"]) for r in rr]
                lo = [float(r["ci95_lo"]) for r in rr]
                hi = [float(r["ci95_hi"]) for r in rr]
                ax.errorbar(x, y, yerr=[np.array(y) - lo, np.array(hi) - y], capsize=1.5, elinewidth=0.5, **kw(arm))
                pts += [dict(figure="S2F2", world=wd, Re=Re, arm=arm, w=a, restricted_mean=b, label=r["label"])
                        for a, b, r in zip(x, y, rr)]
            ax.set_yscale("log")
            ax.set_xscale("log")
            ax.set_xticks([3, 6, 11])
            ax.set_xticklabels(["3", "6", "11"])
            ax.set_title(f"World {wd}, Re {Re}", fontsize=8)
            ax.set_xlabel("window w (frames after the change)")
    for a in axes[:, 0]:
        a.set_ylabel("horizon (Lyapunov times), ε = 0.1σ_A")
    h, l = axes[0, 0].get_legend_handles_labels()
    fig.legend(h, l, loc="outside lower center", ncol=2, fontsize=6, frameon=False)
    save(fig, "S2F2_recovery", pts)
    # S2F3
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 4.0), constrained_layout=True, sharey=True)
    pts = []
    cats = [("H", "H: Re 40 only\n(1 condition)"), ("L_range", "L_range: Re 34-46\n(1,024 conditions)"),
            ("L_range_wide", "L_range-wide: Re 30-60\n(1,024 conditions)")]
    for ax, wd in zip(axes, ("D", "C")):
        for Re, off, ms in ((50, -0.12, 5), (56, 0.12, 7)):
            for xi, (arm, _) in enumerate(cats):
                r = sel(rows, world=wd, arm=arm, Re=Re, w=11, eps=0.1, score="future")
                if not r:
                    continue
                y = float(r[0]["restricted_mean"])
                ax.errorbar([xi + off], [y], yerr=[[y - float(r[0]["ci95_lo"])], [float(r[0]["ci95_hi"]) - y]], capsize=2,
                            **kw(arm, ls="none", ms=ms, label=None))
                ax.annotate(f"Re {Re}", (xi + off, y), xytext=(4, 0), textcoords="offset points", fontsize=5.5)
                pts.append(dict(figure="S2F3", world=wd, Re=Re, arm=arm, restricted_mean=y, label=r[0]["label"]))
            o = sel(rows, world=wd, arm="O", Re=Re, w=11, eps=0.1, score="future")
            if o:
                ax.axhline(float(o[0]["restricted_mean"]), color="k", lw=0.5, ls=(0, (1, 2)) if Re == 50 else (0, (4, 2)))
        ax.set_xticks(range(len(cats)))
        ax.set_xticklabels([c[1] for c in cats], fontsize=6)
        ax.set_title(f"World {wd} (lines: oracle at Re 50 dotted, Re 56 dashed)", fontsize=8)
    axes[0].set_ylabel("horizon at w = 11, ε = 0.1σ_A (Lyapunov times)")
    save(fig, "S2F3_conditions", pts)
    # S2F4
    det = rd("s2_detector.csv")
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 4.4), constrained_layout=True, sharey=True)
    pts = []
    greys = {36: "0.65", 40: "0.5", 44: "0.35", 50: "0.2", 56: "0.0"}
    for ax, wd in zip(axes, ("D", "C")):
        for d in det:
            if d["world"] != wd or d["arm"] not in ("H", "P1"):
                continue
            Re = int(d["Re"])
            ws = [3, 6, 11]
            y = [float(d[f"re_hat_w{w}"]) for w in ws]
            m, ls, _, fill, _ = STYLE[d["arm"]]
            ax.plot(ws, y, marker=m, ls=ls, color=greys[Re], mfc=greys[Re] if fill else "white", mec=greys[Re], ms=4, lw=1)
            ax.annotate(f"{d['arm']} {Re}", (11, y[-1]), xytext=(3, 0), textcoords="offset points", fontsize=5, va="center")
            pts += [dict(figure="S2F4", world=wd, arm=d["arm"], Re=Re, w=a, re_hat=b, slope=d["slope_per_frame"],
                         label=d["label"]) for a, b in zip(ws, y)]
        for Re in greys:
            ax.axhline(Re, color="k", lw=0.4, ls=(0, (1, 3)))
        ax.set_xscale("log")
        ax.set_xticks([3, 6, 11])
        ax.set_xticklabels(["3", "6", "11"])
        ax.set_xlabel("window w (frames)")
        ax.set_title(f"World {wd}: circle solid = H, plus dash-dot = P1; grey = test Re", fontsize=7)
    axes[0].set_ylabel("identified Re (mean over states); dotted = true Re")
    save(fig, "S2F4_detector", pts)


if __name__ == "__main__":
    main()
