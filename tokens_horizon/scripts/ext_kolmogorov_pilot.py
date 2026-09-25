"""Kolmogorov flow Phase A pilot (post-freeze extension): lambda_1, resolution / dt / precision checks, sigma_A
sample and timings. Touches no confirmation data. All numbers are estimates (pilot).

  python scripts/ext_kolmogorov_pilot.py lyap --N 64 --dt 0.01 --dtype f64 --delta0 1e-6 --tag n64
  python scripts/ext_kolmogorov_pilot.py sample
Seeds: lyapunov block of the proposed Kolmogorov system index (th.kolmogorov.SYSTEM_INDEX); stream 0 gives the
random initial conditions (the same low-mode field on every grid), stream 1 the perturbation directions,
stream 2 the sigma_A / statistics sample.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from th import config  # noqa: E402
from th import kolmogorov as K  # noqa: E402

OUT = config.RESULTS / "ext" / "kolmogorov_pilot"
GPU_GB = 1.2   # allocator cap per process; at most two pilot processes at once (4 GB total incl. contexts)


def device(want):
    if want.startswith("cuda"):
        free, _ = torch.cuda.mem_get_info(0)
        if free < 1.0 * 2 ** 30:
            raise SystemExit(f"cuda:0 has only {free / 2**30:.2f} GB free")
        torch.cuda.set_per_process_memory_fraction(min(1.0, GPU_GB * 2 ** 30 / torch.cuda.mem_get_info(0)[1]), 0)
        return "cuda:0"
    torch.set_num_threads(32)
    return "cpu"


def lyap(a):
    dev = device(a.device)
    dtype = torch.float64 if a.dtype == "f64" else torch.float32
    m = K.Kolmogorov(N=a.N, dt=a.dt, device=dev, dtype=dtype)
    t0 = time.time()
    w = K.burned_starts(m, "lyapunov", a.B, stream=0, burn_time=a.burn)
    t_burn = time.time() - t0
    r = K.lyapunov_twin(m, w, a.T + a.transient, tau=a.tau, delta0=a.delta0, t_transient=a.transient,
                        rng=np.random.default_rng(K.seed("lyapunov", 1)))
    el = time.time() - t0
    lam = r["lam"]
    ntr = int(round(a.transient / a.tau))
    diag = {k: v[:, ntr:] for k, v in r["diag"].items()}
    out = dict(label="estimate (pilot)", system=K.SYSTEM, Re=m.Re, n=m.n, N=a.N, dt=a.dt, dtype=a.dtype,
               device=dev, delta0=a.delta0, tau=a.tau, burn_time=a.burn, transient=a.transient, T=r["t_used"],
               starts=a.B, seed_ic=K.seed("lyapunov", 0), seed_pert=K.seed("lyapunov", 1),
               lam_mean=float(lam.mean()), lam_se=float(lam.std(ddof=1) / np.sqrt(len(lam))),
               lam_sd_per_start=float(lam.std(ddof=1)), lam_per_start=lam.tolist(),
               local_growth_max=float(r["local"].max()),
               stats={k: dict(mean=float(v.mean()), se=float(v.mean(1).std(ddof=1) / np.sqrt(v.shape[0])),
                              per_start=v.mean(1).tolist()) for k, v in diag.items()},
               seconds=el, seconds_burn=t_burn, git=config.git_sha())
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"lyap_{a.tag}.json").write_text(json.dumps(out, indent=1))
    print(a.tag, f"lam = {out['lam_mean']:.5f} +- {out['lam_se']:.5f}", f"{el:.0f}s",
          {k: round(v["mean"], 4) for k, v in out["stats"].items()}, flush=True)


def sample(a):
    """sigma_A pilot sample + spectrum-tail resolution indicator + timings, 64^2 unless --N."""
    dev = device(a.device)
    m = K.Kolmogorov(N=a.N, dt=a.dt, device=dev)
    w = K.burned_starts(m, "lyapunov", a.B, stream=2, burn_time=a.burn)
    every = int(round(a.every / m.dt))
    X = []
    spec = torch.zeros(m.N, dtype=torch.float64, device=m.device)
    kmag = torch.sqrt(m.K2).round().long()
    wgt = torch.full_like(m.K2, 2.0)
    wgt[:, 0] = 1.0
    for s in range(a.S):
        w = m.flow(w, every)
        X.append(m.to_phys(w).cpu().numpy().astype(np.float64))
        e = (wgt * w.abs() ** 2 * m.K2inv).mean(0)            # energy per mode (up to a constant)
        spec.index_add_(0, kmag.flatten(), e.flatten())
    X = np.stack(X, 1)                                          # (B, S, N, N)
    flat = X.reshape(-1, m.N, m.N)
    sA = K.sigma_A(flat)
    per_traj = [K.sigma_A(X[i]) for i in range(len(X))]
    spec = (spec / spec.sum()).cpu().numpy()
    kmax = m.N // 3
    # timings (per state per step), both precisions on this device
    tim = {}
    for dt_name, dtp in (("f64", torch.float64), ("f32", torch.float32)):
        mm = K.Kolmogorov(N=a.N, dt=a.dt, device=dev, dtype=dtp)
        for B in (100, 1000):
            ww = mm.random_ic(np.random.default_rng(0), B)
            ww = mm.flow(ww, 5)
            if dev != "cpu":
                torch.cuda.synchronize()
            t = time.time()
            ww = mm.flow(ww, 200)
            if dev != "cpu":
                torch.cuda.synchronize()
            tim[f"{dt_name}_B{B}_us_per_state_step"] = (time.time() - t) / 200 / B * 1e6
    out = dict(label="estimate (pilot)", N=m.N, dt=m.dt, states=int(flat.shape[0]), trajectories=a.B,
               sample_every=a.every, burn_time=a.burn, seed=K.seed("lyapunov", 2),
               sigma_A=sA, sigma_A_bootstrap_sd=float(np.std([K.sigma_A(flat[np.random.default_rng(i).integers(0, len(flat), len(flat))]) for i in range(50)])),
               sigma_A_per_traj_range=[float(min(per_traj)), float(max(per_traj))],
               omega_rms=float(np.sqrt((flat ** 2).mean())), omega_absmax=float(np.abs(flat).max()),
               mean_field_rms=float(np.sqrt((flat.mean(0) ** 2).mean())),
               energy_spectrum_shell=spec[: kmax + 3].tolist(),
               energy_fraction_above_k_half_cut=float(spec[kmax // 2 + 1:].sum()),
               energy_fraction_last_shell=float(spec[kmax]),
               timings=tim, device=dev,
               peak_gpu_bytes=int(torch.cuda.max_memory_allocated(0)) if dev != "cpu" else 0,
               git=config.git_sha())
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"sample_{a.tag}.json").write_text(json.dumps(out, indent=1))
    print(json.dumps({k: v for k, v in out.items() if k != "energy_spectrum_shell"}, indent=1))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("cmd", choices=["lyap", "sample"])
    p.add_argument("--N", type=int, default=64)
    p.add_argument("--dt", type=float, default=0.01)
    p.add_argument("--dtype", default="f64")
    p.add_argument("--delta0", type=float, default=1e-6)
    p.add_argument("--tau", type=float, default=1.0)
    p.add_argument("--B", type=int, default=128)
    p.add_argument("--T", type=float, default=2000.0)
    p.add_argument("--transient", type=float, default=20.0)
    p.add_argument("--burn", type=float, default=K.BURN_TIME)
    p.add_argument("--S", type=int, default=100)
    p.add_argument("--every", type=float, default=5.0)
    p.add_argument("--device", default="cuda:0")
    p.add_argument("--tag", default="n64")
    a = p.parse_args()
    {"lyap": lyap, "sample": sample}[a.cmd](a)
