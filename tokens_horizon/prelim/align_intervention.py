"""Matched perturbation intervention for r (review v2, point 6).

Same initial states and matched error magnitudes; three error orientations:
  fresh    - direction of a 1,024-code k-means codebook's error at that state
  aligned  - leading growing direction, from a tangent vector evolved along the trajectory for 10 time units
  random   - isotropic
r(delta) = (d(lambda*T)/d ln(1/delta))^-1, from mean VPT on a delta grid.
If aligned errors give r ~ 1 at codebook precision while fresh errors give r > 1, orientation explains the excess.
"""
import json
import numpy as np
from sklearn.cluster import KMeans
from systems import lorenz_f, rk4, rk4_tangent, sample_attractor, DT

LY = json.load(open("lyap.json")); lam = LY["lorenz28"]["lam_max"]
f, jac, _ = lorenz_f(28.0); off = np.array([1.0, 1.0, 20.0])
EPS = 0.3; T_MAX = 25.0
rng = np.random.default_rng(11)
train = sample_attractor(f, 3, 100, 800, 10, seed=10, offset=off)
sA = float(np.sqrt(((train - train.mean(0)) ** 2).sum(1).mean()))
km = KMeans(n_clusters=1024, n_init=1, max_iter=60, random_state=0).fit(train)

n = 600
x = off + rng.standard_normal((n, 3))
for _ in range(4000):
    x = rk4(f, x)
v = rng.standard_normal((n, 3, 1)); v /= np.linalg.norm(v, axis=1, keepdims=True)
for s in range(1000):                       # 10 time units ~ 9 Lyapunov times
    x, v = rk4_tangent(f, jac, x, v)
    if s % 10 == 0:
        v /= np.linalg.norm(v, axis=1, keepdims=True)
ic = x.copy()
d_al = v[:, :, 0] / np.linalg.norm(v[:, :, 0], axis=1, keepdims=True)
d_al *= rng.choice([-1.0, 1.0], size=(n, 1))
d_fr = km.cluster_centers_[km.predict(ic)] - ic; d_fr /= np.linalg.norm(d_fr, axis=1, keepdims=True)
d_rn = rng.standard_normal((n, 3)); d_rn /= np.linalg.norm(d_rn, axis=1, keepdims=True)
deltas = np.logspace(-0.5, -4, 15)
out = dict(lam=lam, deltas=deltas.tolist())
for tag, d in [("fresh", d_fr), ("aligned", d_al), ("random", d_rn)]:
    X = np.tile(ic, (len(deltas), 1)); Xh = np.concatenate([ic + dl * sA * d for dl in deltas])
    vpt = np.full(len(X), np.nan)
    for s in range(1, int(T_MAX / DT) + 1):
        X, Xh = rk4(f, X), rk4(f, Xh)
        err = np.linalg.norm(Xh - X, axis=1) / sA
        hit = np.isnan(vpt) & (err > EPS); vpt[hit] = s * DT
    vpt[np.isnan(vpt)] = T_MAX
    m = lam * vpt.reshape(len(deltas), n).mean(1)
    r = 1 / np.gradient(m, np.log(1 / deltas))
    out[tag] = dict(lamvpt=m.tolist(), r=r.tolist())
    print(tag, " ".join(f"{dl:.0e}:{mm:.2f}/r{rr:.2f}" for dl, mm, rr in zip(deltas, m, r)), flush=True)
json.dump(out, open("align_intervention.json", "w"), indent=1)
