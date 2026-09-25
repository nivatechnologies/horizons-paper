"""Post-freeze extension, part 2 pilot: Kuramoto-Sivashinsky resolution, Lyapunov spectra, sigma_A, timings.

Measures system properties only (as Task 0 did for the original freeze). No tokenizer, no bound, no decode-and-integrate,
and no confirmation data. Seeds: lyapunov block 50000 and a pilot block 60000, with proposed system indices ks22 = 6,
ks100 = 7 (block base + 100 * index + stream). Writes results/ext/ks_pilot.json.

Usage: python scripts/ext_ks_pilot.py {lyap|full|resolution|sigma|timing|all}
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import json   # noqa: E402
import sys    # noqa: E402
import time   # noqa: E402
from concurrent.futures import ProcessPoolExecutor   # noqa: E402
from pathlib import Path   # noqa: E402

import numpy as np   # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from th import config   # noqa: E402
from th.ks import KS, kaplan_yorke, block_seed, steps   # noqa: E402

MAX_WORKERS = 40
OUT = config.RESULTS / "ext"
SYS = {  # candidate production settings (pilot); index = proposed system index for seeds
    "ks22": dict(L=22.0, N=64, dt=0.1, index=6, burn=1000.0, n_exp=14, T=20000.0, renorm=10),
    "ks100": dict(L=100.0, N=256, dt=0.1, index=7, burn=500.0, n_exp=40, T=10000.0, renorm=5),
}
LYAP_BASE, PILOT_BASE = 50000, 60000
N_STARTS = 16


def embed(v, N_to):
    """Spectral embedding of rfft coefficients from grid N_from to N_to (same field, zero-padded)."""
    N_from = 2 * (v.shape[-1] - 1)
    out = np.zeros(v.shape[:-1] + (N_to // 2 + 1,), complex)
    K = min(v.shape[-1], out.shape[-1])
    out[..., :K] = v[..., :K] * (N_to / N_from)
    return out


def start(name, block_base, stream, n, N_to=None, dt=None):
    """Small random start(s) on the production grid, embedded in the target grid, then burned in on the target config."""
    s = SYS[name]
    base = KS(s["L"], s["N"], s["dt"])
    rng = np.random.default_rng(block_seed(block_base, s["index"], stream))
    v = base.small_random_start(rng, n)
    ks = KS(s["L"], N_to or s["N"], dt or s["dt"])
    if ks.N != base.N:
        v = embed(v, ks.N) * ks.mask
    return ks, ks.flow(v, steps(s["burn"], ks.dt))


def lyap_job(args):
    name, N, dt, stream, n_exp, T, renorm = args
    ks, v = start(name, LYAP_BASE, stream, 1, N, dt)
    t0 = time.time()
    spec = ks.benettin(v, T, n_exp, renorm_every=renorm, rng=np.random.default_rng(1000 + stream))[0]
    return dict(name=name, N=N, dt=dt, stream=stream, spec=spec.tolist(), trace=ks.trace, dim=ks.dim,
                T=T, secs=time.time() - t0)


def summarize(rows):
    spec = np.array([r["spec"] for r in rows])
    mean = spec.mean(0)
    se = spec.std(0, ddof=1) / np.sqrt(len(spec))
    r0 = rows[0]
    out = dict(N=r0["N"], dt=r0["dt"], T=r0["T"], n_starts=len(rows), n_exp=spec.shape[1], dim=r0["dim"],
               spectrum=mean.tolist(), spectrum_se=se.tolist(), lam_max=float(mean[0]), lam_max_se=float(se[0]),
               lam_max_per_start=spec[:, 0].tolist(), d_ky=kaplan_yorke(mean),
               d_ky_per_start=[kaplan_yorke(s) for s in spec], secs_per_start=float(np.mean([r["secs"] for r in rows])))
    dk = np.array(out["d_ky_per_start"])
    out["d_ky_se"] = float(np.nanstd(dk, ddof=1) / np.sqrt(np.isfinite(dk).sum()))
    if spec.shape[1] == r0["dim"]:
        sums = spec.sum(1)
        out.update(trace=r0["trace"], sum=float(mean.sum()), sum_minus_trace=float(mean.sum() - r0["trace"]),
                   rel_sum_error=float((mean.sum() - r0["trace"]) / abs(r0["trace"])),
                   per_start_sum_max_abs_err=float(np.abs(sums - r0["trace"]).max()))
    return out


def run_jobs(jobs):
    rows = []
    with ProcessPoolExecutor(min(MAX_WORKERS, len(jobs))) as ex:
        for r in ex.map(lyap_job, jobs):
            rows.append(r)
    grouped = {}
    for r in rows:
        grouped.setdefault((r["name"], r["N"], r["dt"], len(r["spec"])), []).append(r)
    return {f"{k[0]}_N{k[1]}_dt{k[2]:g}_p{k[3]}": summarize(v) for k, v in grouped.items()}


def lyap():
    jobs = []
    for name, s in SYS.items():
        for N, dt in [(s["N"], s["dt"]), (s["N"], s["dt"] / 2), (2 * s["N"], s["dt"])]:
            renorm = s["renorm"] * (2 if dt < s["dt"] else 1)
            jobs += [(name, N, dt, i, s["n_exp"], s["T"], renorm) for i in range(N_STARTS)]
    return run_jobs(jobs)


def full():
    """Full retained spectrum (2M exponents) at small dt for the sum-versus-trace check."""
    jobs = []
    s = SYS["ks22"]
    for dt in (0.02, 0.01, 0.005):
        jobs += [("ks22", s["N"], dt, i, (s["N"] - 1) // 3 * 2, 500.0, 1) for i in range(N_STARTS)]
    s = SYS["ks100"]
    jobs += [("ks100", s["N"], 0.01, i, (s["N"] - 1) // 3 * 2, 200.0, 1) for i in range(8)]
    return run_jobs(jobs)


def full_fine():
    """Sum-versus-trace convergence in dt: L = 22 at dt = 0.0025, L = 100 at dt = 0.005, and L = 22 at the production
    dt (documents that the discrete map's most stiff exponents differ from the continuous ones at large dt)."""
    jobs = []
    s = SYS["ks22"]
    jobs += [("ks22", s["N"], 0.0025, i, (s["N"] - 1) // 3 * 2, 500.0, 1) for i in range(N_STARTS)]
    jobs += [("ks22", s["N"], s["dt"], i, (s["N"] - 1) // 3 * 2, 500.0, 1) for i in range(N_STARTS)]
    s = SYS["ks100"]
    jobs += [("ks100", s["N"], 0.005, i, (s["N"] - 1) // 3 * 2, 200.0, 1) for i in range(8)]
    return run_jobs(jobs)


def res_job(args):
    name, N, dt, times = args
    s = SYS[name]
    # identical starts for all configs (pilot block stream 1, 64 starts): burn on the production config, then embed
    ks = KS(s["L"], N, dt)
    ks0, v0 = start(name, PILOT_BASE, 1, 64)
    v = embed(v0, N) * ks.mask if N != ks0.N else v0.copy()
    snaps, t_prev = {}, 0.0
    for t in times:
        v = ks.flow(v, steps(t - t_prev, dt))
        t_prev = t
        snaps[t] = ks.to_real(v)[:, :: N // s["N"]]    # on the production grid points
    return name, N, dt, snaps


def resolution():
    out = {}
    for name, s in SYS.items():
        times = [1.0, 10.0, 50.0, 100.0]
        cfgs = [(s["N"], s["dt"]), (s["N"], s["dt"] / 2), (2 * s["N"], s["dt"]), (2 * s["N"], s["dt"] / 4)]
        with ProcessPoolExecutor(len(cfgs)) as ex:
            res = list(ex.map(res_job, [(name, N, dt, times) for N, dt in cfgs]))
        ref = {(N, dt): sn for _, N, dt, sn in res}
        base = ref[(s["N"], s["dt"])]
        rows = {}
        for (N, dt), sn in ref.items():
            if (N, dt) == (s["N"], s["dt"]):
                continue
            rows[f"N{N}_dt{dt:g}"] = {f"t{t:g}": dict(
                max_rel=float((np.linalg.norm(base[t] - sn[t], axis=1) / np.linalg.norm(sn[t], axis=1)).max()),
                median_rel=float(np.median(np.linalg.norm(base[t] - sn[t], axis=1) / np.linalg.norm(sn[t], axis=1))))
                for t in times}
        out[name] = dict(prod=dict(N=s["N"], dt=s["dt"]), compared_to_production=rows, n_starts=64)
        # retained-spectrum tail on the production config
        ks, v = start(name, PILOT_BASE, 2, 64)
        amp = np.zeros(ks.K)
        for _ in range(200):
            v = ks.flow(v, steps(1.0, ks.dt))
            amp += np.abs(v).mean(0) / 200
        out[name]["spectrum_tail_ratio_mM_over_max"] = float(amp[ks.M] / amp.max())
        out[name]["spectrum_ratio_m_at_kmax_half"] = float(amp[ks.M // 2] / amp.max())
    return out


def sigma():
    """sigma_A from a pilot sample (pilot block stream 3; not the calibration block): 64 trajectories x 100 states
    every 20 time units after burn-in. Euclidean norm over the N grid points (the tokenized state)."""
    out = {}
    for name, s in SYS.items():
        ks, v = start(name, PILOT_BASE, 3, 64)
        tr, _ = ks.trajectory(v, 100, steps(20.0, ks.dt))
        X = tr[:, 1:].reshape(-1, ks.N)
        d = np.linalg.norm(X - X.mean(0), axis=1)
        per_traj = np.sqrt((np.linalg.norm(tr[:, 1:] - X.mean(0), axis=-1) ** 2).mean(1))
        out[name] = dict(sigma_A=float(np.sqrt((d ** 2).mean())), sigma_A_se=float(per_traj.std(ddof=1) / 8.0),
                         rms_per_point=float(np.sqrt((X ** 2).mean())), mean_norm=float(np.linalg.norm(X.mean(0))),
                         n_states=int(len(X)), n_traj=64, spacing_tu=20.0,
                         min_state_norm=float(np.linalg.norm(X, axis=1).min()))
    return out


def timing():
    """Single-process step rate on a batch of 1,000 states (the panel batch) and 1 fft worker."""
    out = {}
    for name, s in SYS.items():
        ks = KS(s["L"], s["N"], s["dt"])
        v = ks.small_random_start(np.random.default_rng(0), 1000)
        v = ks.flow(v, 5)
        t0 = time.time()
        n = 200
        ks.flow(v, n)
        sec = (time.time() - t0) / n
        out[name] = dict(sec_per_step_batch1000=sec, state_steps_per_sec=1000 / sec)
    return out


if __name__ == "__main__":
    what = sys.argv[1]
    OUT.mkdir(parents=True, exist_ok=True)
    fn = OUT / "ks_pilot.json"
    store = json.loads(fn.read_text()) if fn.exists() else {}
    for w in (["timing", "sigma", "resolution", "full", "lyap"] if what == "all" else [what]):
        t0 = time.time()
        store[w] = globals()[w]()
        store[w + "_wall_secs"] = time.time() - t0
        store["sha"] = config.git_sha()
        store["settings"] = SYS
        fn.write_text(json.dumps(store, indent=1))
        print(w, "done", round(time.time() - t0, 1), "s", flush=True)
