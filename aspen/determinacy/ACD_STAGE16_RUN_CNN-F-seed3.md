# Stage 16 run: CNN-F-seed3

Post hoc on confirmation; licenses no frozen route. Every run is reported, without selection among seeds. Case-level uncertainty and training-run variation are separate.

| Lead | State RMSE/sigma | State ACC | S confidence | Pooled S error | Case S error | Case error lower | Case error upper |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2.0 | 0.12291900067318846 | 0.9822158321205802 | 0.715 | 0.009615384615384581 | 0.009487734487734545 | 0.0 | 0.028000000000000025 |
| 3.0 | 0.27219758049961634 | 0.9257630218424223 | 0.406875 | 0.01228878648233489 | 0.021139359698681748 | 0.0 | 0.052000000000000046 |

| Lead | Policy | Regret | Capture | Harms | Acting share | Chosen-action histogram |
|---|---|---:|---:|---:|---:|---|
| 2.0 | E | 0.018286784856963858 | 0.9417105802385248 | 1 | 1.0 | [147, 2, 2, 11, 15, 14, 4, 5, 0] |
| 2.0 | C_delta_0 | 0.02248441645641181 | 0.9283305622518707 | 0 | 0.96 | [144, 2, 2, 9, 14, 14, 3, 4, 8] |
| 3.0 | E | 0.08528118788438119 | 0.8423226481113602 | 11 | 0.995 | [90, 6, 10, 20, 17, 32, 9, 15, 1] |
| 3.0 | C_delta_0 | 0.17347100710530217 | 0.6792674948793845 | 1 | 0.715 | [73, 4, 6, 10, 13, 25, 2, 10, 57] |

| Lead | Patterns | Coverage | Answers | Pooled error | Case error |
|---|---|---:|---:|---:|---:|
| 2.0 | all_eight | 0.5 | 800 | 0.00125 | 0.0010309278350515427 |
| 2.0 | all_eight | 0.7 | 1120 | 0.007142857142857143 | 0.0067881192881192876 |
| 2.0 | seven_zero_mean | 0.5 | 700 | 0.0014285714285714286 | 0.0013513513513513375 |
| 2.0 | seven_zero_mean | 0.7 | 980 | 0.011224489795918367 | 0.01132167152575314 |
| 3.0 | all_eight | 0.5 | 800 | 0.0225 | 0.03136398176291777 |
| 3.0 | all_eight | 0.7 | 1120 | 0.07678571428571429 | 0.08536133046183303 |
| 3.0 | seven_zero_mean | 0.5 | 700 | 0.032857142857142856 | 0.035148645093396436 |
| 3.0 | seven_zero_mean | 0.7 | 980 | 0.08775510204081632 | 0.09699688920794436 |

Uniform-decrease collapse for E: {"2.0": false, "3.0": false}.

All training times, selected steps, guard outcomes, per-draw cost errors, confidence bounds, calibration tests, paired endpoints and histograms remain in the full receipt.
