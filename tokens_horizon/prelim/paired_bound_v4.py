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
