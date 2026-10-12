# Stage23 one-run budget amendment

Todd authorizes extending the current weight 0.1 seed-one run to twelve GPU-hours after partial training. This changes its budget from Freeze G; it is reported explicitly. Freeze G remains preserved, and the selection and confirmatory criteria are unchanged. Other runs retain ten GPU-hours. This authorization does not override the nonfinite guard.

```json
{
  "authorization": "Todd: can we extend the cap on 0.1 to 12 hours?",
  "scope": "Current weight 0.1 seed-one run only; every other weight and any later seed keeps its original cap",
  "model": "CNN-noF-response-0.1-seed1",
  "weight": 0.1,
  "old_cap_seconds": 36000,
  "new_cap_seconds": 43200,
  "additional_budget_seconds": 7200,
  "scientific_criteria_unchanged": true,
  "budget_changed": true,
  "unchanged": [
    "data",
    "initialization and batch seeds",
    "optimizer and schedule",
    "gradient balancing and four-tick truncation",
    "nonfinite guard and abort rule",
    "checkpoint eligibility and validation selection",
    "Q1 and Q2 populations, thresholds and bounds"
  ],
  "partial_training_at_amendment": {
    "step": 3600,
    "charged_gpu_seconds": 9615.947486607009,
    "completed_updates": 3600,
    "skipped_updates": 0
  },
  "original_gpu_index": 2,
  "original_trainer_sha256": "c20d533df67ed2360ad5731fe9a6c3b9a476dae238527fe15a7541c273d4e19e",
  "execution_code_hashes": {
    "acd_stage23_select.py": "81eebf67c0f7e8415e0b1bf69d3dba6ac3ac56c348ee8c48736493a7a5f5199c",
    "acd_stage23_cap12_train.py": "9a41cb55e6401cb656bb080f6f4910379f965794016eba6d0c9f9d27aabc1ce0",
    "acd_stage23_cap12_watch.py": "186a6098186376084a4d49c8c91385603823ad88787ca561d5dc3ec6dc48abbb"
  },
  "cap_only_source_diff_test": "PASS: reversing the two budget substitutions reproduces the original run source exactly",
  "application": "Continue original job to its cap; resume latest scheduled optimizer/RNG checkpoint, all previous and replayed work charged against total 12-hour cap; no guard-aborted run is resumed",
  "selection_gate": "Wait for this one continuation completion; fail loudly on any nonzero return or missing complete.json",
  "utc": 1791788550.6192055
}
```
