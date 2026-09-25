# Kuramoto–Sivashinsky pilot (post-freeze extension, part 2 pilot)

All numbers are **estimate (pilot)**. They measure system properties only. No tokenizer, bound, decode-and-integrate
or confirmation data was used. Code: `th/ks.py`, `scripts/ext_ks_pilot.py`. Raw output: `ks_pilot.json`. Proposed
freeze values: `ks_pilot_proposal.yaml`.

## Scheme
- **Equation and domain:** u_t = −u u_x − u_xx − u_xxxx on [0, L), periodic, zero mean.
- **Discretization:** Fourier pseudo-spectral, rfft on N grid points. The state that is tokenized and scored is u(x_j).
- **Dealiasing:** Orszag 2/3 rule. Modes 1 ≤ m ≤ M = ⌊(N−1)/3⌋ are kept in the state and the nonlinear term; all other modes are zero. This is the exact Galerkin truncation, with 2M real degrees of freedom.
- **Time stepping:** ETDRK4 with contour-integral coefficients (Kassam & Trefethen 2005), in float64.
- **Tangent:** the exact derivative of the discrete ETDRK4 map.

## Lyapunov (Benettin/QR, 16 starts, lyapunov seed block)

| config | λ1 ± s.e. | D_KY ± s.e. |
|---|---|---|
| L = 22, N 64, dt 0.1 (20,000 tu) | 0.04845 ± 0.00032 | 4.241 ± 0.002 |
| L = 22, dt 0.05 | 0.04868 ± 0.00035 | 4.241 |
| L = 22, N 128 | 0.04864 ± 0.00042 | 4.244 |
| L = 100, N 256, dt 0.1 (10,000 tu) | 0.09063 ± 0.00034 | 21.48 ± 0.01 |
| L = 100, dt 0.05 | 0.09123 ± 0.00048 | 21.50 |
| L = 100, N 512 | 0.09043 ± 0.00040 | 21.48 |

**Comparison with the literature, L = 22.**
- The L = 22 spectrum (0.0484, 0.0005, −0.0001, −0.0036, −0.188, −0.257, −0.290, −0.311, −1.963, −1.967) matches Cvitanović, Davidchack & Siminos (2010): 0.048, 0, 0, −0.003, −0.189, −0.256, −0.290, −0.310, −1.963, −1.967.
- Their exponents imply D_KY ≈ 4.24.
- Edson et al. (2019, Table 1) report λ1 = 0.043 and D_KY = 5.198. Their L = 22 column has five exponents ≥ −0.008 before −0.185, where ours has four.
- **[hypothesis]** Edson's run carries the spatial mean mode, which is conserved and gives one extra neutral exponent. That would add about 1 to D_KY. Our system is zero-mean. Their L = 100 value is also about 1 above ours (22.44 against 21.48).
- **Stop condition:** λ1(L = 22) lies inside [0.040, 0.050]. Nothing was tuned.

## Sum-versus-trace (full retained spectrum)
The trace is 2 Σ_{m≤M}(k²−k⁴): −11,663.74 for L = 22 (N = 64, 42 exponents) and −26,836.40 for L = 100 (N = 256, 170 exponents).

| config | relative error of the sum |
|---|---|
| L = 22, dt 0.02 / 0.01 / 0.005 / 0.0025 | 0.38 / 0.086 / 1.3e-4 / 2.0e-6 |
| L = 100, dt 0.01 / 0.005 | 1.6e-3 / 1.3e-5 |
| L = 22, dt 0.1 (production) | 0.81 |

- **Convergence:** the sum converges to the trace as dt → 0. At dt = 0.0025 the error is 0.024 in absolute terms, out of 11,664.
- **Production dt:** at dt = 0.1, the stiff exponents of the discrete map saturate near −111 instead of −1,258. The ETDRK4 tangent couples the stiff modes to the resolved ones at order k u/|L_m|, which is far above e^{hL_m}.
- **Leading exponents are unaffected:** the first 10 agree across every dt to within their s.e. The check therefore applies to the Galerkin flow, which the small-dt runs approach. It does not apply to the production-dt map's stiff tail.

## Resolution (64 identical starts, pilot block)
| comparison | max relative difference at t = 1 / 10 / 50 |
|---|---|
| L = 22, dt/2 | 6.5e-6 / 6.8e-5 / 7.5e-3 |
| L = 22, 2N | 5.1e-8 / 5.7e-8 / 4.9e-8 |
| L = 100, dt/2 | 7.1e-6 / 1.1e-4 / 8.0e-2 |
| L = 100, 2N | 5.6e-7 / 5.7e-7 / 7.0e-7 |

- **Growth with t:** the dt/2 difference grows only by chaotic amplification.
- **Spectral tail:** mean |û_M| / max |û_m| is 4.9e-8 (L = 22) and 6.3e-7 (L = 100).
- **Effect of halving:** halving dt or doubling N moves λ1 by ≤ 0.7% (≤ 1.0 combined s.e.) and D_KY by ≤ 0.03.

## σ_A (pilot sample: 64 trajectories × 100 states, 20 tu apart)
- **L = 22:** 9.478 ± 0.012 (Euclidean norm over 64 points; per-point RMS 1.185).
- **L = 100:** 20.99 ± 0.015 (per-point RMS 1.312).
- The frozen σ_A will come from the calibration block.

## Proposal summary
| | L = 22 | L = 100 |
|---|---|---|
| N, dt | 64, 0.1 | 256, 0.1 |
| Burn-in | 1,000 tu | 500 tu |
| Δ (λΔ) | 0.4, 1.0, 2.0 (0.019, 0.048, 0.097) | 0.2, 0.5, 1.0 (0.018, 0.045, 0.091) |
| W/λ | 557.4 tu | 297.9 tu |
| Pre-history / post | 121.5 / 561.4 tu | 65.0 / 300.0 tu |
| Context (2.99 Lyapunov times) | 61.6 tu | 33.0 tu |
| Patch length, P = 8 / 16 / 32 | 8 / 4 / 2 points | 32 / 16 / 8 points |

- **Alternative Δ for L = 22:** 0.4, 0.9, 1.9 is closest to the targets, but the panel must then be stored every dt.
- **Blocks:**
  - Calibration: 10⁶ states for each L.
  - Training: 100 trajectories of 375 tu for L = 22 and 100 of 200 tu for L = 100, about 1,815 Lyapunov times each.
  - Confirmation: 1,000 panel states.
- **Seeds:** the freeze.yaml scheme, with new system indices ks22 = 6 and ks100 = 7.
- **Compute (single process):**
  - Panel: 73 s for L = 22 and 122 s for L = 100.
  - Decode-and-integrate: 24 s and 42 s per tokenizer.
  - Calibration integration: 130 s and 212 s.
