# Stage 16 run: CNN-noF-seed1

Post hoc on confirmation; licenses no frozen route. Every run is reported, without selection among seeds. Case-level uncertainty and training-run variation are separate.

| Lead | State RMSE/sigma | State ACC | S confidence | Pooled S error | Case S error | Case error lower | Case error upper |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2.0 | 0.12588033156029854 | 0.9814012220006092 | 0.74375 | 0.06554621848739495 | 0.06353571428571425 | 0.04200000000000004 | 0.08699999999999997 |
| 3.0 | 0.27724899578680673 | 0.9233929106425421 | 0.46375 | 0.08086253369272234 | 0.11482412060301506 | 0.06999999999999995 | 0.16200000000000003 |

| Lead | Policy | Regret | Capture | Harms | Acting share | Chosen-action histogram |
|---|---|---:|---:|---:|---:|---|
| 2.0 | E | 0.05359153851836664 | 0.8291761122146777 | 6 | 1.0 | [200, 0, 0, 0, 0, 0, 0, 0, 0] |
| 2.0 | C_delta_0 | 0.049503452340670065 | 0.8422069524141288 | 5 | 0.995 | [199, 0, 0, 0, 0, 0, 0, 0, 1] |
| 3.0 | E | 0.26563275850931173 | 0.5088685913544396 | 30 | 1.0 | [200, 0, 0, 0, 0, 0, 0, 0, 0] |
| 3.0 | C_delta_0 | 0.25852836736867996 | 0.5220039804082908 | 29 | 0.995 | [199, 0, 0, 0, 0, 0, 0, 0, 1] |

| Lead | Patterns | Coverage | Answers | Pooled error | Case error |
|---|---|---:|---:|---:|---:|
| 2.0 | all_eight | 0.5 | 800 | 0.0375 | 0.03711414213926767 |
| 2.0 | all_eight | 0.7 | 1120 | 0.060714285714285714 | 0.05862499999999993 |
| 2.0 | seven_zero_mean | 0.5 | 700 | 0.045714285714285714 | 0.046065699006875405 |
| 2.0 | seven_zero_mean | 0.7 | 980 | 0.07142857142857142 | 0.07083934583934592 |
| 3.0 | all_eight | 0.5 | 800 | 0.085 | 0.10540476190476189 |
| 3.0 | all_eight | 0.7 | 1120 | 0.13035714285714287 | 0.142797619047619 |
| 3.0 | seven_zero_mean | 0.5 | 700 | 0.07857142857142857 | 0.07407979407979415 |
| 3.0 | seven_zero_mean | 0.7 | 980 | 0.13877551020408163 | 0.15018037518037508 |

Uniform-decrease collapse for E: {"2.0": true, "3.0": true}.

All training times, selected steps, guard outcomes, per-draw cost errors, confidence bounds, calibration tests, paired endpoints and histograms remain in the full receipt.
