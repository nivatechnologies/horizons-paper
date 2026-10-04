---
created: '2026-10-03'
related:
  - T_Research-Paper-Guideline
  - T_Spec-Integrity-Gate
  - R_Adapt-The-Physics-Results-2026-09
  - WO_Aspen-Info-Efficiency-Kill-Test-2026-10-03
  - WO_Aspen-Act-Beyond-Horizon-Kill-Test-2026-10-03
status: issued
tags:
  - work-order
  - paper
  - aspen
  - world-models
  - generalization
  - extrapolation
title: 'WO: Aspen kill test A, where the evidence isn''t'
type: work-order
---
# Aspen kill test A: where the evidence isn't

> **Amendment 1 (2026-10-04) is at the end of this WO and supersedes any conflicting text above. Read it first.** It pins referents, readings and precedence pre-emptively, after the act-beyond-the-horizon WO stopped at its gate for the same defect classes ([[R_Aspen-Act-Beyond-Horizon-Spec-Gate-2026-10-04]]). Still run the full gate.

Stage-1 kill test under [[T_Research-Paper-Guideline]] for the Aspen abstract (deadline Oct 9).

**Thesis under test.** Out of distribution is a property of the question, not of the input. A learned world model fails on a query when the test point is displaced from the training data **along the directions that query is sensitive to**, and is largely unaffected by an equal displacement orthogonal to them. A model that carries the law and identifies parameters at run time is insensitive to the direction; its error depends only on how well the query's own context window identifies the parameters.

**Why this design.** The novelty check found that projecting a query's sensitivity onto data-informed directions is established in calibration of mechanistic models and, for networks, in weight space after training (Madras et al. 1910.09573). It also found that training-data Fisher information is not coverage. So this WO measures coverage directly, in physical-parameter coordinates, before any training, with a controlled-angle experiment rather than a correlation over uncontrolled points.

**Repo and branch:** `nivatechnologies/horizons-paper`, branch `paper/aspen-2026-10`, work under `aspen/evidence/`. Reuse the Adapt-the-Physics Kolmogorov solver, World D generator, chaos gate, the L_range and FNO-Re training code, and the NUMBERS checker.
**Results by:** 2026-10-06.
**Compute:** Baccus, the GB10 Spark, the 128-core machine, cloud B200 if needed. Stopping the Qwen vLLM services needs Todd's go.
**Standalone:** no Niva platform code. No AI attribution in commits.

## Spec integrity gate

Before executing, run checks 1 to 9 including 5a in [[T_Spec-Integrity-Gate]] against this work order and report the results. For each threshold, state a concrete passing input and a concrete failing input, and cite each or label it a hypothesis under test per check 5a. The query set is a selector; check 9 is satisfied by Step 0. Report the authorship of every other selector (angle set, displacement size, arms). If any check fails, do not execute that part; report and stop for that part.

## Step 0: blinded query set (Codex)

Before any data, run OpenAI Codex CLI with exactly this prompt and nothing else. Commit prompt and verbatim answer as `aspen/evidence/CODEX_QUERIES.md`.

> A 2D incompressible flow on a 2π-periodic square is computed with the vorticity equation, Kolmogorov forcing A·sin(4y), Reynolds number Re and linear drag α. An engineer forecasts it from a short window of full-field observations. Propose four scalar forecast quantities, each evaluated a fixed short time ahead, that a practitioner would care about, chosen so that they depend on (Re, A, α) in clearly different proportions. Give the exact formula for each.

Use Codex's four queries. Claude's set (kinetic energy, enstrophy, drag dissipation α·2E, forcing power input) is reported alongside, with the overlap.

## Systems

- **K, Kolmogorov (World D truth).** 64², forcing sin(4y), Δ = 0.35, full-field vorticity, 2% RMS noise, window w = 11, query horizon 0.5 Lyapunov times of the test system.
- **D, damped-driven pendulum in state space** (cheap second system). θ = (g/L, c, F, drive frequency). Queries from the same Codex step, with the pendulum description substituted; commit separately.

## Coordinates and the index (computed before any training)

