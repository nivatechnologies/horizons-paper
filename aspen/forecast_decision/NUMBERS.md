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

## AFD_STAGE1_READING

Measured case/panel reading; no licensed sentence. Source: runs/stage1_reading.json, checked from runs/stage1_cases.json.

```json
{
  "stage": "1",
  "S": [
    "CNN-20k"
  ],
  "read_at": "2026-10-05T01:04:12.967722+00:00",
  "actor": "coordinator",
  "licensed_sentences": [],
  "leads": [
    {
      "T": 1.0,
      "eligible": 200,
      "total": 200,
      "eligible_fraction": 1.0,
      "sufficiency": false,
      "sufficiency_status": "TRIVIAL",
      "null_gap": 0.0,
      "myopic_P": 1.0,
      "fixed_P": 1.0,
      "fixed_action": 0,
      "random_P": 0.125,
      "arms": {
        "N-last": {
          "P": 1.0,
          "wACC": 0.9849100042814521,
          "wRMSE": 0.1240178037518267,
          "failed_cases": 0,
          "dropped_members": 0,
          "attempted_members": 12800,
          "reliable": true,
          "excluded_wRMSE_cases": 0,
          "all_case_wACC": 0.9849100042814521
        },
        "N-oracle": {
          "P": 1.0,
          "wACC": 0.9857956917433289,
          "wRMSE": 0.11844249662820784,
          "failed_cases": 0,
          "dropped_members": 0,
          "attempted_members": 12800,
          "reliable": true,
          "excluded_wRMSE_cases": 0,
          "all_case_wACC": 0.9857956917433289
        },
        "CNN-20k": {
          "P": 0.995,
          "wACC": 0.9967817255836324,
          "wRMSE": 0.05506697337683795,
          "failed_cases": 0,
          "dropped_members": 0,
          "attempted_members": 12800,
          "reliable": true,
          "excluded_wRMSE_cases": 0,
          "all_case_wACC": 0.9967817255836324
        }
      },
      "comparable": true,
      "gap": 0.0050000000000000044,
      "lower95": 0.0,
      "upper95": 0.015,
      "H1a": "otherwise",
      "eligibility_bootstrap_agreement": 200,
      "eligible_full_argmin_disagreements": 0
    },
    {
      "T": 1.5,
      "eligible": 196,
      "total": 200,
      "eligible_fraction": 0.98,
      "sufficiency": false,
      "sufficiency_status": "TRIVIAL",
      "null_gap": 0.04591836734693877,
      "myopic_P": 0.9438775510204082,
      "fixed_P": 0.9438775510204082,
      "fixed_action": 0,
      "random_P": 0.125,
      "arms": {
        "N-last": {
          "P": 0.9897959183673469,
          "wACC": 0.9624484402315499,
          "wRMSE": 0.19702586021288537,
          "failed_cases": 0,
          "dropped_members": 0,
          "attempted_members": 12800,
          "reliable": true,
          "excluded_wRMSE_cases": 0,
          "all_case_wACC": 0.9618713839733347
        },
        "N-oracle": {
          "P": 0.9897959183673469,
          "wACC": 0.9645554226577753,
          "wRMSE": 0.18947765381314682,
          "failed_cases": 0,
          "dropped_members": 0,
          "attempted_members": 12800,
          "reliable": true,
          "excluded_wRMSE_cases": 0,
          "all_case_wACC": 0.9640029904754097
        },
        "CNN-20k": {
          "P": 0.9081632653061225,
          "wACC": 0.9900113760254783,
          "wRMSE": 0.09474127066401852,
          "failed_cases": 0,
          "dropped_members": 0,
          "attempted_members": 12800,
          "reliable": true,
          "excluded_wRMSE_cases": 0,
          "all_case_wACC": 0.9895537116190168
        }
      },
      "comparable": true,
      "gap": 0.08163265306122447,
      "lower95": 0.046153846153846156,
      "upper95": 0.11734693877551021,
      "H1a": "otherwise",
      "eligibility_bootstrap_agreement": 200,
      "eligible_full_argmin_disagreements": 0
    },
    {
      "T": 2.0,
      "eligible": 188,
      "total": 200,
      "eligible_fraction": 0.94,
      "sufficiency": true,
      "sufficiency_status": "SUFFICIENT",
      "null_gap": 0.17021276595744683,
      "myopic_P": 0.7659574468085106,
      "fixed_P": 0.7659574468085106,
      "fixed_action": 0,
      "random_P": 0.125,
      "arms": {
        "N-last": {
          "P": 0.9361702127659575,
          "wACC": 0.9241666899444396,
          "wRMSE": 0.28816478316330907,
          "failed_cases": 0,
          "dropped_members": 0,
          "attempted_members": 12800,
          "reliable": true,
          "excluded_wRMSE_cases": 0,
          "all_case_wACC": 0.924011281767082
        },
        "N-oracle": {
          "P": 0.973404255319149,
          "wACC": 0.927783691490088,
          "wRMSE": 0.2791728916765553,
          "failed_cases": 0,
          "dropped_members": 0,
          "attempted_members": 12800,
          "reliable": true,
          "excluded_wRMSE_cases": 0,
          "all_case_wACC": 0.9276252376306217
        },
        "CNN-20k": {
          "P": 0.8138297872340425,
          "wACC": 0.9738843551311618,
          "wRMSE": 0.15525566849775835,
          "failed_cases": 0,
          "dropped_members": 0,
          "attempted_members": 12800,
          "reliable": true,
          "excluded_wRMSE_cases": 0,
          "all_case_wACC": 0.9734910601170312
        }
      },
      "comparable": true,
      "gap": 0.12234042553191493,
      "lower95": 0.07405458089668615,
      "upper95": 0.1736842105263158,
      "H1a": "otherwise",
      "eligibility_bootstrap_agreement": 200,
      "eligible_full_argmin_disagreements": 0
    },
    {
      "T": 2.5,
      "eligible": 177,
      "total": 200,
      "eligible_fraction": 0.885,
      "sufficiency": true,
      "sufficiency_status": "SUFFICIENT",
      "null_gap": 0.27118644067796605,
      "myopic_P": 0.6836158192090396,
      "fixed_P": 0.6836158192090396,
      "fixed_action": 0,
      "random_P": 0.125,
      "arms": {
        "N-last": {
          "P": 0.9548022598870056,
          "wACC": 0.8760458713809702,
          "wRMSE": 0.3742862542273116,
          "failed_cases": 0,
          "dropped_members": 0,
          "attempted_members": 12800,
          "reliable": true,
          "excluded_wRMSE_cases": 0,
          "all_case_wACC": 0.8701547577314895
        },
        "N-oracle": {
          "P": 0.96045197740113,
          "wACC": 0.8824456481467892,
          "wRMSE": 0.36289334307717386,
          "failed_cases": 0,
          "dropped_members": 0,
          "attempted_members": 12800,
          "reliable": true,
          "excluded_wRMSE_cases": 0,
          "all_case_wACC": 0.8757169559801049
        },
        "CNN-20k": {
          "P": 0.6836158192090396,
          "wACC": 0.9490887272880308,
          "wRMSE": 0.2229035430923001,
          "failed_cases": 0,
          "dropped_members": 0,
          "attempted_members": 12800,
          "reliable": true,
          "excluded_wRMSE_cases": 0,
          "all_case_wACC": 0.9450398601625438
        }
      },
      "comparable": true,
      "gap": 0.27118644067796605,
      "lower95": 0.21426507018992566,
      "upper95": 0.32954545454545453,
      "H1a": "PASS",
      "eligibility_bootstrap_agreement": 200,
      "eligible_full_argmin_disagreements": 0
    },
    {
      "T": 3.0,
      "eligible": 168,
      "total": 200,
      "eligible_fraction": 0.84,
      "sufficiency": true,
      "sufficiency_status": "SUFFICIENT",
      "null_gap": 0.33333333333333337,
      "myopic_P": 0.6011904761904762,
      "fixed_P": 0.6011904761904762,
      "fixed_action": 0,
      "random_P": 0.125,
      "arms": {
        "N-last": {
          "P": 0.9345238095238095,
          "wACC": 0.8020348621937876,
          "wRMSE": 0.4708367285659139,
          "failed_cases": 0,
          "dropped_members": 0,
          "attempted_members": 12800,
          "reliable": true,
          "excluded_wRMSE_cases": 0,
          "all_case_wACC": 0.7983959969702099
        },
        "N-oracle": {
          "P": 0.9642857142857143,
          "wACC": 0.8102663771879757,
          "wRMSE": 0.4595201456940228,
          "failed_cases": 0,
          "dropped_members": 0,
          "attempted_members": 12800,
          "reliable": true,
          "excluded_wRMSE_cases": 0,
          "all_case_wACC": 0.8059439085881199
        },
        "CNN-20k": {
          "P": 0.5119047619047619,
          "wACC": 0.9042640060652423,
          "wRMSE": 0.3150369860001232,
          "failed_cases": 0,
          "dropped_members": 0,
          "attempted_members": 12800,
          "reliable": true,
          "excluded_wRMSE_cases": 0,
          "all_case_wACC": 0.9003805370158311
        }
      },
      "comparable": true,
      "gap": 0.42261904761904767,
      "lower95": 0.35119047619047616,
      "upper95": 0.4911242603550296,
      "H1a": "PASS",
      "eligibility_bootstrap_agreement": 199,
      "eligible_full_argmin_disagreements": 0
    },
    {
      "T": 4.0,
      "eligible": 129,
      "total": 200,
      "eligible_fraction": 0.645,
      "sufficiency": false,
      "sufficiency_status": "INSUFFICIENT",
      "null_gap": 0.40310077519379844,
      "myopic_P": 0.4573643410852713,
      "fixed_P": 0.4573643410852713,
      "fixed_action": 0,
      "random_P": 0.125,
      "arms": {
        "N-last": {
          "P": 0.8604651162790697,
          "wACC": 0.6413617518082525,
          "wRMSE": 0.6269389492832356,
          "failed_cases": 0,
          "dropped_members": 0,
          "attempted_members": 12800,
          "reliable": true,
          "excluded_wRMSE_cases": 0,
          "all_case_wACC": 0.6303572461844908
        },
        "N-oracle": {
          "P": 0.8837209302325582,
          "wACC": 0.6492898750515743,
          "wRMSE": 0.6204911286406833,
          "failed_cases": 0,
          "dropped_members": 0,
          "attempted_members": 12800,
          "reliable": true,
          "excluded_wRMSE_cases": 0,
          "all_case_wACC": 0.6393205338779815
        },
        "CNN-20k": {
          "P": 0.4418604651162791,
          "wACC": 0.7820225355199821,
          "wRMSE": 0.49286184821503404,
          "failed_cases": 0,
          "dropped_members": 0,
          "attempted_members": 12800,
          "reliable": true,
          "excluded_wRMSE_cases": 0,
          "all_case_wACC": 0.7672228601032045
        }
      },
      "comparable": true,
      "gap": 0.41860465116279066,
      "lower95": 0.3333333333333333,
      "upper95": 0.5038759689922481,
      "H1a": "otherwise",
      "eligibility_bootstrap_agreement": 200,
      "eligible_full_argmin_disagreements": 0
    },
    {
      "T": 6.0,
      "eligible": 130,
      "total": 200,
      "eligible_fraction": 0.65,
      "sufficiency": false,
      "sufficiency_status": "INSUFFICIENT",
      "null_gap": 0.0,
      "myopic_P": 0.8846153846153846,
      "fixed_P": 0.8846153846153846,
      "fixed_action": 0,
      "random_P": 0.125,
      "arms": {
        "N-last": {
          "P": 0.8846153846153846,
          "wACC": 0.3563904535747531,
          "wRMSE": 0.7738437843547827,
          "failed_cases": 0,
          "dropped_members": 0,
          "attempted_members": 12800,
          "reliable": true,
          "excluded_wRMSE_cases": 0,
          "all_case_wACC": 0.35660905085212735
        },
        "N-oracle": {
          "P": 0.8615384615384616,
          "wACC": 0.3651039043461701,
          "wRMSE": 0.7704953582612297,
          "failed_cases": 0,
          "dropped_members": 0,
          "attempted_members": 12800,
          "reliable": true,
          "excluded_wRMSE_cases": 0,
          "all_case_wACC": 0.36458937104364236
        },
        "CNN-20k": {
          "P": 0.5,
          "wACC": 0.4668857778450962,
          "wRMSE": 0.7263324530473968,
          "failed_cases": 0,
          "dropped_members": 0,
          "attempted_members": 12800,
          "reliable": true,
          "excluded_wRMSE_cases": 0,
          "all_case_wACC": 0.4667184150340533
        }
      },
      "comparable": true,
      "gap": 0.3846153846153846,
      "lower95": 0.3014705882352941,
      "upper95": 0.4645943966306537,
      "H1a": "otherwise",
      "eligibility_bootstrap_agreement": 198,
      "eligible_full_argmin_disagreements": 0
    }
  ],
  "primary": {
    "T": 2.0,
    "eligible": 188,
    "total": 200,
    "eligible_fraction": 0.94,
    "sufficiency": true,
    "sufficiency_status": "SUFFICIENT",
    "null_gap": 0.17021276595744683,
    "myopic_P": 0.7659574468085106,
    "fixed_P": 0.7659574468085106,
    "fixed_action": 0,
    "random_P": 0.125,
    "arms": {
      "N-last": {
        "P": 0.9361702127659575,
        "wACC": 0.9241666899444396,
        "wRMSE": 0.28816478316330907,
        "failed_cases": 0,
        "dropped_members": 0,
        "attempted_members": 12800,
        "reliable": true,
        "excluded_wRMSE_cases": 0,
        "all_case_wACC": 0.924011281767082
      },
      "N-oracle": {
        "P": 0.973404255319149,
        "wACC": 0.927783691490088,
        "wRMSE": 0.2791728916765553,
        "failed_cases": 0,
        "dropped_members": 0,
        "attempted_members": 12800,
        "reliable": true,
        "excluded_wRMSE_cases": 0,
        "all_case_wACC": 0.9276252376306217
      },
      "CNN-20k": {
        "P": 0.8138297872340425,
        "wACC": 0.9738843551311618,
        "wRMSE": 0.15525566849775835,
        "failed_cases": 0,
        "dropped_members": 0,
        "attempted_members": 12800,
        "reliable": true,
        "excluded_wRMSE_cases": 0,
        "all_case_wACC": 0.9734910601170312
      }
    },
    "comparable": true,
    "gap": 0.12234042553191493,
    "lower95": 0.07405458089668615,
    "upper95": 0.1736842105263158,
    "H1a": "otherwise",
    "eligibility_bootstrap_agreement": 200,
    "eligible_full_argmin_disagreements": 0
  }
}
```

