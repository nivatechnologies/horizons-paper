---
amends: WO_AIConf-Tokens-Horizon-Extension-2026-09-25
created: '2026-09-25'
status: issued
tags:
  - work-order
  - aiconf-papers
  - tokens-horizon
  - paper
title: 'WO amendment 1: Tokens-horizon extension'
type: work-order-amendment
---

# Amendment 1 to the tokens-horizon extension WO

Apply before producing any further extension result. If a result already produced conflicts with an item below, keep it, label it superseded, and rerun under the amendment. Commit this amendment into EXT_FREEZE as its own commit, stating what changed and why.

## A1. Exact support distance only (mathematical validity)
The output-support bound needs the exact distance from the true state to the nearest representable output, or a certified lower bound on it. Encoder round-trip error ‖x − D(E(x))‖ is an upper bound on that distance, so it can never certify a bound. Counterexample: residual stages C1 = {0, 2}, C2 = {0, 3} and target x = 3. Greedy encoding gives 2 + 0 (error 1), while 0 + 3 represents x exactly.
- Residual-VQ rows report distortion, decode-and-integrate and persistence only. **They report no bound.**
- Every nearest-code search used for a bound is exact (brute force). No approximate indexes (IVF, HNSW, PQ). Approximate methods are fine only for fitting codebooks.
- No bound is reported for any neural or convolutional decoder. Round-trip error, if reported at all, is labelled "context, not a bound".

## A2. Output contract
In EXT_FREEZE, name the exact scored field and every preprocessing step (for example mean-mode handling). Nothing is applied between patch concatenation and scoring: no spectral filtering, projection, dealiasing or mean correction. If a step is unavoidable, compute the bound for the post-processed support or report no bound. A must remain codebook-valued after every step applied before scoring.

## A3. Wording and rate accounting
- Describe the patch family as "spatially distributed tokenization at practical per-token vocabulary sizes, with an exactly analyzable product decoder". Do not describe it as "the way image and video tokenizers do it".
- Report nominal bits per frame (P·b) everywhere.
- Fit D_eff separately for each patch count P. It estimates P·d_patch for that factorization, not the attractor dimension. Never pool different P into one slope.
- Thresholds are "the smallest tested rate for this tokenizer family", not minimum bit requirements. Freeze how non-monotonic crossings and "not reached within the tested grid" are reported.

## A4. Survival, not only means
For every bound row, also report the fraction of states whose support survives through 1, 3 and 10 Lyapunov times, P(T_out ≥ t). The threshold table carries survival fractions next to the restricted means.

## A5. Calibration adequacy for large codebooks
- Aim for at least 50 calibration samples per code, or state the achieved number.
- Report fitting and held-out distortion, held-out code occupancy and the unused-code rate.
- At the two largest b, report how distortion and the bound change when the calibration set is halved.
- For shared patch codebooks, report the patch count and the number of independent trajectories separately.

## A6. E4 selection rule
Freeze the selection algorithm, not only its result.
- Evaluate candidates on the **validation** block, never on confirmation.
- Selection rule: the smallest-bits configuration with ≥ 2^10 codes per token and ≥ 16 tokens per frame whose validation-panel mean bound is below 1 Lyapunov time.
- Also train one nearby non-binding configuration as a contrast.
- **No qualifying cell** means the result is the representability map and no learned cell. Do not change domain size, patching or tolerance to find a binding case. "No tested practical configuration was support-limited at this tolerance" is a valid result.
- A mean bound below 1 marks a potentially support-limited configuration. Whether the learner actually saturates it is assessed afterwards, using the tie and ratio statistics.

## A7. E4 normalization and model contract
- Context is about 3 Lyapunov times. At λ ≈ 0.045 that is about 66 time units, not 3.3. State training-data length and step budget in Lyapunov times as well as in physical time and samples.
- Freeze the spatial-temporal input contract in EXT_FREEZE. Recommended: each frame's patch tokens form one step, with patch-position and time embeddings, causal in time and full attention within a frame.
- Use **one shared categorical head across patch positions**, conditioned by patch-position embedding, not one head per patch. At 16 patches × 1,024 classes × width 128, per-patch heads alone would exceed the backbone.
- Report adapter, backbone and head parameters, and training compute, separately for A, B and C.

## A8. Controls added to E5 (Lorenz-63, existing models, no retraining)
1. **B scored after snapping:** score B's existing rollouts a second time with each output snapped to its nearest prototype (the same rollout and the same fed-back codes). Report this next to B and the bound. This isolates the scored output from everything else B changes.
2. **Ties:** replace "A's tie rate excluding p_0 states" with P(VPT_A = T_out | T_out > Δ). Also report the share of states with T_out = Δ, where a tie is automatic under future-only scoring. Do the same for persistence and the random-code forecaster.
3. **Same-panel headline:** the means of the bound, A, B, C and D on the first 300 states (the particle-filter panel), with paired differences to the particle filter on that panel.
4. **Protocol facts into NUMBERS:** the number of trajectories in the confirmation block, their lengths, the spacing between starts, and the bootstrap resampling unit.
5. **Probe-control reading:** if the trained-A probe beats the untrained-A probe, the paper may say only that "training makes the precision more recoverable by the tested readout". It may not say the untrained representation lacks it.

## A9. A predictive test of the exchange rate (KS L = 22, whole-state k-means)
Compute decode-and-integrate at the even rates {6, 8, 10, 12} first. Fit the slope and commit the predicted horizons for the odd rates {7, 9, 11}. Only then compute the odd rates and report the prediction errors. This is the only predictive claim the slope form can make.

## A10. Revised cut order
1. The Kolmogorov 16×16-patch rows.
2. The larger-model control (E5.3).
3. The rest of the Kolmogorov family.

Never cut: E0, E1–E3 on KS, E4 if a qualifying cell exists, E5.1, E5.2, A8 and A9.

## A11. Number provenance
make_numbers.py fails on duplicate IDs and on unresolved lookups instead of silently picking one occurrence.
