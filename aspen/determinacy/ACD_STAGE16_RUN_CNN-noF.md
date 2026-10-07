# Stage 16 run: CNN-noF

Post hoc on confirmation; licenses no frozen route. Every run is reported, without selection among seeds. Case-level uncertainty and training-run variation are separate.

| Lead | State RMSE/sigma | State ACC | S confidence | Pooled S error | Case S error | Case error lower | Case error upper |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2.0 | 0.12284385860398833 | 0.982278424658333 | 0.740625 | 0.0658227848101266 | 0.06238690476190467 | 0.041000000000000036 | 0.08499999999999996 |
| 3.0 | 0.27178083353422244 | 0.9259207405767692 | 0.4625 | 0.07567567567567568 | 0.10875209380234496 | 0.06599999999999995 | 0.15500000000000003 |

| Lead | Policy | Regret | Capture | Harms | Acting share | Chosen-action histogram |
|---|---|---:|---:|---:|---:|---|
| 2.0 | E | 0.05359153851836664 | 0.8291761122146777 | 6 | 1.0 | [200, 0, 0, 0, 0, 0, 0, 0, 0] |
| 2.0 | C_delta_0 | 0.049503452340670065 | 0.8422069524141288 | 5 | 0.995 | [199, 0, 0, 0, 0, 0, 0, 0, 1] |
| 3.0 | E | 0.26563275850931173 | 0.5088685913544396 | 30 | 1.0 | [200, 0, 0, 0, 0, 0, 0, 0, 0] |
| 3.0 | C_delta_0 | 0.25852836736867996 | 0.5220039804082908 | 29 | 0.995 | [199, 0, 0, 0, 0, 0, 0, 0, 1] |

| Lead | Patterns | Coverage | Answers | Pooled error | Case error |
|---|---|---:|---:|---:|---:|
| 2.0 | all_eight | 0.5 | 800 | 0.0375 | 0.03899711399711414 |
| 2.0 | all_eight | 0.7 | 1120 | 0.059821428571428574 | 0.05623809523809509 |
| 2.0 | seven_zero_mean | 0.5 | 700 | 0.04428571428571428 | 0.045109395109395156 |
| 2.0 | seven_zero_mean | 0.7 | 980 | 0.07346938775510205 | 0.0709813874788493 |
| 3.0 | all_eight | 0.5 | 800 | 0.07875 | 0.10272023809523811 |
| 3.0 | all_eight | 0.7 | 1120 | 0.12142857142857143 | 0.1289107142857142 |
| 3.0 | seven_zero_mean | 0.5 | 700 | 0.07285714285714286 | 0.07051671732522802 |
| 3.0 | seven_zero_mean | 0.7 | 980 | 0.12857142857142856 | 0.12907647907647923 |

Uniform-decrease collapse for E: {"2.0": true, "3.0": true}.

All training times, selected steps, guard outcomes, per-draw cost errors, confidence bounds, calibration tests, paired endpoints and histograms remain in the full receipt.
