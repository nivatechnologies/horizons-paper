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
