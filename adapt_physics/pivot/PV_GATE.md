# Pivot kill test (physics plus learned correction): spec integrity gate

- **Work order:** "WO: Adapt the Physics, pivot kill test", issued 2026-09-26.
- **When:** run by the executing agent after step 0 (Codex, committed `5b6bdd1`, clarification `6f30a74`) and before
  the pivot freeze and any pivot test data.
- **Template:** T_Spec-Integrity-Gate, checks 1–9 including 5a.
- **Labels:** "cited" values come from stage-1 results (`adapt_physics/results/ap_rows.csv`, w = 11, ε = 0.1, 300
  states). "Hypothesis" marks a value under test.

## Summary

| Part | Outcome | Action |
|---|---|---|
| Step 0 (Codex mismatch term) | check 9 satisfied for the mismatch selector: blinded second author, no repo access | done; the answer is implemented as clarified |
| PASS / MIDDLE / KILL | two-sided (check 1). The categories overlap (a KILL can also meet MIDDLE) and the WO gives no precedence (check 3) | pinned: KILL is evaluated first, then PASS, then MIDDLE, else "otherwise" |
| World D criteria at Re 36/40/44/50 | independence is partial (check 2): the thresholds were written after the stage-1 values of O and L_range on these same panels were known | reported. The information the D test consumes is H, which is new. World C and Re 56 are fresh. |
| Hybrid H | pass once pinned | continuous-time correction (the solver is differentiable in torch); architecture, training and budget pinned in the freeze |
| Codex term magnitude | the clarified start (β_T = 3.35) changes η̄ by +40%, not 12.5% | tuned with the same sign to the clarified target (Codex's own procedure) |
| Other selectors | check 9 not satisfied (authorship below) | results labelled selector-dependent, except the mismatch term |

## Spec errors and pins

1. **The outcome categories overlap.**
   - Example: in World D with O/L_range = 1.9 (cited at Re 50: 3.37/1.76), H = 0.69·O gives H/L_range = 1.31. That
     meets MIDDLE's 1.3× and KILL's "below 70% of O at Re 50" at the same time.
   - Pin: KILL → PASS → MIDDLE → otherwise.
2. **Independence of the World D thresholds.** The 85%, 1.5× and 95% bars were set after the stage-1 numbers for
   O, L_range, L0 and L0-big on the same World D panels were known (the harvest note quotes them). What the test adds
   there is H alone. World C (new panels) and Re 56 (new) are fresh.
3. **"Training conditions" is unpinned.** Pin: the number of distinct Re values in the training data, plus the
   number of training states.
   - L0, L0-big and H: one condition (Re 40), 102,400 states.
   - L_range: 1,024 conditions (one Re per trajectory, Re ~ U[34, 46]), 204,800 states.
4. **P1's search range.** The WO widens the search to [25, 80] for H only. P1 and P1x keep the stage-1 range
   [25, 70], for continuity. Every test Re (≤ 56) lies inside both.
5. **"H is at least 95% of the best learned arm at Re 40"** applies in World D only, where L0-big exists. In World C
   there is no Re 40 criterion.
6. **Reuse.** World D at Re 36/40/44/50 reuses the stage-1 panels and stage-1 evaluations (O, P1, P1x, persistence,
   L0, L_range, L0-big). The code and inputs are identical, so recomputing would reproduce them exactly.
7. **The Codex magnitude.** Codex's clarified starting value gives +39.8% in η̄. Its own instruction is "tune around
   this setting until the change is 12.5%, chaotic dynamics persisting". The tuned value is recorded in the freeze.
   The one-time "ask for a smaller magnitude" message is reserved for a chaos-gate failure at Re 40, as the WO
   specifies.
8. **"Time to 90% of the oracle"** uses the tested grid w ∈ {3, 6, 11, 23}, as in stage 1.

## Checks

**1. Two-sided feasibility**, with the oracle ceiling checked (the stage-1 spec lesson).

The stage-1 World D values at w = 11, ε = 0.1 are cited:

| Re | O/L_range | Implied need for PASS |
|---|---|---|
| 36 | 2.82/1.46 = 1.94 | H ≥ 0.85·O gives H/L_range ≥ 1.65, so the 1.5× bar is reachable |
| 50 | 3.37/1.76 = 1.91 | same: ≥ 1.62 |
| 40 | 0.95 × max(L0, L0-big) = 0.95 × 3.04 = 2.88 | H ≥ 0.83·O(3.46) |
| 44 | — | only H ≥ 0.85·O is required |
| 56 | not yet known (hypothesis: the gap grows) | — |

| Case | Input | Status |
|---|---|---|
| PASS | H/O = 0.9 at every drifted Re in D; 0.75 in C with H/L_range ≥ 1.2 | hypothesis |
| KILL | H/L_range ≤ 1.0 at Re 50 in C | hypothesis |
| MIDDLE | H/O = 0.75 in D (≥ 1.3 L_range, below 85% O) | hypothesis |

**2. Independence.** Partial, as item 2 above. World C and Re 56 are fresh.

**3. Referents.** Pinned as above. The criteria are ratios of 300-state restricted means (Lyapunov times of the test
system) at w = 11, ε = 0.1. "H" means H with Re identified on the hybrid.

**4. Source class.**
- The Codex term is a plausible laboratory effect, with order-of-magnitude literature pointers. It is not a
  measurement of a specific apparatus.
- The stage-1 values are measured.
- The harvest note's interpretations are hypotheses.

**5. No example as definition.** None.

**5a.** Every input above is cited or labelled a hypothesis.

**6. Surprise.**
- The hybrid's correction, trained only at Re 40, could learn an Re-dependent discrepancy. The Re fit would then be
  biased again, as P1's was, and H would collapse under drift. The window-drift detector would show it.
- Also surprising would be L_range beating H inside its training range (Re 36 and 44).

**7. Null baseline.** Persistence, P1 (physics without correction) and L0 are all present.

**8. Comparator separability.** L_range is the named opponent and is the strongest learned drift arm in stage 1. In
World D, L0-big is reported beside it.

**9. Selector separation.**

| Selector | Author | Check 9 |
|---|---|---|
| Mismatch term | blinded Codex (second author) | satisfied |
| Hybrid architecture and budget (width 32, 12 modes, 4 layers, 2.37 M parameters; 1-frame rollouts, batch 64, 2,000 steps) | the executing agent, frozen before any test data. The budget was set by a timing pilot on training data only (2.2 s per step, launch-bound). | not satisfied |
| Test Re, thresholds, arms | the WO author (Todd and Claude), after stage 1 | not satisfied; see item 2 |

## Stops

None. Every part executes under the pins above.
