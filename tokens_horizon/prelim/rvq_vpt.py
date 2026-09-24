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
