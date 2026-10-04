# Act beyond the horizon: spec integrity gate (2026-10-04)

Status: **BLOCKED for calibration, experimental data, training, evaluation and scientific verdicts.** Step 0's two blinded action-set generations may proceed independently. This is a specification audit, not an empirical KILL result.

## Authority and execution boundary

Read through the niva-obsidian MCP:
- 02-Projects/WO_Aspen-Act-Beyond-Horizon-Kill-Test-2026-10-03.md (WO).
- 00-Foundations/T_Spec-Integrity-Gate.md (checks 1–9 including 5a).
- 00-Foundations/T_Research-Paper-Guideline.md (guideline; frontmatter says draft for ratification).

The WO explicitly requires stopping each part that fails a check. No revised scoring rule is silently substituted. User instruction overrides the WO branch: paper/aspen-2026-10-horizon, based on latest fetched paper branch origin/paper/adapt-physics-2026-09 at 8147f8262dd5c9659bbc2cd83c70990d8b517584. Work stays under aspen/horizon/.

Compute assignment from user: Baccus for Kolmogorov; sulaco (192.168.88.228) for Lorenz-96 and truth ensembles. Read-only connection check succeeded: local hostname baccus; remote hostname sulaco, nproc = 256 logical CPUs. No experiment or training jobs launched; no Qwen service stopped.

## Checks

| Check | Outcome | Evidence / scope |
|---|---|---|
| 1. Two-sided feasibility | Individual numeric thresholds feasible; joint outcome classification FAILS | Examples below. A nonmonotone accuracy curve can satisfy PASS and KILL together because T_d is the largest successful T. |
| 2. Independence | Calibration/test separation specified; estimator independence UNPINNED | Fresh held-out cases provide new information. Separate truth and arm member streams, training/validation/test seeds, and posterior construction are not pinned. Sharing initial members with truth can bias top-1 upward, even on held-out cases. |
| 3. Referents | FAIL | Forecast anomaly reference and action/arm aggregation, off-grid readings, posterior sampler, Lorenz F identification, simultaneous bootstrap rule, regret denominator, and learned-arm tuning are not operationally defined. |
| 4. Source class | PASS for the audit; empirical claims unvalidated | WO is a hypothesis/protocol, not evidence. Existing solver code is implementation; old World D calibration is prior measured evidence at its recorded conditions. Prior-work citations in WO have not been verified here and establish no new result or budget. |
| 5. No example as definition | PASS | WO's feasibility examples are illustrations only. They cannot define interpolation, confidence, or an outcome rule. |
| 5a. Example provenance | PASS | Every constructed numeric example below is explicitly hypothetical under test. No physical feasibility claim is inferred from them. |
| 6. Surprise | PASS | Decisions dying with forecasts, or learned decision accuracy following forecast skill rather than response fidelity, contradict the stated thesis. |
| 7. Null baseline | PASS for decision accuracy; forecast/regret details UNPINNED | Random choice and myopic null included. Random expected top-1 is 1/8 or 1/6. Report actual null performance on eligible cases. Forecast climatology reference and regret normalization still need definitions. |
| 8. Comparator separability | UNPINNED for learned comparator and member-gain claim | Same-physics unpaired comparator is identifiable, but member budgets, censored readings and uncertainty on M ratios are unspecified. FNO/emulator sizes, training budget, validation selection and tuning are absent, so strongest-practice superiority is not licensed. |
| 9. Selector separation | Step 0 mechanism admissible, pending verbatim outputs and overlap; remaining provenance incomplete | WO supplies Claude's comparison sets and requires blinded Codex sets. Other selector provenance is reported below; unknown authorship cannot be promoted to verified independence. |

## Blocking defects and differential corrections to request

1. **Forecast horizon has no unique referent (check 3).** Is T_f measured for the uncontrolled dynamics, every controlled action, a selected action, the Niva arm, or each learned arm? Persistent forcing changes the response mean; subtracting uncontrolled versus action-conditioned climatology can change anomaly correlation. Specify the anomaly field, correlation axes, averaging over cases/actions, forecast member count, zero-variance behavior and no-crossing censoring. A corrected rule must leave noncrossing/undefined curves censored, not assign a convenient finite T_f.

