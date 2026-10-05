# Aspen kill test: good forecasts, wrong actions (v5.1)

**Status.** v5, revised before any data after four GPT design reviews. Their dispositions are in §13 (v1), §14 (v2), §15 (v3) and §16 (v4). Stage 2b tests a two-scale Lorenz-96 in which the physics arm knows only the resolved dynamics (§5b, §7.7). v5 adds a model trained directly on intervention cost (CNN-cost, H1e). v5.1 adds the preflight details from GPT's design go for Stage 1 (§17). Todd approves the headline contract and authorizes execution; nothing runs before that.

**What this is.**
- This is the one permitted pivot under [[T_Research-Paper-Guideline]] §4, after [[WO_Aspen-Act-Beyond-Horizon-Kill-Test-2026-10-03]] returned no PASS.
- It promotes that WO's reported third clause to a headline and tests it on fresh panels.
- If the kill test KILLs, the Aspen paper stops for this deadline and a findings harvest is written.

**Origin of the hypothesis (exploratory, not evidence).** On the AAH Lorenz-96 panel at 2 LT ([[R_Aspen-Act-Beyond-Horizon-Kill-Test-2026-10]]):
- The CNN emulator had point ACC 0.9874 against the physics arm's 0.9625.
- Its top-1 action accuracy was 0.7358 against 0.9637 (193/200 cases eligible), with a cost-difference relative error of 0.6714.
- The myopic null scored 0.8394.

These numbers selected the hypothesis, the primary lead and the thresholds. They are not evidence. Only the fresh panels count.

## 1. Headline contract (for Todd's go)

| Field | Content |
|---|---|
| Headline sentence (assembled only from the licensed sentences in §7.6 and §7.7) | On Lorenz-96, a deterministic learned emulator with window ACC at least as high and window RMSE no higher than a physics arm's identifies the best intervention X% of the time against Y% [and incurs higher energy regret, capturing B_W against B_N of the attainable energy reduction]. The validation-selected emulator retains a W-point gap [; each tested repair's reading is stated]. A model trained directly on intervention cost [retains a gap / is no more than five points worse / is unresolved]. [Two-scale sentence from §7.7.] |
| Revelation | **Now:** world models meant for planning are trained and judged by forecast skill, and residual objective mismatch is assumed to be fixable by training on the decision. **Instead:** in chaotic dynamics, what ranks small interventions is the system's response to them, in both mean and spread. Forecast-trained and rollout-trained deterministic emulators do not recover it; the known law with run-time identification does. Whether training directly on intervention cost (H1e) or on solver-generated counterfactual pairs (H1c) recovers it is tested, not assumed. The clause about training on the decision is used only if H1e RETAINS (S10). |
| Contribution beyond prior work | Lambert et al. 2020 established objective mismatch in model-based RL. Tian et al. 2026 documented unphysical perturbation responses in operational ML weather models. This paper adds three things: (1) the intervention-selection consequence, quantified with exact paired truth in a chaotic system; (2) a budgeted comparison of repairs (longer training, rollout training, decision-window rollout with regret-based checkpoint selection, direct cost training, counterfactual supervision), reporting actual compute; only CNN-roll and CNN-resp are compute-matched; (3) an alternative that works, with its per-decision cost. |
| Incumbent's most natural fixes, and the arms that measure them | CNN-80k (longer); CNN-roll (rollout through the decision window); CNN-R2 (the reviewer-named decision-window rollout with regret-based checkpoint selection); CNN-cost (the reviewer-named decision-trained comparator: predicts intervention cost directly); CNN-resp (counterfactual supervision). |
| Reader, and what they do differently | Physics world-model and ML-weather researchers at Aspen, and weather-intervention groups (Moonshot Goal 8; Huang, Liu and Lall 2026). They would measure an emulator's response fidelity, in mean and spread, before using it to choose interventions. |
| Reader's operating point | Lorenz-96 (N = 40, F = 8), noisy observations, small persistent forcing actions, primary lead 2 LT. All emulators are deterministic; like the physics arms, they get their ensembles from perturbed input windows. In Stages 1 and 2 the physics arm and truth share the law family, with one parameter identified online. **Stage 2b** removes the exact closed law: the truth has unresolved fast variables, and the physics arm (N2) is a hybrid of the known resolved dynamics, a closure fitted from the same X data the base emulator trains on, and an online forcing adjustment (§5b). It is an idealized analogue of unresolved-process parameterization. **Guideline deviation for Todd:** §2 says a toy setting cannot carry the headline. The bridge to real emulators is Tian et al. (GraphCast, NeuralGCM), whose object, an initial-state tangent-linear response, differs from ours, which is a finite persistent-forcing response. |
| Strongest incumbent | L*, the validation-selected emulator: the model in S with the lowest validation-panel regret at T*, which may be an unrepaired model. It is chosen by a rule frozen before any test data, under the isolation rule (§7.3, §9). CNN-cost predicts no states, so it is not an emulator; it is read separately (H1e), and its reading is mandatory wherever S1 or S2 appears. |
| Null models | Random (1/8); myopic (cost over [0, 1 LT] from N-last); best fixed action, chosen on the validation panel. |
| Niva arm | N-last: run-time identification of F plus the deterministic RK4 solver, with paired members. In Stage 2b, N2 (§5b). |
| Publish threshold | H1a PASS and H1b PASS (§7). Any wording that physics makes better decisions in energy terms also needs the regret condition REG (§7.3b). |
| Kill threshold | H1a KILL: every comparably skilled learned model is shown noninferior to the physics arm in top-1, within 0.05. H1b KILL ends the full headline but leaves the counterexample (§7.6). |
| Pre-mortem | (1) "Lorenz-96, matched law": Stage 2b, where only the resolved dynamics are known and the closure is fitted from X data; N-mis covers parametric error. (2) "Weak, undertrained or not decision-trained CNN": the ladder, CNN-R2, L* chosen on validation, and CNN-cost trained directly on intervention cost. (3) "Actions too small to matter": injected work, and the energy reduction relative to taking no action (§6); a δ = 0.04 panel; H1c and H1e show whether the response is learnable. |
| Venue and date | Aspen "World Modeling for Physics" abstract, due Oct 9, 23:59 AoE. |
| Todd go / no-go | **GO**, Todd, 2026-10-04, on v5.1. Covers Stage 1 and the continuation rules in §9. |

## 2. Spec integrity gate

> **Spec integrity gate.** Before executing, run checks 1 to 9 including 5a in [[T_Spec-Integrity-Gate]] against this work order and report the results. For each scoring axis, filter, threshold or classification here, state a concrete passing input and a concrete failing input, and cite each or label it a hypothesis under test per check 5a. For any selector this WO contains or relies on (query set, candidate list, shortlist, taxonomy, vocabulary, comparator or domain framing), report who authored it and satisfy check 9 by a second author or three independent framings. If any check fails, do not execute that part; report the failure and stop for that part. Faithful execution of a defective specification is a worse outcome than a halt.

**Selector provenance**
- **Action set:** blinded Codex run 1 from AAH Step 0, reused unchanged.
- **Authored by Claude after seeing the AAH panel:**
  - the primary lead T* = 2 LT and the thresholds;
  - the CNN ladder, CNN-roll and CNN-resp.

  Independence comes from fresh panels whose seeds are disjoint from every AAH stream.
- **CNN-R2:** named by the GPT reviewer as a second author (check 9) in the design review of 2026-10-04. The executor freezes its details (§5) after Step 0 and before any test access.
- **L*:** chosen by the frozen validation rule, not by any author.
- **Stage 2b system and its physics arm** (two-scale parameters, closure form, F̂ range): authored by Claude in v4, before any two-scale data. The action set is reused unchanged.
- **Named by the GPT reviewer in the v4 review (check 9), specified by Claude in v5:** CNN-cost and CNN2-cost (a history-and-action model predicting expected cost), N2-offline (online forcing adjustment against a forcing fixed offline), the training-seed repeats, observation-conditioned two-scale truth, and the X-only closure fit.

## 3. Step 0: read-only verification at `paper/aspen-2026-10-horizon` @ `1cd0ab7`

Before any new data, confirm each item below against the code and record it in `AFD_STEP0.md`:
1. **CNN:** input history length, input normalization, action-channel encoding, model output spacing, architecture and parameter count (999,681 per the results note), optimizer and learning-rate schedule.
2. **AAH formulas:** the exact ACC, response-correlation and response-relative-error formulas, and whether they use all cases or eligible cases.
3. **Initial states:** the physics arm starts each member from its last perturbed frame; the CNN receives the member's whole window.
4. **LT:** its value in time units from `AAH_FREEZE.md`.
5. **Reuse:**
   - the per-action 500-LT climatology files and their hashes;
   - the F identifier;
   - which model the AAH myopic null used.
6. **Seeds:** the AAH seed namespaces.
7. **Checkpoint, actions and sampler:** the CNN-20k checkpoint hash; the 8 action patterns and their unit RMS; the observation sampler (noise model and window construction).

**Limit on reuse.**
- Where code and this WO differ on anything that defines a scientific quantity (sampler, truth, eligibility, metrics, arm inputs, scoring), stop. Report it, and wait for a WO amendment before data.
- Only non-definitional details (I/O, batching, file layout) follow the code without amendment.

