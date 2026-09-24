# FREEZE: How Much Horizon Does a Bit Buy?

Committed before any result on confirmation trajectories and before any learned-model training run
(the only training before this commit is the Task 0 timing pilot on the training block, which sets the step
budget and produces no result). `freeze.yaml` is the machine-readable twin that all code reads. Where
the two differ, `freeze.yaml` governs, and the difference is an error to be fixed in a new commit.

A frozen value found to be wrong is fixed in a new commit that states the error. Everything downstream is
rerun and both results are reported. Checkpoints are selected by validation loss only.

Environment: Python 3.12.3, venv at `<repo>/.venv`, lockfile `env/requirements.lock`
(sha256 `249a442443acd4f6176852df8e9f8ba62942478045c98f06c1bbb716b43dac5c`): numpy 2.1.3, scipy 1.18.1,
scikit-learn 1.9.1, torch 2.13.0+cu130, matplotlib 3.11.2, pyyaml 6.0.3. Hardware: Baccus, 128 cores,
3 × NVIDIA CMP 170HX (sm_80).

## 2.1 Systems and integration
Lorenz-63 σ = 10, β = 8/3, ρ ∈ {28, 45}. Lorenz-96 F = 8, d ∈ {5, 6, 10, 20}. RK4, dt = 0.01, float64. Burn-in
5,000 steps from Gaussian starts (Lorenz: (1, 1, 20) + N(0, I); L96: 8 + N(0, I)). Full spectrum by Benettin/QR
(renormalize every 10 steps, 16 starts, lyapunov seed block). The spectrum sum must be within 1e-3 of the divergence.
Step-halving (dt = 0.005) on every headline configuration.

**Measured λ (dt = 0.01), which fixes the window W/λ everywhere:**

| system | λ | s.e. | D_KY | sum − divergence |
|---|---|---|---|---|
| lorenz28 | 0.905345 | 0.0015 | 2.062 | 1.0e-4 |
| lorenz45 | 1.215288 | 0.0018 | 2.082 | 1.2e-4 |
| l96_5 | 0.473576 | 0.0077 | 2.909 | 2.9e-6 |
| l96_6 | 0.946390 | 0.0078 | 4.036 | 3.5e-6 |
| l96_10 | 1.168334 | 0.0135 | 6.483 | 6.7e-6 |
| l96_20 | 1.553689 | 0.0148 | 13.472 | 1.3e-5 |

## 2.2 Trajectories, splits, seeds
Seed = block base + 100 × system index + stream. Block bases: calibration 10000, training 20000, validation 30000,
confirmation 40000, lyapunov 50000. System index: lorenz28 0, lorenz45 1, l96_5 2, l96_6 3, l96_10 4, l96_20 5.
- Calibration: 150 trajectories × 1,000 states every 0.1 tu = 150,000 states (codebooks, σ_A, D_eff, h).
- Training: 100 trajectories × 20 tu (2,000 tu), stored every dt. The data axis uses 1,000 × 20 tu (20,000 tu), of which the first 100 are the base set.
- Validation: 50 × 20 tu for checkpoint selection. A 300-state validation panel is used for the pre-Task-3 stall check only.
- Confirmation: 1,000 independent panel trajectories per system, each with 6.5 tu of history before t = 0 and W/λ + 0.2 tu after. The history panel (300) is the first 300.
Model seeds {0, 1, 2}. Seeds {3, 4} are added for A, B, D (4 and 6 bits) and C (both noise levels) at lorenz28, Δ = 0.02.
Bootstrap: 2,000 reps, seed 777. Whole states (independent trajectories) and model seeds are resampled.

## 2.3 Tokenizers
k-means on calibration states: n_init 1, max_iter 300, tol 1e-8, random_state = bits. Rates 4, 6, 8, 10 (attribution),
plus 5, 7, 9, 11, 12 (exchange law). Assignment is the exact nearest prototype. Scalar quantization: uniform bins per coordinate over
the calibration range, decoded to calibration cell means. Residual VQ: 8 bits per stage. These last two are used for bounds and references only.

## 2.4 Scoring
Error e_j = ‖x̂_j − x_j‖ / σ_A (σ_A = RMS distance of calibration states to their mean). ε = 0.3 is primary, 0.1 and 0.5 are reported.
Δ ∈ {0.02, 0.05, 0.1} on common physical trajectories (subsampled, no interpolation). H_W = E[min(λT, W)], W = 27,
with the non-crossing fraction reported. **Primary: future frames only (j ≥ 1).** Secondary: from t = 0, with the current-frame
output fixed per arm (A and B: the current token's prototype; D and A-probe: the reconstruction; C and E: the observed state;
references: their state estimate). p_0 is reported at every rate. Every comparison uses the same states, grid, start frame and window.