2. **Required readings are outside the fixed grid (check 3).** With T_f=2 LT, 1.5 T_f=3 LT is not in {0.5,1,2,4,8,12,16,20}; with T_f=1, the KILL location 1.5 LT is missing. The WO's own PASS example also uses 6 LT, which is missing. “By” could mean an earlier observed crossing, the endpoint, or interpolated accuracy. At grid points 2 and 4, accuracies 0.7 and 0.3 do not determine accuracy at 3. Specify extra sampling, a discrete rule or interpolation before calibration/test. Do not reinterpret missing readings as PASS, KILL or measured data.

3. **PASS and KILL overlap (checks 1, 3).** Hypothetical input: both systems T_f=1, top-1=0.4 at T=1, top-1=0.85 at T=4, paired/unpaired members=16/64 at T_f. T_d>=4 meets PASS, while accuracy already fell below 0.5 “by” 1.5 T_f meets KILL. No monotonicity is guaranteed by the definition. Fix precedence or define a sustained decision horizon. Differential prediction: this example must cease to be simultaneously PASS and KILL; it must not automatically become a PASS.

4. **Decision truth confidence is underspecified (check 3).** Specify paired resampling unit, simultaneous best-vs-all confidence, bootstrap procedure/replicates/seed, and eligibility per case/horizon/window/timing. Marginal 99% intervals are not a defined joint 99% best-action claim. Specify truth/arm stream independence while retaining within-arm pairing. Preserve near-ties as excluded/reported; do not make them determinable by changing the rule after seeing the panel.

5. **Sequential commitment needs a statistical rule (check 3).** Repeatedly examining nominal 95% pairwise intervals after choosing the leader does not by itself define overall 95% selection coverage. Specify scheduled looks, multiplicity/optional-stopping treatment, start/batch sizes, interval construction and noncommitment at M=256. The WO's Kim–Nelson citation is a method pointer, not a complete implementation. If 95% is descriptive nominal coverage instead, state that and do not call it an error guarantee. Wide or nonseparating cases must remain uncommitted.

6. **Control variate changes the estimand as written (checks 2, 3).** For true paired difference D and tangent prediction L, E[D-L]=E[D]-E[L]. Subtraction alone does not estimate expected cost difference. Hypothetical input: E[D]=1 and E[L]=2; subtraction changes +1 into -1 and reverses the preference. Define a centered variate D-b(L-E[L]) with an independently justified mean and coefficient, or report residuals without ranking them as original costs. Unknown variate means must remain unavailable, not assumed zero.

7. **Observation uncertainty and identified parameters are unpinned (check 3).** “Consistent with observations” plus truth+noise spun through a window is not an executable posterior sampler. Specify noise scale/distribution, which observation initializes the ensemble, conditioning/assimilation, whether truth is used only to generate observations, and identical information across arms. Kolmogorov P1x can be reused, but Lorenz runtime F estimation is not specified. Do not use true hidden state as a forecast input merely because it exists for synthetic truth.

8. **Action calibration and learned comparison require a freezeable protocol (checks 3, 8).** Pin calibration case count, amplitude units/norm and small-amplitude bound, amplitude grid/selection/tie rule, learned datasets/architecture/budget/validation, numerical precision/time step, member search grid and repeats. A failed calibration must remain failed when no small amplitude meets 80%; no unlimited amplitude escalation. Step 0 returns two competing sets per system; choose or compare them by a pre-data rule, not the most successful outcome.

9. **Objective and reporting definitions are incomplete (check 3).** Lorenz energy is explicit. Pin Kolmogorov enstrophy dissipation (viscous alone or including drag), treatment of velocity versus vorticity forcing, normalized/realized regret, and sample units for partial correlations. Old World D dissipation convention is available as a reference, not silently inherited for a differently worded objective.

## Every threshold: concrete passing and failing inputs

All inputs in this table are **constructed hypotheses under test**, not observations, citations to established physical outcomes, or definitional anchors. “Pass” means satisfying the named condition; for KILL it means triggering KILL. Protocol constants (grid size, noise, panel counts) are settings, not empirical thresholds.

