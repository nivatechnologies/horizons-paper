# Aspen kill test: counterfactual confidence in partially observed chaotic systems (v2.2)

**Status.** Draft v2.2 for Todd's go. Nothing runs before it.
- v2 applies GPT's design review of v1 (2026-10-04). The disposition and differential prediction are in §17.
- v2.1 applies GPT's execution review of v2 (2026-10-04): §18.
- v2.2 replaces the percentile-bootstrap gate bounds after the executor's spec-gate halt (2026-10-05): §19.
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
| Headline sentence (assembled only from §11) | With 11 noisy snapshots spanning 0.84 Lyapunov times, the posterior under the known law answers the sign of a small intervention's effect on window energy with at least 95% probability for X% of case–action questions at 2 LT, against Z% for the sign of the unforced window-energy anomaly. Confident answers are right W% of the time [L1–L3]. The factual and counterfactual futures share their uncertainty: their posterior correlation is ρ, so the difference carries c of the summed uncertainty [L4]. Four measurements targeted at the decision question turn V% of open decision questions into confident, correct answers, against U% for the better of spread-targeted and forecast-targeted measurements [L6]. |
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
| Todd go / no-go | **Pending.** |

## 2. Spec integrity gate

> **Spec integrity gate.** Before executing, run checks 1 to 9 including 5a in [[T_Spec-Integrity-Gate]] against this work order and report the results in `ACD_SPEC_GATE.md`. For each scoring axis, filter, threshold or classification here, state a concrete passing input and a concrete failing input, and cite each or label it a hypothesis under test per check 5a (§12 gives the author's; the executor checks them). For any selector this WO contains or relies on, report who authored it and how check 9 is satisfied. If any check fails, do not execute that part; report the failure and stop for that part. Faithful execution of a defective specification is a worse outcome than a halt.

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
   - `fit_member` uses L-BFGS-B, maxiter 200, F fixed at `identify(y)`;
   - validity requires RMS ≤ 10·SIGMA.
7. **Development inputs:**
   - `runs/test/input_{c:03d}.npz` for c = 0..199 on sulaco, with hashes matching `AFD_ARTIFACTS.md`;
   - `history("afd-observation-test", c, 0.01)` reproduces them bitwise;
   - stored `actual_cost` matches a recomputation to ≤ 1e-12.
8. **CNN-20k:**
   - `inputs/CNN-20k.pt` and its hash;
   - window length and `sigma` normalization;
   - action channel `0.16·p_k/sigma`;
   - whether the zero action lies inside the training action distribution. Report and continue.
9. **Two-scale kernel (R7 only):** `rhs2` (h = 1, c = 10, b = 10 as coded) and `two_scale_state_dt = 0.001`.

**Step 0b: blinded selector (check 9).**
- Before any data and before the spec-gate sign-off, run OpenAI Codex CLI with exactly the prompt below and nothing else. Commit the prompt and the verbatim answer as `aspen/determinacy/CODEX_SELECTOR.md`.
- Report the overlap with this WO's question types (S, P, B, Fc) and targeting rules (question, forecast, spread, random).
- Any Codex question type that can be computed from saved per-draw costs is added as a reported reading. It cannot be a gate or a publish route.

> A chaotic system (the Lorenz-96 model, 40 variables, forcing F) is observed at all sites with noise for a short window. An operator can apply one of eight small persistent forcing patterns, or none, and cares about one scalar outcome: the mean energy over a later time window. Using only the observations and the known equations, list the questions about this particular observed instance that a physicist would most want answered before acting, and for each say how one would judge whether the available observations are sufficient to answer it. Then propose three rules for choosing four additional precise point measurements, taken at the decision time, that would best help answer such questions.

**Limit on reuse.**
- Where code and this WO differ on anything that defines a scientific quantity, stop and report. Wait for an amendment before data.
- Non-definitional details follow the code.

**Branch.**
- `paper/aspen-2026-10-determinacy` from `origin/paper/aspen-2026-10-forecast-decision` @ `1b1094a`; work under `aspen/determinacy/`.
- Import `protocol.py` and `physics.py` unchanged, and record their hashes.
- Push to `origin`. No AI attribution in commits.

## 4. System, panels and realized outcomes

- **System:** Step 0 items 1–5. RK4, dt 0.01, float64. All eight leads, with window [T, T + 1] LT by the inherited predicate. Readings use 2 and 3 LT.
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
  - IDs are 1,200,000 + i, in the `protocol.rng` SeedSequence form.
  - Assert leaf uniqueness and disjointness from `protocol.IDS` and `AAH_IDS`. The `sub` roles go in `ACD_FREEZE.md`.

## 5. The posterior (the Niva arm) and its checks

**Declared model and prior.**
- θ = (x_first ∈ ℝ⁴⁰, F). H_t(θ) is the RK4 state at frame t = 0..10.
- Likelihood: y_t,i ~ N(H_t(θ)_i, (0.02·SIGMA)²), independent.
- Prior: x_first,i ~ N(0, (10·SIGMA)²) independent, which is flat relative to the likelihood; F ~ Uniform(6, 10). The prior is stated in the paper's Setup.
- χ²(θ; y) = Σ(H − y)²/(0.02·SIGMA)², which equals 440·val/(0.02·SIGMA)² on `extras.objective`'s scale.

**Sampler.**
- NUTS (Hoffman and Gelman 2014) with a dense mass matrix adapted in warmup. NumPyro or BlackJAX in float64 is recommended. A sampler written from scratch around the existing adjoint is acceptable only if it passes the implementation check below.
- 4 chains, 1000 warmup and 1000 draws each. Initialize from 4 distinct RML members.
- Thin to S = 512 draws (128 per chain) for forecasting.
- Each draw is propagated to t = 0 and forecast under the 8 actions and no action at all leads, giving J_s(k, T). Per-draw costs are saved.

**Diagnostics, per case.**
- Split R-hat ≤ 1.01 and bulk ESS ≥ 400 for all 41 parameters and the log-likelihood (Vehtari et al. 2021).
- **Gate functionals:** split R-hat ≤ 1.01 and bulk ESS ≥ 400 on the forecast draws for D_k (k = 0..7) and J_8 at 2 and 3 LT. Different functions of one chain can mix differently. If a functional falls short, forecast all 4000 post-warmup draws for that case and recompute.
- **Monte Carlo error of each answer probability:** se(p) = sqrt(p(1 − p)/ESS), using the ESS of the event's indicator.
  - A question with |p − 0.95| < 2·se(p) is flagged threshold-uncertain.
  - It keeps its point classification, and the flagged count is reported per type and lead.
- Divergent transitions ≤ 1% of draws.
- A failing case is rerun once with 2000 warmup. If it still fails, it is excluded and reported.
- More than 5% of cases excluded on a panel is a halt.
- Report F boundary contacts.

**Implementation check (Stage 0).**
- Sample a 41-dimensional Gaussian whose precision is the Gauss–Newton Hessian at the MAP of `acd-dtcheck` case 0.
- The sample mean and all 41 marginal variances must match within 4 Monte Carlo standard errors, and the variances along the largest and smallest Hessian eigendirections within 10%.
- Halt otherwise.

**Joint adjoint (for MAP, RML and any hand-written sampler).**
- Extend `extras.objective` to return ∂/∂F (∂rhs_i/∂F = 1 through the RK4 stages).
- On case 0 of `acd-dtcheck`, at a non-optimal point, the maximum absolute error against centred finite differences (eps 1e-6) over all 41 components must be < 1e-6 on the code's scale. Halt otherwise.

**MAP, multi-start.**
- L-BFGS-B over 41 variables, F ∈ [6, 10], maxiter 500.
- 4 starts: (y_0, F̂ = `identify(y)`), (y_0, 6.5), (y_0, 9.5) and the best RML member.
- χ²_min is the lowest χ² found by any start, member or posterior draw.
- Report the spread of minima across starts, boundary contacts and non-convergence.

**Coverage and fit (reported; gating as stated).**
- **Truth coverage:** Δχ²(θ_true) = χ²((true[0], 8); y) − χ²_min ≤ 56.94 = χ²₀.₉₅(41), with an expected rate of about 0.95 by Wilks' theorem.
  - On a completed 200-case panel, a rate below 0.85 is a halt on development and a KILL on confirmation. Stage 1a (20 cases) has its own floor of 15/20 (§13).
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
- **Climate-confident:** the climatological null gives the same answer for at least 95% of its states.
  - The null knows F = 8 exactly, which the inference does not. That makes the observation-confident share conservative.
  - A climate-confident answer is never described as fixed by physics.
- **Observation-confident:** confident and not climate-confident.
- **Realized answer** a*(q) comes from J*. An exact zero difference counts as "not lower" or "no" and is logged.
- **Split stability (reported):** classification differences between chains {1, 2} and {3, 4}, per type and lead.

**dt check (Stage 0).** On the 8 `acd-dtcheck` cases:
- Forecast the S posterior draws at dt and at dt/2 from the same states and F.
- Pass if, at every lead up to 3 LT, at most 0.5% of (draw, question) answers and at most 1% of classifications differ.
- Otherwise halt.

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
  - at least ⌈0.875·M⌉ valid members per case, with more than 5% of cases short being a halt.
- Unweighted RML is not an exact posterior sampler for a nonlinear forward model (Ba et al. 2021). It is reported as an independent estimate.
- **Comparison with the posterior** is made on the same signed event, never on each sampler's modal probability, which can hide opposite answers. The events are P(D_k < 0) for S_k, P(J_k < J_l) for P_kl and P(J_8 > J̄) for Fc.
  - z = (p_RML − p_post)/sqrt(se_RML² + se_post²), with se_RML = sqrt(p(1 − p)/M_valid) and se_post from §5.
  - **Substantive disagreement:** |z| > 3.
  - Threshold-crossing disagreement is reported as a diagnostic, next to the share expected from Monte Carlo error alone.
  - Mean |p_RML − p_post| and RML's own realized calibration are also reported.
  - RML is approximate. Disagreement alone does not show the posterior sampler is wrong (§13, Stage 1a).

### 7.4 CNN-20k ensemble (R6; confirmation; sulaco GPU)
- 128 windows y + ε_m, using the same ε_m as RML, under the 8 patterns and no action, encoded as in `campaign.inference`.
- Per-member costs are saved. A member that goes invalid under any action is dropped for all actions.
- No training. Do not stop the Qwen vLLM services; halt and ask if GPU memory is short.

### 7.5 Forecast-horizon rule (R2c)
- T_h is the largest lead at which at least half the panel's Fc answers are confident.
- The rule answers every question at leads ≤ T_h with the posterior's modal answer and abstains beyond.

## 8. Targeted measurement (R5)

**Designated question.** At T ∈ {2, 3} LT, P(a1, a2), where a1 and a2 have the lowest posterior-mean J at T.

**Population.**
- The first 100 cases by index in which P(a1, a2) is not confident at T.
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

**Refit.** Rerun the posterior (§5, same diagnostics) with the probe terms added, then recompute p for P(a1, a2).

**Measures.**
- **Settled-correct share C_arm:** the fraction of the population that is confident after the probe and whose modal answer equals the realized answer.
- **Also reported:**
  - settled share regardless of correctness;
  - confident-but-wrong counts;
  - post-probe truth coverage, with probe terms included in Δχ².

**Q-BEATS at T.** All of the following:
1. C_Q − max(C_V, C_F) ≥ 0.10 (gate check 8).
2. Exact one-sided McNemar tests (binomial on the discordant cases) of Q against V and of Q against F both give p ≤ 0.01. Requiring both is an intersection–union test, so no further multiplicity correction applies.
3. Arm Q settles at least 20 questions, with a one-sided 95% Clopper–Pearson lower bound on their accuracy ≥ 0.80 (one settled answer per case, so the answers are independent).
4. Post-probe truth coverage for arm Q is ≥ 0.85.

C_Q against C_R is reported.

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
- whether the leads where the S and Fc confident shares differ match the leads where c_k and the divergence ratio change.

## 10. Readings and statistics

**Statistics (v2.2).** The case is the statistical unit throughout. Every gate and route test is valid at finite sample size; no gate or route uses a percentile bootstrap.

- **Betting bounds for bounded case-level means** (Waudby-Smith and Ramdas 2024). These are used for R0, for the L7 and L8 upper bounds, and for the R2a and R2b intervals.
  - For case values x_c ∈ [0, 1], taken in case-index order, and a null value m ∈ (0, 1), define two capitals: K⁺(m) = Π(1 + λ⁺_c(x_c − m)) and K⁻(m) = Π(1 − λ⁻_c(x_c − m)).
  - **Bets (aGRAPA):** λ⁺_c = clip((μ̂ − m)/(σ̂² + (μ̂ − m)²), 0, 0.75/m) and λ⁻_c = clip((m − μ̂)/(σ̂² + (m − μ̂)²), 0, 0.75/(1 − m)). Here μ̂ and σ̂² are the running mean and variance of the earlier cases plus one pseudo-observation with mean 1/2 and variance 1/4.
  - **One-sided lower bound at level α:** scan a 0.001 grid upward from 0.500. The bound is the last m before the first m at which K⁺(m) never reaches 1/α.
  - **One-sided upper bound:** scan downward from 1.000 with K⁻ in the same way.
  - **Two-sided interval at level α:** m is excluded if max(½K⁺(m), ½K⁻(m)) reaches 1/α at some case. The interval runs from the smallest to the largest grid value not excluded.
  - R2 case-level differences d ∈ [−1, 1] enter as x = (d + 1)/2.
  - **Validity** follows from Ville's inequality. The bounds need no resampling and stay valid when a case's answers fail together or errors are sparse.
- **Clopper–Pearson exact bounds** for one answer per case: R0-F, and R5's settled-answer accuracy.
- **Exact one-sided McNemar tests** for R5's paired comparisons.
- **Descriptive intervals** (R1 shares, R1m, R3, R3b, R6 and every reported-only number) are case-bootstrap percentile intervals, B = 10,000 (`acd-bootstrap`, `sub` = reading number). They are labelled approximate and never gate or license a comparison word. A zero-denominator replicate is redrawn and the count of redraws is reported.
- **Levels:**
  - R0 and R0-F bounds are one-sided at 95%, per lead.
  - The five publish routes (R2a at 2 and 3 LT, R2b, R5 at 2 and 3 LT) each use level 0.01, so their intervals are 99% and their tests use p ≤ 0.01.
- **Statistical audit (Stage 0, synthetic data only, before Step 0).** Write `ACD_STATS_AUDIT.md`. Any failure halts.
  1. Clopper–Pearson and McNemar match `scipy.stats` exact values.
  2. Null validity, with at least 20,000 simulated panels of 200 cases per configuration:
     - the R0 test at case-averaged accuracy exactly 0.90, for each case-size distribution × error mechanism. Sizes: the executor's {0: 0.85, 1: 0.10, 8: 0.05}, uniform on 0–8, and half empty. Mechanisms: independent answers, whole-case errors, and errors only in eight-answer cases;
     - the R2 intervals at mean 0, for symmetric, skewed and sparse case-level differences.
     - Each false-PASS or non-coverage rate must be at most its nominal level plus 2 Monte Carlo standard errors.
  3. The executor's 0.888 counterexample, reported.
  4. A power table, reported: R0 at case-averaged accuracy 0.95, 0.97 and 0.985 with 50, 80, 120 and 160 nonempty cases; R2a at Δ = 0.15 and 0.25.

| Reading | What | Rule |
|---|---|---|
| **R0** (gate, per lead) | Case-averaged accuracy of observation-confident S answers: r_T = mean, over cases with at least one such answer, of a_c = (correct)/(observation-confident S) in case c. The answer-level ratio (all correct)/(all answers) is also computed. | **NOT EVALUABLE:** fewer than 100 such answers or fewer than 30 cases. **PASS:** betting one-sided 95% lower bound on r_T ≥ 0.90, and answer-level point ≥ 0.90. **FAIL:** betting one-sided 95% upper bound on r_T < 0.90. **INSUFFICIENT:** evaluable and neither PASS nor FAIL. Also reported: the answer-level ratio with its own betting lower bound. For each grid value m, it applies the same test to x_c = (n_c/8)(a_c − m) + m ∈ [0, 1], whose mean exceeds m exactly when the answer-level ratio does. Also reported: all confident S; P, B and Fc; reliability diagram (p bins [0.5, 0.6), …, [0.9, 0.95), [0.95, 1]); PIT or rank histogram of realized D_k among draws; coverage; fit flags; split stability. |
| **R0-F** (per lead) | Accuracy of confident Fc answers (one per case) | **NOT EVALUABLE:** fewer than 30 confident Fc. **PASS:** Clopper–Pearson one-sided 95% lower bound ≥ 0.90. **FAIL:** one-sided 95% upper bound < 0.90. **INSUFFICIENT:** evaluable and neither. |
| **R1** | Confidence map | For every type and lead: confident, observation-confident and climate-confident shares, with 95% intervals; S per action. |
| **R1m** | Mechanism | §9. |
| **R2a** (route at 2 and 3 LT) | Same-lead comparison: Δ_T = mean over c of (s_c − f_c), with s_c = (1/8)·#{S_k observation-confident} and f_c = 1[Fc confident] | Needs R0 and R0-F PASS at T. **DIFFERS:** \|Δ_T\| ≥ 0.15 and the 99% interval excludes 0. **EQUIVALENT:** the 99% interval lies within [−0.10, 0.10]. **INCONCLUSIVE:** otherwise. |
| **R2b** (route) | Ordered loss times | Eligible (c, k): S_k observation-confident and Fc confident at lead 0. L_S and L_F are the first leads at which S_k and Fc are no longer confident. A question still confident at 6 LT has its loss **not observed within the tested range**: it counts as later than any observed loss, and two such questions tie. Δ_loss = mean over eligible cases of (mean over that case's eligible k of [1(L_S > L_F) − 1(L_S < L_F)]). Cases with no eligible action are excluded; fewer than 30 eligible cases is NOT EVALUABLE. Needs R0 and R0-F to be PASS or NOT EVALUABLE at every lead. **OUTLIVES:** Δ_loss ≥ 0.20 and 99% lower bound > 0. **PRECEDES:** Δ_loss ≤ −0.20 and 99% upper bound < 0. **NO DIRECTIONAL PREFERENCE:** the 99% interval lies within [−0.10, 0.10]. Otherwise **NO ORDER DETECTED**. Report the eligible counts; the shares of earlier, later, same-lead and both-beyond-range pairs; and the variant using observation-confidence for L_S. |
| **R2c** | Forecast-horizon rule | At every lead: the share of S answered by the rule that are not confident, and their realized accuracy; the share refused that are confident, and their realized accuracy. |
| **R3** / **R3b** | Crude sampler / RML smoother | Confidence shares, realized accuracy of confident S (the R0 statistic), reliability diagram, and classification agreement (Cohen's κ) with the posterior. |
| **R5** | Targeted measurement | §8. |
| **R6** | CNN-20k ensemble | Its confidence shares; realized accuracy of its confident S; among S answers not confident under the posterior, the share it is confident on (X) and its realized accuracy there (Y); κ with the posterior. |
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
| L3a | R2a at T | DIFFERS: "At T the two shares differ by Δ (99% interval [a, b])." EQUIVALENT: "At T the two shares are within 0.10 of each other (Δ, 99% interval [a, b])." INCONCLUSIVE: "At T the difference is Δ (99% interval [a, b]), which establishes neither a difference nor equivalence." |
| L3b | R2b | OUTLIVES: "Paired by case, confidence in an intervention's sign outlasts confidence in the forecast sign: it is lost later in P₊ and earlier in P₋ of case–action pairs (99% interval for the difference [a, b])." PRECEDES: the same with "is lost before". NO DIRECTIONAL PREFERENCE: "Paired by case, confidence in an intervention's sign shows no directional preference between earlier and later loss relative to the forecast sign (Δ_loss, 99% interval [a, b] within ±0.10)." Otherwise the numbers only, with no ordering word. |
| L4 | R0 PASS at T | "At T, the posterior correlation between factual and counterfactual window energies is ρ (median), so the difference carries c of their summed uncertainty; confidence in the sign tracks z_D [binned result]." |
| L5 | R0 PASS at T | "Of the confident sign answers at T, K% are given by climatology at the true forcing; the rest depend on the observations." |
| L6 | R5 at T | Q-BEATS: "Four precise measurements targeted at the decision question turn C_Q of open decision questions at T into confident, correct answers, against C_best for the better of spread-targeted and forecast-targeted measurements, C_R for random sites and C_A for all 40." Otherwise: "Question-, forecast-, spread-targeted and random measurements turned C_Q, C_F, C_V and C_R of open decision questions at T into confident, correct answers; question targeting did not reliably beat the better alternative." |
| L7 | R3, R3b | Crude: if its case-averaged confident-S accuracy at 2 LT is below 0.85 with a betting one-sided 95% upper bound below 0.90, "An ensemble built from perturbed last frames gives confident answers that are right only r_c of the time." Otherwise the neutral form with both numbers. RML: "A randomized-maximum-likelihood ensemble smoother agreed with the posterior on A% of confidence classifications, and its confident answers were right r_m of the time." |
| L8 | R6, R0 PASS at T | "On sign questions where the posterior is not confident at T, a deterministic CNN emulator's ensemble is confident on X% and right on Y% of those." The word "overconfident" only if its case-averaged confident-S accuracy is below 0.85 with a betting one-sided 95% upper bound below 0.90. |
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
| Implementation check | Variances within 4 MC standard errors, eigendirections within 6% → pass | Smallest-eigendirection variance off by 25% → halt |
| Coverage | 0.94, Wilson [0.90, 0.97] → valid | 0.80 → halt or KILL |
| R0 | 410 answers in 120 cases, case-averaged 0.97, betting lower bound 0.93, answer-level 0.97 → PASS | Case-averaged 0.84 with upper bound 0.88 → FAIL. 40 perfect cases, lower bound 0.89 → INSUFFICIENT. 70 answers → NOT EVALUABLE |
| R0, climate-heavy case | — | All confident S at 0.95 but observation-confident upper bound 0.88 → FAIL (v1 would have passed) |
| R0, executor's counterexample | — | No observed errors among about 30 nonempty cases (10 of eight answers, 20 of one) → lower bound 0.86 → not PASS (v2.1 forced PASS) |
| R0-F | 30 confident, all correct → Clopper–Pearson lower bound 0.905 → PASS | 25 of 30 correct → upper bound 0.93 → INSUFFICIENT; 20 of 40 → FAIL |
| R2a | Δ = 0.26 [0.15, 0.37] → DIFFERS | Δ = 0.04 [−0.06, 0.09] → EQUIVALENT. Δ = 0.17 [−0.02, 0.35] → INCONCLUSIVE |
| R2b | Δ_loss = 0.31 [0.12, 0.48] → OUTLIVES. Δ_loss = −0.27 [−0.44, −0.09] → PRECEDES. Δ_loss = 0.01 [−0.07, 0.08] → NO DIRECTIONAL PREFERENCE | Δ_loss = 0.12 [−0.05, 0.30] → NO ORDER DETECTED. 24 eligible cases → NOT EVALUABLE |
| Stage 1a sampler comparison | 14% threshold-crossing disagreement, 0.4% substantive (\|z\| > 3) → continue | 9% substantive, and the posterior rerun disagrees with itself on 3% → halt |
| R5 | C_Q = 0.34, C_V = 0.19, C_F = 0.15; discordant cases 18 against 3 versus V (p = 0.0007) and 21 against 2 versus F (p < 0.0001); 32 of 34 settled correct (Clopper–Pearson lower bound 0.83); coverage 0.93 → Q-BEATS | C_Q = 0.34 against random 0.12 but spread 0.30 → not (v1 would have passed). 34 settled but only 0.71 correct → not |
| L7 crude | 0.78, upper bound 0.82 → strong form | 0.91 → neutral form |
| L8 "overconfident" | 0.70, upper bound 0.78 → used | 0.88 → not used |
| Stage 1 strong | R2b Δ_loss = 0.33, interval excluding 0 | Δ_loss = 0.18 → Todd decides |

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
- **Separability (check 8):** R5 thresholds against the better of the spread and forecast arms. R3, R3b and R6 are reported with intervals, and no ranking beyond L7 and L8 is licensed.

## 13. Stages, gates, compute

| Stage | Dates | Work | Gate |
|---|---|---|---|
| 0 | Oct 5 | Step 0b, then the statistical audit (§10), then spec-gate sign-off; Step 0; `acd_protocol.py`; joint adjoint FD check; sampler implementation check; dt check; climatological null. **Benchmarks**, each including compilation, forecasting and diagnostics: an ordinary case (posterior, RML, crude, forecasts), a 4-site refit, and an all-site refit. **Projection** for every posterior run in Stages 1–3, about 1,900 four-chain runs at the maximum populations (400 ordinary, 500 development refits, 1,000 confirmation refits), plus an allowance for reruns. Write `ACD_NUMERICAL_REPORT.md`. | Halts in §14 |
| 1a | Oct 5 | **Validation, development cases 0–19:** posterior with diagnostics, multi-start MAP, RML, crude; coverage; posterior–RML agreement at 2 and 3 LT. | **Halt** if diagnostics fail in more than 1 of 20 cases, or coverage is below 15/20 (a Stage 1a floor; §5's 0.85 applies to the completed 200-case panel). **Sampler disagreement:** if more than 5% of S questions at 2 LT disagree substantively between posterior and RML (\|z\| > 3, §7.3), rerun the posterior on those cases with a fresh seed and 4 times the draws. Continue if the two posterior runs disagree substantively on at most 1% of those questions, and report RML as biased there; otherwise halt. Threshold-crossing disagreement alone never halts. Report either way. |
| 1b | Oct 5–6 | **Development kill test, cases 0–199:** R0, R0-F, R1, R1m, R2a, R2b, R2c, R3, R3b, and R5 at 2 LT. Script-generated `ACD_STAGE1_READING.md` and the vault note `R_Aspen-Counterfactual-Determinacy-Stage1-2026-10`. Claude writes the gate summary. | **Strong:** R0 PASS at 2 LT, and one of the following. Each must also meet its route's prerequisites from §11: calibration at its own lead, R0-F for R2a, R0 and R0-F PASS or NOT EVALUABLE at every lead for R2b, and R5's count, accuracy and coverage conditions. The options: \|Δ_T\| ≥ 0.25 with the interval excluding 0 (R2a); \|Δ_loss\| ≥ 0.30 with the interval excluding 0 (R2b); C_Q − max(C_V, C_F) ≥ 0.15 with both McNemar p ≤ 0.01 (R5). These are 1.5 times the publish margins. **Stop and report:** R0 FAIL at both 2 and 3 LT. **Otherwise:** Todd decides. |
| 2 | Oct 6–7 | On Todd's go: write `ACD_FREEZE.md` (hashes, namespaces, sub roles, null outputs, thresholds, the Stage 1 reading hash), then the confirmation panel in blind order. Run every reading, with R5 at 2 and 3 LT, and R6. Write `ACD_STAGE2_READING.md`. | Publish, kill or decide (§11) |
| 3 | Oct 7 | R7 if time allows; F1 assembly. | Reported |
| 4 | Oct 8–9 | NUMBERS `ACD_*` and `check_acd.py`; independent factual audit; figures. Claude drafts the abstract from L1–L10. Todd submits. | Release checklist |

**Compute.**
- sulaco CPU for the posterior, fits and integration; sulaco GPU for CNN inference only.
- No training. Do not stop the Qwen vLLM services, and use no cloud.
- Leave the AFD close-out on Baccus untouched.
- If the Stage 0 projection exceeds 12 wall-hours for Stages 1–3, apply the cut order. If it still exceeds 12 wall-hours after every permitted cut, halt and report the projection.

**Figures** are greyscale-safe, with every distinction carried by a second cue.
- **F1, illustrative case chosen by rule:** the first confirmation case in which, at 2 LT, some S_k is observation-confident, P(a1, a2) is not confident, and arm Q resolved it correctly. It shows two posterior draws with opposite answers to P(a1, a2), their diverging trajectories, and the probe. It is labelled illustrative.
- **F2:** confident share against lead per question type, with observation-confident solid and all-confident dashed.
- **F3:** the mechanism: ρ_k, c_k and the divergence ratio against lead.
- **F4:** reliability diagrams for the posterior, RML, crude and CNN.
- **F5:** R5 settled-correct shares by arm, hatched.

## 14. Halts and cut order

**Halts.** Report and wait.
- A Step 0 definitional mismatch.
- Adjoint error ≥ 1e-6.
- The implementation check or the dt check fails.
- More than 5% of cases fail posterior diagnostics after a rerun.
- Development coverage below 0.85 on the completed 200-case panel.
- More than 5% of cases short of valid RML members.
- A Stage 1a halt condition.
- The runtime projection exceeds 12 wall-hours after every permitted cut.
- Any statistical-audit failure (§10).
- The CNN needs the Qwen services stopped.
- Any confirmation reading computed before `ACD_FREEZE.md` is committed.

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
  - `posterior.py` (model, NUTS, diagnostics, implementation check);
  - `fits.py` (MAP, RML, joint adjoint);
  - `questions.py`;
  - `campaign.py`;
  - `measure.py`;
  - `mechanism.py`;
  - `cnn_ensemble.py`;
  - `analysis.py`;
  - `figures.py`;
  - `check_acd.py`.
- **Reports:**
  - `ACD_SPEC_GATE.md`, `ACD_STEP0.md`, `CODEX_SELECTOR.md`;
  - `ACD_NUMERICAL_REPORT.md`, `ACD_STAGE1A_VALIDATION.md`, `ACD_STAGE1_READING.md`;
  - `ACD_FREEZE.md`, `ACD_STAGE2_READING.md`;
  - NUMBERS `ACD_*`, `CLAIM_LEDGER.md`.
- **Vault:**
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

