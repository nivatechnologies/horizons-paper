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
