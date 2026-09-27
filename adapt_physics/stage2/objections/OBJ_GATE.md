# Objections and edge timing WO: spec integrity gate

- **Work order:** "WO: Adapt the Physics, objections and edge timing" (WO_Adapt-The-Physics-Drifting-Discrepancy-2026-09-27).
- **When:** run by the executing agent after stage-2 part B completed and was exported, and before the objections
  freeze, any World V data and any Part 2 evaluation.
- **Template:** T_Spec-Integrity-Gate, checks 1–9 including 5a.

## Summary

| Part | Outcome | Action |
|---|---|---|
| Part 1 readings (holds / degrades / loses its lead) | two-sided (check 1) | executed |
| Part 1 detector reading ("flags" if the 95% interval of H's slope excludes zero) | **nearly degenerate** (checks 1 and 6): there is no effect-size floor, and with 3 seeds × 300 states even a negligible slope excludes zero | executed as written. The slope magnitude and the implied change in Re across the window are reported beside the reading. |
| Part 2 claim reading | two-sided (check 1) | executed |
| Part 2 identification through the network | procedure unpinned (as the WO requires) | pinned in the freeze before any evaluation |
| Part 3 "datacenter value for the same arm" | referent unpinned (check 3): datacenter per-state costs come from batch-300 runs | pinned: the same harness at batch 1 on a Baccus GPU, with the batch-300 per-state costs cited beside |
| Part 3 "same code, FP32" | internal conflict: the datacenter solver arms run the oracle in float64 | pinned: the datacenter settings are kept (O float64; hybrid and networks float32) |
| Part 3 torch | the Orin has no torch wheel built for compute capability 8.7 | NVIDIA's JetPack 7 wheel is used (torch 2.11.0 + CUDA 13.0, running sm_80 kernels by binary compatibility); CPU-vs-GPU numerics were checked to machine precision; the datacenter runs torch 2.13.0. The horizon agreement check reports the effect. |
| Part 3 jetson_clocks | it cannot be enabled without sudo | recorded as off; the power mode is MAXN |
| Selectors (check 9) | not satisfied for the α(Re) form, the Re 50 cell and the arm set | results labelled selector-dependent |

## Pins

1. **World V.**
   - Drag follows viscosity: α(Re) = α₀·40/Re with α₀ = 0.0773273; α = 0.0618619 at Re 50.
   - Implementation: `KolmoDrag(..., alpha_ref_re=40)`. At Re 40 it is bit-identical to World D (checked).
   - Physical justification (the WO's, labelled a hypothesis, check 4): the linear drag in a laboratory Kolmogorov
     flow is bottom friction from a thin viscous layer, α ∝ ν. If Re drifts because ν drifts (temperature), the drag
     drifts with it.
2. **Streams never used before.**
   - World V Re 50 panel: test and noise stream 40.
   - L_range_V data: training and validation stream 3.
   - Chaos gate: Lyapunov streams 500 and 600.
3. **Seeds.**
   - H: World D seeds 0–2 (reused, not retrained). L0: seeds 0–2 (reused).
   - L_range_V: seed 0, plus seeds 1 and 2 if time allows (cut order 2).
   - L_param: seeds 1 and 2 are new, using the stage-1 recipe. L_param_C: seed 0.
4. **Windows.**
   - Part 1: H, P1x_V and H+true Re at w ∈ {3, 6, 11, 23}; the others at w = 11 (and ε 0.3).
   - Part 2: FNO-Re + true Re at w = 11. FNO-Re + identified Re at w ∈ {3, 6, 11, 23}.
5. **Identification through the network (FNO-Re + identified Re).**
   - The same golden-section search as H: Re ∈ [25, 80], exactly 30 evaluations, midpoint of the final bracket.
   - Misfit: the mean over scored frames of ‖x̂ − y‖²/σ_A², where x̂ is the network's autoregressive rollout at the
     candidate Re, and n_in = 4.
   - For w ≥ 5: the inputs are window frames 1..4, and frames 5..w are scored.
   - For w < 5 (only w = 3): the inputs are the 4 observed frames ending at frame 1 (frames −2..1, including
     pre-change frames), and frames 2..w are scored.
   - The forecast then runs from the 4 frames ending at k = w, at the identified Re.
6. **L_ft on fresh panels.** Stage-1 procedure: L0 seed 0 as the base; 200 AdamW steps at learning rate 1e-4 with
   weight decay 0, full batch. The w pairs have their target in the window, and the inputs may be earlier
   observations. Re 44, 50 and 56, all 300 states, w = 11.
7. **Estimator.** Stage-2 part A, unchanged: seed-pooled, with trajectories resampled and then seeds within each
   trajectory. Ratios and paired differences use the same resampling.
8. **Part 3.**
   - States 0–22 of the part A World D Re 50 fresh panel: 0–2 are warm-up, 3–22 are timed. Batch 1, w = 11.
   - Timing is CUDA-synchronized.
   - tegrastats is sampled every 100 ms, with each line timestamped on receipt.
   - Energy per state = mean VDD_IN over the arm's timed interval × mean wall time.
   - The datacenter comparison uses the same harness at batch 1 on a Baccus GPU.

## Checks

**1. Two-sided feasibility.** These are all stated before any objections result.

| Reading | Meets | Does not meet |
|---|---|---|
| Part 1 "holds" (H/O ≥ 0.85 and H/L_range ≥ 1.5) | the World D analogue: part A Re 50, H/O = 0.974 and H/L_range = 1.84 (cited, APSK) | H/L_range_V < 1.2 (hypothesis: the drag mismatch biases Re, as it did for P1 in stage 1) |
| Part 1 detector "flags" | part A World C, H slope −0.003 per frame with a 95% interval excluding 0 (cited) | a slope interval including 0 (hypothesis) |
| Part 2 claim, "H − (FNO-Re + true Re) ≥ 0.25, 95% interval above 0 at Re 50 and 56" | screening at Re 50: H 3.30 against L_param + true Re 2.33, a difference of 0.97 (stage 1, APH; cited) | FNO-Re + true Re within 0.25 of H at Re 56 (hypothesis; Re 56 was not in stage 1) |

**2. Independence.** World V and its panel are new. The Part 2 panels are the fresh part A panels; H's values there
were already known, but FNO-Re is new information.

**3. Referents.** Pinned above.

**4. Source class.**
- The α ∝ ν justification is a physical hypothesis, stated as the WO's.
- The 69%/98% screening numbers in the WO are single-seed screening values, not confirmations.

**5 and 5a.** Every input is cited or labelled a hypothesis.

**6. Surprise.**
- H's Re estimate staying unbiased in World V: the correction absorbs a fixed drag, so a 20% change should bias Re.
- FNO-Re + identified Re beating FNO-Re + true Re: the identification would then be compensating for the network's
  error.

**7. Null baseline.** L0 and the Part A persistence and P1 values are all available.

**8. Comparator separability.** L_range_V is the in-world opponent. L0 is reported beside it.

**9. Selector separation.** Not satisfied (authorship as above). Results are selector-dependent.

## Stops

None. The detector-reading degeneracy is reported, not stopped: it is a reported reading, not a criterion.
