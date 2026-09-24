"""Tasks 3 and 4 analysis: learned arms against the frozen bounds and references, same states.

Reads runs/learned/main/*/ (per-state horizons) and runs/headline/*.npz (bound, references).
Writes results/learned/{cells.csv, comparisons.csv, learned.json}. Readings are the frozen margins only.
Labels: cells of trained arms are `learned`; differences, ratios and fractions are `estimate`.
"""
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np  # noqa: E402

from th import config, score  # noqa: E402

FZ = config.freeze()
RUN = config.RUNS / "learned" / "main"
OUT = config.RESULTS / "learned"
PRIMARY = "eps0.3_future"
SCORES = ["eps0.3_future", "eps0.3_from_t0", "eps0.1_future", "eps0.5_future"]
N_HIST = FZ["blocks"]["confirmation"]["history_panel_states"]
NEAR = FZ["margins"]["near"]["upper_limit"]
STALL = FZ["stop"]["stall_repeat_fraction"]


def load_runs():
    groups = defaultdict(list)
    for done in sorted(RUN.glob("*/done")):
        d = done.parent
        info = json.loads((d / "info.json").read_text())
        z = dict(np.load(d / "eval.npz"))
        j = info["job"]
        key = (j["system"], j["arm"], j["bits"], j["delta"], j.get("noise", 0.0), j.get("n_traj") or 0)
        groups[key].append(dict(seed=j["seed"], info=info, z=z))
    for k in groups:
        groups[k].sort(key=lambda r: r["seed"])
    return groups


def ref_arrays(system, bits, delta):
    p = config.RUNS / "headline" / f"{system}_b{bits}_D{delta:g}_dt0.01_M1500.npz"
    if not p.exists():
        return None
    z = dict(np.load(p))
    if float(z["PF_fallback_rate"]) > FZ["references"]["particle_filter"]["fallback_rate_limit"]:
        p3 = p.with_name(p.name.replace("M1500", "M3000"))
        if p3.exists():
            z3 = dict(np.load(p3))
            for k in z3:
                if k.startswith(("H_PF", "PF_")):
                    z[k] = z3[k]
    return z


def stack(runs, key):
    return np.stack([r["z"][key] for r in runs])          # (S, n)


def ratio_boot(Ha, Hb, reps=None):
    """mean(Ha) / mean(Hb), paired states, seeds of Ha resampled."""
    reps = reps or FZ["seeds"]["bootstrap_reps"]
    rng = np.random.default_rng(FZ["seeds"]["bootstrap_seed"])
    Ha = np.atleast_2d(Ha)
    n = Ha.shape[1]
    r = np.empty(reps)
    for i in range(reps):
        ni = rng.integers(0, n, n)
        si = rng.integers(0, Ha.shape[0], Ha.shape[0])
        r[i] = Ha[np.ix_(si, ni)].mean() / Hb[ni].mean()
    return dict(ratio=float(Ha.mean() / Hb.mean()), ci95=(float(np.quantile(r, .025)), float(np.quantile(r, .975))))


def cell_row(key, runs):
    system, arm, bits, delta, noise, ntraj = key
    row = dict(system=system, arm=arm, bits=bits, delta=delta, noise=noise, n_traj=ntraj or 100,
               seeds=",".join(str(r["seed"]) for r in runs), n_seeds=len(runs), label="learned")
    for sc in SCORES:
        H = stack(runs, f"H_{sc}")
        m, lo, hi = score.bootstrap_mean(H)
        row[f"H_{sc}"], row[f"H_{sc}_lo"], row[f"H_{sc}_hi"] = m, lo, hi
        m3, lo3, hi3 = score.bootstrap_mean(H[:, :N_HIST])
        row[f"H300_{sc}"], row[f"H300_{sc}_lo"], row[f"H300_{sc}_hi"] = m3, lo3, hi3
    ev = [r["info"]["eval"] for r in runs]
    if arm == "A":
        rep = [e["repeat_fraction"] for e in ev]
        row["repeat_fraction_mean"] = float(np.mean(rep))
        row["repeat_fraction_max"] = float(np.max(rep))
        row["true_repeat_fraction"] = float(np.mean([e["true_repeat_fraction"] for e in ev]))
        row["stalled_seeds"] = int(sum(x > STALL for x in rep))
        Hd = stack(runs, f"Hdiag_{PRIMARY}")
        row["Hdiag_primary"], row["Hdiag_primary_lo"], row["Hdiag_primary_hi"] = score.bootstrap_mean(Hd)
    if arm == "D":
        row["recon_rmse_rel"] = float(np.mean([e["recon_rmse_rel"] for e in ev]))
    if "current_token_rmse_rel" in ev[0]:
        row["current_token_rmse_rel"] = float(ev[0]["current_token_rmse_rel"])
    inf = runs[0]["info"]
    row.update(params_total=inf["params"]["total"], params_backbone=inf["params"]["backbone"],
               params_head=inf["params"]["head"], params_adapter=inf["params"]["adapter"],
               train_flops=inf["train_flops"], steps=inf["steps"],
               best_val_mean=float(np.mean([r["info"]["best_val"] for r in runs])))
    if arm == "E":
        row["temperature_mean"] = float(np.mean([r["info"]["temperature"] for r in runs]))
    if "probes" in inf:
        for kind in ("linear", "mlp"):
            row[f"probe_{kind}_recon_rmse_rel"] = float(np.mean([r["info"]["probes"][kind]["recon_rmse_rel"]
                                                                 for r in runs]))
            H = stack(runs, f"Hprobe_{kind}_{PRIMARY}")
            row[f"probe_{kind}_H"], row[f"probe_{kind}_H_lo"], row[f"probe_{kind}_H_hi"] = score.bootstrap_mean(H)
    return row


