# Stage 2 inference coordinator

The coordinator runs on Baccus as a transient user unit, `aspen-afd-stage2-inference.service`. Its lifecycle is independent of agent and terminal sessions. Training runs on Baccus; every actual model evaluation runs on the sulaco GPU under the campaign's shared `gpu.lock`. Each case process exits and releases its GPU context before another worker can take that lock. Qwen services are unchanged.

Read status with `systemctl --user status aspen-afd-stage2-inference --no-pager`; progress is in `runs/stage2_inference_coordinator.log` and `runs/stage2_inference/manifest.json`. The latter becomes complete only after every prescribed one-scale model is evaluated or explicitly recorded as cut. It names `runs/training/final_selection_stage2.json` as the separate frozen validation selection manifest; this evaluator makes no selection decisions.

The root-issued `runs/stage2_authorization.json` must authorize continuation under WO v5.2 §9 and bind the Stage 1 reading's SHA256. The evaluator checks that binding without parsing the Stage 1 gate. Training and selection never receive this coordinator's test records.

Checkpoint transfers resume safely: finalized local checkpoint hashes must match their training completion metadata, and missing or mismatching sulaco copies are repaired before evaluation. Each checkpoint, current source hashes, training metadata and available normalization constants are appended to sulaco's `AFD_ARTIFACTS.md` before its own evaluation. Historical registrations are retained. Root merges ledger entries into the local ledger without overwriting local-only records.

The one-scale state output schema matches campaign.py. CNN-cost outputs primary-only `cost[8]`, `survivors[64]`, `rawprediction[64,8]`. The secondary panel uses action amplitude .32 and preserves observation/member noise .02 sigma. First sixteen primary cases have an additional measured `primary_decision_timing` sidecar, including input transfers, propagation through output tick 36 for state models, paired drops, window cost and argmin; model loading is excluded. Existing CNN-20k outputs are preserved and receive timing metadata only.

Verification: Python compilation and a numerical parity check against the inherited cost formula with lead-dependent paired member drops passed. The transient unit was checked active and its actual sulaco checkpoint registration matched the frozen CNN-20k SHA256. No two-scale data or inference are accessed.

Resume after a failed unit with `python stage2_inference_coordinator.py` from this directory, or launch another transient user unit with the same working directory and append log destinations. Do not run two coordinators concurrently. Authorized model cuts go in `runs/stage2_inference/cuts.json` as `{"models": [...]}`; authorized secondary-panel removal uses `runs/stage2_inference/cut_secondary.json`. This agent has applied no cuts.
