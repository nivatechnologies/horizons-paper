"""Task 2.5: dimension. Distortion curves (k-means, from t2_system_table), scalar quantization distortion vs nominal
rate, residual-VQ oracle horizons (1, 2, 3 stages = 8, 16, 24 bits) and decode-and-integrate horizon vs k-means rate.

Scalar quantization: the library ScalarQuantizer encodes a cell as one int64 (ravel_multi_index), which overflows
when levels^d > 2^63 (l96_20 at levels >= 9). Distortion is therefore computed by an independent implementation of
the same rule (uniform bins over the calibration range, cell = tuple of bin indices, decode to the calibration cell
mean, unseen cells to the geometric centre); it is cross-checked against the library wherever the library runs.
In-sample (calibration) and held-out (confirmation panel t = 0 states) distortion are both reported.

Residual VQ: th.tokenize.ResidualVQ stage codebooks (fitted here, cached as runs/cache/rvq_<sys>_stage<s>.npz);
quantization reproduced stage by stage with a bounded KD-tree worker count.
Labels: distortions = estimate; RVQ and k-means decode-and-integrate horizons = reference.
"""
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "4")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("TH_KDTREE_WORKERS", "4")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np  # noqa: E402

from th import config, data, score  # noqa: E402
from th import exchange as ex  # noqa: E402
from th.tokenize import ResidualVQ, ScalarQuantizer  # noqa: E402

SYSTEMS = ["lorenz28", "lorenz45", "l96_5", "l96_6", "l96_10", "l96_20"]
RUNS = config.RUNS / "exchange_law"
OUT = config.RESULTS / "dimension"
DELTA = 0.02
FZ = config.freeze()


class SQ:
    """Independent implementation of the frozen scalar-quantization rule (tuple cell keys, no int64 packing)."""

    def __init__(self, X, levels):
        self.n, self.d = levels, X.shape[1]
        self.lo, self.hi = X.min(0), X.max(0)
        self.edges = [np.linspace(self.lo[j], self.hi[j], levels + 1)[1:-1] for j in range(self.d)]
        idx = self.idx(X)
        self.keys, inv = np.unique(idx, axis=0, return_inverse=True)
        inv = inv.ravel()
        self.means = np.zeros((len(self.keys), self.d))
        np.add.at(self.means, inv, X)
        self.means /= np.bincount(inv)[:, None]
        self.inv_train = inv

    def idx(self, X):
        return np.stack([np.searchsorted(self.edges[j], X[:, j]) for j in range(self.d)], 1).astype(np.int16)

    def quantize(self, X):
        idx = self.idx(X)
        lookup = {tuple(k): i for i, k in enumerate(self.keys.tolist())}
        w = (self.hi - self.lo) / self.n
        out = np.empty_like(X)
        unseen = 0
        for i, k in enumerate(idx.tolist()):
            j = lookup.get(tuple(k))
            if j is None:
                out[i] = self.lo + (np.array(k) + 0.5) * w
                unseen += 1
            else:
                out[i] = self.means[j]
        return out, unseen


def rms_rel(A, B, sA):
    return float(np.sqrt(((A - B) ** 2).sum(-1).mean()) / sA)


def scalar_system(system):
    X, _ = data.calibration(system)
    sA = data.sigma_A(system)
    x0 = data.panel(system, "confirmation")
    x0 = x0["traj"][:, x0["pre"]]
    rows = []
    for L in FZ["tokenizers"]["scalar_levels"]:
        q = SQ(X, L)
        d_in = rms_rel(q.means[q.inv_train], X, sA)
        qh, unseen = q.quantize(x0)
        d_out = rms_rel(qh, x0, sA)
        lib_diff = None
        lib_status = "ok"
        try:
            lq = ScalarQuantizer(system, L)
            lib_diff = float(np.abs(lq.quantize(x0) - qh).max())
        except ValueError as e:
            lib_status = f"library not runnable: {str(e)[:60]}"
        rows.append(dict(system=system, levels=L, rate_nominal_bits=float(X.shape[1] * np.log2(L)),
                         cells_used=int(len(q.keys)), delta_calib_over_sigma_A=d_in,
                         delta_heldout_over_sigma_A=d_out, heldout_unseen_frac=unseen / len(x0),
                         library_max_abs_diff=lib_diff, library_status=lib_status, label="estimate"))
    return rows


