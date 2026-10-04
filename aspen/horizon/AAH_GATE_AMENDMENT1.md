## Amendment 1 gate rerun — 2026-10-04

Amendment 1 was reread from 02-Projects/WO_Aspen-Act-Beyond-Horizon-Kill-Test-2026-10-03.md through the niva-obsidian MCP. It supersedes conflicting original text. Exact amendment is retained as aspen/horizon/AAH_AMENDMENT1.md. Step 0 remains complete and was **not rerun**.

**Result: one unresolved check-3 referent in A5 blocks the censored member-gain reading and therefore final PASS classification.** Other original defects are resolved or their affected arms explicitly removed. This is a specification result, not an empirical KILL. No new empirical data are needed to establish the remaining ambiguity.

### Original defects: disposition

| Original defect | Amendment | Rerun disposition |
|---|---|---|
| 1. Forecast horizon/action/anomaly reference | A1 defines Niva M=64, true controlled trajectory, action climatology, spatial ACC, case/action averaging, first crossing and censoring | Resolved |
| 2. Off-grid readings | A2 grid, G(x), sufficiency threshold and no interpolation | Resolved; undefined G beyond 20 cannot support the corresponding criterion |
| 3. PASS/KILL overlap | A3 sustained horizon and KILL precedence | Resolved; old overlap example has undefined T_d and cannot PASS |
| 4. Truth bootstrap and stream independence | A4 disjoint streams, paired member bootstrap, bounds and eligibility | Resolved operationally; bootstrap confidence is an estimated design level, not a distribution-free guarantee |
| 5. Sequential commitment and member budgets | A5 six looks, bounds, empirical commitment errors, nested fixed-M budgets | Commitment resolved; censored M_95 referent remains ambiguous |
| 6. Uncentered control variate | A6 removes it from stage 1 | Resolved by removal; unavailable, never ranked |
| 7. Observation uncertainty / parameter identification | A7 observation equations, perturbed-observation sampler, P1x and F fitting | Resolved; label as perturbed-observation ensemble, not Bayesian posterior |
| 8. Actions/calibration/learned settings | A0 final run-1 set; A8 grids, sizes, numerics, training and stability rules | Resolved for stage-1 design; routine exact architecture/seed/batching choices belong in the pre-data freeze |
| 9. Objectives/regret/correlations | A9 exact formulas and descriptive correlation unit | Resolved for nondegenerate inputs; undefined zero-denominator metrics must remain unavailable, not fabricate values |

### Remaining A5 ambiguity (check 3; affects check 4 if read as a physical bound)

A5 tests M in {8,16,32,64,128,256}, then states: “If none qualifies, it is censored at '> 256', and its lower bound is 512.”

Two possible constructs give different readings:
1. **Grid-budget M_95:** the smallest successful allowed budget on a powers-of-two grid that continues with 512,1024,... . Then failure through 256 implies grid-budget M_95 >= 512. The 512 bound is valid for that construct. The current text lists only budgets through 256 and does not explicitly define this continuation.
2. **Actual member count M_95:** the smallest integer count needed to reach 95% accuracy. Failure on the tested grid establishes no success through its tested budgets; even assuming a monotone threshold, >256 gives only >=257, not >=512.

Concrete hypothetical counterexample, **hypothesis under test**: paired reaches 95% at M=128; unpaired fails at every tested budget through 256 but first succeeds at M=300. The actual ratio is 300/128=2.34375, below 3. Assigning 512 as the lower bound gives 512/128=4 and passes. This can turn a failure of the actual-member-count claim into a PASS before the missing evidence exists.

Clarification was requested during this rerun: whether M_95 means continuing powers-of-two budgets or actual integer counts. No answer has yet established the referent. This is a clarification of the measured construct, not a request for permission or to loosen a threshold.

Differential prediction for a correction: declaring the grid construct must leave grid-budget cases requiring 512 or more censored, and must not assert that an actual count such as 300 is at least 512. Choosing actual counts must leave a censored unpaired case with paired M=128 unable to establish the 3x criterion from >256 alone. Cases with paired M=64 can still clear 3x using a conservative integer lower bound; a correction must distinguish these cases, not revive everything.

### Checks 1–9 including 5a

| Check | Result | Reason |
|---|---|---|
| 1. Two-sided feasibility | Pass for specified individual thresholds and amended outcomes | Updated concrete inputs below; sustained horizon removes prior overlap |
| 2. Independence | Pass in amended design | Calibration/test and truth/arm/training/validation namespaces separated; within-arm pairing preserved |
| 3. Referent | **Fail for censored member-gain reading**; pass for remaining core definitions | A5 grid-budget versus actual-count distinction changes a verdict; other earlier referents now named |
| 4. Source class | Pass for protocol; member-bound claim conditional | Amendment is a rule/hypothesis, not measured evidence. 512 is justified only under the continuing grid construct |
| 5. No example as definition | Pass | Examples illustrate; none resolves the missing M_95 construct |
| 5a. Example provenance | Pass | All constructed inputs in this rerun explicitly labelled hypotheses under test |
| 6. Surprise | Pass | Decisions may die with forecasts or pairing may not provide 3x gain; learned response and forecast associations may reverse thesis |
| 7. Null baseline | Pass | Random/myopic nulls preserved; action-specific climatology gives zero skill under A1's low-forecast-anomaly rule |
| 8. Comparator separability | Pass for stage-1 design | Same-physics unpaired comparator retained; learned readings expressly carry no strongest-practice claim; censored member ratio still blocked by check 3 |
| 9. Selector separation | Pass under WO's specified Step 0 mechanism; provenance recorded | Final blinded run-1 action set selected before data; run-2/Claude overlap retained; other selectors belong to WO author, distinct from this executing reader |

