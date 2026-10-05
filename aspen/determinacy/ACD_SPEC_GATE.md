# ACD spec integrity gate — v2.3 — proceed with resolution rules

The entire v2.3 work order was read; sources/WO_v2.3.md archives it. Todd authorizes Stage 0 through the Stage 1 gate. Only H1–H3 stop this run. Step 0b at eb87279 is preserved, with no new selector or model review.

## Checks 1–9 including 5a

| Check | Assessment |
|---|---|
| 1 Feasibility | PASS: both operational outcomes constructed in the witness inventory. |
| 2 Independence | PASS as designed: exploratory development, future disjoint confirmation, samplers observe no hidden truth; signed calibration scored separately. |
| 3 Referents | PASS: case-average R0, separate answer point, fixed pre-probe pair, same-modal-answer climate confidence and specified refit order/seed roles. |
| 4 Source class | PASS for the repaired statistics: m-independent predictable bets, nonnegative factors, monotone capitals, outward integer inversion. Synthetic null/monotonicity/exact checks pass. Development remains exploratory and RML approximate. |
| 5 Examples | PASS: equations, not illustrative bounds, define outcomes. |
| 5a Witnesses | PASS: every constructed example is a synthetic hypothesis under test. |
| 6 Surprise | PASS: sign may precede Fc, covariance may not cancel, Q may lose to F/V/R, sampler diagnostics and coverage can fail and will be reported. |
| 7 Null | PASS: climatological and random-site nulls; Q now must beat random as well. |
| 8 Separability | PASS: point margin against max(V,F,R), all three exact paired tests, accuracy/count/coverage safeguards. |
| 9 Selector separation | PASS: blinded competing selector at eb87279, overlap and divergence already reported. One independent framing, not multiple negatives. |

## Findings and resolutions

- §6 says knowledge of true forcing makes the observation share conservative. That is an information heuristic, not a pointwise proof for every action/lead. **R-other:** report the actual null answer shares and its information advantage; claim only the declared “not climate-confident” classification, not a proven ordering of posteriors.
- The independent selector proposed expected-regret targeting and conflicting-scenario separation beyond Q/F/V/R. These are **untested comparators**, recorded under **R-other**; L6 names only the tested arms and does not claim best possible targeting.
- Wilks truth coverage is approximate at this nonlinear finite-noise operating point. **R-other:** report measured Δχ² coverage, not posterior probability or model identification from it. Coverage findings use R-cov if triggered.
- Old §17–§19 halt descriptions are archival; current §14 and §20 govern. No additional halt or threshold change is inferred from them.

The original bootstrap and grid findings are repaired by §10 v2.3; R-stat did not fire in the new audit. The previous witness inventory below is retained for operational geometry, with v2.3 overrides explicit: failed numerics/coverage/diagnostics trigger resolution rules rather than halts; R0 and R0-F have four statuses; R2 prerequisites and matching bound direction apply; crossed intervals license less; Q must beat V,F,R and use exact CP/McNemar. All hypothetical bounds below are classifier inputs, never observed outcomes or anchors.

## Hard-stop controls

All sampling/targeting observational input goes through acd_protocol.load_observed and logs the observed-only access. Truth-bearing arrays are read only for Step 0 item 7, scoring/coverage, authorized dt recomputation, and the designed probes. No confirmation access exists in this run. No service stop, cloud compute, training or Baccus close-out mutation is authorized or performed. JAX_PLATFORMS=cpu and float64 are set before JAX import; modules are prefixed acd_.

## Selector provenance

GPT framed trajectory versus intervention effects and covariance; Claude specified the questions, targeting/comparators, thresholds and leads after AFD exploratory results. Actions and energy/windows are inherited. The blinded Codex competing selector at eb87279 overlaps S/P, broadens B to include no-action, partially overlaps Fc, and proposes Q-family targeting plus the two untested algorithms above. Primary selector omissions are not independent empirical negatives. Extra cost-derived regret/backfire/nine-action readings stay descriptive.

## Complete operational witness inventory



**Every input in the following table is a synthetic hypothesis under test (check 5a).** Unless a row varies a prerequisite, assume all other prerequisites pass, ample cases, no ties, and valid diagnostics. Bounds shown are hypothetical inputs to classifications. They do not validate the grid inversion. The v2.2 formula and all audit inputs are synthetic, not empirical anchors. This table assesses scientific axes, filters and thresholds without running experiment data.

