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
