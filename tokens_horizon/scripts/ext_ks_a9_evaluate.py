"""Post-freeze extension A9 evaluation (Amendment 2 B1) against the committed prediction (468cabc).

Per odd rate R in {7, 9, 11}: observed restricted-mean decode-and-integrate horizon (Delta 0.92, eps 0.3, future
frames, 1,000 confirmation states, W = 27) with its 95% bootstrap CI; observed - H_hat(R) with its 90% bootstrap CI
over states (H_hat fixed, from results/ext/ks/a9_prediction.json, not refitted); criterion: the 90% CI lies within
+-0.10 Lyapunov times. Bootstrap: th/score.bootstrap_mean (seed 777, 2,000 reps, states resampled).
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from th import config   # noqa: E402
from th import ks as K   # noqa: E402
from th.score import bootstrap_mean   # noqa: E402

E3 = config.RUNS / "ext" / "ks" / "e3"
pred = json.loads((config.RESULTS / "ext" / "ks" / "a9_prediction.json").read_text())
a9 = K.ext_freeze()["ks"]["a9"]
delta = float(a9["delta"])
rows = []
for R in a9["odd_rates"]:
    z = np.load(E3 / f"ks22_whole_b{R}.npz")
    H = z[f"di_d{delta:g}_eps0.3_future_H"]
    c = z[f"di_d{delta:g}_eps0.3_future_crossed"]
    hhat = float(pred["predictions"][str(R)])
    m, lo, hi = bootstrap_mean(H)
    dm, dlo, dhi = bootstrap_mean(H - hhat, ci=0.90)
    met = (dlo >= -0.10) and (dhi <= 0.10)
    rows.append(dict(R=R, observed=m, observed_ci95_lo=lo, observed_ci95_hi=hi, censored_frac=float(1 - c.mean()),
                     H_hat=hhat, diff=dm, diff_ci90_lo=dlo, diff_ci90_hi=dhi,
                     criterion="criterion met" if met else "criterion not met", n=int(len(H))))
out = dict(label="post-freeze extension; A9 result (Amendment 2 B1), reference (decode-and-integrate)",
           git_sha=config.git_sha(), prediction_commit="468cabc", predictor=pred["predictor"], delta=delta, eps=0.3,
           score=pred["score"], rule=a9["pass"], rows=rows, scope=a9["scope"],
           scope_sentence=("This tests prospective interpolation across held-out rates within the specified system, "
                           "tokenizer family and rate range; it does not test extrapolation or cross-system transfer."),
           decode_and_integrate_note=pred["decode_and_integrate_note"])
fd = config.RESULTS / "ext" / "ks"
(fd / "a9_result.json").write_text(json.dumps(out, indent=1))
with open(fd / "a9_result.csv", "w", newline="") as fh:
    fh.write(f"# git_sha={config.git_sha()}; POST-FREEZE EXTENSION\n")
    w = csv.DictWriter(fh, list(rows[0]))
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(r)
