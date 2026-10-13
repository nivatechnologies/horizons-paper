# Stage 23 closeout — implementation verification and exclusion accounting

No training, optimizer run, new panel, panel rescoring or realized-outcome access occurred. Freeze G and every existing scientific receipt, reading and frozen implementation remain unchanged. This document is generated from receipts/acd_stage23_closeout.json.

## Models and fixed batch

Selected checkpoint SHA-256: `5e308dad4185f7d0a74d1e7c3326016d83292351e7de8966c6980a6cb2fa8b3b`. Selected step: 20000. Initialization seed: 1973631741. Rebuilt initial tensor hash: `8fe19941844395a2caf99ea1f39433316ea2d5e65ac7e951ab626ffa8e3bf7a1`. No step-zero hash was recorded, so there is no independent saved hash against which to compare the rebuilt state.

First training batch-order seed: 3521043623. Every recorded start retains its original amplitude under all frozen action patterns, paired with no action. Canonical batch hash: `48b2968a04634295194a5b4fbf498b26588954dffe78619f48c12b2aa0ff017b`. The canonical encoding hashes sorted tensor names, dtypes, shapes and C-order bytes, including the start-index vector.

Start indices: [1448, 2505, 1738, 1510, 574, 3848, 1568, 77, 1715, 865, 1146, 3197, 417, 454, 2309, 2265, 861, 150, 1875, 2545, 1083, 1238, 4038, 1721, 3379, 769, 2980, 4068, 1807, 2747, 3569, 1804, 2381, 175, 3893, 3210, 3846, 1589, 3369, 1078, 1941, 267, 3591, 984, 459, 1226, 2400, 3895, 3687, 3285, 114, 3051, 622, 3857, 433, 604, 154, 456, 1450, 2601, 3293, 352, 2852, 1836, 1679, 1389, 1170, 694, 1483, 3593, 1878, 2345, 2263, 504, 973, 3983, 2226, 527, 277, 1300, 2070, 2528, 1600, 3694, 1989, 2429, 2104, 1438, 3396, 172, 812, 3322, 1060, 1947, 2729, 2281, 4089, 512, 1919, 491, 3683, 1787, 3207, 1425, 535, 2473, 2310, 2295, 3340, 796, 1339, 3321, 247, 1084, 1958, 1165, 2250, 612, 2079, 3474, 2601, 3685, 2484, 735, 527, 114, 1031, 1078].

## Gate summary

| Check | Initial state | Selected checkpoint | Pass rule | Outcome |
|---|---|---|---|---|
| A1 | max absolute 0; max relative 0 | same target | relative difference at most 1e-6; matching subtraction | PASS |
| A2 | action 0.0008682254797; twin 0.0008682254505 | action 0.0005639789391; twin 0.0005514946898 | both norms nonzero; action minus twin in prediction and target | PASS |
| A3 | smallest norm 2.040683853e-07 | smallest norm 0.00127581181 | every trainable tensor has nonzero norm | PASS |
| A4 | worst best-step relative error 8.637997589e-09 | worst best-step relative error 1.745629512e-09 | at most 1e-4 for every fixed direction | PASS |
| A5 | paired norm share 0.0299999956; max direction difference 0 | paired norm share 0.02999999933; max direction difference 0 | frozen balancing formula and global clipping; independently computed directions agree exactly | PASS |

A1 independently reproduces the frozen FP32 branch-state serialization and then compares state differences in float64. Both branches use action minus no action. The raw float64 RK4 trajectory discrepancy is 0. The target discrepancy against unquantized float64 physics is 3.319650856e-07 absolute and 7.309994797e-08 relative in the maximum norm; this storage-quantization reading is separate from the target-equivalence gate.

A2 uses gradients with respect to each rollout prediction, including its downstream dependence within the frozen truncated segments. A3 uses the raw paired-loss parameter gradients. The verification compiles the exact frozen base and paired function ASTs without invoking the training run. Only the detach statement is removed for A4.