- **Whitened parameters:** u = (θ − μ_train) / half-range, per parameter, so one training-range width is a unit step.
- **Query sensitivity:** g = ∂q/∂u at the test point, by central differences on paired solver runs from the same initial states, averaged over 64 attractor states at that θ.
- **Displacement:** d = u* − Π(u*), where Π is the nearest point of the training box.
- **The two terms:**
  - D_g = |ĝ · d|, the displacement along the query's sensitivity.
  - D_⊥ = |(I − ĝĝᵀ) d|, the displacement orthogonal to it.
  - Context identifiability I = gᵀ F_ctx⁻¹ g, the query variance induced by parameter uncertainty given the context window (F_ctx from solver tangent-linear runs, initial state as nuisance where feasible; label the approximation used).

## The controlled-angle panel

- **Training box:** Re ∈ [34, 46], A ∈ [0.9, 1.1] × nominal, α ∈ [0.8, 1.2] × 0.07733 (K). Analogous box for D, in the freeze.
- **Test points:** for each query, displacements of magnitude 1.0 (one width) from the box face, at angles 0°, 45° and 90° to that query's ĝ, plus magnitude 0 (in-distribution reference). Where an angle is not realizable within the chaos gate, take the nearest realizable angle and record it.
- **Panel:** 100 test states per test point.

## Arms

- **L_range-3:** history-conditioned FNO trained across the 3-parameter box (the L_range recipe).
- **FNO-θ:** FNO given the true θ as input, trained across the box (the FNO-Re recipe, extended to three parameters).
- **Law arm:** true model family with all three parameters identified at run time from the context window (the P1x identifier, extended to three parameters by bounded multi-parameter search).
- **Nulls:** persistence; the law arm at the box-centre θ, no identification.
- **Ensemble disagreement:** 3 seeds of L_range-3, as an after-training reference predictor (not an arm).
- Query error = |q̂ − q| normalized by the query's attractor standard deviation at the test θ.

## Baselines the index must beat (as predictors of error)

Whitened Euclidean distance ‖d‖; Mahalanobis distance to the training distribution; ensemble disagreement.

## Pre-committed outcomes (frozen)

Primary: system K, w = 11, both learned arms.
- **PASS:**
  - Error at 0° is at least 2× error at 90° for at least 3 of 4 queries, for at least one learned arm.
  - Across all test points, Spearman ρ(error, D_g) ≥ 0.6 and ρ(error, D_⊥) ≤ 0.3 for that arm.
  - The law arm's 0°/90° error ratio is ≤ 1.3 for at least 3 of 4 queries.
- **KILL:**
  - Learned-arm error at 0° and 90° is within 1.3× for at least 3 of 4 queries for both learned arms.
  - Or |ρ(error, D_g) − ρ(error, D_⊥)| < 0.15 for both learned arms.
- **Otherwise:** report; Todd decides.
- **Reported, not criteria:**
  - Partial correlations controlling for λ_max(θ*) × horizon.
  - Index against the three baselines.
  - Dependence of the law arm's error on I.
  - System D results.

Two-sided feasibility, both hypotheses under test: pass input, L_range-3 error 0.40 at 0° and 0.12 at 90° on three queries, law arm 0.10 and 0.09; fail input, L_range-3 error 0.30 at 0° and 0.27 at 90°.

Surprise (check 6): learned models fail equally whatever the direction, which would make out-of-distribution a property of the input after all. That is a publishable boundary, not a rescue target.

## Cut order

1. System D. 2. The 45° points. 3. Ensemble disagreement.

Never cut: Step 0, the 0° and 90° points, the law arm, FNO-θ, nulls.

## Deliverables

- NUMBERS sections `AEA*`, with the checker extended to them.
- Freeze (`AEA_FREEZE.md`) before any test-panel data and before learned-arm training.
- Results note generated by script into `04-Results/R_Aspen-Evidence-Alignment-Kill-Test-2026-10.md`.
- Greyscale figures (patterns and direct labels): error against angle per query and arm; error against D_g and D_⊥; the index against the baselines.
- Session-review entries, including spec errors in this WO.

## Amendment 1 (2026-10-04)

**Conventions.** "≥", "≤" and "at least" are inclusive; "<", ">" and "below" are strict. Precedence of outcomes: KILL, then PASS, then otherwise.

**Differential prediction.** These outcomes are unchanged by this amendment:
- a learned arm whose error does not depend on direction still KILLs;
- a query whose 0° or 90° point fails the chaos gate is still unusable and is **not** substituted;
- fewer than three evaluable queries still cannot PASS.

### Scope

System D (pendulum) moves to stage 2. Stage 1 is Kolmogorov only.

### Queries (Step 0)

