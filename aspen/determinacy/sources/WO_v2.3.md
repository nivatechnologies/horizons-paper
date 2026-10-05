# Aspen kill test: counterfactual confidence in partially observed chaotic systems (v2.3)

**Status.** v2.3. Todd's go covers Stage 0 through the Stage 1 gate.
- v2 applies GPT's design review of v1 (2026-10-04). The disposition and differential prediction are in §17.
- v2.1 applies GPT's execution review of v2 (2026-10-04): §18.
- v2.2 replaces the percentile-bootstrap gate bounds after the executor's spec-gate halt (2026-10-05): §19.
- v2.3 makes every betting bound a monotone, continuous-parameter inversion, and replaces halts with resolution rules so the run proceeds to the Stage 1 gate (Todd, 2026-10-05): §20.
- The main change: the construct is now probabilistic. An answer is *confident* when its posterior probability under the declared law is at least 0.95, and confident answers are scored against realized outcomes. No sentence claims that the observations fix an answer, or that every consistent instance agrees.
- This is a pivot under [[T_Research-Paper-Guideline]] §4, after [[WO_Aspen-Forecast-Decision-Kill-Test-2026-10-04]] closed on 2026-10-04 (its reference ensemble was built the same way as one arm).

**Question.** For one observed instance of a chaotic system, the factual future and the future under an intervention share most of their uncertainty. Does that uncertainty cancel in their difference, so the sign of the intervention's effect stays confidently answerable at leads where the factual forecast is not? Or does the intervention decorrelate the two futures and lose that sign first? And which extra measurement makes an open decision question confidently and correctly answerable?

**Origin of the hypothesis (exploratory, not evidence).** On the AFD Stage 1 test panel ([[R_Aspen-Forecast-Decision-Realized-Check-2026-10-05]]):
- N-win (4D-Var fits of perturbed observation windows, forcing fixed) picked the realized best of 8 actions in 88.5%, 68.5%, 56.5% and 39% of cases at 2, 3, 4 and 6 LT. Chance is 12.5%, and the best fixed action scored 14% at 6 LT.
- The perturbed-last-frame reference ensemble agreed with the realized best in 76%, 46.5%, 31% and 17% of cases.

These numbers selected the leads and thresholds below. That panel is this WO's development panel. Only the confirmation panel counts as evidence.

**Why this design cannot repeat the AFD flaw.** No ensemble serves as truth anywhere. Every accuracy is scored against the single realized trajectory of the hidden true state under the true forcing, which no sampler sees. The climatological null and the comparator ensembles are never references.

## 1. Headline contract (for Todd's go)

| Field | Content |
|---|---|
| Headline sentence (assembled only from §11) | With 11 noisy snapshots spanning 0.84 Lyapunov times, the posterior under the known law answers the sign of a small intervention's effect on window energy with at least 95% probability for X% of case–action questions at 2 LT, against Z% for the sign of the unforced window-energy anomaly. Averaged over cases, confident intervention-sign answers that climatology alone does not give are right W% of the time [L2]. The factual and counterfactual futures share their uncertainty: their posterior correlation is ρ, so the difference carries c of the summed uncertainty [L4]. Four measurements targeted at the decision question turn C_Q of open decision questions into confident, correct answers, against C_best for the best of spread-targeted, forecast-targeted and random measurements [L6]. |
| Revelation | **Now:** predictability in chaotic systems is studied per observable at the ensemble or climate level (Lorenz's second kind; fluctuation–dissipation response). Intervention experiments on Lorenz-96 choose actions from ensemble forecasts and observations are targeted at forecast error, so an intervention's consequence is treated as knowable about as long as the forecast it acts on. **Instead:** for one observed instance, the confidence horizon of an intervention's effect is its own quantity. It is set by how much uncertainty the factual and counterfactual futures share, measured here against the forecast sign on the same posterior and explained by the measured covariance. Measurements chosen for the decision question resolve it where measurements chosen for the forecast or for state spread do [or do not]. |
| Contribution beyond prior work | Aalaila et al. 2026 list as open the temporal windows within which counterfactual reasoning stays tractable. Majda, Abramov and Gershgorin 2010 give ensemble-level response skill. Kreutz, Raue and Timmer 2011 give per-prediction profile likelihood. Lorenz and Emanuel 1998, Xie et al. 2013, Saito and Kotsuki 2026 and Hashimoto et al. 2026 target observations at analysis or forecast error. Sun, Miyoshi and Richard 2023 and Mitsui et al. 2025 run LETKF-conditioned interventions on Lorenz-96 without assessing whether an instance's intervention effect is predictable. This paper adds four things. (1) Instance-level posterior confidence in intervention signs against the forecast sign on the same posterior, separated from what climatology alone gives. (2) The covariance mechanism. (3) Calibration against realized truth. (4) Measurement targeted at the counterfactual question, against forecast-targeted and spread-targeted measurement. |
| The incumbent's most natural fixes, and the arms that measure them | **Forecast-horizon rule** (answer inside the forecast's confident lead, abstain past it): R2c. **Perturbed-last-frame ensemble:** R3. **Randomized-maximum-likelihood ensemble smoother:** R3b. This is the exact-gradient member of the perturbed-observation family that Lorenz and Emanuel found best. **A learned emulator's perturbed-input ensemble:** R6, using CNN-20k. **Spread-targeted and forecast-sensitivity-targeted measurement:** R5. |
| Reader, and what they do differently | Predictability, data-assimilation, intervention (control-simulation) and ML-weather physicists, plus world-model researchers. They would report an intervention's confidence horizon separately from the forecast's, and target measurements at the decision question. |
| Reader's operating point | Lorenz-96, N = 40, true F = 8. All 40 sites are observed every 0.05 time units for 0.5 time units (11 frames, 0.84 LT) with Gaussian noise of 0.02·SIGMA. Interventions are persistent forcing patterns at 2% of F. The declared model class is one-scale Lorenz-96 with unknown state and unknown uniform forcing in [6, 10]. **Guideline deviation for Todd:** a toy setting carries the headline. The bridge is that Lorenz-96 is the standard testbed of the targeting and control-simulation literatures cited above. |
| Null models | Climatological ensemble at the true forcing (§7.1). Random measurement sites (§8). |
| Niva arm | The posterior over (state, forcing) under the declared law, sampled by a gradient-based MCMC with checked diagnostics (§5). The solver calculates every question for every posterior draw at query time, followed by question-targeted measurement (§8). |
| Publish threshold | On the confirmation panel, R0 PASS at 2 LT, and at least one route (each needs R0 PASS at its own lead): **R2a DIFFERS** at 2 or 3 LT (which also needs R0-F PASS at that lead); **R2b OUTLIVES or PRECEDES** (which needs R0 and R0-F to be PASS or NOT EVALUABLE at every lead); **R5 Q-BEATS** at 2 or 3 LT. |
| Kill threshold | On the confirmation panel, R0 FAIL at both 2 and 3 LT, or truth coverage below 0.85. |
| Pre-mortem | **(1) "Predictability depending on the observable is known."** The claim is the instance-level paired-difference horizon against the forecast on the same posterior, with its covariance mechanism (R1m) and realized calibration. Kreutz et al. and Lorenz's second kind are cited as the frame. **(2) "Sampler artifact."** NUTS with diagnostics and an implementation check on a known Gaussian (§5); an independent RML cross-check on every case, with a 20-case validation before the full development run; realized calibration (R0); multi-start MAP. **(3) "Perfect-model twin."** Scope is the declared model class; a χ² goodness-of-fit is reported per case; R7 runs a two-scale truth (optional). **(4) "No LETKF arm."** Declined as class D; reason in §17. |
| Venue and date | Aspen "World Modeling for Physics" abstract, due Oct 9, 23:59 AoE. ACP participant application due Oct 15. |
| Todd go / no-go | **GO** for Stage 0 through the Stage 1 gate (Todd, 2026-10-05). Freeze, confirmation and CNN inference need a separate go. |

## 2. Spec integrity gate

