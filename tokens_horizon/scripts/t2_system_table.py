"""Task 2.1 (system table, D_eff part): lambda, s.e., spectrum-sum error, D_KY (dt = 0.01 and 0.005), sigma_A,
k-means distortion curves delta(R) for R = 4..12, and D_eff = -1/slope(log2 delta vs R) over the frozen fit rates
with a bootstrap interval over calibration trajectories (codebooks fixed).

Writes results/system_table.{json,csv}, results/dimension/distortion_kmeans.{json,csv},
runs/exchange_law/distortion_<system>.npz (per-trajectory sums of squared quantization error).
Labels: every number is an 'estimate' (Monte Carlo population quantity).
"""
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np  # noqa: E402

from th import config, data  # noqa: E402
from th.exchange import nearest, write_csv, write_json  # noqa: E402
from th.tokenize import kmeans_codebook  # noqa: E402

SYSTEMS = ["lorenz28", "lorenz45", "l96_5", "l96_6", "l96_10", "l96_20"]
RATES = list(range(4, 13))
RUNS = config.RUNS / "exchange_law"


def distortion(system):
    """Per-trajectory sums of squared quantization error for each rate (exact nearest prototype)."""
    p = RUNS / f"distortion_{system}.npz"
    if p.exists():
        z = np.load(p)
        return z["sq_by_traj"], z["count"]
    X, traj = data.calibration(system)
    n_traj = int(traj.max()) + 1
    sq = np.zeros((len(RATES), n_traj))
    for i, R in enumerate(RATES):
        cbp = config.CACHE / f"kmeans_{system}_{R}.npz"
        if not cbp.exists():
            raise RuntimeError(f"missing {cbp}; never fit k-means here")
        cb = kmeans_codebook(system, R)
        _, d = nearest(cb, X)
        sq[i] = np.bincount(traj, weights=d ** 2, minlength=n_traj)
    count = np.bincount(traj, minlength=n_traj)
    RUNS.mkdir(parents=True, exist_ok=True)
    np.savez(p, sq_by_traj=sq, count=count, rates=np.array(RATES))
    return sq, count


def deff_from(sq, count, fit_idx):
    delta = np.sqrt(sq[fit_idx].sum(1) / count.sum())
    R = np.array(RATES)[fit_idx]
    slope = np.polyfit(R, np.log2(delta), 1)[0]
    return -1.0 / slope


def one(system):
    fz = config.freeze()
    sA = data.sigma_A(system)
    sq, count = distortion(system)
    delta_rel = np.sqrt(sq.sum(1) / count.sum()) / sA
    fit_idx = [RATES.index(r) for r in fz["exchange_law"]["deff_fit_rates"]]
    deff = deff_from(sq, count, fit_idx)
    rng = np.random.default_rng(fz["seeds"]["bootstrap_seed"])
    reps = fz["seeds"]["bootstrap_reps"]
    n_traj = len(count)
    bs = np.empty(reps)
    for r in range(reps):
        k = rng.integers(0, n_traj, n_traj)
        bs[r] = deff_from(sq[:, k], count[k], fit_idx)
    # local (pairwise) dimension between consecutive rates, for the figure
    local = [float(-1.0 / (np.log2(delta_rel[i + 1]) - np.log2(delta_rel[i]))) for i in range(len(RATES) - 1)]
    return system, dict(sigma_A=sA, delta_rel=delta_rel.tolist(), deff=float(deff),
                        deff_ci95=[float(np.quantile(bs, 0.025)), float(np.quantile(bs, 0.975))],
                        deff_boot_sd=float(bs.std(ddof=1)), local_dim=local)


if __name__ == "__main__":
    config.ensure_dirs()
    lyap = json.loads((config.RESULTS / "lyapunov.json").read_text())["systems"]
    with ProcessPoolExecutor(6) as ex:
        res = dict(ex.map(one, SYSTEMS))
    sha = config.git_sha()
    table, rows, drows = {}, [], []
    for s in SYSTEMS:
        r = res[s]
        t = {}
        for dtk in ("dt0.01", "dt0.005"):
            L = lyap[s][dtk]
            t[dtk] = dict(lam_max=L["lam_max"], lam_max_se=L["lam_max_se"], sum_error=L["sum_error"], d_ky=L["d_ky"])
            for q in ("lam_max", "lam_max_se", "sum_error", "d_ky"):
                rows.append(dict(system=s, quantity=q, dt=float(dtk[2:]), value=float(L[q]), ci95_lo=None,
                                 ci95_hi=None, label="estimate", source="results/lyapunov.json"))
        t["sigma_A"] = r["sigma_A"]
        t["d_eff"] = r["deff"]
        t["d_eff_ci95"] = r["deff_ci95"]
        t["d_eff_fit_rates"] = config.freeze()["exchange_law"]["deff_fit_rates"]
        t["label"] = "estimate"
        rows.append(dict(system=s, quantity="sigma_A", dt=0.01, value=r["sigma_A"], ci95_lo=None, ci95_hi=None,
                         label="estimate", source="calibration block"))
        rows.append(dict(system=s, quantity="d_eff", dt=0.01, value=r["deff"], ci95_lo=r["deff_ci95"][0],
                         ci95_hi=r["deff_ci95"][1], label="estimate",
                         source="k-means R in {6,8,10,12}; bootstrap over 150 calibration trajectories"))
        table[s] = t
        for R, dl in zip(RATES, r["delta_rel"]):
            drows.append(dict(system=s, rate_bits=R, delta_over_sigma_A=dl, label="estimate"))
        print(f"{s:9s} lam={t['dt0.01']['lam_max']:.4f} dky={t['dt0.01']['d_ky']:.3f} sA={r['sigma_A']:.4f} "
              f"Deff={r['deff']:.3f} [{r['deff_ci95'][0]:.3f},{r['deff_ci95'][1]:.3f}]", flush=True)
    write_json(config.RESULTS / "system_table.json",
               dict(git_sha=sha, label="estimate", note="all entries are estimates; D_eff interval: bootstrap over "
                    "calibration trajectories, codebooks fixed, 2,000 reps, seed 777, 95%", systems=table))
    write_csv(config.RESULTS / "system_table.csv", rows)
    write_json(config.RESULTS / "dimension" / "distortion_kmeans.json",
               dict(git_sha=sha, label="estimate", rates=RATES,
                    systems={s: dict(delta_over_sigma_A=res[s]["delta_rel"], d_eff=res[s]["deff"],
                                     d_eff_ci95=res[s]["deff_ci95"], local_dim_between_rates=res[s]["local_dim"],
                                     d_ky=lyap[s]["dt0.01"]["d_ky"]) for s in SYSTEMS}))
    write_csv(config.RESULTS / "dimension" / "distortion_kmeans.csv", drows,
              "delta = RMS exact-nearest-prototype error on the calibration block, / sigma_A")
