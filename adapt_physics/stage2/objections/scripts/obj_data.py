"""Objections WO, Part 1 data: World V = World D with drag tied to viscosity, alpha(Re) = alpha0 * 40 / Re
(obj_freeze.yaml). Same generation code as stage2/scripts/s2_data.py; streams never used before:
test/noise stream 40 (Re 50 panel), training/validation stream 3 (L_range_V data), Lyapunov streams 500/600.

  chaos <device>              lambda and sigma_A at Re 50 in World V
  panel <device>              300 fresh trajectories, Re 40 -> Re 50 at t_c (alpha follows Re), stage-1 observation model
  train <set> <device>        train_range_V (1,024 x 200, Re ~ U[34, 46]) or val_range_V (128 x 100)
Writes runs/cache/obj_V_Re50[_obs].npy, train_range_V.npy, val_range_V.npy; results in stage2/objections/results/.
"""
import fcntl
import json
import math
import sys
import time
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from ap import config  # noqa: E402
from ap.solver import KolmoDrag, lyapunov, obs_noise, STEPS_PER_OBS  # noqa: E402

RES = config.PKG / "stage2" / "objections" / "results"
BURN, PRE, WMAX = 500.0, 10, 23
TEST_STREAM, TRAIN_STREAM, LYAP = 40, 3, 500


def alpha0():
    return float(config.freeze()["drag"]["alpha"])


def V(re, device, **kw):
    return KolmoDrag(re, alpha=alpha0(), alpha_ref_re=40.0, device=device, **kw)


def upd(fname, d):
    RES.mkdir(parents=True, exist_ok=True)
    fn = RES / fname
    with open(RES / f".{fname}.lock", "w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        s = json.loads(fn.read_text()) if fn.exists() else {}
        s.update(d)
        s["git_sha"] = config.git_sha()
        fn.write_text(json.dumps(s, indent=1))


def chaos(device, Re=50.0):
    t0 = time.time()
    m = V(np.full(64, Re), device)
    wh = m.random_ic(np.random.default_rng(config.seed("lyapunov", LYAP)), 64)
    wh = m.flow(wh, int(BURN / m.dt))
    S, w2 = [], wh.clone()
    for _ in range(200):
        w2 = m.flow(w2, 140)
        S.append(m.to_phys(w2).cpu().numpy())
    S = np.stack(S, 1).reshape(-1, 4096)
    sA = float(np.sqrt(((S - S.mean(0)) ** 2).sum(1).mean()))
    lam = lyapunov(m, wh, t_total=800.0, rng=np.random.default_rng(config.seed("lyapunov", LYAP + 100)))
    se = float(lam.std(ddof=1) / math.sqrt(len(lam)))
    out = dict(world="V", Re=Re, alpha=float(alpha0() * 40 / Re), lam=float(lam.mean()), lam_se=se,
               lam_ci95=[float(lam.mean() - 1.96 * se), float(lam.mean() + 1.96 * se)], sigma_A=sA,
               chaotic=bool(lam.mean() - 1.96 * se > 0), seconds=time.time() - t0)
    upd("chaos_V.json", {"Re50": out})
    print(out, flush=True)


def panel(device, Re=50, n=300):
    cg = json.loads((RES / "chaos_V.json").read_text())["Re50"]
    sA, lam = cg["sigma_A"], cg["lam"]
    F = int(math.ceil(10.0 / lam / 0.35))
    rng = np.random.default_rng(config.seed("test", TEST_STREAM))
    u = rng.uniform(0, 1, n)
    m = V(np.full(n, 40.0), device)
    wh = m.random_ic(rng, n)
    t0 = time.time()
    wh = m.flow(wh, int(BURN / m.dt))
    nk = PRE + 1 + WMAX + F
    stem = "obj_V_Re50"
    T = np.lib.format.open_memmap(config.CACHE / f"{stem}.npy", mode="w+", dtype=np.float64, shape=(nk, n, 64, 64))
    T[0] = m.to_phys(wh).cpu().numpy()
    for j in range(1, PRE + 1):
        wh = m.flow(wh, STEPS_PER_OBS)
        T[j] = m.to_phys(wh).cpu().numpy()
    s = np.clip(np.round(u * STEPS_PER_OBS).astype(int), 1, STEPS_PER_OBS)
    out = torch.empty_like(wh)
    for sv in np.unique(s):
        idx = torch.as_tensor(np.where(s == sv)[0], device=wh.device)
        m1 = V(np.full(len(idx), 40.0), device)
        x = m1.flow(wh[idx], int(sv))
        m1.set_re(np.full(len(idx), float(Re)))            # alpha follows Re (set_re recomputes it)
        out[idx] = m1.flow(x, STEPS_PER_OBS - int(sv))
    wh = out
    m.set_re(np.full(n, float(Re)))
    T[PRE + 1] = m.to_phys(wh).cpu().numpy()
    for j in range(PRE + 2, nk):
        wh = m.flow(wh, STEPS_PER_OBS)
        T[j] = m.to_phys(wh).cpu().numpy()
    T.flush()
    nrng = np.random.default_rng(config.seed("noise", TEST_STREAM))
    Y = np.asarray(T[:PRE + 1 + WMAX]) + obs_noise(nrng, (PRE + 1 + WMAX, n, 64, 64), sA)
    np.save(config.CACHE / f"{stem}_obs.npy", Y)
    upd("test_panels.json", {stem: dict(world="V", Re=Re, amp=1.0, n=n, seed=config.seed("test", TEST_STREAM),
                                        noise_seed=config.seed("noise", TEST_STREAM), frames_stored=nk, F=F, lam=lam, sigma_A=sA,
                                        alpha0=alpha0(), alpha_test=alpha0() * 40 / Re, beta=0.0,
                                        t_c_offset_steps=s.tolist(), seconds=time.time() - t0)})
    print("panel", stem, "done", round(time.time() - t0), flush=True)


def train(name, device, chunk=256):
    block, n, nf = {"train_range_V": ("training", 1024, 200), "val_range_V": ("validation", 128, 100)}[name]
    rng = np.random.default_rng(config.seed(block, TRAIN_STREAM))
    re = rng.uniform(34.0, 46.0, n)
    m = V(re[:1], device)
    wh_all = m.random_ic(rng, n)
    X = np.lib.format.open_memmap(config.CACHE / f"{name}.npy", mode="w+", dtype=np.float32, shape=(n, nf, 64, 64))
    t0 = time.time()
    for i in range(0, n, chunk):
        m.set_re(re[i:i + chunk])
        wh = m.flow(wh_all[i:i + chunk], int(BURN / m.dt))
        for k in range(nf):
            wh = m.flow(wh, STEPS_PER_OBS)
            X[i:i + chunk, k] = m.to_phys(wh).cpu().numpy()
        print(name, min(i + chunk, n), round(time.time() - t0), flush=True)
    X.flush()
    np.save(config.CACHE / f"{name}_re.npy", re)
    upd("data_blocks.json", {name: dict(block=block, stream=TRAIN_STREAM, seed=config.seed(block, TRAIN_STREAM), n_traj=n,
                                        n_frames=nf, re=[34.0, 46.0], alpha="alpha0 * 40 / Re", seconds=time.time() - t0)})


if __name__ == "__main__":
    torch.set_num_threads(8)
    c = sys.argv[1]
    if c == "chaos":
        chaos(sys.argv[2])
    elif c == "panel":
        panel(sys.argv[2])
    elif c == "train":
        train(sys.argv[2], sys.argv[3])
