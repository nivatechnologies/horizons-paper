
## EXT2 session review: learned-tokenizer kill test (2026-09-26)

**Spec errors found in the WO.** These come from the gate report `ext2/EXT2_GATE.md`, run before the freeze.

1. **The kill-criterion referent is unpinned (gate check 3).** "At least 2^10 codes per token" excludes both b10
   configurations: [8,5,5,5] gives 1,000 codes, and 1,000 < 1,024. The literal eligible set is {L8-b12, L8-b16,
   L16-b12}. The nominal set, reading b10 as the FSQ paper's approximate 2^10, is all five.

   The executor did not issue the verdict. It reports R1 under both sets, and both sets give the same answer (see the
   results note).
2. **Under the literal set, the k-means analogue of the kill test already fails R1 everywhere (checks 1 and 6).**
   From KKE3 at ε 0.1, Δ 0.35, future frames:
   - 8x8 b12: difference 0.207, below the 0.25 margin;
   - 8x8 b16: ceiling 1.133, above DI 0.782;
   - 16x16 b12: ceiling 2.555, above DI 1.433.

   Only 16x16 b10 passes R1, with ceiling 0.0445 against DI 1.056.
3. **The premise in "Why" is partly false (check 4).** "At 0.1σ no decodable frame is within tolerance" holds only
   at the low-bit end of each layout. KKE3 gives p₀ = 0.37 at 8x8 b16, 0.217 at 16x16 b12 and 0.048 at 16x16 b16,
   and in those rows the ceiling lies above DI.
4. **There were no Kolmogorov training or validation blocks.** They were generated under the frozen seed scheme:
   training seed 20800 (204,800 states, 256 trajectories) and validation seed 30800 (6,400 states, 64 trajectories).
5. **R2's "or above it" was unpinned.** Pinned as: the upper 95% limit of (DI − T_pt) is below 0.
6. **Architecture, loss scale, optimizer constants and the divergence rule were not specified.** They were pinned in
   the freeze before training.
7. **The figure ID "F8" collides** with the existing `figures/F8_controls`. The new figure was issued as F9.
8. **The figure's ε was unpinned.** F7 is drawn at ε 0.3; F9 shows ε 0.1 and 0.3.
9. **The FSQ paper's appendix listing** writes `tan(offset/half_l)` for the bound shift. Arctanh is what was
   intended, and arctanh is what was used.

**Process notes.**
- **Order of work:**
  - freeze commit `9f12064`;
  - timing pilot of 300 steps (L8-b12), not used;
  - measurement smoke test on the pilot checkpoint, written to scratch and not used.
- **Execution slip:** the first launch line backgrounded the whole `&&` chain, so two training queues started
  without their variables and exited immediately. They were relaunched within a minute; no run was affected.
- **Analysis bug:** a filter-order error in the analysis script (it read train info before checking that the file
  existed) was fixed before any result was written.
- **Divergence:** none of the five runs diverged, so the lr 1e-4 fallback was never used.
- **Checkpoints:** every selected checkpoint is the last one (step 30,000), so validation loss was still falling when
  the budget ran out. Longer training would be expected to lower reconstruction error further, but this was not
  tested. The readings are therefore conditional on the frozen 30,000-step budget.
- **Timing:** training took 60 to 80 min per config, slowed by sharing the GPUs with the measurement runs.
  Measurement took about 1 to 2 h per config.
- **Restart:** the Qwen vLLM services were restarted after the GPU work, and all three /health endpoints returned
  200.
- **Scope:** one tokenizer family, one architecture, one seed and one budget. Check 9 was not satisfied by a
  second author. The result is one negative for "learned tokenizers bind at tight tolerance", not a general one.
