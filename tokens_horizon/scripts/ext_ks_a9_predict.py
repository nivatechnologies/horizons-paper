"""Post-freeze extension A9 (Amendment 2 B1): prediction for the KS L = 22 whole-state odd rates.

Per even rate R in {6, 8, 10, 12}: restricted-mean decode-and-integrate horizon (Lyapunov times), Delta = 0.92,
eps = 0.3, future frames, confirmation panel (1,000 states), W = 27, with the censored fraction (states not crossing
within W). An even rate is excluded only if more than 5% of its states are censored. Predictor: OLS
H_hat(R) = a + s R, intercept free. Writes results/ext/ks/a9_prediction.json with the exposure record.
Reads only the even-rate decode-and-integrate arrays; no odd-rate decode-and-integrate exists or is read.
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from th import config   # noqa: E402
from th import ks as K   # noqa: E402
from th.score import bootstrap_mean   # noqa: E402

E3 = config.RUNS / "ext" / "ks" / "e3"
a9 = K.ext_freeze()["ks"]["a9"]
delta = float(a9["delta"])
rows, used = [], []
for R in a9["even_rates"]:
    z = np.load(E3 / f"ks22_whole_b{R}.npz")
    H = z[f"di_d{delta:g}_eps0.3_future_H"]
    c = z[f"di_d{delta:g}_eps0.3_future_crossed"]
    m, lo, hi = bootstrap_mean(H)
    cens = float(1 - c.mean())
    excl = cens > 0.05
    rows.append(dict(R=R, restricted_mean=m, ci95_lo=lo, ci95_hi=hi, censored_frac=cens, excluded=bool(excl), n=int(len(H))))
    if not excl:
        used.append((R, m))
Rs = np.array([u[0] for u in used], float)
Hs = np.array([u[1] for u in used], float)
A = np.stack([np.ones_like(Rs), Rs], 1)
coef, *_ = np.linalg.lstsq(A, Hs, rcond=None)
a, s = float(coef[0]), float(coef[1])
pred = {int(R): a + s * R for R in a9["odd_rates"]}
odd_files = [str(p.name) for p in E3.glob("ks22_whole_b*.npz")
             if int(p.stem.split("_b")[1]) in a9["odd_rates"] and any(k.startswith("di_") for k in np.load(p).files)]
out = dict(
    label="post-freeze extension; A9 prediction (Amendment 2 B1), estimate",
    git_sha=config.git_sha(),
    system="ks22", tokenizer="whole-state k-means", delta=delta, eps=0.3, score="restricted-mean decode-and-integrate horizon, future frames, W = 27 Lyapunov times, confirmation panel 1,000 states (Lyapunov times)",
    even_rates=rows, fit_rates=[int(r) for r in Rs], predictor=dict(form="H_hat(R) = a + s R (OLS, intercept free)", a=a, s=s),
    predictions={str(k): v for k, v in pred.items()},
    pass_rule=a9["pass"], scope=a9["scope"],
    exposure_record=("no odd-rate DI computed or inspected: whole-state ks22 rates 7, 9, 11 were run through E3 with "
                     "decode-and-integrate skipped by code (scripts/ext_ks_e3.py, ODD set); their per-state files hold "
                     "bound and persistence arrays only; odd-rate files containing decode-and-integrate arrays at "
                     "prediction time: " + (", ".join(odd_files) if odd_files else "none")),
    decode_and_integrate_note="the integrator projects the decoded initial condition onto modes 1..M (reference trajectory only)",
)
fn = config.RESULTS / "ext" / "ks" / "a9_prediction.json"
fn.write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