def rvq_system(system):
    p = RUNS / f"rvq_{system}.npz"
    if p.exists():
        z = np.load(p)
        return json.loads(str(z["summary"]))
    t0 = time.time()
    sA = data.sigma_A(system)
    lam = config.lam(system)
    X, _ = data.calibration(system)
    rvq = ResidualVQ(system, max(FZ["tokenizers"]["rvq_stages"]))
    out, arrays = [], {}
    for S in FZ["tokenizers"]["rvq_stages"]:
        books = rvq.books[:S]

        def quant(Z, books=books):
            R = Z.reshape(-1, Z.shape[-1]).copy()
            acc = np.zeros_like(R)
            for cb in books:
                q, _ = ex.nearest(cb, R)
                acc += q
                R -= q
            return acc.reshape(Z.shape)

        d_cal = rms_rel(quant(X), X, sA)
        H, c, e0, psha = ex.decode_integrate(system, quant, DELTA)
        m, lo, hi = score.bootstrap_mean(H)
        arrays[f"H_stages{S}"] = H
        arrays[f"crossed_stages{S}"] = c
        out.append(dict(system=system, stages=S, bits=S * FZ["tokenizers"]["rvq_bits_per_stage"],
                        delta_calib_over_sigma_A=d_cal, delta_panel_over_sigma_A=float(np.sqrt((e0 ** 2).mean())),
                        H_mean=m, H_ci95_lo=lo, H_ci95_hi=hi, frac_no_cross=float(1 - c.mean()),
                        lam=lam, label="reference"))
        print(system, S, f"{time.time() - t0:.0f}s dcal={d_cal:.5f} H={m:.3f}", flush=True)
    np.savez(p, summary=json.dumps(out), sha=config.git_sha(), **arrays)
    return out


def di_rows(system):
    rows = []
    for R in range(4, 13):
        p = RUNS / f"di_{system}_R{R}.npz"
        if not p.exists():
            continue
        z = np.load(p)
        m, lo, hi = score.bootstrap_mean(z["H"])
        rows.append(dict(system=system, rate_bits=R, H_mean=m, H_ci95_lo=lo, H_ci95_hi=hi,
                         frac_no_cross=float(1 - z["crossed"].mean()),
                         delta_panel_over_sigma_A=float(np.sqrt((z["err0_rel"] ** 2).mean())), label="reference"))
    return rows


if __name__ == "__main__":
    config.ensure_dirs()
    OUT.mkdir(parents=True, exist_ok=True)
    sha = config.git_sha()
    with ProcessPoolExecutor(6) as pool:
        rvq = [r for rr in pool.map(rvq_system, SYSTEMS) for r in rr]
        sq = [r for rr in pool.map(scalar_system, SYSTEMS) for r in rr]
    di = [r for s in SYSTEMS for r in di_rows(s)]
    for r in rvq:
        print(f"RVQ {r['system']:9s} {r['bits']:2d} bits dcal={r['delta_calib_over_sigma_A']:.5f} "
              f"H={r['H_mean']:.3f} [{r['H_ci95_lo']:.3f},{r['H_ci95_hi']:.3f}] nc={r['frac_no_cross']:.3f}")
    for r in sq:
        print(f"SQ  {r['system']:9s} L={r['levels']:2d} R={r['rate_nominal_bits']:6.2f} din={r['delta_calib_over_sigma_A']:.4f} "
              f"dout={r['delta_heldout_over_sigma_A']:.4f} unseen={r['heldout_unseen_frac']:.3f} lib={r['library_status']} "
              f"{r['library_max_abs_diff']}")
    ex.write_csv(OUT / "rvq_oracle.csv", rvq, "RVQ decode-and-integrate horizons, confirmation panel, Delta 0.02, "
                 "future frames, eps 0.3; H = reference, delta = estimate")
    ex.write_csv(OUT / "scalar_quantization.csv", sq, "distortion estimates")
    ex.write_csv(OUT / "di_vs_kmeans_rate.csv", di, "k-means decode-and-integrate horizons; reference")
    ex.write_json(OUT / "dimension.json", dict(git_sha=sha, rvq_oracle=rvq, scalar_quantization=sq,
                                               di_vs_kmeans_rate=di,
                                               note="RVQ/DI horizons: reference; distortions: estimate"))
