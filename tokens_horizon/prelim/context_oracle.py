"""Does token history buy horizon?  (empirical check of the unstable-coordinate argument)

Tokens are observed every model step (Delta = 0.05 time units). The context oracle
estimates the current state as the training-set conditional mean of x_0 given the last
L+1 tokens (k_{-L}, ..., k_0), then integrates the true system exactly. L = 0 is the
plain cell-mean oracle. If past tokens only refine stable/neutral coordinates, the
horizon gain from context is bounded and does not keep growing with L.
"""
import json, sys, time
import numpy as np
from sklearn.cluster import KMeans
from systems import lorenz_f, rk4, DT
from quant_vpt import vpt_curve, summarize

LYAP = json.load(open("lyap.json"))
SUB = 5  # RK4 substeps per model step -> Delta = 0.05


def trajectories(f, n_traj, n_steps, seed, offset):
    rng = np.random.default_rng(seed)
    x = offset + rng.standard_normal((n_traj, 3))
    for _ in range(5000):
        x = rk4(f, x)
    out = np.empty((n_steps, n_traj, 3))
    for t in range(n_steps):
        for _ in range(SUB):
            x = rk4(f, x)
        out[t] = x
    return out  # (T, n_traj, 3)


def run(name, rho, Ns=(16, 64, 256), Ls=(0, 1, 2, 4, 8), n_ic=1000):
    f, _, _ = lorenz_f(rho)
    lam = LYAP[name]["lam_max"]
    off = np.array([1.0, 1.0, 20.0])
    tr = trajectories(f, 400, 1500, 11, off)          # 600k training states, sequential
    te = trajectories(f, n_ic, 40, 21, off)            # test: last state is the IC, 39 steps of history
    flat = tr.reshape(-1, 3)
    sigma_A = float(np.sqrt(((flat - flat.mean(0)) ** 2).sum(1).mean()))
    ic = te[-1]
    out = dict(name=name, lam=lam, sigma_A=sigma_A, results=[])
    for N in Ns:
        km = KMeans(n_clusters=N, n_init=1, max_iter=100, random_state=0).fit(flat[::3])
        ktr = km.predict(flat).reshape(tr.shape[:2])      # (T, n_traj)
        kte = km.predict(te.reshape(-1, 3)).reshape(te.shape[:2])
        for L in Ls:
            if np.log2(N) * (L + 1) > 62:
                continue
            # keys over windows (k_{t-L}, ..., k_t)
            def keys(K, t_idx):
                key = np.zeros(K.shape[1], dtype=np.int64)
                for j in range(L + 1):
                    key = key * N + K[t_idx - j]
                return key
            ktr_keys = np.concatenate([keys(ktr, t) for t in range(L, tr.shape[0])])
            xtr = tr[L:].reshape(-1, 3)
            uk, inv = np.unique(ktr_keys, return_inverse=True)
            means = np.zeros((len(uk), 3)); np.add.at(means, inv, xtr)
            cnt = np.bincount(inv); means /= cnt[:, None]
            kq = keys(kte, te.shape[0] - 1)
            pos = np.searchsorted(uk, kq)
            pos = np.clip(pos, 0, len(uk) - 1)
            hit = (uk[pos] == kq) & (cnt[pos] >= 3)
            est = km.cluster_centers_[kte[-1]].copy()     # back-off: plain cell mean
            est[hit] = means[pos[hit]]
            delta = float(np.sqrt(((est - ic) ** 2).sum(1).mean()))
            v = vpt_curve(f, ic, est, sigma_A, 40.0)
            r = dict(N=N, bits=int(np.log2(N)), L=L, hit_frac=float(hit.mean()), delta_rel=delta / sigma_A,
                     vpt=summarize(v[0.3]))
            out["results"].append(r)
            print(f"[{name}] N={N:4d} L={L} hit={hit.mean():.2f} delta_rel={delta/sigma_A:.4f} "
                  f"lamVPT mean={lam*r['vpt']['mean']:.2f}", flush=True)
    json.dump(out, open(f"ctx_{name}.json", "w"), indent=1)


if __name__ == "__main__":
    run("lorenz28", 28.0)
