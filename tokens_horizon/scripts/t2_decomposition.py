"""Task 2.3: single-frame MSE decomposition on lorenz28 (freeze 2.5, Amendment 1).

Target: the empirical conditional law of all 150,000 calibration states, grouped by their t = 0 cell under the frozen
codebook and propagated once with the true dynamics. At each integrator step t:
  I     = sum_k p_k tr Cov_k(t)                    information term, within-cell covariance with n/(n-1)
  O     = sum_k p_k d_C(m_k(t))^2                  output term, plug-in on the cell mean
  O_bc  = sum_k p_k max(d_C(m_k)^2 - tr Cov_k / n_k, 0)     first-order bias correction
  E     = sum_k p_k (||g_k(t) - m_k(t)||^2 - d_C(m_k(t))^2)  excess of projected decode-and-integrate,
          g_k(t) = nearest prototype to phi_t(c_k)
Known-zero test: O(0) < known_zero_ratio * I(0) (amended to 1e-6); the original 1e-10 outcome is also recorded.
Ensemble-RMSE horizons (Lyapunov times): first step where sqrt(curve)/sigma_A > eps, for I, I+O, I+O_bc, I+O+E.
Shares of O, O_bc and E (relative to I) at the information-bound crossing. Intervals: bootstrap over the 150
calibration trajectories (per-trajectory cell sums are kept, so each resample recombines them exactly).
Labels: I-horizon = bound (information bound on single-frame forecasts); others and shares = estimate.
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np  # noqa: E402

from th import config, data  # noqa: E402
from th.systems import DT, get_system, rk4, flow  # noqa: E402
from th.tokenize import kmeans_codebook, kmeans_labels  # noqa: E402

FZ = config.freeze()
DC = FZ["decomposition"]
SYS = DC["system"]
EPS = [FZ["scoring"]["eps_primary"]] + FZ["scoring"]["eps_secondary"]
ORIGINAL_RATIO = 1.0e-10
OUT_R = config.RESULTS / "decomposition"
OUT_RUN = config.RUNS / "decomposition"


def terms_from_sums(cnt, s1, s2, C, G):
    """cnt (K,), s1 (T,K,3), s2 (T,K) -> I, O, Obc, E curves (T,)."""
    ok = cnt >= 2
    n = cnt[ok]
    p = n / n.sum()
    m = s1[:, ok] / n[None, :, None]
    tr = (s2[:, ok] / n - (m ** 2).sum(-1)) * n / (n - 1)
    # d_C(m)^2: nearest prototype distance of each cell mean
    T, K = m.shape[:2]
    from scipy.spatial import cKDTree
    tree = cKDTree(C)
    dC2 = tree.query(m.reshape(-1, 3), workers=8)[0].reshape(T, K) ** 2
    I = (tr * p).sum(1)
    O = (dC2 * p).sum(1)
    Obc = (np.maximum(dC2 - tr / n, 0) * p).sum(1)
    E = ((((G[:, ok] - m) ** 2).sum(-1) - dC2) * p).sum(1)
    return I, O, Obc, E


def cross(curve, sA, lam, eps):
    over = np.sqrt(np.maximum(curve, 0)) / sA > eps
    return float(lam * DT * (np.argmax(over) if over.any() else len(curve) - 1)), int(np.argmax(over)) if over.any() else -1


def summarize(I, O, Obc, E, sA, lam):
    out = {}
    for eps in EPS:
        tI, iI = cross(I, sA, lam, eps)
        r = dict(T_info=tI, T_codebook=cross(I + O, sA, lam, eps)[0], T_codebook_bc=cross(I + Obc, sA, lam, eps)[0],
                 T_projected_DI=cross(I + O + E, sA, lam, eps)[0])
        j = iI if iI >= 0 else len(I) - 1
        r.update(O_share_at_Tinfo=float(O[j] / I[j]), Obc_share_at_Tinfo=float(Obc[j] / I[j]),
                 E_share_at_Tinfo=float(E[j] / I[j]), info_crossed=iI >= 0)
        out[f"eps{eps}"] = r
    return out


def run_rate(bits, reps, cb=None, lab=None, out_run=None, name=None):
    """Frozen codebook unless `cb`/`lab` are supplied (post-freeze robustness check only)."""
    sysm = get_system(SYS)
    lam, sA = config.lam(SYS), data.sigma_A(SYS)
    X, traj = data.calibration(SYS)
    if cb is None:
        cb = kmeans_codebook(SYS, bits)
        lab = kmeans_labels(SYS, bits)
    C, K = cb.C, cb.K
    ntr = int(traj.max()) + 1
    steps = int(round(DC["horizon_time"] / DT))
    gidx = traj * K + lab
    cnt_tk = np.bincount(gidx, minlength=ntr * K).reshape(ntr, K).astype(float)
    S1 = np.empty((steps + 1, ntr, K, 3))
    S2 = np.empty((steps + 1, ntr, K))
    G = np.empty((steps + 1, K, 3))
    x, xc = X.copy(), C.copy()
    for s in range(steps + 1):
        if s > 0:
            x = rk4(sysm.f, x)
            xc = rk4(sysm.f, xc)
        for d in range(3):
            S1[s, :, :, d] = np.bincount(gidx, weights=x[:, d], minlength=ntr * K).reshape(ntr, K)
        S2[s] = np.bincount(gidx, weights=(x ** 2).sum(1), minlength=ntr * K).reshape(ntr, K)
        G[s] = C[cb.encode(xc)]
    cnt = cnt_tk.sum(0)
    I, O, Obc, E = terms_from_sums(cnt, S1.sum(1), S2.sum(1), C, G)
    ratio0 = float(O[0] / I[0])
    kz = dict(O0_over_I0=ratio0, threshold_amended=DC["known_zero_ratio"], passes_amended=ratio0 < DC["known_zero_ratio"],
              threshold_original=ORIGINAL_RATIO, passes_original=ratio0 < ORIGINAL_RATIO,
              Obc0_over_I0=float(Obc[0] / I[0]), kmeans_n_iter=cb.meta.get("n_iter"))
    point = summarize(I, O, Obc, E, sA, lam)
    if not kz["passes_amended"]:        # stop condition: no decomposition numbers at this rate
        reps = 0
    # bootstrap over calibration trajectories
    rng = np.random.default_rng(FZ["seeds"]["bootstrap_seed"] + bits)
    boots = []
    A1 = S1.reshape(steps + 1, ntr, -1)
    A2 = S2
    for r in range(reps):
        w = np.bincount(rng.integers(0, ntr, ntr), minlength=ntr).astype(float)
        c = w @ cnt_tk
        s1 = np.einsum("j,tjk->tk", w, A1).reshape(steps + 1, K, 3)
        s2 = np.einsum("j,tjk->tk", w, A2)
        boots.append(summarize(*terms_from_sums(c, s1, s2, C, G), sA, lam))
    ci = {}
    for e, d in point.items():
        ci[e] = {}
        for k, v in d.items():
            if isinstance(v, bool):
                continue
            vals = np.array([b[e][k] for b in boots]) if boots else np.array([np.nan])
            ci[e][k] = [float(np.quantile(vals, 0.025)), float(np.quantile(vals, 0.975))]
    cells = dict(min=int(cnt.min()), median=float(np.median(cnt)), max=int(cnt.max()))
    out_run = out_run or OUT_RUN
    out_run.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(out_run / (name or f"{SYS}_b{bits}.npz"), I=I, O=O, Obc=Obc, E=E, t=np.arange(steps + 1) * DT,
                        lam=lam, sigma_A=sA)
    return dict(bits=bits, known_zero=kz, point=point, ci95=ci, cell_members=cells, bootstrap_reps=reps)


def main():
    reps = FZ["seeds"]["bootstrap_reps"]
    if len(sys.argv) > 1 and sys.argv[1] == "--reps":
        reps = int(sys.argv[2])
    OUT_R.mkdir(parents=True, exist_ok=True)
    res = []
    for bits in DC["rates"]:
        t0 = time.time()
        r = run_rate(bits, reps)
        res.append(r)
        kz, p = r["known_zero"], r["point"]["eps0.3"]
        print(f"b{bits} O0/I0={kz['O0_over_I0']:.3e} amended_ok={kz['passes_amended']} original_ok={kz['passes_original']} "
              f"T_info={p['T_info']:.3f} T_cb={p['T_codebook']:.3f} T_proj={p['T_projected_DI']:.3f} "
              f"Oshare={p['O_share_at_Tinfo']:.4f} Ebc={p['Obc_share_at_Tinfo']:.4f} Eshare={p['E_share_at_Tinfo']:.4f} "
              f"({time.time()-t0:.0f}s)", flush=True)
    stop = [r["bits"] for r in res if not r["known_zero"]["passes_amended"]]
    sha = config.git_sha()
    (OUT_R / "decomposition.json").write_text(json.dumps(dict(git_sha=sha, system=SYS, rates=res,
                                                              stop_known_zero_amended=stop), indent=1, default=float))
    with open(OUT_R / "decomposition.csv", "w") as fh:
        fh.write(f"# git_sha={sha}; T_info = bound (single-frame information bound, ensemble RMSE); other horizons and "
                 f"shares = estimate; known-zero amended threshold {DC['known_zero_ratio']}, original {ORIGINAL_RATIO}\n")
        cols = ["T_info", "T_codebook", "T_codebook_bc", "T_projected_DI", "O_share_at_Tinfo", "Obc_share_at_Tinfo",
                "E_share_at_Tinfo"]
        fh.write("bits,eps,O0_over_I0,passes_amended_1e-6,passes_original_1e-10," +
                 ",".join(f"{c},{c}_lo,{c}_hi" for c in cols) + ",min_cell,median_cell,label\n")
        for r in res:
            for e in (f"eps{x}" for x in EPS):
                p, c = r["point"][e], r["ci95"][e]
                vals = ",".join(f"{p[k]},{c[k][0]},{c[k][1]}" for k in cols)
                kz = r["known_zero"]
                fh.write(f"{r['bits']},{e[3:]},{kz['O0_over_I0']},{kz['passes_amended']},{kz['passes_original']},"
                         f"{vals},{r['cell_members']['min']},{r['cell_members']['median']},estimate\n")
    if stop:
        print("STOP: known-zero test fails under the amended threshold at bits", stop)


if __name__ == "__main__":
    main()
