# ACD statistical audit — v2.3

**PASS.**
Synthetic only; host sulaco; seed 2026100522; 20000 panels/configuration; 5000 panels/power cell; 24.41 CPU wall seconds.

Predictable m-independent bets capped at .9, prefix log-capitals, monotone integer bisection and outward rounding. Per-side alpha/2 is used for two-sided bounds. The audit imports no experiment or truth module.

Monotonicity: 1000 sequences on a 1e-4 grid, 0 violations. Exact CP error 4.77e-15; McNemar error 6.66e-16.

| Sequence | Candidate | 99% interval | Rejected | Peak capital |
|---|---|---|---|---|
| 200 × 1.0 | 0.9629 | [0.97, 1.0] | True | 712.608375 |
| 200 × 0.0 | 0.0371 | [0.0, 0.03] | True | 712.608375 |

Both previous unrejected real-mean counterexamples are now rejected by their own capital; continuous coverage no longer relies on scanning a non-monotone sublevel set.

Null criterion: nominal + 2·sqrt(nominal·(1−nominal)/N). Half empty is P(0)=.5, otherwise uniform 1–8; eight-only errors fail an entire eight-answer case.

| Sizes | Error mechanism | False PASS | Limit |
|---|---|---|---|
| executor | independent | 0.00010 | 0.05308 |
| executor | whole-case | 0.00390 | 0.05308 |
| executor | eight-only | 0.00215 | 0.05308 |
| uniform | independent | 0.02025 | 0.05308 |
| uniform | whole-case | 0.03545 | 0.05308 |
| uniform | eight-only | 0.00575 | 0.05308 |
| half-empty | independent | 0.01070 | 0.05308 |
| half-empty | whole-case | 0.03865 | 0.05308 |
| half-empty | eight-only | 0.01850 | 0.05308 |

| R2 null shape | Noncoverage | Limit |
|---|---|---|
| symmetric | 0.00585 | 0.01141 |
| skewed | 0.00230 | 0.01141 |
| sparse | 0.00000 | 0.01141 |

The executor’s original population has answer-level accuracy **0.888**, case-level accuracy **0.953333**. It is an alternative under the explicitly changed estimand. The old no-error bootstrap PASS frequency is 0.06375; the new procedure gives 0.02505. The answer-level point floor remains .90. Thirty perfect nonempty cases with 100 answers give L=.883 and INSUFFICIENT.

Power (descriptive synthetic probabilities):

| Case accuracy | Nonempty cases | Mechanism | PASS probability | MC SE |
|---|---|---|---|---|
| 0.95 | 50 | independent | 0.1212 | 0.0046 |
| 0.95 | 50 | whole-case | 0.1592 | 0.0052 |
| 0.95 | 80 | independent | 0.5510 | 0.0070 |
| 0.95 | 80 | whole-case | 0.3242 | 0.0066 |
| 0.95 | 120 | independent | 0.7726 | 0.0059 |
| 0.95 | 120 | whole-case | 0.3730 | 0.0068 |
| 0.95 | 160 | independent | 0.8700 | 0.0048 |
| 0.95 | 160 | whole-case | 0.4310 | 0.0070 |
| 0.97 | 50 | independent | 0.5280 | 0.0071 |
| 0.97 | 50 | whole-case | 0.3380 | 0.0067 |
| 0.97 | 80 | independent | 0.9140 | 0.0040 |
| 0.97 | 80 | whole-case | 0.6602 | 0.0067 |
| 0.97 | 120 | independent | 0.9818 | 0.0019 |
| 0.97 | 120 | whole-case | 0.7334 | 0.0063 |
| 0.97 | 160 | independent | 0.9936 | 0.0011 |
| 0.97 | 160 | whole-case | 0.8190 | 0.0054 |
| 0.985 | 50 | independent | 0.8842 | 0.0045 |
| 0.985 | 50 | whole-case | 0.5948 | 0.0069 |
| 0.985 | 80 | independent | 0.9922 | 0.0012 |
| 0.985 | 80 | whole-case | 0.9056 | 0.0041 |
| 0.985 | 120 | independent | 0.9990 | 0.0004 |
| 0.985 | 120 | whole-case | 0.9514 | 0.0030 |
| 0.985 | 160 | independent | 0.9998 | 0.0002 |
| 0.985 | 160 | whole-case | 0.9822 | 0.0019 |

| R2a Δ | Shape | Route power | MC SE | Strong power |
|---|---|---|---|---|
| 0.15 | high-variance | 0.0966 | 0.0042 | 0.0560 |
| 0.15 | low-variance | 0.5226 | 0.0071 | 0.0000 |
| 0.25 | high-variance | 0.4494 | 0.0070 | 0.3968 |
| 0.25 | low-variance | 1.0000 | 0.0000 | 0.5350 |

R2 power assumes its calibration prerequisites. No R-stat fallback fired. Exact values, Monte Carlo counts, power estimates and source hashes: `ACD_STATS_AUDIT_v2.3.json`.

- acd_stats.py: `1c97d51262a7546b70320c1207de554eff6f9b6a58b00428a2640f5ead6f685a`
- acd_stats_audit.py: `92e4f1954c53f68fe2c794265aa22651b1e5d0edfddbf13b22183276be6c8f2f`
