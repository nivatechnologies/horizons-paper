# Kolmogorov flow: Phase A pilot (post-freeze extension)

All numbers are **estimate (pilot)**. This pilot measures system properties only. It produced no confirmation data,
no tokenizer, no bound and no decode-and-integrate result. The proposed part-2 values are in
`kolmogorov_pilot_proposal.yaml`, and the raw outputs are in `kolmogorov_pilot/*.json`.
Code: `th/kolmogorov.py` and `scripts/ext_kolmogorov_pilot.py`.

## System
- **Equation (vorticity form):** ω_t + u·∇ω = (1/Re)∇²ω − n cos(n y), with ∇²ψ = −ω, u = ψ_y, v = −ψ_x.
- **Domain and parameters:** [0, 2π)², n = 4, Re = 40.
- **Forcing:** sin(n y) x̂ in the x-momentum equation, which is the form of Chandler & Kerswell (2013, JFM 722,
  554–595, §2). The same equations are restated in arXiv:2408.05079.
- **Laminar check:** the laminar state ω = −(Re/n) cos(n y) is held to 8e-13 over 10 time units.
- **Scheme:** pseudo-spectral, 2/3-rule square dealiasing (|k_x|, |k_y| ≤ 21 at N = 64), integrating-factor RK4.
  - IFRK4 is used because the viscous term is diagonal and only mildly stiff (|k|²dt/Re ≤ 0.11). The integrating
    factor treats it exactly.
  - Accuracy is checked by halving dt.
- **Tests:**
  - An exact viscous-decay eigenmode is reproduced to 1e-14.
  - In an inviscid, unforced run, the enstrophy drift falls 31× when dt is halved.
- **Burn-in:** 500 time units from random low-mode initial conditions. The ensemble energy and dissipation settle
  within about 50–100 time units (64 starts), and no start was trapped off the turbulent state.

## λ₁ (renormalized twins)
Setup: τ = 1, δ₀ = 1e-6·‖ω‖, 128 starts, 2,000 time units each, with the first 20 time units discarded.

| run | λ₁ ± s.e. | vs 64², dt 0.01, f64 |
|---|---|---|
| 64², dt 0.01, float64 | **0.12683 ± 0.00079** | (reference) |
| 128², dt 0.01 | 0.12584 ± 0.00078 | −0.78% (0.9 s.e.) |
| 64², dt 0.005 | 0.12697 ± 0.00077 | +0.11% |
| 64², float32, δ₀ 1e-4 | 0.12612 ± 0.00075 | −0.56% (0.7 s.e.) |
| 64², float64, δ₀ 1e-4 | 0.12683 ± 0.00079 | −0.01% |

- **Chaos:** every start is positive (the minimum is 0.106). The Lyapunov time is 7.9 time units.
- **Stop condition:** not triggered. Going from 64² to 128² moves λ by 0.8%, against the 5% limit.
- **Statistics:** these agree within 0.3% (≤ 0.8 s.e.) across the grid, dt and precision checks.
  - Time-mean E = 0.6837 ± 0.0003, Z = 2.345 ± 0.008, and I = D = 0.1173 ± 0.0004.
  - The energy balance closes.
  - At 64², the energy fraction in the last retained shell is 2e-8, and above k = 11 it is 6e-5.
- **Float32:** it does not change λ materially. It is not needed, because float64 is fast on this card.

## Proposals (details in the YAML)
- **Grid, precision, device:** N = 64, dt = 0.01, float64 on cuda:0.
- **Frame unit:** 0.07 time units (7 dt).
- **Frame intervals:** Δ = 0.14, 0.35 and 0.70, giving λΔ = 0.0178, 0.0444 and 0.0888.
- **Window:** W/λ = 212.9 time units.
- **Panel:** 46.2 time units of pre-history (5.86 Lyapunov times) and 214.9 time units after t = 0.
  - That is 3,731 stored frames per state.
  - The 1,000-state panel takes 56 GB as exact float64 retained Fourier coefficients.
- **Scored field (A2):** grid vorticity on the 64 × 64 grid.
  - Nothing is applied before scoring.
  - The true states are exactly band-limited and zero-mean in exact arithmetic.
  - Decoded patch concatenations are scored as is.
- **σ_A (pilot):** 131.7 in the grid-Euclidean norm (2.06 per point), from 10,000 states on 100 trajectories.
  - The per-trajectory range is 98–137, so the frozen value should come from the calibration fit split.
- **Calibration (A5):**
  - **Fit split:** 256 independent trajectories × 800 states, every 1.4 time units (204,800 states).
    - Patch counts: 3.28M patches for the 4×4 layout, 13.1M for 8×8 and 52.4M for 16×16.
    - At 2^16 codes that is 50, 200 and 800 samples per code.
  - **Held-out split:** 64 trajectories × 800 states (51,200 states).
  - **Memory:** 3.4 GB and 0.8 GB as float32.
- **Seeds:** system index 8 (KS uses 6 and 7). Streams are 1080x, 2080x, 3080x, 4080x and 5080x.

## Compute (cuda:0 float64, measured; "contended" means with the coordinator's jobs running)
| task | GPU | CPU, 32 threads |
|---|---|---|
| 1,000-state panel | 9 min (35 min contended) | 4.5 h |
| Calibration generation | about 7 min | about 3 h |
| Decode-and-integrate, per tokenizer | 2.6 min | 1.3 h |
| Decode-and-integrate, 15 tokenizers | 40 min (2.4 h contended) | 19 h |

**k-means at 2^16 codes, 300 iterations:**
- **4×4 layout:** about 2.6 GPU-hours. On CPU it is about 26 hours.
- **8×8 layout:** 0.65 GPU-hours on a subset of 50 samples per code.
- **16×16 layout:** about 0.5 GPU-hours on a subset of 50 samples per code.
- **Whole rate ladder:** about 1.6–2× the 2^16 cost for each layout.

**Exact nearest-code d_C for the bound:** about 5 minutes per 2^16 codebook.

**Summary:** the GPU is needed for large-K k-means and is recommended for decode-and-integrate.
