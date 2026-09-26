"""Adapt the Physics data blocks (truth = Kolmogorov with drag alpha from results/drag_calibration.json).

  train <block> <device>   training / validation sets for the learned arms (ap_freeze.yaml data):
                           nominal (Re 40), range (Re ~ U[34, 46] per trajectory); frames every 0.35 tu after a 500-tu
                           burn-in at the trajectory's Re; float32 grids (n_traj, n_frames, 64, 64) + re (n_traj,)
  chaos <Re> <device>      chaos gate at one Re with drag: lambda (renormalized twins, 64 starts x 800 tu after a
                           500-tu burn-in, 20-tu transient) with a 95% interval over starts, and sigma_A (64 trajectories,
                           200 states every 1.4 tu)
  test <Re> <device>       test panel (after the freeze): 300 independent trajectories; burn-in 500 tu at Re 40; frames
                           k = -10..0 at Re 40; the change to the test Re at t_c = t_0 + u * 0.35 (u ~ U(0,1) per
                           trajectory, rounded to the 0.01 step); truth frames k = 1 .. 23 + F_max stored as float64
                           grids; noisy observations for k = -10..23 (2% sigma_A(test Re) white noise, noise block)

Seeds: ap.config.seed(block, stream); streams listed in ap_freeze.yaml data.
"""
import json
import math
import sys
import time
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ap import config  # noqa: E402
from ap.solver import KolmoDrag, lyapunov, obs_noise, STEPS_PER_OBS, UNIT  # noqa: E402

BURN = 500.0
SETS = {  # name: (block, stream, n_traj, n_frames, Re spec)
    "train_nominal": ("training", 0, 512, 200, 40.0),
    "train_range": ("training", 1, 1024, 200, (34.0, 46.0)),
    "val_nominal": ("validation", 0, 64, 100, 40.0),
    "val_range": ("validation", 1, 128, 100, (34.0, 46.0)),
}
TEST_RE = {36: 0, 38: 1, 40: 2, 44: 3, 50: 4}      # test Re -> stream
PRE, WMAX = 10, 23


def alpha():
    return float(json.loads((config.RESULTS / "drag_calibration.json").read_text())["alpha"])


def gen_set(name, device, chunk=256):
    block, stream, n, nf, respec = SETS[name]
    rng = np.random.default_rng(config.seed(block, stream))
    re = np.full(n, respec) if isinstance(respec, float) else rng.uniform(*respec, n)
    m = KolmoDrag(re[:1], alpha=alpha(), device=device)
    wh_all = m.random_ic(rng, n)
    config.CACHE.mkdir(parents=True, exist_ok=True)
    X = np.lib.format.open_memmap(config.CACHE / f"{name}.npy", mode="w+", dtype=np.float32, shape=(n, nf, 64, 64))
    t0 = time.time()
    for i in range(0, n, chunk):
        m.set_re(re[i:i + chunk])
        wh = m.flow(wh_all[i:i + chunk], int(BURN / m.dt))
        for k in range(nf):
            wh = m.flow(wh, STEPS_PER_OBS)
            X[i:i + chunk, k] = m.to_phys(wh).cpu().numpy()
        print(name, i + chunk, round(time.time() - t0), flush=True)
    X.flush()
    np.save(config.CACHE / f"{name}_re.npy", re)
    upd("data_blocks.json", {name: dict(block=block, stream=stream, seed=config.seed(block, stream), n_traj=n,
                                        n_frames=nf, re=respec, burn_in=BURN, unit=UNIT, seconds=time.time() - t0)})


