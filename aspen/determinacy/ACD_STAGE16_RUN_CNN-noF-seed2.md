# Stage 16 run: CNN-noF-seed2

Post hoc on confirmation; licenses no frozen route. Every run is reported, without selection among seeds. Case-level uncertainty and training-run variation are separate.

| Lead | State RMSE/sigma | State ACC | S confidence | Pooled S error | Case S error | Case error lower | Case error upper |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2.0 | 0.12372494395274164 | 0.9821591515988132 | 0.740625 | 0.0582278481012658 | 0.05687963627662118 | 0.03600000000000003 | 0.07899999999999996 |
| 3.0 | 0.2731837345162948 | 0.9254718405372104 | 0.46125 | 0.08130081300813008 | 0.10979301268245989 | 0.06599999999999995 | 0.139 |

| Lead | Policy | Regret | Capture | Harms | Acting share | Chosen-action histogram |
|---|---|---:|---:|---:|---:|---|
| 2.0 | E | 0.05359153851836664 | 0.8291761122146777 | 6 | 1.0 | [200, 0, 0, 0, 0, 0, 0, 0, 0] |
| 2.0 | C_delta_0 | 0.049503452340670065 | 0.8422069524141288 | 5 | 0.995 | [199, 0, 0, 0, 0, 0, 0, 0, 1] |
| 3.0 | E | 0.26563275850931173 | 0.5088685913544396 | 30 | 1.0 | [200, 0, 0, 0, 0, 0, 0, 0, 0] |
| 3.0 | C_delta_0 | 0.25852836736867996 | 0.5220039804082908 | 29 | 0.995 | [199, 0, 0, 0, 0, 0, 0, 0, 1] |

| Lead | Patterns | Coverage | Answers | Pooled error | Case error |
|---|---|---:|---:|---:|---:|
| 2.0 | all_eight | 0.5 | 800 | 0.0325 | 0.03347763347763355 |
| 2.0 | all_eight | 0.7 | 1120 | 0.054464285714285715 | 0.05287150035893773 |
| 2.0 | seven_zero_mean | 0.5 | 700 | 0.041428571428571426 | 0.04383458646616534 |
| 2.0 | seven_zero_mean | 0.7 | 980 | 0.0653061224489796 | 0.06514382402707264 |
| 3.0 | all_eight | 0.5 | 800 | 0.08125 | 0.10626346015793253 |
| 3.0 | all_eight | 0.7 | 1120 | 0.12232142857142857 | 0.13286309523809536 |
| 3.0 | seven_zero_mean | 0.5 | 700 | 0.07571428571428572 | 0.07876447876447867 |
| 3.0 | seven_zero_mean | 0.7 | 980 | 0.12653061224489795 | 0.13640823163436222 |

Uniform-decrease collapse for E: {"2.0": true, "3.0": true}.

All training times, selected steps, guard outcomes, per-draw cost errors, confidence bounds, calibration tests, paired endpoints and histograms remain in the full receipt.
