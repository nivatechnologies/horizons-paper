# Stage 16 run: CNN-F

Post hoc on confirmation; licenses no frozen route. Every run is reported, without selection among seeds. Case-level uncertainty and training-run variation are separate.

| Lead | State RMSE/sigma | State ACC | S confidence | Pooled S error | Case S error | Case error lower | Case error upper |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2.0 | 0.1222305645916389 | 0.982641089882762 | 0.72125 | 0.008665511265164683 | 0.007573582196697792 | 0.0 | 0.025000000000000022 |
| 3.0 | 0.26967646236052784 | 0.9272569891305935 | 0.4075 | 0.0076687116564416735 | 0.011134048995320667 | 0.0 | 0.040000000000000036 |

| Lead | Policy | Regret | Capture | Harms | Acting share | Chosen-action histogram |
|---|---|---:|---:|---:|---:|---|
| 2.0 | E | 0.008949414351581461 | 0.9714735983477135 | 1 | 1.0 | [150, 1, 2, 10, 14, 15, 3, 5, 0] |
| 2.0 | C_delta_0 | 0.01842447173651432 | 0.9412717011036449 | 1 | 0.975 | [147, 1, 2, 10, 14, 14, 3, 4, 5] |
| 3.0 | E | 0.08503967746662472 | 0.8427691794516248 | 11 | 1.0 | [94, 5, 7, 20, 19, 32, 8, 15, 0] |
| 3.0 | C_delta_0 | 0.18267198202213727 | 0.6622557083919911 | 1 | 0.71 | [76, 4, 4, 9, 15, 22, 3, 9, 58] |

| Lead | Patterns | Coverage | Answers | Pooled error | Case error |
|---|---|---:|---:|---:|---:|
| 2.0 | all_eight | 0.5 | 800 | 0.00125 | 0.0008680555555556912 |
| 2.0 | all_eight | 0.7 | 1120 | 0.00625 | 0.0055675805675805545 |
| 2.0 | seven_zero_mean | 0.5 | 700 | 0.0014285714285714286 | 0.0010869565217390686 |
| 2.0 | seven_zero_mean | 0.7 | 980 | 0.011224489795918367 | 0.009329446064139879 |
| 3.0 | all_eight | 0.5 | 800 | 0.02 | 0.02578725038402463 |
| 3.0 | all_eight | 0.7 | 1120 | 0.075 | 0.08685092127303162 |
| 3.0 | seven_zero_mean | 0.5 | 700 | 0.022857142857142857 | 0.02710827347698852 |
| 3.0 | seven_zero_mean | 0.7 | 980 | 0.08979591836734693 | 0.10561139028475708 |

Uniform-decrease collapse for E: {"2.0": false, "3.0": false}.

All training times, selected steps, guard outcomes, per-draw cost errors, confidence bounds, calibration tests, paired endpoints and histograms remain in the full receipt.