def comp(rows, name, a_label, b_label, Ha, Hb, context, reading=True):
    pd = score.paired_diff(Ha, Hb)
    r = dict(comparison=name, a=a_label, b=b_label, **context, n_states=int(np.atleast_2d(Ha).shape[1]),
             diff_a_minus_b=pd["diff"], ci90_lo=pd["ci90"][0], ci90_hi=pd["ci90"][1],
             ci95_lo=pd["ci95"][0], ci95_hi=pd["ci95"][1], label="estimate")
    r["reading"] = "; ".join(score.reading(pd)) if reading else "reported as gap only (WO section 4)"
    rows.append(r)
    return pd


def main():
    groups = load_runs()
    OUT.mkdir(parents=True, exist_ok=True)
    cells = [cell_row(k, v) for k, v in sorted(groups.items(), key=lambda kv: str(kv[0]))]
    comps, extra = [], []
    flags = []
    by = {k: v for k, v in groups.items()}

    def g(system, arm, bits, delta, noise=0.0, ntraj=0):
        return by.get((system, arm, bits, delta, noise, ntraj))

    for system in ("lorenz28", "lorenz45", "l96_5"):
        for delta in FZ["scoring"]["frame_intervals"]:
            C0 = g(system, "C", 0, delta, 0.0)
            for bits in (4, 6, 8, 10):
                ref = ref_arrays(system, bits, delta)
                A, B, D = g(system, "A", bits, delta), g(system, "B", bits, delta), g(system, "D", bits, delta)
                E = g(system, "E", bits, delta)
                ctx = dict(system=system, bits=bits, delta=delta)
                for sc in ("eps0.3_future", "eps0.3_from_t0"):
                    c = dict(ctx, score=sc)
                    if ref is not None:
                        bound, di, pf = ref[f"H_bound_{sc}"], ref[f"H_DI_{sc}"], ref[f"H_PF_{sc}"]
                        pf_label = "reference" if float(ref["PF_fallback_rate"]) <= \
                            FZ["references"]["particle_filter"]["fallback_rate_limit"] else "unreliable"
                    for nm, R in (("A", A), ("B", B), ("C(sigma=0)", C0), ("D", D), ("E", E)):
                        if R is None or ref is None:
                            continue
                        H = stack(R, f"H_{sc}")
                        is_A = nm == "A"
                        comp(comps, f"{nm} vs output-support bound", nm, "bound", H, bound, c, reading=not is_A)
                        comp(comps, f"{nm} vs history reference", nm, f"history ref ({pf_label})", H[:, :N_HIST], pf, c)
                        comp(comps, f"{nm} vs decode-and-integrate", nm, "decode-and-integrate", H, di, c)
                        o = score.outlast(H, bound)
                        extra.append(dict(kind="outlast_vs_bound", arm=nm, **c, outlast=o["outlast"], ties=o["ties"],
                                          label="estimate"))
                        # investigation trigger: a learned model exceeding the history reference beyond the near margin
                        pd = score.paired_diff(H[:, :N_HIST], pf)
                        if pd["diff"] > NEAR and nm != "C(sigma=0)":
                            flags.append(dict(arm=nm, **c, diff=pd["diff"], ci95=pd["ci95"]))
                        if nm in ("D",):
                            pd = score.paired_diff(pf, H[:, :N_HIST])
                            extra.append(dict(kind="near_history_reference", arm=nm, **c,
                                              ref_minus_model=pd["diff"], upper95=pd["ci95"][1],
                                              near=bool(score.near(pd)), label="estimate"))
                    if A is not None and ref is not None and sc == PRIMARY:
                        HA = stack(A, f"H_{sc}")
                        rb = ratio_boot(HA, bound)
                        extra.append(dict(kind="A_fraction_of_bound_H_A_over_U_C", **c, ratio=rb["ratio"],
                                          ci95_lo=rb["ci95"][0], ci95_hi=rb["ci95"][1], label="estimate"))
                        Hd = stack(A, f"Hdiag_{sc}")
                        comp(comps, "A diagnostic readout vs A", "A readout", "A", Hd, HA, c)
                        comp(comps, "A diagnostic readout vs B", "A readout", "B", Hd, stack(B, f"H_{sc}"), c) \
                            if B is not None else None
                    if A is not None and B is not None:
                        comp(comps, "A vs B (categorical-pipeline penalty)", "A", "B",
                             stack(A, f"H_{sc}"), stack(B, f"H_{sc}"), c)
                    if B is not None and C0 is not None:
                        comp(comps, "B vs C sigma=0 (quantized-observation-and-feedback penalty)", "B", "C(sigma=0)",
                             stack(B, f"H_{sc}"), stack(C0, f"H_{sc}"), c)
                    if E is not None and C0 is not None:
                        comp(comps, "E vs C sigma=0", "E", "C(sigma=0)", stack(E, f"H_{sc}"), stack(C0, f"H_{sc}"), c)
                    if E is not None and A is not None:
                        comp(comps, "E vs A", "E", "A", stack(E, f"H_{sc}"), stack(A, f"H_{sc}"), c)
                    # A-probes: vs current-token baseline (decode-and-integrate) and vs D
                    if A is not None and "probes" in A[0]["info"] and ref is not None:
                        for kind in ("linear", "mlp"):
                            Hp = stack(A, f"Hprobe_{kind}_{sc}")
                            comp(comps, f"A-probe ({kind}) vs current-token baseline", f"A-probe {kind}",
                                 "decode-and-integrate", Hp, di, c)
                            if D is not None:
                                comp(comps, f"A-probe ({kind}) vs D", f"A-probe {kind}", "D", Hp,
                                     stack(D, f"H_{sc}"), c)
                            if sc == PRIMARY:
                                rm = [r["info"]["probes"][kind]["recon_rmse_rel"] for r in A]
                                ct = A[0]["info"]["eval"]["current_token_rmse_rel"]
                                extra.append(dict(kind=f"probe_{kind}_recon", **c, probe_rmse_rel_per_seed=rm,
                                                  current_token_rmse_rel=ct,
                                                  probe_below_baseline_all_seeds=bool(all(x < ct for x in rm)),
                                                  label="estimate"))
            # C noise variant vs C sigma=0
            C3 = g(system, "C", 0, delta, FZ["learned"]["c_noise_levels"][1])
            if C0 is not None and C3 is not None:
                for sc in ("eps0.3_future",):
                    comp(comps, "C noise-injected vs C sigma=0", "C(sigma=0.03)", "C(sigma=0)",
                         stack(C3, f"H_{sc}"), stack(C0, f"H_{sc}"), dict(system=system, bits=0, delta=delta, score=sc))
    # data-size axis
    for bits in (6, 10):
        A2k, A20k = g("lorenz28", "A", bits, 0.05), g("lorenz28", "A", bits, 0.05, 0.0, 1000)
        if A2k is not None and A20k is not None:
            comp(comps, "A 20,000 tu vs A 2,000 tu (data axis)", "A 20k", "A 2k", stack(A20k, f"H_{PRIMARY}"),
                 stack(A2k, f"H_{PRIMARY}"), dict(system="lorenz28", bits=bits, delta=0.05, score=PRIMARY))
    sha = config.git_sha()
    for rows, name in ((cells, "cells"), (comps, "comparisons"), (extra, "extra")):
        keys = []
        for r in rows:
            for k in r:
                if k not in keys:
                    keys.append(k)
        with open(OUT / f"{name}.csv", "w", newline="") as fh:
            fh.write(f"# git_sha={sha}\n")
            w = csv.DictWriter(fh, fieldnames=keys)
            w.writeheader()
            for r in rows:
                w.writerow({k: (json.dumps(v) if isinstance(v, (list, tuple)) else v) for k, v in r.items()})
    (OUT / "learned.json").write_text(json.dumps(dict(git_sha=sha, cells=cells, comparisons=comps, extra=extra,
                                                      investigation_flags=flags), indent=1, default=float))
    print(f"{len(cells)} cells, {len(comps)} comparisons, {len(flags)} investigation flags")
    for f in flags:
        print("FLAG", f)


if __name__ == "__main__":
    main()
