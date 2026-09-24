---
created: '2026-09-23'
related:
  - WO_AIConf-Tokens-Horizon-Paper-2026-09-23
status: unratified-input
tags:
  - aiconf-papers
  - tokens-horizon
  - preliminary
title: 'Tokens-horizon paper: preliminary code and reference outputs'
type: results
---
# Tokens-horizon paper: preliminary code and reference outputs

Preliminary scripts written in chat on 2026-09-23 (numpy, scipy, scikit-learn 1.8, matplotlib; float64; 2-core container). Extract each block below into `tokens_horizon/prelim/<filename>` unchanged. Run `lyap.py` first (and `lyap5.py` for Lorenz-96 d = 5 and 6); the other scripts read `lyap.json`. All numbers here are exploratory and are re-estimated on confirmation trajectories under the WO's freeze.

## Reference outputs for the WO Task 0 reproduction check

`paired_bound_v4.py` (Lorenz-63 ρ = 28, 300 states, Δ = 0.02, 1,500 particles, W = 27 Lyapunov times):

| bits | p_0 | bound, future-only | history ref, future-only | decode-and-integrate, future-only | persistence, future-only | reference outlasts bound | bound, from t = 0 | history ref, from t = 0 | filter fallback rate |
|---|---|---|---|---|---|---|---|---|---|
| 4 | 0.267 | 0.123 (0% no cross) | 2.926 | 0.279 | 0.053 | 99.3% | 0.102 | 2.925 | 0.19% |
| 6 | 0.003 | 7.684 (2% no cross) | 3.834 | 0.638 | 0.058 | 16.0% | 7.683 | 3.828 | 0.22% |
| 8 | 0.000 | 25.840 (93% no cross) | 4.247 | 1.070 | 0.062 | 0.0% | 25.840 | 4.247 | 1.27% |

`mse_decomp_v4.py` (Lorenz-63 ρ = 28, all members of each cell of 150,000 states; ensemble-RMSE horizons in Lyapunov times):

| bits | O(0)/I(0), all members | O(0)/I(0), 48 draws | T_info | T_codebook | T_projected_DI | O share at T_info (bias-corrected) | excess share at T_info | min / median cell size |
|---|---|---|---|---|---|---|---|---|
| 4 | 1.8e-09 | 0.0098 | 0.072 | 0.018 | 0.018 | 0.3979 | 0.0000 | 6996 / 8985 |
| 6 | 4.2e-28 | 0.0173 | 0.217 | 0.190 | 0.190 | 0.2029 | 0.0361 | 1299 / 2274 |
| 8 | 3.1e-28 | 0.0203 | 0.334 | 0.334 | 0.325 | 0.0540 | 0.0942 | 153 / 582 |
| 10 | 3.2e-28 | 0.0204 | 0.460 | 0.460 | 0.442 | 0.0128 | 0.2465 | 16 / 148 |

`lyap.py` / `lyap5.py`: λ = 0.9026 (Lorenz-63 ρ = 28), 1.2203 (ρ = 45), 0.4712, 0.9740, 1.2005, 1.5381 (Lorenz-96 d = 5, 6, 10, 20); D_KY = 2.06, 2.08, 2.88, 4.05, 6.50, 13.41.

Other exploratory results (single-frame exchange rate 0.215 Lyapunov times per bit on Lorenz-63 over 6–12 bits; D_eff tracking D_KY within 9%; r = 1.4–1.6 at codebook precision; classical FSLE 0.92–1.10λ; aligned errors r up to 2.2) come from `quant_vpt.py`, `staircase.py`, `rvq_vpt.py`, `pf_oracle.py`, `align_intervention.py`, `fsle.py`, `context_oracle.py` and `review_checks.py`.

Known quirks: `pf_oracle.py` saves `pf_<name>.json` for 800 particles and `pf_<name>_M3000.json` otherwise; `quant_vpt.py` and `staircase.py` take the system name as the first argument (`lorenz28`, `lorenz45`, `l96_5`, `l96_6`, `l96_10`, `l96_20`); `review_checks.py` is superseded by `paired_bound_v4.py` and `mse_decomp_v4.py` for the headline and decomposition and is kept for the step-halving and geometric-mean checks.

## Files

Code blocks follow, one per file, in order: systems.py, lyap.py, lyap5.py, paired_bound_v4.py, mse_decomp_v4.py, quant_vpt.py, staircase.py, rvq_vpt.py, pf_oracle.py, align_intervention.py, fsle.py, context_oracle.py, review_checks.py.

