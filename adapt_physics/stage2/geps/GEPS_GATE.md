# GEPS as a learned adaptive opponent: spec integrity gate

- **Work order:** "WO: Adapt the Physics, GEPS as a learned adaptive opponent", issued 2026-09-27.
- **When:** run by the executing agent before the GEPS freeze and before any test-panel evaluation. Training started
  first: the WO allows it, since its freeze requirement applies to test-panel evaluation. The recipe was already
  fixed in code at that point.
- **Template:** T_Spec-Integrity-Gate, checks 1–9 including 5a.

## Summary

| Part | Outcome | Action |
|---|---|---|
| Evaluation scope (300 states × 5 Re × two budgets) | **fails feasibility** | Stopped and reported to Todd. His ruling (2026-09-28) is in "Scope change" below. |
| "The published recipe for 2D Kolmogorov" | two unpinned referents (check 3), and paper and code disagree (check 4) | pinned below: paper Table 12 for the hyperparameters; the released code for the integrator |
| Reading ("does not close the gap") | two-sided (check 1) | executed as frozen, on the scoped panel |
| Selector (check 9) | GEPS was named by an external review of the draft, not by the WO author | the comparator is independently selected |

## Scope change (Todd's ruling, recorded)

- **Measured cost:** GEPS adaptation costs about 84–93 ms per state per adaptation step on a DGX Spark GB10. That
  is after an exactly equivalent reformulation of its low-rank layers (below), which roughly halved the cost from
  about 175 ms.
- **What the WO's scope needs:**
  - the never-cut minimum (500 and 5,000 adaptation steps at Re 50 and 56, 300 states): about 77 Spark-hours;
  - the full WO scope: about 5 times that.
- **What is available:** about 13 Spark-hours remained after the 8 h training cap and before the 15:00 UTC
  deadline.

Todd's ruling:
1. Evaluate on the first N states of the fresh World D panels at Re 50 and 56, with both budgets, plus the
   no-adaptation reference at Re 50.
2. Fit the contexts for many states in one batched pass, with the weights frozen and per-state losses **summed**.
3. N is the largest number of leading panel states, at least 50 and at most 300, for which that work finishes by
   14:30 UTC across both Sparks. It is set from a batched-throughput pilot on **training data**.
4. Keep the batch-1 per-state timing for the cost row.
5. Cut: Re 36/40/44, the GEPS-wide evaluation and the Spark H timing.
6. Follow-up (2026-09-28): the pilot rule gives N ≈ 42, below the floor, so **N = 50**. Todd accepted finishing after
   14:30 UTC at FP32 (projected: reading cells ~14:50, no-adaptation ~15:10, batch-1 timing ~15:40 UTC). The reading
   cells run first. GEPS-wide is retrained at lr 1e-3 after the published 1e-2 diverged (a deviation, in the freeze),
   and its evaluation stays cut, because the range budgets at N do not finish by 14:30.

**Exactness of the batching, checked:**
- GEPS's adaptation optimizer is Adam, which is elementwise.
- `adapt.py` has no gradient-norm clipping. `clip_grad_norm_` appears only in `train.py`.
- No layer couples samples (no batch norm), so each state's gradient depends only on its own loss.
- GEPS's ReduceLROnPlateau is a single global scheduler. Batching under it would couple the states' learning rates,
  so the wrapper keeps a per-state Adam and plateau schedule. That is identical to adapting each state alone.
- Empirical check on training data: 3 states adapted in one batch and each alone agree to 2.3e-7 relative after 60
  steps, i.e. float32 rounding.

## Spec errors and pins

1. **The published recipe is unpinned, and the paper and code disagree.**
   - The repository's launch scripts are templates with placeholders, and the Kolmogorov-specific values exist only
     in paper Table 12: context c = 4, depth 4, width 64, Swish, batch 4, 20,000 epochs, learning rate 1e-2, decay
     0.9, no teacher forcing; adaptation 500 epochs at learning rate 1e-2. These are used.
   - The paper says RK4 NeuralODE, but the released `Forecaster` hard-codes `method = 'euler'`. The released code
     is used, as the WO asks for the official implementation.
