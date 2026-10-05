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

CNN2-roll feasibility uses an isolated 100-update full36-step pilot on Baccus GPU1, microbatch64/effective128, initialized from completed CNN2-20k. The pilot keeps the frozen10000-update learning-rate schedule and64-batch normalization. It writes no checkpoint or candidate. Source/data preregistration is runs/training_pilot/preregistration.json; exact initializer/capacity registration precedes execution. Pilot phase time is measured and charged against Stage2b reserve, with a15-minute conservative maximum and inclusion in the20h aggregate guard. Mandatory base and available R2 training take priority. Feasibility compares measured setup/normalization plus10000 times measured update median plus required measured selector reserve with7200seconds; this is labeled a projection, not measured full-run duration. A failed feasibility condition cuts only the optional CNN2-roll allocation and records measured evidence in cuts.json. A feasible exact10000-update arm runs after mandatory R2, within its unchanged2h cap.
