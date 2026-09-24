"""Figure F3: single-frame decomposition by rate (lorenz28, Amendment 1).

(a) Ensemble-RMSE horizon against token rate: information bound (I), codebook-valued single-frame forecaster
    (I + O, and I + O_bc), projected decode-and-integrate (I + O + E). 95% intervals over calibration trajectories.
(b) Shares at the information-bound crossing: output term O (plug-in and bias-corrected) and the excess E, relative to I.
(c) The three error curves sqrt(term)/sigma_A against lambda*t at every rate, with the eps = 0.3 line.
Greyscale-safe: marker shape, dash pattern and direct labels; no colour.
Reads results/decomposition/decomposition.json and runs/decomposition/*.npz; writes figures/F3_decomposition.*.
"""
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

E = "eps0.3"
OUT = config.FIGS / "F3_decomposition"


def main():
    J = json.loads((config.RESULTS / "decomposition" / "decomposition.json").read_text())
    rates = J["rates"]
    bits = [r["bits"] for r in rates]
    sha = config.git_sha()
    rows = []
    plt.rcParams.update({"font.size": 8, "axes.linewidth": 0.6, "font.family": "DejaVu Sans"})
    fig, ax = plt.subplots(1, 3, figsize=(7.2, 2.6), constrained_layout=True)
    series = [("T_info", "information bound I", "o", "-", 2.0, "k", "bound"),
              ("T_codebook", "codebook-valued, I + O", "s", (0, (5, 2)), 1.2, "white", "estimate"),
              ("T_codebook_bc", "I + O (bias-corrected)", "D", (0, (1, 1.5)), 1.0, "white", "estimate"),
              ("T_projected_DI", "projected decode-and-integrate, I + O + E", "^", (0, (6, 2, 1, 2)), 1.0, "k",
               "estimate")]
    for key, lab, m, ls, lw, fc, label in series:
        y = np.array([r["point"][E][key] for r in rates])
        lo = np.array([r["ci95"][E][key][0] for r in rates])
        hi = np.array([r["ci95"][E][key][1] for r in rates])
        ax[0].errorbar(bits, y, yerr=[y - lo, hi - y], marker=m, ls=ls, lw=lw, color="k", mfc=fc, ms=4, capsize=2,
                       elinewidth=0.6, label=lab)
        rows += [dict(panel="a", series=key, bits=b, value=v, ci95_lo=l, ci95_hi=h, label=label)
                 for b, v, l, h in zip(bits, y, lo, hi)]
    ax[0].set_xlabel("token rate (bits)")
    ax[0].set_ylabel("ensemble-RMSE horizon (Lyapunov times)")
    ax[0].set_xticks(bits)
    ax[0].legend(fontsize=5.5, frameon=False, loc="upper left")
    ax[0].set_title("(a) single-frame horizons", fontsize=8)
    for key, lab, m, ls, fc in (("O_share_at_Tinfo", "O / I (plug-in)", "s", (0, (5, 2)), "white"),
                                ("Obc_share_at_Tinfo", "O_bc / I", "D", (0, (1, 1.5)), "white"),
                                ("E_share_at_Tinfo", "E / I (projection excess)", "^", "-", "k")):
        y = np.array([r["point"][E][key] for r in rates])
        lo = np.array([r["ci95"][E][key][0] for r in rates])
        hi = np.array([r["ci95"][E][key][1] for r in rates])
        ax[1].errorbar(bits, y, yerr=[y - lo, hi - y], marker=m, ls=ls, color="k", mfc=fc, ms=4, capsize=2,
                       elinewidth=0.6, lw=1.0, label=lab)
        rows += [dict(panel="b", series=key, bits=b, value=v, ci95_lo=l, ci95_hi=h, label="estimate")
                 for b, v, l, h in zip(bits, y, lo, hi)]
    ax[1].set_xlabel("token rate (bits)")
    ax[1].set_ylabel("share of I at the information-bound crossing")
    ax[1].set_xticks(bits)
    ax[1].legend(fontsize=5.5, frameon=False)
    ax[1].set_title("(b) output and excess terms", fontsize=8)
    dashes = {4: "-", 6: (0, (5, 2)), 8: (0, (1, 1.5)), 10: (0, (6, 2, 1, 2))}
    for r in rates:
        z = np.load(config.RUNS / "decomposition" / f"{J['system']}_b{r['bits']}.npz")
        lt = z["lam"] * z["t"]
        sA = float(z["sigma_A"])
        n = np.searchsorted(lt, 1.2)
        for curve, lw in ((z["I"], 1.6), (z["I"] + z["O"] + z["E"], 0.7)):
            ax[2].plot(lt[:n], np.sqrt(np.maximum(curve[:n], 0)) / sA, ls=dashes[r["bits"]], color="k", lw=lw)
        ax[2].text(lt[n - 1], np.sqrt(z["I"][n - 1]) / sA, f"{r['bits']} b", fontsize=6, va="center")
    ax[2].axhline(0.3, color="k", lw=0.5, ls=":")
    ax[2].text(0.02, 0.31, "ε = 0.3", fontsize=6)
    ax[2].set_xlabel("λ t")
    ax[2].set_ylabel("RMSE / σ_A")
    ax[2].set_title("(c) thick: √I; thin: √(I+O+E)", fontsize=8)
    fig.savefig(OUT.with_suffix(".svg"))
    fig.savefig(OUT.with_suffix(".png"), dpi=200)
    with open(OUT.with_suffix(".csv"), "w", newline="") as fh:
        fh.write(f"# git_sha={sha}\n")
        w = csv.DictWriter(fh, fieldnames=["panel", "series", "bits", "value", "ci95_lo", "ci95_hi", "label"])
        w.writeheader()
        w.writerows(rows)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