## 2.5 Bounds and references
- Output-support bound: d_C(x_t) on the true future; T_out = first frame with d_C > εσ_A; per-state strict outlast, ties reported.
- Single-frame decomposition: specified as in WO 2.5, known-zero threshold as amended below (Amendment 1).
- Decode-and-integrate; persistence; **climatology (added, gate check 7)**.
- Particle filter: 1,500 particles, context 3.2 tu, initialized from calibration members of the first observed cell, indicator
  likelihood, Gaussian fallback exp(−d²/δ_cell²) to the observed prototype (counted), systematic resampling, jitter 5% of
  per-coordinate spread. Sensitivity: 3,000 particles at 4 and 8 bits, Δ = 0.05. Fallback > 5% → rerun with 3,000; if still > 5%, the reference is labelled unreliable there.

## 2.6 Exchange law
D_eff = −1/slope(log2 δ against R) over {6, 8, 10, 12} on calibration states (interval: bootstrap over calibration trajectories).
h: 1,000 calibration states, error directions of the 1,024-code codebook, rescaled to δ ∈ logspace(−0.5, −4, 15)·σ_A, integrated
with the true system, H_W on the Δ = 0.02 grid (future frames, ε = 0.3), linear interpolation in ln δ. Saturation limit 5%.
Prediction H_W(R) = h(δ̂(R)), where δ̂(R) is the calibration RMS quantization error. Measured: decode-and-integrate on the 1,000-state
confirmation panel (Δ = 0.02, future frames, ε = 0.3). Held-out rates {5, 7, 9, 11}. **Criterion per rate:** |pred − meas| ≤
0.15·meas if meas ≥ 0.5, otherwise ≤ 0.075. "Predicts held-out rates" only if all four pass. Systems: lorenz28, lorenz45, l96_5, l96_6.
r for fresh codebook-direction, aligned (tangent evolved 10 tu) and isotropic errors, plus the classical FSLE. The fixed-slope
comparator of the blinded second author is reported beside the criterion, never in place of it.

## 2.7 Learned arms
Backbone: pre-LN causal transformer, 4 layers, width 128, 4 heads, FF 512, GELU, no dropout, learned positions. Context 3.3 tu
(166 / 66 / 33 frames). AdamW lr 3e-4, cosine decay, weight decay 0.01, batch 256. **Step budget 10,000** (pilot: 0.025 s/step at
Δ = 0.02 after moving batching to the GPU; the full grid projects to ≈ 7.5 GPU-hours, well under 24 h). Validation every 500 steps;
the best validation-loss checkpoint is used. Arms A, B, C (σ ∈ {0, 0.03}·σ_A per coordinate on training inputs), D, E and A-probes
(linear and MLP) are as in the WO table. Details are in `freeze.yaml: pins`. Grid as in WO 2.7 plus the extra seeds above.

## 2.8 Margins
Differences in restricted-mean λ·VPT on the primary score, with paired bootstrap. Approximately equal: 90% CI within ±0.10.
Well below: difference ≥ 0.25 and the 95% CI excludes 0. Near: upper 95% limit of (reference − model) ≤ 0.15. A non-significant difference is not equivalence.

## Readings and stop conditions
WO §4 and §5 verbatim apply. Labels: bound, reference, learned, estimate.

## Amendment 1 (2026-09-24): known-zero threshold

**Error stated.** The WO's known-zero threshold O(0) < 1e-10·I(0) was an authoring error: the preliminary reference
table already shows O(0)/I(0) = 1.8e-9 at 4 bits under the same k-means settings (n_init 1, max_iter 300, tol 1e-8),
so the test could not pass at 4 bits with the frozen tokenizer. Under the original threshold the test failed at 4 bits
on the frozen calibration codebooks (plug-in O(0)/I(0) = 8.6e-10; 6, 8, 10 bits about 3e-28) and the decomposition was
not run (freeze `f750ca1`, gate/GATE_REPORT.md).

**Amendment** (directed by Todd): the threshold becomes **O(0) < 1e-6·I(0)**, plug-in O on all members. The k-means
settings and every codebook are unchanged. The decomposition (Task 2.3, F3) runs under the amended threshold; both
the original failure and the amended result are reported.
