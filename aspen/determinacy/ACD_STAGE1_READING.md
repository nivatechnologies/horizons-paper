# Aspen counterfactual determinacy — Stage 1 (v2.3)

**Stage 1 gate: STRONG.** Development only; Todd decides whether to authorize a freeze and confirmation.

Completed 200 cases on sulaco CPU at dt=0.01; truth coverage 192/200; diagnostic exclusions 0/200.

| Lead (LT) | R0 | Case accuracy [L,U] | Answer accuracy / answers / cases | Included-case R0 accuracy [L,U] | R0-F |
|---|---|---|---|---|---|
| 0 | PASS | 1.000 [0.983, 1.000] | 1.0 / 1374 / 200 | PASS 1.0 [0.983, 1.000] | PASS |
| 1 | PASS | 0.999 [0.982, 1.000] | 0.9992175273865415 / 1278 / 200 | PASS 0.9991666666666668 [0.982, 1.000] | PASS |
| 1.5 | PASS | 0.998 [0.980, 1.000] | 0.9974747474747475 / 1188 / 200 | PASS 0.9977380952380953 [0.980, 1.000] | PASS |
| 2 | PASS | 0.994 [0.976, 1.000] | 0.9939879759519038 / 998 / 196 | PASS 0.9942419825072886 [0.976, 1.000] | PASS |
| 2.5 | PASS | 0.994 [0.974, 1.000] | 0.9925768822905621 / 943 / 194 | PASS 0.993759204712813 [0.974, 1.000] | PASS |
| 3 | PASS | 0.986 [0.964, 1.000] | 0.9896602658788775 / 677 / 180 | PASS 0.9862433862433863 [0.964, 1.000] | PASS |
| 4 | PASS | 0.988 [0.947, 1.000] | 0.9895833333333334 / 288 / 115 | PASS 0.9884057971014493 [0.947, 1.000] | PASS |
| 6 | NOT EVALUABLE | 1.000 [0.088, 1.000] | 1.0 / 5 / 5 | NOT EVALUABLE 1.0 [0.088, 1.000] | NOT EVALUABLE |

| Lead (LT) | All-confident S | Observation-confident S | Confident Fc | Median rho | Median cancellation |
|---|---|---|---|---|---|
| 2 | 0.744 | 0.624 | 0.845 | 0.979 | 0.026 |
| 3 | 0.423 | 0.423 | 0.605 | 0.762 | 0.261 |

R0 includes the required sensitivity with excluded cases included; the worse status governs. Bounds are v2.3 betting bounds; R0-F uses exact Clopper–Pearson.

R2a at 2 LT: DIFFERS; Δ=-0.221, 99% interval [-0.322, -0.106].
R2a at 3 LT: DIFFERS; Δ=-0.182, 99% interval [-0.310, -0.072].

R2b: PRECEDES; Δ_loss=-0.210, 99% interval [-0.384, -0.016], 192 eligible cases.

R5 at 2 LT: Q-BEATS; common population 60; margin 0.23333333333333334. Only Q, F, V and R support the tested comparison.

| Arm | Confident correct / population | Confident wrong | Accuracy lower bound | Truth coverage |
|---|---|---|---|---|---|
| Q | 27 / 60 | 0 | 0.895 | 0.950 |
| F | 13 / 60 | 0 | 0.794 | 0.950 |
| V | 7 / 60 | 0 | 0.652 | 0.917 |
| R | 6 / 60 | 0 | 0.607 | 0.950 |

Exact one-sided McNemar p-values (Q against each alternative): V: 1.7940998e-05, F: 0.00025939941, R: 4.7683716e-07. The Q accuracy/count/coverage safeguards and R0 at 2 LT pass.

Forecast-horizon rule R2c: largest lead with at least half the panel’s Fc answers confident is 3.0 LT. Its errors/refusals at every lead are in the receipt.

| Comparator | Lead (LT) | Confident S share | Observation-confident S share | Case accuracy [L,U] | R0 | S classification kappa |
|---|---|---|---|---|---|---|
| Crude | 2 | 0.404 | 0.290 | 0.991 [0.973, 1.000] | PASS | 0.475 |
| Crude | 3 | 0.111 | 0.111 | 0.950 [0.871, 0.999] | INSUFFICIENT | 0.278 |
| RML | 2 | 0.741 | 0.621 | 0.997 [0.979, 1.000] | PASS | 0.965 |
| RML | 3 | 0.436 | 0.436 | 0.991 [0.970, 1.000] | PASS | 0.934 |

Resolution rules fired: R-other, R-rml, R-time.

- **R-other**: Spec gate scope findings.
- **R-rml**: Full-panel signed-event cross-check flags.
- **R-time**: Stages1–3 full projection exceeds12h.

R-time resolution: initial serial projection 29.16 hours; prescribed cuts R7, R5-A, R6-3LT, RML-conf, P/B-other-leads, R5-3LT; R5 cap 60, 1000 warmup and 500 draws per chain. Arm A is cut after its required Stage0 benchmark.

R-rml resolution: report the full-panel signed-event flags as coupled diagnostics; RML remains an approximate cross-check. The Stage1a 0/160 result did not trigger its rerun rule.

R-other resolutions: report the literal climate classification without a proven confidence ordering; name only Q/F/V/R in the tested targeting comparison (regret/scenario targeting is untested); report Wilks truth coverage as measured, approximate coverage.

All share/mechanism/comparator bootstrap intervals are approximate and descriptive. Extra selector readings (unforced distribution, effect magnitudes/backfire, nine-action best and regret) are reported only. The full receipt includes R1/R1m maps, reliability, rank histogram, threshold uncertainty, split stability, RML cross-checks and R5 site/refit records: `runs/audit/acd_stage1.json`.

This is development analysis; it licenses no confirmation claim. Work stops here. No freeze, confirmation reading or CNN inference was performed.