**Push** `paper/aspen-2026-10-horizon`, `paper/aspen-2026-10-evidence` and this WO's branch to `origin` (`nivatechnologies/horizons-paper`). No AI attribution in commits.

## 4. System, panels and truth

- **System:** Lorenz-96, N = 40, true F = 8, RK4 with dt 0.01 in float64. LT as recorded in `AAH_FREEZE.md`.
- **Actions:**
  - The 8 Codex run-1 patterns p_k, each at unit RMS; the action is δ·8·p_k, applied persistently from t = 0.
  - Primary δ = 0.02. Secondary δ = 0.04, the edge of the learned training range [−2δ, 2δ].
- **Cost:** C = the mean of E = (1/2N)Σx_i² over the decision window [T, T + W], with W = 1 LT, sampled every 0.05 time units. T and T + W are rounded to the nearest 0.05 output time, and the window includes both ends; the resulting output indices are recorded in `AFD_FREEZE.md`. The same rule applies to every lead and window in this WO.
- **Observations:**
  - y_t = x_true(t) + ε_t, with ε ~ N(0, (0.02σ)²) independently per site and frame; σ is the attractor spatial RMS.
  - The window is 11 frames at 0.05 spacing, ending at t = 0.
- **Case generation:**
  - Each case starts from its own independent random initial condition, spun up for 50 LT.
  - No two cases, in any panel, share a trajectory.
  - **The case is the statistical unit for every case-level interval.**
- **Member windows:**
  - Member m's window is y + fresh noise from the same model.
  - All operational arms use identical member windows, paired across actions.
- **Panels:**

  | Panel | Cases | Purpose |
  |---|---|---|
  | Test | 200 (`afd-test-*`) | All readings |
  | Validation | 100 (`afd-val-*`) | CNN-R2 and CNN-cost checkpoint selection, L* selection, best-fixed null; never read for outcomes |
  | Secondary | 100 at δ = 0.04 (`afd-test2-*`) | Reported only |

- **Truth:**
  - M_truth = 2048 members per case and action from the panel's truth stream, with true F and the same sampler.
  - **Split-sample eligibility:**
    - the winner b is the argmin of the mean cost over members 0–1023;
    - the case is eligible if, for every j ≠ b, the one-sided lower bound of the mean paired difference C_j − C_b over members 1024–2047 is > 0;
    - the bound is computed as mean − z·sd/√1024, with z = 2.983 (level 0.01/7).
  - Eligibility uses truth only, so it cannot favour any arm.
  - Cross-check: a paired bootstrap with B = 20,000, which puts about 29 replicates in the tail. Report agreement.
  - The truth-best action for scoring is b. J*(c, k), the mean over all 2048 members, is used for regret and response metrics.
  - Report any eligible case where the full-sample argmin differs from b.
  - **No-action reference:** the truth also runs the unforced case (u = 0) on the same members, giving J*_0(c). It is not a choice for any arm and plays no part in eligibility, which ranges over the 8 actions. It measures how much energy the actions can save (§6).
- **Timestep check (before any truth is generated, for each system):**
  - On 16 cases from `afd-dtcheck` (`afd2-dtcheck` for Stage 2b), with all 8 actions, run 512 truth members at dt and at dt/2 from identical member initial states.
  - Pass if every cost difference J_k − J_b (b from the dt run) changes between resolutions by less than the larger of 0.05·S_J and two standard errors of that change, computed from the paired members. S_J is computed on these 16 cases.
  - Otherwise halve dt for that system, record it, and repeat.
  - **Propagation:** in Stages 1 and 2 the physics arms use the truth's dt, so a refinement applies to truth, every one-scale solver run and the physics arms, and per-decision cost is reported at the dt used. In Stage 2b a refinement applies to every two-scale solver run (truth, training data, labels); N2 and its variants keep their own dt of 0.01.
  - The check runs before any panel is generated.
  - Report how often the argmin changes between resolutions.
- **Leads:**
  - Primary T* = 2 LT, so the decision window is [2, 3] LT.
  - Secondary 1, 1.5, 2.5, 3, 4 and 6 LT, reported only.
- **Seeds:**
  - PCG64 hierarchical SeedSequence, with namespaces `afd-test-truth`, `afd-test-arm`, `afd-val-truth`, `afd-val-arm`, `afd-test2-truth`, `afd-test2-arm`, `afd-train-pairs`, `afd-train-cost`, `afd-cnn-seed2`, `afd-cnn-seed3`, `afd-dtcheck` and `afd-bootstrap`.
  - Assert leaf uniqueness, and disjointness from every AAH namespace.

## 5. Arms

**Physics arms**

| Arm | Definition |
|---|---|
| **N-last** (Niva arm) | F̂ per case by golden-section search on [6, 10] with 30 evaluations, fitted to the observed window y (AAH A7). Each member starts from its last frame. RK4, M = 64, paired. |
| **N-oracle** (privileged reference) | As N-last, with true F. It sets the sampling floor for the response metrics. Every training trajectory uses F = 8, so a forcing fixed offline from training data equals the true F; N-oracle is therefore also the offline-forcing comparison for N-last. |
| **N-mis** (sensitivity) | As N-last, with F̂ × 1.1. |
| **N-win** (secondary) | As N-last, with a strong-constraint 4D-Var initial state per member. It minimizes the misfit over the member's 11-frame window with L-BFGS (at most 200 iterations), starting from the first frame, then propagates to t = 0. Members whose fit is non-finite or fails to converge are dropped (rules in §6). |

**Learned set S**, used for H1a, H1b and H1d. Every model keeps the AAH CNN interface.

| Arm | Recipe |
|---|---|
| **CNN-20k** | The existing AAH checkpoint, unchanged. |
| **CNN-5k, CNN-80k** | The base recipe from scratch, same seed, differing only in update count. If the learning-rate schedule is tied to total updates, scale it. Checkpoint selection as in the base recipe. |
| **CNN-roll** | Fine-tuned from CNN-20k for 10,000 updates. State rollout loss unrolled through **T* + W = 3 LT** on the paired training set. Final checkpoint. |
| **CNN-R2** (reviewer-named) | Decision-window rollout training. Keep the CNN interface and train state rollouts through 3 LT. Initialize from CNN-20k or from scratch; the executor freezes the choice. Total training GPU time at most 4× the recorded GPU time of the AAH CNN-20k training on the same GPU type, counting the 20k base if it is used. If that record is missing, at most 10 GPU-hours. Save a checkpoint every 2,000 updates and **select by mean normalized regret at T* on the validation panel** (M = 64, validation member windows). Optimizer, loss weighting, unroll schedule, validation sampling and checkpoint rule are frozen in `AFD_FREEZE.md` after Step 0 and before test access. |

**Repair subset Rep** = {CNN-80k, CNN-roll, CNN-R2}, with baseline CNN-20k. CNN-5k and CNN-20k are in S but are not repairs.

**Seed repeats** (reported; not in S). CNN-20k-s2 and CNN-20k-s3: the base recipe, identical except for training seeds from `afd-cnn-seed2` and `afd-cnn-seed3`. Each is scored against the H1a witness criteria at the same level as a witness in S. Report how many of the three base models (CNN-20k and the two repeats) meet them. Every other recipe has one training run.

**CNN-cost** (decision-trained comparator and H1e; not in S, because it predicts no states).
- **Model:** the AAH CNN input interface (member window and action channel) and convolutional trunk, with the state output replaced by global pooling and a scalar head that predicts the window-mean energy over [T*, T* + W]. The executor freezes the architectural details.
- **Training set** (`afd-train-cost`): 16,384 start states drawn from the learned-train trajectories, disjoint from every panel. For each start, build the observation window and one member window as in §4. Run the true solver from that member window's last frame under each of the 8 actions at amplitude δ, as one truth member would be run. The 8 labels are the realized window-mean energies; the input is the member window.
- **Loss:** for each start, the squared error of the 8 predictions after subtracting their mean across actions (the part that ranks actions), plus the squared error of that mean. Each term is normalized by its variance on the training set and weighted equally.
- **Budget and selection:** as CNN-R2: at most 4× the recorded AAH CNN-20k GPU time, or 10 GPU-hours if that record is missing. Save a checkpoint every 2,000 updates and select by mean normalized regret at T* on the validation panel. Details are frozen in `AFD_FREEZE.md` before any test access.
- **Scoring:** Ĵ_cost(c, k) is the mean of its predictions over the 64 member windows. It is scored on the primary test panel at T* only. Forecast-skill and response metrics are unavailable for it.
- **Disclosure:** its labels are solver-generated for every action from the same state. Report its solver data cost with CNN-resp's.

