# Stage 16 run: CNN-noF-seed4

Post hoc on confirmation; licenses no frozen route. Every run is reported, without selection among seeds. Case-level uncertainty and training-run variation are separate.

| Lead | State RMSE/sigma | State ACC | S confidence | Pooled S error | Case S error | Case error lower | Case error upper |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2.0 | 0.12269613757542236 | 0.9824488176251527 | 0.75 | 0.06916666666666671 | 0.06880357142857152 | 0.04700000000000004 | 0.09199999999999997 |
| 3.0 | 0.271870610104885 | 0.9259694514455562 | 0.456875 | 0.07797537619699046 | 0.11282142857142863 | 0.06599999999999995 | 0.128 |

| Lead | Policy | Regret | Capture | Harms | Acting share | Chosen-action histogram |
|---|---|---:|---:|---:|---:|---|
| 2.0 | E | 0.05359153851836664 | 0.8291761122146777 | 6 | 1.0 | [200, 0, 0, 0, 0, 0, 0, 0, 0] |
| 2.0 | C_delta_0 | 0.049503452340670065 | 0.8422069524141288 | 5 | 0.995 | [199, 0, 0, 0, 0, 0, 0, 0, 1] |
| 3.0 | E | 0.26563275850931173 | 0.5088685913544396 | 30 | 1.0 | [200, 0, 0, 0, 0, 0, 0, 0, 0] |
| 3.0 | C_delta_0 | 0.26563275850931173 | 0.5088685913544396 | 30 | 1.0 | [200, 0, 0, 0, 0, 0, 0, 0, 0] |

| Lead | Patterns | Coverage | Answers | Pooled error | Case error |
|---|---|---:|---:|---:|---:|
| 2.0 | all_eight | 0.5 | 800 | 0.03625 | 0.038167388167388294 |
| 2.0 | all_eight | 0.7 | 1120 | 0.059821428571428574 | 0.05909523809523809 |
| 2.0 | seven_zero_mean | 0.5 | 700 | 0.041428571428571426 | 0.04105848861283645 |
| 2.0 | seven_zero_mean | 0.7 | 980 | 0.07551020408163266 | 0.07708940719144797 |
| 3.0 | all_eight | 0.5 | 800 | 0.08375 | 0.10542857142857132 |
| 3.0 | all_eight | 0.7 | 1120 | 0.12589285714285714 | 0.13754761904761892 |
| 3.0 | seven_zero_mean | 0.5 | 700 | 0.08 | 0.08135764944275581 |
| 3.0 | seven_zero_mean | 0.7 | 980 | 0.1346938775510204 | 0.13943001443001446 |

Uniform-decrease collapse for E: {"2.0": true, "3.0": true}.

All training times, selected steps, guard outcomes, per-draw cost errors, confidence bounds, calibration tests, paired endpoints and histograms remain in the full receipt.
