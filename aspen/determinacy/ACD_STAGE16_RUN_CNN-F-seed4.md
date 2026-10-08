# Stage 16 run: CNN-F-seed4

Post hoc on confirmation; licenses no frozen route. Every run is reported, without selection among seeds. Case-level uncertainty and training-run variation are separate.

| Lead | State RMSE/sigma | State ACC | S confidence | Pooled S error | Case S error | Case error lower | Case error upper |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2.0 | 0.12240569439801482 | 0.9822481829201888 | 0.72375 | 0.010362694300518172 | 0.008796296296296191 | 0.0 | 0.026000000000000023 |
| 3.0 | 0.26905807119960407 | 0.9272935666531691 | 0.409375 | 0.013740458015267132 | 0.01690207156308854 | 0.0 | 0.04700000000000004 |

| Lead | Policy | Regret | Capture | Harms | Acting share | Chosen-action histogram |
|---|---|---:|---:|---:|---:|---|
| 2.0 | E | 0.015633149986350337 | 0.9501690839108082 | 1 | 1.0 | [150, 2, 2, 11, 14, 14, 3, 4, 0] |
| 2.0 | C_delta_0 | 0.020080167556427168 | 0.9359941441465799 | 0 | 0.965 | [146, 1, 2, 9, 14, 14, 3, 4, 7] |
| 3.0 | E | 0.0735366101713502 | 0.864037330549317 | 10 | 0.995 | [92, 6, 10, 19, 17, 32, 8, 15, 1] |
| 3.0 | C_delta_0 | 0.18226106309852366 | 0.6630154610329155 | 3 | 0.705 | [73, 4, 6, 11, 11, 24, 2, 10, 59] |

| Lead | Patterns | Coverage | Answers | Pooled error | Case error |
|---|---|---:|---:|---:|---:|
| 2.0 | all_eight | 0.5 | 800 | 0.00125 | 0.0010416666666666075 |
| 2.0 | all_eight | 0.7 | 1120 | 0.008035714285714285 | 0.006932419432419512 |
| 2.0 | seven_zero_mean | 0.5 | 700 | 0.0014285714285714286 | 0.0013513513513513375 |
| 2.0 | seven_zero_mean | 0.7 | 980 | 0.012244897959183673 | 0.010231990231990173 |
| 3.0 | all_eight | 0.5 | 800 | 0.02625 | 0.03516087516087507 |
| 3.0 | all_eight | 0.7 | 1120 | 0.07410714285714286 | 0.08136515912897824 |
| 3.0 | seven_zero_mean | 0.5 | 700 | 0.032857142857142856 | 0.03960799789529079 |
| 3.0 | seven_zero_mean | 0.7 | 980 | 0.08469387755102041 | 0.0983488872936108 |

Uniform-decrease collapse for E: {"2.0": false, "3.0": false}.

All training times, selected steps, guard outcomes, per-draw cost errors, confidence bounds, calibration tests, paired endpoints and histograms remain in the full receipt.