### Updated two-sided threshold inputs

**Every numeric example below is a constructed hypothesis under test**, not a physical observation, established example or definitional anchor. Passing means satisfying the named condition; for KILL it means triggering it.

| Threshold / classifier | Passing input | Failing input |
|---|---|---|
| Positive chaos-gate lower bound, every action | all action lambda 95% intervals [0.10,0.20] | one interval [-0.01,0.20] |
| Calibration >=80%, L96 n=40 / Kolmo n=20 | 32/40 and 16/20 eligible at delta=0.05 | 31/40 or 15/20 at every grid amplitude |
| Small-amplitude bound delta<=0.1 | first eligible amplitude 0.1 | success only at 0.2: unavailable, no escalation |
| Truth eligibility, one-sided q=0.01/(K-1), B=2000 | every paired percentile lower bound +0.1 | any bound 0 or -0.01 |
| Grid sufficiency >=50% | 100/200 and 15/30 eligible (10/20 if cut used) | 99/200 or 14/30 (9/20 if cut used) |
| Forecast first ACC<0.2 | mean ACC 0.3 at 1, 0.19 at 1.5: T_f=1.5 | all grid values >=0.2: censored |
| A1 low-anomaly guard: squared forecast norm <1e-12 times truth norm | truth norm-squared 1, forecast 0.5e-12: ACC=0 | forecast 2e-12: use formula if norms nonzero |
| Sustained accuracy >=0.8 | every sufficient point from T_f=1 to T=3 has 0.8 | accuracy at T=2 is 0.79 despite later recovery |
| PASS horizon T_d>=G(3 T_f), both systems | T_f=1, T_d=3 in both systems | one T_d=2.5 |
| Fixed-M top-1>=0.95 | 190/200 correct eligible cases at M=64 | 189/200 |
| Measured member ratio>=3 | paired M_95=32, unpaired=128, ratio 4 | paired=64, unpaired=128, ratio 2 |
| Censored member ratio | continuing grid construct: paired=128, unpaired grid-budget bound=512 gives 4 | actual-count construct: first unpaired success 300 gives 2.34375; same missing-grid observation cannot decide the construct |
| Sequential commitment bound >0 at q=0.05/(6(K-1)), B=1000 | all competitor bounds +0.02 at M=64 | one bound 0 or -0.01 at every look: uncommitted at 256 |
| Commitment maximum M=256 | separation at final look 256 | hypothetical separation only at 512: uncommitted |
| KILL: both accuracy<0.5 at sufficient G(1.5 T_f) | T_f=2, G=3, accuracy 0.42 and 0.40 | either accuracy 0.5, insufficient point or censored T_f |
| Otherwise | one system passes, other lacks sustained horizon, neither KILL | both unambiguously PASS with measured member ratios |
| Learned stability: finite and RMS<=10 sigma | finite state, RMS=10 sigma | nonfinite state or RMS=10.01 sigma |
| Drop >50% members: score wrong | 33/64 dropped: forced wrong | 32/64 dropped: retained-member decision used |
| Normalized regret, nondegenerate costs | best=2, chosen=3, worst=6: 0.25 | chosen=best=2: 0; all costs equal: denominator zero, unavailable |
| Null choice expectation, K=8/6 | random probabilities 1/8 and 1/6 | claiming 0.5 as chance for these sets |

Fixed dimensions, panel counts, dt/precision, 2% noise, 1e-12 jitter, 10% misspecification, training steps/range, look counts and bootstrap counts are protocol settings. They are recorded as settings, not empirical pass thresholds. Equality conventions follow Amendment 1.

### Correction discipline verified

The previous overlapping example is not PASS: accuracy 0.4 at T_f=1 makes sustained T_d undefined, irrespective of later 0.85. An executable arithmetic check also verified G(1.5*2)=3, G(3*2)=6, and undefined G(3*8). A curve at 0.8 until 2.5 and 0.79 at 3 has T_d=2.5 despite later recovery. Failed amplitude grids remain failed; removed variate remains unavailable; no forecast crossing stays censored; no separation at 256 stays uncommitted; near-ties remain excluded/reported.

### Selector provenance and scope

Final action selector: Codex CLI run 1, generated blinded before data; run 2 and explicitly attributed Claude families used only for recorded overlap. Horizon grid, window, objectives, systems, arms, sufficiency/eligibility and cut order: amended WO author (Claude attribution remains role-based from guideline, not verified author metadata). M_95 construct: unresolved in amended WO; this executor has not silently authored a replacement. Branch/machine routing: Todd's direct instructions. Multiple calls to one prompt remain one framing.

### Disposition

The amended work order has not passed as a whole because A5's member-gain referent remains unresolved. Stop the affected censored-member comparison and final PASS reading. Other core protocol definitions pass the design gate, and the removed control-variate arm stays removed. No calibration, truth ensemble, test-panel or learned-training job was launched during this rerun under the user's conditional instruction to execute if the gate passes. No Step 0 rerun, service shutdown, fabricated freeze, empirical NUMBERS or scientific verdict.

Continue on paper/aspen-2026-10-horizon once the M_95 construct is established, with Baccus for Kolmogorov and sulaco for Lorenz-96/truth ensembles. This audit did not change either criterion.
