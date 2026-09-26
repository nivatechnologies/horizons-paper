# Stage 2 (confirmation and robustness): spec integrity gate

- **Work order:** "WO: Adapt the Physics, stage 2 (confirmation and robustness)", issued 2026-09-26.
- **When:** run by the executing agent before the stage-2 freeze and before any fresh panel.
- **Template:** T_Spec-Integrity-Gate, checks 1–9 including 5a.
- **Criteria:** copied from the pivot WO **unchanged**, with the pivot gate's precedence KILL → PASS → MIDDLE. They
  are not re-derived here.

## Summary

| Part | Outcome | Action |
|---|---|---|
| Part A criteria | pass: copied unchanged; checks 1 and 8 were done in the pivot gate. Check 2 (independence) now passes: fresh panels and seeds, criteria written before them | executed |
| Seed-pooled estimator and "seeds resampled within each trajectory" | the referent is unpinned (check 3): which seeds and how resampled | pinned below |
| "Every criterion's value with its interval" | there is no interval for a ratio in the pivot; the estimator is unpinned | pinned: a percentile bootstrap of the ratio of means, with the same resampling as the paired differences |
| PASS "0.95 × max(L0, L0-big)" at Re 40 | L0-big has one seed (seed 0), L0 has three | pinned: seed-pooled L0 against seed-0 L0-big, as written |
| Part B items 1–7 | settings unpinned (check 3): seeds, Re values, arms, search details | pinned below, before any result |
| Windows on the fresh panels | the WO names w = 3 and 6 (item 5) and w = 11 (part A); w = 23 is not named | pinned: w ∈ {3, 6, 11} for every arm. The pivot's w = 23 is not repeated, because it is the costliest cell (22 misfit frames × 30 evaluations × 3 seeds per Re and world). The detector slope therefore uses three points. |
| Selectors (check 9) | the part B ranges and sizes (Re 30–60, 5% noise, amplitude ±10%, straddle offsets) were authored by the WO author | not satisfied; part B is labelled selector-dependent. The mismatch term remains Codex's. |

## Pins (spec errors or omissions in the WO)

1. **Seed-pooled estimator.** Seeds 0, 1 and 2 for H, L_range and L0 in each world.
   - **Point value:** a per-state mean over seeds, then the mean over states.
   - **Bootstrap:** 2,000 reps with seed 777. Resample the 300 trajectories; then, within each resampled trajectory,
     resample that arm's seeds with replacement.
   - **Differences and ratios:** each arm is resampled independently within the same trajectory.
   - **Single-seed arms** (O, P1, P1x, persistence, L0-big) have one value per state.
2. **Criterion intervals.** A 95% percentile interval of each ratio of means under the resampling above. The
   criterion itself uses the point ratio, as in the pivot.
3. **Seeds for training.** Seed s sets both `torch.manual_seed(s)` and the batch-sampling generator
   `default_rng(s)`. The validation windows are unchanged, and seed 0 is the existing model. There are no other
   differences.
4. **Fresh streams.** Test and noise streams are the pivot stream + 20:
   - World D: 20, 22, 23, 24, 25 for Re 36, 40, 44, 50, 56.
   - World C: 30, 32, 33, 34, 35.
   - Two-parameter panels: 26 and 27.
   - 5%-noise observations: the test stream + 50.
   - Wide-range training data: training and validation stream 2 in D and 12 in C.
   None of these streams has been used before.
5. **Part B seeds.**
   - Items 2, 3 and 4 use seed 0 of H and L_range (single-seed, labelled).
   - Items 5, 6 and 7 reuse the part A evaluations (all seeds).
   - Item 1 is one seed, as the WO says.
6. **Item 2 (windows straddling the change).**
   - Re 44 and 50 in both worlds.
   - The 11-frame window ends 8, 5 or 2 frames after t_c, i.e. it starts 3, 6 or 9 frames before.
   - H identifies Re on those 11 frames with the same search.
   - H and L_range forecast from the last frame of the window.
7. **Item 3 (two parameters).**
   - World D only. The truth changes Re and the forcing amplitude A at t_c.
   - The chaos gate and σ_A are measured for each case.
   - H identifies (Re, A) per state by Nelder–Mead:
     - start (40, 1.0); initial simplex steps +5 in Re and +0.1 in A;
     - coefficients: reflection 1, expansion 2, contraction 0.5, shrink 0.5;
     - exactly 60 objective evaluations, with the same misfit as the Re search;
     - parameters clipped to Re ∈ [25, 80] and A ∈ [0.5, 1.5];
     - the estimate is the best vertex after 60 evaluations.
   - A diagnostic **H_Re_only** identifies Re alone (with A fixed at 1) by the usual search.
   - Arms: O (true Re and A), L_range (not retrained), H, H_Re_only.
8. **Item 4 (noisier sensors).** 5% noise at Re 44 and 50 in both worlds. Arms: O, H (seed 0), L_range (seed 0).
9. **Item 7 correlation.** In World C, the Spearman correlation per state between H's identified-Re slope
   (seed-averaged, w = 3, 6, 11) and H's shortfall from the oracle (O − H at w = 11, ε = 0.1, seed-averaged). A 95%
   interval comes from bootstrapping over trajectories. Reported for every Re.
10. **"Training conditions" for item 1.** L_range-wide has 1,024 trajectories, each with its own Re in [30, 60], and
    204,800 states. The pivot count is 1,024 for L_range (range 34–46) and 1 for H.

## Checks

**1. Two-sided feasibility.** Part A inherits the pivot gate. The screening values are the passing input, and are
cited: H/O ≥ 0.92 in D and ≥ 0.82 in C at the criterion Re (pivot NUMBERS APVK). The failing input (hypothesis): seed
variance of the H correction collapses one seed at Re 56 in World C, taking H/O below 0.70.

**2. Independence.** Satisfied for part A: the panels and seeds are fresh, and the criteria were fixed before them.

**3. Referents.** Pinned above.

**4. Source class.** The screening values are single-seed screening estimates. Stage 2 confirms them; it does not
tune.

**5 and 5a.** Every input is cited or labelled a hypothesis.

**6. Surprise.**
- Seeds 1 and 2 of H could learn a correction that biases Re (the detector would show it).
- L_range-wide could match H at Re 56 inside its range. That is the likely reader outcome, and it would bound the
  headline.

**7. Null baseline.** Persistence, P1 and L0 are all present.

**8. Comparator separability.** L_range and L_range-wide are reported separately.

**9. Selector separation.** Not satisfied for part B. The results are labelled selector-dependent.

## Stops

None.