**CNN-resp** (positive control and H1c; not in S). Identical to CNN-roll, plus a paired-difference loss.
- **Paired training set:** from `afd-train-pairs`, 4,096 start states drawn from the learned-train trajectories. Each gets one unordered action pair (j, k) drawn uniformly from the 28 pairs, and one shared amplitude a ~ U[−2δ, 2δ]. Run the true solver for 3 LT from the same true start under each action. Build input windows exactly as the base recipe does.
- **CNN-roll loss:** L_roll = the mean over steps of ‖x̂ − x‖², over both continuations.
- **CNN-resp loss:** L_roll + L_diff, with L_diff = the mean over steps of ‖(x̂^(j) − x̂^(k)) − (x^(j) − x^(k))‖².
- **Normalization:** compute the constants for L_roll and L_diff once, at the CNN-20k checkpoint, on the same first 64 batches, before either arm updates. Both arms use these frozen constants; the weights are then equal.
- **Matched training:** same optimizer, batch, data order and 10,000 updates as CNN-roll. Final checkpoint.

**Nulls**
- Random (1/8).
- Myopic: N-last's cost over [0, 1 LT].
- Best fixed: the action most often truth-best (b) at T* on the validation panel.

**Numerics:** run all CNN inference on one full-FP32 CUDA backend with TF32 disabled and deterministic cuDNN.

## 5b. Stage 2b: two-scale Lorenz-96, where only the resolved dynamics are known

**Purpose.** In Stages 1 and 2 the physics arm runs the exact law. Here the truth has unresolved fast variables, as in Lorenz (1996), and the physics arm is a hybrid: the known resolved dynamics, a closure fitted from X data, and an online forcing adjustment. It is an idealized analogue of unresolved-process parameterization. N2's closure and CNN2-20k are fitted from the same X-only training trajectories, so they differ in how they represent the missing dynamics, not in what data they see. CNN2-roll and CNN2-cost also use solver-generated counterfactual data (§5), which N2 does not.

**Truth system**
- Slow variables, k = 1..40: dX_k/dt = −X_{k−1}(X_{k−2} − X_{k+1}) − X_k + F − (hc/b)·Σ_j Y_{j,k} + u_k.
- Fast variables, j = 1..10 for each k: dY_{j,k}/dt = −cb·Y_{j+1,k}(Y_{j+2,k} − Y_{j−1,k}) − c·Y_{j,k} + (hc/b)·X_k. The fast variables form one cyclic chain of 400 (Y_{11,k} = Y_{1,k+1}), as in Lorenz (1996).
- Parameters: K = 40, J = 10, F = 10, h = 1, b = 10, c = 10. These are Lorenz's two-level values, with K = 40 so the Codex action set applies unchanged.
- Integration: RK4 in float64 with dt = 0.001. Two checks before any two-scale truth: the decision-cost timestep check in §4, and a state check (from 16 attractor states integrated to t = 0.1, max|X_dt − X_dt/2| ≤ 1e-6·σ_X). If either fails, halve dt and record the change.
- Actions act on X only: u = δ·10·p_k (10 is the RMS of the base forcing), with the same eight patterns, δ = 0.02, persistent from t = 0. The no-action reference of §4 is run as well.
- Per-action X climatologies come from 500-LT_ref two-scale runs.

**Observations and sampler**
- Only X is observed, with noise of 2% of σ_X (the attractor RMS of X), on the same 11-frame window at 0.05 spacing.
- Member windows are built as in §4.
- **Observation-conditioned fast state.** Truth members start from the member's last X frame. Their fast state is drawn conditional on the X history, not taken from the realized Y:
  - draw an initial fast state from a library of 4,096 fast states saved from independent two-scale attractor runs (`afd2-fastlib`);
  - integrate the fast equations alone over the member's window (0.5 time units, five fast damping times 1/c), with X prescribed by linear interpolation between the member's window frames;
  - the fast state at the window's end is the member's Y(0).
- Members are paired across actions, so each member's fast state is drawn once and shared by all actions. Neither arm observes Y, so the truth-best action is defined from the information the arms have.
- **Hidden-state sensitivity** (reported; not used for any reading): on 50 test cases (`afd2-test-oracle`), also compute a 1,024-member truth whose fast state is the realized Y_true(0) plus independent noise of 2% of σ_Y. Report how often b changes, and the change in each arm's top-1 and regret.

**Leads.** Leads are in model time: T* = 2 LT_ref and W = 1 LT_ref, where LT_ref is the one-scale Lyapunov time from `AAH_FREEZE.md`. They are not Lyapunov times of the two-scale system. Before any test data, characterize two-scale slow-variable error growth: from 16 states (`afd2-twin`), run twin pairs with X perturbed by 2% of σ_X and fast states conditioned as above, and report the median X RMSE/σ_X and ACC against lead, with the leads where ACC crosses 0.9 and 0.5. Secondary leads are 1 and 1.5 LT_ref only, whose windows lie inside the primary run. Report every arm's two-scale point-ACC curve.

**Truth, eligibility and panels**
- As §4: M_truth = 2048 with split-sample eligibility.
- 200 test cases and 100 validation cases. Each comes from its own independent spin-up of at least 50 LT_ref; no trajectory is shared.
- Seeds: `afd2-test-truth`, `afd2-test-arm`, `afd2-test-oracle`, `afd2-val-truth`, `afd2-val-arm`, `afd2-train`, `afd2-train-cost`, `afd2-fastlib`, `afd2-twin`, `afd2-dtcheck` and `afd2-bootstrap`, disjoint from every other namespace.

**Arms**

| Arm | Definition |
|---|---|
| **N2** (Niva arm: known resolved dynamics, closure fitted from X, online forcing adjustment) | dX_k/dt = −X_{k−1}(X_{k−2} − X_{k+1}) − X_k + F̂ + P(X_k) + u_k. **Closure from X only:** on the `afd2-train` trajectories, the same ones CNN2-20k trains on, store X every 0.005 time units; estimate dX_k/dt by centred differences; subtract the resolved terms −X_{k−1}(X_{k−2} − X_{k+1}) − X_k and the trajectory's recorded action u_k; fit the residual by least squares as c0 + a1·X_k + a2·X_k² + a3·X_k³, pooled over k and time. P(X) = a1·X + a2·X² + a3·X³ is then frozen, and c0 is kept for N2-offline. No quantity derived from Y is used. **Online forcing adjustment:** F̂ per case by golden-section search on [4, 16] with 30 evaluations, fitted to the observed window. With closure error, F̂ acts as an effective bias correction, not an estimate of the physical F. Members start from their last frame. RK4 with dt 0.01; M = 64, paired. |
| **N2-offline** (attribution) | As N2, with the forcing fixed at c0 from the closure fit instead of identified per case. |
| **N2-noclosure** (sensitivity) | As N2, with P ≡ 0. |
| **CNN2-20k** | The AAH base CNN recipe, trained on X from `afd2-train`: 2,048 trajectories of 25 LT_ref, each with an action pattern drawn from the eight and an amplitude in [−2δ, 2δ]. 20,000 updates, with the base checkpoint rule. |
| **CNN2-roll** | As CNN-roll (§5), fine-tuned from CNN2-20k. Its paired training set is built as in §5 from `afd2-train`: the true two-scale solver runs from the same full state under each action, and the inputs are X only. |
| **CNN2-R2** | As CNN-R2 (§5), on two-scale data, with checkpoints selected on the two-scale validation panel. |
| **CNN2-cost** | As CNN-cost (§5), on two-scale data (`afd2-train-cost`): 16,384 start states drawn from the `afd2-train` trajectories; each member start gets a fast state conditioned as for truth members, and all 8 actions are run with the two-scale solver. Checkpoints selected on the two-scale validation panel. |
| **Nulls** | Random; myopic, using N2; best fixed action, from the two-scale validation panel. |

Stage 2b omits CNN-resp (budget) and an oracle arm (no one-scale law is exact). All metrics, failure handling, reliability and tie rules follow §6, computed on X.

## 6. Metrics

Notation: arm a, case c, action k, lead T. Ĵ_a is the mean over the arm's M = 64 members. Unless stated, averages run over **eligible** cases, which are the cases decisions are scored on. All-case versions are reported alongside.

- **Top-1:** P_a is the fraction of eligible cases where argmin_k Ĵ_a = b.
- **Forecast skill over the decision window:**
  - **wACC_a:** the mean over output times in [T, T + W] of the AAH A1 spatial ACC. It is computed between the arm's ensemble-mean state and the realized true state under action k (true initial state, true F), with anomalies from the action-k climatology. Set ACC = 0 if Σa_f² < 1e-24·Σa_o². Averaged over eligible cases and all actions.
  - **wRMSE_a:** the same window and average, using RMSE/σ.
  - Report the AAH point ACC at T as well, for replication.
- **Cost forecast error** (reported): the mean of |Ĵ_a − J*| / S_J over eligible cases and actions.
- **Response metrics (measured before any cost is computed).** The member-mean energy at a time is (‖x̄‖² + tr Cov(x))/(2N), with the member covariance normalized by 1/M. An action's effect on cost therefore has a mean part and a spread part, and both are scored.
  - **Mean-state response error, MSRE_a:** Δx̄_a(c, k, t) is the arm's ensemble-mean state under action k minus that under action b, at output times t in the window; Δx̄* is the same from the 2048-member truth. MSRE_a = √(Σ‖Δx̄_a − Δx̄*‖²) / √(Σ‖Δx̄*‖²), summed over eligible cases, k ≠ b and window times.
  - **Variance response error, VRE_a:** Δv_a(c, k, t) = tr Cov_a(x | k, t) − tr Cov_a(x | b, t); Δv* is the same from truth. VRE_a = √(Σ(Δv_a − Δv*)²) / √(ΣΔv*²), over the same entries.
  - **Cost-difference split:** for each arm, report how much of its cost-difference error comes from the mean part and how much from the spread part. The two parts sum exactly to the window-mean cost difference.
