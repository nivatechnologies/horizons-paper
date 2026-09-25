"""POST-FREEZE EXTENSION, Amendment 1 items A8.3 and A8.4 (Lorenz-63 rho = 28; existing outputs, no new models).

A8.3 Same-panel headline: restricted means of the output-support bound, A, B, C (sigma = 0) and D on the first 300
     confirmation states (the particle-filter panel), with paired differences to the particle filter on that panel,
     for every rate and frame interval of the frozen grid. Primary score (eps 0.3, future frames).
A8.4 Protocol facts: number of confirmation trajectories, their lengths, how starts are spaced, and the bootstrap
     resampling unit, for every original-freeze system with a confirmation panel.
Labels: bound / reference / learned per series; differences are estimates.
"""
import csv
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np  # noqa: E402

from th import config, data, score  # noqa: E402

FZ = config.freeze()
P = "eps0.3_future"
N_HIST = FZ["blocks"]["confirmation"]["history_panel_states"]
OUT = config.RESULTS / "ext"
LM = config.RUNS / "learned" / "main"


def learned(arm, bits, delta, noise=None):
    tag = f"lorenz28_{arm}_b{bits}_D{delta}_s"
    runs = []
    for d in sorted(LM.glob(tag + "*")):
        rest = d.name[len(tag):]
        seed, *suffix = rest.split("_")
        if not seed.isdigit() or not (d / "done").exists():
            continue
        if arm == "C":
            if suffix != [f"n{noise}"]:
                continue
        elif suffix:
            continue
        runs.append(np.load(d / "eval.npz")[f"H_{P}"][:N_HIST])
    return np.stack(runs) if runs else None


def ref(bits, delta):
    p = config.RUNS / "headline" / f"lorenz28_b{bits}_D{delta:g}_dt0.01_M1500.npz"
    z = dict(np.load(p))
    label = "reference"
    if float(z["PF_fallback_rate"]) > FZ["references"]["particle_filter"]["fallback_rate_limit"]:
        p3 = p.with_name(p.name.replace("M1500", "M3000"))
        if p3.exists():
            z3 = dict(np.load(p3))
            z["H_PF_" + P] = z3["H_PF_" + P]
            z["PF_fallback_rate"] = z3["PF_fallback_rate"]
        if float(z["PF_fallback_rate"]) > FZ["references"]["particle_filter"]["fallback_rate_limit"]:
            label = "reference (unreliable)"
    return z, label


def same_panel():
    rows = []
    for bits in (4, 6, 8, 10):
        for delta in FZ["scoring"]["frame_intervals"]:
            z, pf_label = ref(bits, delta)
            pf = z[f"H_PF_{P}"]
            series = {"bound": (z[f"H_bound_{P}"][:N_HIST], "bound"), "A": (learned("A", bits, delta), "learned"),
                      "B": (learned("B", bits, delta), "learned"), "C (sigma=0)": (learned("C", 0, delta, 0.0), "learned"),
                      "D": (learned("D", bits, delta), "learned")}
            m, lo, hi = score.bootstrap_mean(pf)
            rows.append(dict(bits=bits, delta=delta, series="history reference (particle filter)", n_states=len(pf),
                             mean=m, ci95_lo=lo, ci95_hi=hi, diff_vs_pf="", diff_ci95_lo="", diff_ci95_hi="",
                             reading="", label=pf_label))
            for name, (H, lab) in series.items():
                m, lo, hi = score.bootstrap_mean(H)
                pd = score.paired_diff(H, pf)
                rows.append(dict(bits=bits, delta=delta, series=name, n_states=N_HIST, mean=m, ci95_lo=lo, ci95_hi=hi,
                                 diff_vs_pf=pd["diff"], diff_ci95_lo=pd["ci95"][0], diff_ci95_hi=pd["ci95"][1],
                                 reading="; ".join(score.reading(pd)) + ("" if pf_label == "reference"
                                                                          else " (particle filter unreliable here)"),
                                 label=lab))
    return rows


def protocol_facts():
    rows = []
    b = FZ["blocks"]
    for system in ("lorenz28", "lorenz45", "l96_5", "l96_6", "l96_10", "l96_20"):
        pnl = data.panel(system, "confirmation")
        n, steps, _ = pnl["traj"].shape
        dt = pnl["dt"]
        pre = pnl["pre"]
        post = steps - 1 - pre
        rows.append(dict(
            system=system, confirmation_trajectories=n, history_panel_states=N_HIST,
            steps_per_trajectory=steps, dt=dt, pre_history_time=pre * dt, post_time=post * dt,
            window_time_W_over_lambda=config.window_time(system),
            burn_in_steps=FZ["integration"]["burn_in_steps"],
            start_spacing="independent trajectories: each from its own Gaussian start, burned in 5,000 steps; "
                          "not segments of one long trajectory, so starts share no path",
            seed=config.seed("confirmation", system),
            bootstrap_unit="one confirmation state = one independent trajectory (learned arms: model seeds too); "
                           f"{FZ['seeds']['bootstrap_reps']} reps, seed {FZ['seeds']['bootstrap_seed']}",
            label="protocol fact"))
    return rows


def write(name, rows):
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / f"{name}.csv", "w", newline="") as fh:
        fh.write(f"# git_sha={config.git_sha()}; POST-FREEZE EXTENSION (Amendment 1 {name})\n")
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    sp, pf = same_panel(), protocol_facts()
    write("a8_same_panel", sp)
    write("a8_protocol_facts", pf)
    (OUT / "a8.json").write_text(json.dumps(dict(git_sha=config.git_sha(), same_panel=sp, protocol_facts=pf),
                                            indent=1, default=float))
    for r in sp:
        if r["delta"] == 0.02 or r["bits"] == 4:
            print(f"b{r['bits']} D{r['delta']} {r['series']:36s} {r['mean']:.3f} "
                  + (f"vs PF {r['diff_vs_pf']:+.3f} [{r['diff_ci95_lo']:+.3f}, {r['diff_ci95_hi']:+.3f}] {r['reading']}"
                     if r["diff_vs_pf"] != "" else f"({r['label']})"))
    for r in pf:
        print(r["system"], r["confirmation_trajectories"], r["steps_per_trajectory"], r["pre_history_time"],
              round(r["post_time"], 2))
