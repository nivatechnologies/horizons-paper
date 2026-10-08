# Stage 16 run: CNN-F-seed1

Post hoc on confirmation; licenses no frozen route. Every run is reported, without selection among seeds. Case-level uncertainty and training-run variation are separate.

| Lead | State RMSE/sigma | State ACC | S confidence | Pooled S error | Case S error | Case error lower | Case error upper |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2.0 | 0.12173085736746007 | 0.982784267942989 | 0.72125 | 0.0077989601386482255 | 0.006721981721981796 | 0.0 | 0.025000000000000022 |
| 3.0 | 0.2708719108359547 | 0.9263362739829093 | 0.406875 | 0.007680491551459334 | 0.012026515151515205 | 0.0 | 0.040000000000000036 |

| Lead | Policy | Regret | Capture | Harms | Acting share | Chosen-action histogram |
|---|---|---:|---:|---:|---:|---|
| 2.0 | E | 0.018156893639259368 | 0.9421246105763526 | 1 | 1.0 | [149, 2, 2, 10, 16, 14, 4, 3, 0] |
| 2.0 | C_delta_0 | 0.022013121767976013 | 0.9298328216233495 | 0 | 0.96 | [146, 1, 2, 8, 15, 14, 3, 3, 8] |
| 3.0 | E | 0.0784428916332222 | 0.8549660513174058 | 11 | 0.995 | [90, 7, 9, 18, 17, 31, 11, 16, 1] |
| 3.0 | C_delta_0 | 0.18493449875237944 | 0.6580725156448172 | 1 | 0.7 | [74, 4, 5, 9, 11, 23, 2, 12, 60] |

| Lead | Patterns | Coverage | Answers | Pooled error | Case error |
|---|---|---:|---:|---:|---:|
| 2.0 | all_eight | 0.5 | 800 | 0.0 | 0.0 |
| 2.0 | all_eight | 0.7 | 1120 | 0.00625 | 0.005489417989417933 |
| 2.0 | seven_zero_mean | 0.5 | 700 | 0.0 | 0.0 |
| 2.0 | seven_zero_mean | 0.7 | 980 | 0.012244897959183673 | 0.010349854227405197 |
| 3.0 | all_eight | 0.5 | 800 | 0.02 | 0.02747644512350389 |
| 3.0 | all_eight | 0.7 | 1120 | 0.07589285714285714 | 0.08692869107441958 |
| 3.0 | seven_zero_mean | 0.5 | 700 | 0.024285714285714285 | 0.028742436200999588 |
| 3.0 | seven_zero_mean | 0.7 | 980 | 0.08673469387755102 | 0.09879157693228047 |

Uniform-decrease collapse for E: {"2.0": false, "3.0": false}.

All training times, selected steps, guard outcomes, per-draw cost errors, confidence bounds, calibration tests, paired endpoints and histograms remain in the full receipt.
