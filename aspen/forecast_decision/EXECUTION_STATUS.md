# Execution status — 2026-10-05

WO v5.2 (go-v5.2), Amendment 1 approved by Todd on 2026-10-04, resolves the historical Step 0 window halt. Step 0 and integrity gate are complete. Every scoring and label window uses inherited unrounded endpoints with tolerance 1e-12. CNN-R2 and CNN-cost each use the 10 GPU-hour fallback; historical CPU wall time is not GPU time.

Freeze committed before new data. One-scale timestep check passed without refinement. Two-scale state, sampler and decision-timestep reports exist; see AFD_NUMERICAL_REPORT.md and checked NUMBERS. Two-scale truth remains blocked only on Todd's required sampler-report go, requested and pending.

Stage 1 completed: SUFFICIENT; H1a OTHERWISE. The coordinator read and checked the gate. WO §9 authorizes automatic Stage 2 continuation. No sentence is licensed at Stage 1. Exact values and provenance: AFD_STAGE1_READING.md, NUMBERS.md, runs/stage1_checker.json.

Stage 2 training and isolated validation selection are running on Baccus and sulaco. Training/selection workers have no test-output mounts. Additional one-scale physics and secondary-amplitude truth are complete; descriptive metrics and inference coordination continue. Two-scale preparation is complete; its panel storage is separate from the one-scale secondary panel. No Qwen service was stopped. No cloud compute is used.

Origin branches were pushed; later progress commits continue on paper/aspen-2026-10-forecast-decision. Runtime artifact records are appended before evaluation on sulaco and synchronized to AFD_ARTIFACTS.md locally.

## Historical Step 0 halt (resolved)
Design integrity gate PASS; Step 0 HALT under WO §3 for the cost-window mismatch recorded in AFD_STEP0.md. No AFD scientific data, timestep checks, step-rate measurements, training, sampler report, or Stage-1 reading exist. No Qwen service was changed. No worker was launched.

Read-only source and retained artifacts remain in the horizon checkout at 1cd0ab701b5e663eb7e0304b1d705ddeabe80617. A separate AFD worktree holds these reports; the horizon and evidence branches were not modified.

Requested origin pushes completed:
- paper/aspen-2026-10-horizon: 1cd0ab701b5e663eb7e0304b1d705ddeabe80617
- paper/aspen-2026-10-evidence: a2bfe4567245de106349704121747218835f2790
- paper/aspen-2026-10-forecast-decision: initial preflight commit 9ab4771, followed by this status record.

Preflight checker passes and tampered parameter count is rejected. It verifies retained values, hashes and the exact differing cost-window predicates; it is not a campaign outcome checker.

Resume requires a WO amendment resolving the scientific implementation mismatch, as §3 explicitly requires. Then finish the full recipe/rule freeze before generating any data. Do not treat this halt as H1a KILL, cancel the campaign, or harvest a scientific negative: the scientific test has not run.
