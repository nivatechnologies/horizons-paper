## GB10 execution results — Amendment 1b

Frozen outcome: **otherwise**. Evaluable queries: **4 of 4**. Complete arm panel: **True**. Step 0 was retained without rerunning.

The experiment uses the amended fixed-lead sensitivity and inherited 8-frame L_range / 4-frame FNO-θ inputs, with three parameter channels only for FNO-θ. All arms use the same physical query functional at each test θ; its explicit parameter factors are evaluation constants, not additional inputs to L_range or the identifier. Point errors use each point's 0.5-Lyapunov-time lead and 100 independent states. The law uses all 11 observations and exactly 270 misfit evaluations per state.

45° points, ensemble disagreement and context identifiability were cut in the specified order before data. This is one selector framing with four queries; a negative is not four independent negative findings. Selector provenance and exact query overlap remain in CODEX_QUERIES.md, QUERY_OVERLAP.md and the gate appendix.

### Every-point chaos gate

| point | Re | A | alpha | lam | ci_lo | ci_hi | chaotic |
|---|---|---|---|---|---|---|---|
| centre | 40 | 1 | 0.07733 | 0.1734 | 0.1649 | 0.182 | True |
| q0_0 | 38.7 | 1.2 | 0.08157 | 0.2089 | 0.2011 | 0.2167 | True |
| q0_90 | 52 | 1.021 | 0.07778 | 0.2843 | 0.2809 | 0.2877 | True |
| q1_0 | 34.43 | 1.2 | 0.07467 | 0.1026 | 0.09578 | 0.1093 | True |
| q1_90 | 39.61 | 1.014 | 0.1083 | 0.1547 | 0.1531 | 0.1564 | True |
| q2_0 | 45.96 | 1.142 | 0.1068 | 0.2689 | 0.2666 | 0.2711 | True |
| q2_90 | 52 | 0.9501 | 0.06699 | 0.2477 | 0.2416 | 0.2538 | True |
| q3_0 | 37.48 | 1.2 | 0.07491 | 0.1573 | 0.148 | 0.1665 | True |
| q3_90 | 39.81 | 1.015 | 0.1083 | 0.1553 | 0.1538 | 0.1569 | True |

Source: aspen/evidence/results/chaos.csv; checked in NUMBERS.md.

### Endpoint ratios

| query | arm | error_0 | error_90 | ratio | symmetric_ratio | available |
|---|---|---|---|---|---|---|
| forcing_power | L_range-3 | 0.02692 | 0.04668 | 0.5768 | 1.734 | True |
| forcing_power | FNO-theta | 0.01259 | 0.02888 | 0.436 | 2.294 | True |
| forcing_power | law | 0.01965 | 0.008602 | 2.285 | 2.285 | True |
| forcing_power | persistence | 0.5636 | 0.7439 | 0.7576 | 1.32 | True |
| forcing_power | centre-law | 0.3563 | 0.1 | 3.562 | 3.562 | True |
| viscous_energy | L_range-3 | 0.07385 | 0.06732 | 1.097 | 1.097 | True |
| viscous_energy | FNO-theta | 0.01812 | 0.02065 | 0.8772 | 1.14 | True |
| viscous_energy | law | 0.0908 | 0.02689 | 3.376 | 3.376 | True |
| viscous_energy | persistence | 0.8632 | 0.9235 | 0.9348 | 1.07 | True |
| viscous_energy | centre-law | 0.4806 | 0.1235 | 3.893 | 3.893 | True |
| drag_energy | L_range-3 | 0.08908 | 0.1156 | 0.7705 | 1.298 | True |
| drag_energy | FNO-theta | 0.06325 | 0.04896 | 1.292 | 1.292 | True |
| drag_energy | law | 0.02625 | 0.0113 | 2.323 | 2.323 | True |
| drag_energy | persistence | 0.6264 | 0.3793 | 1.651 | 1.651 | True |
| drag_energy | centre-law | 1.075 | 0.4938 | 2.177 | 2.177 | True |
| viscous_enstrophy | L_range-3 | 0.05851 | 0.1811 | 0.3231 | 3.095 | True |
| viscous_enstrophy | FNO-theta | 0.01725 | 0.02816 | 0.6124 | 1.633 | True |
| viscous_enstrophy | law | 0.08138 | 0.07983 | 1.019 | 1.019 | True |
| viscous_enstrophy | persistence | 0.6785 | 1.129 | 0.6007 | 1.665 | True |
| viscous_enstrophy | centre-law | 0.7633 | 0.0817 | 9.342 | 9.342 | True |

Source: aspen/evidence/results/ratios.csv; checked in NUMBERS.md.

### Index and baselines

| arm | n_units | rho_g | rho_perp | gap | rho_euclidean | rho_mahalanobis |
|---|---|---|---|---|---|---|
| L_range-3 | 12 | 0.3844 | 0.8115 | 0.4271 | 0.7053 | 0.6336 |
| FNO-theta | 12 | -0.1993 | 0.1993 | 0.3986 | 0.3131 | 0.1424 |
| law | 12 | 0.6941 | 0.5873 | 0.1068 | 0.5326 | 0.6798 |
| persistence | 12 | -0.1886 | 0.4449 | 0.6336 | -0.02159 | -0.1602 |
| centre-law | 12 | 0.8685 | 0.4983 | 0.3702 | 0.7809 | 0.9468 |

Source: aspen/evidence/results/correlations.csv; checked in NUMBERS.md.

The partial correlation controlling λ(θ)·h is unavailable because that control equals 0.5 at every point. Unavailable statistics satisfy no outcome clause. No epsilon denominator or excluded-point substitution is used.

### Learned recipe and cost

| arm | steps | n_in | param_channels | params | best_step | best_val | train_seconds |
|---|---|---|---|---|---|---|---|
| L_range-3 | 3e+04 | 8 | 0 | 1.68e+07 | 3e+04 | 0.0001871 | 6310 |
| FNO-theta | 3e+04 | 4 | 3 | 1.68e+07 | 3e+04 | 9.858e-05 | 6236 |

Source: aspen/evidence/results/training.csv; checked in NUMBERS.md.

### Figures and provenance

Greyscale figures: aspen/evidence/figures/AEA1_error_angle.png, AEA2_error_displacement.png, AEA3_index_baselines.png, with SVG equivalents. Mean normalized query errors and state-bootstrap 95% intervals are in AEA-E. Centre and reported local gradients are in AEA-G and AEA-GP. Tables use inherited NUMBERS column/section validation, producing commit SHAs and source SHA256 hashes.

The frozen PASS/KILL rules return otherwise; Todd decides the next stage.

L_range-3: 0 queries with R ≥ 2; 2 with max(R, 1/R) ≤ 1.3; correlation gap 0.4271.

FNO-theta: 0 queries with R ≥ 2; 2 with max(R, 1/R) ≤ 1.3; correlation gap 0.3986.

The law meets R ≤ 1.3 for 1 queries. Neither PASS nor KILL is satisfied. This selector framing does not establish the proposed directional thesis. No stage-2 experiment was started.
