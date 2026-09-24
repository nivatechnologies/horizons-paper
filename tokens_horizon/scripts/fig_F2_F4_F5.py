"""Figures F2 (exchange law), F4 (r by orientation, with FSLE), F5 (dimension). Greyscale-safe: categories are
encoded by marker shape, fill, dash pattern and direct labels, never by colour alone (all ink is black/grey).
Each figure ships as SVG + PNG + CSV; the CSV's first line carries the git SHA.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from th import config  # noqa: E402
from th.exchange import write_csv  # noqa: E402

R = config.RESULTS
FIG = config.FIGS
plt.rcParams.update({"font.size": 8, "axes.linewidth": 0.6, "lines.linewidth": 1.0, "svg.fonttype": "none",
                     "axes.spines.top": False, "axes.spines.right": False})
SHA = config.git_sha()


def save(fig, name, rows, note):
    FIG.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG / f"{name}.svg")
    fig.savefig(FIG / f"{name}.png", dpi=300)
    write_csv(FIG / f"{name}.csv", rows, note)
    plt.close(fig)


def f2():
    el = json.loads((R / "exchange_law" / "exchange_law.json").read_text())["systems"]
    systems = list(el)
    fig, axes = plt.subplots(1, len(systems), figsize=(7.0, 2.1), constrained_layout=True)
    rows = []
    for ax, s in zip(axes, systems):
        rr = [r for r in el[s]["rates"] if r["role"] in ("fit", "heldout")]
        hi = max(max(r["meas"] for r in rr), max((r["pred"] or 0) for r in rr)) * 1.12
        g = np.linspace(0, hi, 200)
        tol = np.where(g >= 0.5, 0.15 * g, 0.075)
        ax.fill_between(g, g - tol, g + tol, color="0.88", lw=0, label="criterion band")
        ax.plot(g, g, color="0.4", lw=0.6, ls="--")
        missing = [str(r["rate_bits"]) for r in rr if r["pred"] is None]
        if missing:
            ax.annotate("no prediction at R = " + ", ".join(missing) + "\n(" + "$\\hat\\delta$ outside h range)",
                        (0.04, 0.84), xycoords="axes fraction", fontsize=6)
        for r in rr:
            held = r["role"] == "heldout"
            p = r["pred"]
            if p is not None:
                ax.errorbar(r["meas"], p, xerr=[[r["meas"] - r["meas_ci95_lo"]], [r["meas_ci95_hi"] - r["meas"]]],
                            yerr=[[p - r["pred_ci95_lo"]], [r["pred_ci95_hi"] - p]], fmt="o" if held else "s",
                            ms=4.5, mfc="white" if held else "black", mec="black", ecolor="0.3", elinewidth=0.6,
                            capsize=0)
                ax.annotate(str(r["rate_bits"]), (r["meas"], p), xytext=(3, -8), textcoords="offset points", fontsize=6)
            rows.append(dict(system=s, rate_bits=r["rate_bits"], role=r["role"], measured=r["meas"],
                             measured_label="reference", predicted=p, predicted_label="estimate",
                             outcome=r["outcome"]))
        ax.set_xlim(0, hi)
        ax.set_ylim(0, hi)
        ax.set_aspect("equal")
        ax.set_title(s, fontsize=8)
    fig.supxlabel("measured $H_W$ (decode-and-integrate reference, Lyapunov times)", fontsize=8)
    axes[0].set_ylabel("predicted $h(\\hat\\delta(R))$")
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    axes[0].legend(handles=[Line2D([], [], marker="s", ls="", mfc="black", mec="black", label="fit rate"),
                             Line2D([], [], marker="o", ls="", mfc="white", mec="black", label="held-out rate"),
                             Patch(color="0.88", label="criterion band")], fontsize=6, frameon=False, loc="upper left")
    save(fig, "F2_exchange_law", rows, "predicted = estimate; measured = reference")


def f4():
    el = json.loads((R / "exchange_law" / "exchange_law.json").read_text())["systems"]
    systems = list(el)
    style = {"fresh": dict(marker="o", ls="-", mfc="black"), "aligned": dict(marker="^", ls="--", mfc="white"),
             "isotropic": dict(marker="s", ls=":", mfc="0.6"),
             "aligned_endpoint": dict(marker="v", ls="-.", mfc="white")}
    fig, axes = plt.subplots(1, len(systems), figsize=(7.0, 2.3), constrained_layout=True, sharey=True)
    rows = []
    for ax, s in zip(axes, systems):
        dl = np.array(el[s]["rel_deltas"])
        for o, st in style.items():
            r = np.array(el[s]["orientations"][o]["r_central"])
            ax.plot(dl, r, color="black", ms=3.5, mec="black", lw=0.8, label=o.replace("_", " "), **st)
            for d, v in zip(dl, r):
                rows.append(dict(system=s, series=o, delta_or_scale_over_sigma_A=float(d), value=float(v),
                                 quantity="r central difference", label="estimate"))
        fs = el[s]["fsle"]
        sc = np.array([f["scale_rel"] for f in fs])
        inv = 1 / np.array([f["fsle_over_lambda"] for f in fs])      # plot lambda/FSLE on the r axis
        ax.plot(sc, inv, color="0.45", lw=1.6, ls="-", label="$\\lambda$/FSLE")
        for d, v in zip(sc, inv):
            rows.append(dict(system=s, series="FSLE", delta_or_scale_over_sigma_A=float(d), value=float(v),
                             quantity="lambda/FSLE (FSLE/lambda inverted)", label="estimate"))
        ax.axhline(1, color="0.5", lw=0.5)
        ax.set_xscale("log")
        ax.set_xlim(5e-5, 0.5)
        ax.set_ylim(0, 3)
        ax.invert_xaxis()
        ax.set_title(s, fontsize=8)
        ax.set_xlabel("$\\delta/\\sigma_A$")
    axes[0].set_ylabel("$r = (dH_W/d\\ln(1/\\delta))^{-1}$")
    axes[-1].legend(fontsize=6, frameon=False, loc="upper left")
    save(fig, "F4_r_orientation", rows, "all estimates; FSLE row stores lambda/FSLE so it shares the r axis")


def f5():
    dist = json.loads((R / "dimension" / "distortion_kmeans.json").read_text())
    dim = json.loads((R / "dimension" / "dimension.json").read_text())
    systems = list(dist["systems"])
    marks = dict(zip(systems, ["o", "s", "^", "v", "D", "P"]))
    fills = dict(zip(systems, ["black", "white", "black", "white", "black", "white"]))
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 2.8), constrained_layout=True)
    rows = []
    rates = dist["rates"]
    for s in systems:
        v = dist["systems"][s]
        a1.plot(rates, v["delta_over_sigma_A"], color="black", marker=marks[s], mfc=fills[s], ms=3.5, lw=0.8)
        a1.annotate(f"{s}  $D_{{eff}}$={v['d_eff']:.2f} [{v['d_eff_ci95'][0]:.3f},{v['d_eff_ci95'][1]:.3f}]"
                    f"  $D_{{KY}}$={v['d_ky']:.2f}", (rates[-1], v["delta_over_sigma_A"][-1]), xytext=(4, 4 if s == "lorenz45" else -2),
                    textcoords="offset points", fontsize=5.5, va="center")
        for R_, d in zip(rates, v["delta_over_sigma_A"]):
            rows.append(dict(panel="a", system=s, x_bits=R_, series="k-means distortion", value=d, lo=None, hi=None,
                             label="estimate"))
    a1.set_yscale("log", base=2)
    a1.set_xlim(3.5, 19)
    a1.set_xlabel("rate R (bits)")
    a1.set_ylabel("$\\delta(R)/\\sigma_A$ (calibration RMS)")
    a1.set_title("a  k-means distortion", fontsize=8, loc="left")
    di = dim["di_vs_kmeans_rate"]
    rvq = dim["rvq_oracle"]
    for s in systems:
        d = [r for r in di if r["system"] == s]
        q = [r for r in rvq if r["system"] == s]
        if not d:
            continue
        a2.plot([r["rate_bits"] for r in d], [r["H_mean"] for r in d], color="black", marker=marks[s],
                mfc=fills[s], ms=3.5, lw=0.8, ls="-")
        if q:
            a2.plot([r["bits"] for r in q], [r["H_mean"] for r in q], color="0.35", marker=marks[s], mfc=fills[s],
                    ms=4.5, lw=0.8, ls="--")
        last = q[-1] if q else d[-1]
        a2.annotate(s, ((last.get("bits") or last.get("rate_bits")), last["H_mean"]), xytext=(4, 0),
                    textcoords="offset points", fontsize=6, va="center")
        for r in d:
            rows.append(dict(panel="b", system=s, x_bits=r["rate_bits"], series="k-means decode-and-integrate",
                             value=r["H_mean"], lo=r["H_ci95_lo"], hi=r["H_ci95_hi"], label="reference"))
        for r in q:
            rows.append(dict(panel="b", system=s, x_bits=r["bits"], series="RVQ oracle decode-and-integrate",
                             value=r["H_mean"], lo=r["H_ci95_lo"], hi=r["H_ci95_hi"], label="reference"))
    a2.set_xlim(3, 29)
    a2.set_xlabel("rate (bits)")
    a2.set_ylabel("$H_W$ (Lyapunov times)")
    a2.set_title("b  horizons: k-means (solid), residual VQ (dashed)", fontsize=8, loc="left")
    save(fig, "F5_dimension", rows, "distortion = estimate; horizons = reference")


if __name__ == "__main__":
    f2()
    f4()
    f5()
