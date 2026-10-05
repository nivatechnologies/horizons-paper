# AFD numerical and sampler preflight

One-scale decision timestep check **PASS**, dt=0.01; 896 comparisons, 0 failures, no winner changes at any checked lead. Every one-scale solver run uses this dt. The output grid/predicate is unchanged.

Two-scale benchmark: 0.008907205 seconds per RK4 step for 2048 members on one sulaco CPU core at dt=.001. Projected mandatory 300-case, nine-action/no-action truth through 3 LT_ref: **11.884 single-core hours**. The WO estimated about96 including about15 for preparation/labels/checks. Combining the measured truth-rate projection with that still-unmeasured extra estimate gives 26.884 core-hours; this is not measured total campaign time. Actual dt chosen by the two-scale decision check may alter the projection.

Two-scale state check **PASS** at dt=0.001. Fast-state library contains4096 independent spinups, hashed before use.

Sampler check on 16 twin states and 64 conditioned draws each:
- pooled RMS draw spread / RMS error of conditional mean: **0.996688**;
- conditional-mean / realized subgrid-term correlation: **0.940899**;
- RMS draw spread: 0.405420243; RMS mean error: 0.406767536.

Per-state values, raw arrays and hashes are retained. The spread/error ratio is close to unity; no acceptance threshold was specified, so this report assigns no invented sampler PASS. Two-scale truth is awaiting Todd's go. State/time-step checks and the raw sampler do not establish that this observation-conditioned distribution is calibrated beyond these states.

Every value above traces to NUMBERS §AFD_NUMERICAL_PREFLIGHT. Recompute with report_preflight.py; checker passes and altered sampler ratio is rejected.
