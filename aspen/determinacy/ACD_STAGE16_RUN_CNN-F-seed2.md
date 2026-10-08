# Stage 16 run: CNN-F-seed2

Post hoc on confirmation; licenses no frozen route. Every run is reported, without selection among seeds. Case-level uncertainty and training-run variation are separate.

| Lead | State RMSE/sigma | State ACC | S confidence | Pooled S error | Case S error | Case error lower | Case error upper |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2.0 | 0.12128988716266453 | 0.9827426969953712 | 0.713125 | 0.006134969325153339 | 0.005342187126106679 | 0.0 | 0.02300000000000002 |
| 3.0 | 0.2679098861972505 | 0.9274443713091889 | 0.415625 | 0.010526315789473717 | 0.018632958801498067 | 0.0 | 0.04600000000000004 |

| Lead | Policy | Regret | Capture | Harms | Acting share | Chosen-action histogram |
|---|---|---:|---:|---:|---:|---|
| 2.0 | E | 0.018283585136917524 | 0.9417207793974454 | 2 | 1.0 | [149, 2, 2, 12, 13, 13, 4, 5, 0] |
| 2.0 | C_delta_0 | 0.018471086174888587 | 0.9411231168343708 | 0 | 0.97 | [146, 2, 2, 10, 13, 13, 4, 4, 6] |
| 3.0 | E | 0.07296240409998975 | 0.8650989866427247 | 11 | 0.99 | [93, 7, 10, 20, 17, 30, 5, 16, 2] |
| 3.0 | C_delta_0 | 0.16516190963797883 | 0.6946302790728736 | 1 | 0.725 | [74, 5, 6, 11, 13, 24, 1, 11, 55] |

| Lead | Patterns | Coverage | Answers | Pooled error | Case error |
|---|---|---:|---:|---:|---:|
| 2.0 | all_eight | 0.5 | 800 | 0.0 | 0.0 |
| 2.0 | all_eight | 0.7 | 1120 | 0.005357142857142857 | 0.004714046422589102 |
| 2.0 | seven_zero_mean | 0.5 | 700 | 0.0 | 0.0 |
| 2.0 | seven_zero_mean | 0.7 | 980 | 0.01020408163265306 | 0.01024897268552083 |
| 3.0 | all_eight | 0.5 | 800 | 0.02 | 0.030417621594092115 |
| 3.0 | all_eight | 0.7 | 1120 | 0.075 | 0.08644412538884905 |
| 3.0 | seven_zero_mean | 0.5 | 700 | 0.027142857142857142 | 0.03080687830687845 |
| 3.0 | seven_zero_mean | 0.7 | 980 | 0.08673469387755102 | 0.09819334769083499 |

Uniform-decrease collapse for E: {"2.0": false, "3.0": false}.

All training times, selected steps, guard outcomes, per-draw cost errors, confidence bounds, calibration tests, paired endpoints and histograms remain in the full receipt.