A5 compares the clipped gradient delivered to the optimizer, not an AdamW parameter delta. No optimizer was instantiated or run. Global clipping was inactive on this fixed batch in both model states; the recorded coefficients are in the receipt.

## A1b — descriptive window energies

| Model state | Mean predicted action-minus-twin energy | Mean physics energy difference | Effect RMSE | Effect bias |
|---|---:|---:|---:|---:|
| initial | -0.0001475224004 | -0.0158668106 | 0.2847167917 | 0.0157192882 |
| selected | 0.002472089334 | -0.0158668106 | 0.4326192659 | 0.01833889993 |

Window ticks: [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]. Energies are accumulated in physical units in float64. Every start-pattern energy difference is retained in the JSON receipt; no criterion is attached to A1b.

## A3 — every parameter tensor

| Model state | Parameter | Shape | Paired gradient norm |
|---|---|---|---:|
| initial | net.0.weight | [256, 12, 5] | 1.460661497e-05 |
| initial | net.0.bias | [256] | 1.336716537e-06 |
| initial | net.2.weight | [256, 256, 5] | 6.38629208e-05 |
| initial | net.2.bias | [256] | 1.541544862e-06 |
| initial | net.4.weight | [256, 256, 5] | 6.214189489e-05 |
| initial | net.4.bias | [256] | 1.683483333e-06 |
| initial | net.6.weight | [256, 256, 5] | 6.197555922e-05 |
| initial | net.6.bias | [256] | 1.583294647e-06 |
| initial | net.8.weight | [1, 256, 1] | 2.56483072e-05 |
| initial | net.8.bias | [1] | 2.040683853e-07 |
| selected | net.0.weight | [256, 12, 5] | 0.01893350109 |
| selected | net.0.bias | [256] | 0.002206464298 |
| selected | net.2.weight | [256, 256, 5] | 0.01120932586 |
| selected | net.2.bias | [256] | 0.00127581181 |
| selected | net.4.weight | [256, 256, 5] | 0.01366212033 |
| selected | net.4.bias | [256] | 0.00155675807 |
| selected | net.6.weight | [256, 256, 5] | 0.01266773231 |
| selected | net.6.bias | [256] | 0.00160036271 |
| selected | net.8.weight | [1, 256, 1] | 0.03841425478 |
| selected | net.8.bias | [1] | 0.003712348174 |

## A4 — directional finite differences

Fixed direction namespace: acd-stage23-closeout-directions. Seed: 7.501298705e+18. The same unit directions are used for both model states.

