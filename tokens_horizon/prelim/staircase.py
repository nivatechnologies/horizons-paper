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
