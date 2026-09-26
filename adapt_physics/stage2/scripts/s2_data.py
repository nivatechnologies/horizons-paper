"""Stage-2 data (stage2/s2_freeze.yaml). Same generation code as pivot/scripts/pv_data.py; fresh, never-used streams.

  test <world> <Re> <device>        fresh panel: test and noise stream = pivot stream + 20 (World D: 20-25, World C: 30-35)
  test2p <case> <device>            World D two-parameter drift at t_c: Re44_A1.1 (stream 26), Re50_A0.9 (stream 27)
  chaos2p <case> <device>           lambda and sigma_A of a two-parameter system (Lyapunov streams 300+)
  noise5 <world> <Re>               5% sigma_A observations of a fresh panel's truth (noise stream = test stream + 50); CPU
  wide <world> <set> <device>       train_range_wide / val_range_wide: Re ~ U[30, 60] per trajectory (training/validation
                                    stream 2 in D, 12 in C); sizes as train_range / val_range
Files: runs/cache/s2_test_Re<Re>_<world>[.npy|_obs.npy|_obs5.npy], s2_test2p_<case>..., train_range_wide[_C].npy.
Results: stage2/results/{test_panels.json, chaos_2p.json, data_blocks.json}.
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

RES = config.PKG / "stage2" / "results"
PR = config.PKG / "pivot" / "results"
BURN, PRE, WMAX = 500.0, 10, 23
TEST_STREAM = {36: 0, 40: 2, 44: 3, 50: 4, 56: 5}
WOFF = {"D": 20, "C": 30}
CASES = {"Re44_A1.1": (44, 1.1, 26), "Re50_A0.9": (50, 0.9, 27)}


def world(w):
    alpha = float(config.freeze()["drag"]["alpha"])
    beta = 0.0 if w == "D" else float(json.loads((PR / "beta_calibration.json").read_text())["beta"])
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


def system_props(w, Re, case=None):
    if case:
        return json.loads((RES / "chaos_2p.json").read_text())[case]
    if w == "D" and Re != 56:
        return json.loads((config.RESULTS / "chaos_gate.json").read_text())[f"Re{Re}"]
    return json.loads((PR / f"chaos_gate_{w}.json").read_text())[f"Re{Re}"]


def make_panel(w, Re, amp_new, stream, stem, device, n=300):
    alpha, beta = world(w)
    cg = system_props(w, Re, stem.split("s2_test2p_")[-1] if "test2p" in stem else None)
    sA, lam = cg["sigma_A"], cg["lam"]
    F = int(math.ceil(10.0 / lam / 0.35))
    rng = np.random.default_rng(config.seed("test", stream))
    u = rng.uniform(0, 1, n)
    m = KolmoDrag(np.full(n, 40.0), alpha=alpha, beta=beta, device=device)
    wh = m.random_ic(rng, n)
    t0 = time.time()
    wh = m.flow(wh, int(BURN / m.dt))
    nk = PRE + 1 + WMAX + F
    T = np.lib.format.open_memmap(config.CACHE / f"{stem}.npy", mode="w+", dtype=np.float64, shape=(nk, n, 64, 64))
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
        m1.set_amp(np.full(len(idx), amp_new))
        out[idx] = m1.flow(x, STEPS_PER_OBS - int(sv))
    wh = out
    m.set_re(np.full(n, float(Re)))
    m.set_amp(np.full(n, amp_new))
    T[PRE + 1] = m.to_phys(wh).cpu().numpy()
    for j in range(PRE + 2, nk):
        wh = m.flow(wh, STEPS_PER_OBS)
        T[j] = m.to_phys(wh).cpu().numpy()
    T.flush()
    nrng = np.random.default_rng(config.seed("noise", stream))
    Y = np.asarray(T[:PRE + 1 + WMAX]) + obs_noise(nrng, (PRE + 1 + WMAX, n, 64, 64), sA)
    np.save(config.CACHE / f"{stem}_obs.npy", Y)
    upd("test_panels.json", {stem: dict(world=w, Re=Re, amp=amp_new, n=n, seed=config.seed("test", stream),
                                        noise_seed=config.seed("noise", stream), frames_stored=nk, F=F, lam=lam, sigma_A=sA,
                                        alpha=alpha, beta=beta, t_c_offset_steps=s.tolist(), seconds=time.time() - t0)})
    print("panel", stem, "done", round(time.time() - t0), flush=True)


def chaos2p(case, device):
    Re, amp, stream = CASES[case]
    alpha, _ = world("D")
    t0 = time.time()
    m = KolmoDrag(np.full(64, float(Re)), alpha=alpha, device=device, amp=np.full(64, amp))
    wh = m.random_ic(np.random.default_rng(config.seed("lyapunov", 300 + stream)), 64)
    wh = m.flow(wh, int(BURN / m.dt))
    S, w2 = [], wh.clone()
    for _ in range(200):
        w2 = m.flow(w2, 140)
        S.append(m.to_phys(w2).cpu().numpy())
    S = np.stack(S, 1).reshape(-1, 4096)
    sA = float(np.sqrt(((S - S.mean(0)) ** 2).sum(1).mean()))
    m2 = KolmoDrag(np.full(128, float(Re)), alpha=alpha, device=device, amp=np.full(128, amp))   # twins: 2 x 64
    m2.set_re(np.full(64, float(Re)))
    m2.F_hat = m2.F_hat0[None] * torch.full((128, 1, 1), amp, device=m2.device, dtype=m2.dtype)
    lam = lyapunov(m2, wh, t_total=800.0, rng=np.random.default_rng(config.seed("lyapunov", 400 + stream)))
    se = float(lam.std(ddof=1) / math.sqrt(len(lam)))
    out = dict(case=case, Re=Re, amp=amp, alpha=alpha, lam=float(lam.mean()), lam_se=se,
               lam_ci95=[float(lam.mean() - 1.96 * se), float(lam.mean() + 1.96 * se)], sigma_A=sA,
               chaotic=bool(lam.mean() - 1.96 * se > 0), seconds=time.time() - t0)
    upd("chaos_2p.json", {case: out})
    print(out, flush=True)


def noise5(w, Re):
    stem = f"s2_test_Re{Re}_{w}"
    stream = TEST_STREAM[Re] + WOFF[w]
    info = json.loads((RES / "test_panels.json").read_text())[stem]
    T = np.load(config.CACHE / f"{stem}.npy", mmap_mode="r")
    n = T.shape[1]
    nrng = np.random.default_rng(config.seed("noise", stream + 50))
    Y = np.asarray(T[:PRE + 1 + WMAX]) + obs_noise(nrng, (PRE + 1 + WMAX, n, 64, 64), info["sigma_A"], rel=0.05)
    np.save(config.CACHE / f"{stem}_obs5.npy", Y)
    upd("test_panels.json", {stem + "_noise5": dict(noise_rel=0.05, noise_seed=config.seed("noise", stream + 50))})
    print("noise5", stem, flush=True)


def wide(w, name, device, chunk=256):
    alpha, beta = world(w)
    block, n, nf = {"train_range_wide": ("training", 1024, 200), "val_range_wide": ("validation", 128, 100)}[name]
    stream = 2 if w == "D" else 12
    rng = np.random.default_rng(config.seed(block, stream))
    re = rng.uniform(30.0, 60.0, n)
    m = KolmoDrag(re[:1], alpha=alpha, beta=beta, device=device)
    wh_all = m.random_ic(rng, n)
    sfx = "" if w == "D" else "_C"
    X = np.lib.format.open_memmap(config.CACHE / f"{name}{sfx}.npy", mode="w+", dtype=np.float32, shape=(n, nf, 64, 64))
    t0 = time.time()
    for i in range(0, n, chunk):
        m.set_re(re[i:i + chunk])
        wh = m.flow(wh_all[i:i + chunk], int(BURN / m.dt))
        for k in range(nf):
            wh = m.flow(wh, STEPS_PER_OBS)
            X[i:i + chunk, k] = m.to_phys(wh).cpu().numpy()
        print(name, w, min(i + chunk, n), round(time.time() - t0), flush=True)
    X.flush()
    np.save(config.CACHE / f"{name}{sfx}_re.npy", re)
    upd("data_blocks.json", {f"{name}_{w}": dict(block=block, stream=stream, seed=config.seed(block, stream), n_traj=n,
                                                 n_frames=nf, re=[30.0, 60.0], alpha=alpha, beta=beta,
                                                 seconds=time.time() - t0)})


if __name__ == "__main__":
    torch.set_num_threads(8)
    c = sys.argv[1]
    if c == "test":
        w, Re = sys.argv[2], int(sys.argv[3])
        make_panel(w, Re, 1.0, TEST_STREAM[Re] + WOFF[w], f"s2_test_Re{Re}_{w}", sys.argv[4])
    elif c == "test2p":
        Re, amp, stream = CASES[sys.argv[2]]
        make_panel("D", Re, amp, stream, f"s2_test2p_{sys.argv[2]}", sys.argv[3])
    elif c == "chaos2p":
        chaos2p(sys.argv[2], sys.argv[3])
    elif c == "noise5":
        noise5(sys.argv[2], int(sys.argv[3]))
    elif c == "wide":
        wide(sys.argv[2], sys.argv[3], sys.argv[4])