| Model state | Direction | Step size | Autodiff | Central difference | Relative error |
|---|---:|---:|---:|---:|---:|
| initial | 1 | 0.001 | 1.987690621e-07 | 1.987690637e-07 | 7.953948024e-09 |
| initial | 1 | 0.0001 | 1.987690621e-07 | 1.987690568e-07 | 2.695537749e-08 |
| initial | 1 | 1e-05 | 1.987690621e-07 | 1.987691262e-07 | 3.221377744e-07 |
| initial | 2 | 0.001 | -1.972961924e-06 | -1.972961919e-06 | 2.850438078e-09 |
| initial | 2 | 0.0001 | -1.972961924e-06 | -1.972961933e-06 | 4.183548539e-09 |
| initial | 2 | 1e-05 | -1.972961924e-06 | -1.972961378e-06 | 2.771759168e-07 |
| initial | 3 | 0.001 | 9.361471326e-07 | 9.36147132e-07 | 5.805774236e-10 |
| initial | 3 | 0.0001 | 9.361471326e-07 | 9.361470626e-07 | 7.470240788e-08 |
| initial | 3 | 1e-05 | 9.361471326e-07 | 9.361476871e-07 | 5.923937151e-07 |
| initial | 4 | 0.001 | 7.813194885e-07 | 7.813194952e-07 | 8.637997589e-09 |
| initial | 4 | 0.0001 | 7.813194885e-07 | 7.813194189e-07 | 8.905293936e-08 |
| initial | 4 | 1e-05 | 7.813194885e-07 | 7.813194536e-07 | 4.464796812e-08 |
| initial | 5 | 0.001 | 1.265374239e-06 | 1.265374239e-06 | 7.012744197e-10 |
| initial | 5 | 0.0001 | 1.265374239e-06 | 1.265374194e-06 | 3.494257623e-08 |
| initial | 5 | 1e-05 | 1.265374239e-06 | 1.265374611e-06 | 2.940774971e-07 |
| selected | 1 | 0.001 | 0.001502538126 | 0.001502527822 | 6.857682975e-06 |
| selected | 1 | 0.0001 | 0.001502538126 | 0.001502538023 | 6.870290443e-08 |
| selected | 1 | 1e-05 | 0.001502538126 | 0.001502538124 | 1.619011118e-09 |
| selected | 2 | 0.001 | -0.009910081291 | -0.009909918553 | 1.642147259e-05 |
| selected | 2 | 0.0001 | -0.009910081291 | -0.009910079662 | 1.643286717e-07 |
| selected | 2 | 1e-05 | -0.009910081291 | -0.009910081274 | 1.745629512e-09 |
| selected | 3 | 0.001 | 0.01129576047 | 0.01129564186 | 1.050051521e-05 |
| selected | 3 | 0.0001 | 0.01129576047 | 0.01129575929 | 1.049473738e-07 |
| selected | 3 | 1e-05 | 0.01129576047 | 0.01129576047 | 6.329345605e-10 |
| selected | 4 | 0.001 | 0.004720956028 | 0.004720977206 | 4.485981763e-06 |
| selected | 4 | 0.0001 | 0.004720956028 | 0.004720956238 | 4.454590728e-08 |
| selected | 4 | 1e-05 | 0.004720956028 | 0.004720956035 | 1.467705291e-09 |
| selected | 5 | 0.001 | -0.002859025294 | -0.002858985882 | 1.378513787e-05 |
| selected | 5 | 0.0001 | -0.002859025294 | -0.002859024899 | 1.384010826e-07 |
| selected | 5 | 1e-05 | -0.002859025294 | -0.002859025291 | 9.714251754e-10 |

Truncated versus untruncated gradient cosine (descriptive): initial 0.98835745, selected -0.09456350089. Their difference is not a failed gate.

## Posterior exclusions

The rule and single-retry contract were frozen before generation. The pushed contract is byte-identical to its committed version. Contract publication: 2026-10-10T23:16:16.100984+00:00; first observation write: 2026-10-10T23:16:19.166001+00:00.

Frozen Stage19 rule inherited by Stage21 and Stage22:

> Retain 128 evenly spaced draws per chain (512 total). Split rank R-hat <=1.01 and bulk ESS >=400 are required for every parameter and the log likelihood, with divergent fraction <=0.01. Test all eight D_k and J_8 at both 2 and 3 LT. A failed functional gate triggers forecasts and diagnostics on all 2000 draws, with an integer confidence threshold of 1900 votes. If gates still fail, including any parameter failure, rerun once with 2000 warm-up iterations and 500 draws per chain. Exclude only after that retry fails. Preserve both attempts and every gate vector. The frozen forward forecast map is used for the diagnostics.

Stage22 inheritance:

> The unchanged Stage21 sampler is called through the count-parameterized copy. The launcher changes panel paths and dispatches the new Stage22 seed namespaces; all priors, NUTS settings, initialization, diagnostic gates, thinning, full-draw functional rescoring and single warm-up retry remain frozen. The new assignment is the same balanced permutation with its assigned count supplied by Freeze F. Spin-up, observation frames, absolute noise, reference LT, nine-option amplitude and frozen windows remain unchanged.