### `systems.py`

```python
"""Systems, integrators and Lyapunov estimation for the preliminary check."""
import numpy as np

DT = 0.01


def lorenz_f(rho, sigma=10.0, beta=8.0 / 3.0):
    def f(x):
        X, Y, Z = x[..., 0], x[..., 1], x[..., 2]
        return np.stack([sigma * (Y - X), X * (rho - Z) - Y, X * Y - beta * Z], axis=-1)

    def jac(x):
        X, Y, Z = x[..., 0], x[..., 1], x[..., 2]
        J = np.zeros(x.shape[:-1] + (3, 3))
        J[..., 0, 0] = -sigma
        J[..., 0, 1] = sigma
        J[..., 1, 0] = rho - Z
        J[..., 1, 1] = -1.0
        J[..., 1, 2] = -X
        J[..., 2, 0] = Y
        J[..., 2, 1] = X
        J[..., 2, 2] = -beta
        return J

    return f, jac, 3


def l96_f(d, F=8.0):
    def f(x):
        return (np.roll(x, -1, -1) - np.roll(x, 2, -1)) * np.roll(x, 1, -1) - x + F

    def jac(x):
        n = x.shape[:-1]
        J = np.zeros(n + (d, d))
        for i in range(d):
            J[..., i, (i + 1) % d] += x[..., (i - 1) % d]
            J[..., i, (i - 2) % d] += -x[..., (i - 1) % d]
            J[..., i, (i - 1) % d] += x[..., (i + 1) % d] - x[..., (i - 2) % d]
            J[..., i, i] += -1.0
        return J

    return f, jac, d


def rk4(f, x, dt=DT):
    k1 = f(x)
    k2 = f(x + 0.5 * dt * k1)
    k3 = f(x + 0.5 * dt * k2)
    k4 = f(x + dt * k3)
    return x + dt / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)


def rk4_tangent(f, jac, x, Q, dt=DT):
    """RK4 for state plus tangent vectors (columns of Q)."""
    def g(x, Q):
        return f(x), jac(x) @ Q
    k1x, k1Q = g(x, Q)
    k2x, k2Q = g(x + 0.5 * dt * k1x, Q + 0.5 * dt * k1Q)
    k3x, k3Q = g(x + 0.5 * dt * k2x, Q + 0.5 * dt * k2Q)
    k4x, k4Q = g(x + dt * k3x, Q + dt * k3Q)
    return (x + dt / 6 * (k1x + 2 * k2x + 2 * k3x + k4x),
            Q + dt / 6 * (k1Q + 2 * k2Q + 2 * k3Q + k4Q))


def sample_attractor(f, d, n_traj, n_keep, stride, burn=5000, seed=0, x0_scale=1.0, offset=0.0):
    rng = np.random.default_rng(seed)
    x = offset + x0_scale * rng.standard_normal((n_traj, d))
    for _ in range(burn):
        x = rk4(f, x)
    out = np.empty((n_keep, n_traj, d))
    for k in range(n_keep):
        for _ in range(stride):
            x = rk4(f, x)
        out[k] = x
    return out.reshape(-1, d)


def lyapunov_spectrum(f, jac, x0, n_exp, t_total=500.0, renorm_every=10, burn=2000):
    """Benettin/QR on a batch of initial points; returns mean and per-trajectory spectra."""
    x = x0.copy()
    for _ in range(burn):
        x = rk4(f, x)
    B, d = x.shape
    Q = np.tile(np.eye(d)[:, :n_exp], (B, 1, 1))
    sums = np.zeros((B, n_exp))
    n_steps = int(round(t_total / DT))
    for s in range(1, n_steps + 1):
        x, Q = rk4_tangent(f, jac, x, Q)
        if s % renorm_every == 0:
            Q, R = np.linalg.qr(Q)
            diag = np.abs(np.diagonal(R, axis1=-2, axis2=-1))
            sums += np.log(diag)
    spec = sums / (n_steps * DT)
    return spec.mean(0), spec
```

### `lyap.py`

