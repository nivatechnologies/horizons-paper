# ACD spec integrity gate — v2.1 — HALT

Date: 2026-10-05. Scope: the complete vault work order, read in full, followed by both standing templates. Their bodies are archived in `sources/`. Authorization: Todd's current instruction covers execution through Stage 1 and the declared toy-setting deviation; the work order's stale “Pending” field is not a new approval requirement. Confirmation, freeze and CNN inference remain unauthorized.

Base: `1b1094ae8f2536b9fe43e55ceeabfd3f02d14abc`. Branch: `paper/aspen-2026-10-determinacy`. The remote forecast-decision branch was `9f86d2969e1b09acacf25936d396ef77cf57a3d1` when fetched; the new branch uses the explicitly requested older base. The Baccus forecast-decision worktree was not modified. No applicable AGENTS.md was found in this worktree or its filesystem ancestors.

Step 0b ran first, without experimental data. Prompt and verbatim answer plus overlap are committed in `CODEX_SELECTOR.md` at `eb87279`. The competing selector is a fresh blinded CLI session. No development artifacts or scientific code have been read for Step 0; no posterior, forecast, null, probe, confirmation or CNN run has started. The synthetic arithmetic audit below was reproduced on sulaco CPU; it imports no experiment code.

## Decision and failed check

**FAIL check 4 (source class / what an input licenses): WO §10 prescribes raw case-percentile bootstrap quantiles but treats them as one-sided 95% accuracy confidence bounds for R0/R0-F and licensed sentences.** At the accuracy boundary, empirical self-consistency is not evidence for a population bound. This is a correctness and interval-validity defect (guideline classes A/B), not a request for extra experiments.

WO §2 and Todd's instruction require stopping on any failed check. Stop before Step 0. `ACD_STEP0.md`, numerical report, validation and Stage 1 reading are intentionally absent because their prerequisites have not passed. This is a specification halt, not a scientific kill or an unfavorable development result.

### Reproducible counterexample

All case summaries in this subsection are **synthetic hypotheses under test**, not claimed Lorenz-96 observations. They obey the specified maximum of eight S questions per case and the specified case as statistical unit. The counterexample establishes an interval failure on allowed scoring inputs; it does not assert that this distribution occurs on Aspen's development panel.

Consider 200 independent cases, each with (observation-confident S count, correct count) distributed as:

| Count | Correct | Probability |
|---|---|---|
| 0 | 0 | 0.850 |
| 1 | 1 | 0.100 |
| 8 | 8 | 0.043 |
| 8 | 0 | 0.007 |

The population ratio-of-sums accuracy is `(0.100 + 8*0.043)/(0.100 + 8*(0.043+0.007)) = 0.888`, below 0.90. Let E be the event that there are no incorrect cases, at least 30 nonempty cases, and at least 100 answers. For every nonempty case-bootstrap resample on E, correct count equals answer count. Every defined bootstrap accuracy is 1; its 5th percentile is 1, so R0 PASS is forced for any 10,000-replicate seed.

If `e` counts eight-answer correct cases and `o` counts one-answer cases, the exact event probability is:

`sum 200!/(e!o!(200-e-o)!) * .043^e * .100^o * .850^(200-e-o)`

over `e+o >= 30`, `8e+o >= 100`, `e+o <= 200`. The sum is **0.061120375098500886**. The counterexample script uses a deterministic multinomial sum in log space, not Monte Carlo. Empty bootstrap resamples can have undefined ratios; even if any such replicate blocks PASS, their union probability is bounded by `10000*.85^200 < 8e-11`. Subtracting that bound still gives a false-PASS probability above **6.11%**, exceeding 5%. Thus even R0's published count floors do not repair the claimed confidence level; coverage is at most about **93.89%** on this allowed population.

A simpler illustration for R0-F is 30 confident, correct cases: all bootstrap bounds equal 1, while at true accuracy 0.95 that event occurs with probability `.95^30 = 0.21463876394293727`. The advertised lower bound covers the population accuracy at most 78.54% in that example. This illustration shows boundary undercoverage, not a false PASS below the 0.90 threshold; the preceding R0 construction demonstrates the latter separately.