| Axis/filter/classification (WO section) | Passing / first branch | Failing / other branch |
|---|---|---|
| Scientific definition agreement (§3) | Code has the exact declared cost/window/action | Cost uses terminal energy instead of window energy: R-def follows inherited code |
| Seed leaf disjointness (§4) | Distinct stream/case/sub leaves outside inherited IDs | Reused leaf or inherited ID: fail assertion |
| Observation likelihood / prior support (§5) | F=8, finite 40-state vector | F=10.1 has zero prior density; nonfinite state invalid |
| Posterior parameter and log-likelihood diagnostics (§5) | All R-hat=1.005, ESS=600 | One R-hat=1.02 or ESS=399: rerun; persistent fail excludes |
| Gate functional diagnostics (§5) | All D_k/J_8 at 2/3 LT meet 1.01/400 | Thinned ESS=300: forecast full draws; persistent failure follows rerun rule |
| Divergences (§5) | 40/4000=1% | 41/4000>1%: fails diagnostics |
| F boundary / convergence reporting (§5) | Interior minima; all starts converge | F=6 or optimizer fails: report, not automatic independent halt |
| Threshold uncertainty (§5) | p=.94, se=.01: flagged | p=.98, se=.005: not flagged |
| Panel diagnostic exclusion (§5/§14) | 10/200=5% excluded | 11/200>5%: R-diag flags exclusions |
| Gaussian implementation mean/variance (§5) | Every error 3 MC SE; both extreme-direction variances off 6% | Any mean/variance error 5 MC SE or extreme variance off 25%: R-impl doubles and rechecks |
| Joint FD adjoint (§5) | Maximum absolute error 9e-7 | Error 1e-6: R-grad uses JAX AD |
| Multi-start minimum bookkeeping (§5) | Lowest χ² retained across four starts, RML and posterior | Retaining a higher start's χ² is an implementation failure |
| Truth coverage χ² (§5) | Δχ²=56.90: covered | Δχ²=57: not covered |
| Completed-panel coverage (§5) | 170/200=.85: no R-cov flag | 169/200<.85: R-cov reports development; KILL on future confirmation |
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
| dt answer and classification checks (§6) | Every lead ≤3 has .004 answer changes and .008 class changes | Any lead has .006 answer changes or .011 class changes: R-dt halves and rechecks |
| Null (§7.1) | 4096 independently seeded spun-up states and mean over states/leads | Observation-conditioned states called climatology or ensemble used as truth: invalid |
| Crude/RML member counts (§7) | 128 crude draws; 112/128 valid RML | 111/128 valid RML: short case; short cases use available members under R-rml |
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
| Stage 1a diagnostics/coverage (§13) | 1/20 diagnostics failures and 15/20 covered: continue | 2/20 failures or 14/20 covered: R-diag/R-cov flags |
| Stage 1a disagreement/rerun (§13) | >5% substantive S disagreements then fresh 4x posterior agrees within 1%: continue, label RML biased | Repeat posterior disagreements >1%: R-rml flags and retains rerun; threshold crossings alone never halt |
| Stage 1 strong (§13) | R0 PASS at 2, route prerequisites, and R2a abs(Δ)=.26, R2b abs(Δ)=.31, or R5 margin=.16 with all three McNemar p≤.01 | R2b abs(Δ)=.18 or missing route prerequisite: not strong; R0 FAIL both 2/3: stop/report |
| Runtime projection and cuts (§13/§14) | All required costs/compile/diagnostics plus rerun allowance fit 12h after permitted cuts | >12h after R7,A,R6@3,RML-conf,P/B-other-leads,R5@3 cuts: R-time reduces population then draws; never cut required core |
| Freeze / blind order (§4/§14) | Freeze committed before confirmation; outputs hashed before realized outcomes | Confirmation reading before freeze: halt |
| Illustrative selector (§13) | First confirmation index satisfying all declared predicates | Choosing the prettiest or a later matching case: invalid selector use |


### v2.3 statistical and sensitivity witnesses

All are synthetic hypotheses under test, rather than observed anchors.

| Rule | First branch | Other branch |
|---|---|---|
| Monotone capital | Predictable m-independent bet ≤.9; every factor ≥.1 | m-dependent betting cannot license integer bisection |
| Continuous inversion | 200 ones: 99% interval [.970,1] | The historical [.963,1] excluded unrejected .9629 under v2.2 |
| Audit | Exact matches and null rate ≤nominal+2SE | Larger discrepancy: R-stat repairs/rechecks, then conservative bound |
| R0 exclusion sensitivity | Primary PASS and included-case PASS | Primary PASS, included-case FAIL: reported FAIL |
| Crossed bounds | Lower ≤upper and matching direction licenses route | Lower >upper: R2a INCONCLUSIVE/R2b NO ORDER DETECTED |
| R5 random safeguard | Margin ≥.10 and p≤.01 against V, F and R | F/V beaten but R not beaten: no Q-BEATS |
| R-time | Projected stages fit 12 hours | Cut permitted arms/leads, population 60 then draws 500; report and continue |

## Runtime resolution ledger

The complete triggered-rule log is runs/resolutions.jsonl. Scientific findings and exclusions will be summarized in the Stage 1 reading. This gate does not authorize confirmation or a publish claim.
