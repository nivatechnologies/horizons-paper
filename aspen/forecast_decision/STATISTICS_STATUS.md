# Statistics coordinator status

Baseline, N-mis, N-win and null descriptive metrics are checked from raw primary-panel arrays, with paired case bootstrap, all-case counterparts, exclusions, mean/spread cost decomposition, energy benefit, action usage and injected work. The evidence is registered in NUMBERS_FULL_METRICS_BASELINE.md. This descriptive report licenses no headline sentence. Figures under figures/baseline include the WO §11 primary scatter plots and baseline lead comparison.

Test access was authorized after the root coordinator's Stage 1 reading, at 2026-10-05T01:08:15Z. The statistics worker has no training or model-selection role and does not open the initial Stage 1 gate reading. Access events are retained in runs/statistics_access.jsonl.

The sulaco user service `aspen-afd-statistics.service` waits for the FINAL validation-selection consumer manifest and completed inference registry, checks checkpoint identities and complete compute receipts, then evaluates Stage 2 and generates its checked report. The Baccus user service `aspen-afd-statistics-manifests.service` copies only public selection, inference and compute metadata to sulaco; it transfers no test output to Baccus. The statistics evaluator loads metric code after readiness, and preserves immutable source snapshots for provenance.

Inspect or resume:

```bash
ssh sulaco 'systemctl --user status aspen-afd-statistics.service'
ssh sulaco 'cat /home/todd/work/aspen-forecast-decision-20261005/aspen/forecast_decision/runs/stage2_statistics_status.json'
systemctl --user status aspen-afd-statistics-manifests.service
ssh sulaco 'systemctl --user restart aspen-afd-statistics.service'
```

Final products use distinct NUMBERS_FULL_METRICS_STAGE2.md and NUMBERS_FULL_METRICS_STAGE2B.md fragments; root registers them in the main NUMBERS file. The complete Stage 2 gate report is generated only after all mandatory arms, validation selection and test inference finish. Its arithmetic checker recomputes the gate and sentence conditions and rejects finite tampering and NaN. Root renders checked figures locally and assigns the separate factual audit. The factual audit and final publication decision remain open.

Stage 2b truth still requires Todd's separate sampler go. No Stage 2b outcome or full-campaign completion is claimed here. The one-scale secondary panel is descriptive and supplies no gate or licensed sentence.
