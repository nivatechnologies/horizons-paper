## Amendment 1 (2026-10-04): answers to the spec gate

Numbered to match the nine blocking defects in [[R_Aspen-Act-Beyond-Horizon-Spec-Gate-2026-10-04]]. Equality conventions: every "at least", "≥" and "≤" is inclusive; every "below" and "<" is strict.

**Differential prediction (correction discipline).** These cases stay failed or unavailable after this amendment:
- the gate's overlapping example (T_f = 1, top-1 0.4 at T = 1, 0.85 at T = 4) is **not** a PASS;
- a calibration in which no amplitude on the grid reaches 80% determinable stays **failed**, and the run stops;
- the uncentered control variate stays **unavailable**; it is removed;
- a forecast curve that never crosses stays **censored**, and that system cannot PASS;
- cases with no separation at M = 256 stay **uncommitted**;
- near-ties stay **excluded and reported**.

The amendment unblocks calibration, truth, arms, panels and figures only because their definitions are now executable; no threshold was loosened.

### A0. Final action sets (Step 0 resolution, pre-data)

- **Codex run 1's sets are final for both systems.** Run 1 used no tools and so complied with "nothing else"; run 2 searched the web.
- Run 2's sets and Claude's sets are reported with overlap only; they are not analysed.
- **Velocity-form forcing:** where a Kolmogorov proposal is a velocity forcing, convert it to vorticity forcing by f_ω = ∂x f_y − ∂y f_x.
- **Non-executable formulas:** if a formula is not executable as written, ask Codex once with a single clarifying question and record both.
- **Normalization:** every pattern p_k is normalized to unit RMS over the domain, then scaled. The action is δ·RMS(base forcing)·p_k, so δ is a fraction of the base forcing's RMS.
  - Lorenz-96: base forcing F = 8.
  - Kolmogorov: the base vorticity forcing.

### A1. Forecast horizon T_f (defect 1)

- **Model:** the Niva arm's ensemble-mean forecast (M = 64 members, identified parameters).
- **Target:** for each test case c and action k, the realized true trajectory under action k, run from the true initial state with the true parameters.
- **Anomaly reference:** the action-k climatological mean field.
  - It comes from one long true run per action: 500 LT after 50 LT spin-up, true parameters, sampled every output step.
- **Correlation:** ACC(c, k, T) = Σ a_f·a_o / √(Σ a_f² · Σ a_o²), summed over spatial points at the single time T.
  - Points: the 40 sites for Lorenz-96; the 64² vorticity grid for Kolmogorov.
  - a_f is the forecast anomaly; a_o is the observed (true) anomaly.
  - If Σ a_f² < 1e-12 · Σ a_o², set ACC = 0 (a climatology forecast has no skill).
- **Averaging:** the arithmetic mean over all test cases and all K actions gives ACC(T).
- **Horizon:** T_f is the **first grid point** with ACC(T) < 0.2.
  - If ACC(T) ≥ 0.2 at every grid point, T_f is censored (> 20 LT) and that system cannot PASS or KILL.
- **Reported, not criteria:** T_f for each learned arm, computed the same way from that arm's own ensemble mean.

### A2. Horizon grid and readings (defect 2)

- **Grid:** T ∈ {0.25, 0.5, 0.75, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10, 12, 16, 20} LT, where LT is the unperturbed system's Lyapunov time.
  - One rollout to 21 LT yields every window, so the denser grid adds negligible cost.
- **No interpolation.** Every criterion is read at grid points by these discrete rules:
  - **G(x):** the smallest grid value ≥ x. Undefined if x > 20.
  - **Sufficient grid point:** a grid point counts only if at least 50% of the panel's cases are eligible there (A4). Insufficient points are reported and cannot support a PASS.

### A3. Decision horizon and outcome precedence (defect 3)

