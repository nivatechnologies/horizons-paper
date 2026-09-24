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
