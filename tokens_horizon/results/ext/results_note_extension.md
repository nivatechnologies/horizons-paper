
## POST-FREEZE extension (WO 2026-09-25, Amendments 1 and 2)

All numbers below are generated from committed result files by `scripts/ext_results_note.py`; NUMBERS.md sections K and K2 hold the full tables. Labels: bound / reference / learned / estimate; everything here is a **post-freeze extension**. Freeze commits: part 1 `94c6cd7`, Amendment 1 `f7fedcb`, Amendment 2 `d960d0b`, part 2a (KS) `b5b476e` with fix 1 `fd992f1`, part 2b (Kolmogorov) `ef2d9f0`; A9 prediction `468cabc`; B3 prefix-invariance pass `f5c9747`.

### Systems

| system | L | N | dt | λ | D_KY | W (time units) | Δ | σ_A |
|---|---|---|---|---|---|---|---|---|
| ks22 | 22 | 64 | 0.0025 | 0.04896 ± 0.00036 | 4.24 | 551.52 | 0.37 / 0.92 / 1.84 | 9.486 |
| ks100 | 100 | 256 | 0.005 | 0.09101 ± 0.00042 | 21.48 | 296.66 | 0.2 / 0.495 / 0.99 | 21.001 |
| kolmo40 (Re 40, n 4) | 2π | 64² | 0.01 | 0.12683 ± 0.00079 | – | 212.88 | 0.14 / 0.35 / 0.7 | 131.843 |

