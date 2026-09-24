"""Ideal-tokenizer check: no learning.

For each system:
  1. sample the attractor (train / test splits from independent trajectories)
  2. build tokenizers: k-means VQ codebooks (N = 2^k) and per-dimension uniform grids
  3. measure distortion delta(R) and fit the quantization dimension D_q
  4. oracle forecast: decode the token of x0 to its cell mean, evolve exactly,
     measure valid prediction time (VPT) against the true trajectory
  5. control: random-direction perturbation of the same norm as each IC's quantization error
"""
import json, sys, time
import numpy as np
from sklearn.cluster import KMeans
from systems import lorenz_f, l96_f, rk4, sample_attractor, DT

LYAP = json.load(open("lyap.json"))
EPS = [0.1, 0.3, 0.5]


def vpt_curve(f, x_true0, x_hat0, sigma_A, t_max):
    """Return VPT (time units) for each IC and each eps threshold."""
    n = x_true0.shape[0]
    x, xh = x_true0.copy(), x_hat0.copy()
    vpt = {e: np.full(n, np.nan) for e in EPS}
    e0 = np.linalg.norm(xh - x, axis=1) / sigma_A
    for e in EPS:
        vpt[e][e0 > e] = 0.0
    steps = int(round(t_max / DT))
    for s in range(1, steps + 1):
        x, xh = rk4(f, x), rk4(f, xh)
        err = np.linalg.norm(xh - x, axis=1) / sigma_A
        for e in EPS:
            hit = np.isnan(vpt[e]) & (err > e)
            vpt[e][hit] = s * DT
    for e in EPS:
        vpt[e][np.isnan(vpt[e])] = t_max
    return vpt


def summarize(v):
    return dict(mean=float(np.mean(v)), median=float(np.median(v)),
                q25=float(np.quantile(v, 0.25)), q75=float(np.quantile(v, 0.75)))


def run(name, sysdef, n_train_traj, n_keep, stride, n_ic, t_max, ks, grid_ns, offset):
    f, jac, d = sysdef
    lam = LYAP[name]["lam_max"]
    t0 = time.time()
    train = sample_attractor(f, d, n_train_traj, n_keep, stride, seed=10, offset=offset)
    test = sample_attractor(f, d, 200, 300, stride, seed=20, offset=offset)
    mu = train.mean(0)
    sigma_A = float(np.sqrt(((train - mu) ** 2).sum(1).mean()))
    rng = np.random.default_rng(3)
    ic = test[rng.choice(len(test), n_ic, replace=False)]
    print(f"[{name}] sampled {train.shape} train, {test.shape} test, sigma_A={sigma_A:.3f} ({time.time()-t0:.0f}s)", flush=True)

    out = dict(name=name, d=d, lam=lam, sigma_A=sigma_A, n_train=len(train), vq=[], grid=[])

    # ---- VQ codebooks
    for k in ks:
        N = 2 ** k
        t1 = time.time()
        km = KMeans(n_clusters=N, n_init=1, max_iter=80, tol=1e-5, random_state=k).fit(train)
        C = km.cluster_centers_
        lab_test = km.predict(test)
        delta = float(np.sqrt(((test - C[lab_test]) ** 2).sum(1).mean()))
        counts = np.bincount(lab_test, minlength=N) / len(lab_test)
        p = counts[counts > 0]
        H = float(-(p * np.log2(p)).sum())
        xh0 = C[km.predict(ic)]
        v = vpt_curve(f, ic, xh0, sigma_A, t_max)
        # control: random direction, same norm as each IC's quantization error
        q_err = np.linalg.norm(xh0 - ic, axis=1, keepdims=True)
        u = rng.standard_normal(ic.shape)
        u /= np.linalg.norm(u, axis=1, keepdims=True)
        vc = vpt_curve(f, ic, ic + q_err * u, sigma_A, t_max)
        rec = dict(bits=k, N=N, delta=delta, delta_rel=delta / sigma_A, H_used=H,
                   vpt={str(e): summarize(v[e]) for e in EPS},
                   vpt_rand={str(e): summarize(vc[e]) for e in EPS})
        out["vq"].append(rec)
        print(f"  VQ k={k:2d} delta_rel={delta/sigma_A:.4f} H={H:.2f} "
              f"lamVPT(0.3) med={lam*rec['vpt']['0.3']['median']:.2f} mean={lam*rec['vpt']['0.3']['mean']:.2f} "
              f"rand mean={lam*rec['vpt_rand']['0.3']['mean']:.2f} ({time.time()-t1:.0f}s)", flush=True)

    # ---- per-dimension uniform grid tokenizers (FSQ-like scalar binning)
    lo, hi = train.min(0), train.max(0)
    for n in grid_ns:
        edges = [np.linspace(lo[j], hi[j], n + 1)[1:-1] for j in range(d)]

        def code(X):
            idx = np.stack([np.searchsorted(edges[j], X[:, j]) for j in range(d)], 1)
            return np.ravel_multi_index(idx.T, (n,) * d)

        c_tr = code(train)
        uniq, inv = np.unique(c_tr, return_inverse=True)
        means = np.zeros((len(uniq), d))
        np.add.at(means, inv, train)
        means /= np.bincount(inv)[:, None]
        lookup = dict(zip(uniq.tolist(), range(len(uniq))))

        def decode(X):
            c = code(X)
            out_ = np.empty_like(X)
            for i, ci in enumerate(c):
                j = lookup.get(int(ci))
                if j is None:  # unseen cell: use geometric centre
                    idx = np.unravel_index(ci, (n,) * d)
                    w = (hi - lo) / n
                    out_[i] = lo + (np.array(idx) + 0.5) * w
                else:
                    out_[i] = means[j]
            return out_

        dec_test = decode(test)
        delta = float(np.sqrt(((test - dec_test) ** 2).sum(1).mean()))
        c_te = code(test)
        _, cnt = np.unique(c_te, return_counts=True)
        p = cnt / cnt.sum()
        H = float(-(p * np.log2(p)).sum())
        v = vpt_curve(f, ic, decode(ic), sigma_A, t_max)
        rec = dict(levels=n, bits_nominal=float(d * np.log2(n)), used=int(len(uniq)),
                   bits_used=float(np.log2(len(uniq))), H_used=H, delta=delta, delta_rel=delta / sigma_A,
                   vpt={str(e): summarize(v[e]) for e in EPS})
        out["grid"].append(rec)
        print(f"  grid n={n:2d} nominal={rec['bits_nominal']:.1f} used={rec['bits_used']:.1f} "
              f"delta_rel={delta/sigma_A:.4f} lamVPT(0.3) mean={lam*rec['vpt']['0.3']['mean']:.2f}", flush=True)

    json.dump(out, open(f"quant_{name}.json", "w"), indent=1)
    print(f"[{name}] done in {time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    which = sys.argv[1]
    if which.startswith("lorenz"):
        rho = float(which[len("lorenz"):])
        run(which, lorenz_f(rho), n_train_traj=150, n_keep=1000, stride=10, n_ic=1000,
            t_max=30.0, ks=range(2, 13), grid_ns=[2, 3, 4, 5, 6, 8, 10, 12, 16], offset=np.array([1.0, 1.0, 20.0]))
    else:
        d = int(which.split("_")[1])
        run(which, l96_f(d), n_train_traj=120, n_keep=1000, stride=10, n_ic=1000,
            t_max=15.0, ks=range(2, 13), grid_ns=[2, 3] if d > 10 else [2, 3, 4], offset=8.0)
