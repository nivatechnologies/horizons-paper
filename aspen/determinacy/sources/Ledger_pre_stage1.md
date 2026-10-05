# Counterfactual determinacy claim ledger

| Date | Headline | Effect at operating point | Breadth | Headline value | Change type | Reason | Trigger hit? |
|---|---|---|---|---|---|---|---|
| 2026-10-05 | v2.1: instance-level posterior intervention-sign confidence against the unforced energy-anomaly sign, with covariance mechanism and question-targeted measurement | Unmeasured | Declared one-scale Lorenz-96, N=40, F_true=8, unknown inferred F∈[6,10], inherited actions and noise | Unmeasured; no scientific result | No scope or threshold change | Pre-data spec gate halted: nominal accuracy bounds fail a synthetic scoring counterexample | Spec-integrity check 4; amendment required before Step 0 |

# Aspen counterfactual determinacy — pre-data spec halt

2026-10-05. Work order: [[WO_Aspen-Counterfactual-Determinacy-2026-10-04]], v2.1. Branch `paper/aspen-2026-10-determinacy` pinned to `1b1094a`.

Step 0b is complete: exact prompt and verbatim blinded Codex CLI answer, with overlap, committed at `eb87279`. [Selector](https://github.com/nivatechnologies/horizons-paper/blob/91e77a6/aspen/determinacy/CODEX_SELECTOR.md).

**HALT before Step 0: spec integrity check 4 fails.** The raw case-percentile bootstrap in §10 does not license the nominal accuracy confidence bounds used by R0/R0-F. A synthetic 200-case population has ratio-of-sums accuracy 0.888; a no-error sample meeting ≥100 answers and ≥30 cases receives a bootstrap lower bound of 1. Its exact probability is 0.061120375098500886, above the stated 5% error rate. Empty-replicate handling cannot remove this counterexample: even invalidating a whole run on an empty replicate reduces the probability by less than 8e-11. This is a mathematical scoring-input counterexample, not an observed Lorenz-96 failure.

[Full gate and witness inventory](https://github.com/nivatechnologies/horizons-paper/blob/91e77a6/aspen/determinacy/ACD_SPEC_GATE.md), [audit script](https://github.com/nivatechnologies/horizons-paper/blob/91e77a6/aspen/determinacy/spec_boundary_counterexample.py), [sulaco CPU receipt](https://github.com/nivatechnologies/horizons-paper/blob/91e77a6/aspen/determinacy/SPEC_BOUNDARY_COUNTEREXAMPLE.json). Gate report commit: `91e77a6`.

No development/confirmation data were read and no scientific numerical run, training, freeze or CNN inference started. Baccus forecast-decision close-out and Qwen services remain untouched. Request a targeted statistical amendment specifying defensible bounds at sparse-error boundaries and case dependence, with a differential prediction retaining low-accuracy failures and count floors; then rerun the gate. Scientific headline value remains unmeasured; this is not a scientific kill.



## v2.2 gate update

| Date | Headline | Effect at operating point | Breadth | Headline value | Change type | Reason | Trigger hit? |
|---|---|---|---|---|---|---|---|
| 2026-10-05 | v2.2 headline; L2 now states case-averaged accuracy and gives answer-level accuracy alongside | Unmeasured | Scientific scope unchanged | Unmeasured | Explicit estimand and status change in Amendment 1 | Betting/exact procedures implemented; prescribed synthetic checks pass, but grid inversion excludes unrejected continuous means | Check 4 blocks sign-off before Step 0 |

# v2.2 statistical audit and spec halt

2026-10-05. [[WO_Aspen-Counterfactual-Determinacy-2026-10-04]] v2.2, Amendment 1. Branch `paper/aspen-2026-10-determinacy`; commit `dd82355`. Step 0b at `eb87279` remains byte-for-byte unchanged.

Implemented §10 standalone statistics and ran the complete prescribed synthetic audit on sulaco CPU. Exact Clopper–Pearson and McNemar checks pass. All nine R0 null configurations (20,000 panels of 200 cases each) pass; maximum false PASS .02685. All three R2 mean-zero configurations pass; maximum noncoverage .00425. Full power table (5,000 panels/cell) and the original .888 construction are reported. That construction's new case-average accuracy is .9533333333, so it is an alternative under the changed estimand, not a .90 case-mean null. Its 30-perfect-case fixture has lower .857 and is INSUFFICIENT.

**New halt: literal grid inversion does not preserve the continuous retained set.** With 200 synthetic x values all 1, the reported 99% interval is [.963,1], but m=.9629 has hedged prefix maximum 89.0105921166<100 and is never rejected by the specified capital rule. It is nevertheless omitted by the grid interval. The reflected all-zero case omits unrejected .0371 from [0,.037]. This demonstrates an inversion-consistency failure, **not** a measured exceedance of a Monte Carlo error-rate limit. The claimed finite-sample coverage proof therefore cannot be signed off under spec check 4 as written.

[Statistical audit and power table](https://github.com/nivatechnologies/horizons-paper/blob/dd82355/aspen/determinacy/ACD_STATS_AUDIT.md), [full re-assessed spec gate](https://github.com/nivatechnologies/horizons-paper/blob/dd82355/aspen/determinacy/ACD_SPEC_GATE.md), [prescribed audit receipt](https://github.com/nivatechnologies/horizons-paper/blob/dd82355/aspen/determinacy/STATS_AUDIT.json), [grid witness receipt](https://github.com/nivatechnologies/horizons-paper/blob/dd82355/aspen/determinacy/STATS_GRID_AUDIT.json).

Required correction: specify and justify conservative continuous-mean inversion, accounting for the possible nonconvexity of aGRAPA retained sets. Differential prediction: .9629/.0371 stay included when unrejected; the 30-perfect-case fixture stays INSUFFICIENT; five Q-only discordances stay nonsignificant; floors and route prerequisites remain binding. No replacement procedure or threshold was applied.

No experimental data read; Step 0 and all scientific stages remain unstarted. No confirmation, freeze, CNN, training, cloud computation or service changes. Baccus close-out untouched.

