# Durable training and validation controllers

All controllers are Baccus user systemd services. They run independently of agent/tool sessions; Todd's user manager has Linger=yes. Their unit files are under `/home/todd/.config/systemd/user/`.

| Unit | Source | Persistent log |
|---|---|---|
| aspen-afd-training-scheduler.service | training_scheduler.py | runs/training/controller_logs/aspen-afd-training-scheduler.log |
| aspen-afd-validation-selector.service | selection_manager.py | runs/training/controller_logs/aspen-afd-validation-selector.log |
| aspen-afd-validation-finalization.service | validation_finalization_controller.py | runs/training/controller_logs/aspen-afd-validation-finalization.log |
| aspen-gpu-reservation-guard.service | gpu_reservation_guard.py | GUARD_STATUS/guard.log |

Inspect with `systemctl --user status UNIT`; restart a failed controller only after checking its persistent log. The scheduler recovers detached worker PID files on restart and starts future training with nohup on Baccus. The original four workers remain alive under their existing persistent SSH exec processes; this does not make them restartable after process loss. No optimizer state recovery is claimed for them.

Checkpoint regret selection now occurs inside the physically isolated sulaco worker. The supervisor copies its checkpoint choice; it does not compute an argmin. It binds one validation input artifact, selected source and the current model checkpoint directory. It masks /mnt and /home. Every state checkpoint also saves primary-window ensemble means for later CPU tie metrics, avoiding another GPU inference pass.

L* selection runs in a separate sulaco CPU bubblewrap worker with curated validation-only inputs, predictions and initializer equality proofs. It uses the frozen all-case mean normalized regret, eligible-case wACC/wRMSE tie metrics and frozen arm order. Campaign consumer manifests are runs/training/final_selection_stage2.json and final_selection_stage2b.json. They contain FINAL status, selected_L, S, finalized checkpoint hashes, completion timestamp, cuts/not_run and a public compute manifest path. Per-case validation choices are not included.

Public compute receipts distinguish the synchronized recorded training/selection phase from the conservative GPU reservation wall upper bound. Legacy CUDA startup timing remains unavailable. No CPU wall time is converted to GPU hours. GUARD_STATUS provides measured process-start/CLOCK_BOOTTIME reservation bounds, cap controls and immutable evidence snapshots. Manager admissions honor selection_allowed and active selectors honor stop_requested; in-flight command reservations remain active until the corresponding acknowledgement is published.

The guard reads only root-issued stage2_authorization.json and campaign_control.json, not scientific gate outputs. Controllers stop launching on root execution=stop. Two-scale checkpoint-selected training waits for authorized fixed validation inputs. CNN2-roll remains deferred pending measured feasibility and an explicit cut decision. No cuts have been applied by this agent.

A real 100-case validation-only baseline smoke check passed the isolated CPU selection path. It is under runs/validation_finalize_smoke, not a campaign selection manifest. Syntax checks passed for the controllers and workers.

Externally stopped variable-update recipes write a separate resource_stop.json after the guard observes process death. This receipt records completed_updates_lower_bound, completed_updates_exact=null, the last synchronized phase subtotal as a lower bound, and an immutable copy of the guard evidence. It never fabricates training_complete.json. The scheduler may release the slot; final scientific selection still requires validation of every produced scheduled checkpoint. A missing acknowledgement creates finalization_blocker.json and prevents FINAL selection. Exact-count recipes cannot use this terminal path. Public compute manifests label externally stopped phase subtotals as lower bounds and retain unknown exact total GPU time.
