# GPU reservation guard

The Baccus user service `aspen-gpu-reservation-guard.service` runs
`gpu_reservation_guard.py --enforce`, with restart on failure. It reads only
source-independent training metadata, progress, and validation receipts.
It has not opened any test output or Stage-1 scientific reading.

Each reported reservation is labelled **GPU RESERVATION WALL UPPER BOUND**.
The process start comes from `/proc/PID/stat` field 22 divided by
`os.sysconf("SC_CLK_TCK")`, compared with local `CLOCK_BOOTTIME`. This includes
CPU preparation and CUDA setup/waits. It is a conservative resource reservation,
not actual GPU time; exact startup CUDA residency is unavailable. Actual selector
charges retain their measured receipt values separately.

The guard counts each validation checkpoint once. An R2 step-2000 receipt may
contain the initialization validation charge again: its
`checkpoint_validation_gpu_seconds` is counted while the separate raw step-zero
receipt supplies the initialization charge. No CPU duration is relabelled as a
GPU measurement. An active selector is conservatively reserved from the
selection manager's Baccus-local launch boottime until its receipt is committed.

Completed selector reservations are separate from actual GPU timers. New
receipts supply `selector_reservation_wall_seconds` measured over the
supervisor SSH command, including setup and lock wait. Legacy receipts use
local acknowledgement mtime minus checkpoint-JSON mtime, including queue wait.
That legacy measurement depends on local filesystem clock/timestamp fidelity
and can overbound substantially; it is never labelled actual GPU time. Negative,
unavailable, nonfinite, or below-actual bounds produce an alert and stop that
model rather than assert budget assurance. Each checkpoint reservation is
counted once, including the separately recorded R2 initialization checkpoint.

The selection-manager handshake is `runs/training/MODEL/selection_in_progress.json`:
`active`, integer `step`, `clock_host: "baccus"`, and
`launch_boottime_seconds` sampled immediately before remote launch. Per-model
guard statuses expose `selection_allowed` and `stop_requested` for that manager.

At 60 seconds remaining under an individual conservative reservation ceiling,
the guard requests selection stop and freezes/kills only the identified training
worker tree. Aggregate ceilings include each model once, with CNN2 base counted
once globally and additionally included in CNN2-R2's individual ceiling. The
PID start identity is checked before every signal. No unrelated service is
signalled.

CNN2-R2 includes the base model's process reservation and every completed or
active base selector reservation, including its final L* validation. Those
components are explicit in `included_base_reservation_components`; the aggregate
subtracts this full repeated base amount so the base is counted once. Missing
base assurance stays unavailable and stops R2; actual GPU timers do not replace
an unavailable reservation bound.

New selector admission requires remaining individual reservation above twice
the maximum observed same-kind (state or cost) selector reservation plus the
60-second stop margin. This applies after exact-count training completes too.
An already active selector keeps running while above the stop margin; completed
training does not disable the active-selector cap stop. This resource guard
does not alter scientific checkpoint eligibility or selection ranking.

The frozen workers have no graceful interruption/save handler. A resource
cutoff therefore does not produce a fabricated completion receipt. Exact-count
requirements remain unmet if a worker cannot finish: progress-based feasibility
warnings and worker-death alerts preserve this distinction. Variable-count
models retain only existing scheduled checkpoints. Final synchronized GPU time
is unavailable after a forced stop and must not be invented.

`summary.json`, model status JSON files, and `state.json` retain the measurements
and control state. Guard state survives service restarts. Independent smoke
checks verified `/proc` field parsing and the initialization-charge deduplication.
Exclusive-created `snapshots/` JSON files retain immutable startup, five-minute,
and alert/stop-event evidence: common boottime, measured start ticks and clock
Hz, actual selector timers, reservation components, and gate control status.
NUMBERS should cite these snapshots, not mutable status files.

The root alone owns `runs/campaign_control.json` (`campaign`, `execution`,
`reason`, `recorded_at`). An execution value of `stop` stops the campaign's
training workers without reading test outcomes. The guard reads only
`authorized` and `stage1_reading_sha256` from the root-issued
`runs/stage2_authorization.json`, and records the generation gate state.

The conservative operational two-scale evidence cutoff is
2026-10-08T00:00:00Z, chosen by the coordinator from the Oct 7 reading target
and Oct 8 factual-audit date. The WO specifies no explicit cutoff time.
Unfinished two-scale workers stop at that time and the campaign must report
Stage 2b as not run. The guard does not change frozen scientific methods/caps.