```python
import numpy as np, json, time
from systems import *
res = {}
rng = np.random.default_rng(1)
for name, (f, jac, d), nexp, t in [
    ("lorenz28", lorenz_f(28.0), 3, 400.0),
    ("lorenz45", lorenz_f(45.0), 3, 400.0),
    ("l96_10", l96_f(10), 10, 300.0),
    ("l96_20", l96_f(20), 20, 200.0),
]:
    t0 = time.time()
    off = 8.0 if name.startswith("l96") else 0.0
    x0 = off + rng.standard_normal((8, d))
    if name.startswith("lorenz"): x0 = x0 + np.array([1.0, 1.0, 20.0])
    mean, spec = lyapunov_spectrum(f, jac, x0, nexp, t_total=t)
    pos = mean[mean > 0.02]
    # Kaplan-Yorke dimension
    cs = np.cumsum(mean); j = np.max(np.where(cs >= 0)[0]) + 1 if cs[0] >= 0 else 0
    dky = j + (cs[j-1] / abs(mean[j]) if j < len(mean) else 0.0)
    res[name] = dict(spectrum=mean.round(4).tolist(), lam_max=float(mean[0]), lam_max_sd=float(spec[:,0].std()),
                     sum=float(mean.sum()), h_ks=float(pos.sum()), d_ky=float(dky), secs=round(time.time()-t0,1))
    print(name, res[name], flush=True)
json.dump(res, open("lyap.json", "w"), indent=1)
```

### `lyap5.py`

```python
import numpy as np, json
from systems import *
res = json.load(open("lyap.json"))
rng = np.random.default_rng(2)
for d in [5, 6]:
    f, jac, _ = l96_f(d)
    mean, spec = lyapunov_spectrum(f, jac, 8.0 + rng.standard_normal((8, d)), d, t_total=300.0)
    cs = np.cumsum(mean); j = np.max(np.where(cs >= 0)[0]) + 1
    dky = j + (cs[j-1] / abs(mean[j]) if j < len(mean) else 0.0)
    res[f"l96_{d}"] = dict(spectrum=mean.round(4).tolist(), lam_max=float(mean[0]), lam_max_sd=float(spec[:,0].std()),
                          sum=float(mean.sum()), h_ks=float(mean[mean>0.02].sum()), d_ky=float(dky))
    print(d, res[f"l96_{d}"])
json.dump(res, open("lyap.json", "w"), indent=1)
```

### `paired_bound_v4.py`

