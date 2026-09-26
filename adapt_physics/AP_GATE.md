# Adapt the Physics, stage 1: spec integrity gate

- **Work order:** "WO: Adapt the Physics kill test (stage 1)", issued 2026-09-26, with the contract
  P_Paper-Adapt-The-Physics-2026-09.
- **Template:** T_Spec-Integrity-Gate, checks 1–9 including 5a.
- **When:** run by the executing agent before the freeze and before any test panel existed.
- **Labels:** "cited" means the source is given. "Hypothesis" means a constructed value under test (check 5a).

## Summary

| Part | Outcome | Action |
|---|---|---|
| Systems, drag, drift, observations, Kolmogorov arms | pass once pinned (checks 3 and 4) | pinned in `ap_freeze.yaml` |
| Readings (well below, approximately equal) | pass (frozen margins from the tokens-horizon freeze) | executed |
| Kill rule | passes check 1, but its panel is unpinned (check 3). L_ft runs on 100 states and the other arms on 300 | pinned: the kill rule is evaluated on the first 100 states of each panel, where every arm is present; the 300-state values are reported beside it |
| "Unannounced" change against a window defined from t_c | referent unpinned (check 3) | pinned (item 2 below) |
| L_ft "one-step pairs inside the window" | degenerate for w ≤ 4 with a 4-frame input (check 1: zero pairs at w = 3) | pinned: the target frame lies in the window, and the inputs may be earlier observations |
| **Lorenz-63 mechanism part** | **fails check 3**: its arms and measurement are not specified; only the models and ρ values are | **not executed.** It is also first in the cut order. |
| Selectors (drift sizes, arms, architectures, windows) | check 9 not satisfied | reported; results labelled selector-dependent |

## Spec errors and pins

1. **The Lorenz-63 part is unspecified.** "The existing continuous-state models C trained at ρ = 28" plus three test
   ρ values do not define an arm set, an adaptation procedure or a score. It is cut, first in the cut order, and the
   failure is reported here.
2. **"Unannounced" is unpinned.** The window is defined as "w frames after t_c", so an arm that uses exactly the
   window knows where it starts. Pins:
   - t_c falls uniformly inside the observation interval after frame k = 0 (t_c = t_0 + u·0.35, u ~ U(0, 1) per
     trajectory, rounded to the 0.01 step). Frame 1 therefore mixes pre- and post-change dynamics.
   - Arms are told neither the new Re nor t_c inside the interval.
   - P1, P1x and L_ft use frames 1..w.
   - L_range and L0 use their last n_in observed frames, which include pre-change frames when w < n_in.
3. **Kill-rule panel.** L_ft runs on the first 100 states, the others on 300, so I\* and A\* as written would
   compare means over different states. Pin: I\*, A\* and every kill ratio use the first 100 states. The 300-state
   ratios (A\* without L_ft) are reported beside them.
4. **L_ft pairs.** With a 4-frame input, "one-step pairs inside the window" gives w − 4 pairs: none at w = 3 and 2 at
   w = 6. Pin: the pairs are the w one-step pairs whose **target** is a window frame; input frames may be earlier
   observations. The targets are the noisy observations, since the arm never sees truth.
5. **Drag calibration.** "Drag carries 15% of total enstrophy dissipation" is pinned as α⟨ω²⟩ / (α⟨ω²⟩ +
   Re⁻¹⟨|∇ω|²⟩) = 0.15. This is time- and ensemble-averaged at Re 40 on the calibration block (64 trajectories,
   300-tu burn-in, 300-tu average), solved by secant iteration to ±0.002.
6. **Noise scale.** "2% σ_A RMS" is pinned as white noise with Euclidean norm 0.02 σ_A(test Re) in RMS over the
   4,096 grid values, on every observed frame of the panel (pre- and post-change).
