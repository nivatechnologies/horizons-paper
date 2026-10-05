# ACD spec integrity gate — v2.2 — HALT

2026-10-05. The entire v2.2 vault note was read, especially §10 and §19; archived as `sources/WO_v2.2.md`. Both standing templates previously read in full remain applicable and are archived in `sources/`. This is the complete re-assessment, not a sign-off based only on the amendment.

Branch `paper/aspen-2026-10-determinacy`, requested base `1b1094ae8f2536b9fe43e55ceeabfd3f02d14abc`. Step 0b stays byte-for-byte unchanged from `eb87279`, as Todd instructed. The prior v2.1 gate remains available at `91e77a6`. Current authorization covers the synthetic statistical audit and, if every prerequisite passes, Steps 0 through Stage 1. The stale “Pending” field is not an approval blocker. Confirmation, freeze and CNN inference remain held.

## Decision

**HALT: check 4 cannot sign off on the finite-sample confidence-interval claim in §10.** The prescribed exact and Monte Carlo audits pass, but the literal grid inversion removes real means that the capital rule does not reject. The method's Ville justification applies to the continuous retained set, not to extra exclusions made by its inward grid endpoints. This is one correctness/source-class defect, not an unfavorable scientific result.

For 200 synthetic x values all equal to 1, the stated two-sided 99% grid interval is [.963,1]. At m=.9629 the largest K+ is 178.0211842333, largest K− is 1, and the largest hedged capital is 89.0105921166, below the required 100. Thus m is not rejected by §10's capital condition, yet is outside the grid interval. The reflected x=0 construction omits unrejected m=.0371 from [0,.037]. These are synthetic hypotheses under test, not claimed Lorenz-96 observations.

Evidence: `statistics.py` implements the literal grid prescription; `stats_grid_audit.py` reproduces the discrepancy; `STATS_GRID_AUDIT.json` records it on sulaco CPU. `ACD_STATS_AUDIT.md` reports all audit results and the power table. This failure is **not** a measured exceedance of a Monte Carlo false-PASS/noncoverage limit. It is a mismatch between continuous test inversion and the procedure the WO says that theorem licenses. The missing justification blocks check 4 under the template's rule that any check that cannot be answered in writing blocks execution.

No rule was silently repaired. An amendment must specify a conservative inversion for real-valued means and justify any assumption about the shape of the retained set. The primary betting paper's Appendix E.4 notes aGRAPA sublevel sets need not be intervals; consequently neither a monotone root-search shortcut nor a numerical grid is automatically a coverage-preserving inversion. [Primary source](https://arxiv.org/html/2010.09686v7).

Differential prediction required for a correction: .9629/.0371 must remain included when their capitals never cross the threshold; the 30-perfect-case R0 fixture must remain INSUFFICIENT; five Q-favouring discordances must stay nonsignificant at .01; the answer-point floor, all count floors and route prerequisites remain binding. Power changes from any interval amendment must be disclosed. No replacement algorithm, threshold or estimand has been selected by the executor.

## Audit and amendment disposition

Implemented predictable aGRAPA capitals and prefix maxima, literal one-/two-sided grid scans, case-averaged R0 and its answer-point floor, transformed answer-ratio lower bounds, four reading statuses, exact Clopper–Pearson bounds, exact one-sided McNemar, and reported-only bootstrap redraws. Standalone code imports no experiment module. Existing sulaco Python environment was used without modification; 16 CPU threads for the prescribed audit, one for the grid check. No training, GPU use, cloud computation, service changes or Baccus close-out changes.

- Exact agreement: CP maximum absolute error 4.774e-15; McNemar 6.661e-16.
- 20,000 independent 200-case panels per configuration: nine R0 null configurations all pass, maximum false-PASS .02685; three R2 mean-zero configurations all pass, maximum noncoverage .00425.
- Original .888 answer-accuracy construction has case accuracy .9533333333 under v2.2, so it is no longer a .90 case-mean null. Old no-error PASS frequency .06305, new full-rule PASS .00050; the exact 30-case fixture has lower .857 and is INSUFFICIENT.
- All required R0/R2a power cells reported (5,000 panels/cell); at .97 and 80 nonempty cases, power is .7900 for independent answers and .4724 for whole-case errors.
- Grid consistency check fails as detailed above. Approximate bootstrap intervals are clearly descriptive and do not repair or license a gate.