```python
"""Paired headline check (review v2, point 1 and 4).

Same initial states, same frame grid (Delta = 0.02), scoring from t = 0 on that grid, same window:
  - output-support bound T_out for the codebook
  - history-conditioned reference (particle filter, 3.2 time units of context)
  - decode-and-integrate reference
All reported as restricted means E[min(lambda*T, W)] with W = 27 Lyapunov times, plus the
fraction of initial states that do not cross within the window.
"""
import json, time
import numpy as np
from sklearn.cluster import KMeans
from systems import lorenz_f, rk4, DT

LY = json.load(open("lyap.json")); lam = LY["lorenz28"]["lam_max"]
f, _, _ = lorenz_f(28.0)
off = np.array([1.0, 1.0, 20.0])
EPS = 0.3
DELTA = 0.02; SUB = int(round(DELTA / DT))
TAU = 3.2; L = int(round(TAU / DELTA))
W_LYAP = 27.0; T_WIN = W_LYAP / lam
N_FR = int(np.ceil(T_WIN / DELTA))
rng = np.random.default_rng(42)


def flow(x, n):
    for _ in range(n):
        x = rk4(f, x)
    return x


x = flow(off + rng.standard_normal((300, 3)), 5000)
train = []
for _ in range(500):
    x = flow(x, 10); train.append(x.copy())
train = np.concatenate(train)
sA = float(np.sqrt(((train - train.mean(0)) ** 2).sum(1).mean()))

n_ic, M = 300, 1500
xt = flow(off + rng.standard_normal((n_ic, 3)), 3000)
hist = [xt.copy()]
for _ in range(L):
    xt = flow(xt, SUB); hist.append(xt.copy())
ic = hist[-1]
# true future on the frame grid
fut = [ic.copy()]; y = ic.copy()
for _ in range(N_FR):
    y = flow(y, SUB); fut.append(y.copy())
fut = np.array(fut)  # (N_FR+1, n_ic, 3)


def first_cross(err_fn, start):
    """first frame index >= start where err_fn(j) > eps; restricted to the window. Returns lambda*T (from t=0 clock) and censor flags."""
    first = np.full(n_ic, np.nan)
    for j in range(start, N_FR + 1):
        e = err_fn(j)
        hit = np.isnan(first) & (e > EPS); first[hit] = j
    cens = np.isnan(first); first[cens] = N_FR
    return lam * first * DELTA, cens


def traj_of(xhat0):
    z = xhat0.copy(); out_ = [z.copy()]
    for _ in range(N_FR):
        z = flow(z, SUB); out_.append(z.copy())
    return np.array(out_)


out = dict(delta=DELTA, tau=TAU, window_lyap=W_LYAP, n_ic=n_ic, particles=M, rows=[])
for N in (16, 64, 256):
    t0 = time.time()
    km = KMeans(n_clusters=N, n_init=1, max_iter=100, random_state=0).fit(train)
    C = km.cluster_centers_; lab = km.predict(train)
    members = [np.where(lab == k)[0] for k in range(N)]
    dcell = float(np.sqrt(((train - C[lab]) ** 2).sum(1).mean()))
    toks = [km.predict(h) for h in hist]
    # particle filter (indicator likelihood; soft fallback counted)
    P = np.stack([train[rng.choice(members[toks[0][i]], M)] for i in range(n_ic)])
    fallbacks = 0
    for j in range(1, L + 1):
        P = flow(P.reshape(-1, 3), SUB).reshape(n_ic, M, 3)
        pk = km.predict(P.reshape(-1, 3)).reshape(n_ic, M)
        inside = (pk == toks[j][:, None]).astype(float)
        none = inside.sum(1) == 0; fallbacks += int(none.sum())
        d2 = ((P - C[toks[j]][:, None, :]) ** 2).sum(-1)
        w = inside + 1e-9 * np.exp(-(d2 - d2.min(1, keepdims=True)) / dcell ** 2)
        w /= w.sum(1, keepdims=True)
        cdf = np.cumsum(w, 1); cdf[:, -1] = 1.0
        u = (np.arange(M)[None, :] + rng.random((n_ic, 1))) / M
        rows = np.arange(n_ic)[:, None]
        idx = np.clip(np.searchsorted((cdf + 2 * rows).ravel(), (u + 2 * rows).ravel()).reshape(n_ic, M) - rows * M, 0, M - 1)
        P = P[rows, idx]
        P = P + 0.05 * P.std(1, keepdims=True) * rng.standard_normal(P.shape)
    est = P.mean(1)
    H = traj_of(est); Dd = traj_of(C[toks[-1]])
    dC = np.array([np.linalg.norm(fut[j] - C[km.predict(fut[j])], axis=1) / sA for j in range(N_FR + 1)])
    res = {}
    for tag, start in (("from_t0", 0), ("future_only", 1)):
        h, hc = first_cross(lambda j: np.linalg.norm(H[j] - fut[j], axis=1) / sA, start)
        d, dcn = first_cross(lambda j: np.linalg.norm(Dd[j] - fut[j], axis=1) / sA, start)
        o, oc = first_cross(lambda j: dC[j], start)
        p, pc = first_cross(lambda j: np.linalg.norm(C[toks[-1]] - fut[j], axis=1) / sA, start)  # persistence: hold current prototype
        res[tag] = dict(out_bound=dict(restricted_mean=float(o.mean()), frac_no_cross=float(oc.mean())),
                        history_ref=dict(restricted_mean=float(h.mean()), frac_no_cross=float(hc.mean()), median=float(np.median(h))),
                        decode_integrate=dict(restricted_mean=float(d.mean()), frac_no_cross=float(dcn.mean())),
                        persistence=dict(restricted_mean=float(p.mean())),
                        frac_history_exceeds_out_bound=float((h > o).mean()),
                        gap_history_minus_bound=float(h.mean() - o.mean()))
    row = dict(bits=int(np.log2(N)), p0_outside_tolerance=float((dC[0] > EPS).mean()), **res["from_t0"], future_only=res["future_only"],
               pf_fallback_events=fallbacks, pf_fallback_rate=fallbacks / (n_ic * L))
    out["rows"].append(row)
    print(json.dumps(row), f"({time.time()-t0:.0f}s)", flush=True)
json.dump(out, open("paired_bound_v4.json", "w"), indent=1)
```

### `mse_decomp_v4.py`

