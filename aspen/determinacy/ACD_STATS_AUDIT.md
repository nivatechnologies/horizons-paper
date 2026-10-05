# ACD statistical audit — v2.2

**Overall statistical audit: HALT.** The prescribed exact-value and Monte Carlo checks pass; an inversion-consistency check fails. All data below are synthetic hypotheses under test. No experimental input was opened. Run on sulaco CPU with 16 Numba threads, NumPy 2.5.3, SciPy 1.18.1. Wall time including compilation: 15.238 seconds.

Implementation: `statistics.py`. Driver: `stats_audit.py`. Receipt: `STATS_AUDIT.json`. Seed 2026100522 is an audit-only stream; no experimental namespace is used. Step 0b remains unchanged at eb87279.

## Conventions and exact checks

Running pseudo moments are count=1, sum=0.5, sum of squares=0.5: one unit of prior weight with mean 0.5 and variance 0.25. Bets depend only on earlier cases, including these prior moments. Capital is accumulated in log space, and rejection uses the maximum over all prefixes. Bounds follow the stated 0.001 grid literally. If no lower grid value is rejected at 0.500, return the trivial lower bound 0; endpoints 0 and 1 use the finite limiting bet. No monotonicity is assumed: each preceding grid point is checked for a one-sided scan; two-sided intervals use the complete retained-grid hull.

R0 filters empty cases for case-averaged accuracy and retains them in the transformed answer-ratio process. NOT EVALUABLE precedes PASS/FAIL; INSUFFICIENT is evaluable with neither bound establishing a direction. Descriptive bootstraps redraw empty-denominator replicates and report redraws; an entirely empty denominator is NOT EVALUABLE.

Clopper–Pearson maximum difference from SciPy exact bounds: 4.77e-15 (tolerance 1e-10). Checked every success count at n=1,5,20,30,34,40,100,200; the two tails of a 90% two-sided interval are the requested one-sided 95% bounds.

McNemar maximum absolute error: 6.66e-16 (tolerance 1e-12). Checked every discordance split with 1–100 discordant cases against SciPy and an independently summed exact binomial tail. No discordance gives p=1; five discordances all for Q give p=0.03125. Thirty perfect Fc cases give a lower bound of 0.904966147145 and PASS.