> **Spec integrity gate.** Before executing, run checks 1 to 9 including 5a in [[T_Spec-Integrity-Gate]] against this work order and report the results in `ACD_SPEC_GATE.md`. For each scoring axis, filter, threshold or classification here, state a concrete passing input and a concrete failing input, and cite each or label it a hypothesis under test per check 5a (§12 gives the author's; the executor checks them). For any selector this WO contains or relies on, report who authored it and how check 9 is satisfied.
>
> **For this run (Todd, 2026-10-05), a failed check does not halt.** The executor records the finding in `ACD_SPEC_GATE.md`, applies the matching resolution rule in §14, and continues. Where no rule matches, it takes the reading that licenses less and flags it for the Stage 1 gate summary. Only the hard stops in §14 halt.

**Selector provenance**
- **Question family:** GPT framed trajectory versus intervention difference versus sign or ordering (2026-10-04). The covariance mechanism and the spread-targeted comparator are also GPT's (design review, 2026-10-04). Claude specified the question types, the thresholds, the targeting rules and the comparators.
- **Inherited:** the action set (blinded Codex run 1, AAH Step 0) and the observable and window predicate (AAH; AFD Amendment 1).
- **Authored by Claude after seeing the AFD development-panel numbers:**
  - leads 2 and 3 LT;
  - confidence threshold 0.95;
  - R0 bound 0.90;
  - R2 margins 0.15 and 0.20;
  - R5 margin 0.10;
  - probe precision.
- **Independence** comes from the confirmation panel, whose seeds are disjoint from every AAH and AFD stream.
- **Check 9: Step 0b.** A blinded Codex selector run from a different starting point; overlap reported (§3). Step 0b needs no data, so it runs first. The spec gate is signed off only after it, with check 9 assessed on its output.

## 3. Step 0: read-only verification at `paper/aspen-2026-10-forecast-decision` @ `1b1094a`

Confirm each item against the code and record it in `ACD_STEP0.md`. Claude read these files on 2026-10-04; the executor verifies them and does not trust them.
1. **Protocol:**
   - `LT = 0.5928295944308761`;
   - `SIGMA = 4.312600593723798`;
   - `LEADS = [0, 1, 1.5, 2, 2.5, 3, 4, 6]`;
   - `OUT = 0.05`;
   - `TICKS` 0..83;
   - `WINDOWS` by the unrounded predicate (Amendment 1).
2. **Observations:** `physics.history(name, case, dt)`:
   - spin-up from 8 + N(0, 1) for 50 LT at F = 8;
   - 11 frames at 0.05 spacing;
   - y = true + 0.02·SIGMA·N(0, 1);
   - the last frame is t = 0.
3. **Actions:**
   - `protocol.patterns()` gives 8 unit-RMS rows. Action k is forcing F + 0.16·p_k; index 8 is no action.
   - Realized outcome: `actual = simulate(true[-1], 8 + 0.16·[p; 0])`, and `actual_cost = costs(actual)` has shape (9, 8).
4. **Cost:** the window mean of E = ½·mean(x²).
5. **Timestep:** `runs/numerics/dtcheck.json` has `chosen_dt = 0.01`, status PASS.
6. **Fitting code:**
   - `extras.objective` is Σ(state − window)²/440 over 11 frames;
   - its adjoint is exact RK4 reverse mode;
   - `fit_member` uses L-BFGS-B, maxiter 200, F fixed at `identify(y, dt)`;
   - validity requires RMS ≤ 10·SIGMA.
7. **Development inputs:**
   - `runs/test/input_{c:03d}.npz` for c = 0..199 on sulaco, with hashes matching `AFD_ARTIFACTS.md`;
   - `history("afd-observation-test", c, 0.01)` reproduces them bitwise;
   - stored `actual_cost` in `runs/test/cpu_{c:03d}.npz` matches a recomputation to ≤ 1e-12.
   - A hash mismatch with `AFD_ARTIFACTS.md` is recorded, and the stored file is the data (R-def).
8. **CNN-20k:**
   - `inputs/CNN-20k.pt` and its hash;
   - window length and `sigma` normalization;
   - action channel `0.16·p_k/sigma`;
   - whether the zero action lies inside the training action distribution. Report and continue.
9. **Two-scale kernel (R7 only):** `rhs2` (h = 1, c = 10, b = 10 as coded) and `two_scale_state_dt = 0.001`.

**Step 0b: blinded selector (check 9).**
- **Complete at `eb87279`; it is not rerun.** Check 9 is assessed on that output.
- A Codex targeting rule outside Q, F, V and R is listed in `ACD_SPEC_GATE.md` as an untested comparator, and L6 names only the arms tested.
- The original instruction, kept for the record: before any data and before the spec-gate sign-off, run OpenAI Codex CLI with exactly the prompt below and nothing else, and commit the prompt and verbatim answer as `aspen/determinacy/CODEX_SELECTOR.md`.
- Report the overlap with this WO's question types (S, P, B, Fc) and targeting rules (question, forecast, spread, random).
- Any Codex question type that can be computed from saved per-draw costs is added as a reported reading. It cannot be a gate or a publish route.

> A chaotic system (the Lorenz-96 model, 40 variables, forcing F) is observed at all sites with noise for a short window. An operator can apply one of eight small persistent forcing patterns, or none, and cares about one scalar outcome: the mean energy over a later time window. Using only the observations and the known equations, list the questions about this particular observed instance that a physicist would most want answered before acting, and for each say how one would judge whether the available observations are sufficient to answer it. Then propose three rules for choosing four additional precise point measurements, taken at the decision time, that would best help answer such questions.

**Limit on reuse.**
- Where code and this WO differ on an **inherited** definition (observation model, actions, cost, windows, realized outcome), the code's rule governs, as in AFD Amendment 1. The difference is recorded in `ACD_STEP0.md` and the run continues.
- **New** definitions (questions, confidence, posterior, readings) follow this WO.
- If the development inputs do not reproduce bitwise, the stored inputs are the data. Record it and continue.
- Non-definitional details follow the code.

**Branch.**
- `paper/aspen-2026-10-determinacy` from `origin/paper/aspen-2026-10-forecast-decision` @ `1b1094a`; work under `aspen/determinacy/`.
- Import `protocol.py` and `physics.py` unchanged, and record their hashes. `extras.py` and `campaign.py` are not edited.
- **Module names:** new modules carry an `acd_` prefix (e.g. `acd_campaign.py`, `acd_stats.py`), so nothing shadows `campaign.py` or Python's `statistics`.
- **Outputs:** `aspen/determinacy/runs/{audit,dtcheck,null,dev}/`. The chosen dt goes to `aspen/determinacy/runs/numerics/acd_dt.json`. Inherited files under `protocol.ROOT/runs/` are read-only.
- **Python packages:** installing into the ACD virtual environment is authorised.
  - JAX is installed CPU-only (`jax[cpu]`), and every entry point sets `JAX_PLATFORMS=cpu` and `jax_enable_x64=True`, so nothing touches the GPU used by the Qwen services.
  - A JAX copy of the RK4 map is allowed. On dtcheck case 0 it must match `physics.step` over the 11 frames to within 1e-12 relative; the result is recorded.
  - If JAX cannot be installed, the hand-written sampler and adjoint are used, and the missing R-grad and R-impl fallbacks are flagged. If R-grad then triggers, MAP and RML use the state adjoint with a centred finite difference (eps 1e-6) for ∂/∂F.
  - If the JAX copy fails the 1e-12 match, it is not used, as if JAX were unavailable.
- Push to `origin`. No AI attribution in commits.

## 4. System, panels and realized outcomes

- **System:** Step 0 items 1–5. RK4, dt 0.01, float64. All eight leads, with window [T, T + 1] LT by the inherited predicate. Readings use 2 and 3 LT, except R2b and its R0 and R0-F prerequisites, which use all eight leads.
- **Panels:**

  | Panel | Cases | Observations | Purpose |
  |---|---|---|---|
  | Development | 200 | existing `afd-observation-test`, cases 0–199 | Stage 1a validation (cases 0–19), then the Stage 1b kill test. Realized outcomes were already seen in AFD exploratory checks |
  | Confirmation | 200 | new `acd-observation-conf`, via `history()` | All evidence |
  | dt check | 8 | `acd-dtcheck` | Stage 0 |
  | Two-scale (R7, optional) | 50 | `acd-twoscale` | Model-error sensitivity |

- **Realized outcome:** J*(k, T) from `actual`, with the hidden true state and F = 8. Realized answers come from J*.
- **Blind order on the confirmation panel:** for each case, the observations are generated and hashed; then every sampler's outputs are written and hashed (posterior, RML, crude, CNN); only then is `actual` computed.
- **Seeds:**
  - `aspen/determinacy/acd_protocol.py` defines `acd-observation-conf`, `acd-posterior-{dev,conf}`, `acd-sampler-{dev,conf}` (RML perturbations), `acd-crude-{dev,conf}`, `acd-climatology`, `acd-measure-{dev,conf}`, `acd-dtcheck`, `acd-bootstrap` and `acd-twoscale`.
  - `acd_protocol.py` defines `ACD_IDS = {name: 1_200_000 + i}` in the listed order. It asserts no overlap with `protocol.IDS.values()` or `AAH_IDS`, then calls `protocol.IDS.update(ACD_IDS)` at import. `protocol.rng` and `physics.history` then serve the ACD names, and both files stay byte-unchanged (hashes recorded).
  - **Sub roles,** fixed in `acd_protocol.py` in Stage 0, recorded in `ACD_NUMERICAL_REPORT.md` and copied to `ACD_FREEZE.md`:
    - history: sub 0 initial state, sub 1 noise (inherited);
    - `acd-sampler-{p}`: sub 0, member m, gives ε_m;
    - `acd-crude-{p}`: sub 0, member, gives ε′;
    - `acd-posterior-{p}`, member = chain: sub 0 primary, sub 1 R-diag rerun, sub 2 Stage 1a rerun, sub 10 + arm (Q, F, V, R, A = 0–4) for R5 refits and sub 20 + arm for their reruns, with action = the index of T in `LEADS`;
    - `acd-measure-{p}`, action = the index of T in `LEADS`: sub 0 η, sub 1 random-arm sites;
    - `acd-dtcheck`: cases 0–7 via history; sub 2 RML ε, sub 3 crude, sub 4 posterior chains, sub 5 implementation-check sampler, sub 6 R-diag rerun;
    - `acd-climatology`: sub 0, case = null state index;
    - `acd-bootstrap` sub: R0 answer-level 0, R1 1, R1m 2, R2c 3, R3 4, R3b 5, R6 6, coverage 7.
  - Assert leaf uniqueness over all of these.

## 5. The posterior (the Niva arm) and its checks

**Declared model and prior.**
- θ = (x_first ∈ ℝ⁴⁰, F). H_t(θ) is the RK4 state at frame t = 0..10.
- Likelihood: y_t,i ~ N(H_t(θ)_i, (0.02·SIGMA)²), independent.
- Prior: x_first,i ~ N(0, (10·SIGMA)²) independent, which is flat relative to the likelihood; F ~ Uniform(6, 10). The prior is stated in the paper's Setup.
- χ²(θ; y) = Σ(H − y)²/(0.02·SIGMA)², which equals 440·val/(0.02·SIGMA)² on `extras.objective`'s scale.

**Sampler.**
- NUTS (Hoffman and Gelman 2014) with a dense mass matrix adapted in warmup. NumPyro or BlackJAX in float64 is recommended. A sampler written from scratch around the existing adjoint is acceptable only if it passes the implementation check below.
- **Order per case:**
  1. RML fits (§7.3).
  2. MAP from 4 starts. The fourth starts from the member with the lowest χ²(θ; y).
  3. A provisional χ²_min over the MAP fits and the members fixes RML validity.
  4. NUTS, 4 chains with 1000 warmup and 1000 draws each, started from the 4 lowest-index valid members.
  5. The final χ²_min includes the draws and is used for coverage and fit.

  MAP and RML minimize χ² with the prior omitted.
- **Thinning:** keep draws ⌊i·D/128⌋, i = 0…127, in each chain, giving S = 512. D is the number of post-warmup draws per chain (1000 unless R-impl or R-time changes it).
- **Forecasts:** each draw θ_s = (x_first,s, F_s) gives x_s(0) = H_10(θ_s), the frame-10 state of the same RK4 map at the chosen dt. It is forecast with `physics.simulate(x_s(0), F_s + 0.16·[p; 0], dt)` over all 84 ticks, with index 8 as no action, and J_s(k, T) = `costs(·)`. RML members use their fitted F_m. The crude sampler uses F̂ = `identify(y, dt)`.
- **Saved per draw:** θ_s, x_s(0), J_s, and the per-tick sums that §9's divergence ratio needs.

**Diagnostics, per case.**
- Split R-hat ≤ 1.01 and bulk ESS ≥ 400 for all 41 parameters and the log-likelihood (Vehtari et al. 2021).
- **Gate functionals:** split R-hat ≤ 1.01 and bulk ESS ≥ 400 on the forecast draws for D_k (k = 0..7) and J_8 at 2 and 3 LT. Different functions of one chain can mix differently.
  - If a functional falls short, forecast all 4·D post-warmup draws for that case and recompute. That set then replaces the 512 draws for every question in that case, with ⌈0.95·4D⌉ as the confidence threshold.
  - If a functional is still short with all 4·D draws, the case fails diagnostics: rerun once with 2000 warmup, then apply R-diag.
- **Monte Carlo error of each answer probability:** se = sqrt(p̃(1 − p̃)/n), with p̃ = (k + ½)/(N + 1).
  - k of the N draws give the event, and n is the indicator's bulk ESS (n = N if the indicator is constant).
  - A question with |p − 0.95| < 2·se(p) is flagged threshold-uncertain.
  - It keeps its point classification, and the flagged count is reported per type and lead.
- Divergent transitions ≤ 1% of draws.
- A failing case is rerun once with 2000 warmup. If it still fails, it is excluded and reported.
- The exclusion rate is reported with every reading. Above 5% it is flagged in the gate summary (§14, resolution rule R-diag).
- R0 is also computed with each excluded case's last run included. The reported status is the less favourable of the two, in the order PASS, INSUFFICIENT, FAIL; NOT EVALUABLE follows the primary computation. So exclusions cannot raise R0. L2 reports the primary W and B, with the included-case values beside them.
- Report F boundary contacts.

**Implementation check (Stage 0).**
- Sample a 41-dimensional Gaussian whose precision is the Gauss–Newton Hessian at the MAP of `acd-dtcheck` case 0.
- The sample mean and all 41 marginal variances must match within 4 Monte Carlo standard errors, and the variances along the largest and smallest Hessian eigendirections within 10%.
- If it fails: a hand-written sampler is replaced by NumPyro NUTS. If NumPyro fails, warmup and draws are doubled and the check is repeated once.
  - If the doubled check passes, production runs use the doubled settings, and the R-time projection includes them.
  - If it fails, production uses NumPyro at doubled settings and the finding is flagged (§14, R-impl).

**Joint adjoint (for MAP, RML and any hand-written sampler).**
- A new function in `acd_fits.py` (not an edit to `extras.py`) extends `extras.objective`'s reverse mode to return ∂/∂F as well (∂rhs_i/∂F = 1 through the RK4 stages).
- On case 0 of `acd-dtcheck`, at a non-optimal point, the maximum absolute error against centred finite differences (eps 1e-6) over all 41 components must be < 1e-6 on the code's scale. If it is not, MAP and RML use JAX automatic differentiation of the same RK4 map. Record it and continue (§14, R-grad).

**MAP, multi-start.**
- L-BFGS-B over 41 variables, F ∈ [6, 10], maxiter 500.
- 4 starts: (y_0, F̂ = `identify(y, dt)`), (y_0, 6.5), (y_0, 9.5) and the RML member with the lowest χ²(θ; y).
- χ²_min is fixed by the order above: provisional for RML validity, final for coverage and fit.
- Report the spread of minima across starts, boundary contacts and non-convergence.

**Coverage and fit (reported; gating as stated).**
- **Truth coverage:** Δχ²(θ_true) = χ²((true[0], 8); y) − χ²_min ≤ 56.94 = χ²₀.₉₅(41), with an expected rate of about 0.95 by Wilks' theorem.
  - On the confirmation panel, a rate below 0.85 is a KILL. On the development panel it is a reading reported at the Stage 1 gate, not a halt. Stage 1a (20 cases) flags a rate below 15/20.
  - Reported with a Wilson 95% interval.
- **Posterior rank of the true F** among the draws: histogram and uniformity test.
- **Goodness of fit:** χ²_min against χ²₀.₉₉(399) = 467.6; the expected flag rate is about 1%.

## 6. Questions and confidence

**Questions.** For every case and lead T, there are 38 questions:

| Type | Count | Question | Answers |
|---|---|---|---|
| S_k | 8 | Does action k lower window energy below no action? (D_k = J_k − J_8 < 0) | lower / not lower |
| P_kl | 28 | Is J_k < J_l? (k < l) | yes / no |
| B | 1 | argmin over k = 0..7 of J (ties to the lowest index) | 8 answers |
| Fc | 1 | Is the unforced window energy above the climatological mean J̄ (the sign of the unforced window-energy anomaly)? | yes / no |

J̄ is the null's no-action window cost, averaged over all its states and leads (§7.1).

**Definitions**, for a draw set of size S:
- **Posterior probability** p(q) is the share of draws giving the modal answer â(q). A tie between answers counts as not confident.
- **Confident:** p(q) ≥ 0.95, which means at least ⌈0.95·S⌉ draws.
- **Climate-confident:** at least 95% of the null's states give the sampler's modal answer â(q). The null's shares are computed once in Stage 0, per type, action or pair, and lead. Fc is expected not to be climate-confident, because J̄ is the null's own mean; the null's Fc share is reported.
  - The null knows F = 8 exactly, which the inference does not. That makes the observation-confident share conservative.
  - A climate-confident answer is never described as fixed by physics.
- **Observation-confident:** confident and not climate-confident.
- **Realized answer** a*(q) comes from J*. An exact zero difference counts as "not lower" or "no" and is logged.
- **Split stability (reported):** classification differences between chains {1, 2} and {3, 4}, per type and lead.

**dt check (Stage 0).** On the 8 `acd-dtcheck` cases:
- Forecast each draw's x_s(0), computed once at dt, under F_s + 0.16·[p; 0] at dt and at dt/2.
- Pool the 8 cases and 38 questions at each lead up to 3 LT.
- Pass if, at every lead up to 3 LT, at most 0.5% of (draw, question) answers and at most 1% of classifications differ.
- Otherwise, halve dt for every forecast and fit, including realized outcomes recomputed from the stored true state, and repeat the check once. Record it and continue with the finer dt (§14, R-dt).

## 7. Comparators

### 7.1 Climatological null
- 4096 states from 8 + N(0, 1) (`acd-climatology`), spun up 50 LT at F = 8.
- Each runs under every action and no action at all leads, giving the null shares and J̄.
- Computed in Stage 0.

### 7.2 Crude sampler (R3)
- 128 members x = y_10 + ε′, with ε′ ~ N(0, (0.02·SIGMA)²), and F = F̂.
- This is the N-last construction and the AFD reference's construction. Same questions and the same confidence rule.

### 7.3 RML ensemble smoother (R3b, the independent cross-check)
- M = 128 members (Kitanidis 1995; Oliver, He and Reynolds 1996): θ_m = argmin χ²(θ; y + ε_m), with ε_m from `acd-sampler-{panel}`, starting from (y_0 + ε_m,0, F̂). Same optimizer as the MAP.
- **Valid:**
  - finite;
  - RMS ≤ 10·SIGMA;
  - Δχ²_m ≤ 74.75 = χ²₀.₉₉₉(41);
  - at least ⌈0.875·M⌉ valid members per case. A short case is reported, and RML readings use the valid members it has.
- Unweighted RML is not an exact posterior sampler for a nonlinear forward model (Ba et al. 2021). It is reported as an independent estimate.
- **Comparison with the posterior** is made on the same signed event, never on each sampler's modal probability, which can hide opposite answers. The events are P(D_k < 0) for S_k, P(J_k < J_l) for P_kl and P(J_8 > J̄) for Fc.
  - z = (p_RML − p_post)/sqrt(se_RML² + se_post²), using §5's se with N = n = M_valid for RML. z = 0 when the two p are equal.
  - **Substantive disagreement:** |z| > 3.
  - Threshold-crossing disagreement is reported as a diagnostic, next to the share expected from Monte Carlo error alone.
  - Mean |p_RML − p_post| and RML's own realized calibration are also reported.
  - RML is approximate. Disagreement alone does not show the posterior sampler is wrong (§13, Stage 1a).

### 7.4 CNN-20k ensemble (R6; confirmation; sulaco GPU)
- 128 windows y + ε_m, using the same ε_m as RML, under the 8 patterns and no action, encoded as in `campaign.inference`.
- Per-member costs are saved. A member that goes invalid under any action is dropped for all actions.
- No training. Do not stop the Qwen vLLM services. If GPU memory is short, run inference with smaller micro-batches. If it still does not fit, R6 is cut and reported.

### 7.5 Forecast-horizon rule (R2c)
- T_h is the largest lead at which at least half the panel's Fc answers are confident.
- The rule answers every question at leads ≤ T_h with the posterior's modal answer and abstains beyond. If no lead qualifies, the rule abstains at every lead.

## 8. Targeted measurement (R5)

**Designated question.** At T ∈ {2, 3} LT, P_kl with k = min(a1, a2) and l = max(a1, a2), where a1 and a2 are the two actions among k = 0..7 with the lowest pre-probe posterior-mean J at T. They stay fixed through the refits.

**Population.**
- The first 100 cases by index in which P(a1, a2) is not confident at T, among cases not excluded under R-diag.
- The population is common to every arm. A refit that still fails diagnostics after its rerun counts as unresolved for that arm, and it never leaves the denominator.
- Fewer than 40 such cases is NOT EVALUABLE.

**Probe.**
- Each site measures x_i(0) at the decision time, with noise σ_probe = 0.1·0.02·SIGMA. The factor 0.1 is a design choice, not an instrument figure.
- z_i = x_true,i(0) + η_i. One η over all 40 sites is drawn per case and lead (`acd-measure-{panel}`), and all arms share it.

**Arms**, 4 sites each.

| Arm | Site rule |
|---|---|
| **Q, question-targeted** | Greedy: each added site maximizes the expected reduction in posterior variance of D = J_a1 − J_a2. It uses the draws' sample covariance with x(0) and the linear-Gaussian update, as in ensemble-sensitivity targeting (Xie et al. 2013). |
| **F, forecast-targeted** | The same rule, for the no-action forecast J_8 at T. |
| **V, spread-targeted** | The 4 sites with the largest posterior variance of x_i(0). This is the strategy family Lorenz and Emanuel 1998 found best for forecast error. |
| **R, random** | 4 sites uniformly without replacement. |
| **A, all** | All 40 sites, as the ceiling. |

**Refit.**
- The likelihood gains z_i ~ N(H_10(θ)_i, σ_probe²) for the arm's sites.
- NUTS settings and parameter diagnostics are unchanged (§5). The refit's gate functional is D = J_a1 − J_a2 at T, and the all-draws fallback applies to the designated question only. Chains start from each pre-probe chain's last draw, and no RML is run.
- Post-probe χ²_min is the lower of two values: an L-BFGS-B fit with the probe terms, started from the pre-probe MAP, and the best refit draw.
- p is recomputed from the 512 thinned refit draws, forecast under a1 and a2 only.

**Measures.**
- **Settled-correct share C_arm:** the fraction of the population that is confident after the probe and whose modal answer equals the realized answer.
- **Also reported:**
  - settled share regardless of correctness;
  - confident-but-wrong counts;
  - post-probe truth coverage, with probe terms included in Δχ².

**Q-BEATS at T.** All of the following:
1. C_Q − max(C_V, C_F, C_R) ≥ 0.10 (gate checks 7 and 8).
2. Exact one-sided McNemar tests (binomial on the discordant cases) of Q against V, against F and against R all give p ≤ 0.01. Requiring all three is an intersection–union test, so no further multiplicity correction applies.
3. Arm Q settles at least 20 questions, with a one-sided 95% Clopper–Pearson lower bound on their accuracy ≥ 0.80 (one settled answer per case, so the answers are independent).
4. Post-probe truth coverage for arm Q is ≥ 0.85.

C_A is reported as the ceiling.

## 9. Mechanism (R1m)

Computed from per-draw costs for every case, action and lead:
- Var(J_k), Var(J_8), ρ_k = Corr(J_k, J_8);
- the cancellation factor c_k = Var(D_k)/(Var(J_k) + Var(J_8)), which equals 1 − 2Cov/(Var(J_k) + Var(J_8));
- the signal-to-noise ratios z_D = |E D_k|/sd(D_k) and z_F = |E J_8 − J̄|/sd(J_8);
- the divergence ratio: the posterior-mean RMS of x_k(t) − x_8(t) against the posterior RMS spread of x_8(t), at each output tick.

**Reported:**
- panel medians and interquartile ranges per lead;
- P(confident) against z_D and against c_k, in bins;
- the lead at which the median ρ_k falls below 0.5;
- whether the leads where the S and Fc confident shares differ match the leads where c_k and the divergence ratio change. This is descriptive, with no comparison word.
- P(confident) is also reported against Φ(z_D), with the deviation from it. Agreement there is expected by construction.

## 10. Readings and statistics

**Statistics (v2.3).** The case is the statistical unit throughout. Every gate and route decision is valid at finite sample size; no gate or route uses a percentile bootstrap.

- **Betting bounds for bounded case-level means:** predictable plug-in bets after Waudby-Smith and Ramdas (2024), valid for any predictable λ ∈ [0, 1) by Ville's inequality. These are used for R0, for the L7 and L8 upper bounds, and for the R2a and R2b intervals.
  - **Inputs:** case values x_c ∈ [0, 1], taken in case-index order (t = 1..n), and a one-sided level α. R2 case-level differences d ∈ [−1, 1] enter as x = (d + 1)/2.
  - **Bets** (predictable plug-in, independent of the null value m):
    - λ_t = min(0.9, sqrt(2 ln(1/α) / (σ̂²_{t−1} · t · ln(t + 1)))), where α is the per-side level (α/2 for a two-sided α).
    - μ̂_t = (1/2 + Σ_{i≤t} x_i)/(t + 1) and σ̂²_t = (1/4 + Σ_{i≤t} (x_i − μ̂_i)²)/(t + 1), with σ̂²_0 = 1/4.
  - **Capitals:** K⁺_t(m) = Π_{i≤t}(1 + λ_i(x_i − m)) and K⁻_t(m) = Π_{i≤t}(1 − λ_i(x_i − m)), for every real m ∈ [0, 1]. Because λ_i ≤ 0.9, every factor is at least 0.1.
  - **Monotonicity:** each K⁺_t(m) is non-increasing in m and each K⁻_t(m) is non-decreasing. So max_t K⁺_t(m) ≥ 1/α holds exactly on an interval [0, m⁺], and max_t K⁻_t(m) ≥ 1/α exactly on [m⁻, 1].
  - **One-sided lower bound L at level α:** the largest multiple of 0.001 at which max_t K⁺_t(m) ≥ 1/α, or 0 if there is none.
    - By monotonicity this equals m⁺ rounded down.
    - Compute it by bisection over k ∈ {0, …, 1000}, testing m = k/1000 exactly with log-capitals.
  - **One-sided upper bound U:** the smallest multiple of 0.001 at which max_t K⁻_t(m) ≥ 1/α, or 1 if there is none.
    - K⁺ never rejects m = 1, and K⁻ never rejects m = 0, because every factor there is at most 1.
  - For R2, L and U are computed on x and reported as 2L − 1 and 2U − 1.
  - **Two-sided interval at level α:** [L, U], each computed at α/2.
  - **Coverage:** at the true mean μ, K⁺ and K⁻ are nonnegative supermartingales, so P(max_t K ≥ 1/α) ≤ α by Ville's inequality.
    - If μ is not rejected, then μ > m⁺ ≥ L (and symmetrically for U).
    - Outward rounding keeps this, so coverage holds for every real μ. The 0.001-grid evaluation is exact because rejection is monotone in m.
  - The bounds need no resampling and stay valid when a case's answers fail together or errors are sparse.
  - **Decisions are read from these bounds,** so every sentence's interval matches its decision.
  - **Crossed or offset bounds:**
    - If L > U, the interval is reported as empty and flagged. R2a then reads INCONCLUSIVE, and R2b reads NO ORDER DETECTED.
    - If the point estimate lies outside a nonempty interval, both are reported and the reading is flagged.
- **Clopper–Pearson exact bounds** for one answer per case: R0-F, and R5's settled-answer accuracy.
- **Exact one-sided McNemar tests** for R5's paired comparisons.
- **Descriptive intervals** (R1 shares, R1m, R3, R3b, R6 and every reported-only number) are case-bootstrap percentile intervals, B = 10,000 (`acd-bootstrap`, `sub` per §4). They are labelled approximate and never gate or license a comparison word. A zero-denominator replicate is redrawn and the count of redraws is reported.
- **Levels:**
  - R0 and R0-F bounds are one-sided at 95%, per lead.
  - The five publish routes (R2a at 2 and 3 LT, R2b, R5 at 2 and 3 LT) each use level 0.01, so their intervals are 99% and their tests use p ≤ 0.01.
- **Statistical audit (Stage 0, synthetic data only, before Step 0).** Write `ACD_STATS_AUDIT.md`.
  - Any failure is resolved by rule R-stat (§14), not by a halt.
  - **Definitions:** the Monte Carlo SE is sqrt(nominal·(1 − nominal)/N). "Half empty" means P(0) = 0.5, with the rest uniform on 1–8. In "eight-only", a failing eight-answer case fails all eight answers. The R2 null shapes are those of the v2.2 audit.
  - Claude's pre-check of this construction (2026-10-05, synthetic, 4,000 panels): false-PASS at case-averaged 0.90 was at most 0.043. Power at 80 nonempty cases and 0.97 was 0.90 with independent answers and 0.64 with whole-case errors. 35 perfect cases give L = 0.900, 30 give 0.883. Two hundred perfect cases give the 99% interval [0.970, 1].
  0. **Monotonicity check:** on 1,000 random synthetic sequences, max_t K⁺_t(m) is non-increasing and max_t K⁻_t(m) non-decreasing on a 10⁻⁴ grid. The executor's witnesses (m = 0.9629 and 0.0371) are recomputed and reported.
  1. Clopper–Pearson and McNemar match `scipy.stats` exact values.
  2. Null validity, with at least 20,000 simulated panels of 200 cases per configuration:
     - the R0 test at case-averaged accuracy exactly 0.90, for each case-size distribution × error mechanism. Sizes: the executor's {0: 0.85, 1: 0.10, 8: 0.05}, uniform on 0–8, and half empty. Mechanisms: independent answers, whole-case errors, and errors only in eight-answer cases;
     - the R2 intervals at mean 0, for symmetric, skewed and sparse case-level differences.
     - Each false-PASS or non-coverage rate must be at most its nominal level plus 2 Monte Carlo standard errors.
  3. The executor's 0.888 counterexample, reported.
  4. A power table, reported: R0 at case-averaged accuracy 0.95, 0.97 and 0.985 with 50, 80, 120 and 160 nonempty cases; R2a at Δ = 0.15 and 0.25.

| Reading | What | Rule |
|---|---|---|
| **R0** (gate, per lead) | Case-averaged accuracy of observation-confident S answers: r_T = mean, over cases with at least one such answer, of a_c = (correct)/(observation-confident S) in case c. The answer-level ratio (all correct)/(all answers) is also computed. | Statuses are assigned in this order: **NOT EVALUABLE** (fewer than 100 such answers or fewer than 30 cases); **INSUFFICIENT**, flagged, if L ≥ 0.90 and U < 0.90; **PASS** (betting one-sided 95% lower bound L on r_T ≥ 0.90, and answer-level point ≥ 0.90); **FAIL** (betting one-sided 95% upper bound U on r_T < 0.90); **INSUFFICIENT** otherwise. Also reported: the answer-level ratio, as a point estimate with a descriptive bootstrap interval. Also reported: all confident S; P, B and Fc; reliability diagram (p bins [0.5, 0.6), …, [0.9, 0.95), [0.95, 1]); PIT or rank histogram of realized D_k among draws; coverage; fit flags; split stability. |
| **R0-F** (per lead) | Accuracy of confident Fc answers (one per case) | Same order as R0: **NOT EVALUABLE** (fewer than 30 confident Fc); **PASS** (Clopper–Pearson one-sided 95% lower bound ≥ 0.90); **FAIL** (one-sided 95% upper bound < 0.90); **INSUFFICIENT** otherwise. |
| **R1** | Confidence map | For every type and lead: confident, observation-confident and climate-confident shares, with 95% intervals; S per action. |
| **R1m** | Mechanism | §9. |
| **R2a** (route at 2 and 3 LT) | Same-lead comparison: Δ_T = mean over c of (s_c − f_c), with s_c = (1/8)·#{S_k observation-confident} and f_c = 1[Fc confident] | Needs R0 and R0-F PASS at T; otherwise the reading is **PREREQUISITE NOT MET**, reported as numbers only. **DIFFERS:** Δ_T ≥ 0.15 with 99% lower bound > 0, or Δ_T ≤ −0.15 with 99% upper bound < 0. **EQUIVALENT:** the 99% interval lies within [−0.10, 0.10]. **INCONCLUSIVE:** otherwise. |
| **R2b** (route) | Ordered loss times | Eligible (c, k): S_k observation-confident and Fc confident at lead 0. L_S and L_F are the first leads at which S_k and Fc are no longer confident. A question still confident at 6 LT has its loss **not observed within the tested range**: it counts as later than any observed loss, and two such questions tie. Δ_loss = mean over eligible cases of (mean over that case's eligible k of [1(L_S > L_F) − 1(L_S < L_F)]). Cases with no eligible action are excluded; fewer than 30 eligible cases is NOT EVALUABLE. Needs R0 and R0-F to be PASS or NOT EVALUABLE at every lead; otherwise the reading is **PREREQUISITE NOT MET**, reported as numbers only. **OUTLIVES:** Δ_loss ≥ 0.20 and 99% lower bound > 0. **PRECEDES:** Δ_loss ≤ −0.20 and 99% upper bound < 0. **NO DIRECTIONAL PREFERENCE:** the 99% interval lies within [−0.10, 0.10]. Otherwise **NO ORDER DETECTED**. Report the eligible counts; the shares of earlier, later, same-lead and both-beyond-range pairs; and the variant using observation-confidence for L_S. |
| **R2c** | Forecast-horizon rule | At every lead: the share of S answered by the rule that are not confident, and their realized accuracy; the share refused that are confident, and their realized accuracy. |
| **R3** / **R3b** | Crude sampler / RML smoother | Confidence shares; the R0 statistic (case-averaged accuracy of observation-confident S answers, with confidence from that sampler's members and climate-confidence from the same null); reliability diagram; classification agreement (Cohen's κ) with the posterior. |
| **R5** | Targeted measurement | §8. |
| **R6** | CNN-20k ensemble | Its confidence shares; the R0 statistic, defined as for R3; among S answers not confident under the posterior, the share it is confident on (X) and its realized accuracy there (Y); κ with the posterior. |
| **R7** (optional) | Model error | Two-scale truth (`rhs2`, dt 0.001), observing X only with the same noise, under the same declared one-scale model class. Report the fit flag rate against 467.6 and the R0 statistic. |

## 11. What each outcome licenses (frozen)

**Scope rules.**
- "Confident" is defined once, in Setup: posterior probability of the modal answer ≥ 0.95 under the declared model class and prior.
- Never write "fixed", "determined by the observations", "every consistent instance", "settled", "certified", "guaranteed" or "proven".
- Climate-confident answers are "given by climatology at the true forcing", never "fixed by structure".
- Fc is always "the sign of the unforced window-energy anomaly".
- Claims are scoped to the declared model class, noise and actions.
- World models enter only as what a world model would need to report. CNN-20k is "a deterministic CNN emulator".

| # | Condition | Licensed sentence |
|---|---|---|
| L1 | R0 and R0-F PASS at T | "With 11 noisy snapshots spanning 0.84 Lyapunov times, the posterior under the known law answers the sign of a small intervention's effect on window energy with at least 95% probability for X% of case–action questions at T (X_o% beyond what climatology alone gives), against Z% for the sign of the unforced window-energy anomaly." |
| L2 | R0 PASS at T | "Averaged over cases, confident intervention-sign answers that climatology alone does not give are right W% of the time at T (one-sided 95% lower bound B); over all such answers, A%." |
| L3a | R2a at T | DIFFERS: "At T the observation-confident S share and the confident Fc share differ by Δ (99% interval [a, b])." EQUIVALENT: "At T the observation-confident S share and the confident Fc share are within 0.10 of each other (Δ, 99% interval [a, b])." INCONCLUSIVE: "At T the difference is Δ (99% interval [a, b]), which establishes neither a difference nor equivalence." |
| L3b | R2b | OUTLIVES: "Paired by case, confidence in an intervention's sign outlasts confidence in the forecast sign: it is lost later in P₊ and earlier in P₋ of a case's eligible actions, averaged over cases (99% interval for the difference [a, b])." P₊ (P₋) is the mean over eligible cases of the share of the case's eligible actions lost later (earlier), so P₊ − P₋ = Δ_loss. PRECEDES: the same with "is lost before". NO DIRECTIONAL PREFERENCE: "Paired by case, confidence in an intervention's sign shows no directional preference between earlier and later loss relative to the forecast sign (Δ_loss, 99% interval [a, b] within ±0.10)." Otherwise the numbers only, with no ordering word. |
| L4 | R0 PASS at T | "At T, the posterior correlation between factual and counterfactual window energies is ρ (median), so the difference carries c of their summed uncertainty." |
| L5 | R0 PASS at T | "Of the confident sign answers at T, K% are given by climatology at the true forcing; the rest depend on the observations." |
| L6 | R5 at T | Q-BEATS: "Four precise measurements targeted at the decision question turn C_Q of open decision questions at T into confident, correct answers, against C_best for the best of spread-targeted, forecast-targeted and random measurements, and C_A for all 40." Otherwise: "Question-, forecast-, spread-targeted and random measurements turned C_Q, C_F, C_V and C_R of open decision questions at T into confident, correct answers; question targeting did not reliably beat the best alternative." |
| L7 | R3, R3b | Crude: if its R0 statistic at 2 LT is below 0.85 with a betting one-sided 95% upper bound below 0.90, "An ensemble built from perturbed last frames gives confident answers that are right only r_c of the time." Otherwise the neutral form with both numbers. RML: "A randomized-maximum-likelihood ensemble smoother agreed with the posterior on A% of confidence classifications, and its confident answers were right r_m of the time." |
| L8 | R6, R0 PASS at T | "On sign questions where the posterior is not confident at T, a deterministic CNN emulator's ensemble is confident on X% and right on Y% of those." The word "overconfident" only if its R0 statistic is below 0.85 with a betting one-sided 95% upper bound below 0.90. |
| L9 | R2c | "Answering every question up to the lead at which the forecast sign is confident for half the cases, and none beyond, would answer U% of sign questions the posterior is not confident on (right V%) and refuse D% that it is confident on." |
| L10 | R7 run | "When the truth has fast variables the declared model lacks, the goodness-of-fit check flags G% of cases, and confident answers are right r₂ of the time." |

**Headline assembly.** The abstract and introduction are assembled only from L1–L10 plus Setup. The revelation's mechanism clause uses L4's numbers. Its last clause takes "do" or "do not" from L6.

**Publish, kill and decide.**
- **Publish:** confirmation R0 PASS at 2 LT, and at least one route: R2a DIFFERS at T (with R0 and R0-F PASS at T), R2b OUTLIVES or PRECEDES (with R0 and R0-F PASS or NOT EVALUABLE at every lead), or R5 Q-BEATS at T (with R0 PASS at T).
- **Kill:** confirmation R0 FAIL at both 2 and 3 LT, or confirmation coverage below 0.85. FAIL means the upper bound shows accuracy below 0.90, not merely a missed PASS.
- **Otherwise,** including R0 INSUFFICIENT: Todd decides.

**Abstract numbers.** They come from the confirmation panel. If it is not complete by Oct 8, Todd decides whether to use development numbers, labelled as such.

## 12. Two-sided feasibility, surprise, null (checks 1, 5a, 6, 7, 8)

All inputs are **hypotheses under test** (check 5a).

| Reading | Passing or first-branch input | Failing or other-branch input |
|---|---|---|
| Implementation check | Variances within 4 MC standard errors, eigendirections within 6% → pass | Smallest-eigendirection variance off by 25% → R-impl (NumPyro, then doubled draws), continue |
| Coverage | 0.94, Wilson [0.90, 0.97] → valid | 0.80 → development: reported Stage 1 reading; confirmation: KILL |
| R0 | 120 cases, 115 perfect and 5 with one or two errors, lower bound 0.965, answer-level 0.98 → PASS | 100 cases at case-averaged 0.80, upper bound 0.862 → FAIL. 30 perfect cases, lower bound 0.883 → INSUFFICIENT. 70 answers → NOT EVALUABLE |
| R0, climate-heavy case | — | All confident S at 0.95 but observation-confident upper bound 0.88 → FAIL (v1 would have passed) |
| R0, executor's counterexample | — | No observed errors among about 30 nonempty cases (10 of eight answers, 20 of one) → lower bound 0.883 → not PASS (v2.1 forced PASS) |
| R0-F | 30 confident, all correct → Clopper–Pearson lower bound 0.905 → PASS | 25 of 30 correct → upper bound 0.93 → INSUFFICIENT; 20 of 40 → FAIL |
| R2a | Δ = 0.26 [0.15, 0.37] → DIFFERS | Δ = 0.04 [−0.06, 0.09] → EQUIVALENT. Δ = 0.17 [−0.02, 0.35] → INCONCLUSIVE |
| R2b | Δ_loss = 0.31 [0.12, 0.48] → OUTLIVES. Δ_loss = −0.27 [−0.44, −0.09] → PRECEDES. Δ_loss = 0.01 [−0.07, 0.08] → NO DIRECTIONAL PREFERENCE | Δ_loss = 0.12 [−0.05, 0.30] → NO ORDER DETECTED. 24 eligible cases → NOT EVALUABLE |
| Stage 1a sampler comparison | 14% threshold-crossing disagreement, 0.4% substantive (\|z\| > 3) → continue | 9% substantive, and the posterior rerun disagrees with itself on 3% → flag those cases, keep the 4× posterior, continue |
| R5 | C_Q = 0.34, C_V = 0.19, C_F = 0.15; discordant cases 18 against 3 versus V (p = 0.0007) and 21 against 2 versus F (p < 0.0001); C_R = 0.12 with 24 against 2 versus R; 34 of 36 settled correct (Clopper–Pearson lower bound 0.835); coverage 0.93 → Q-BEATS | C_Q = 0.34 against random 0.12 but spread 0.30 → not (v1 would have passed). 34 settled but only 0.71 correct → not |
| L7 crude | 0.78, upper bound 0.82 → strong form | 0.91 → neutral form |
| L8 "overconfident" | 0.70, upper bound 0.78 → used | 0.88 → not used |
| Stage 1 strong | R2b Δ_loss = 0.33, interval excluding 0 | Δ_loss = 0.18 → Todd decides |
| Adjoint check | Maximum error 9e-7 → pass | 2e-6 → R-grad |
| dt check | 0.4% answer and 0.8% classification changes → pass | 0.6% answer changes → R-dt |
| Posterior diagnostics | R-hat 1.005, ESS 600, 0.5% divergent → pass | R-hat 1.02 → rerun, then R-diag |
| RML validity | Δχ² = 74 → valid | Δχ² = 75 → invalid member |
| R5 population | 40 qualifying cases → evaluable | 39 → NOT EVALUABLE |
| R2a prerequisite | R0 and R0-F PASS at T → read | 25 confident Fc at 3 LT → R0-F NOT EVALUABLE → PREREQUISITE NOT MET |

**Checks 2, 3, 6, 7 and 8.**
- **Independence (check 2):**
  - truth is never seen by any sampler;
  - the null sees no observations;
  - targeting uses draws only;
  - confirmation realized outcomes come after the hashes.
- **Referents (check 3):**
  - "confident" classifies a (case, lead, question) triple by the posterior draws of that case;
  - the realized answer comes from `actual`.
- **Surprises (check 6):**
  - the intervention sign outlives the forecast sign by more than 0.3 in R2b;
  - c_k stays below 0.2 at 3 LT;
  - RML and the posterior disagree on more than 10% of classifications;
  - forecast-targeted measurement resolves decision questions as well as question-targeted measurement does.
- **Nulls (check 7):** the climatological null and random sites.
- **Separability (check 8):** R5 thresholds against the best of the spread, forecast and random arms. R3, R3b and R6 are reported with intervals, and no ranking beyond L7 and L8 is licensed.

## 13. Stages, gates, compute

| Stage | Dates | Work | Gate |
|---|---|---|---|
| 0 | Oct 5 | Step 0b (complete at `eb87279`), then the statistical audit (§10), then the spec gate (findings resolved by §14 rules); Step 0; `acd_protocol.py`; joint adjoint FD check; sampler implementation check; dt check; climatological null. **Benchmarks**, each including compilation, forecasting and diagnostics: an ordinary case (posterior, RML, crude, forecasts), a 4-site refit, and an all-site refit, all on dtcheck or development cases. **Projection** for every posterior run in Stages 1–3, about 1,900 four-chain runs at the maximum populations (400 ordinary, 500 development refits, 1,000 confirmation refits), plus an allowance for reruns. Write `ACD_NUMERICAL_REPORT.md`. | Hard stops and resolution rules in §14 |
| 1a | Oct 5 | **Validation, development cases 0–19:** posterior with diagnostics, multi-start MAP, RML, crude; coverage; posterior–RML agreement at 2 and 3 LT. | **Flag** (no halt) if diagnostics fail in more than 1 of 20 cases, or coverage is below 15/20. **Sampler disagreement:** if more than 5% of S questions at 2 LT disagree substantively between posterior and RML (\|z\| > 3, §7.3), rerun every case with at least one substantive S disagreement at 2 LT, with 4 chains of 4D draws thinned per chain at ⌊i·4D/512⌋, i = 0…511, giving S = 2048, and use the rerun. If the two posterior runs still disagree substantively on more than 1% of those questions, those cases are flagged and the posterior with 4 times the draws is kept. Continue to Stage 1b either way, and report everything in `ACD_STAGE1A_VALIDATION.md`. |
| 1b | Oct 5–6 | **Development kill test, cases 0–199:** R0, R0-F, R1, R1m, R2a, R2b, R2c, R3, R3b, and R5 at 2 LT. Script-generated `ACD_STAGE1_READING.md` and the vault note `R_Aspen-Counterfactual-Determinacy-Stage1-2026-10`. Claude writes the gate summary. | **Strong:** R0 PASS at 2 LT, and one of the following. Each must also meet its route's prerequisites from §11: calibration at its own lead, R0-F for R2a, R0 and R0-F PASS or NOT EVALUABLE at every lead for R2b, and R5's count, accuracy and coverage conditions. The options: Δ_T ≥ 0.25 with 99% lower bound > 0, or Δ_T ≤ −0.25 with upper bound < 0 (R2a); Δ_loss ≥ 0.30 with lower bound > 0, or Δ_loss ≤ −0.30 with upper bound < 0 (R2b); crossed bounds are never strong; C_Q − max(C_V, C_F, C_R) ≥ 0.15 with all three McNemar p ≤ 0.01 (R5). These are above the publish margins (0.25, 0.30 and 0.15 against 0.15, 0.20 and 0.10). **Stop and report:** R0 FAIL at both 2 and 3 LT. **Otherwise:** Todd decides. |
| 2 | Oct 6–7 | On Todd's go: write `ACD_FREEZE.md` (hashes, namespaces, sub roles, null outputs, thresholds, the Stage 1 reading hash), then the confirmation panel in blind order. Run every reading, with R5 at 2 and 3 LT, and R6. Write `ACD_STAGE2_READING.md`. | Publish, kill or decide (§11) |
| 3 | Oct 7 | R7 if time allows; F1 assembly. | Reported |
| 4 | Oct 8–9 | NUMBERS `ACD_*` and `check_acd.py`; independent factual audit; figures. Claude drafts the abstract from L1–L10. Todd submits. | Release checklist |

**Compute.**
- sulaco CPU for the posterior, fits and integration; sulaco GPU for CNN inference only.
- No training. Do not stop the Qwen vLLM services, and use no cloud.
- Leave the AFD close-out on Baccus untouched.
- If the Stage 0 projection exceeds 12 wall-hours for Stages 1–3, apply the cut order. If it still exceeds 12 wall-hours, reduce the R5 population from 100 to 60 cases, and then the posterior draws from 4×1000 to 4×500. Report the projection and continue (R-time).

**Figures** are greyscale-safe, with every distinction carried by a second cue.
- **F1, illustrative case chosen by rule:** the first confirmation case in which, at 2 LT, some S_k is observation-confident, P(a1, a2) is not confident, and arm Q resolved it correctly. It shows two posterior draws with opposite answers to P(a1, a2), their diverging trajectories, and the probe. It is labelled illustrative.
- **F2:** confident share against lead per question type, with observation-confident solid and all-confident dashed.
- **F3:** the mechanism: ρ_k, c_k and the divergence ratio against lead.
- **F4:** reliability diagrams for the posterior, RML, crude and CNN.
- **F5:** R5 settled-correct shares by arm, hatched.

## 14. Hard stops, resolution rules and cut order

**Hard stops.** Only these halt the run before the planned Stage 1 gate:
- **H1.** Sampler, targeting or null code that opens a truth-bearing array (`true`, `actual`, `actual_cost`, `truth_*`, any `cpu_*.npz`) or receives a value computed from one.
  - Samplers and targeting read data only through `acd_protocol.load_observed(panel, c)`, which returns `observed` alone and appends to `runs/acd_access.jsonl`.
  - Truth is read only by scoring and coverage code (`acd_questions.py`, `acd_analysis.py`), by Step 0 item 7, by the R-dt recomputation, and by `acd_measure.py` to form z, which is the designed measurement.
  - Inherited files that store `true` and `observed` together are not H1.
- **H2.** Any confirmation-panel reading before `ACD_FREEZE.md` is committed. Confirmation is outside this go in any case.
- **H3.** An action outside the authorization: stopping the Qwen services, cloud compute, training, or touching the Baccus close-out.

**Resolution rules.** Each rule is applied, recorded in the relevant report and summarized at the Stage 1 gate. The run continues.

| Rule | Trigger | Resolution |
|---|---|---|
| R-def | Step 0 difference from the code on an inherited definition | Code's rule governs; record |
| R-grad | Adjoint error ≥ 1e-6 | JAX automatic differentiation for MAP and RML |
| R-impl | Sampler implementation check fails | NumPyro NUTS; then doubled warmup and draws; record |
| R-dt | dt check fails | Halve dt everywhere, recheck once, continue with the finer dt |
| R-diag | Posterior diagnostics fail after a rerun | Exclude the case and report the rate. Above 5%, flag it |
| R-cov | Development coverage below 0.85 | Report as a Stage 1 reading |
| R-rml | RML members short or sampler disagreement | §7.3 and §13 Stage 1a rules; RML stays a cross-check |
| R-stat | A statistical-audit item fails | First correct the implementation and rerun the audit. If an item still fails: for item 1, use `scipy.stats` directly. For any betting item, replace every decision lower bound by min(betting, B_lo) and every upper bound by max(betting, B_hi). For R0, L7 and L8, B_lo is the one-sided 95% Clopper–Pearson lower bound on the share of nonempty cases whose observation-confident answers are all correct, and B_hi is the Clopper–Pearson upper bound on the share with at least one correct. For R2a and R2b, B = d̄ ∓ sqrt(2·ln(2/α)/n), the Hoeffding bound at the same 99% level. Record and continue |
| R-time | Projection over budget after cuts | §13 compute reductions |
| R-gpu | GPU memory short for CNN | Smaller micro-batches, else cut R6 |
| R-other | Any other spec finding | For a reading, take the reading that licenses less. For anything else, take the option that exposes no truth or confirmation data and changes no threshold. Record and flag it |

**Cut order** (first cut first):
1. R7.
2. R5 arm A (the all-site ceiling).
3. R6 at 3 LT.
4. R3b on the confirmation panel.
5. P and B at leads other than 2 and 3 LT.
6. R5 at 3 LT.

**Never cut:** Steps 0 and 0b, the implementation, adjoint and dt checks, the null, coverage, diagnostics, R0, R0-F, R1, R1m, R2a, R2b, R3, R5 at 2 LT, the blind order.

## 15. Deliverables

- **Code** in `aspen/determinacy/`:
  - `acd_protocol.py`;
  - `acd_posterior.py` (model, NUTS, diagnostics, implementation check);
  - `acd_fits.py` (MAP, RML, joint adjoint);
  - `acd_questions.py`;
  - `acd_campaign.py`;
  - `acd_measure.py`;
  - `acd_mechanism.py`;
  - `acd_cnn_ensemble.py`;
  - `acd_analysis.py` and `acd_stats.py` (the §10 statistics);
  - `acd_figures.py`;
  - `check_acd.py`.
- **Reports:**
  - `ACD_SPEC_GATE.md`, `ACD_STEP0.md`, `CODEX_SELECTOR.md`;
  - `ACD_NUMERICAL_REPORT.md`, `ACD_STAGE1A_VALIDATION.md`, `ACD_STAGE1_READING.md`;
  - `ACD_FREEZE.md`, `ACD_STAGE2_READING.md`;
  - NUMBERS `ACD_*`, `CLAIM_LEDGER.md`.
- **Vault:**
  - If the vault is not reachable from sulaco, write the notes under `aspen/determinacy/vault/` for transfer;
  - results notes generated by script into `04-Results/`;
  - the claim ledger `L_Aspen-Counterfactual-Determinacy-Claim-Ledger-2026-10`;
  - a session-review entry for each spec error found in this WO.
- **Push** each day. No AI attribution.

## 16. Prior work to cite and design around

Checked at source in the factual audit. † marks a detail still to verify.
- **Aalaila et al. 2026**, *Scientific Reports* (nature.com/articles/s41598-026-52349-2): counterfactual reliability in chaotic systems under noise and parameter uncertainty. Lists the open questions addressed here.
- **Majda, Abramov and Gershgorin 2010**, "High skill in low-frequency climate response through fluctuation dissipation theorems despite structural instability", *PNAS* 107(2): 581–586. Ensemble-level response skill.
- **Lorenz 1975**, "Climatic predictability", GARP Publ. Ser. 16† (predictability of the first and second kind). **Lorenz 1996**, ECMWF Seminar on Predictability† (the model).
- **Lorenz and Emanuel 1998**, "Optimal sites for supplementary weather observations: simulation with a small model", *J. Atmos. Sci.* 55(3): 399–414. Lorenz-96 targeting for forecast error. Multiple replication with perturbed observations performed best; the spread arm follows their rationale that errors are largest where ensemble estimates differ most.
- **Xie, Zhang, Zhang, Poterjoy and Weng 2013**, "Observing strategy and observation targeting for tropical cyclones using ensemble-based sensitivity analysis and data assimilation", *Mon. Wea. Rev.* 141: 1437–1453, doi 10.1175/MWR-D-12-00188.1. Ensemble-sensitivity targeting for forecast metrics, with limited effectiveness under nonlinearity. The basis of arms Q and F.
- **Saito and Kotsuki 2026**, "Sparse sensor placement for reducing forecast errors in ensemble Kalman filtering", arXiv 2606.27267. Greedy A-optimal placement for forecast error on Lorenz-96.
- **Hashimoto, Hashimoto and Kuroki 2026**, "Forecast-ensemble-based active binary-threshold query design for interval data assimilation", arXiv 2609.05307. Adaptive query targets and thresholds on Lorenz-96, for assimilation accuracy.
- **Sun, Miyoshi and Richard 2023**, "Control simulation experiments of extreme events with the Lorenz-96 model", *Nonlin. Processes Geophys.* 30: 117–128. **Mitsui, Kotsuki, Fujiwara, Okazaki and Tokuda 2025**, "Bottom–up approach for mitigating extreme events with limited intervention options: a case study with Lorenz 96 model", *Nonlin. Processes Geophys.* 32: 457†(pages). Both use LETKF-conditioned interventions and do not assess instance-level predictability of an intervention's effect.
- **Kreutz, Raue and Timmer 2011**, arXiv 1107.0013: prediction profile likelihood.
- **Cieślak and Czyżewski 2026**, arXiv 2606.20655: identifiability of targets from available inputs.
- **Zhong, Shen, Catanach and Huan**, "Goal-oriented Bayesian optimal experimental design for nonlinear models using Markov chain Monte Carlo", SIAM/ASA JUQ, doi 10.1137/24M1649344 (arXiv 2403.18072). **Go, Qian and Yoon 2026**, "Goal-driven Bayesian optimal experimental design for robust decision-making under model uncertainty", arXiv 2605.26093. Goal-oriented design in non-chaotic settings.
- **Ba, de Wiljes, Oliver and Reich 2021**, "Randomized maximum likelihood based posterior sampling", arXiv 2101.03612 (*Computational Geosciences*†). Unweighted RML is inexact for nonlinear forward models. **Kitanidis 1995**†; **Oliver, He and Reynolds 1996**†: RML.
- **Hoffman and Gelman 2014**, NUTS, *JMLR* 15: 1593–1623. **Vehtari, Gelman, Simpson, Carpenter and Bürkner 2021**, rank-normalized R-hat, *Bayesian Analysis* 16(2): 667–718†.
- **Waudby-Smith and Ramdas 2024**, "Estimating means of bounded random variables by betting", *J. R. Stat. Soc. B* 86(1)† (arXiv 2010.09686): betting confidence bounds. **Clopper and Pearson 1934**, *Biometrika* 26: 404–413. **McNemar 1947**, *Psychometrika* 12: 153–157.
- **Tan et al. 2026**, arXiv 2607.27017 v4: context.

## 17. Design review of v1: disposition (GPT, 2026-10-04) and correction discipline

§17–§19 are the disposition record. Where they describe a halt or a prerequisite that differs from §10, §11 or §14, those sections and §20 govern.

| # | Comment | Class | Disposition | Reason |
|---|---|---|---|---|
| 1 | The headline promised set-based agreement, while the rule computes high probability. They differ even with perfect sampling (z = 2: 97.7% probability, yet an opposite instance at Δχ² ≈ 4 inside 56.94). | A | Fix | The probabilistic construct is chosen. All set language is removed (§11 scope rules). The profile check (v1 R4b) answered a different confidence question and is dropped. Witness exhibits survive only as the illustration in F1. |
| 2 | Unweighted RML is not the posterior for a nonlinear model. Coverage and χ² radii do not validate answer probabilities; an independent calculation is needed before the full development run. | A, B | Fix | NUTS is now the primary sampler, with R-hat, ESS and divergence diagnostics and an implementation check on a known Gaussian. RML is an independent cross-check on every case. Stage 1a validates on 20 cases first, and posterior–RML disagreement above 10% halts. MAP is multi-start, with boundary contacts and non-convergence reported. |
| 3a | R0 gated all S, so climate-easy answers could carry it. | A | Fix | R0 gates observation-confident S only. |
| 3b | R5 gated confidence, not correctness. | A | Fix | The measure is confident and correct, with an accuracy floor, a settled-count floor and post-probe coverage. |
| 3c | A 3 LT route could publish with calibration passing only at 2 LT. | A | Fix | Each route needs R0 PASS at its own lead. R2a also needs R0-F, so both compared answer sets must be accurate. R2b spans leads, so it needs R0 and R0-F not to FAIL at any lead. |
| 4a | The "horizon makes everything answerable" framing is a strawman. | C (would mislead) | Fix | The revelation is rewritten against observable-dependent predictability, ensemble-level response and forecast-targeted observation. |
| 4b | Targeted beating random is not novel (Hashimoto et al. 2026). | C, D | Fix | Spread-targeted (Lorenz and Emanuel) and forecast-sensitivity-targeted (Xie et al.) arms are added. The route must beat the better of them. Hashimoto et al. and Saito and Kotsuki are cited. |
| 4c | "EnKF samples the same consistent set" is false. | A | Fix | Removed. Mitsui et al. and Sun et al. are cited correctly. **A LETKF arm is declined as class D.** In this fixed 11-frame window, a filter started from climatology is handicapped. The fair ensemble-smoother incumbent is RML, which is run as R3b. The headline concerns the posterior's own horizon, which a LETKF only approximates. |
| 4d | Measure the covariance mechanism Var(J_k − J_0) = Var(J_k) + Var(J_0) − 2Cov, and divergence. | D, accepted | Fix | R1m and L4. It can change the headline because it supplies the physical explanation. |
| 5 | "Outlives" is not shown by a difference at one lead. | A | Fix | R2a licenses only the same-lead difference. "Outlives" and "precedes" need the paired loss-time reading R2b. |
| 6 | COMPARABLE is not equivalence. | A | Fix | EQUIVALENT is an interval within ±0.10; otherwise INCONCLUSIVE. |
| 7 | Fc needs qualification. | C (would mislead) | Fix | It is always "the sign of the unforced window-energy anomaly". |
| 8 | The null knows F = 8, and 95% climatological frequency is not physical necessity. | A | Fix | Renamed "climate-confident", with the information difference stated. It makes the observation share conservative. |
| 9 | The member cut conflicted with the 112-member halt and the 64/64 split. | B | Fix | Rules are functions of S and M. The member cut is removed, since NUTS is cheap. |
| 10 | L8 promised witnesses for every open question; R4a gave them only for pairs at 2 and 3 LT. | A | Fix | L8 is removed. F1 is illustration only. |
| 11 | A GPT review does not satisfy check 9. | B | Fix | Step 0b: a blinded Codex selector, with overlap reported. |
| 12 | A point estimate ≥ 0.90 with lower bound 0.85 does not show accuracy ≥ 0.90. | A | Fix | PASS needs a lower bound ≥ 0.90. |
| 13 | Four citations needed identification. | A | Fix | Completed in §16, with Xie et al. 2013 confirmed and used. |

**Differential prediction (v1 → v2).** These cases license less under v2:
1. A 97.7%-probability sign with an opposite instance at Δχ² 4. v1 wrote "the observations fix"; v2 writes "answered with at least 95% probability".
2. All confident S at 0.95 accuracy while observation-confident S are at 0.86. v1 R0 passed; v2 fails.
3. R0 at 0.92 with lower bound 0.86. v1 passed; v2 fails.
4. Targeted measurement makes twice as many answers confident as random, but they are 60% correct. v1 BEATS; v2 does not.
5. Targeted beats random but ties spread-targeted. v1 had a publish route; v2 does not.
6. A 3 LT difference with R0 failing at 3 LT. v1 had a route; v2 does not.
7. An interval of [−0.02, 0.18]. v1 said "decline together"; v2 says INCONCLUSIVE.
8. A single-lead difference of 0.2. v1 said "outlives"; v2 says "at T the shares differ", and "outlives" needs R2b.
9. RML probabilities biased by nonlinearity. v1 used them; v2 uses NUTS, and a disagreement of more than 10% halts.

**Changes that could make a reading easier, disclosed.**
- The R5 population rose from 60 to 100 cases, which raises power.
- R2b is a new publish route. Its margin (0.20) and the family-wide 99% level (stricter than v1's 98.75%) are fixed before data.
- No other threshold is looser than in v1.

## 18. Execution review of v2: disposition (GPT, 2026-10-04) and correction discipline

The reviewer supports the staged run through the Stage 1 gate, with confirmation held, once these corrections are written in. It agreed to leaving LETKF out.

| # | Comment | Class | Disposition | Reason |
|---|---|---|---|---|
| 1a | The spec gate required check 9 before Step 0b had produced the artifact check 9 needs. | B | Fix | Step 0b runs first, and the gate is signed off after it (§2, §3, §13). |
| 1b | The 15/20 Stage 1a floor conflicted with the 0.85 halt. | B | Fix | 15/20 applies to Stage 1a; 0.85 applies to the completed 200-case panel (§5, §13, §14). |
| 2a | A 10% classification-disagreement halt rejects correct samplers. At p = 0.95, samples of 128 and 512 draws disagree on the threshold about half the time. Compare modal probabilities and opposite answers can hide. | A | Fix | The comparison uses the same signed event with Monte Carlo error; \|z\| > 3 counts as substantive. A posterior rerun with 4 times the draws decides; threshold-crossing disagreement is a diagnostic only (§7.3, §13). |
| 2b | Monitor precision of the gate functionals, not only the parameters. | B | Fix | R-hat and ESS for D_k and J_8 at 2 and 3 LT, with a full-draw fallback; se(p) and a threshold-uncertain count (§5). |
| 3 | Benchmark the measurement refits (about 1,900 four-chain runs at the maximum populations). Halt if the projection exceeds budget after cuts. | B | Fix | Three benchmarks including compilation, forecasting and diagnostics; an explicit halt; arm A added to the cut order (§13, §14). |
| 4a | R2b had no rule for cases with no eligible action, and no floor. | A | Fix | Such cases are excluded; at least 30 eligible cases are required. |
| 4b | Δ_loss = 0 does not mean confidence is lost at the same lead. | A | Fix | The reading and sentence become NO DIRECTIONAL PREFERENCE. |
| 4c | Loss beyond 6 LT is unobserved. | A | Fix | It is "not observed within the tested range", with stated ordering rules. |
| 4d | R0-F's FAIL and NOT EVALUABLE statuses were undefined. | B | Fix | Defined in §10. |
| 5 | "Strong" must satisfy the chosen route's prerequisites. | A | Fix | §13 Stage 1b. |
| 6a | R5 needs a common population across arms. | A | Fix | Failed refits count as unresolved and stay in the denominator. |
| 6b | "Beats the better alternative" needs bounds against both V and F, or a recomputed best in each replicate. | A | Fix | Both lower bounds must be > 0 (an intersection–union test). |

**Differential prediction (v2 → v2.1).** These cases license less under v2.1:
1. Q beats V with a bound above 0, but its bound against F is at or below 0 while V had the higher point estimate. v2 compared Q with V only and read BEATS; v2.1 does not.
2. Failed Q refits dropped from Q's denominator would inflate C_Q under v2. v2.1 counts them as unresolved.
3. Half of the actions lose confidence earlier and half later, so Δ_loss = 0. v2 wrote "lost at the same lead"; v2.1 writes "no directional preference".
4. R2b on 24 eligible cases. v2 had no floor; v2.1 is NOT EVALUABLE.
5. A Stage 1 "strong" via R2a at 3 LT with R0 failing at 3 LT. v2 was ambiguous; v2.1 is not strong.

**Changes that make continuing easier, disclosed.**
- The sampler halt now needs substantive disagreement that the posterior's own rerun does not resolve. v2's rule would have halted on Monte Carlo noise alone. No reading threshold changes.
- Stage 1a with 16/20 coverage no longer meets two conflicting instructions.

## 19. Amendment 1 (v2.2): gate bounds, after the executor's spec-gate halt (2026-10-05)

**The halt.** The executor stopped before Step 0 on check 4 and was correct to.
- v2.1's percentile case bootstrap degenerates when no errors are observed: every resample has accuracy 1.
- On a synthetic population with answer-level accuracy 0.888, built from one-answer and eight-answer cases where eight-answer cases occasionally fail together, R0 PASS is forced with probability 0.0611. The nominal rate is 0.05.
- At 30 perfect Fc answers, the bootstrap bound is 1. ([[T_Spec-Integrity-Gate]] check 4; `ACD_SPEC_GATE.md` at `91e77a6`.)

| # | Defect | Class | Disposition | Reason |
|---|---|---|---|---|
| 1 | Percentile bootstrap used as a confidence bound for R0 and R0-F | A, B | Fix | R0 uses a betting bound valid at finite sample size (Waudby-Smith and Ramdas 2024). R0-F uses exact Clopper–Pearson bounds. |
| 2 | Within-case dependence and sparse errors | A | Fix | The bounds treat the case as the unit, with no assumption about how a case's answers fail together. |
| 3 | Empty replicates | B | Fix | No gate resamples. Descriptive bootstraps redraw zero-denominator replicates and report the count. |
| 4 | L7 and L8 upper bounds share the boundary defect | A | Fix | Betting upper bounds on case-averaged accuracy. |
| 5 | Which intervals are calibrated route tests | B | Fix | The R2a and R2b intervals are betting intervals; R5 uses exact McNemar and Clopper–Pearson. All other intervals are labelled approximate and descriptive. |
| 6 | A synthetic audit before data | B | Added | §10 statistical audit, with its own halt. |

**Explicit changes the executor asked to be named.**
- **R0's estimand is now case-averaged accuracy.** The answer-level ratio is reported alongside, and its point estimate must also be at least 0.90 for PASS.
  - **Reason:** when up to eight answers in a case can fail together, a bound valid at finite sample size for the answer-level ratio has little power below about 450 answers. Claude's simulation of the betting test gave 2% power at 270 answers and 0.985 accuracy, and 61–97% at 450 answers.
  - The case-averaged estimand treats the case as the unit, as the WO does everywhere else. It needs about 44 perfect cases to pass, with power 0.81 at 80 cases and 0.97 accuracy, and 0.97 at 120 cases.
  - L2 names the estimand and gives the answer-level number too.
- **R0 and R0-F have three outcomes.** FAIL now means the upper bound shows accuracy below 0.90. INSUFFICIENT means an evaluable panel that shows neither.
  - The kill uses FAIL only, so a panel too thin to show accuracy is not read as evidence against it.
  - Publish routes still need PASS. R2b's prerequisite stays as strict as in v2.1: PASS or NOT EVALUABLE at every lead.

**Differential prediction (v2.1 → v2.2).**

These license less:
1. The executor's construction, with no observed errors in about 30 nonempty cases. v2.1 forced PASS; v2.2 gives a lower bound of 0.86, so not PASS.
2. Case-averaged accuracy of 0.90 with errors in whole cases. v2.1's false-PASS rate was uncontrolled; v2.2 holds it at or below 0.05 by Ville's inequality. Claude's simulation gave at most 0.024 at 80 and 160 cases.
3. R5 with 5 discordant cases, all favouring Q. v2.1's bootstrap bound exceeded 0; the exact McNemar p = 0.031 > 0.01, so it is not significant.
4. An answer-level point estimate of 0.89 with a case-averaged lower bound of 0.91. v2.2 does not PASS.
5. Thirty perfect Fc answers. v2.1 bound 1.0; v2.2 bound 0.905. It still passes, now with a valid bound.

These could license more, disclosed:
1. A panel with answer-level accuracy of 0.91 whose errors sit in a few large cases. v2.1's answer-level bootstrap bound could fall below 0.90 (FAIL), while v2.2's case-averaged bound can reach 0.90 (PASS). This follows from the estimand change, and it is the main way v2.2 licenses more. The answer-level point floor of 0.90 limits it.
2. A panel that would have been FAIL under v2.1 for lack of evidence is now INSUFFICIENT. That avoids a kill, and Todd decides.

**No change** to the 0.90 threshold, the count floors, the confidence threshold, the R2 and R5 margins, or the route structure.

## 20. Amendment 2 (v2.3): continuous inversion, a pre-release review, and resolution rules in place of halts (2026-10-05)

**The second halt.** The executor stopped before Step 0 on check 4, again correctly. v2.2's bets depended on the null value m (aGRAPA aimed at m, capped at 0.75/m), so the capital was not monotone in m. The grid scan could then exclude a real mean that the capital never rejects: with 200 synthetic ones, m = 0.9629 fell outside the reported interval [0.963, 1] without being rejected. Waudby-Smith and Ramdas note that aGRAPA sublevel sets need not be intervals.

**Pre-release review.** Before v2.3 was released, Claude ran an independent agent review acting as the executor. It applied the spec gate, checked implementability against `protocol.py`, `physics.py`, `extras.py` and `campaign.py`, and verified §10 numerically.
- It confirmed the new construction:
  - the bets are predictable and do not depend on m;
  - every factor is at least 0.1;
  - across 1,000 random sequences on a 10⁻⁴ grid, there were 0 monotonicity violations;
  - every number quoted reproduced;
  - false-PASS at case-averaged accuracy 0.90 was at most 0.037 across 9 configurations of 20,000 panels;
  - R2 non-coverage at mean 0 was at most 0.0053.
- It found 25 further items. All are applied, and the main ones are below.
- A second focused pass on the revised text found one formula error from the first pass, now corrected: the Monte Carlo SE divided an event count by the ESS. It also found a few ambiguities the edits had introduced: draw counts tied to D, refit diagnostics, how the two R0 computations combine, module prefixes, the direction of the "strong" rule, and seed roles for reruns. All are applied.

| # | Defect | Class | Disposition |
|---|---|---|---|
| 1 | The grid inversion is not licensed by Ville's inequality when the capital is not monotone in m | A | Bets no longer depend on m; the capitals are monotone; the bound is the largest multiple of 0.001 that is rejected, found by bisection on k; coverage holds for every real mean (§10) |
| 2 | The answer-level betting bound had m-dependent inputs | A | Removed; the answer-level point must still be ≥ 0.90 for PASS |
| 3 | Decisions and reported intervals could disagree; bounds could cross; DIFFERS had no direction | A | One bound for both; crossed or offset bounds are flagged; DIFFERS needs the matching side |
| 4 | Read literally, H1 fired on the inherited data layout | A | H1 is now operational: truth-bearing arrays are listed, and samplers read through `load_observed` with an access log |
| 5 | ACD stream names could not reach `protocol.rng` | A | `protocol.IDS.update(ACD_IDS)` at import; the inherited files stay byte-unchanged |
| 6 | A draw's forecast forcing and state were not stated; `sub` roles were deferred to the freeze | A | F_s and x_s(0) = H_10(θ_s) are stated; all roles are fixed in Stage 0 (§4) |
| 7 | "Climate-confident" did not say whose answer is compared | A | The null must give the sampler's modal answer |
| 8 | JAX on a GPU could pre-allocate the memory the Qwen services use | B | JAX is CPU-only and installation is authorised |
| 9 | Fit order was circular; R5 refit, diagnostic fallbacks, statuses and prerequisites were underspecified | B | Each is specified (§5, §8, §10) |
| 10 | The R2 part of R-stat was not a remedy | A | Replaced by Hoeffding bounds; R-stat now covers every audited item |
| 11 | Excluding cases on diagnostics could raise R0 | A | PASS also requires R0 computed with the excluded cases included |
| 12 | R5 was not thresholded against the random arm (check 7) | A | Q must beat V, F and R |
| 13 | The §12 R5 example was internally inconsistent; the headline did not match L2; §20 misfiled two predictions | A | Corrected |

**Halts are replaced by resolution rules (Todd's instruction).** Only hard stops H1–H3 halt. Every other finding is resolved by a named rule in §14, recorded, and flagged at the Stage 1 gate. The gate exists so that a defective specification cannot produce an inflated claim, and that purpose is kept:
- Each resolution rule either switches to a more conservative or better-checked procedure (R-grad, R-impl, R-dt, R-stat), or reports instead of gating (R-cov, R-diag, R-rml).
- R-other takes the reading that licenses less.
- None makes a publish route easier to reach.
- The hard stops cover the failures that would contaminate evidence: truth leakage, reading the confirmation panel early, and unauthorized actions.

**Differential prediction (v2.2 → v2.3).**

These license less or the same:
1. 30 perfect cases. L = 0.883, so R0 stays INSUFFICIENT.
2. Five discordant cases, all favouring Q. McNemar p = 0.031, not significant.
3. An answer-level point below 0.90. Not PASS.
4. Q beats V and F but not random sites by 0.10 with p ≤ 0.01. v2.2 read BEATS; v2.3 does not.
5. A case dropped for failed diagnostics that would have lowered R0. v2.2 could PASS; v2.3 requires PASS with it included.
6. A Δ_T of +0.16 with an interval entirely below 0. v2.2 could read DIFFERS; v2.3 cannot.

These could license more, disclosed:
1. 200 perfect cases: the 99% interval narrows from [0.963, 1] to [0.970, 1].
2. R0 passes with fewer perfect cases: 35 now, against about 44 under v2.2. The new bets reach a larger stake (0.9 against 0.75/m ≈ 0.83 at m = 0.90). At 80 cases and accuracy 0.97, power is 0.90 against v2.2's audited 0.79. False-PASS stays at or below 0.05 by Ville's inequality; the review's simulation found at most 0.037.
3. Development coverage below 0.85, diagnostic exclusions above 5%, and Stage 1a flags no longer halt. They are reported at the Stage 1 gate, where Todd decides. No publish route depends on the development panel.

**No change** to estimands, the 0.90 and 0.95 thresholds, count floors, R2 margins, routes, or the confirmation KILL on coverage. R5's margin now also applies against the random arm.