- **Sustained decision horizon:** T_d is the largest grid T ≥ T_f such that top-1 accuracy is ≥ 0.8 at **every** grid point in [T_f, T], and each of those points is sufficient.
  - If top-1 at T_f itself is below 0.8, or T_f is not sufficient, T_d is undefined and that system cannot PASS.
- **Precedence:** KILL, then PASS, then otherwise.
- **KILL:** on both systems T_f is defined, and top-1 accuracy at G(1.5·T_f) is below 0.5, with that point sufficient.
- **PASS:** on both systems, all of:
  - T_f is defined;
  - T_d is defined and T_d ≥ G(3·T_f);
  - the member criterion in A5 holds at T_f.
- **Otherwise:** report; Todd decides. This includes a pass on one system, censoring, and insufficient points.
- Accuracy is computed over eligible cases only, with persistent actions, W = 1 LT and M = 64 members drawn from the arm stream.

### A4. Decision truth, eligibility and stream independence (defects 2 and 4)

- **Seed namespaces, disjoint, each committed in the freeze:** calibration, test-truth, test-arm, learned-train, learned-val, climatology, jitter.
  - Within a stream, pairing across actions is exact: the same member index means the same initial window perturbation and the same noise.
- **Truth:** for case c, the truth ensemble draws M_truth members from the test-truth stream with the sampler in A7.
  - Integration uses the **true** parameters.
  - M_truth = 1024 for Lorenz-96 and 512 for Kolmogorov.
  - The expected cost of action k is the member mean.
- **Eligibility per (case, T, W, timing):**
  - b = argmin of the mean cost.
  - Paired bootstrap with B = 2000 replicates (seed in the freeze); the resampling unit is the member index, applied identically to all K actions.
  - For each j ≠ b, take the one-sided lower bound of mean(C_j − C_b) at level 0.01/(K−1) (Bonferroni).
  - The case is eligible if all K−1 lower bounds are > 0. Ineligible cases are near-ties: reported, not scored.

### A5. Members needed and sequential commitment (defect 5)

- **Members needed (fixed-M, the criterion):**
  - For M ∈ {8, 16, 32, 64, 128, 256}, each arm uses the first M members of its stream (nested).
  - M_95 is the smallest M with top-1 ≥ 0.95 on eligible cases. If none qualifies, it is censored at "> 256", and its lower bound is 512.
  - **Member criterion at T_f:** (M_95 unpaired, or its lower bound if censored) ÷ (M_95 paired) ≥ 3. If paired M_95 is censored, the criterion fails.
- **Commitment (reported, not a criterion):**
  - Looks at M ∈ {8, 16, 32, 64, 128, 256}; at each look the leader is the argmin of the mean cost.
  - Commit when, for every j ≠ leader, the paired-bootstrap one-sided lower bound of mean(C_j − C_leader) is > 0 at level 0.05/(6·(K−1)), Bonferroni across 6 looks and K−1 comparisons, with B = 1000.
  - Report the members used at commitment, the empirical error rate against truth, and the cases still uncommitted at 256.
  - The 5% is a nominal design level; the empirical error rate is the reported quantity, not a guarantee.

### A6. Control variate (defect 6)

Removed from stage 1. A linear-response estimator, with a properly centered variate, moves to stage 2. No ranking uses D − L.

### A7. Observations, sampler and identification (defect 7)

- **Observations:** y_t = x_true(t) + ε_t, with ε_t ~ N(0, (0.02·σ)²) independent per grid point and frame. σ is the spatial RMS of the state on the unperturbed attractor.
  - Window: 11 frames ending at t = 0.
  - Frame spacing: Lorenz-96 0.05 time units; Kolmogorov Δ = 0.35, as in the harness.
  - **The truth is used only to generate observations and scores**, never as a forecast input.
- **Sampler (perturbed-observation ensemble; label it as such, not a Bayesian posterior):**
  - Member m's input window is y_{−10..0} + ε_{m,−10..0}, with fresh draws from the same noise model.
  - Solver arms start from the member's last frame.
  - Learned arms receive the member's whole window.
  - **Every arm and the truth use this sampler**, from their own streams.