def upd(fname, d):
    """Locked read-modify-write (several data jobs update the same file)."""
    import fcntl
    fn = config.RESULTS / fname
    config.RESULTS.mkdir(parents=True, exist_ok=True)
    with open(config.RESULTS / f".{fname}.lock", "w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        s = json.loads(fn.read_text()) if fn.exists() else {}
        s.update(d)
        s["git_sha"] = config.git_sha()
        fn.write_text(json.dumps(s, indent=1))


def chaos(Re, device):
    Re = float(Re)
    t0 = time.time()
    m = KolmoDrag(np.full(64, Re), alpha=alpha(), device=device)
    wh = m.random_ic(np.random.default_rng(config.seed("lyapunov", int(Re))), 64)
    wh = m.flow(wh, int(BURN / m.dt))
    # sigma_A: 200 states every 1.4 tu per trajectory
    S = []
    w2 = wh.clone()
    for _ in range(200):
        w2 = m.flow(w2, 140)
        S.append(m.to_phys(w2).cpu().numpy())
    S = np.stack(S, 1).reshape(-1, 4096)
    mu = S.mean(0)
    d2 = ((S - mu) ** 2).sum(1)
    sA = float(np.sqrt(d2.mean()))
    per = np.sqrt(d2.reshape(64, -1).mean(1))
    lam = lyapunov(m, wh, t_total=800.0, rng=np.random.default_rng(config.seed("lyapunov", 100 + int(Re))))
    se = float(lam.std(ddof=1) / math.sqrt(len(lam)))
    out = dict(Re=Re, alpha=alpha(), lam=float(lam.mean()), lam_se=se, lam_ci95=[float(lam.mean() - 1.96 * se),
               float(lam.mean() + 1.96 * se)], lam_min_start=float(lam.min()), sigma_A=sA,
               sigma_A_traj_sd=float(per.std(ddof=1)), n_starts=64, t_lyap=800.0, chaotic=bool(lam.mean() - 1.96 * se > 0),
               seconds=time.time() - t0)
    upd("chaos_gate.json", {f"Re{Re:g}": out})
    print(out, flush=True)


def test(Re, device):
    Re = int(Re)
    cg = json.loads((config.RESULTS / "chaos_gate.json").read_text())[f"Re{Re:g}"]
    sA, lam = cg["sigma_A"], cg["lam"]
    F = int(math.ceil(10.0 / lam / UNIT))
    n = 300
    stream = TEST_RE[Re]
    rng = np.random.default_rng(config.seed("test", stream))
    u = rng.uniform(0, 1, n)
    m = KolmoDrag(np.full(n, 40.0), alpha=alpha(), device=device)
    wh = m.random_ic(rng, n)
    t0 = time.time()
    wh = m.flow(wh, int(BURN / m.dt))
    nk = PRE + 1 + WMAX + F
    T = np.lib.format.open_memmap(config.CACHE / f"test_Re{Re}.npy", mode="w+", dtype=np.float64, shape=(nk, n, 64, 64))
    T[0] = m.to_phys(wh).cpu().numpy()                     # k = -10
    for j in range(1, PRE + 1):                            # k = -9 .. 0
        wh = m.flow(wh, STEPS_PER_OBS)
        T[j] = m.to_phys(wh).cpu().numpy()
    # change inside (t_0, t_0 + 0.35]: s steps at Re 40 then 35 - s at the test Re
    s = np.clip(np.round(u * STEPS_PER_OBS).astype(int), 1, STEPS_PER_OBS)
    out = torch.empty_like(wh)
    for sv in np.unique(s):
        idx = torch.as_tensor(np.where(s == sv)[0], device=wh.device)
        m1 = KolmoDrag(np.full(len(idx), 40.0), alpha=alpha(), device=device)
        x = m1.flow(wh[idx], int(sv))
        m1.set_re(np.full(len(idx), float(Re)))
        out[idx] = m1.flow(x, STEPS_PER_OBS - int(sv))
    wh = out
    m.set_re(np.full(n, float(Re)))
    T[PRE + 1] = m.to_phys(wh).cpu().numpy()               # k = 1
    for j in range(PRE + 2, nk):
        wh = m.flow(wh, STEPS_PER_OBS)
        T[j] = m.to_phys(wh).cpu().numpy()
    T.flush()
    nrng = np.random.default_rng(config.seed("noise", stream))
    Y = (np.asarray(T[:PRE + 1 + WMAX]) + obs_noise(nrng, (PRE + 1 + WMAX, n, 64, 64), sA)).astype(np.float64)
    np.save(config.CACHE / f"test_Re{Re}_obs.npy", Y)
    upd("test_panels.json", {f"Re{Re}": dict(Re=Re, n=n, seed=config.seed("test", stream),
                                             noise_seed=config.seed("noise", stream), t_c_offset_steps=s.tolist(),
                                             frames_stored=nk, k_first=-PRE, F=F, lam=lam, sigma_A=sA,
                                             noise_rel=0.02, seconds=time.time() - t0)})
    print("test", Re, "done", round(time.time() - t0), flush=True)


if __name__ == "__main__":
    torch.set_num_threads(8)
    cmd = sys.argv[1]
    if cmd == "train":
        gen_set(sys.argv[2], sys.argv[3])
    elif cmd == "chaos":
        chaos(sys.argv[2], sys.argv[3])
    elif cmd == "test":
        test(sys.argv[2], sys.argv[3])