The original bootstrap boundary defect is fixed at the capital-test/exact-binomial level and the estimand/kill changes are explicitly disclosed in §19. The new halt concerns inversion of those tests, not opposition to the disclosed estimand change or low power.

## Full checks 1–9, including 5a

| Check | Assessment | Evidence and limits |
|---|---|---|
| 1 Two-sided feasibility | PASS for operational rule geometry | Full hypothetical witness inventory below. Four R0/R0-F statuses have different witnesses. Statistical geometry is feasible; inferential validity is separately blocked. |
| 2 Independence | PASS as designed; code verification pending | Development remains exploratory, confirmation uses new disjoint streams, truth never enters sampling, null sees no observations, targeting uses draws, common probe noise pairs arms. Synthetic audit consumes no experimental inputs. |
| 3 Referents | PASS for scientific objects; grid interpretation identified explicitly | Case/lead/question unit, first-frame state and F, costs and realized answers are pinned. New R0 averages over nonempty cases; answer-level ratio remains separate. R2b requires PASS/NOT EVALUABLE, excluding INSUFFICIENT. In §10 the null mean is continuous; it has not been redefined to lie on the grid. |
| 4 Source class | **FAIL / sign-off blocked** | Betting theorem licenses point-null capital rejection for predictable bounded streams with common conditional mean. Grid interval omits unrejected real means; that extra exclusion is not licensed by the stated Ville argument. Monte Carlo validity at .90/0 cannot establish continuous-parameter coverage for the literal endpoints. |
| 5 No example as definition | PASS | Equations define rules; §12/§19 fixtures are illustrative hypotheses. Actual strong margins .25/.30/.15 prevail over the approximate “1.5 times” shorthand. Reported power is not a guarantee. |
| 5a Witness provenance | PASS | All audit distributions and witness rows are explicitly synthetic hypotheses under test; no physical claim is inferred from them. Source work order is a design, inherited code assertions still await Step 0. |
| 6 Surprise | PASS | Sign confidence could precede Fc; cancellation could disappear; F/V could match Q; RML could differ beyond MC error; coverage could fail. Case dependence can sharply reduce power, as audit demonstrates. |
| 7 Null | PASS as designed | True-F climatological null and random sites; neither serves as truth. Computation follows later gates. |
| 8 Comparator separability | PASS as designed | Q must exceed max(V,F) in point share and pass both exact paired tests; exact accuracy/count/coverage safeguards remain. No comparator rank is licensed by approximate overlapping intervals. |
| 9 Selector separation | PASS, inherited artifact unchanged | Competing blinded selector at eb87279; overlap/divergence reported. No new model review or selector run. S/P direct, B wider nine-action family, Fc partial, Q-family overlap, F/V/R not independently proposed. Descriptive regret/backfire readings remain required if execution resumes. |

The full gate is not signed off. Steps 0, Stage 0 scientific checks, Stage 1a and Stage 1b have not begun. Scientific reports are not fabricated at an unmet prerequisite.

## Selector provenance and independence accounting

Action set: inherited AAH blinded Codex selector, as asserted by the WO and pending code/source verification. Observable/window: inherited AAH/AFD. GPT originated trajectory/effect framing, covariance and spread comparator; Claude specified questions, targeting/comparators, leads, precision, confidence/calibration thresholds and margins after exploratory AFD numbers. Claude authored Amendment 1's statistics, estimand/status changes and audit configurations. The executor's statistics follow that declared procedure and are being tested, not treated as findings by authorship.

One competing blinded operational framing was generated in Step 0b; its competing suggestions and omissions remain in CODEX_SELECTOR.md. There is no claim of several independent negatives. Primary-WO selectors include first-index R5 populations, top-two pairs, eligible-at-zero loss comparisons, and the first qualifying illustrative confirmation case. The synthetic case-size/error-mechanism grid is an authored audit selector; deterministic off-grid witnesses expose a limitation it did not sample. Empirical test rates are reported only for the specified synthetic configurations, not as universal validation. Confirmation would remain the only independent scientific evidence.