| Threshold / filter | Passing input | Failing input |
|---|---|---|
| Positive Lyapunov exponent if reusing old chaos gate | lambda 95% interval [0.10,0.20] | interval [-0.01,0.20] |
| Calibration determinability >=80% at 20 LT | 16/20 cases eligible | 15/20 eligible |
| Truth best determinable at 99% confidence | simultaneous 99% lower bounds C_j-C_best all +0.10 | one bound -0.01 |
| Forecast first correlation <0.2 | correlations 0.7,0.3,0.19: crossing at third T | all >=0.2: no crossing, censored |
| Decision accuracy >=0.8, M=64 | 160/200 correct eligible cases | 159/200 |
| Members achieve >=95% top-1 | 190/200 correct at M=64 | 189/200 |
| Commitment: leader better than every alternative at 95% | every simultaneous difference lower bound +0.02 | one lower bound -0.01 |
| Commitment cap M=256 | intervals separate at M=256 | no separation through M=256: noncommit |
| PASS: both T_d/T_f>=3 | L96 8/2=4; Kolmo 4/1=4 | L96 4/2=2; Kolmo 4/1=4 |
| PASS: both unpaired/paired member ratios>=3 at T_f | 60/12=5 in both systems | 24/12=2 in either system |
| Combined PASS | both horizon ratios 4 and both member ratios 5, no conflicting KILL | one horizon ratio 2 despite other passing values |
| KILL: both accuracy<0.5 by 1.5 T_f | 84/200 and 11/30 correct at specified endpoints, assuming all eligible | 100/200 on either system (0.5 does not qualify) |
| Otherwise | one system horizon ratio 4, other 2, neither KILL | unambiguous combined PASS |
| Near-tie exclusion | one competitor's 99% interval crosses zero | all simultaneous bounds strictly positive |
| Rollout stable through 21 LT (reported only) | all states finite and within a prospectively specified stability rule | nonfinite state at 10 LT; finite-but-pathological rule is currently unpinned |
| Control-variate residual preserves ranking | E[D]=1, known E[L]=2, centered E[D-(L-2)]=1 | uncentered E[D-L]=-1 |
| Random-choice expectation | chance probabilities 1/8 L96 and 1/6 Kolmo | asserting 0.5 as chance for these K |

Equality conventions for 99%/95% eligibility, small amplitude and rollout stability are not supplied by the WO. Table examples do not resolve those omissions. Horizon ratios require a defined/censored T_f; the KILL example requires a defined “by” rule. Fixed 2% noise, 1e-12 jitter, 10% misspecification, 16x compression, ±2 delta training range, panel sizes and M values remain exact settings; none is evidence of measured performance.

## Selector provenance

The supplied WO has no explicit author frontmatter. The guideline assigns WO drafting to Claude; attribution to Claude below is therefore **role-based, not verified document history**.

| Selector | Author / provenance | Separation status |
|---|---|---|
| Candidate actions | two independent Codex CLI responses to identical supplied prompt, plus WO's explicitly attributed Claude sets | admissible mechanism; overlap must be reported after responses; final-set resolution still needs pre-data rule |
| Horizon grid | WO author (role-based Claude attribution) | evaluated here by a distinct executing party; no competing horizon framing in WO |
| W=1 LT primary, W=2 sensitivity | WO author (role-based Claude attribution) | rationale given (fixed averaging duration); not independent selector evidence |
| Energy / enstrophy-dissipation objectives | WO author (role-based Claude attribution) | energy formula pinned; Kolmogorov formula unpinned |
| Systems, arm/comparator families, cut order, panel eligibility | WO author (role-based Claude attribution) | report alongside any eventual finding; independent comparator selector/tuning absent |
| Branch and machine routing | Todd, direct instructions in this session | overrides older WO routing/branch |

Step 0's two responses are one prompt framing, not two independent negative findings. Any later ranking/negative must carry selector provenance and count independent framings rather than candidate/query count.

## Disposition

Proceed only with the independent blinded text generation and documentation. Stop all scientific execution that depends on the failed definitions, including calibration, truth ensembles, learned training, test panels, NUMBERS measurements and figures. Do not create AAH_FREEZE.md as though the protocol is complete. Proposed corrections above are requests for an amended WO, not adopted rules. Experimental results remain NOT RUN; no empirical PASS/KILL conclusion.

## Step 0 completion addendum

Both blinded CLI invocations completed successfully before any new experimental data. Exact prompts, verbatim final/preliminary responses and selector overlap are retained in aspen/horizon/CODEX_ACTIONS.md. Run-to-run exact overlap: 7/8 Lorenz-96 patterns and 4/6 Kolmogorov body-force patterns. Claude-family overlap is reported with the WO's formula ambiguities. Run 1 used no tools; run 2 searched the web; neither executed shell commands. Step 0 text generation is complete; final-set choice and scientific execution remain blocked. No empirical PASS/KILL result.


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
