"""Post-freeze extension, part 2 pilot at the production dt = 0.005 (coordinator decision after the dt = 0.1 pilot).

System properties only: Lyapunov spectra and sum-versus-trace, trajectory halving, step timing. No tokenizer, bound,
decode-and-integrate or confirmation data. Same seeds as scripts/ext_ks_pilot.py (lyapunov block 50000, pilot block
60000, system indices ks22 = 6, ks100 = 7). Adds key "dt0005" to results/ext/ks_pilot.json (other keys kept).

Runs (48 processes at most):
  ks22  full retained spectrum (42 exponents), QR every step, 16 starts x T22 tu  -> lambda_1, D_KY and sum-trace
  ks100 leading 40 exponents, QR every 20 steps (0.1 tu), 16 starts x T100 tu    -> lambda_1, D_KY
  ks100 full retained spectrum (170 exponents), QR every step, 16 starts x 200 tu -> sum-trace (same starts)
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
sys.path.insert(0, str(Path(__file__).resolve().parent))
from th import config   # noqa: E402
from th.ks import KS, block_seed, steps   # noqa: E402
import ext_ks_pilot as P   # noqa: E402

DT = 0.005
T22, T100 = 16000.0, 10000.0
SYSD = {k: dict(v, dt=DT) for k, v in P.SYS.items()}


def start(name, block_base, stream, n, N_to=None, dt=DT):
    """As ext_ks_pilot.start, but burned on the dt = 0.005 configuration (small start drawn on the base grid)."""
    s = SYSD[name]
    base = KS(s["L"], s["N"], DT)
    rng = np.random.default_rng(block_seed(block_base, s["index"], stream))
    v = base.small_random_start(rng, n)
    ks = KS(s["L"], N_to or s["N"], dt)
    if ks.N != base.N:
        v = P.embed(v, ks.N) * ks.mask
    return ks, ks.flow(v, steps(s["burn"], ks.dt))


def lyap_job(args):
    name, N, dt, stream, n_exp, T, renorm = args
    ks, v = start(name, P.LYAP_BASE, stream, 1, N, dt)
    t0 = time.time()
    spec = ks.benettin(v, T, n_exp, renorm_every=renorm, rng=np.random.default_rng(1000 + stream))[0]
    return dict(name=name, N=N, dt=dt, stream=stream, spec=spec.tolist(), trace=ks.trace, dim=ks.dim,
                T=T, secs=time.time() - t0)


def lyap():
    jobs = [("ks22", 64, DT, i, 42, T22, 1) for i in range(16)]
    jobs += [("ks100", 256, DT, i, 40, T100, 20) for i in range(16)]
    jobs += [("ks100", 256, DT, i, 170, 200.0, 1) for i in range(16)]
    rows = []
    with ProcessPoolExecutor(48) as ex:
        for r in ex.map(lyap_job, jobs):
            rows.append(r)
    grouped = {}
    for r in rows:
        grouped.setdefault((r["name"], r["N"], r["dt"], len(r["spec"])), []).append(r)
    return {f"{k[0]}_N{k[1]}_dt{k[2]:g}_p{k[3]}": P.summarize(v) for k, v in grouped.items()}


def res_job(args):
    name, N, dt, times = args
    s = SYSD[name]
    ks = KS(s["L"], N, dt)
    ks0, v0 = start(name, P.PILOT_BASE, 1, 64)
    v = P.embed(v0, N) * ks.mask if N != ks0.N else v0.copy()
    snaps, t_prev = {}, 0.0
    for t in times:
        v = ks.flow(v, steps(t - t_prev, dt))
        t_prev = t
        snaps[t] = ks.to_real(v)[:, :: N // s["N"]]
    return name, N, dt, snaps


def resolution():
    out = {}
    times = [1.0, 10.0, 50.0, 100.0]
    jobs = []
    for name, s in SYSD.items():
        jobs += [(name, N, dt, times) for N, dt in [(s["N"], DT), (s["N"], DT / 2), (2 * s["N"], DT)]]
    with ProcessPoolExecutor(len(jobs)) as ex:
        res = list(ex.map(res_job, jobs))
    for name, s in SYSD.items():
        ref = {(N, dt): sn for nm, N, dt, sn in res if nm == name}
        base = ref[(s["N"], DT)]
        rows = {}
        for (N, dt), sn in ref.items():
            if (N, dt) == (s["N"], DT):
                continue
            rel = {t: np.linalg.norm(base[t] - sn[t], axis=1) / np.linalg.norm(sn[t], axis=1) for t in times}
            rows[f"N{N}_dt{dt:g}"] = {f"t{t:g}": dict(max_rel=float(rel[t].max()), median_rel=float(np.median(rel[t])))
                                      for t in times}
        out[name] = dict(prod=dict(N=s["N"], dt=DT), compared_to_production=rows, n_starts=64)
    return out


def timing():
    out = {}
    for name, s in SYSD.items():
        ks = KS(s["L"], s["N"], DT)
        v = ks.flow(ks.small_random_start(np.random.default_rng(0), 1000), 5)
        t0 = time.time()
        ks.flow(v, 400)
        sec = (time.time() - t0) / 400
        out[name] = dict(sec_per_step_batch1000=sec, state_steps_per_sec=1000 / sec)
    return out


if __name__ == "__main__":
    what = sys.argv[1:] or ["timing", "resolution", "lyap"]
    fn = P.OUT / "ks_pilot.json"
    for w in what:
        t0 = time.time()
        r = globals()[w]()
        store = json.loads(fn.read_text())
        d = store.setdefault("dt0005", {})
        d[w] = r
        d[w + "_wall_secs"] = time.time() - t0
        d["sha"] = config.git_sha()
        d["settings"] = dict(SYSD, T22=T22, T100=T100)
        fn.write_text(json.dumps(store, indent=1))
        print(w, "done", round(time.time() - t0, 1), "s", flush=True)
