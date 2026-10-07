# Stage 19 Freeze B addendum — training-seed replication

Freeze B's original L3 pooled-error count remains descriptive and unchanged. This addendum adds confirmatory fresh-panel readings using only the four new matched seed pairs. The retained pair, stored index zero, was already tested by L1 and does not enter either new criterion. This stage licenses no frozen route.

## Step 0 — timing inventory

The inventory was completed before this document was written. Confirmation-panel inference already has partial new-seed outputs, disclosed below. No completed confirmation evaluation or new-seed score was found. No new-seed fresh-panel evaluation was found. Todd will judge whether the disclosed confirmation-panel timing preserves the freeze status. Under Step 0's continuation rule, absence of fresh-panel new-seed evaluations permits this addendum to proceed.

| Selected new run | Host | Selected step | Confirmation case files written | Status |
|---|---|---:|---:|---|
| CNN-F-seed1 | 192.168.88.4 | 20000 | 57 | partial inference; not scored or reported |
| CNN-F-seed3 | 192.168.88.12 | 20000 | 68 | partial inference; not scored or reported |

Every other new Stage16 run has no selected checkpoint in this snapshot. Retained index-zero CNN-F and CNN-noF have selected checkpoints and were evaluated on both panels. The inventory records checkpoint hashes and every partial case-file path. Fresh inference directories contain only the retained models. No realized arrays were opened for the inventory.

## L3a — primary

Pair CNN-F seed i with CNN-noF seed i for stored indices i = 1, 2, 3, 4, using every run committed by Stage16 under its frozen recipe. For each pair and each fresh instance, compute the L1 difference exactly: seven zero-mean patterns at 2 LT; CNN-noF's share of confident answers wrong minus CNN-F's share. Each model uses its own confident-answer denominator. An instance-pair contributes only if both models give at least one confident answer. Preserve the invalid-draw rule and the Stage9 F5 inference construction.

Within each instance, average those differences over the new pairs for which they are defined. An instance contributes if at least one pair defines the difference. In ascending instance order, apply acd_stats.difference_interval at alpha = 0.01 to the instance means. This is the two-sided 99% v2.3 betting interval with the instance as unit. L3a is confirmed only if the interval lies wholly above zero. An empty or offset interval licenses no confirmation.

## L3b — required

The per-pair L1 point estimate must be positive in at least three of the four new pairs. L3 is confirmed only if both L3a and L3b hold. Stored index zero enters neither criterion. Never select a subset of seeds.

## Failed and missing runs

If any of the eight new runs fails under Stage16's frozen recipe, including a cap, an abort or no eligible checkpoint, L3a and L3b are not evaluable. A saved checkpoint from such a run does not restore confirmatory evaluability. Report every available pair descriptively without substitution. Pending runs remain pending. A pair with no contributing instances has no positive point estimate.

## Descriptive readings

For every stored index 0–4, report the L1 statistic with its two-sided 99% interval; pooled and case-averaged confident intervention-sign error with the existing v2.3 bounds for both models, retaining all-eight and seven-pattern fields; CNN-noF C(delta=0) harms among actions taken at 3 LT with its exact one-sided 95% Clopper–Pearson lower bound; whether its E and C(delta=0) policies each choose uniform decrease in every instance; and state anomaly correlation at 2 and 3 LT. Preserve the original strict-positive harm definition and report exact zero-effect ties separately. Report Freeze B's original pooled-error count across all five pairs descriptively. Keep seed variation separate from case-level uncertainty.

## Execution gate and code provenance

Do not begin new-seed fresh-panel inference until this addendum is committed and pushed and all eight new Stage16 runs are committed. Resolve each selected checkpoint hash from its committed Stage16 receipt; pair by stored seed index. Use the Stage19 Part2 inference and Stage9 F5 scientific paths unchanged by the hashes below. Separate per-seed output directories must carry their checkpoint provenance, and completed per-case outputs must be written and hashed before scoring reads them. Any additional executable checkpoint/name adapter must be hashed and pushed before execution. Do not alter Stage16 or Stage18 training, checkpoints or queues.

The current learned scorer includes the already committed additive audit diagnostics from commit 4613502: per-case L1 numerator/denominator records and exact zero-effect tie counts. Its L1 computation is unchanged. Its current hash is recorded here; the inference and betting implementation hashes match Freeze B.

Realized outcomes enter only inside Stage19 scoring code from the existing fresh-panel scoring cache. After all eight new runs commit and inference completes, write receipts/acd_stage19_L3.json and the L3 section of ACD_STAGE19_READING.md. Register every reported number, retain every prior registry value, and push fast-forward. This addendum does not launch inference or scoring and does not edit the paper or abstract.

## Inventory and hashes

Inventory:

```json
{
  "selected_new_runs": [
    {
      "host": "192.168.88.4",
      "run": "CNN-F-seed1",
      "selected_path": "/home/todd/work/aspen-stage9-20261006/stage16/training/CNN-F-seed1/selected.pt",
      "selected_step": 20000,
      "selected_sha256": "1c1e3a8c169cb1394fd01eb5237e49a198a82759f5be4f030ccfe57426e61e25",
      "completed_updates": 20000,
      "skipped_updates": 0,
      "charged_gpu_seconds": 4790.267958985991
    },
    {
      "host": "192.168.88.12",
      "run": "CNN-F-seed3",
      "selected_path": "/home/todd/work/aspen-stage9-20261006/stage16/training/CNN-F-seed3/selected.pt",
      "selected_step": 20000,
      "selected_sha256": "df39ee98a5e350f770eb684192fc819af985055eb6bf7c8d1c3b7d428cc87b78",
      "completed_updates": 20000,
      "skipped_updates": 0,
      "charged_gpu_seconds": 4665.470521214011
    }
  ],
  "new_seed_evaluations": [
    {
      "host": "192.168.88.4",
      "panel": "confirmation",
      "run": "CNN-F-seed1",
      "written_case_count": 57,
      "case_files": [
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/000.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/001.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/002.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/003.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/004.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/005.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/006.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/007.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/008.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/009.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/010.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/011.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/012.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/013.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/014.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/015.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/016.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/017.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/018.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/019.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/020.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/021.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/022.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/023.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/024.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/025.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/026.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/027.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/028.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/029.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/030.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/031.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/032.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/033.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/034.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/035.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/036.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/037.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/038.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/039.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/040.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/041.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/042.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/043.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/044.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/045.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/046.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/047.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/048.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/049.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/050.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/051.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/052.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/053.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/054.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/055.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed1/056.npz"
      ],
      "completed_evaluation": false,
      "scored_or_reported": false
    },
    {
      "host": "192.168.88.12",
      "panel": "confirmation",
      "run": "CNN-F-seed3",
      "written_case_count": 68,
      "case_files": [
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/000.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/001.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/002.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/003.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/004.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/005.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/006.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/007.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/008.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/009.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/010.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/011.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/012.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/013.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/014.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/015.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/016.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/017.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/018.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/019.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/020.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/021.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/022.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/023.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/024.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/025.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/026.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/027.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/028.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/029.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/030.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/031.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/032.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/033.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/034.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/035.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/036.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/037.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/038.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/039.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/040.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/041.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/042.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/043.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/044.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/045.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/046.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/047.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/048.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/049.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/050.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/051.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/052.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/053.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/054.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/055.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/056.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/057.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/058.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/059.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/060.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/061.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/062.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/063.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/064.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/065.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/066.npz",
        "/home/todd/work/aspen-stage9-20261006/stage16/inference/CNN-F-seed3/067.npz"
      ],
      "completed_evaluation": false,
      "scored_or_reported": false
    }
  ],
  "new_seed_fresh_evaluations": [],
  "sulaco_scoring_inventory": [
    "/home/todd/work/aspen-determinacy-stage16-20261007/aspen/determinacy/runs/stage16/metrics_CNN-F.json",
    "/home/todd/work/aspen-determinacy-stage16-20261007/aspen/determinacy/runs/stage16/metrics_CNN-noF.json"
  ],
  "scope": "Read-only inventory on both Sparks, Sulaco scoring directories and Baccus fresh-panel outputs; only retained index-zero fresh-panel model directories exist. No realized arrays opened.",
  "recorded_utc": "2026-10-07T21:32:54.582603+00:00",
  "retained_index_zero_checkpoints": {
    "CNN-F": "f883730e8df0798c07effbb1d51b05a646bea6f688b2a4bc74b9edf4ca104e8b",
    "CNN-noF": "4bfef787a80269dada0acd7ca74ef84eb6442a580c706a57333c55dc647b1f67"
  }
}
```

Code hashes:

```json
{
  "acd_stage19_freeze_b_l3.py": "99a1f92424f08fce7eadfcf0478215254d1ff025b509d035200036c0504a7f92",
  "acd_stage19_l3_statistic.py": "72da9641cfa8341a50b85514e42f0f15be1e5886e79348c9870c345cee5ce33b",
  "acd_stage19_inference.py": "591f6ce4989b19be4bbda36e6ffa39ecf34940bc513a1770e361b00ee1a7ef6d",
  "acd_stage9_cnn.py": "3ca018b1dc35c5cb9734787e852240e7517d88007515692d27fd882f3c13d434",
  "acd_stage9_train.py": "9c36418c45ab0727d2c4294b96bed1102b85d65d269636f6c9b38e3573605269",
  "acd_stage19_learned.py": "9319e768f5d211472d6c52fe0b7c4cef975d878be242b14807a43178e7e85930",
  "acd_stage6_analysis.py": "c9fa8c1f9e211f8e7ea47ec63947bff3693258c738c377ce7874b425bba58cd8",
  "acd_stage13_analysis.py": "ffe50e4894aa97eb6de690abc996c1a8589ec8be926af0100f077b2220be289b",
  "acd_stage9_receipts.py": "966a21bc72ef4b3c8ede354a1246fb5d01c4b3df440ef19902ec032a688b456c",
  "acd_stats.py": "1c97d51262a7546b70320c1207de554eff6f9b6a58b00428a2640f5ead6f685a",
  "acd_protocol.py": "160eabe8ccee07d0de17576a441b6fef1a93e1d5dbb68f2df9eb118a1eaad000",
  "acd_stage19_part2_gate.py": "518e5890d5ac88f210a47a304ae9fd7cb47986ff444b3d078dc13ffc76b1a001"
}
```
