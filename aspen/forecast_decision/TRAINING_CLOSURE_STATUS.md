# Training closure under WO Section 19

Todd's named stop was executed only against CNN-cost, PID285573, verified by its exact command and process start ticks7267401. SIGSTOP then SIGKILL stopped the worker; its process is absent. Qwen and every other training worker were untouched. Before/after retention evidence is `runs/training/CNN-cost/closed_stop.json`; every cost checkpoint hash remains unchanged. Exact final GPU time and exact final update count are unavailable and are not invented.

CNN-roll PID283638, CNN-R2 PID286883 and already-running CNN2-20k PID359369 remain permitted to finish within their existing frozen caps. CNN-resp had already completed. The distinction is intentional: closure blocks expansion but preserves these existing jobs.

The durable marker is `runs/training/closure_control.json`. New training launches and the Stage2b queue/pilot are prohibited, including direct launcher calls. The training scheduler and final-selection services are stopped and disabled. The budget guard remains active and records the named CNN-cost closure stop without globally stopping the other workers. Unit evidence is `runs/training/closure/runtime_units.json`.

Only the legacy CNN-R2 generation may continue its frozen scheduled-checkpoint validation to finish that job and account for its cap. The allowance is bound to PID286883/start_ticks7301216. New receipts and choices are labeled CLOSED_REFERENCE_ONLY, not authoritative for any future WO. No L*/FINAL consumer selection, test evaluation, new model or two-scale truth is authorized by this allowance. Cost selectors are blocked.

`runs/training/closure/checkpoint_inventory.json` records source hashes and retained snapshot copies under `runs/training/closure/saved_checkpoints`. No checkpoint was deleted. The persistent `aspen-afd-retention-watch.service` also retains new byte-consistent versions under `runs/training/closure/checkpoint_versions`, with hashes and original paths in `ongoing_retention.json`. This preserves future saved checkpoints from the permitted running jobs without selecting or interpreting them. Its log is `retention_watch.log` in that directory.

Stage1 test/artifact retention remains with the coordinator; this worker did not read test outputs or scientific outcomes during closure. Source guards, named process identity, direct-launch rejection, running-worker preservation and retained hashes were independently audited as PASS.
