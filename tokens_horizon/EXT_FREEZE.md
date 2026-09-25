# EXT_FREEZE: post-freeze extension (realistic vocabularies, physical systems, reviewer controls)

Everything under this file is a **post-freeze extension**. The original freeze (`FREEZE.md`, `f750ca1`; Amendment 1
`747a8c7`) is untouched, and no original NUMBERS.md ID changes. The one exception is the WO's item E0.1, the
duplicate `DDI` section, now `DDH`. `ext_freeze.yaml` is the machine-readable twin.

**Staging.** This file is committed in two parts, each before any result it governs:
- **Part 1:** general rules, the E5 reviewer controls on Lorenz-63, the readings and the spec-gate notes.
- **Part 2:** Kuramoto–Sivashinsky, Kolmogorov flow, tokenizer grids, the E3 grid and the E4 learned cell. It needs
  resolution and λ pilots, which measure system properties and produce no extension result, as Task 0 did for the
  original freeze.

A frozen extension value found to be wrong is fixed in a new commit that states the error.

## Part 1

### General
- **Scoring, margins, bootstrap and labels:** as in `freeze.yaml`.
- **NUMBERS.md sections:** extension rows go in **K** (systems, tokenizers, bounds) and **K2** (learned cells and
  controls), each labelled "post-freeze extension".

### E5 reviewer controls (Lorenz-63 ρ = 28; frozen blocks, codebooks and backbone unless stated)
1. **Probe control.**
   - Cells: 4 bits at Δ ∈ {0.02, 0.05, 0.1}, and 6 bits at Δ = 0.02. Seeds 0–2.
   - Untrained A: the identical architecture with the identical initial weights the trained A of that seed started from.
   - Linear and MLP probes on each, under the frozen probe protocol.
   - A token-history baseline: an MLP on the one-hot tokens of the last k frames, with k = the frozen context length for that Δ.
   - Reported beside the trained-A probe: reconstruction RMSE/σ_A, and the decode-and-integrate horizon of the reconstruction on the 1,000 confirmation states.
2. **Tie baselines.**
   - Cells: 4 bits, all three Δ.
   - Measured: the tie rate with the output-support bound (future frames, ε 0.3) for persistence and for a random-code forecaster. The random-code forecaster draws an independent uniform codeword every frame; 5 draws are averaged, with fixed seeds.
   - Also reported: A's tie rate over all states, and excluding p_0 states (d_C(x_0) > εσ_A).
3. **Larger and longer model.**
   - Arms: A and B at 4 and 10 bits, plus C (σ = 0); Δ = 0.05; 3 seeds.
   - Backbone: 6 layers, width 256, 4 heads, feed-forward 1024.
   - Steps: 40,000, which is 4× the budget. Otherwise the frozen optimizer and validation-loss selection.
   - Paired with the frozen-size cells.

### Readings (WO §6)
- **Bounds (descriptive only).** Two statements are allowed:
  - The smallest total bits per frame at which the bound's restricted mean exceeds 1, 3 and 10 Lyapunov times, with bootstrap intervals.
  - Whether the bound falls below 1 Lyapunov time at any configuration with ≥ 2^12 codes per token and ≥ 64 tokens per frame (yes or no, with the configuration).
- **Learned cells:** the frozen margins.
- **Probe control:** "training put the precision in A's hidden state" may be said only if two conditions both hold:
  - the untrained-A probe is well below the trained-A probe on horizon, under the frozen margin;
  - the untrained-A probe is worse on reconstruction in every seed.

  Otherwise the paper says only that the hidden state holds the precision.

### Spec-gate notes on this WO (checks 1–9 and 5a, abbreviated)
- **Check 1: two-sided feasibility.**
  - The probe-control reading can come out either way:
    - **Passes** if an untrained transformer's hidden state carries little of the state. **[hypothesis]**
    - **Fails** if random features of a 166-frame token history already localize it. **[hypothesis]** This is plausible: the frozen MLP probe of trained A reaches 0.08 σ_A.
  - The "≥ 2^12 codes and ≥ 64 tokens" bound reading can be answered only by Kolmogorov 8×8 or 16×16 patches, because KS uses P ≤ 32. If Kolmogorov is stopped or cut, the answer is "not determinable", not "no".
- **Check 3: referents.**
  - "Random-code forecaster" and "tie rate excluding p_0" are pinned above.
  - The "A factorized over patches" design is pinned in part 2.
- **Check 7: null baseline.** Persistence, and the new random-code forecaster, which is a second null.
- **Check 9: selector.** The WO's author chose Kuramoto–Sivashinsky L = 22. The blinded second author proposed the same system independently in the original gate (`gate/check9_blinded_selector_codex.md`), which is overlap. Kolmogorov flow was chosen by one author only, so it is labelled selector-dependent.
- **Errors in the WO:** see part 2 and the session review.

## Amendment 1 (2026-09-25)

Source: the vault note `02-Projects/WO_AIConf-Tokens-Horizon-Extension-Amendment-1-2026-09-25.md`, read from Drive
(6,661 bytes, md5 4f1d4cd429ff59e958a49b122e53690b). Copied verbatim to `gate/ext_amendment1_verbatim.md`. Where the
two differ, it governs over part 1 above. It was applied before any further extension result.