- **Ranking metrics** (descriptive):
  - the per-case Spearman correlation between Ĵ_a(c, ·) and J*(c, ·) over the 8 actions, averaged over eligible cases;
  - the sign accuracy of the winner-versus-runner-up margin.
- **Cost-difference RE and correlation** (descriptive; as defined in v1 of this WO): over all 28 action pairs. If Step 0 shows AAH computed them differently, report both.
- **Regret (the practical decision metric):** R_a is the mean over **all** cases of (J*(c, chosen) − min_k J*) / S_J, where S_J is the panel median of (max_k J* − min_k J*). Also report eligible-case regret, raw energy units and realized regret. ΔR_L = R_L − R_N, with a paired bootstrap over cases.
- **Energy saved relative to no action:** B_a = Σ_c (J*_0(c) − J*(c, chosen_a)) / Σ_c (J*_0(c) − min_k J*(c, k)), over all cases: the fraction of the attainable energy reduction that arm a's choices capture. Also report, for each arm and for b, the raw reduction J*_0 − J*(chosen) and that reduction as a percentage of J*_0.
- **Action usage:** the frequency of each action as b and as each arm's choice; the fraction of cases where b differs from the best fixed action; and, over the 8 actions, the rank correlation between per-action injected work and the panel-mean J*(·, k).
- **Injected work:** R_W, the ratio of the action's work (1/N)∫Σ_i δ·8·p_k,i·x_i dt to the base forcing's work (1/N)∫Σ_i F·x_i dt over [0, T + W], on truth trajectories, averaged over cases and actions and reported per action. In Stage 2b, use δ·10 and F = 10.
- **Per-decision cost:** end-to-end wall time and compute per decision.
  - N-last: identification plus 8 actions × 64 members to T + W.
  - Learned arms: inference.
  - Report learned training cost, and the solver data cost of CNN-resp and CNN-cost, separately.
- **Drops and failures (learned arms and N-win):**
  - A member is unstable if any state is non-finite or its RMS exceeds 10× the attractor RMS; for CNN-cost, if any prediction is non-finite. It is dropped for all actions; metrics use the survivors.
  - A case with more than 50% of members dropped is a **failed case** for that arm. Its values:
    - top-1 wrong;
    - expected regret equal to the case's worst regret, (max_k J* − min_k J*) / S_J, and realized regret equal to its realized counterpart;
    - ACC 0 at every window time.
  - Failed cases are excluded from wRMSE, MSRE, VRE, cost forecast error, the ranking metrics and cost-difference RE. Each of those is reported with its count of excluded cases.
  - **Reliability rule:** an arm with more than 1% failed cases or more than 1% dropped members cannot:
    - be an H1a PASS witness;
    - support H1b PASS as L*;
    - count in the H1d set (it is listed as unstable);
    - if it is CNN-resp or CNN-roll, support any H1c or H2 reading other than inconclusive;
    - if it is CNN-cost, support any H1e reading other than UNRESOLVED.
- **Intervals:** paired bootstrap over cases (B = 2000; `afd-bootstrap`), with levels stated per criterion. A one-sided bound at level q is a percentile of the bootstrap distribution: the lower bound is its (1 − q) quantile and the upper bound its q quantile, using NumPy's default linear interpolation.
- **Unavailable values:** if the denominator of MSRE, VRE or cost-difference RE is exactly zero, or S_J is zero, that metric is unavailable for that arm and lead. B_a is unavailable if its denominator is ≤ 0. Forecast-skill and response metrics are unavailable for CNN-cost. No epsilon is used.
- **Ties:**
  - ties in argmin_k Ĵ_a, in choosing b, and for the best fixed action go to the lowest action index in the Codex run-1 order;
  - L* ties go to lower validation regret, then higher validation wACC, then lower validation wRMSE, then the frozen order CNN-R2, CNN-roll, CNN-80k, CNN-20k, CNN-5k.

## 7. Pre-committed outcomes (frozen in `AFD_FREEZE.md` before any test access)

Precedence within each hypothesis: **KILL, then PASS, then otherwise.** An unavailable statistic satisfies no clause. "≥" and "≤" are inclusive; "<" and ">" are strict.

**Point-estimate forecast comparisons are operational rules, labelled as such.** Decision gaps use interval rules.

### 7.1 Sufficiency (test panel, T*)

- At least 80% of cases are eligible.
- P_N − max(P_myopic, P_fixed) ≥ 0.05.

If either fails, the outcome is **otherwise** (INSUFFICIENT or TRIVIAL), and no H1 to H3 reading is made.

### 7.2 H1a: counterexample replication

The comparable set is C = {L ∈ S : wACC_L ≥ wACC_N − 0.01}. This is operational.

- **KILL:** C is nonempty, and for every L in C the one-sided upper bound of P_N − P_L is ≤ 0.05, at level 1 − 0.05/|C|. This is noninferiority of the learned model within 0.05; it allows the learned model to be better.
- **PASS:** some eligible witness L in C meets all three:
  - wACC_L ≥ wACC_N and wRMSE_L ≤ wRMSE_N (operational);
  - P_N − P_L ≥ 0.15;
  - the one-sided lower bound of P_N − P_L is ≥ 0.10, at level 1 − 0.05/|S|.
- **Otherwise:** anything else.
- PASS and KILL are exclusive: a witness's point gap of at least 0.15 forces its upper bound above 0.05.

### 7.3 H1b: validation-selected emulator (headline condition)

- L*, the validation-selected emulator, is the model in S with the lowest validation mean normalized regret at T*. It may be unrepaired. Ties follow §6. It is a deterministic function of validation outputs under the isolation rule (§9), and its selection time is recorded.
- G* = P_N − P_{L*} on the test panel.
- **KILL:** the one-sided 95% upper bound of G* is ≤ 0.05.
- **PASS:** G* ≥ 0.10, the one-sided 95% lower bound of G* is ≥ 0.05, and L* meets the reliability rule in §6.
- **Otherwise:** inconclusive.

### 7.3a H1d: every tested repair

Each reliable repair X in Rep gets one reading at T*, using one-sided bounds of P_N − P_X at level 1 − 0.05/|Rep|:
- **RETAINS a gap:** the lower bound is > 0.05.
- **CLOSES (no more than five points worse):** the upper bound is ≤ 0.05. The repair may be better than the physics arm.
- **UNRESOLVED:** otherwise.

Separately, X **NARROWS** the base model's gap if P_X − P_20k ≥ 0.05 and the one-sided lower bound of P_X − P_20k, at the same level, is > 0.

- **H1d HOLDS:** every reliable repair in Rep RETAINS a gap. An unreliable repair is listed as unstable and is not counted.
- **H1d FAILS:** otherwise.

### 7.3b Regret condition REG(L)

- REG(L) holds if ΔR_L > 0 and its one-sided lower bound is > 0. The level depends on how L was chosen:
  - L*, chosen on validation: 95%;
  - a witness W chosen on test results: 1 − 0.05/|S|, simultaneous over S;
  - CNN-cost, specified in advance and not selected on test: 95%;
  - S6: 1 − 0.05/(|S| + 2), simultaneous over S, CNN-resp and CNN-cost.
- Without REG, a top-1 gap licenses only "identifies the best intervention less often". It never licenses "chooses worse" or any energy-based recommendation.

### 7.3c H1e: model trained directly on intervention cost (reported; mandatory wherever S1 or S2 appears)

G_cost = P_N − P_cost, with one-sided 95% bounds.
- **RETAINS a gap:** the lower bound is > 0.05.
- **CLOSES (no more than five points worse):** the upper bound is ≤ 0.05. CNN-cost may be better than the physics arm.
- **UNRESOLVED:** otherwise, or if CNN-cost fails the reliability rule.

### 7.4 H1c: counterfactual supervision (reported; licenses S4, S4b or S5)

G_resp = P_N − P_resp.
- **CLOSES:** the one-sided 95% upper bound of G_resp is ≤ 0.05, and CNN-resp meets the reliability rule.
- **OPEN:** G_resp ≥ 0.10, the one-sided 95% lower bound is > 0, and CNN-resp meets the reliability rule.
- **Inconclusive:** otherwise.

### 7.5 H2: repair effect (CNN-resp against CNN-roll, matched)

- **Evaluable only if P_N − P_roll ≥ 0.15.**
- **REPAIR WORKS:** P_resp − P_roll ≥ 0.10 with one-sided 95% lower bound > 0; |wACC_resp − wACC_roll| ≤ 0.02 and |wRMSE_resp − wRMSE_roll| ≤ 0.02; and CNN-resp meets the reliability rule.
  - If MSRE_resp ≤ 0.7·MSRE_roll **and** VRE_resp ≤ 0.7·VRE_roll, report that the added loss improved both the mean and the spread response at matched forecast skill.
  - If only one of the two improves, the mechanism is unresolved.
