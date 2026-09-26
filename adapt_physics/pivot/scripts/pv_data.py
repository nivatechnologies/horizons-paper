"""Pivot data (pivot/pv_freeze.yaml worlds): World D = stage-1 truth (drag alpha); World C = World D + the Codex term
(topographic beta, pivot/results/beta_calibration.json). Same generation code and seed scheme as scripts/ap_data.py,
with World C on streams offset by 10 (training/validation/test/noise) and Lyapunov streams offset by 200.

  chaos <world> <Re> <device>   lambda (64 starts x 800 tu, 95% interval) and sigma_A for one Re
  train <world> <set> <device>  set in train_nominal, val_nominal, train_range, val_range (sizes as stage 1)
  test <world> <Re> <device>    300-trajectory test panel (after the pivot freeze)

World D reuses the stage-1 chaos gate, training/validation sets and test panels (Re 36/40/44/50); only Re 56 is new
(test stream 5). Files: runs/cache/<name>[_C].npy; results: pivot/results/chaos_gate_<world>.json,
pivot/results/test_panels_<world>.json, pivot/results/data_blocks_C.json.
"""
import fcntl
import json
import math
import sys
import time
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from ap import config  # noqa: E402
from ap.solver import KolmoDrag, lyapunov, obs_noise, STEPS_PER_OBS  # noqa: E402

RES = config.PKG / "pivot" / "results"
BURN, PRE, WMAX = 500.0, 10, 23
SETS = {"train_nominal": ("training", 0, 512, 200, 40.0), "train_range": ("training", 1, 1024, 200, (34.0, 46.0)),
        "val_nominal": ("validation", 0, 64, 100, 40.0), "val_range": ("validation", 1, 128, 100, (34.0, 46.0))}
TEST_STREAM = {36: 0, 38: 1, 40: 2, 44: 3, 50: 4, 56: 5, 54: 6}
OFF = {"D": 0, "C": 10}


def world(w):
    alpha = float(config.freeze()["drag"]["alpha"])
    beta = 0.0 if w == "D" else float(json.loads((RES / "beta_calibration.json").read_text())["beta"])
    return alpha, beta


