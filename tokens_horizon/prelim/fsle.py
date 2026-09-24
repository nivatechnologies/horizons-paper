"""Classical FSLE by scale-crossing times (Aurell et al. 1997), Lorenz-63 rho=28.
One small perturbation per initial state, grown without renormalisation; record first-passage
times through doubling levels. lambda(delta) = ln2 / <tau(delta -> 2 delta)>."""
import json, numpy as np
from sklearn.cluster import KMeans
from systems import lorenz_f, rk4, sample_attractor, DT
LY = json.load(open("lyap.json")); lam = LY["lorenz28"]["lam_max"]
f, _, _ = lorenz_f(28.0); off = np.array([1.0, 1.0, 20.0])
train = sample_attractor(f, 3, 100, 800, 10, seed=10, offset=off)
test = sample_attractor(f, 3, 100, 200, 10, seed=21, offset=off)
sA = float(np.sqrt(((train - train.mean(0)) ** 2).sum(1).mean()))
rng = np.random.default_rng(9); ic = test[rng.choice(len(test), 1000, replace=False)]
km = KMeans(n_clusters=1024, n_init=1, max_iter=60, random_state=0).fit(train)
e = km.cluster_centers_[km.predict(ic)] - ic; e /= np.linalg.norm(e, axis=1, keepdims=True)
levels = 1e-9 * 2.0 ** np.arange(0, 32)          # up to ~2.1 sigma
levels = levels[levels <= 0.6]
x, y = ic.copy(), ic + 1e-9 * sA * e
first = np.full((len(levels), len(ic)), np.nan)
for s in range(1, 4501):
    x, y = rk4(f, x), rk4(f, y)
    err = np.linalg.norm(y - x, axis=1) / sA
    for li, L in enumerate(levels):
        m = np.isnan(first[li]) & (err > L)
        first[li][m] = s * DT
tau = np.diff(first, axis=0)                      # time from level n to n+1
ok = ~np.isnan(tau)
mean_tau = np.array([np.nanmean(t) for t in tau])
fsle = np.log(2) / mean_tau
res = [dict(delta=float(levels[i]), r=float(fsle[i] / lam), frac=float(ok[i].mean())) for i in range(len(mean_tau))]
for r in res:
    if r["delta"] > 1e-5: print(f"delta={r['delta']:.2e}  FSLE/lambda={r['r']:.2f}  n={r['frac']:.2f}")
json.dump(res, open("fsle_lorenz28.json", "w"), indent=1)