| Case | Attempt | Warm-up | Parameter / log-likelihood max R-hat | Minimum ESS | Functional max R-hat | Minimum ESS | Divergent fraction | Full-draw functional rescore | Outcome |
|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| 401 | 0 | 1000 | 1.011017747 | 879.4731251 | 1.003512778 | 1383.759851 | 0 | True | FAIL |
| 401 | 1 | 2000 | 1.006179474 | 750.2674443 | 1.01071127 | 1498.353641 | 0 | True | FAIL |
| 812 | 0 | 1000 | 1.010583897 | 787.1615666 | 1.004665645 | 448.2712324 | 0 | False | FAIL |
| 812 | 1 | 2000 | 1.012844424 | 762.5980991 | 1.004049116 | 428.0458437 | 0 | False | FAIL |
| 910 | 0 | 1000 | 1.010513147 | 893.57682 | 1.002214878 | 1675.317984 | 0 | True | FAIL |
| 910 | 1 | 2000 | 1.011277601 | 909.9510357 | 1.005677142 | 1381.206731 | 0 | True | FAIL |

The thresholds are copied from the frozen diagnostic implementation: {"rhat_max": 1.01, "ess_min": 400, "divergent_fraction_max": 0.01}.

| Case | Final exclusion reason after retry |
|---:|---|
| 401 | D_2 at 3 LT rhat 1.01071127 against 1.01 |
| 812 | x_first[30] rhat 1.010460781 against 1.01; log_likelihood rhat 1.012844424 against 1.01 |
| 910 | x_first[4] rhat 1.011277601 against 1.01 |

Every attempt’s complete recorded R-hat and ESS vectors, sampler settings, divergence counts and metadata hashes are in the receipt. All three exclusions follow a failed initial attempt and the single failed warm-up retry. No ESS or divergence threshold was violated in these records.

Missing records are reported rather than reconstructed: numeric per-chain NUTS PRNG keys were not saved; the namespace root was recorded. When full-draw rescoring replaced the initial functional diagnostic vector, that initial thinned vector was not retained. Raw invalid-draw counts were not recorded. No posterior draw arrays or realized-outcome arrays were opened to reconstruct these quantities.

## Provenance

- `/mnt/niva-array/work/aspen-determinacy-stage23-20261012/aspen/determinacy/acd_stage23_train.py`: `c20d533df67ed2360ad5731fe9a6c3b9a476dae238527fe15a7541c273d4e19e`
- `/mnt/niva-array/work/aspen-determinacy-stage23-20261012/aspen/determinacy/ACD_STAGE23_FREEZE_G.md`: `ac7e71048c8b4885d2df237459089a3ee4bdc35ca914352227bd423e4e41fb5b`
- `/mnt/niva-array/work/aspen-determinacy-stage19-20261007/aspen/determinacy/acd_stage18_data.py`: `8ac51783c4346c9d5e69944706999b2e88e4fb6837e4d22648373f3f44790438`
- `/mnt/niva-array/work/aspen-forecast-decision-20261005/aspen/forecast_decision/physics.py`: `13ef98834e47bd667f53cce50af3e7d573a1bc4eb9c38987f389a05b1f2fc5d7`
- `/mnt/niva-array/work/aspen-forecast-decision-20261005/aspen/forecast_decision/protocol.py`: `e6d002264a8000ac88d15db41b76cd69bf17c5472de04b29f51b56408841412d`
- `/tmp/acd_stage23_closeout_check.py`: `89c017d292e9674c5f55bce668557d787e2f6c829e2b8a3a9b4a4abcef822bd3`
- `/tmp/acd_stage23_closeout_finalize.py`: `0e86578541f975c03a5a493682976de65a99faa0766aadf7d854d6624bc0d51d`
- `/mnt/niva-array/work/aspen-determinacy-stage21-20261008/aspen/determinacy/acd_posterior.py`: `0b80c61b2e7530dabec4f9c3f0e7fee51f2cfc1ad15745b729d3ddc227c6a60a`

Registry PASS: 833009 prior keys unchanged; 837605 total keys.