- **Identification of the parameters:**
  - Kolmogorov: Re by the P1x identifier on the observed window y (not member windows).
  - Lorenz-96: F by golden-section search over F ∈ [6, 10] with 30 evaluations. Integrate from y_{−10} with candidate F, and minimize the squared misfit to y_{−9..0}.
  - All members use the one identified value.

### A8. Calibration, numerics and learned arms (defect 8)

- **Calibration panel:** 40 Lorenz-96 cases and 20 Kolmogorov cases, from the calibration stream, with M_truth for calibration = 512 (L96) and 256 (Kolmogorov).
- **Amplitude grid:** δ ∈ {0.01, 0.02, 0.05, 0.1}, evaluated in ascending order.
  - δ* is the **smallest** δ for which ≥ 80% of calibration cases are eligible at T = 20 LT (A4 rule).
  - If no δ ≤ 0.1 qualifies, calibration FAILS: stop and report. No escalation beyond 0.1.
- **Chaos gate:** applied at δ* for every action. An action that fails is reported, and the run stops for Todd.
- **Numerics:**
  - Lorenz-96: RK4, dt 0.01, float64.
  - Kolmogorov: the harness integrator, time step and precision, unchanged and recorded.
  - Jitter arm: after every integrator step, x ← x ⊙ (1 + 1e-12·ξ), with ξ ~ N(0, I) from the jitter stream, independent per action.
- **Learned arms are reported readings, not criteria, and no strongest-practice claim is made from them:**
  - **Kolmogorov action-conditioned FNO:**
    - Architecture: the L_range recipe, unchanged, plus one input channel carrying the action field.
    - Training data: 1,024 trajectories of 25 LT, each with an action pattern drawn uniformly from the K set and amplitude uniform in [−2δ*, 2δ*].
    - Training: 30,000 steps, one seed.
    - Checkpoint: selected by 1-LT rollout error on 64 learned-val trajectories.
  - **Lorenz-96 emulator:**
    - Architecture: periodic 1-D CNN, about 1M parameters, with the action as an input channel.
    - Training data: 2,048 trajectories, otherwise the same protocol, 20,000 steps.
  - **Latent emulator (cut first):** convolutional autoencoder at 16x compression, plus a latent MLP predictor with action input, 20,000 steps.
  - **Stability rule:** a rollout is unstable if any state is non-finite, or its RMS exceeds 10× the attractor RMS.
    - A member that is unstable under any action is dropped from that case for all actions, which preserves the pairing.
    - If more than 50% of a case's members are dropped, that arm's decision for the case is scored wrong.
    - Drop rates are reported.

### A9. Objectives, regret and correlations (defect 9)

- **Lorenz-96:** E = (1/2N)·Σ x_i², averaged over the window at output spacing 0.05.
- **Kolmogorov:** the total enstrophy dissipation rate D_Z = (1/Re)·⟨|∇ω|²⟩ + α·⟨ω²⟩, viscous plus drag, computed spectrally and averaged over the window at Δ = 0.35. ⟨·⟩ is the spatial mean.
- **Normalized regret:** (C_chosen − C_best) / (C_worst − C_best), using truth expected costs.
- **Realized regret:** the same formula on the realized true trajectory, with the true initial state.
- **Partial correlations:** descriptive only. The unit is the (arm, grid T) pair, pooled over the learned arms, the misidentified solver and the jitter arm, with no inference claimed.

### Cut order (replaces the earlier list)

1. The latent emulator.
2. W = 2 LT.
3. Impulsive actions.
4. Kolmogorov panel reduced from 30 to 20 cases, recorded.
5. The misidentified solver.

Never cut: the decision truth, the Niva arm, the unpaired arm, the jitter arm, the action-conditioned FNO and emulator, the myopic null, either system.