- **REPAIR FAILS:** the one-sided 95% upper bound of P_resp − P_roll is ≤ 0.05, |wACC_resp − wACC_roll| ≤ 0.02 and |wRMSE_resp − wRMSE_roll| ≤ 0.02. This is a failed repair; it does not refute the response mechanism.
- **Inconclusive:** otherwise.

**H3: rollout-training extrapolation** (reported). Motivated by Tian et al.; it tests this WO's extrapolation, not their claim about their models.
- **Supported** if all of these hold:
  - wACC_80k ≥ wACC_20k − 0.005 and wACC_roll ≥ wACC_20k − 0.005;
  - MSRE and VRE of both CNN-80k and CNN-roll are each ≥ 0.8× CNN-20k's.
- **Not supported** if any of those four response errors falls below 0.8× CNN-20k's.
- **Unavailable** if any of those arms was not run.
- **Inconclusive** otherwise.

### 7.6 What each outcome licenses (frozen)

Only these sentences may appear in the abstract. Each is used only when its condition holds, and each names only arms that were run.

| # | Licensed sentence | Condition |
|---|---|---|
| S1 | "A deterministic learned emulator (W) with window ACC at least as high and window RMSE no higher than the physics arm's identifies the best intervention less often: P_W against P_N." | H1a PASS. If several witnesses pass, name the one with the highest test wACC (ties by the frozen order in §6) and list all of them in the results. |
| S1s | "Of three independently trained base models, k meet the same criteria." | The seed repeats ran (§5). **Mandatory** with S1 when they ran. |
| S1+ | "…and incurs higher energy regret: R_W against R_N, capturing B_W against B_N of the attainable energy reduction." | S1 and REG(W) at the simultaneous level |
| S2 | "The validation-selected emulator (L*) retains a G*-point gap." | H1b PASS |
| S2+ | "…with higher energy regret, capturing B_L* against B_N of the attainable energy reduction." | S2 and REG(L*) |
| S3 | "None of the tested repaired models (named) closes the gap; each retains one." | H1d HOLDS. Name only repairs that ran; "the longer-trained model" only if CNN-80k ran. |
| S4 | "The model trained with an added loss on solver-generated counterfactual pairs closes the gap, gaining D points over its otherwise identical rollout-trained twin." | H1c CLOSES **and** H2 REPAIR WORKS |
| S4b | "The counterfactual-supervised emulator is no more than five percentage points worse than the physics arm." | H1c CLOSES without H2 REPAIR WORKS |
| S5 | "This counterfactual-pair repair retains a gap." | H1c OPEN |
| S6 | "Physics with run-time identification makes better intervention decisions than every tested learned model, in this matched-law setting." | S2+, S3, S5 and S10, plus REG at the S6 level for every reliable model in S, CNN-resp and CNN-cost |
| S7 | Each repair's reading, in the words of §7.3a: "Repair X retains a gap"; "Repair X is no more than five points worse than the physics arm"; or "Repair X's gap is unresolved (interval a to b)". Add "and narrows the base model's gap" only when NARROWS holds. | **Mandatory** wherever S2 appears and H1d does not HOLD, so that no contradicting or unresolved result inside the paper's scope is omitted. |
| S10 | "A model trained directly on intervention cost, with solver-generated labels for every action, also identifies the best intervention less often: P_cost against P_N." | H1e RETAINS |
| S10+ | "…with higher energy regret." | S10 and REG(CNN-cost) |
| S10b | "A model trained directly on intervention cost, with solver-generated labels for every action, is no more than five points worse than the physics arm: P_cost against P_N." | H1e CLOSES |
| S10c | "Whether a model trained directly on intervention cost retains a gap is unresolved (P_cost against P_N, interval a to b)." | H1e UNRESOLVED |
| S8 to S12 | Two-scale sentences | §7.7 |

- **Full headline (publish threshold):** S1 and S2.
- **Mandatory companions of S1 or S2:** one of S10, S10b or S10c; S1s if the seed repeats ran; S7 as stated; S9 as stated in §7.7.
- **The clause about training on the decision.** The revelation's claim that training on the decision does not remove the mismatch requires S10. With S10b, the headline is the forecast-versus-decision gap for state-trained emulators, and S10b replaces that clause; Todd decides whether this is still the Aspen headline.
- **H1b KILL or otherwise:** S1 only, as a counterexample. This is scope narrowing; Todd decides whether it is still an Aspen headline.
- **H1a KILL:** stop. Findings harvest.
- **H1a otherwise:** report; Todd decides.
- **Model-level wording.** Each recipe was trained once, except the base recipe when the seed repeats ran. Sentences name trained models ("the rollout-trained model"), not recipes ("rollout training does not…"). The Setup states this once.
- **Scope.** Sentences about emulators refer to the tested deterministic emulators. No sentence generalizes to probabilistic or generative world models.
- **No sentence may say** that counterfactual supervision is necessary, or that physics must stay online.

### 7.7 Stage 2b: two-scale outcomes

These are read on the two-scale test panel at T*, with these substitutions:
- N2 replaces N-last;
- S₂ = {CNN2-20k, CNN2-roll, CNN2-R2};
- Rep₂ = {CNN2-roll, CNN2-R2}, with baseline CNN2-20k;
- L*₂ is chosen on the two-scale validation panel;
- CNN2-cost replaces CNN-cost.

All definitions, levels, reliability, tie and isolation rules are those of §6 and §7.2–§7.3c.

- **Sufficiency₂:** at least 80% of cases are eligible, and P_fixed ≤ 0.85. Otherwise the two-scale outcome is otherwise (INSUFFICIENT or TRIVIAL).
- **H1a₂, H1b₂, H1d₂, H1e₂ and REG₂:** as §7.2 to §7.3c.
- **Physics-arm floor:** if P_N2 − max(P_myopic, P_fixed) < 0.05, report that the physics arm, knowing only the resolved dynamics, is no better than a trivial rule at T*.
- **Attribution to the online forcing adjustment:** no sentence attributes a Stage-2b result to it unless S12 holds. P_N2off is N2-offline's top-1, reported either way.

| # | Licensed sentence | Condition |
|---|---|---|
| S8 | "With unresolved fast scales, where the physics arm knows only the resolved dynamics and fits its closure from the X data the base emulator trains on, a deterministic learned emulator (W2) with window ACC at least as high and window RMSE no higher also identifies the best intervention less often: P_W2 against P_N2." | Sufficiency₂ holds, the physics-arm floor holds, and H1a₂ PASSes. This is a two-scale counterexample, not the strongest-incumbent result. |
| S8+ | "…and the validation-selected emulator retains a G*₂-point gap [with higher energy regret]." | S8 and H1b₂ PASS [and REG₂(L*₂)]. Required for any two-scale wording beyond the counterexample. |
| S7₂ | Each two-scale repair's reading, in the words of S7. | **Mandatory** wherever S8+ appears and H1d₂ does not HOLD. |
| S11 | CNN2-cost's reading, in the words of S10, S10b or S10c. | **Mandatory** wherever S8 appears, if CNN2-cost ran. |
| S12 | "The online forcing adjustment adds D points over a forcing fixed offline." | P_N2 − P_N2off ≥ 0.05, with one-sided 95% lower bound > 0 |
| S9 | "With unresolved fast scales, [the two-scale panel could not test the claim / the comparably skilled emulators are no more than five points worse than the physics arm / the physics arm is no better than a trivial rule / the comparison is unresolved]." | Stage 2b ran and S8 is not licensed. Take the first bracket that applies, in this order: Sufficiency₂ fails; H1a₂ KILLs; the physics-arm floor fails; otherwise. **Mandatory** wherever S1 or S2 appears. |

If Stage 2b does not finish by the Oct 8 evidence cutoff, it is reported as not run, and no two-scale sentence is licensed.

## 8. Two-sided feasibility

**Every input below is a constructed hypothesis under test (check 5a), not a measurement.**