7. **FNO details.**
   - Modes: 16 × 16, kept in both ky half-planes.
   - Inputs: 4 frames for L0, L0-big and L_param (the WO does not give L_param's input count); 8 frames for L_range.
   - Channels: periodic coordinates; a Re channel, (Re − 40)/6, for L_param only.
   - Residual output.
   - L0-big: width 156, 99.8 M parameters against 16.8 M, which is 5.94×.
   - Training data, step budgets, optimizer, input-noise augmentation and validation are pinned in the freeze. The
     WO fixes none of them.
8. **Identification objective.** The model is started from the projected first window frame. The misfit is the mean
   of ‖x_model(k) − y_k‖²/σ_A² over frames 2..w. The estimate is the midpoint of the final golden-section bracket
   after exactly 30 evaluations.
9. **"Time to 90% of oracle"** is defined only on the tested grid w ∈ {3, 6, 11, 23}. If no tested w reaches it, the
   result is "not reached".
10. **The flag referent.** "As large as" is pinned as I\*/A\* at Re 40 ≥ I\*/A\* at Re 44 (100-state panel,
    primary cell).
11. **The kill rule has no uncertainty term.** It is a ratio of restricted means. Paired differences with bootstrap
    intervals are reported beside it, and the rule itself is applied as written.

## Checks

**1. Two-sided feasibility.** All inputs below are hypotheses under test unless cited.

The anchor for the oracle's scale is cited: tokens-horizon EXT2, NUMBERS K3D. Decode-and-integrate from a 0.0245σ_A
initial error on Kolmogorov Re 40 (no drag) lasts 1.83 Lyapunov times at ε = 0.1. The oracle here starts from about
0.02σ_A of projected noise, so O ≈ 1.5–2 is expected. A 2× ratio therefore needs A\* ≲ 1 while I\* stays near O.

| Condition | Passing input (hypothesis) | Failing input (hypothesis) |
|---|---|---|
| Kill-rule pass | I\* = 1.6, A\* = 0.6 at Re 44 and I\* = 1.5, A\* = 0.5 at Re 50 | I\* = 1.6, A\* = 1.3 at Re 44 (A\* ≥ 0.75 I\*, so kill) |
| In between | I\* = 1.6, A\* = 1.0 | as above |
| Flag | ratio 2.5 at Re 40 against 3 at Re 44 (no flag) | ratio 3 at Re 40 against 3 at Re 44 (flag) |
| Chaos gate | λ 95% interval above 0 (cited: Re 40 without drag, λ = 0.1268 ± 0.0008, tokens-horizon KSYS) | λ interval including 0 at Re 36 with drag (hypothesis; drag stabilizes) |
| Well below / approximately equal | frozen tokens-horizon margins with cited examples: NUMBERS K3D, KKE3 | same |

**2. Independence.** The test consumes post-change observations and truth trajectories that were not used for any
design choice. Drift sizes, windows and arms were fixed in the WO before any data existed. It passes.

**3. Referents.** It fails for the Lorenz-63 part (item 1), which is cut. The items above are pinned. The object of
the kill rule is the ratio of 100-state restricted means (Lyapunov times of the test system) at Re 44, ε = 0.1σ_A
(test system) and w = 11.

**4. Source class.**
- The drift sizes and the "0.5 Lyapunov time" window are design choices.
- w = 11 is 0.49 Lyapunov times at the no-drag λ of 0.1268. With drag, λ(Re 40) is measured and the w-to-Lyapunov
  mapping is reported.
- The external-review dispositions are revisions, not evidence.
- The prior-work items in the contract are cited as existence claims only.

**5. No example as definition.** No worked example carries a definition. The contract's headline sentence is marked
as a target, not a result.

**5a.** Every passing and failing input above is labelled as a hypothesis or cited.

**6. Surprise.**
- It would surprise the author if L_range, the in-range history-conditioned FNO, reached at least 0.75 I\* at Re 44.
  That is the kill outcome.
- It would also surprise the author if drag mismatch made P1 worse than P0 or than persistence.
- A third surprise would be L0-big recovering the drift.

**7. Null baseline.** Persistence, P0 (the nominal solver) and L0 (the frozen nominal FNO) are all present.

**8. Comparator separability.** A\* is the best of three opponents. Each is reported separately with 95% intervals,
and the paired differences between the top two are reported.

**9. Selector separation.**

| Selector | Author |
|---|---|
| Drift sizes, windows, arm set, FNO architecture | Todd and Claude (chat), revised against an external GPT review. A review revises a selector; it is not a competing selector. |
| Exact FNO widths, data sizes and budgets | the executing agent, frozen before any test panel |

Check 9 is **not satisfied**: there is no second-author selector and no three framings. Results are labelled
**selector-dependent**. A kill or a pass holds for this arm set, architecture family and these budgets only.

## Stops

- The Lorenz-63 mechanism part is not executed.
- Everything else executes under the pins above.
