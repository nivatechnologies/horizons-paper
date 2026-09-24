"""POST-FREEZE robustness check (requested 2026-09-24, after the freeze and after the Task 2 results).

Question: how much do the single-frame decomposition and the output-support bound depend on the k-means
initialization? On the same 150,000 lorenz28 calibration states, refit the 4- and 6-bit codebooks with
random_state 0-4, every other k-means setting as frozen (n_init 1, max_iter 300, tol 1e-8). For each codebook:
the single-frame decomposition (same estimator, same trajectory bootstrap) and the output-support bound on the
Task 2 headline panel (1,000 confirmation states, Delta 0.02 / 0.05 / 0.1, eps 0.1 / 0.3 / 0.5, both scores).
The frozen-seed codebook (random_state = bits) stays primary. No history reference, no learned model.

The refitted codebooks live only under runs/postfreeze/codebook_seeds/ and never touch the frozen caches.
Labels: every number here is tagged "post-freeze robustness"; bound values are bounds for their own codebook.
"""
import csv
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np  # noqa: E402
from sklearn.cluster import KMeans  # noqa: E402

from th import config, data, score  # noqa: E402
from th.tokenize import Codebook, kmeans_codebook, kmeans_labels  # noqa: E402
import t2_decomposition as dec  # noqa: E402

FZ = config.freeze()
SYS = "lorenz28"
BITS = (4, 6)
SEEDS = (0, 1, 2, 3, 4)
RUN = config.RUNS / "postfreeze" / "codebook_seeds"
RES = config.RESULTS / "postfreeze"
KM = FZ["tokenizers"]["kmeans"]
EPS = [FZ["scoring"]["eps_primary"]] + FZ["scoring"]["eps_secondary"]


def fit(bits, rs):
    p = RUN / f"kmeans_{SYS}_b{bits}_rs{rs}.npz"
    if p.exists():
        z = np.load(p)
        return Codebook(z["C"], json.loads(str(z["meta"]))), z["labels"]
    X, _ = data.calibration(SYS)
    km = KMeans(n_clusters=2 ** bits, n_init=KM["n_init"], max_iter=KM["max_iter"], tol=KM["tol"], random_state=rs).fit(X)
    meta = dict(n_iter=int(km.n_iter_), inertia=float(km.inertia_), bits=bits, random_state=rs)
    RUN.mkdir(parents=True, exist_ok=True)
    np.savez(p, C=km.cluster_centers_, labels=km.labels_, meta=json.dumps(meta))
    return Codebook(km.cluster_centers_, meta), km.labels_


def bound_on_panel(cb):
    pnl = data.panel(SYS, "confirmation")
    lam, sA, W = config.lam(SYS), data.sigma_A(SYS), FZ["scoring"]["window_lyapunov_times"]
    out = {}
    for delta in FZ["scoring"]["frame_intervals"]:
        _, fut = data.frames(pnl, delta)
        fut = fut[:data.n_future_frames(SYS, delta) + 1]
        e = cb.dist(fut) / sA
        for k, v in score.horizon_all(e, lam, delta, W).items():
            m, lo, hi = score.bootstrap_mean(v["H"])
            out[f"D{delta}_{k}"] = dict(mean=m, lo=lo, hi=hi, no_cross=float(1 - v["crossed"].mean()))
        for eps in EPS:
            out[f"D{delta}_p0_eps{eps}"] = float((e[0] > eps).mean())
    return out