```python
"""Single-frame MSE decomposition, v4 (review 3, point 2).

Target: the empirical conditional law of 150,000 stored attractor states (all members of each cell),
propagated once with the true dynamics. Terms per time t:
  I = sum_k p_k tr Cov_k            (information; unbiased within-cell covariance)
  O = sum_k p_k d_C(m_k)^2          (output restriction; plug-in with all members)
  O_bc = O - sum_k p_k tr Cov_k / n_k   (first-order bias correction for a finite cell mean)
  E = sum_k p_k (||g_k - m_k||^2 - d_C(m_k)^2)   for g = projected decode-and-integrate
      (nearest prototype to phi_t(c_k)), a codebook-valued single-frame forecaster
Known-answer test: at t = 0 with converged k-means, m_k = c_k so O = 0 exactly.
Convergence check: O from 48 draws per cell (the v3 estimator) vs all members.
"""
import json
import numpy as np
from sklearn.cluster import KMeans
from systems import lorenz_f, rk4, sample_attractor, DT

LY = json.load(open("lyap.json")); lam = LY["lorenz28"]["lam_max"]
f, _, _ = lorenz_f(28.0); off = np.array([1.0, 1.0, 20.0])
EPS = 0.3; T_MAX = 6.0; steps = int(T_MAX / DT)
train = sample_attractor(f, 3, 150, 1000, 10, seed=10, offset=off)
sA = float(np.sqrt(((train - train.mean(0)) ** 2).sum(1).mean()))
books = {}
for k in (4, 6, 8, 10):
    km = KMeans(n_clusters=2 ** k, n_init=1, max_iter=300, tol=1e-8, random_state=k).fit(train)
    lab = km.labels_; N = 2 ** k
    n = np.bincount(lab, minlength=N).astype(float)
    books[k] = dict(C=km.cluster_centers_, lab=lab, n=n, p=n / n.sum(), Xc=km.cluster_centers_.copy(),
                    I=np.empty(steps + 1), O=np.empty(steps + 1), Obc=np.empty(steps + 1), E=np.empty(steps + 1), O48=None)
    # v3-style 48-draw plug-in at t = 0 for the known-answer comparison
    rng = np.random.default_rng(1)
    m48 = np.stack([train[rng.choice(np.where(lab == j)[0], 48, replace=True)].mean(0) for j in range(N)])
    d48 = ((m48[:, None, :] - km.cluster_centers_[None]) ** 2).sum(-1).min(1)
    books[k]["O48_t0"] = float((books[k]["p"] * d48).sum())
X = train.copy()
for s in range(steps + 1):
    if s > 0:
        X = rk4(f, X)
    for k, b in books.items():
        if s > 0:
            b["Xc"] = rk4(f, b["Xc"])
        N = len(b["n"]); lab = b["lab"]; n = b["n"]; p = b["p"]; C = b["C"]
        m = np.stack([np.bincount(lab, weights=X[:, d], minlength=N) for d in range(3)], 1) / n[:, None]
        sq = np.bincount(lab, weights=(X ** 2).sum(1), minlength=N) / n
        tr = (sq - (m ** 2).sum(1)) * n / np.maximum(n - 1, 1)
        dm = ((m[:, None, :] - C[None]) ** 2).sum(-1)
        dC2 = dm.min(1)
        g = C[((b["Xc"][:, None, :] - C[None]) ** 2).sum(-1).argmin(1)]   # projected decode-and-integrate
        b["I"][s] = (p * tr).sum(); b["O"][s] = (p * dC2).sum()
        b["Obc"][s] = (p * np.maximum(dC2 - tr / n, 0)).sum()
        b["E"][s] = (p * (((g - m) ** 2).sum(1) - dC2)).sum()


def cross(curve):
    over = curve > EPS
    return float(lam * DT * (np.argmax(over) if over.any() else steps))


out = []
for k, b in books.items():
    I, O, Obc, E = b["I"], b["O"], b["Obc"], b["E"]
    ti = int(round(cross(np.sqrt(I) / sA) / (lam * DT)))
    row = dict(bits=k, O_t0_all_members_rel=float(O[0] / I[0]), O_t0_48draws_rel=float(b["O48_t0"] / I[0]),
               T_info=cross(np.sqrt(I) / sA), T_codebook=cross(np.sqrt(I + O) / sA), T_codebook_bc=cross(np.sqrt(I + Obc) / sA),
               T_projected_DI=cross(np.sqrt(I + O + E) / sA),
               O_share_at_Tinfo=float(O[ti] / I[ti]), Obc_share_at_Tinfo=float(Obc[ti] / I[ti]), E_share_at_Tinfo=float(E[ti] / I[ti]),
               min_cell_members=int(b["n"].min()), median_cell_members=float(np.median(b["n"])))
    out.append(row); print(json.dumps(row), flush=True)
json.dump(out, open("mse_decomp_v4.json", "w"), indent=1)
```