### What changed and why
- **A1 (validity).** A bound needs the exact support distance, or a certified lower bound on it. An encoder round-trip
  error is an upper bound and cannot certify a bound. Consequences:
  - Residual-VQ rows report no bound.
  - Neural or convolutional decoders get no bound.
  - Nearest-code searches used for a bound are exact brute force, with no approximate index.

  Executor pin on `th/patchvq.py`:
  - The float32 GPU brute force is certified. The float64 distances of the float32 top-k candidates are checked
    against a rigorous float32 rounding margin; any row not certified is recomputed by float64 brute force over all
    codes on the CPU.
  - The code-neighbour candidate set is used only to *certify non-crossing*. If UB = Σ_p min over a candidate subset
    is ≤ T², then d_C² ≤ UB ≤ T². This is exact logic in the valid direction.
  - A crossing is only ever declared from an exact brute-force d_C. No reported d_C and no crossing comes from an
    approximate search.
- **A2 (output contract).** Scored fields are pinned in part 2.
  - KS: the real-space field u on the N-point grid.
  - Kolmogorov: the vorticity field on the N×N grid.
  - The decoded state is the concatenation of decoded patches, scored as is, with no filtering, projection,
    dealiasing or mean correction.
  - A's outputs are decoded prototypes, so codebook-valued.
  - The decode-and-integrate reference is not a bound. Its integrator's own Galerkin projection applies only to the
    reference trajectory, and this is stated where it is reported.
- **A3 (wording and rates).**
  - The patch family is described as "spatially distributed tokenization at practical per-token vocabulary sizes,
    with an exactly analyzable product decoder".
  - Rates are nominal P·b bits per frame.
  - D_eff is fitted separately for each P.
  - Threshold reporting is frozen as follows. For each tokenizer family and threshold (1, 3, 10 Lyapunov times) we
    report three things: the smallest tested nominal rate whose restricted mean reaches the threshold; whether every
    higher tested rate in that family also reaches it (a "monotone" flag, with any exceptions listed); and the
    smallest tested rate whose lower 95% bootstrap limit reaches it.
  - If no tested rate reaches the threshold, we report "not reached within the tested grid".
  - These are "the smallest tested rate for this tokenizer family", never minimum bit requirements.
- **A4.** Every bound row also reports the survival fractions P(T_out ≥ t) for t = 1, 3, 10 Lyapunov times.
- **A5 (calibration).**
  - Target ≥ 50 calibration samples per code, or report the achieved number.
  - Report fitting and held-out distortion, held-out occupancy and the unused-code rate.
  - Halve the calibration set at the two largest b.
  - For patch codebooks, report patches and independent trajectories separately.
  - Sizes are frozen in part 2.
- **A6, A7 (E4).** Frozen in part 2:
  - Selection runs on the validation block only, with the smallest-bits rule given in the amendment and one
    non-binding contrast.
  - "No qualifying cell" is a valid result.
  - Context is about 3 Lyapunov times.
  - Frame-as-step input with patch-position and time embeddings.
  - One shared categorical head across patch positions.
  - Parameters and compute are reported per arm.
- **A8 (E5 additions).** These supersede the part-1 tie item and extend the controls.
  1. B's existing rollouts are re-scored with each output snapped to its nearest prototype, using the same rollout
     and the same fed-back codes.
  2. Ties become P(VPT = T_out | T_out > Δ), plus the share of states with T_out = Δ, for A, persistence and the
     random-code forecaster.
  3. Same-panel headline: the means of the bound, A, B, C and D on the first 300 states, with paired differences to
     the particle filter.
  4. Protocol facts go into NUMBERS.
  5. The probe-control reading becomes: "training makes the precision more recoverable by the tested readout" when
     the trained probe beats the untrained one. The paper never says the untrained representation lacks it.
- **A9.** Predictive test on KS L = 22 with whole-state k-means:
  1. Compute decode-and-integrate at 6, 8, 10 and 12 bits.
  2. Fit the slope and commit the predictions for 7, 9 and 11 bits.
  3. Only then compute the odd rates.
- **A10.** The cut order is now: Kolmogorov 16×16 patches, then E5.3, then the rest of Kolmogorov.
  Never cut: E0, E1–E3 on KS, E4 if a qualifying cell exists, E5.1, E5.2, A8 and A9.
- **A11.** `make_numbers.py` fails on duplicate IDs and on unresolved lookups.

### Results already produced that the amendment affects
- **Superseded:** `results/ext/e5_tie_baselines.csv` and the tie part of `results/ext/e5.json` (produced 04:37,
  before this amendment). They report A's tie rate excluding p_0 states, which A8.2 replaces. The files are kept
  with a SUPERSEDED marker and rerun under A8.2.
- **Reading superseded:** the E5.1 probe-control numbers (reconstruction RMSE, horizon) are unaffected. The reading
  sentence from part 1 is replaced by A8.5.
- **Unaffected:**
  - the E5.3 training (configuration unchanged; only its cut rank moves);
  - the KS and Kolmogorov pilots (system properties, not results);
  - the E0 fixes and figures;
  - every original-freeze result.
