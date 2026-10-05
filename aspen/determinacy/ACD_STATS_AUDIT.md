# ACD statistical audit — v2.3

**PASS.** Synthetic only, sulaco CPU. 20,000 200-case panels per null configuration; 5,000 panels per power cell. Seed 2026100522. Wall time 17.54s.

Predictable plug-in λ is independent of m, capped .9; running residual variance follows §10 exactly. Capital prefix maxima are evaluated in log space. Monotone integer bisection returns largest rejected lower grid point and smallest rejected upper grid point, outward-rounded. Two-sided bounds use alpha/2. No truth or experiment module is imported.

Monotonicity: 1000 sequences, 1e-4 grid, 0 violations. CP exact error 4.77e-15; McNemar exact error 6.66e-16. Reference: scipy.stats exact proportion_ci and binomtest.

Prior witnesses recomputed (candidate may be excluded only if its own capital now rejects it):

| Sequence | Candidate | 99% interval | Candidate rejected | Peak capital |
|---|---:|---|---|---:|
| 200×1.0 | 0.9629 | [0.97, 1.0] | True | 712.608375 |
| 200×0.0 | 0.0371 | [0.0, 0.03] | True | 712.608375 |

Null criterion: nominal + 2 sqrt(nominal·(1−nominal)/N), fixed by §10. All distributions are synthetic hypotheses under test. Half-empty is P(0)=.5 plus uniform nonempty 1–8. Eight-only errors fail an entire eight-answer case; error probability .3 or .8 sets the nonempty case accuracy to .90.

| Sizes | Mechanism | False PASS | Limit |
|---|---|---:|---:|
| executor | independent | 0.00010 | 0.05308 |
| executor | whole-case | 0.00390 | 0.05308 |
| executor | eight-only | 0.00215 | 0.05308 |
| uniform | independent | 0.02025 | 0.05308 |
| uniform | whole-case | 0.03545 | 0.05308 |
| uniform | eight-only | 0.00575 | 0.05308 |
| half-empty | independent | 0.01070 | 0.05308 |
| half-empty | whole-case | 0.03865 | 0.05308 |
| half-empty | eight-only | 0.01850 | 0.05308 |

| R2 shape | Noncoverage | Limit |
|---|---:|---:|
| symmetric | 0.00585 | 0.01141 |
| skewed | 0.00230 | 0.01141 |
| sparse | 0.00000 | 0.01141 |

The .888 answer-accuracy construction has case-accuracy .9533333333 under the new estimand; it is an alternative, not a .90 case-mean null.

{
  "answer_accuracy": 0.888,
  "case_accuracy": 0.9533333333333335,
  "interpretation": "case accuracy=.953333, so this is an alternative, not a v2.3 null",
  "old_no_error_PASS": {
    "rate": 0.06375,
    "mc_se": 0.001727511758281257,
    "panels": 20000,
    "events": 1275
  },
  "new_PASS": {
    "rate": 0.02505,
    "mc_se": 0.0011050451913835922,
    "panels": 20000,
    "events": 501
  },
  "thirty_perfect_fixture": {
    "status": "INSUFFICIENT",
    "cases": 30,
    "answers": 100,
    "case_accuracy": 1.0,
    "case_lower": 0.883,
    "case_upper": 1.0,
    "answer_accuracy": 1.0,
    "fallback": false
  }
}

Power: uniform nonempty case sizes 1–8, then empty cases. Cell values are probability (MC SE); low power is reported, not a halt.

| Accuracy | Nonempty | Independent answers | Whole-case errors |
|---|---:|---:|---:|
| 0.95 | 50 | 0.1212 (0.0046) | 0.1592 (0.0052) |
| 0.95 | 80 | 0.5510 (0.0070) | 0.3242 (0.0066) |
| 0.95 | 120 | 0.7726 (0.0059) | 0.3730 (0.0068) |
| 0.95 | 160 | 0.8700 (0.0048) | 0.4310 (0.0070) |
| 0.97 | 50 | 0.5280 (0.0071) | 0.3380 (0.0067) |
| 0.97 | 80 | 0.9140 (0.0040) | 0.6602 (0.0067) |
| 0.97 | 120 | 0.9818 (0.0019) | 0.7334 (0.0063) |
| 0.97 | 160 | 0.9936 (0.0011) | 0.8190 (0.0054) |
| 0.985 | 50 | 0.8842 (0.0045) | 0.5948 (0.0069) |
| 0.985 | 80 | 0.9922 (0.0012) | 0.9056 (0.0041) |
| 0.985 | 120 | 0.9990 (0.0004) | 0.9514 (0.0030) |
| 0.985 | 160 | 0.9998 (0.0002) | 0.9822 (0.0019) |

R2 high variance: −1/+1 with prescribed mean; low variance: Δ±.25. Statistical route power assumes calibration prerequisites already pass.

| Δ | Shape | Publish power | Strong power |
|---|---|---:|---:|
| 0.15 | high-variance | 0.0966 | 0.0560 |
| 0.15 | low-variance | 0.5226 | 0.0000 |
| 0.25 | high-variance | 0.4494 | 0.3968 |
| 0.25 | low-variance | 1.0000 | 0.5350 |

Every prescribed check passes; **R-stat did not fire**. Full receipt and code hashes: ACD_STATS_AUDIT_v2.3.json; host output runs/audit/acd_stats_audit.json. No confirmation, freeze or CNN inference.