### `quant_vpt.py`

```python
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
```

### `staircase.py`

```python
"""Horizon vs initial precision, far below what codebooks reach.

Error directions come from a k-means codebook (the direction a VQ tokenizer actually
puts its error), rescaled to a sweep of magnitudes. An isotropic random direction is the
comparison. Output: VPT vs ln(1/delta) and the local effective growth rate
lambda_eff = 1 / (dVPT / d ln(1/delta)).
"""
import json, sys
import numpy as np
from sklearn.cluster import KMeans
from systems import lorenz_f, l96_f, rk4, sample_attractor, DT

LYAP = json.load(open("lyap.json"))
EPS = 0.3


def run(name, sysdef, offset, t_max, n_ic=600):
    f, jac, d = sysdef
    lam = LYAP[name]["lam_max"]
    train = sample_attractor(f, d, 100, 800, 10, seed=10, offset=offset)
    test = sample_attractor(f, d, 100, 200, 10, seed=20, offset=offset)
    sigma_A = float(np.sqrt(((train - train.mean(0)) ** 2).sum(1).mean()))
    rng = np.random.default_rng(5)
    ic = test[rng.choice(len(test), n_ic, replace=False)]
    km = KMeans(n_clusters=1024, n_init=1, max_iter=60, random_state=0).fit(train)
    e_vq = km.cluster_centers_[km.predict(ic)] - ic
    e_vq /= np.linalg.norm(e_vq, axis=1, keepdims=True)
    e_rn = rng.standard_normal(ic.shape)
    e_rn /= np.linalg.norm(e_rn, axis=1, keepdims=True)
    deltas = np.logspace(-0.5, -9, 18)  # relative to sigma_A
    out = dict(name=name, lam=lam, sigma_A=sigma_A, deltas=deltas.tolist())
    for tag, e in [("vq_dir", e_vq), ("random_dir", e_rn)]:
        X = np.tile(ic, (len(deltas), 1))
        Xh = np.concatenate([ic + dl * sigma_A * e for dl in deltas])
        vpt = np.full(len(X), np.nan)
        steps = int(round(t_max / DT))
        for s in range(1, steps + 1):
            X, Xh = rk4(f, X), rk4(f, Xh)
            err = np.linalg.norm(Xh - X, axis=1) / sigma_A
            hit = np.isnan(vpt) & (err > EPS)
            vpt[hit] = s * DT
        vpt[np.isnan(vpt)] = t_max
        vpt = vpt.reshape(len(deltas), n_ic)
        mean = vpt.mean(1)
        out[tag] = dict(mean=mean.tolist(), median=np.median(vpt, 1).tolist(),
                        censored_frac=float((vpt >= t_max).mean()))
        L = np.log(1 / deltas)
        slope = np.gradient(mean, L)
        print(f"[{name}] {tag}: lam={lam:.3f}")
        for dl, m, sl in zip(deltas, mean, slope):
            print(f"   delta_rel={dl:.1e}  lamVPT={lam*m:6.2f}  lambda_eff/lambda={1/(sl*lam):.2f}")
    json.dump(out, open(f"stair_{name}.json", "w"), indent=1)


if __name__ == "__main__":
    which = sys.argv[1]
    if which.startswith("lorenz"):
        run(which, lorenz_f(float(which[6:])), np.array([1.0, 1.0, 20.0]), t_max=45.0)
    else:
        run(which, l96_f(int(which.split("_")[1])), 8.0, t_max=30.0)
```

### `rvq_vpt.py`

