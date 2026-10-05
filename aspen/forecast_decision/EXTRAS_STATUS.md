# Optional one-scale execution status

Owner: one_scale_extras physics/data worker. No training, model selection, Stage 1 gate reading or result-report access.

2026-10-05: read WO_v5.2 and AFD_FREEZE before implementation. CPU capacity was verified read-only on sulaco; no service was modified. Source extras.py implements independent secondary-panel generation and optional N-mis / N-win. Source artifact registration is required before evaluation.

Benchmark evidence: runs/extras_benchmark.json. Exact RK4 reverse derivative was checked against centered finite differences on an independent afd-dtcheck case (case 100). N-win benchmarks all member windows for that independent case. The 200-case fit-only projection multiplies the measured benchmark wall duration by the panel case count; it excludes rollout time and is not a measured campaign duration. No optional cuts justified by this measurement.

Test-access identity/timestamps will be recorded per case in runs/extras_access.jsonl. Each arm output has costs, means, spread traces and paired survivors for every frozen lead. N-win convergence diagnostics are retained per member. Secondary truth includes the no-action reference, actual-state trajectories and exact-endpoint RK4-stage injected work.
