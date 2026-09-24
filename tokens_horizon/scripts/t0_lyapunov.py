"""Task 0 / 2.1: Lyapunov spectra by Benettin/QR on the lyapunov seed block (no confirmation data).

Writes results/lyapunov.json. lam_max fixes the window W/lam for every horizon; it is copied into freeze.yaml.
Also runs the step-halving check (dt = 0.005) on the same starts.
"""
import json
import sys
from concurrent.futures import ProcessPoolExecutor

import numpy as np

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[1]))
from th import config  # noqa: E402
from th.systems import get_system, benettin, kaplan_yorke  # noqa: E402

T_TOTAL = {"lorenz28": 1000.0, "lorenz45": 1000.0, "l96_5": 1000.0, "l96_6": 1000.0, "l96_10": 500.0, "l96_20": 300.0}
N_STARTS = 16


def one(args):
    name, dt = args
    s = get_system(name)
    rng = np.random.default_rng(config.seed("lyapunov", name))
    x0 = s.gaussian_starts(rng, N_STARTS)
    spec = benettin(s, x0, T_TOTAL[name], dt=dt, burn=int(round(20.0 / dt)))
    mean = spec.mean(0)
    se = spec.std(0, ddof=1) / np.sqrt(len(spec))
    return name, dt, dict(spectrum=mean.tolist(), spectrum_se=se.tolist(), lam_max=float(mean[0]),
                          lam_max_se=float(se[0]), sum=float(mean.sum()), divergence=s.divergence,
                          sum_error=float(mean.sum() - s.divergence),
                          per_start_sum_max_abs_err=float(np.abs(spec.sum(1) - s.divergence).max()),
                          d_ky=kaplan_yorke(mean), d_ky_per_start=[kaplan_yorke(r) for r in spec],
                          t_total=T_TOTAL[name], n_starts=N_STARTS)


if __name__ == "__main__":
    names = list(T_TOTAL)
    jobs = [(n, 0.01) for n in names] + [(n, 0.005) for n in names]
    out = {}
    with ProcessPoolExecutor(len(jobs)) as ex:
        for name, dt, r in ex.map(one, jobs):
            out.setdefault(name, {})[f"dt{dt:g}"] = r
            print(name, dt, round(r["lam_max"], 4), "+-", round(r["lam_max_se"], 4), "sum_err", f"{r['sum_error']:.2e}",
                  "dky", round(r["d_ky"], 3), flush=True)
    config.ensure_dirs()
    (config.RESULTS / "lyapunov.json").write_text(json.dumps(dict(sha=config.git_sha(), systems=out), indent=1))