def upd(fname, d):
    RES.mkdir(parents=True, exist_ok=True)
    fn = RES / fname
    with open(RES / f".{fname}.lock", "w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        s = json.loads(fn.read_text()) if fn.exists() else {}
        s.update(d)
        s["git_sha"] = config.git_sha()
        fn.write_text(json.dumps(s, indent=1))


def sfx(w):
    return "" if w == "D" else "_C"


def chaos(w, Re, device):
    Re = float(Re)
    alpha, beta = world(w)
    t0 = time.time()
    m = KolmoDrag(np.full(64, Re), alpha=alpha, beta=beta, device=device)
    loff = 0 if w == "D" else 200
    wh = m.random_ic(np.random.default_rng(config.seed("lyapunov", int(Re) + loff)), 64)
    wh = m.flow(wh, int(BURN / m.dt))
    S, w2 = [], wh.clone()
    for _ in range(200):
        w2 = m.flow(w2, 140)
        S.append(m.to_phys(w2).cpu().numpy())
    S = np.stack(S, 1).reshape(-1, 4096)
    d2 = ((S - S.mean(0)) ** 2).sum(1)
    sA = float(np.sqrt(d2.mean()))
    lam = lyapunov(m, wh, t_total=800.0, rng=np.random.default_rng(config.seed("lyapunov", 100 + int(Re) + loff)))
    se = float(lam.std(ddof=1) / math.sqrt(len(lam)))
    out = dict(world=w, Re=Re, alpha=alpha, beta=beta, lam=float(lam.mean()), lam_se=se,
               lam_ci95=[float(lam.mean() - 1.96 * se), float(lam.mean() + 1.96 * se)], lam_min_start=float(lam.min()),
               sigma_A=sA, n_starts=64, t_lyap=800.0, chaotic=bool(lam.mean() - 1.96 * se > 0), seconds=time.time() - t0)
    upd(f"chaos_gate_{w}.json", {f"Re{Re:g}": out})
    print(out, flush=True)


def gen_set(w, name, device, chunk=256):
    alpha, beta = world(w)
    block, stream, n, nf, respec = SETS[name]
    stream += OFF[w]
    rng = np.random.default_rng(config.seed(block, stream))
    re = np.full(n, respec) if isinstance(respec, float) else rng.uniform(*respec, n)
    m = KolmoDrag(re[:1], alpha=alpha, beta=beta, device=device)
    wh_all = m.random_ic(rng, n)
    X = np.lib.format.open_memmap(config.CACHE / f"{name}{sfx(w)}.npy", mode="w+", dtype=np.float32, shape=(n, nf, 64, 64))
    t0 = time.time()
    for i in range(0, n, chunk):
        m.set_re(re[i:i + chunk])
        wh = m.flow(wh_all[i:i + chunk], int(BURN / m.dt))
        for k in range(nf):
            wh = m.flow(wh, STEPS_PER_OBS)
            X[i:i + chunk, k] = m.to_phys(wh).cpu().numpy()
        print(name, w, min(i + chunk, n), round(time.time() - t0), flush=True)
    X.flush()
    np.save(config.CACHE / f"{name}{sfx(w)}_re.npy", re)
    upd(f"data_blocks_{w}.json", {name: dict(block=block, stream=stream, seed=config.seed(block, stream), n_traj=n,
                                             n_frames=nf, re=respec, alpha=alpha, beta=beta, seconds=time.time() - t0)})


def test(w, Re, device):
    Re = int(Re)
    alpha, beta = world(w)
    cg = json.loads((RES / f"chaos_gate_{w}.json").read_text())[f"Re{Re}"] if (w == "C" or Re == 56) else \
        json.loads((config.RESULTS / "chaos_gate.json").read_text())[f"Re{Re}"]
    sA, lam = cg["sigma_A"], cg["lam"]
    F = int(math.ceil(10.0 / lam / 0.35))
    n = 300
    stream = TEST_STREAM[Re] + OFF[w]
    rng = np.random.default_rng(config.seed("test", stream))
    u = rng.uniform(0, 1, n)
    m = KolmoDrag(np.full(n, 40.0), alpha=alpha, beta=beta, device=device)
    wh = m.random_ic(rng, n)
    t0 = time.time()
    wh = m.flow(wh, int(BURN / m.dt))
    nk = PRE + 1 + WMAX + F
    T = np.lib.format.open_memmap(config.CACHE / f"test_Re{Re}{sfx(w)}.npy", mode="w+", dtype=np.float64, shape=(nk, n, 64, 64))
    T[0] = m.to_phys(wh).cpu().numpy()
    for j in range(1, PRE + 1):
        wh = m.flow(wh, STEPS_PER_OBS)
        T[j] = m.to_phys(wh).cpu().numpy()
    s = np.clip(np.round(u * STEPS_PER_OBS).astype(int), 1, STEPS_PER_OBS)
    out = torch.empty_like(wh)
    for sv in np.unique(s):
        idx = torch.as_tensor(np.where(s == sv)[0], device=wh.device)
        m1 = KolmoDrag(np.full(len(idx), 40.0), alpha=alpha, beta=beta, device=device)
        x = m1.flow(wh[idx], int(sv))
        m1.set_re(np.full(len(idx), float(Re)))
        out[idx] = m1.flow(x, STEPS_PER_OBS - int(sv))
    wh = out
    m.set_re(np.full(n, float(Re)))
    T[PRE + 1] = m.to_phys(wh).cpu().numpy()
    for j in range(PRE + 2, nk):
        wh = m.flow(wh, STEPS_PER_OBS)
        T[j] = m.to_phys(wh).cpu().numpy()
    T.flush()
    nrng = np.random.default_rng(config.seed("noise", stream))
    Y = np.asarray(T[:PRE + 1 + WMAX]) + obs_noise(nrng, (PRE + 1 + WMAX, n, 64, 64), sA)
    np.save(config.CACHE / f"test_Re{Re}{sfx(w)}_obs.npy", Y)
    upd(f"test_panels_{w}.json", {f"Re{Re}": dict(world=w, Re=Re, n=n, seed=config.seed("test", stream),
                                                  noise_seed=config.seed("noise", stream), frames_stored=nk, F=F, lam=lam,
                                                  sigma_A=sA, alpha=alpha, beta=beta, t_c_offset_steps=s.tolist(),
                                                  seconds=time.time() - t0)})
    print("test", w, Re, "done", round(time.time() - t0), flush=True)


if __name__ == "__main__":
    torch.set_num_threads(8)
    c = sys.argv[1]
    if c == "chaos":
        chaos(sys.argv[2], sys.argv[3], sys.argv[4])
    elif c == "train":
        gen_set(sys.argv[2], sys.argv[3], sys.argv[4])
    elif c == "test":
        test(sys.argv[2], sys.argv[3], sys.argv[4])