## Complete operational witness inventory


**Every input in the following table is a synthetic hypothesis under test (check 5a).** Unless a row varies a prerequisite, assume all other prerequisites pass, ample cases, no ties, and valid diagnostics. Bounds shown are hypothetical inputs to classifications. They do not validate the grid inversion. The v2.2 formula and all audit inputs are synthetic, not empirical anchors. This table assesses scientific axes, filters and thresholds without running experiment data.

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
| Q-BEATS margin/bounds (§8) | C_Q=.34, C_V=.19, C_F=.15; McNemar p=.0007/<.0001 | Best alternative=.30, or either McNemar p>.01: no Q-BEATS |
| Q count/accuracy/coverage (§8) | 34 confident answers, accuracy .94, Clopper–Pearson lower .83, coverage .93 | 19 confident; Clopper–Pearson lower .79; or coverage .84: no Q-BEATS |
| Mechanism (§9) | Positive variances, ρ=.9 and c=.1 satisfy variance identity | ρ near 0 and c near 1: little cancellation, reported; zero variance makes correlation undefined and must be reported |
| R0 (§10) | 410 answers/120 cases, case mean .97, betting lower .93, answer point .97: PASS | Evaluable betting upper .88: FAIL; bounds [.89,.99]: INSUFFICIENT; 99 answers or 29 cases: NOT EVALUABLE |
| R0 climate-heavy safeguard (§10) | Observation-confident subset lower .94 | All-confident accuracy .95 but observation-confident betting upper .88: FAIL |
| R0-F (§10) | 30 confident cases, exact lower .905: PASS | 30 cases exact upper .89: FAIL; exact bounds [.85,.95]: INSUFFICIENT; 29 cases: NOT EVALUABLE |
| R1 map (§10) | Shares/intervals for all types and leads | Missing Fc, an action, or climate/observation separation: incomplete reporting |
| R2a (§10) | Δ=.26, 99% interval [.15,.37]: DIFFERS | Δ=.04 interval [-.06,.09]: EQUIVALENT; Δ=.17 interval [-.02,.35]: INCONCLUSIVE |
| R2a prerequisites (§10/§11) | R0 and R0-F PASS at the compared lead | R0 PASS only at another lead or R0-F FAIL/INSUFFICIENT: no publish route |
| R2b eligibility and floor (§10) | 30 eligible cases with S observation-confident and Fc confident at 0 | No eligible action: omit case; 29 eligible cases: NOT EVALUABLE |
| R2b loss/censoring (§10) | S loss unobserved to 6 and Fc loss at 4: S later | Both unobserved: tie; Δ=0 alone does not establish same-lead loss |
| R2b outcomes (§10) | Δ=.31 interval [.12,.48]: OUTLIVES; -.27 [-.44,-.09]: PRECEDES | .01 [-.07,.08]: NO DIRECTIONAL PREFERENCE; .12 [-.05,.30]: NO ORDER DETECTED |
| R2b calibration prerequisites (§10/§11) | Every lead R0/R0-F PASS or NOT EVALUABLE | Either FAIL or INSUFFICIENT at any lead: no ordering publish route |
| R2c (§10) | Answer at or below T_h and report its errors/refusals | Treating rule-answered as automatically confident is invalid |
| R3/R3b/R6 accuracy/agreement (§10) | Accuracies, probability bins, κ and counts reported | High κ or confidence share called calibration without actual outcomes: invalid source use |
| L7 strong crude wording (§11) | Accuracy .78 and betting one-sided upper .82 | Accuracy .88, or upper .91: neutral wording |
| L8 overconfident wording (§11) | Accuracy .70 and upper .78 | Accuracy .85 or upper .90: word not licensed |
| CNN validity/service halt (§7.4/§14) | Valid member in every action; existing services continue | Invalid under one action: drop across all; requiring Qwen shutdown: halt |
| R7 (§10) | Two-scale truth, one-scale inference and reported fit/calibration | Claiming same-class calibration from mismatched truth: invalid; optional arm may be cut |
| Publish / kill / otherwise (§11) | R0 PASS at 2 plus valid R2a/R2b/R5 route: publish condition | R0 FAIL at both 2/3 or coverage<.85: kill; neither: Todd decides |
| Licensed sentences (§11) | L1 with both calibration passes; L4 with R0 pass | L1 without Fc pass, or outlives from R2a alone: unlicensed |
| Stage 1a diagnostics/coverage (§13) | 1/20 diagnostics failures and 15/20 covered: continue | 2/20 failures or 14/20 covered: halt |
| Stage 1a disagreement/rerun (§13) | >5% substantive S disagreements then fresh 4x posterior agrees within 1%: continue, label RML biased | Repeat posterior disagreements >1%: halt; threshold crossings alone never halt |
| Stage 1 strong (§13) | R0 PASS at 2, route prerequisites, and R2a abs(Δ)=.26, R2b abs(Δ)=.31, or R5 margin=.16 with both McNemar p≤.01 | R2b abs(Δ)=.18 or missing route prerequisite: not strong; R0 FAIL both 2/3: stop/report |
| Runtime projection and cuts (§13/§14) | All required costs/compile/diagnostics plus rerun allowance fit 12h after permitted cuts | >12h after R7,A,R6@3,RML-conf,P/B-other-leads,R5@3 cuts: halt; never cut required core |
| Freeze / blind order (§4/§14) | Freeze committed before confirmation; outputs hashed before realized outcomes | Confirmation reading before freeze: halt |
| Illustrative selector (§13) | First confirmation index satisfying all declared predicates | Choosing the prettiest or a later matching case: invalid selector use |


