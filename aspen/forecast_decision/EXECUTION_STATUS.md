# Execution status — 2026-10-05

## Amendment 1 resolution

WO v5.2 (go-v5.2), §4 and §18, re-read via MCP. Todd's 2026-10-04 approval resolves the Step 0 halt: all new scoring/label windows use inherited unrounded endpoints and tolerance 1e-12. Historical halt text below remains for provenance. Continuing with recipe freeze before any data. CNN-R2 and CNN-cost have individual 10 GPU-hour fallback ceilings; retained CPU wall time is not GPU time.

Design integrity gate PASS; Step 0 HALT under WO §3 for the cost-window mismatch recorded in AFD_STEP0.md. No AFD scientific data, timestep checks, step-rate measurements, training, sampler report, or Stage-1 reading exist. No Qwen service was changed. No worker was launched.

Read-only source and retained artifacts remain in the horizon checkout at 1cd0ab701b5e663eb7e0304b1d705ddeabe80617. A separate AFD worktree holds these reports; the horizon and evidence branches were not modified.

Requested origin pushes completed:
- paper/aspen-2026-10-horizon: 1cd0ab701b5e663eb7e0304b1d705ddeabe80617
- paper/aspen-2026-10-evidence: a2bfe4567245de106349704121747218835f2790
- paper/aspen-2026-10-forecast-decision: initial preflight commit 9ab4771, followed by this status record.

Preflight checker passes and tampered parameter count is rejected. It verifies retained values, hashes and the exact differing cost-window predicates; it is not a campaign outcome checker.

Resume requires a WO amendment resolving the scientific implementation mismatch, as §3 explicitly requires. Then finish the full recipe/rule freeze before generating any data. Do not treat this halt as H1a KILL, cancel the campaign, or harvest a scientific negative: the scientific test has not run.
