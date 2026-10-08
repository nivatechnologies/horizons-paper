# Stage 16 run: CNN-noF-seed3

Post hoc on confirmation; licenses no frozen route. Every run is reported, without selection among seeds. Case-level uncertainty and training-run variation are separate.

| Lead | State RMSE/sigma | State ACC | S confidence | Pooled S error | Case S error | Case error lower | Case error upper |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2.0 | 0.12359160484458959 | 0.982010423262222 | 0.73875 | 0.06429780033840948 | 0.06266071428571418 | 0.041000000000000036 | 0.08499999999999996 |
| 3.0 | 0.27286695473880973 | 0.9250518429903226 | 0.456875 | 0.08344733242134061 | 0.1132440476190476 | 0.06899999999999995 | 0.134 |

| Lead | Policy | Regret | Capture | Harms | Acting share | Chosen-action histogram |
|---|---|---:|---:|---:|---:|---|
| 2.0 | E | 0.05359153851836664 | 0.8291761122146777 | 6 | 1.0 | [200, 0, 0, 0, 0, 0, 0, 0, 0] |
| 2.0 | C_delta_0 | 0.05359153851836664 | 0.8291761122146777 | 6 | 1.0 | [200, 0, 0, 0, 0, 0, 0, 0, 0] |
| 3.0 | E | 0.26563275850931173 | 0.5088685913544396 | 30 | 1.0 | [200, 0, 0, 0, 0, 0, 0, 0, 0] |
| 3.0 | C_delta_0 | 0.26563275850931173 | 0.5088685913544396 | 30 | 1.0 | [200, 0, 0, 0, 0, 0, 0, 0, 0] |

| Lead | Patterns | Coverage | Answers | Pooled error | Case error |
|---|---|---:|---:|---:|---:|
| 2.0 | all_eight | 0.5 | 800 | 0.03875 | 0.039686527877482614 |
| 2.0 | all_eight | 0.7 | 1120 | 0.059821428571428574 | 0.05738690476190467 |
| 2.0 | seven_zero_mean | 0.5 | 700 | 0.045714285714285714 | 0.04348702443940533 |
| 2.0 | seven_zero_mean | 0.7 | 980 | 0.07142857142857142 | 0.07041847041847027 |
| 3.0 | all_eight | 0.5 | 800 | 0.08625 | 0.11021428571428571 |
| 3.0 | all_eight | 0.7 | 1120 | 0.12678571428571428 | 0.13429761904761905 |
| 3.0 | seven_zero_mean | 0.5 | 700 | 0.08142857142857143 | 0.08853046594982061 |
| 3.0 | seven_zero_mean | 0.7 | 980 | 0.12857142857142856 | 0.12978595478595478 |

Uniform-decrease collapse for E: {"2.0": true, "3.0": true}.

All training times, selected steps, guard outcomes, per-draw cost errors, confidence bounds, calibration tests, paired endpoints and histograms remain in the full receipt.