### Amendment-specific witness additions

| Axis/filter/classification | Passing / first branch | Failing / other branch |
|---|---|---|
| v2.2 CP/McNemar exact audit (§10) | Errors <1e-10/<1e-12 against exact reference | Larger discrepancies: audit halt |
| v2.2 null audit (§10) | 20,000 panels/config, false-PASS .02685 or noncoverage .00425 below nominal+2SE | Rate .07 at nominal .05, SE .0018: audit halt |
| v2.2 betting capital (§10) | Predictable bet, values in [0,1], caps .75/m and .75/(1−m), prefix maximum | Bet uses next case, invalid range, or terminal-only capital: implementation failure |
| v2.2 answer-ratio bound (§10) | For all cases use x=(correct−m*answers)/8+m | Removing empty cases without accounting or using answers as independent trials changes target |
| v2.2 grid inversion (§10) | Retain every unrejected real mean in an outer approximation | x=1 for 200 cases: literal interval [.963,1] omits unrejected .9629: failed source claim |
| v2.2 descriptive bootstrap (§10) | Redraw zero denominator and report count; all-empty population NOT EVALUABLE | Retain undefined ratios or use descriptive bounds to gate: invalid |
| v2.2 power table (§10) | All 12 accuracy/count cells, plus both R2a deltas, reported with MC SE | Missing cells: incomplete audit; low power itself is not a new halt |
| R0 answer-point safeguard (§10) | Case lower .91 and answer point .91: may PASS | Same case bound with answer point .89: not PASS |
| R0/R0-F INSUFFICIENT (§10) | Evaluable lower<.90 and upper≥.90 | Calling this FAIL/KILL or permitting it for an R2b prerequisite violates v2.2 |

## Gate summary

Stage: pre-data statistical audit and full v2.2 spec gate, HALT. Headline value: unmeasured. Change: the original boundary defect is repaired by betting/exact tests, all prescribed Monte Carlo checks pass, and the required power table is complete; a continuous-mean grid inversion gap remains. Largest risk: the claimed coverage guarantee is carried from a capital test to an interval that can exclude a mean without capital rejection. Recommendation: stop for a targeted inversion amendment and rerun the necessary audit/gate before Step 0. No scientific kill, threshold relaxation or rescue run is implied.