KS L = 22 D_KY is 4.24 (the WO's 5.2 is from a mean-mode-keeping convention; hypothesis). Kolmogorov: 64² → 128² moves λ by −0.8%. No particle filter was run in these systems (WO E3): with an indicator likelihood, a particle survives only if its predicted state falls in the observed cell, and the number of particles needed for that grows exponentially with the attractor dimension (D_KY 4.2–21 for KS, larger for Kolmogorov) and with the number of tokens per frame; at these dimensions the reference is infeasible (reasoning, not a measurement).

### KS L = 22, whole-state k-means (Δ = 0.92, ε 0.3, future frames)

| bits | bound (bound) | S_out(1) / S_out(3) / S_out(10) | p_0 | decode-and-integrate (reference) | persistence |
|---|---|---|---|---|---|
| 4 | 0.070 | 0.00 / 0.00 / 0.00 | 0.892 | 0.070 | 0.070 |
| 5 | 0.081 | 0.00 / 0.00 / 0.00 | 0.816 | 0.082 | 0.081 |
| 6 | 0.106 | 0.00 / 0.00 / 0.00 | 0.710 | 0.097 | 0.093 |
| 7 | 0.162 | 0.02 / 0.00 / 0.00 | 0.588 | 0.125 | 0.112 |
| 8 | 0.241 | 0.04 / 0.00 / 0.00 | 0.481 | 0.154 | 0.121 |
| 9 | 0.359 | 0.08 / 0.00 / 0.00 | 0.325 | 0.180 | 0.125 |
| 10 | 0.538 | 0.21 / 0.00 / 0.00 | 0.204 | 0.240 | 0.131 |
| 11 | 0.935 | 0.40 / 0.03 / 0.00 | 0.090 | 0.319 | 0.139 |
| 12 | 4.684 | 0.81 / 0.54 / 0.12 | 0.016 | 0.425 | 0.139 |
| 13 | 16.377 | 0.95 / 0.89 / 0.67 | 0.000 | 0.495 | 0.145 |
| 14 | 25.270 | 0.99 / 0.98 / 0.96 | 0.000 | 0.587 | 0.147 |
| 15 | 27.000 | 1.00 / 1.00 / 1.00 | 0.000 | 0.736 | 0.148 |
| 16 | 27.000 | 1.00 / 1.00 / 1.00 | 0.000 | 0.828 | 0.150 |

*Source: `results/ext/ks/e3_rows.csv`*

### KS patch families (primary Δ, ε 0.3, future frames)

| system | P | b | total bits | bound | S_out(1) | decode-and-integrate | persistence |
|---|---|---|---|---|---|---|---|
| ks22 | 8 | 8 | 64 | 27.000 | 1.00 | 0.969 | 0.148 |
| ks22 | 8 | 10 | 80 | 27.000 | 1.00 | 1.357 | 0.150 |
| ks22 | 8 | 12 | 96 | 27.000 | 1.00 | 1.734 | 0.150 |
| ks22 | 8 | 14 | 112 | 27.000 | 1.00 | 2.115 | 0.150 |
| ks22 | 8 | 16 | 128 | 27.000 | 1.00 | 2.570 | 0.151 |
| ks22 | 16 | 8 | 128 | 27.000 | 1.00 | 1.502 | 0.150 |
| ks22 | 16 | 10 | 160 | 27.000 | 1.00 | 2.163 | 0.151 |
| ks22 | 16 | 12 | 192 | 27.000 | 1.00 | 2.650 | 0.151 |
| ks22 | 16 | 14 | 224 | 27.000 | 1.00 | 3.077 | 0.150 |
| ks22 | 16 | 16 | 256 | 27.000 | 1.00 | 3.498 | 0.151 |
| ks22 | 32 | 8 | 256 | 27.000 | 1.00 | 2.219 | 0.150 |
| ks22 | 32 | 10 | 320 | 27.000 | 1.00 | 2.778 | 0.151 |
| ks22 | 32 | 12 | 384 | 27.000 | 1.00 | 3.432 | 0.150 |
| ks22 | 32 | 14 | 448 | 27.000 | 1.00 | 4.124 | 0.150 |
| ks22 | 32 | 16 | 512 | 27.000 | 1.00 | 4.794 | 0.151 |
| ks100 | 8 | 8 | 64 | 0.599 | 0.20 | 0.132 | 0.070 |
| ks100 | 8 | 10 | 80 | 22.836 | 0.99 | 0.228 | 0.102 |
| ks100 | 8 | 12 | 96 | 27.000 | 1.00 | 0.325 | 0.117 |
| ks100 | 8 | 14 | 112 | 27.000 | 1.00 | 0.452 | 0.125 |
| ks100 | 8 | 16 | 128 | 27.000 | 1.00 | 0.572 | 0.129 |
| ks100 | 16 | 8 | 128 | 27.000 | 1.00 | 0.376 | 0.118 |
| ks100 | 16 | 10 | 160 | 27.000 | 1.00 | 0.604 | 0.127 |
| ks100 | 16 | 12 | 192 | 27.000 | 1.00 | 0.880 | 0.133 |
| ks100 | 16 | 14 | 224 | 27.000 | 1.00 | 1.174 | 0.135 |
| ks100 | 16 | 16 | 256 | 27.000 | 1.00 | 1.466 | 0.137 |
| ks100 | 32 | 8 | 256 | 27.000 | 1.00 | 0.925 | 0.132 |
| ks100 | 32 | 10 | 320 | 27.000 | 1.00 | 1.312 | 0.134 |
| ks100 | 32 | 12 | 384 | 27.000 | 1.00 | 1.715 | 0.136 |
| ks100 | 32 | 14 | 448 | 27.000 | 1.00 | 2.131 | 0.137 |
| ks100 | 32 | 16 | 512 | 27.000 | 1.00 | 2.567 | 0.137 |

*Source: `results/ext/ks/e3_rows.csv`*

### A9 prospective test (KS L = 22 whole-state; predictor committed in `468cabc` before any odd rate)

| R | observed (reference) [95%] | Ĥ (estimate) | observed − Ĥ [90%] | criterion |
|---|---|---|---|---|
| 7 | 0.1248 [0.1150, 0.1352] | 0.1216 | 0.0032 [-0.0052, 0.0118] | criterion met |
| 9 | 0.1797 [0.1676, 0.1920] | 0.2288 | -0.0491 [-0.0594, -0.0389] | criterion met |
| 11 | 0.3193 [0.2981, 0.3396] | 0.3360 | -0.0167 [-0.0338, -0.0001] | criterion met |

*Source: `results/ext/ks/a9_result.csv`*

This tests prospective interpolation across held-out rates within the specified system, tokenizer family and rate range; it does not test extrapolation or cross-system transfer. Exposure record: no odd-rate decode-and-integrate horizon was computed or inspected before the prediction commit.

### Kolmogorov patch layouts (Δ = 0.35, ε 0.3, future frames)

| layout | b | total bits | bound | S_out(1) / (3) / (10) | p_0 | decode-and-integrate | persistence |
|---|---|---|---|---|---|---|---|
| 4x4 | 8 | 128 | 0.134 | 0.01 / 0.00 / 0.00 | 0.768 | 0.238 | 0.061 |
| 4x4 | 10 | 160 | 2.101 | 0.54 / 0.28 / 0.02 | 0.266 | 0.415 | 0.115 |
| 4x4 | 12 | 192 | 6.792 | 0.75 / 0.59 / 0.24 | 0.157 | 0.679 | 0.139 |
| 4x4 | 14 | 224 | 10.162 | 0.82 / 0.73 / 0.40 | 0.116 | 0.885 | 0.149 |
| 4x4 | 16 | 256 | 11.819 | 0.85 / 0.77 / 0.48 | 0.093 | 1.125 | 0.153 |
| 8x8 | 8 | 512 | 2.368 | 0.56 / 0.30 / 0.03 | 0.228 | 0.779 | 0.096 |
| 8x8 | 10 | 640 | 12.001 | 0.86 / 0.78 / 0.48 | 0.082 | 1.122 | 0.134 |
| 8x8 | 12 | 768 | 13.965 | 0.90 / 0.82 / 0.56 | 0.048 | 1.456 | 0.149 |
| 8x8 | 14 | 896 | 15.591 | 0.93 / 0.86 / 0.62 | 0.033 | 1.788 | 0.155 |
| 8x8 | 16 | 1024 | 19.033 | 0.97 / 0.91 / 0.75 | 0.007 | 2.029 | 0.158 |
| 16x16 | 8 | 2048 | 18.278 | 0.96 / 0.90 / 0.72 | 0.008 | 1.935 | 0.138 |
| 16x16 | 10 | 2560 | 26.908 | 1.00 / 1.00 / 1.00 | 0.000 | 2.288 | 0.151 |
| 16x16 | 12 | 3072 | 27.000 | 1.00 / 1.00 / 1.00 | 0.000 | 2.662 | 0.156 |
| 16x16 | 14 | 3584 | 27.000 | 1.00 / 1.00 / 1.00 | 0.000 | 2.989 | 0.159 |
| 16x16 | 16 | 4096 | 27.000 | 1.00 / 1.00 / 1.00 | 0.000 | 3.256 | 0.160 |

*Source: `results/ext/kolmo/e3_rows.csv`*

**EXT_FREEZE reading:** bound below 1 Lyapunov time at any configuration with ≥ 2^12 codes per token and ≥ 64 tokens per frame: **no** (smallest: kolmo_patch_L8_b12 at Δ 0.14, 13.90 Lyapunov times; 18 configurations).

Decode-and-integrate resolution check (8×8, b = 12, 300 states, 128² vs 64²): relative change 0.0; crossing frames identical for every state.

### Smallest tested rate reaching 1 / 3 / 10 Lyapunov times (A3 rule; 'not reached' = not within the tested grid)

| system | family | quantity | τ = 1 | τ = 3 | τ = 10 |
|---|---|---|---|---|---|
| ks22 | whole | bound | 12 | 12 | 13 |
| ks22 | whole | decode_and_integrate | not reached within the tested grid | not reached within the tested grid | not reached within the tested grid |
| ks22 | P = 8 | bound | 64 | 64 | 64 |
| ks22 | P = 8 | decode_and_integrate | 80 | not reached within the tested grid | not reached within the tested grid |
| ks22 | P = 16 | bound | 128 | 128 | 128 |
| ks22 | P = 16 | decode_and_integrate | 128 | 224 | not reached within the tested grid |
| ks22 | P = 32 | bound | 256 | 256 | 256 |
| ks22 | P = 32 | decode_and_integrate | 256 | 384 | not reached within the tested grid |
| ks100 | P = 8 | bound | 80 | 80 | 80 |
| ks100 | P = 8 | decode_and_integrate | not reached within the tested grid | not reached within the tested grid | not reached within the tested grid |
| ks100 | P = 16 | bound | 128 | 128 | 128 |
| ks100 | P = 16 | decode_and_integrate | 224 | not reached within the tested grid | not reached within the tested grid |
| ks100 | P = 32 | bound | 256 | 256 | 256 |
| ks100 | P = 32 | decode_and_integrate | 320 | not reached within the tested grid | not reached within the tested grid |
| kolmo40 | layout 4x4 | bound | 160 | 192 | 224 |
| kolmo40 | layout 4x4 | decode_and_integrate | 256 | not reached within the tested grid | not reached within the tested grid |
| kolmo40 | layout 4x4 | persistence | not reached within the tested grid | not reached within the tested grid | not reached within the tested grid |
| kolmo40 | layout 8x8 | bound | 512 | 640 | 640 |
| kolmo40 | layout 8x8 | decode_and_integrate | 640 | not reached within the tested grid | not reached within the tested grid |
| kolmo40 | layout 8x8 | persistence | not reached within the tested grid | not reached within the tested grid | not reached within the tested grid |
| kolmo40 | layout 16x16 | bound | 2048 | 2048 | 2048 |
| kolmo40 | layout 16x16 | decode_and_integrate | 2048 | 4096 | not reached within the tested grid |
| kolmo40 | layout 16x16 | persistence | not reached within the tested grid | not reached within the tested grid | not reached within the tested grid |

Nominal total bits per frame (P·b), primary Δ, ε 0.3, future frames; 'smallest tested rate for this tokenizer family', not a minimum bit requirement. Monotone flags and the lower-95% variant are in the source files (`results/ext/ks/thresholds.csv`, `results/ext/kolmo/thresholds_a3.csv`).

### E4 (learned KS cell)

All 48 candidates (P ∈ {16, 32}, b ∈ {10, …, 16}, both KS domains, all Δ) have a validation restricted-mean bound of 27 (every state survives the window). Selected cell: none; support-permissive contrast: none. "No tested configuration satisfying the E4 size requirements had a validation restricted-mean support horizon below one Lyapunov time." No E4 model was trained; the model code and its prefix-invariance test (Amendment 2 B3) are committed.

### Reviewer controls on Lorenz-63 (K2)

**Probe control (E5.1), MLP probes, horizon [95%]:**

| cell | trained A | untrained A | token-history MLP |
|---|---|---|---|
| b4_D0.02 | 1.136 [1.089, 1.185] | 0.570 [0.528, 0.613] | 2.207 [2.133, 2.280] |
| b4_D0.05 | 1.085 [1.034, 1.136] | 0.520 [0.484, 0.561] | 1.834 [1.760, 1.906] |
| b4_D0.1 | 1.018 [0.960, 1.074] | 0.513 [0.482, 0.549] | 1.446 [1.388, 1.509] |
| b6_D0.02 | 1.083 [1.022, 1.150] | 0.869 [0.819, 0.921] | 2.429 [2.359, 2.504] |

Reading (Amendment 1 A8.5, frozen margins): at 4 bits for all Δ, 'training makes the precision more recoverable by the tested readout'; at 6 bits Δ 0.02 no reading applies. The paper never says the untrained representation lacks it.

**Ties with the bound at 4 bits (Amendment 2 B4): P(VPT = T_out | Δ < T_out ≤ W) [95%]:**

| Δ | A (seeds pooled) | persistence | random-code | automatic first-frame | jointly censored |
|---|---|---|---|---|---|
| 0.02 | 0.863 [0.840, 0.885] | 0.402 | 0.008 | 258 | 0 |
| 0.05 | 0.815 [0.785, 0.845] | 0.136 | 0.009 | 274 | 0 |
| 0.1 | 0.762 [0.733, 0.790] | 0.053 | 0.012 | 259 | 0 |

**B snapped to its nearest prototype (A8.1), 4 bits:**

| Δ | B | B snapped | bound | snapped − bound [95%] | reading |
|---|---|---|---|---|---|
| 0.02 | 1.540 | 0.118 | 0.137 | -0.019 [-0.023, -0.016] | approximately equal ; ci90 [-0.022, -0.016] |
| 0.05 | 1.377 | 0.214 | 0.263 | -0.049 [-0.057, -0.041] | approximately equal ; ci90 [-0.056, -0.042] |
| 0.1 | 1.265 | 0.374 | 0.472 | -0.098 [-0.113, -0.083] | no frozen reading applies (a non-significant difference is not equivalence) ; ci90 [-0.111, -0.085] |

**Larger and longer model (E5.3; width 256, 6 layers, 40,000 steps; Δ 0.05):**

| arm | bits | frozen size | larger | larger − frozen [95%] | reading |
|---|---|---|---|---|---|
| A | 4 | 0.229 | 0.236 | 0.006 [-0.001, 0.014] | approximately equal |
| B | 4 | 1.377 | 1.995 | 0.617 [0.548, 0.688] | frozen size well below larger |
| A | 10 | 2.310 | 2.291 | -0.019 [-0.092, 0.064] | approximately equal |
| B | 10 | 1.485 | 2.599 | 1.114 [1.013, 1.210] | frozen size well below larger |
| C | 0 | 3.079 | 4.078 | 0.998 [0.768, 1.247] | frozen size well below larger |

**Same-panel headline (A8.3), first 300 states, 4 bits, Δ 0.02:**

| series | mean | minus particle filter [95%] | reading |
|---|---|---|---|
| history reference (particle filter) | 3.060 |   |  |
| bound | 0.131 | -2.929 [-3.109, -2.761] | well below the particle filter |
| A | 0.119 | -2.941 [-3.116, -2.780] | well below the particle filter |
| B | 1.574 | -1.486 [-1.679, -1.317] | well below the particle filter |
| C (sigma=0) | 2.514 | -0.546 [-0.767, -0.330] | well below the particle filter |
| D | 1.942 | -1.118 [-1.296, -0.951] | well below the particle filter |

### Release gate B5 (bootstrap resampling unit) — outcome recorded

**FAIL, then rerun.** Reading the resampling unit from the code: confirmation panels are one independent trajectory per state (pass); decomposition and D_eff already resample calibration trajectories (pass); the exchange-law h curve, predictions, r by orientation, FSLE and the post-freeze per-state/geometric variants resampled individual calibration states that share trajectories (1,000 h states from 150 trajectories, median 7 per trajectory, ~14 time units apart, inside the ~30 time-unit scoring window) — fail. Rerun with the calibration trajectory as the resampling unit (commit `100b159`): point estimates unchanged; interval widths ×0.84–1.43 (median ×1.01–1.03); **no frozen reading changed**. Gate record: NUMBERS.md section K2F. Release may proceed on this gate.

