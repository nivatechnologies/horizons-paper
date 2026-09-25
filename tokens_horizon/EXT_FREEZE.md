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