| Criterion | Passing input | Failing input |
|---|---|---|
| Eligibility (one challenger shown) | Confirmation-half paired differences: mean 0.020, sd 0.15, n 1024 → bound 0.0060 > 0 | Mean 0.010 → bound −0.0040: ineligible |
| Sufficiency | 170/200 eligible; P_N 0.96, myopic 0.84, fixed 0.40 → gap 0.12 | Myopic 0.93 → gap 0.03: TRIVIAL |
| H1a PASS | N: wACC 0.95, wRMSE 0.30, P 0.964. CNN-20k: wACC 0.97, wRMSE 0.25, P 0.736, lower bound at the 99% level 0.16, 0 failed cases | CNN-20k wRMSE 0.33 > 0.30: not a witness |
| H1a KILL (noninferiority) | C = {CNN-20k, CNN-80k}, with upper bounds of the gap at the 97.5% level of 0.04 and 0.03 | CNN-80k upper bound 0.07: not KILL |
| H1a witness eligibility | CNN-20k with 0.5% failed cases | 2% failed cases: excluded as a witness |
| H1b PASS | L* = CNN-R2; test G* 0.14, lower bound 0.08 | G* 0.12, lower bound 0.04: otherwise |
| H1b KILL | G* 0.01, upper bound 0.04 | Upper bound 0.06: not KILL |
| H1d HOLDS | Rep = {80k, roll, R2}, all reliable; lower bounds of the gap at the 98.3% level 0.08, 0.11, 0.07: all RETAIN | CNN-80k gap 0.20 with interval −0.01 to 0.41: UNRESOLVED, so H1d FAILS and S7 reports it as unresolved |
| Repair CLOSES | CNN-R2 upper bound 0.04: no more than five points worse | Upper bound 0.06 and lower bound 0.02: UNRESOLVED |
| NARROWS | P_80k − P_20k = 0.12, lower bound 0.04 | Difference 0.04: does not NARROW |
| REG(W), simultaneous | R_W 0.12, R_N 0.04; lower bound of ΔR at the 99% level 0.02 | 95% lower bound 0.01 but 99% lower bound −0.005: REG(W) fails; only "identifies the best intervention less often" |
| S4 against S4b | H1c CLOSES and H2 REPAIR WORKS: S4 | H1c CLOSES with P_roll 0.96, so H2 is not evaluable: S4b only |
| Sufficiency₂ | 180/200 eligible, P_fixed 0.60 | P_fixed 0.88: TRIVIAL |
| S8 / S9 | H1a₂ PASS: CNN2-20k wACC 0.97 against N2 0.93, top-1 0.70 against 0.90, lower bound 0.12: S8 | H1a₂ KILL: S9, "the comparably skilled emulators are no more than five points worse" |
| S8 against S8+ | H1a₂ PASS and H1b₂ PASS: S8+ | H1a₂ PASS and H1b₂ KILL: S8 only, as a counterexample, with S11 |
| S12 | P_N2 0.90, P_N2off 0.82, lower bound 0.03: S12 | P_N2off 0.87, difference 0.03: no attribution to the online adjustment |
| H1e RETAINS / CLOSES | P_N 0.96, P_cost 0.80, lower bound 0.09: RETAINS (S10) / P_cost 0.97, upper bound 0.02: CLOSES (S10b) | P_cost 0.93, lower bound −0.01, upper bound 0.07: UNRESOLVED (S10c); or RETAINS-level bounds with 2% failed cases: UNRESOLVED |
| Seed repeats (S1s) | CNN-20k and both repeats meet the witness criteria: k = 3 | One repeat's wRMSE exceeds N's: k = 2, stated in S1s |
| Energy saved, B | Σ(J*_0 − min_k J*) = 12.0; physics choices save 11.0, W's save 7.2: B_N 0.92, B_W 0.60 | Σ(J*_0 − min_k J*) = −0.3: B unavailable |
| Timestep check | Largest change in J_k − J_b 0.01·S_J, with 2 SE of the change 0.03·S_J: pass | Change 0.08·S_J with 2 SE of 0.03·S_J: halve dt |
| H1c CLOSES / OPEN | G_resp 0.00, upper bound 0.03, 0% failed cases / G_resp 0.12, lower bound 0.04 | G_resp 0.06, lower bound −0.01, upper bound 0.12: inconclusive; or CLOSES-level bounds with 2% failed cases: inconclusive |
| H2 REPAIR WORKS | P_roll 0.74, P_resp 0.90, lower bound 0.09, ΔwACC 0.01, ΔwRMSE 0.01 | ΔwRMSE 0.03: not WORKS (inconclusive) |
| H2 mechanism wording | MSRE 0.65 → 0.30 and VRE 0.70 → 0.35: both improved | VRE 0.70 → 0.68: mechanism unresolved |
| H2 REPAIR FAILS | P_resp 0.75, upper bound of the difference 0.04, ΔwACC 0.01 | Upper bound 0.08: inconclusive |
| H3 supported | CNN-20k MSRE 0.60, VRE 0.70; CNN-80k 0.55 and 0.66, CNN-roll 0.58 and 0.64 (all ≥ 0.48 and 0.56 respectively); wACC within 0.005 or higher | CNN-roll VRE 0.50 < 0.56: not supported |

**Surprise (check 6).** The spec could return:
- CNN-R2 closes the gap (H1b KILL);
- counterfactual supervision closes it (H1c CLOSES);
- a model trained directly on intervention cost closes it (H1e CLOSES);
- the counterexample fails to replicate (H1a KILL);
- the physics arm loses its advantage once only the resolved dynamics are known (S9).

## 9. Stages, gates and compute

**Stage 1: kill test.**
- Run test and validation truth; N-last, N-oracle, CNN-20k and the nulls; all leads.
- Read sufficiency, then H1a with S = {CNN-20k}.
- **KILL:** stop. Write [[F_Aspen-Forecast-Decision-Kill-Test-2026-10]]. The paper stops for this deadline.
- **PASS or otherwise:** proceed automatically to Stage 2. Todd's approval of this WO authorizes that step.
- Stage-2 training may run during Stage 1. Validation readings for CNN-R2 and CNN-cost checkpoint selection, and for L*, may run during Stage 1. No Stage-2 model touches the test panel before the Stage-1 reading.
- Stage 1 starts once its own preflight passes (Step 0, the gate checks, the one-scale timestep check, and the freeze) and Todd's execution go is recorded. It does not wait for any Stage-2 artifact.
- A Stage-1 PASS replicates the counterexample with CNN-20k. It does not show that repairs fail or that physics should replace learned planning, and no sentence is licensed before the Stage-2 reading.

**Isolation rule (validation selection and test access).**
- Before any data are generated, `AFD_FREEZE.md` fixes every rule: training recipes, budgets, checkpoint rules (including CNN-R2's and CNN-cost's), the closure-fitting rule, validation sampling plans and the L* rules. L* is a deterministic function of validation outputs.
- Artifacts those rules produce later (the dt chosen by each timestep check, closure coefficients and c0, the fast-state library, training sets and checkpoints) are hashed into `AFD_ARTIFACTS.md` when produced, and each before its own evaluation on a test panel. Stage 1 needs only its checkpoint, numerical settings and inputs recorded; later artifacts are appended before their own evaluations.
- Training and selection workers have no read access to test outputs. Only the coordinator reads Stage-1 results.
- Record when L* selection completed, when test data were generated and read, and every agent with test access.
- After any test result exists, no frozen training or selection item may change. If one does, the affected results (H1b, H1d, and every sentence that depends on them) are labelled exploratory, or require a fresh confirmation panel. Todd's approval can authorize revised work, but cannot restore confirmatory status.
- The same rule applies to Stage 2b, with its own validation panel and L*₂.

**Stage 2: robustness pilot.**
- Run all of S plus CNN-resp, CNN-cost, the seed repeats, N-mis, N-win and the δ = 0.04 panel.
- Read final H1a, H1b, H1d, H1e, REG, H1c, H2 and H3, energy saved, action usage, injected work and the per-decision cost.
- Send a gate summary to Todd in the guideline template, with the licensed headline from §7.6 and §7.7.

**Stage 2b: two-scale test (§5b).**
- Runs in parallel with Stage 2 after the Stage-1 reading, and stops if Stage 1 KILLs.
- The timestep and state checks, fast-state library, closure fit, error-growth twins, training data, truth ensembles and training may start during Stage 1.
- **Sampler check before two-scale truth.** On the 16 twin states, draw 64 conditioned fast states per state and compare the subgrid term −(hc/b)·Σ_j Y_{j,k} at t = 0 with its realized value: report the ratio of the draws' spread to the error of their mean, and the correlation of that mean with the realized value. Two-scale truth waits for Todd's go on this report.
- Readings follow §7.7. The hidden-state sensitivity is reported with them.

**Compute** (verify capacities read-only at launch):
- **sulaco:** truth (both systems), physics arms and bootstrap on CPU; CNN inference on its CUDA GPU.
- **Baccus:** CNN training.
- Do not stop the Qwen services. No cloud.
- Stage 1 within one day. Training: at most 40 GPU-hours for Stage 2 and 20 for Stage 2b, 60 in total. If a cap would be exceeded, apply the cut order; CNN-roll, CNN-resp, CNN-R2, CNN-cost, CNN2-20k, CNN2-R2 and CNN2-cost keep priority.
- **Stage 2b truth is the largest CPU job.** A plain NumPy benchmark (2-core container, one batch of 2048 two-scale members) took 0.060 s per RK4 step at dt 0.001. With LT_ref assumed to be 0.6 time units, the 300 cases × 9 runs (8 actions and no action) × 2048 members to 3 LT_ref come to about 81 single-core hours. The conditioned fast states, CNN2-cost labels, hidden-state sensitivity, timestep check and training data add about 15 more. Parallelize across cases (or run on a GPU), measure the rate first, and start during Stage 1. If the measured rate puts Stage 2b truth past Oct 7, apply the cut order.

**Dates**
- **Oct 5:** gate, Step 0, freeze, timestep checks, Stage-1 data; fast-state library, closure fit and training start.
- **Oct 6:** Stage-1 reading.
- **Oct 7:** Stage-2 and Stage-2b readings.
- **Oct 8:** independent factual check of headline numbers against NUMBERS.
- **Oct 9:** Todd decides the abstract.

## 10. Cut order