References: [SciPy exact Clopper–Pearson documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats._result_classes.BinomTestResult.proportion_ci.html), [SciPy exact binomial test](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.binomtest.html). The betting source is [Waudby-Smith and Ramdas, Estimating means of bounded random variables by betting](https://arxiv.org/html/2010.09686v7). Predictable nonnegative capital gives point-null control under a common conditional mean; iid case streams meet that condition. This audit does not establish arbitrary continuous-parameter coverage solely by simulations at grid means.

## Null validity

20,000 independent panels of 200 cases per row. False PASS is the complete R0 rule, including both count floors and the answer-level point floor. The executor distribution is {0:.85,1:.10,8:.05}; uniform is 0–8 inclusive; half empty is P(0)=.5 with the other half uniform on 1–8. Independent mechanisms use binomial answer errors; whole-case mechanisms make all answers correct or wrong together; eight-only makes all eight fail together with probability .3 (executor) or .8 (uniform/half-empty), making nonempty case-averaged accuracy exactly .90. This is not the same as an answer-level .90 null.

The criterion is observed rate ≤ nominal + 2 empirical Monte Carlo SE. Zero observed events yield SE=0; they do not imply a zero population error probability.

| Sizes | Mechanism | Evaluable panels | False PASS | MC SE | Limit | Result |
|---|---|---:|---:|---:|---:|---|
| executor | independent | 7571 | 0.00000 | 0.000000 | 0.050000 | PASS |
| executor | whole-case | 7742 | 0.00015 | 0.000087 | 0.050173 | PASS |
| executor | eight-only | 7720 | 0.00000 | 0.000000 | 0.050000 | PASS |
| uniform | independent | 20000 | 0.00765 | 0.000616 | 0.051232 | PASS |
| uniform | whole-case | 20000 | 0.02685 | 0.001143 | 0.052286 | PASS |
| uniform | eight-only | 20000 | 0.00695 | 0.000587 | 0.051175 | PASS |
| half-empty | independent | 20000 | 0.00145 | 0.000269 | 0.050538 | PASS |
| half-empty | whole-case | 20000 | 0.02050 | 0.001002 | 0.052004 | PASS |
| half-empty | eight-only | 20000 | 0.01450 | 0.000845 | 0.051691 | PASS |

R2 mean-zero differences: symmetric ±1 with equal weights; skewed −1/.25 with weights .2/.8; sparse −1/0/1 with weights .01/.98/.01. Transformed x=(d+1)/2, α=.01. Coverage uses the literal full-grid interval; a capital crossing at zero need not be noncoverage if the retained-grid hull still contains zero.

| Differences | Noncoverage | MC SE | Limit | Result |
|---|---:|---:|---:|---|
| symmetric | 0.00425 | 0.000460 | 0.010920 | PASS |
| skewed | 0.00330 | 0.000406 | 0.010811 | PASS |
| sparse | 0.00000 | 0.000000 | 0.010000 | PASS |

## The 0.888 construction and differential prediction

Preserved original case probabilities: (0,0)=.85, (1,1)=.10, (8,8)=.043, (8,0)=.007. Answer-level accuracy is .888; **case-averaged accuracy is .9533333333**, so this construction is an alternative, not a .90 case-mean null under the new estimand. The original analytic false-PASS event probability was .0611203751; the new synthetic run reproduces it within MC error.

Old no-error/count-floor event: 0.06305 ± 0.001719 MC SE. New full-rule PASS: 0.00050 ± 0.000158 MC SE. The latter is not called a false-PASS rate for the case estimand.

Concrete 200-case panel with 10 eight-answer perfect cases, 20 one-answer perfect cases, 170 empty cases: 100 answers, 30 cases, case and answer points both 1. Betting case lower bound **.857**, upper 1, transformed answer-ratio lower **.703**: **INSUFFICIENT**, as the amendment predicts. Forty perfect cases lower=.890; 44 perfect cases lower=.900; 50 perfect cases lower=.911. These are rule calculations, not experimental outcomes.

## Power (reported; no power-based halt)

5,000 panels of 200 cases per cell; first n cases are nonempty with sizes uniform 1–8, remaining cases empty. Accuracy is the true nonempty case mean; independent answers and whole-case errors have that same mean. Full R0 PASS includes all point/count conditions. Values are PASS probability (MC SE).

| True case accuracy | Nonempty cases | Independent answers | Whole-case errors |
|---|---:|---:|---:|
| 0.95 | 50 | 0.0038 (0.0009) | 0.0946 (0.0041) |
| 0.95 | 80 | 0.2952 (0.0065) | 0.2078 (0.0057) |
| 0.95 | 120 | 0.6652 (0.0067) | 0.3546 (0.0068) |
| 0.95 | 160 | 0.8562 (0.0050) | 0.4566 (0.0070) |
| 0.97 | 50 | 0.0744 (0.0037) | 0.2550 (0.0062) |
| 0.97 | 80 | 0.7900 (0.0058) | 0.4724 (0.0071) |
| 0.97 | 120 | 0.9756 (0.0022) | 0.7372 (0.0062) |
| 0.97 | 160 | 0.9954 (0.0010) | 0.8550 (0.0050) |
| 0.985 | 50 | 0.4308 (0.0070) | 0.5226 (0.0071) |
| 0.985 | 80 | 0.9708 (0.0024) | 0.7846 (0.0058) |
| 0.985 | 120 | 0.9996 (0.0003) | 0.9620 (0.0027) |
| 0.985 | 160 | 1.0000 (0.0000) | 0.9924 (0.0012) |

At .97 and 80 cases, independent-answer power is .7900; whole-case power is .4724. At 120 cases these rise to .9756 and .7372. The amendment’s quoted power is distribution dependent; it is not a guarantee for arbitrary case dependence.

R2a power uses 200 cases. High variance is d∈{−1,+1}, with P(+1)=(1+Δ)/2. Low variance is d=Δ±.25 with equal probability. Both are bounded in [−1,1]. Statistical route power assumes R0/R0-F prerequisites already hold. Publish includes point margin .15 and a 99% interval excluding zero; strong uses .25. A population at a point margin will cross that point margin in only about half its samples even with very narrow intervals.

| Δ | Distribution | Publish power (SE) | Strong power (SE) |
|---|---|---:|---:|
| 0.15 | high-variance | 0.0892 (0.0040) | 0.0626 (0.0034) |
| 0.15 | low-variance | 0.5338 (0.0071) | 0.0000 (0.0000) |
| 0.25 | high-variance | 0.4970 (0.0071) | 0.4586 (0.0070) |
| 0.25 | low-variance | 1.0000 (0.0000) | 0.5254 (0.0071) |

## Reproduction and scope

Run from this directory on sulaco:

```bash
NUMBA_NUM_THREADS=16 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/todd/work/aspen-horizon-20261004/.venv/bin/python stats_audit.py
```

This uses an existing environment without installing packages or modifying Qwen services. Source hashes are recorded in STATS_AUDIT.json. The prescribed synthetic checks pass; the full specification must still pass its separate integrity gate before Step 0. No scientific result or publish route is licensed by this audit.

## Inversion consistency failure — halt

The synthetic Monte Carlo tests above are at case accuracy .90 and difference 0, both exactly on the specified grid. They pass. A separate deterministic check tests the claimed inversion of continuous-mean capital tests into a confidence interval, and fails. `stats_grid_audit.py` and `STATS_GRID_AUDIT.json` reproduce this on sulaco without experimental inputs.

For 200 x_c values equal to 1, the literal 99% grid interval is [0.963, 1]. At m=0.9629, the largest K+ over prefixes is 178.02118423327562 and the largest K− is 1. The declared rejection threshold is max(0.5K+,0.5K−)≥100, or an individual capital ≥200. This m is **not rejected** (hedged maximum 89.0105921166), yet the reported interval excludes it. The reflected construction, 200 values all equal to 0, gives [0,.037] and omits unrejected m=.0371 for the same reason.

This establishes that the literal grid interval is not an outer approximation to the continuous retained set defined by the stated capital rule. It does **not** establish that any prescribed Monte Carlo noncoverage rate exceeded its limit; those rates passed. Ville's inequality controls exclusion of each true mean by its capital, but that proof alone does not license the extra exclusions from this grid construction. The WO asserts finite-sample validity for all route intervals, while m is a real number, not a grid-valued parameter. The full spec gate cannot sign off on that assertion as written.

No interval endpoint, capital threshold, grid spacing, bet or publish margin was changed to resolve this. A correction must specify and justify conservative inversion for continuous means, including possible nonconvex aGRAPA retained sets, or explicitly change the inferential target. Simple inward rounding must not exclude an unrejected mean. Appendix E.4 of the [primary betting paper](https://arxiv.org/html/2010.09686v7) warns that aGRAPA sublevel sets need not be intervals; a monotone root-search assumption therefore also needs justification.

Differential prediction: the 30-perfect-case R0 fixture stays INSUFFICIENT; five Q-favouring discordances stay nonsignificant at .01; the disclosed answer-point floor and all route prerequisites remain binding; the retained continuous means .9629 and .0371 must no longer be removed solely by grid endpoints. The executor has not selected a replacement procedure. Stop before Step 0 under §10/§14 and the spec gate.
