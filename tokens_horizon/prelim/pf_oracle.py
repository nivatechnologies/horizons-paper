"""Bayes-optimal use of token history: particle-filter oracle.

The predictor sees tokens k_t = q(x_t) every Delta time units for a context of duration tau,
knows the true dynamics and the partition, and forms the posterior mean of x_0.
It then forecasts by integrating the true system (so the only error is what the
tokens left unknown). This upper-bounds any learned token-conditioned predictor.

Questions: does the horizon gain from history saturate, how does the saturated gain
depend on the frame interval Delta, and is the per-bit slope unchanged by history?
"""
import json, sys, time
import numpy as np
from sklearn.cluster import KMeans
from systems import lorenz_f, rk4, DT
from quant_vpt import vpt_curve, summarize

LYAP = json.load(open("lyap.json"))


def flow(f, x, n_sub):
    for _ in range(n_sub):
        x = rk4(f, x)
    return x


def run(name="lorenz28", rho=28.0, Ns=(16, 64, 256), Deltas=(0.02, 0.05, 0.1),
        taus=(0.0, 0.2, 0.8, 3.2), n_ic=300, M=800, seed=0):
    f, _, _ = lorenz_f(rho)
    lam = LYAP[name]["lam_max"]
    rng = np.random.default_rng(seed)
    off = np.array([1.0, 1.0, 20.0])
    # training cloud for the partition and for initialising particles
    x = off + rng.standard_normal((300, 3))
    x = flow(f, x, 5000)
    train = []
    for _ in range(500):
        x = flow(f, x, 10); train.append(x.copy())
    train = np.concatenate(train)
    sigma_A = float(np.sqrt(((train - train.mean(0)) ** 2).sum(1).mean()))
    out = dict(name=name, lam=lam, sigma_A=sigma_A, results=[])
    for N in Ns:
        km = KMeans(n_clusters=N, n_init=1, max_iter=100, random_state=0).fit(train)
        C = km.cluster_centers_
        lab = km.predict(train)
        members = [np.where(lab == k)[0] for k in range(N)]
        delta_cell = float(np.sqrt(((train - C[lab]) ** 2).sum(1).mean()))
        for Delta in Deltas:
            n_sub = int(round(Delta / DT))
            for tau in taus:
                L = int(round(tau / Delta))
                # true trajectories: start L steps before t=0
                xt = off + rng.standard_normal((n_ic, 3))
                xt = flow(f, xt, 3000)
                hist = [xt.copy()]
                for _ in range(L):
                    xt = flow(f, xt, n_sub); hist.append(xt.copy())
                toks = [km.predict(h) for h in hist]
                # initialise particles from training members of the first observed cell
                P = np.empty((n_ic, M, 3))
                for i in range(n_ic):
                    m = members[toks[0][i]]
                    P[i] = train[rng.choice(m, M)]
                t0 = time.time()
                for j in range(1, L + 1):
                    P = flow(f, P.reshape(-1, 3), n_sub).reshape(n_ic, M, 3)
                    pk = km.predict(P.reshape(-1, 3)).reshape(n_ic, M)
                    inside = (pk == toks[j][:, None]).astype(float)
                    d2 = ((P - C[toks[j]][:, None, :]) ** 2).sum(-1)
                    soft = np.exp(-(d2 - d2.min(1, keepdims=True)) / (delta_cell ** 2))
                    w = inside + 1e-9 * soft
                    w /= w.sum(1, keepdims=True)
                    cdf = np.cumsum(w, 1); cdf[:, -1] = 1.0
                    u = (np.arange(M)[None, :] + rng.random((n_ic, 1))) / M
                    rows = np.arange(n_ic)[:, None]
                    idx = np.searchsorted((cdf + 2 * rows).ravel(), (u + 2 * rows).ravel()).reshape(n_ic, M) - rows * M
                    idx = np.clip(idx, 0, M - 1)
                    P = P[rows, idx]
                    spread = P.std(1, keepdims=True)
                    P = P + 0.05 * spread * rng.standard_normal(P.shape)
                est = P.mean(1)
                ic = hist[-1]
                err = float(np.sqrt(((est - ic) ** 2).sum(1).mean()))
                v = vpt_curve(f, ic, est, sigma_A, 40.0)
                r = dict(N=N, bits=int(np.log2(N)), Delta=Delta, tau=tau, L=L, delta_cell_rel=delta_cell / sigma_A,
                         err_rel=err / sigma_A, vpt=summarize(v[0.3]))
                out["results"].append(r)
                print(f"N={N:4d} Delta={Delta:.2f} tau={tau:4.1f} L={L:3d} err_rel={err/sigma_A:.4f} "
                      f"lamVPT mean={lam*r['vpt']['mean']:.2f} median={lam*r['vpt']['median']:.2f} ({time.time()-t0:.0f}s)",
                      flush=True)
                json.dump(out, open(f"pf_{name}{'_M'+str(M) if M!=800 else ''}.json", "w"), indent=1)


if __name__ == "__main__":
    run()
