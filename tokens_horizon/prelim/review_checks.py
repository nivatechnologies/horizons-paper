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