- Codex's four queries are final.
- A query must be a scalar functional of the state, or of the trajectory up to the query horizon. It is evaluated exactly as Codex wrote it.
- If a formula is not executable as written, ask Codex once with a single clarifying question and record both.
- **Query horizon:** h = 0.5 LT of the test-point θ, from the chaos-gate λ at that θ, after the last observed frame.

### Coordinates, sensitivity and test points

- **Whitened coordinates:** u = (θ − c)/r, where c is the box centre and r the half-range per parameter. The training box is [−1, 1]³.
- **Sensitivity:**
  - g is computed at u = 0 by central differences, step 0.1 in each whitened coordinate.
  - Each difference is paired over 64 attractor states at the centre θ (sensitivity stream), evaluating the query on noise-free true trajectories.
  - ĝ = g/|g|. If |g| < 1e-8 in query units per whitened unit, the query is unusable and reported.
- **Directions:**
  - d0 = +ĝ.
  - d90 = normalize(e_j − (e_j·ĝ)ĝ), where j = argmin_i |ĝ_i| (lowest index on ties), with the sign that makes the e_j component positive.
  - d45 = normalize(d0 + d90).
- **Test point for direction d:** u = s·d, with s > 0 chosen by bisection so that the Euclidean distance from u to the box is exactly 1.0. Map u back to θ.
- **In-distribution reference:** u = 0.
- **Chaos gate:** run at every test point. A failing point is excluded and reported, with no substitution. A query is **evaluable** only if both its 0° and its 90° points pass.
- **Realized displacements, reported:** D_g = |ĝ·(u − Π(u))| and D_⊥ = |(I − ĝĝᵀ)(u − Π(u))|, where Π is projection onto the box.
- **Reported only:** g recomputed at each test point.

### Panels and error

- **Per test point:** 100 states from the test stream, each 200 time units after spin-up at that θ. Each state has an 11-frame observation window with 2% RMS noise, using the harness noise model.
- **Error:** |q̂ − q| / σ_q(θ), where σ_q comes from 1,000 attractor samples at that θ (attractor stream). The point error is the mean over its 100 states.
- **Intervals:** bootstrap intervals over states (B = 2000) are reported. They are not criteria.

### Arms (exact)

- **L_range-3:** the L_range recipe unchanged (architecture, 30,000 steps, checkpoint selection, 11-frame history). The only change is that its 1,024 training conditions are drawn uniformly in the 3-parameter box (training stream).
- **FNO-θ:** the FNO-Re recipe with the three parameters as input channels, trained on the same data.
- **Law arm:** the true model family, with parameters identified by coordinate-wise golden-section search.
  - Three sweeps over (Re, A, α), in that order, 30 evaluations per parameter per sweep.
  - Bounds: Re ∈ [20, 70]; A ∈ [0.5, 1.5] × nominal; α ∈ [0.3, 2.0] × 0.07733.
  - Initialized at the box centre; the misfit is the P1x misfit.
- **Nulls:**
  - Persistence: apply the query to the last observed frame, held fixed.
  - The solver at the box-centre θ, with no identification.
- **Seed streams:** training, validation, sensitivity, attractor, test and identification streams are disjoint, and committed in the freeze.

### Outcomes (replace the earlier block)

For arm a and an evaluable query q, R(a,q) = error at 0° / error at 90°. Q_e is the set of evaluable queries.
- **Insufficient:** if Q_e has fewer than 3 queries, the outcome is otherwise.
- **KILL:** either of these holds for both learned arms:
  - max(R, 1/R) ≤ 1.3 for at least 3 queries in Q_e;
  - |ρ_g − ρ_⊥| < 0.15, where ρ_g = Spearman(error, D_g) and ρ_⊥ = Spearman(error, D_⊥), over that arm's (query, point) units: evaluable queries × {0°, 45°, 90°, centre}, excluding gated-out points.
- **PASS:** a single learned arm a meets all three:
  - R(a,q) ≥ 2 for at least 3 queries in Q_e;
  - ρ_g ≥ 0.6 and ρ_⊥ ≤ 0.3;
  - the law arm has R ≤ 1.3 for at least 3 queries in Q_e.
- **Otherwise:** report; Todd decides.
- **Reported:** both nulls; the index against the baselines; partial correlations controlling for λ(θ)·h; the law arm's error against I.

### Cut order (replaces the earlier list)

1. The 45° points.
2. Ensemble disagreement.
3. Context identifiability I. When computed, use the known-initial-state approximation, labelled as such.