## AFD_STAGE1_CHECKER

{"NaN_rejected": true, "case_count": 200, "leads": 7, "raw_truth_checked": false, "status": "PASS", "tamper_rejected": true}

| Artifact | SHA256 |
|---|---|
| runs/stage1_reading.json | 0434ee279b4733105ddcdf9f2e20db8909a909ff04f30b40d8ae770db68c4eec |
| runs/stage1_cases.json | 472a75670a18983124cd66ed92f5d419aeea8c95d5a13193d3cc58e0c55b95fb |
| runs/stage1_checker_registered.json | 4bf154bbe37f9085d17621b6dd102c4b95b8560a83ca08114066a06aacfcce63 |

## AFD_TWOSCALE_DECISION_DTCHECK

Source: `runs/twoscale/decision_dtcheck.json`; independently replayed from sixteen raw dt-check artifacts.
Checker: `check_twoscale_prep.py`; evidence: `runs/twoscale/dtcheck_checked.json`.

Status: PASS; tamper rejection: True.

| dt | comparisons | failed | elapsed CPU wall seconds | argmin changes (1, 1.5, 2 LT_ref) | S_J |
|---|---|---|---|---|---|
| 0.001 | 336 | 0 | 23.93954798899358 | [0, 0, 0] | [0.32858822303093493, 0.37932914875779034, 0.45728253700369015] |

Chosen dt: 0.001. N2 solver dt remains 0.01 under WO §4 propagation.

Every comparison requires a strictly smaller absolute mean gap change than max(0.05*S_J, two paired standard errors).
State check, sampler approval and decision-cost check remain separate gates. No two-scale panel was launched by this checker.