1. The δ = 0.04 panel.
2. N-win.
3. Leads 4 and 6 LT.
4. CNN-5k.
5. N-mis.
6. N2-noclosure.
7. The hidden-state sensitivity.
8. The seed repeats. If cut, S1s is not used and every sentence stays at model level.
9. CNN-80k. If cut, H3 is unavailable.
10. CNN2-roll.

**Never cut:**
- test and validation truth, including the no-action reference, and the timestep checks;
- N-last, N-oracle, CNN-20k, CNN-roll, CNN-R2, CNN-resp and CNN-cost;
- the nulls;
- the sufficiency rules, decision-window forecast metrics, MSRE, VRE, energy saved and action usage;
- per-decision cost and injected work;
- if Stage 2b runs: two-scale truth, N2, N2-offline, CNN2-20k, CNN2-R2, CNN2-cost and the error-growth twins.

If Stage 2b cannot finish by Oct 8, report it as not run (§7.7).

## 11. Deliverables

- **Branch** `paper/aspen-2026-10-forecast-decision`, based on `paper/aspen-2026-10-horizon` @ `1cd0ab7`. Work under `aspen/forecast_decision/`; push to `origin`.
- **Before any data are generated:**
  - `AFD_STEP0.md`;
  - `AFD_FREEZE.md`, holding:
    - this WO's numbers and rules, the CNN-R2, CNN2-R2, CNN-cost and CNN2-cost specifics, the closure-fitting rule, and the L* and L*₂ rules;
    - seeds, source SHAs and the hashes of existing checkpoints.
- **When produced, and each before its own evaluation on a test panel:** `AFD_ARTIFACTS.md`, with the dt chosen by each timestep check, the closure coefficients and c0, the fast-state library, and the hashes of every training set and selected checkpoint. Stage 1 needs only its own entries.
- **NUMBERS:** sections `AFD*`. The checker recomputes every verdict and which §7.6 and §7.7 sentences are licensed, including the mandatory companions, and rejects NaN in criteria. Include a tamper test.
- **Results note,** generated by script into `04-Results/R_Aspen-Forecast-Decision-Kill-Test-2026-10.md`.
- **Claim ledger:** [[L_Aspen-Forecast-Decision-Claim-Ledger-2026-10]].
- **Greyscale figures** (markers, patterns and direct labels carry every distinction):
  1. Top-1 against decision-window ACC at T*, for every arm (the headline figure).
  2. Top-1 and wACC against lead, for N-last, CNN-20k and L*.
  3. Top-1 against MSRE and against VRE at T*.
  4. Two-scale: top-1 against window ACC at T*, for every Stage-2b arm.

  CNN-cost and CNN2-cost have no window ACC; they appear in figures 1 and 4 as labelled horizontal lines.
- **Session review** entries.

## 12. Prior work to cite and design around

- Lambert et al. 2020, "Objective Mismatch in Model-based Reinforcement Learning", PMLR 120 / arXiv 2002.04523.
- Tian, Holdaway and Kleist 2026, GRL 53, e2025GL119402.
- Huang, Liu and Lall 2026, PLOS Water 5(6): e0000562.
- Liu, Huang and Lall 2026, arXiv 2604.18906.
- Liu, Huang and Lall 2026, Chaos, Solitons and Fractals 210, 118657.
- Liu, Huang and Lall 2026, PRE 113, 064207.
- Mitsui et al. 2025, NPG 32, 457.
- Miyoshi and Sun 2022, NPG 29, 133.
- Kawasaki and Kotsuki 2024, NPG 31, 319.
- Falasca and Zanna, arXiv 2602.13847.
- Kale et al., arXiv 2605.05218.
- "Are AI weather models learning atmospheric physics? A sensitivity analysis of cyclone Xynthia", npj Climate and Atmospheric Science 2025, doi 10.1038/s41612-025-00949-6.
- Bodnar et al. 2025, Nature 641, 1180.
- Lorenz 1996, "Predictability: a problem partly solved", Proc. ECMWF Seminar on Predictability.
- Wilks 2005, "Effects of stochastic parametrizations in the Lorenz '96 system", QJRMS 131, 389–407.
- Voelcker, Liao, Garg and Farahmand 2022, value-gradient weighted model learning, arXiv 2204.01464.
- Hansen, Su and Wang 2023, TD-MPC2, arXiv 2310.16828.
- Two-scale closures with memory and history-based Bayesian closures, arXiv 1612.07223 and 2210.14488 (cited by the v4 reviewer; check authors before citing).

## 13. Design review of v1: disposition (GPT, 2026-10-04) and correction discipline

This table and its differential prediction use v2 terms. In v3, SRE is MSRE (with VRE added), "demonstrated equivalence" is called noninferiority, and §7.6 is a list of licensed sentences rather than a table of rows; "row 4" below corresponds to the S1-only case (§14).

| # | Comment | Class | Disposition | Reason |
|---|---|---|---|---|
| 1 | H1 can PASS on one model while the strongest incumbent closes the gap | A | Fix | Split into H1a (counterexample) and H1b (validation-selected strongest repaired incumbent). The headline needs both; §7.6 maps every combination. |
| 2 | Forecast skill was measured at 2 LT while the decision uses [2, 3] LT; ACC misses amplitude | A | Fix | Comparability now uses window ACC and window RMSE on eligible cases. Point ACC is kept for replication. |
| 3 | Cost-difference RE partly restates the task and is scale-sensitive; "REFUTED" was too strong | A | Fix | The mechanism metric is now SRE (state response, before any cost). RE and ranking metrics are descriptive. H2 reads REPAIR WORKS or REPAIR FAILS; the REFUTED clause is removed. |
| 4 | The fixes were trained over 1 LT for a 3-LT decision | D (accepted: can change the headline) | Fix | CNN-roll and CNN-resp unroll through 3 LT. The reviewer's CNN-R2 is adopted as specified, with regret-based checkpoint selection on validation. |
| 5 | The general revelation is already established; Tian's object differs | C | Fix | The contribution is restated against Lambert and Tian (§1). H3 is relabelled as testing this WO's extrapolation, not Tian's claim. |
| 6 | The matched-law physics arm does not establish physics online; CNN-resp success supports offline supervision | C | Fix | H1c and the §7.6 table decide which claim is licensed. Added per-decision cost and an N-mis arm; the scope is stated. |
| 7 | Eligibility tail resolution; winner-selection bias; point-estimate equivalence | B | Fix | Split-sample truth (2048 members, selection and confirmation halves), a normal bound plus a B = 20,000 cross-check, equivalence via upper bounds, and point-estimate forecast rules labelled operational. |
| 8 | Case independence; drop handling; the limit of "code governs" | B | Fix | Independent per-case spin-ups with the case as the unit. Failed-case scoring is defined for every metric, and drop-affected arms cannot be witnesses. Definitional code differences require an amendment. |
| 9 | The 2% justification compared different quantities | A | Fix | The citation-as-calibration is removed. Injected work R_W is reported; δ is this experiment's forcing amplitude. |

**Differential prediction (v1 → v2).** These cases fail, or fail more easily, under v2:
1. The reviewer's example (CNN-20k gap 0.22, CNN-80k gap 0.00) passed the v1 headline. Under v2 it is H1a PASS. If CNN-80k is L*, H1b KILLs and only the narrowed counterexample headline remains (§7.6, row 4).
2. A witness that forecasts better at 2 LT but worse over [2, 3] LT could pass under v1. It is not a witness under v2.
3. A witness with more than 1% failed cases could pass under v1. It cannot under v2.

**One change makes a KILL harder.** H1a KILL now requires demonstrated equivalence (upper bound ≤ 0.05) instead of a point estimate within 0.05. A noisy near-tie that killed under v1 now reads as otherwise. This loosening of the KILL side is adopted on the reviewer's correctness ground (item 7) and is disclosed here.

## 14. Design review of v2: disposition (GPT, 2026-10-04) and correction discipline

This section uses v3 terms. v4 replaced S7's wording, H1d's set and the S4 condition (§15).

| # | Comment | Class | Disposition | Reason |
|---|---|---|---|---|
| 1 | The full headline could pass while a tested repair closes the gap | A | Fix | H1d (every tested repair) added. S3 is licensed only when it holds, and "longer training" is named only if CNN-80k ran. When H1d fails, the mandatory S7 names the repairs that close or narrow the gap. |
| 2 | Top-1 can favour physics while regret favours the learned model | A | Fix | REG condition added (§7.3b). Without it, the only licensed wording is "identifies the best intervention less often". |
| 3 | SRE misses the spread part of the energy response; H2 matched only on wACC | A | Fix | SRE renamed MSRE and VRE added. The exact mean/spread split of the cost difference is reported. Mechanism wording needs both to improve. H2 also matches wRMSE. |
| 4 | CNN-resp success cannot establish necessity | A | Fix | S4 and S5 wording fixed. The revelation no longer says "only a solver can generate". No necessity or physics-online sentence is licensed. |
| 5 | Order of L* selection and Stage-1 test access | B | Fix | Isolation rule added (§9). |
| 6 | "Demonstrated equivalence" is noninferiority | C | Fix | Renamed. |
| 7 | Failure handling incomplete; reliability not applied to H1c | B | Fix | Every metric now has a failed-case rule. The reliability rule covers H1a, H1b, H1d, H1c and H2. |
| 8 | "Matched compute" overstates; normalization constants | C, B | Fix | Called a budgeted comparison, with actual compute reported. Constants are frozen at CNN-20k before either matched arm updates. |

