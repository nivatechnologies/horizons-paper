# NUMBERS

## AFD_STEP0

Read-only measurements of retained AAH artifacts and exact code predicates.
No AFD scientific outcomes exist. Source SHA: 1cd0ab701b5e663eb7e0304b1d705ddeabe80617

| Key | Value |
|---|---|
| status | HALT_SCIENTIFIC_MISMATCH |
| LT | 0.5928295944308761 |
| sigma | 4.312600593723798 |
| parameter_count | 999681 |
| checkpoint_step | 20000 |
| training_updates | 20000 |
| training_seconds_recorded | 6943.836976528168 |
| gpu_time_recorded | False |

## AFD_WINDOWS

Derived from measured LT; indices are zero-based output ticks.

| Lead (LT) | Existing code indices | WO indices | Equal |
|---|---|---|---|
| 0 | 0–11 | 0–12 | False |
| 1 | 12–23 | 12–24 | False |
| 1.5 | 18–29 | 18–30 | False |
| 2 | 24–35 | 24–36 | False |
| 2.5 | 30–41 | 30–41 | True |
| 3 | 36–47 | 36–47 | True |
| 4 | 48–59 | 47–59 | False |
| 6 | 72–82 | 71–83 | False |

## AFD_HASHES

| Artifact | SHA256 |
|---|---|
| runs/l96/learned/checkpoint.pt | 3c67fc2cfc3a858613160cc81151c09ef45829f08bda67df00b9e78f35f5fe74 |
| runs/l96/test/climatology.npy | 4513b34ab1ab674bb7c5bf295906e38334ce938ebcb729b6bfa9d97467c7499e |
| runs/l96/test/climatology.json | af91ad04ff2dd904465ecbc4c946ff754e81bc77027e390c69858719672464ac |
| runs/l96/learned/training.json | 3fe8ee0e0be84a75bcf6bcda867b9fa00b47d8672a4c99174c5cf3011836fdc9 |
| results/l96_calibration.json | 908d52224800c0cbeb7d4a2a9dfc7e14063a9f22042bb3b0bda70725cf2ef8f6 |
| common.py | 3e73b9359a11e57ce2429031deeaff6fc08868c42f8bb2579645dd7ddf711011 |
| l96.py | 8b8cdc0df14fd1be0ddc127289746605925582b0d85c9dd7d3d7257b0b2c8def |
| train_l96.py | 1bdde8da8fcfc03d937773e10283392ee68a267c29899ffb2892fa920fdf45e7 |
| evaluate_l96.py | a975e321294430895e9821bef2d787e87fe961e1afbe544db8a318d656e7f366 |
| evaluate_l96_neural.py | 6ad71f3cace2c80dfe9a1c62ce0e9df125fb6f686b8d385ad7a04f6942fb3c6e |
| analyze_l96.py | f01d31b8d8e65cdaeac5ec83f728bed020b93b04c24781b5fb5b974731967301 |
| enrich_l96.py | b10305480ee9d50fd74236f88aa20cf4c579e0ac0add1d8d0561deaeddad8c1b |
| profile_l96.py | 92b9d724d79cfe7f9b03ebcc160c61fd267b1eb57533ab81af03d664516b7f4a |
| climatology_l96.py | 5b9c1dab2eb42176f5220a71723ae20432507a051f352820e284935cda17947d |
| learned_l96_data.py | 79f6320621343dbfd273d93f8161876e43d56e7e51f2f2fe0126c4c19ff1ef9b |
| AAH_FREEZE.md | 0272021e7a32d3c802e6175d9f9f7a2f15255664a9b48a08f9bb0bb9ee3f8c78 |
| AAH_FREEZE_CALIBRATION_L96.md | fd000b9e097fc56d3d2eec406361a780cc7cc5846a8b6b6823a19aca29073df9 |
| WO_v5.1.md | 0da15701b4b0386ac09b8da61d893ed5a64132c21299638fcb14d9c5b5758114 |