2. **The published trajectory length.** GEPS's Kolmogorov data are 20 frames per trajectory. Ours are 200-frame
   trajectories, so one 20-frame window per trajectory per epoch, with a random start, is the pinned mapping.
3. **The 8 h cap binds.** At about 1.2 s per step (batch 4, a 20-frame rollout), 8 h is about 24,000 steps, roughly
   95 epochs of 1,024 environments. The checkpoint is selected on validation loss (val_range, fixed 20-frame windows,
   evaluated with the mean training context, since the validation environments are unseen).
4. **Environments.** One per training trajectory, 1,024 in total. The code handles any number of codes, so no
   binning is needed.
5. **Adaptation data.** GEPS has a 1-frame input and adapts on trajectory rollouts. For each test state, the w = 11
   noisy post-change frames form one adaptation trajectory: a rollout from frame 1 with MSE over the 11 frames, as
   in `adapt.py`. The context starts at the mean training code.
6. **No-adaptation reference.** One shared context is fitted with the same procedure (500 steps) on 32 Re-40
   nominal trajectories × 11 frames, treated as one environment, and then used for every test state.
7. **Computationally equivalent reformulation** (`geps_fast.py`).
   - The low-rank layers are computed as f(x; W) + Σ_r c_r f(x; A_r ⊗ B_r) with standard kernels, instead of
     materializing a per-sample weight: the same parameters and names, and the same function.
   - Verified against the released layers: 1.2e-6, 2.0e-7 and 2.1e-7 relative for conv, linear and spectral.
   - The full-model 20-frame rollout agrees to 1.7e-7.
   - TF32 is disabled so that this holds (full FP32).
8. **Environment variable.** `TORCH_DISABLE_NATIVE_JIT=1` routes torch 2.13's Triton-JIT native ops to their ATen
   kernels, because the Sparks lack the Python headers Triton's build needs. There is no numerical change.
9. **Data mapping.** 64 × 64 vorticity scaled by 64/σ_A(Re 40, World D), with Δ = 0.35 (t = 0.35 k). Training uses
   the World D range set (Re U[34, 46], 1,024 × 200) and, for GEPS-wide, the Re 30–60 set. The initial frame gets 2%
   σ_A noise.
10. **Interval.** One seed, so trajectories are resampled only (the crossed scheme reduces to this).

## Checks

**1. Two-sided feasibility.**

| Reading | Holds (hypothesis) | Fails (hypothesis) |
|---|---|---|
| "At Re 50 and 56, H − GEPS-range (better budget) ≥ 0.25 with the 95% interval > 0" | GEPS behaves like the Re-conditioned FNO given the true Re. Cited analogue: H − (FNO-Re + true Re) = 1.04 at Re 50 and 1.60 at Re 56 (APFR-R) | GEPS's adapted context recovers the Re 50 dynamics to within 0.25 of H |

**2. Independence.** New model; the test panels were not used for any GEPS choice. N is chosen from a pilot on
training data only.

**3. Referents.** Pinned above.

**4. Source class.**
- Paper Table 12 is the authors' stated recipe.
- The integrator is taken from the code, because the WO specifies the official implementation.

**5 and 5a.** The inputs above are cited or labelled hypotheses.

**6. Surprise.** GEPS at the 10× budget matching H at Re 50.

**7. Null baseline.** The no-adaptation reference is present. The part A persistence and L0 values are also
available.

**8. Comparator separability.** The Part A values of L_range, L_range-wide and FNO-Re are reported beside GEPS.

**9. Selector separation.** Satisfied for the comparator choice, since an external review named GEPS. The scope was
reduced by Todd's ruling before any test-panel data was touched.

## Stops

- The full evaluation scope stopped on feasibility; it was replaced by the ruling above.
- Nothing else stopped.
