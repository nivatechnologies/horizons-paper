# Aspen horizon: findings harvest, 2026-10-04

Execution is complete with the prescribed Kolmogorov calibration stop. The original two-system headline is unsupported: L96 has Tf=10 LT and sustained Td=12 LT, with a paired/unpaired member ratio of 1 at Tf; Kolmogorov reaches at most 13/20 determinable calibration cases against 16/20 required. The frozen two-system empirical PASS/KILL is unavailable because Kolmogorov stopped before testing. Todd retains the publication/pivot decision; this is an internal harvest.

| Finding | Class | Data | Consequence |
|---|---|---|---|
| L96 decisions sustain through 12 LT after forecast ACC crosses below 0.2 at 10 LT; ratio 1.2 falls below the target 3; paired and unpaired M95 both 128 at Tf | Boundary | results/l96_solver_statistics.json; checked AAHREAD/AAHLARMS/AAHLCONTROL | Original beyond-horizon and member-saving headline is not supported at this operating point |
| At 4 LT, Niva top-1 0.920 vs CNN 0.416, on 125/200 eligible cases; forecast ACC 0.7115 vs 0.8387 | Boundary | Same JSON, AAH* sections | Higher forecast ACC does not ensure better action ranking on this panel; this shorter-lead result does not satisfy the frozen beyond-horizon criterion |
| Myopic top-1 1 at 10,12,16,20 LT; uniform negative-forcing action 0 is truth-best in every eligible case there, and myopic chooses it for all 200 cases | Limitation | results/l96_posthoc_action_frequency.json and solver_statistics; AAHLPOSTHOC/AAHLCONTROL | Post-hoc diagnosis of the selected action panel; no universal claim that long-lead planning is impossible |
| Kolmogorov calibration eligible counts 6,6,13,13 at delta 0.01,0.02,0.05,0.1; all below 16/20 | Boundary | results/kolmo_calibration.json; AAHKCAL | This amplitude/observation/uncertainty protocol stops before test and FNO; it is not an empirical KILL and receives no amplitude/ensemble rescue |
| CNN has 0 dropped members of 51,200 under the all-action 21-LT rule; learned Tf is 10 LT | Limitation | results/l96_neural_artifact_audit.json, solver_statistics and readings.json; AAHLSTABLE/AAHLNAUDIT/AAHPARTIAL | Decision errors occur without triggering the instability drop rule |
| Frozen discrete-grid reading, independent streams, nominal commitment accounting, exact cost replay, and retained-artifact SHA256 inventories are available | Instrument | common.py, readings.py, audit_l96_neural.py, make_numbers.py; results/artifact_inventory.json | Reusable checks; no end-to-end latency or confidence-coverage guarantee |

Descriptive partial correlations over all 48 (arm,T) units are 0.9454 for accuracy–response controlling ACC and -0.4762 for accuracy–ACC controlling response. These are descriptive pooled coefficients, not inference or strongest-practice evidence.

All findings trace to branch `paper/aspen-2026-10-horizon`, repository `aspen/horizon/NUMBERS.md`, its zero-mismatch checker, and raw task-checkout `aspen/horizon/runs/` artifacts on sulaco/Baccus. The final CNN panel uses one full-FP32 CUDA backend; preliminary CPU outputs are retained and excluded. Gate and Step 0 provenance remain in the canonical reports.

Candidate headline contracts: none adopted or dispatched. A new action panel, operating point, robustness campaign or publication is a separate decision. See [[L_Aspen-Act-Beyond-Horizon-Claim-Ledger-2026-10]], [[R_Aspen-Act-Beyond-Horizon-Kill-Test-2026-10]], and [[Session-Review-Aspen-Horizon-2026-10-04]].