Evidence: `spec_boundary_counterexample.py`, `SPEC_BOUNDARY_COUNTEREXAMPLE.json`. Reproduce on the required host with:

```bash
ssh sulaco python3 - < aspen/determinacy/spec_boundary_counterexample.py
```

The general proportion-bootstrap boundary problem is also documented by the primary research paper [A note on bootstrap confidence intervals for proportions (2013)](https://www.sciencedirect.com/science/article/pii/S0167715213002940). Its publisher search abstract states the zero infimum coverage result; full text was inaccessible (403). The halt rests on the explicit calculation above, not unseen paper contents.

### Required amendment, not implemented

Specify an accuracy-bound procedure with a defensible treatment of sparse errors and case dependence for R0 and R0-F, including empty replicate handling. Do not substitute an answer-level binomial/Wilson interval for R0: eight answers can be dependent within a case. Keep the ratio-of-sums target, count floors, and route prerequisites unless the amendment explicitly changes them. Audit the accuracy upper bounds used by L7/L8 for the analogous all-error boundary, and disclose whether other percentile intervals are approximate descriptive intervals or calibrated route tests.

Differential prediction required by the standing gate: low-accuracy populations such as the 0.888 construction must remain failures with controlled false-PASS risk; panels below the count floors remain NOT EVALUABLE; genuinely adequate evidence above 0.90 can still pass. An amendment that merely guarantees every formerly blocked perfect sample passes is not a correction. The executor has not chosen or applied a replacement rule.

## Checks 1–9 including 5a

| Check | Assessment | Evidence / limits |
|---|---|---|
| 1 Two-sided feasibility | PASS for operational geometry | The complete witness table below gives inputs on both sides. Numerical pass fixtures are inputs to rules, not physical predictions. R0's operational rule is feasible but its claimed confidence level fails check 4. |
| 2 Independence | PASS as designed; implementation unverified | Development is exploratory and reused; only new disjoint confirmation seeds provide scientific independence. Hidden realized truth is not sampler input; null sees no observations; Q/F/V target draws; shared probe noise is a paired control. Confirmation forecasts are hashed before actual costs. Step 0 has not verified these code-level properties. |
| 3 Referents | PASS for operational quantities | Unit is case/lead/question; state is first-frame x and uniform F; intervention sign, pair ordering, eight-action winner, and Fc's climatological threshold are explicitly distinct. Cases, members, posteriors and probe refits have separate denominators. Empty bootstrap ratios need amendment as part of the failed interval rule. |
| 4 Source class | **FAIL** | Posterior probabilities are conditional model calculations; realized truth supplies empirical calibration; unweighted RML is approximate; an emulator is not ground truth; the null knows true F. WO §10 nevertheless promotes a degenerate empirical bootstrap distribution into a nominal confidence bound. Counterexample above. |
| 5 No example as definition | PASS | Equations and explicit thresholds define readings. §12 examples illustrate them. “1.5 times” in §13 is explanatory, not authoritative arithmetic: the actual strong margins are 0.25/0.30/0.15. |
| 5a Witness provenance | PASS | Every witness below is explicitly hypothetical. Inherited observations and constants are work-order assertions pending Step 0; §16 references are prior-work assertions, not fresh source verification or implementation evidence. |
| 6 Surprise | PASS | A sign could lose confidence earlier than Fc; c could remain near 1; forecast targeting could equal or beat Q; posterior diagnostics/coverage could fail; RML could disagree beyond event MC error. None is defined away. |
| 7 Null | PASS as designed | 4096 climatological states at known F and random measurement sites. Null never becomes truth; Fc uses its mean. Implementation awaits Step 0/Stage 0. |
| 8 Comparator separability | PASS as designed | Q must exceed both V and F using two paired lower bounds and exceed the better point estimate by the margin. No ranking of crude/RML/CNN is licensed merely by overlapping bands. R5 count/accuracy/coverage safeguards are explicit. |
| 9 Selector separation | PASS with disclosed divergence | `CODEX_SELECTOR.md`: independent fresh author/session and different operational starting point. Direct S/P overlap; eight-action B versus nine-action best; only partial Fc overlap. Q-family overlap; F/V/R not independently proposed. Competing regret/backfire readings retained descriptively. One independent framing, no claim of several independent negatives. |

These are specification assessments, not blanket assertions that the code or data already pass. Overall sign-off is withheld because check 4 fails.

## Selector provenance and independence accounting

The action set is inherited from the AAH blinded Codex selector (provenance asserted by WO, not independently re-audited yet). Energy and windows are inherited from AAH/AFD. GPT originated the trajectory-versus-effect framing, covariance mechanism and spread comparator. Claude authored question details, targeting algorithms/comparator selections, confidence and calibration thresholds, R2/R5 margins, leads and precision after seeing exploratory AFD numbers. No development outcome is treated as an independent confirmation of those choices. The present blinded CLI selector is the second author required by check 9, with its overlap and omissions explicitly reported. Future negative, rank or shortlist readings must carry the selector provenance line and label development as exploratory. The stage populations, first-index rule, eight-action B, designated top-two pair, eligibility at lead 0, and first illustrative-case selector all remain primary-WO choices, not independently derived optimalities.

## Complete operational witness inventory

**Every input in the following table is a synthetic hypothesis under test (check 5a).** Unless a row varies a prerequisite, assume all other prerequisites pass, ample cases, no ties, and valid diagnostics. Bounds shown are hypothetical inputs to classifications; they do not validate the failed interval estimator. This table assesses scientific axes, filters and thresholds without running experiment data.

| Axis/filter/classification (WO section) | Passing / first branch | Failing / other branch |
|---|---|---|
| Scientific definition agreement (§3) | Code has the exact declared cost/window/action | Cost uses terminal energy instead of window energy: halt |
| Seed leaf disjointness (§4) | Distinct stream/case/sub leaves outside inherited IDs | Reused leaf or inherited ID: fail assertion |
| Observation likelihood / prior support (§5) | F=8, finite 40-state vector | F=10.1 has zero prior density; nonfinite state invalid |
| Posterior parameter and log-likelihood diagnostics (§5) | All R-hat=1.005, ESS=600 | One R-hat=1.02 or ESS=399: rerun; persistent fail excludes |
| Gate functional diagnostics (§5) | All D_k/J_8 at 2/3 LT meet 1.01/400 | Thinned ESS=300: forecast full draws; persistent failure follows rerun rule |
| Divergences (§5) | 40/4000=1% | 41/4000>1%: fails diagnostics |
| F boundary / convergence reporting (§5) | Interior minima; all starts converge | F=6 or optimizer fails: report, not automatic independent halt |
| Threshold uncertainty (§5) | p=.94, se=.01: flagged | p=.98, se=.005: not flagged |
| Panel diagnostic exclusion (§5/§14) | 10/200=5% excluded | 11/200>5%: halt |
| Gaussian implementation mean/variance (§5) | Every error 3 MC SE; both extreme-direction variances off 6% | Any mean/variance error 5 MC SE or extreme variance off 25%: halt |
| Joint FD adjoint (§5) | Maximum absolute error 9e-7 | Error 1e-6: halt |
| Multi-start minimum bookkeeping (§5) | Lowest χ² retained across four starts, RML and posterior | Retaining a higher start's χ² is an implementation failure |
| Truth coverage χ² (§5) | Δχ²=56.90: covered | Δχ²=57: not covered |
| Completed-panel coverage (§5) | 170/200=.85: no coverage halt | 169/200<.85: halt on dev, KILL on confirmation |
| Fit flag (§5) | χ²_min=460: no flag | χ²_min=470>467.6: flagged, reported |
| True-F rank (§5) | Uniform-looking histogram / large test p | Boundary-concentrated ranks / small p: reported, no independent threshold invented |
| S and P signed answers (§6) | D=-.01 or J_k−J_l=-.01: lower/yes | Zero or positive: not lower/no; exact zero logged |
| B and ties (§6) | Unique minimum at action 3: answer 3 | Equal minima at 2 and 3: answer 2; not action 8 |
| Fc (§6) | J_8>Jbar: yes | J_8=Jbar or below: no |
| Modal confidence, S=512 (§6) | 487 same answers: confident | 486 same answers or modal tie: not confident |
| Climate confidence (§6) | Same answer in at least 3892/4096 states | 3891 states, or a different climatological answer: not climate-confident for this posterior answer |
| Observation confidence (§6) | Confident posterior, no same climate-confident answer | Posterior not confident, or same climate-confident answer: excluded from observation-confident share |
| Realized accuracy (§6) | Modal answer equals actual answer | Different answer: incorrect even if confidence is 1 |
| Split stability (§6) | Both chain groups agree on classification | One group crosses .95: instability reported, not a new gate |
| dt answer and classification checks (§6) | Every lead ≤3 has .004 answer changes and .008 class changes | Any lead has .006 answer changes or .011 class changes: halt |
| Null (§7.1) | 4096 independently seeded spun-up states and mean over states/leads | Observation-conditioned states called climatology or ensemble used as truth: invalid |
| Crude/RML member counts (§7) | 128 crude draws; 112/128 valid RML | 111/128 valid RML: short case; 11/200 short cases: halt |
| RML validity (§7.3) | Finite; RMS=9*SIGMA; Δχ²=74 | Nonfinite, RMS>10*SIGMA, or Δχ²>74.75: invalid |
| Signed sampler comparison (§7.3) | Same-event p's differ by 2 combined SE | Difference 4 combined SE: substantive; opposite modal answers cannot be hidden by comparing modal masses |
| Threshold crossing (§7.3) | p_post=.96, p_RML=.94 with abs(z)≤3: diagnostic only | abs(z)>3: substantive; handled by Stage 1a rule, not automatically proof posterior is wrong |
| Forecast horizon (§7.5) | Fc confidence share .50 at a lead qualifies | Share .49 does not; largest qualifying lead is used |
| R5 designated pair/population (§8) | First-index case with top-two pair p=.90 is included | Pair p=.97 excluded; only 39 qualifying cases: NOT EVALUABLE |
| Q/F/V/R/A site rules (§8) | Q maximal expected D-variance reduction, F same for J8, V largest four variances, R uniform distinct four, A all 40 | Truth-based site choice, redundant random site, or selecting by another observable violates that arm |
| R5 probe sharing (§8) | Identical per-case/site η vector used across arms | Independent η per arm invalidates prescribed pairing |
| R5 refit denominator (§8) | Confident correct refit contributes 1; failed refit contributes 0 | Dropping failed Q cases or counting wrong confidence as correct invalidates C_Q |
| Q-BEATS margin/bounds (§8) | C_Q=.34, C_V=.19, C_F=.15; lower bounds .04/.08 | Best alternative=.30, or either lower bound=0: no Q-BEATS |
| Q count/accuracy/coverage (§8) | 34 confident answers, accuracy .94, Wilson lower .83, coverage .93 | 19 confident; Wilson lower .79; or coverage .84: no Q-BEATS |
| Mechanism (§9) | Positive variances, ρ=.9 and c=.1 satisfy variance identity | ρ near 0 and c near 1: little cancellation, reported; zero variance makes correlation undefined and must be reported |
| R0 (§10) | 410 answers/60 cases, accuracy .97, lower .95: PASS | Evaluable lower .88: FAIL; 99 answers or 29 cases: NOT EVALUABLE |
| R0 climate-heavy safeguard (§10) | Observation-confident subset lower .94 | All-confident accuracy .95 but observation-confident lower .86: FAIL |
| R0-F (§10) | 30 confident cases, lower .91: PASS | 30 cases lower .89: FAIL; 29 cases: NOT EVALUABLE |
| R1 map (§10) | Shares/intervals for all types and leads | Missing Fc, an action, or climate/observation separation: incomplete reporting |
| R2a (§10) | Δ=.26, 99% interval [.15,.37]: DIFFERS | Δ=.04 interval [-.06,.09]: EQUIVALENT; Δ=.17 interval [-.02,.35]: INCONCLUSIVE |
| R2a prerequisites (§10/§11) | R0 and R0-F PASS at the compared lead | R0 PASS only at another lead or R0-F FAIL: no publish route |
| R2b eligibility and floor (§10) | 30 eligible cases with S observation-confident and Fc confident at 0 | No eligible action: omit case; 29 eligible cases: NOT EVALUABLE |
| R2b loss/censoring (§10) | S loss unobserved to 6 and Fc loss at 4: S later | Both unobserved: tie; Δ=0 alone does not establish same-lead loss |
| R2b outcomes (§10) | Δ=.31 interval [.12,.48]: OUTLIVES; -.27 [-.44,-.09]: PRECEDES | .01 [-.07,.08]: NO DIRECTIONAL PREFERENCE; .12 [-.05,.30]: NO ORDER DETECTED |
| R2b calibration prerequisites (§10/§11) | Every lead R0/R0-F PASS or NOT EVALUABLE | Either FAIL at any lead: no ordering publish route |
| R2c (§10) | Answer at or below T_h and report its errors/refusals | Treating rule-answered as automatically confident is invalid |
| R3/R3b/R6 accuracy/agreement (§10) | Accuracies, probability bins, κ and counts reported | High κ or confidence share called calibration without actual outcomes: invalid source use |
| L7 strong crude wording (§11) | Accuracy .78 and one-sided upper .82 | Accuracy .88, or upper .91: neutral wording |
| L8 overconfident wording (§11) | Accuracy .70 and upper .78 | Accuracy .85 or upper .90: word not licensed |
| CNN validity/service halt (§7.4/§14) | Valid member in every action; existing services continue | Invalid under one action: drop across all; requiring Qwen shutdown: halt |
| R7 (§10) | Two-scale truth, one-scale inference and reported fit/calibration | Claiming same-class calibration from mismatched truth: invalid; optional arm may be cut |
| Publish / kill / otherwise (§11) | R0 PASS at 2 plus valid R2a/R2b/R5 route: publish condition | R0 FAIL at both 2/3 or coverage<.85: kill; neither: Todd decides |
| Licensed sentences (§11) | L1 with both calibration passes; L4 with R0 pass | L1 without Fc pass, or outlives from R2a alone: unlicensed |
| Stage 1a diagnostics/coverage (§13) | 1/20 diagnostics failures and 15/20 covered: continue | 2/20 failures or 14/20 covered: halt |
| Stage 1a disagreement/rerun (§13) | >5% substantive S disagreements then fresh 4x posterior agrees within 1%: continue, label RML biased | Repeat posterior disagreements >1%: halt; threshold crossings alone never halt |
| Stage 1 strong (§13) | R0 PASS at 2, route prerequisites, and R2a abs(Δ)=.26, R2b abs(Δ)=.31, or R5 margin=.16 with required bounds | R2b abs(Δ)=.18 or missing route prerequisite: not strong; R0 FAIL both 2/3: stop/report |
| Runtime projection and cuts (§13/§14) | All required costs/compile/diagnostics plus rerun allowance fit 12h after permitted cuts | >12h after R7,A,R6@3,RML-conf,P/B-other-leads,R5@3 cuts: halt; never cut required core |
| Freeze / blind order (§4/§14) | Freeze committed before confirmation; outputs hashed before realized outcomes | Confirmation reading before freeze: halt |
| Illustrative selector (§13) | First confirmation index satisfying all declared predicates | Choosing the prettiest or a later matching case: invalid selector use |

## Gate summary

Stage and gate: pre-data spec integrity, HALT. Headline value: unmeasured; no scientific threshold evaluated. Change: Step 0b is complete and check 9 is assessable; check 4 exposes an interval defect not corrected by v2.1. Largest risk: calibration bounds can license a false PASS even with the count floors. Recommendation: stop for a targeted statistical amendment, preserve the original scientific thresholds and disjoint confirmation plan, then rerun this gate before Step 0. This report does not amend the work order or authorize a publish route.
