# Stage18 execution continuation

Stage18 D and C remain behind all Stage21 inference. This records the controller and receipt-only derivative renderer, with no change to the frozen data, training, validation selection, conditional replication or failed-run rules. Training data hashes must be committed before C training. Validation reads only generated validation trajectories and the frozen contract settings (sigma, patterns and windows); no confirmation trajectory or outcome participates in checkpoint or weight selection. The conditional replication trigger remains the explicit pooled-and-equal-case comparison in the original freeze. Existing checkpoints, nonfinite guards and cumulative charging provide restart behavior.

```json
{
  "utc": 1791457202.1384351,
  "code_hashes": {
    "acd_stage18_response_controller.py": "daab1f87ea100ce3f852ec3c245e3406aac8230826b98b2f293232f29451e746",
    "acd_stage18_derivative_report.py": "1bb624559fd75bd8bfeea6364ca2de1bef7401de031b8dcb8caab69872dbd5b3",
    "acd_stage18_select.py": "e0e68bd34ec978a862e448a69595b99a10491ae1b2fc3ebf992b362717be9aa4"
  },
  "criteria_unchanged": true,
  "stage21_priority_preserved": true,
  "generation_manifest_must_be_pushed_before_training": true,
  "controller_implements_existing_freeze": true
}
```