**Differential prediction (v2 → v3).** These cases license less under v3:
1. **Reviewer's example** (L* = CNN-R2 with a 0.14 gap; CNN-80k with a 0.00 gap):
   - v2 licensed "no tested learned repair closes the gap".
   - v3: H1d FAILS, so S3 is not licensed. S1 and S2 stand, and the mandatory S7 states that longer training closes the gap.
2. **Physics ahead on top-1 but worse on regret** (16 points ahead):
   - v2 licensed "chooses worse".
   - v3: REG fails, so the only licensed wording is "identifies the best intervention less often".
3. **CNN-resp improves the mean response but not the spread:**
   - v2 reported "improved state response".
   - v3 reports the mechanism as unresolved.
4. **CNN-resp CLOSES:**
   - v2 licensed "the need for physics-generated counterfactual supervision". v3 licenses only S4.
   - A CNN-resp with 2% failed cases could CLOSE under v2; under v3 it reads as inconclusive.

No change in v3 makes any PASS, HOLDS or CLOSES easier.

## 15. Design review of v3: disposition (GPT, 2026-10-04) and correction discipline

This section uses v4 terms. v5 replaced "within five points" with "no more than five points worse", and made S3 and S4 refer to trained models rather than recipes (§16).

| # | Comment | Class | Disposition | Reason |
|---|---|---|---|---|
| 1 | S7 treated an inconclusive result as a working repair; narrowing had no baseline | A | Fix | Each repair gets one of three readings: RETAINS, CLOSES within five points, or UNRESOLVED. NARROWS needs a paired bound against CNN-20k. S7 reports the readings verbatim. |
| 2 | S4 attributed closure to the loss without evidence of its effect | A | Fix | S4 needs both H1c CLOSES and H2 REPAIR WORKS. Otherwise the non-causal S4b applies. |
| 3 | H1a allows equal skill while S1 said "better" | A | Fix | S1 now says "window ACC at least as high and window RMSE no higher". |
| 4 | REG for a witness selected on test results needs selection-aware bounds | B | Fix | Simultaneous level over S for S1+; over S and CNN-resp for S6; 95% for the validation-selected L*. |
| 5 | Todd's approval cannot restore confirmatory status | B | Fix | Under the isolation rule, a changed item makes the dependent results exploratory, or requires a fresh panel. |
| 6 | "Repaired emulator" could name an unrepaired arm | C | Fix | S2 now says "validation-selected emulator". The repair subset Rep is defined for H1d and S7. |
| 7 | Zero denominators and tie-breaking | B | Fix | Rules added in §6. |

**Differential prediction (v3 → v4).** These cases license less under v4:
1. **CNN-80k with a 0.20 gap and an interval of −0.01 to 0.41.** v3 mandated "narrows or closes the gap". v4 reads it as UNRESOLVED and says so.
2. **N-last, CNN-roll and CNN-resp all at 0.96.** v3 licensed the causal S4. In v4, H2 is not evaluable, so only S4b applies.
3. **A witness with exactly equal wACC and wRMSE.** v3 said it "forecasts better". v4 says "at least as high" and "no higher".
4. **REG(W) at 95% after test selection.** v4 needs the simultaneous level, so REG is harder to meet.

**One change makes a reading easier, and it is disclosed here.**
- H1d now ranges over the repair subset Rep instead of all of S, with Bonferroni over |Rep| = 3 instead of |S| = 5.
- v3 wrongly required the unrepaired CNN-5k and CNN-20k to retain a gap for a sentence about repairs.
- Correcting that referent makes HOLDS easier to reach.

**Stage 2b** adds a test. It can only add S8 or S8+, or the mandatory boundary sentence S9, which narrows the headline. It cannot make any Stage 1 or Stage 2 reading easier.

## 16. Design review of v4: disposition (GPT, 2026-10-04) and correction discipline

The reviewer also anticipated objections from the workshop's organizers and participants; those are items 3 to 7.

| # | Comment | Class | Disposition | Reason |
|---|---|---|---|---|
| 1 | Two-scale truth used the realized fast state, which neither arm observes | A | Fix | Truth fast states are drawn conditional on the X history (§5b). The realized-state truth is a reported sensitivity on 50 cases. |
| 2 | N2's closure was fitted to subgrid tendencies computed from Y; the emulators see only X | A | Fix | The closure is fitted from the X-only trajectories CNN2-20k trains on, and N2 is described as a hybrid. A learned closure inside the same solver is future work: it compares closure representations and cannot change the physics-versus-emulator reading. |
| 3 | Regret-based checkpoint selection is not decision-aware training | C, D | Fix | CNN-cost and CNN2-cost are trained directly on intervention cost. H1e's reading is mandatory with S1 or S2, and the revelation's decision clause requires S10. The result could change the headline. |
| 4 | A deterministic emulator cannot represent the uncertainty from unresolved scales | C, D | Fix in part | S1 now says "deterministic", and no sentence generalizes to probabilistic or generative world models. CNN-cost predicts expected cost, spread contribution included, so it answers the decision question. N2 is also deterministic, so the comparison is like for like. A generative emulator is future work. |
| 5 | N2 keeps the resolved equation; online identification has no ablation | C, D | Fix | "The weather modeller's actual situation" is removed. N2 is "known resolved dynamics, closure fitted from X, online forcing adjustment". N2-offline is added, and S12 gates any attribution to the online adjustment. In Stages 1 and 2, N-oracle is the offline-forcing comparison. |
| 6a | Two-scale leads use the one-scale Lyapunov time | C | Fix | Labelled LT_ref. Two-scale error growth is characterized before test data. Two-scale secondary leads are limited to 1 and 1.5 LT_ref, for compute. |
| 6b | Case-bootstrap intervals do not establish that a recipe fails | C, D | Fix | Sentences name trained models, not recipes. Two seed repeats of the base recipe are added (S1s; eighth in the cut order). |
| 7a | No measure of practical energy benefit | D | Fix | No-action truth added. B, the fraction of the attainable energy reduction captured, is reported and stated in S1+ and S2+. |
| 7b | Whether the choices depend on the state | D | Fix | Action usage reported: action frequencies, cases where b differs from the best fixed action, per-action injected work. |
| 7c | Decision costs not checked under timestep refinement | B | Fix | A decision-cost timestep check runs before any truth, for both systems (§4). |
| 8 | S8 read as the full result | A | Fix | S8 is the two-scale counterexample. Anything broader needs S8+, with S7₂ and S11 mandatory. |
| 9 | An upper bound shows "no more than five points worse", not "within five points" | A | Fix | Corrected throughout. |
| 10 | The NUMBERS checker must cover §7.7 | B | Fix | §11. |
| 11 | Closure coefficients cannot be frozen before they are fitted | B | Fix | Rules are frozen before any data. Produced artifacts are hashed into `AFD_ARTIFACTS.md` before any arm runs on a test panel. |

**Differential prediction (v4 → v5).** These cases license less under v5:
1. **CNN-20k loses by 20 points, and CNN-cost scores 0.95 against N-last's 0.96 (upper bound 0.04).** v4's revelation implied that training on the decision does not help. v5 must state S10b and drops that clause.
2. **Two-scale H1a₂ PASS with H1b₂ KILL.** v4's S8 said "the same holds". v5 licenses only the counterexample, with S11.
3. **N2 wins because its closure saw tendencies computed from Y.** That advantage does not exist in v5.
4. **A ranking that depends on the realized fast state.** v4's truth used it. v5's truth averages over fast states consistent with the X history.
5. **A learned model 20 points better than the physics arm.** v4 wrote "within five points". v5 writes "no more than five points worse".
6. **A rollout-trained model retains a gap in its one training run.** v4 allowed "rollout training does not close the gap". v5 says "the rollout-trained model".

No threshold or condition in v5 is looser than in v4. The X-only closure fit makes the physics arm's task harder. The conditioned two-scale truth changes the target itself, in a direction no one can predict before data.

## 17. Design go for Stage 1 (GPT, 2026-10-04): disposition

The reviewer found no remaining design blocker for the one-scale kill test and asked that three preflight details be closed. It reviewed the specification, not the implementation.

| # | Comment | Class | Disposition | Reason |
|---|---|---|---|---|
| 1 | Verify reuse against the code, including the checkpoint hash, action patterns and observation sampler | B | Fix | Step 0 item 7 added; the other items were already in Step 0. |
| 2 | Record numerical conventions: bootstrap quantile method, window endpoints, how a timestep refinement propagates | B | Fix | Percentile rule in §6, window rule in §4, propagation rule in the §4 timestep check. |
| 3 | Hash each artifact before its own evaluation, so Stage 1 does not wait for Stage-2 checkpoints | B | Fix | §9 isolation rule and §11. Stage 1's start condition is stated in §9. |
| 4 | The two-scale sampler needs its own execution review | B | Fix | A sampler check is reported before two-scale truth, which waits for Todd's go on it (§9). |

No threshold or reading changed.