## AFD_ACTIONS

Measured RMS values: [1.0, 1.0, 1.0, 0.9999999999999999, 1.0, 1.0, 1.0, 0.9999999999999999]

## AFD_SEEDS

Retained namespace IDs: {"arm": 300000, "calibration": 100000, "climatology": 600000, "jitter": 700000, "lyapunov": 800000, "observation": 900000, "train": 400000, "truth": 200000, "val": 500000}

## AFD_NUMERICAL_PREFLIGHT

Source: runs/preflight_report.json; values recomputed from recorded comparisons and raw sampler draws.
Truth time is a projection from measured single-core throughput; the WO extra cost remains an unmeasured estimate.

| Key | Value |
|---|---|
| one_scale_dt | 0.01 |
| dt_rounds | 1 |
| checked_comparisons | 896 |
| failed_comparisons | 0 |
| argmin_changes | [0, 0, 0, 0, 0, 0, 0, 0] |
| two_scale_batch_members | 2048 |
| single_core_batch_step_seconds | 0.008907205150171649 |
| dt_benchmark | 0.001 |
| truth_projection_steps | 1779 |
| projected_truth_core_hours | 11.884438471616523 |
| wo_total_estimate_core_hours | 96 |
| wo_extra_estimate_core_hours | 15 |
| projection_with_unmeasured_wo_extra | 26.884438471616523 |
| two_scale_state_dt | 0.001 |
| state_check_rounds | [{"dt": 0.001, "sigma_X": 4.39100317948803, "max_abs_X_difference": 4.800699962004273e-07, "threshold": 4.39100317948803e-06, "passed": true}] |
| sampler_ratio | 0.9966878068707742 |
| sampler_correlation | 0.9408992852605442 |
| sampler_spread | 0.40542024308530517 |
| sampler_mean_error | 0.4067675357223167 |
| sampler_states | 16 |
| sampler_draws_per_state | 64 |
| sampler_per_state_ratios | [1.1695964451174292, 1.1617687150620861, 1.163389886037, 0.7318121144028732, 0.9013407512588125, 0.93511707579016, 0.8170905516384024, 1.0292784364640089, 1.0512178706007087, 0.9712287115072136, 1.145011423965617, 0.898479723312774, 1.1229222639832233, 1.1290454925353803, 0.9179814707730805, 1.1341152612540168] |
| sampler_per_state_correlations | [0.930875437030984, 0.9650483270890302, 0.9516222502373259, 0.8950274608596865, 0.9371789447102453, 0.9388893319528453, 0.93174799929249, 0.952968359057935, 0.9577849337034665, 0.948219474312108, 0.9566548626096886, 0.9476674660236659, 0.9498665061013578, 0.9674651339342258, 0.9167546868396387, 0.9203829727749324] |
| sigma_X | 4.362474573065851 |
| sigma_Y | 0.2553174687832342 |

## AFD_PREFLIGHT_ARTIFACT_HASHES

| Artifact | SHA256 |
|---|---|
| runs/numerics/dtcheck.json | e5dc257018dac8a9104a36ecb58fed3d2f50f9d1a39e6590817587f2c6abeaa2 |
| runs/numerics/twoscale_rate.json | 59b10863b2cf75f89c381ff2d7b67d18b64727cd18b823333b52ffb4c4f8dbba |
| runs/twoscale/statecheck.json | 9b847eaa3db3f895b1a42cbbf563ea4dc5e030d8abd0f71802e7fc1af5a4bc85 |
| runs/twoscale/fastlib.npz | 27066e0ed8bc68429519d086e23d29be4ac5833f2d29baa66fd4952654fa7bf6 |
| runs/twoscale/sampler_raw.npz | d1dfa61e99b52921bab626ba139881b79b614df83e13e4f044c35db7f64b4caf |
| runs/twoscale/sampler_check.json | 26cd64d5c81883e04fa0abf68337be36e5e70de85977e9f7630ffbd42dba3f4e |