def main():
    RES.mkdir(parents=True, exist_ok=True)
    X, _ = data.calibration(SYS)
    reps = FZ["seeds"]["bootstrap_reps"]
    rows = []
    for bits in BITS:
        variants = [("frozen", bits, kmeans_codebook(SYS, bits), kmeans_labels(SYS, bits))]
        for rs in SEEDS:
            cb, lab = fit(bits, rs)
            variants.append((f"rs{rs}", rs, cb, lab))
        for tag, rs, cb, lab in variants:
            t0 = time.time()
            d = dec.run_rate(bits, reps, cb=cb, lab=lab, out_run=RUN, name=f"decomp_{SYS}_b{bits}_{tag}.npz")
            b = bound_on_panel(cb)
            inertia = float(((X - cb.C[lab]) ** 2).sum())
            row = dict(bits=bits, codebook=tag, random_state=rs, primary=(tag == "frozen"),
                       n_iter=cb.meta.get("n_iter"), inertia=inertia,
                       delta_rel=float(np.sqrt(inertia / len(X)) / data.sigma_A(SYS)),
                       same_as_frozen=bool(np.array_equal(cb.C, variants[0][2].C)),
                       O0_over_I0=d["known_zero"]["O0_over_I0"],
                       passes_original_1e_10=d["known_zero"]["passes_original"],
                       passes_amended_1e_6=d["known_zero"]["passes_amended"])
            for eps in EPS:
                p, c = d["point"][f"eps{eps}"], d["ci95"][f"eps{eps}"]
                for k in ("T_info", "T_codebook", "T_codebook_bc", "T_projected_DI", "O_share_at_Tinfo",
                          "Obc_share_at_Tinfo", "E_share_at_Tinfo"):
                    row[f"decomp_eps{eps}_{k}"] = p[k]
                    row[f"decomp_eps{eps}_{k}_lo"], row[f"decomp_eps{eps}_{k}_hi"] = c[k]
            for k, v in b.items():
                if isinstance(v, dict):
                    row[f"bound_{k}"], row[f"bound_{k}_lo"], row[f"bound_{k}_hi"] = v["mean"], v["lo"], v["hi"]
                    row[f"bound_{k}_nocross"] = v["no_cross"]
                else:
                    row[f"bound_{k}"] = v
            row["label"] = "post-freeze robustness (bound columns: bound; decomposition columns: estimate)"
            rows.append(row)
            print(f"b{bits} {tag:6s} n_iter={row['n_iter']} delta_rel={row['delta_rel']:.5f} "
                  f"O0/I0={row['O0_over_I0']:.2e} Oshare={row['decomp_eps0.3_O_share_at_Tinfo']:.4f} "
                  f"Eshare={row['decomp_eps0.3_E_share_at_Tinfo']:.4f} T_info={row['decomp_eps0.3_T_info']:.3f} "
                  f"bound(D.02)={row['bound_D0.02_eps0.3_future']:.3f} ({time.time()-t0:.0f}s)", flush=True)
    # spread across the five refits, next to the frozen value
    spread = []
    num = [k for k in rows[0] if isinstance(rows[0][k], float) and not k.endswith(("_lo", "_hi"))]
    for bits in BITS:
        fr = [r for r in rows if r["bits"] == bits and r["primary"]][0]
        rr = [r for r in rows if r["bits"] == bits and not r["primary"]]
        for k in num:
            v = np.array([r[k] for r in rr], float)
            spread.append(dict(bits=bits, quantity=k, frozen=fr[k], refit_min=float(v.min()), refit_max=float(v.max()),
                               refit_mean=float(v.mean()), refit_sd=float(v.std(ddof=1)),
                               frozen_minus_refit_mean=float(fr[k] - v.mean()),
                               label="post-freeze robustness"))
    sha = config.git_sha()
    (RES / "codebook_seeds.json").write_text(json.dumps(dict(git_sha=sha, note=__doc__, rows=rows, spread=spread),
                                                        indent=1, default=float))
    for name, rr in (("codebook_seeds_rows", rows), ("codebook_seeds_spread", spread)):
        with open(RES / f"{name}.csv", "w", newline="") as fh:
            fh.write(f"# git_sha={sha}; POST-FREEZE robustness check; frozen-seed codebook is primary\n")
            w = csv.DictWriter(fh, fieldnames=list(rr[0].keys()))
            w.writeheader()
            w.writerows(rr)
    print("wrote", RES)


if __name__ == "__main__":
    main()