```python
"""Residual VQ oracle: several tokens per state, to reach total rates a single codebook cannot.

Each stage is a 2^b k-means codebook fitted on the previous stage's residuals.
Oracle forecast as in quant_vpt.py: decode, then integrate the true system exactly.
"""
import json, sys, time
import numpy as np
from sklearn.cluster import KMeans
from systems import lorenz_f, l96_f, sample_attractor
from quant_vpt import vpt_curve, summarize, EPS

LYAP = json.load(open("lyap.json"))


def run(name, sysdef, offset, t_max, bits_per_stage, n_stages, n_ic=1000):
    f, jac, d = sysdef
    lam = LYAP[name]["lam_max"]
    t0 = time.time()
    train = sample_attractor(f, d, 120, 1000, 10, seed=10, offset=offset)
    test = sample_attractor(f, d, 200, 300, 10, seed=20, offset=offset)
    sigma_A = float(np.sqrt(((train - train.mean(0)) ** 2).sum(1).mean()))
    rng = np.random.default_rng(3)
    ic = test[rng.choice(len(test), n_ic, replace=False)]
    res_tr, res_te, res_ic = train.copy(), test.copy(), ic.copy()
    rec_te, rec_ic = np.zeros_like(test), np.zeros_like(ic)
    out = dict(name=name, d=d, lam=lam, sigma_A=sigma_A, bits_per_stage=bits_per_stage, stages=[])
    for s in range(1, n_stages + 1):
        km = KMeans(n_clusters=2 ** bits_per_stage, n_init=1, max_iter=80, random_state=s).fit(res_tr)
        C = km.cluster_centers_
        res_tr = res_tr - C[km.predict(res_tr)]
        q_te = C[km.predict(res_te)]; rec_te += q_te; res_te = res_te - q_te
        q_ic = C[km.predict(res_ic)]; rec_ic += q_ic; res_ic = res_ic - q_ic
        delta = float(np.sqrt((res_te ** 2).sum(1).mean()))
        v = vpt_curve(f, ic, rec_ic, sigma_A, t_max)
        r = dict(stages=s, bits=s * bits_per_stage, delta_rel=delta / sigma_A,
                 vpt={str(e): summarize(v[e]) for e in EPS})
        out["stages"].append(r)
        print(f"[{name}] stages={s} bits={s*bits_per_stage:3d} delta_rel={delta/sigma_A:.5f} "
              f"lamVPT(0.3) mean={lam*r['vpt']['0.3']['mean']:.2f} ({time.time()-t0:.0f}s)", flush=True)
    json.dump(out, open(f"rvq_{name}.json", "w"), indent=1)


if __name__ == "__main__":
    which = sys.argv[1]
    if which.startswith("lorenz"):
        run(which, lorenz_f(float(which[6:])), np.array([1.0, 1.0, 20.0]), 45.0, 8, 4)
    else:
        run(which, l96_f(int(which.split("_")[1])), 8.0, 25.0, 8, 7)
```

### `pf_oracle.py`

```python
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
```

### `align_intervention.py`

```python
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
```

### `fsle.py`

```python
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
```

### `context_oracle.py`

```python
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
```

### `review_checks.py`

