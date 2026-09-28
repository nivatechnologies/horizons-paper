"""GEPS horizon sanity check (Todd 2026-09-28, before the reading is headlined). CPU only; uses only what the frozen Re 50
cells already use (s2_test_Re50_D, states 0-49, frames from k = w).

1. Persistence's horizon on the same 50 states (Part A persistence arm, same scorer).
2. Per-frame error of GEPS-range (both budgets), persistence and H against the 0.1 threshold (plot + CSV).
3. Code path: GEPS and Part A errors are both ||x_hat(w+j) - x(w+j)||_2 / sigma_A (sum over the 64 x 64 field, sqrt),
   row 0 = the noisy observation at k = w, scored by th.score.horizon(err, lam, 0.35, 10, eps=0.1, start=1).
4. Consistency with GEPS's validation loss: the training validation RelativeL2 is ||pred - y|| / ||y|| over a whole
   20-frame window (frame 0 included). The same quantity is computed here from the GEPS errors on the Re 50 cells:
   sqrt(sum_{j<20} (sigma_A err_j)^2) / sqrt(sum_{j<20} ||x(w+j)||^2).

Writes stage2/geps/results/geps_sanity.json, geps_sanity_err_Re50.csv, geps_sanity_err_Re50.png.
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
PKG = HERE.parents[2]
sys.path.insert(0, str(PKG))
sys.path.insert(0, str(PKG.parent / "tokens_horizon"))
from ap import config  # noqa: E402
from th import score  # noqa: E402

PRE, W, N, EPS, DELTA = 10, 11, 50, 0.1, 0.35
RES = HERE.parent / "results"
G = config.RUNS / "geps_eval" / "geps_range_s0_lr0.001"
S2 = config.RUNS / "s2_eval" / "s2_test_Re50_D"
PANEL = "s2_test_Re50_D"


def main():
    tp = json.loads((PKG / "stage2" / "results" / "test_panels.json").read_text())[PANEL]
    lam, sA = tp["lam"], tp["sigma_A"]
    E = {"GEPS-range (500 steps)": np.load(G / f"{PANEL}_adapt500_states0-{N}.npz")["err"].astype(float),
         "GEPS-range (5,000 steps)": np.load(G / f"{PANEL}_adapt5000_states0-{N}.npz")["err"].astype(float),
         "persistence": np.load(S2 / "persistence_s0_std_11.npz")["err"][:, :N].astype(float),
         "H (seed 0)": np.load(S2 / "H_s0_std_11.npz")["err"][:, :N].astype(float)}
    out = dict(panel=PANEL, n=N, eps=EPS, lam=lam, frame_in_lyapunov_times=lam * DELTA)
    for k, e in E.items():
        H, _ = score.horizon(e, lam, DELTA, 10.0, EPS, 1)
        first = np.argmax(e[1:] > EPS, 0) + 1
        out[k] = dict(horizon_mean=float(H.mean()), first_frame_over_eps_median=float(np.median(first)),
                      err_frame1_median=float(np.median(e[1])), err_frame2_median=float(np.median(e[2])))
    # validation-equivalent RelativeL2 over a 20-frame window from k = w (frame 0 = noisy obs, as GEPS's rollout start)
    T = np.load(config.CACHE / f"{PANEL}.npy", mmap_mode="r")
    yn2 = np.stack([(np.asarray(T[PRE + W + j, :N], dtype=np.float64) ** 2).sum((-2, -1)) for j in range(20)])
    for k in ("GEPS-range (500 steps)", "persistence"):
        e = E[k][:20]
        rel = np.sqrt(((sA * e) ** 2).sum(0)) / np.sqrt(yn2.sum(0))
        out[k]["window20_relativeL2_mean"] = float(rel.mean())
    out["field_norm_over_sigma_A_median"] = float(np.median(np.sqrt(yn2[0]) / sA))
    out["validation_relativeL2_geps_range_best"] = 0.2308721  # epoch 30 (best); last check epoch 34 = 0.2430717
    RES.mkdir(parents=True, exist_ok=True)
    (RES / "geps_sanity.json").write_text(json.dumps(out, indent=1))
    J = 30
    with open(RES / "geps_sanity_err_Re50.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        fh.write(f"# git_sha={config.git_sha()}; per-frame error / sigma_A on {PANEL} states 0-{N - 1}, frame 0 = k = w\n")
        w.writerow(["frame", "lyapunov_times"] + [f"{k} {s}" for k in E for s in ("median", "q25", "q75")])
        for j in range(J + 1):
            w.writerow([j, lam * j * DELTA] + [f"{v:.6g}" for k in E for v in
                                                 (np.median(E[k][j]), np.quantile(E[k][j], .25), np.quantile(E[k][j], .75))])
    plot(E, lam, J)
    print(json.dumps(out, indent=1))


def plot(E, lam, J):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    col = {"GEPS-range (500 steps)": "#2a78d6", "persistence": "#eb6834", "H (seed 0)": "#1baf7a"}
    fig, ax = plt.subplots(figsize=(7.2, 4.2), dpi=150)
    x = lam * np.arange(J + 1) * DELTA
    for k, c in col.items():
        e = E[k][:J + 1]
        ax.fill_between(x, np.quantile(e, .25, 1), np.quantile(e, .75, 1), color=c, alpha=0.15, lw=0)
        ax.plot(x, np.median(e, 1), color=c, lw=2, label=k)
        ax.annotate(k, (x[-1], np.median(e[-1])), xytext=(4, 0), textcoords="offset points", va="center", fontsize=8,
                    color="#333333")
    ax.axhline(EPS, color="#777777", lw=1, ls="--")
    ax.text(x[-1], EPS, "threshold 0.1", va="bottom", ha="right", fontsize=8, color="#555555")
    ax.set_yscale("log")
    ax.set_xlabel("forecast time (Lyapunov times)")
    ax.set_ylabel("error / sigma_A (median, IQR band)")
    ax.set_title("Re 50, first 50 states, w = 11: per-frame error", fontsize=10)
    ax.grid(True, which="major", color="#e6e6e6", lw=0.6)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.legend(frameon=False, fontsize=8, loc="lower right")
    ax.set_xlim(0, x[-1] * 1.25)
    fig.tight_layout()
    fig.savefig(RES / "geps_sanity_err_Re50.png")


if __name__ == "__main__":
    main()