```python
"""Cheap checks raised by the external review (Lorenz-63, rho = 28).

(a) Output-support bound: any codebook-valued forecast has error >= d_C(x_t), the distance from the
    true state to its nearest code. T_output = first t with d_C(x_t) > eps*sigma_A is an upper bound on
    the VPT of ANY forecast restricted to the codebook (evaluated on the same time grid).
(b) Geometric-mean vs RMS initial error across rates (mean VPT tracks E[ln|e0|], not RMS).
(c) Exact single-frame information bound (RMSE horizon): given only the current token k, the MMSE
    predictor of x_t is E[phi_t(X0) | k]; its RMSE lower-bounds every single-frame predictor.
    Compared with decode-and-integrate phi_t(E[X0 | k]).
(d) Step halving: decode-and-integrate VPT at dt = 0.01 vs 0.005.
"""
import json, time
import numpy as np
from sklearn.cluster import KMeans
from systems import lorenz_f, rk4, sample_attractor, DT

LY = json.load(open("lyap.json"))
EPS = 0.3
f, _, _ = lorenz_f(28.0)
lam = LY["lorenz28"]["lam_max"]
off = np.array([1.0, 1.0, 20.0])
train = sample_attractor(f, 3, 150, 1000, 10, seed=10, offset=off)
test = sample_attractor(f, 3, 200, 300, 10, seed=20, offset=off)
sigma_A = float(np.sqrt(((train - train.mean(0)) ** 2).sum(1).mean()))
rng = np.random.default_rng(3)
ic = test[rng.choice(len(test), 1000, replace=False)]
out = dict(sigma_A=sigma_A, lam=lam, rows=[])
T_MAX = 30.0
steps = int(T_MAX / DT)

# true trajectories of the ICs, stored every step (1000 x 3000 x 3 = 72 MB) -- fine
traj = np.empty((steps + 1, len(ic), 3)); x = ic.copy(); traj[0] = x
for s in range(1, steps + 1):
    x = rk4(f, x); traj[s] = x

for k in [4, 6, 8, 10, 12]:
    N = 2 ** k
    t0 = time.time()
    km = KMeans(n_clusters=N, n_init=1, max_iter=80, random_state=k).fit(train)
    C = km.cluster_centers_
    row = dict(bits=k)
    # (a) output-support bound along the true trajectory (every 5 steps = model frame grid 0.05)
    grid = np.arange(0, steps + 1, 5)
    dC = np.empty((len(grid), len(ic)))
    for gi, s in enumerate(grid):
        dC[gi] = np.linalg.norm(traj[s] - C[km.predict(traj[s])], axis=1) / sigma_A
    over = dC > EPS
    first = np.where(over.any(0), over.argmax(0), len(grid) - 1)
    T_out = grid[first] * DT
    row["T_output_mean_lam"] = float(lam * T_out.mean())
    row["T_output_censored_frac"] = float((~over.any(0)).mean())
    row["max_cell_dist_rel"] = float(dC.max())
    # (b) initial error statistics
    e0 = np.linalg.norm(C[km.predict(ic)] - ic, axis=1) / sigma_A
    row["e0_rms"] = float(np.sqrt((e0 ** 2).mean())); row["e0_geo"] = float(np.exp(np.log(e0).mean()))
    row["e0_q90"] = float(np.quantile(e0, 0.9)); row["geo_over_rms"] = row["e0_geo"] / row["e0_rms"]
    # decode-and-integrate VPT (dt = 0.01) and step-halving (dt = 0.005) -- (d)
    xh = C[km.predict(ic)].copy(); vpt = np.full(len(ic), np.nan)
    rmse_ref = np.empty(steps + 1)
    for s in range(0, steps + 1):
        if s > 0:
            xh = rk4(f, xh)
        err = np.linalg.norm(xh - traj[s], axis=1) / sigma_A
        rmse_ref[s] = np.sqrt((err ** 2).mean())
        hit = np.isnan(vpt) & (err > EPS); vpt[hit] = s * DT
    vpt[np.isnan(vpt)] = T_MAX
    row["vpt_dt01_lam"] = float(lam * vpt.mean())
    x1, x2 = ic.copy(), C[km.predict(ic)].copy(); v2 = np.full(len(ic), np.nan)
    for s in range(1, 2 * steps + 1):
        x1, x2 = rk4(f, x1, 0.005), rk4(f, x2, 0.005)
        err = np.linalg.norm(x2 - x1, axis=1) / sigma_A
        hit = np.isnan(v2) & (err > EPS); v2[hit] = s * 0.005
    v2[np.isnan(v2)] = T_MAX
    row["vpt_dt005_lam"] = float(lam * v2.mean())
    # (c) exact single-frame MMSE bound (RMSE horizon), for N <= 1024
    first_cross = lambda curve: float(lam * DT * (np.argmax(curve > EPS) if (curve > EPS).any() else steps))
    row["T_rmse_ref_lam"] = first_cross(rmse_ref)
    if N <= 1024:
        lab = km.predict(train)
        p = np.bincount(lab, minlength=N) / len(lab)
        M = 48
        idx = np.concatenate([rng.choice(np.where(lab == j)[0], M, replace=True) for j in range(N)])
        X = train[idx]; cell = np.repeat(np.arange(N), M)
        Xc = C[cell].copy()
        mmse = np.empty(steps + 1); ref2 = np.empty(steps + 1)
        for s in range(0, steps + 1):
            if s > 0:
                X = rk4(f, X); Xc = rk4(f, Xc)
            m = X.reshape(N, M, 3).mean(1)  # E[phi_t(X0) | k]
            var_k = ((X.reshape(N, M, 3) - m[:, None, :]) ** 2).sum(-1).mean(1) * M / (M - 1)
            mmse[s] = np.sqrt((p * var_k).sum()) / sigma_A
            ref_k = ((X.reshape(N, M, 3) - Xc.reshape(N, M, 3)) ** 2).sum(-1).mean(1)
            ref2[s] = np.sqrt((p * ref_k).sum()) / sigma_A
        row["T_rmse_mmse_bound_lam"] = first_cross(mmse)
        row["T_rmse_ref_cellsamples_lam"] = first_cross(ref2)
        row["mmse_curve_rel_t0"] = float(mmse[0])
    out["rows"].append(row)
    print(json.dumps(row), f"({time.time()-t0:.0f}s)", flush=True)
json.dump(out, open("review_checks.json", "w"), indent=1)
```
