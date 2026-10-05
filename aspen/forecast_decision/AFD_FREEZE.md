# AFD rule freeze — v5.2 / Amendment 1

Frozen before any new data. Authorization: WO §1 and §18, Todd 2026-10-04, go-v5.2. The original Step 0 halt is resolved. Rules below implement WO §§4–11; the full authoritative WO body is retained as WO_v5.2.md. Source baseline 1cd0ab701b5e663eb7e0304b1d705ddeabe80617. New source is this committed branch; every actual run records its launch commit and executed file hashes. No training/selection rule below changes after any test output exists.

## Numerical windows and sampling

Measured one-scale LT=0.5928295944308761; sigma=4.312600593723798. LT_ref has exactly this value in two-scale. Output tick n is n*0.05. Include n iff n*0.05 >= T*LT−1e-12 and n*0.05 <= (T+1)*LT+1e-12, with exact unrounded endpoints, including tick zero for the myopic window. Same predicate for cost, window forecast skill, response, CNN-cost labels and both systems. Refining dt never changes output ticks or predicate.

| Lead (LT or LT_ref) | Closed output-index set |
|---|---|
| myopic 0 | 0–11 |
| 1 | 12–23 |
| 1.5 | 18–29 |
| primary 2 | 24–35 |
| 2.5 | 30–41 |
| 3 | 36–47 |
| 4 | 48–59 |
| 6 | 72–82 |

Indices above are computed, not estimated (protocol.py). Two-scale only uses 0,1,1.5,2. State rollouts through 3 LT cover tick 36; tick 36 is outside the primary scoring/loss window. Point skill uses nearest 0.05 tick to each nominal lead; true target and arm output at the same tick.

Truth: float64 RK4, one-scale starting dt .01; two-scale starting .001. Cost is 0.5*mean(state²), mean over included ticks. Truth/operational sampling uses independent case random normal initial conditions about forcing, independent spin-up 50 LT, then true history at eleven ticks ending zero; noisy observation SD .02 times attractor spatial RMS; independent additional iid member noise same SD. Truth and arms use disjoint member streams but the same observation; within each stream every action shares the member window. Two-scale conditions Y as in WO, shared across actions. Realized targets start at the true end of history.

Case/member spin-up and data recipe changes explicitly prescribed in the WO supersede historical AAH counts/eligibility; no old test trajectories are reused. Action patterns and normalizations remain the AAH run-1 formulas and order. Primary amplitude .02; optional secondary .04.

Timestep check: all specified 16 cases and 512 paired members, eight actions, every one-scale reported decision window including myopic; two-scale checks its three reported decision windows. Population SD uses ddof=1 for confirmation bounds and SEs. Cost-difference changes are paired per member between resolutions; S_J is median full-member action cost range on these check cases, separately per lead. Every nonwinner gap must change by strictly less than max(.05*S_J,2*SE). Zero S_J is unavailable and cannot pass. Compare argmin as well; keep halving until pass. One-scale refinement propagates to all new one-scale solver-generated data/labels/physics. Existing CNN-20k checkpoint and historical climatology remain unchanged. Two-scale refinement propagates to all two-scale truth/data/labels; N2 remains .01. State check is as WO §5b and cannot be replaced by the cost check.

## Seeds and isolation

PCG64 with SeedSequence [namespace ID, system tag 0, substream, case/start, member, action]. Unique namespace prefixes already separate systems. protocol.py fixes IDs starting at 1100000 in its displayed NAMES order, outside all AAH IDs. Roles/substreams: initial 0, observation 1, member 2, bootstrap 3, action/amplitude 4, fast-state/perturbation 5, training minibatches 6. Paired streams omit action dependence. Assert all planned leaf root tuples unique before generation; assert disjoint from AAH prefixes. Spawned per-case tasks use explicit case IDs. Store seed manifest in each data artifact.

Training and selection processes run in a bubblewrap mount namespace: /mnt masked; only the task's source, train inputs, checkpoints, validation observations/member windows and validation truth are rebound into a worker directory. Old horizon test outputs and all AFD test outputs are inaccessible. Only coordinator inference/scoring reads Stage-1 test outputs. A selection worker gets validation outputs only. Record worker launch identity/access audit, test generation/read times and L* selection times. No Stage-2 model runs test inference until Stage-1 reading exists. Operational input windows contain no truth labels.

## Model architecture and common training

All state emulators use the exact AAH circular residual CNN architecture/interface, 999681 parameters, eleven normalized frames and one physical action field divided by sigma. Base recipes use AdamW lr1e-3, wd1e-4, cosine over total updates, grad norm clip1, effective batch128, four-step autoregressive MSE average plus additional first-step MSE, base one-noise input recipe. Base validation: 64 trajectory-disjoint learned-val trajectories, one-LT state rollout, checkpoints every1000 updates, lowest MSE, first checkpoint on exact tie. Same base torch seed0 and same train minibatch RNG for CNN-5k/80k; schedule scaled to update total. Repeat torch/data-order seeds derive from afd-cnn-seed2/s3, data unchanged. FP32 CUDA, TF32 off, deterministic cuDNN, no mixed precision. Same controls for inference. Memory batching may subdivide examples, preserving effective batch and gradient sum.

Stage 2 uses the retained learned-train and learned-val trajectories for base recipes. They are disjoint from every new panel. Pair starts drawn uniformly over trajectory IDs/time indices, with enough prehistory; action pair uniform over 28 unordered pairs, amplitude uniform [−.04,.04], true deterministic state shared. Exactly 4096 paired starts, solver continuations through tick36, input windows built as base recipe (one observation noise layer). Pair set disjoint from panels by namespace and trajectories.

CNN-roll/CNN-resp initialize from unchanged CNN-20k, effective batch128 paired starts, same deterministic order/torch seed0, AdamW lr1e-4 wd1e-4, cosine over10000 updates, clip1; complete10000 updates, final checkpoint. Rollout MSE uniform over all36 predicted ticks and both continuations. Resp adds paired-difference MSE over the same ticks. Before updates, compute mean roll and difference losses at CNN-20k on the same first64 training batches; use reciprocals as frozen normalization constants, equal weights. Zero/nonfinite normalization constant is a halt, no epsilon. Same effective batches/order across both models. Save actual normalization constants in AFD_ARTIFACTS before test evaluation.

CNN-R2 initializes from CNN-20k. Same pair set and effective batch128, full36-step differentiable unroll, state MSE only at the primary decision-window ticks24–35, equal weights there, both continuations, normalized states. AdamW lr1e-4 wd1e-4 clip1; cosine annealing by elapsed charged GPU time over individual cap. Complete updates until next update would exceed cap (reserve measured maximum recent update duration); save every2000 updates. Candidate checkpoint0 is frozen initialization; no off-grid last checkpoint enters selection. Select minimum validation all-case mean normalized regret, M64 fixed validation windows, all8 actions. Exact tie: earliest update. Failure/drop/worst regret rules match test. Reject nonfinite candidates. Validation normalization S_J comes from fixed validation truth, never test.

CNN-cost: same four Conv1d/GELU trunk layers (12→256→256→256→256, kernel5/circular), adaptive mean pooling over sites, Linear256→64, GELU, Linear64→1, initialized torch seed0. Predict raw window cost; state interface/action encoding unchanged, no state output. Training exactly16384 starts from base train trajectories, each observation+fresh member-noise window, true solver from its last frame under all8 primary actions. Targets are realized cost at ticks24–35. Loss = action-centered eight-prediction MSE / training variance of action-centered labels + MSE of the eight-action mean / variance of training mean labels, equally weighted. Population variances ddof0, no epsilon; zero/nonfinite normalization halts. AdamW lr1e-3 wd1e-4 clip1, effective batch128 starts/all8 actions, cosine by charged GPU time. Checkpoints every2000 updates; same validation regret selection and tie as R2. No initial untrained cost checkpoint may be selected; if no scheduled checkpoint completes, mandatory model not run and report failure.

## Two-scale recipes and closure

Truth equations/parameters and fast-chain cyclic indexing follow WO §5b exactly. Train2048 independently spun trajectories25 LT_ref with random action and signed amplitude; save X at .005, downsample to .05 for CNN base; retain full-state training starts only for generating labels/counterfactuals. Independent64 learned-val trajectories. Base CNN2-20k: same recipe20000 updates, training sigma is measured X attractor spatial RMS. No Y-derived quantity enters a model input or closure fit.

X-only closure: centered finite difference (X(t+.005)−X(t−.005))/.01 at interior stored times, subtract known resolved tendency and recorded action; pooled ordinary least squares columns [1,X,X²,X³] with full rank required, no pseudoinverse fallback. Freeze coefficients a1–a3 and c0; N2 online Fhat effective bias fit [4,16],30 golden evaluations to observed X history, first observed frame initial state. N2-offline uses c0. N2-noclosure optional.

Fast library:4096 Y states, each from independent random full initial state, spinup50 LT_ref; save final Y. Measured sigma_X/sigma_Y from these independent attractor states, not test outcomes. Condition a sampled library Y by integrating fast equations alone for the .5-time history with linearly interpolated noisy member X. Same Y per member/action. Library index uniform. Statecheck16 independently spun states. Twins16 independently spun states, perturb X by .02 sigma_X and condition fast states as specified; report median X normalized RMSE/ACC curves and first sampled crossings .9/.5; no interpolation. Sampler check uses these16 true histories,64 conditioned Y draws each; report pooled RMS draw SD divided by pooled RMS error of conditional mean subgrid term, and pooled Pearson correlation with realized subgrid term; also state-wise ratios/correlations. Undefined denominators remain unavailable. Two-scale truth waits for Todd go on this report.

CNN2-roll: same paired-set rule and matching36-step state loss, initialized CNN2-20k,10000 updates, final checkpoint.
CNN2-R2: CNN-R2 recipe initialized CNN2-20k, same two-scale paired set, two-scale validation fixed M64, cap includes actual base training GPU time.
CNN2-cost: same cost architecture/loss/batching as CNN-cost,16384 starts, conditioned Y for each member last X, paired across eight actions; two-scale fixed validation selection. Label/output windows use LT_ref.

## Budgets and cut rules

GPU-hours mean charged wall time while the worker owns a training GPU, including validation inference/checkpoint selection attributable to that run; no CPU duration is converted to GPU hours. Timestamp and synchronize CUDA at charge boundaries. Maximum aggregate Stage2=40, Stage2b=20. Training uses Baccus available memory; inference uses sulaco GPU. Reserve measured recent update/validation duration to avoid crossing a ceiling.

| Stage2 model | Individual allocation (GPU h) |
|---|---|
| CNN-5k | 1 |
| CNN-80k | 5 |
| CNN-20k-s2, s3 | 2 each |
| CNN-roll, resp | 5 each |
| CNN-R2 | 10 (WO missing-record fallback) |
| CNN-cost | 10 (WO missing-record fallback) |

Stage2b: base3h; roll2h; R2 **7h including actual base time**, leaving at most7−base hours for fine-tuning/selection; cost8h. Total maximum17h under these reservations, remaining3h reserved for mandatory validation/selection. Never enlarge any individual fallback beyond10h. Measurements, not allocations, determine actual cost. If counts/caps/deadlines conflict, apply WO §10 cut order and report immediately; never silently shorten mandatory update counts or truth panels. If mandatory work cannot fit after allowed cuts, report the unmet requirement rather than invent a completed model.

Cut sequence: secondary amplitude; N-win; leads4/6; CNN-5k; N-mis; N2-noclosure; hidden-state sensitivity; base repeats; CNN-80k; CNN2-roll. All never-cut items in WO §10 remain mandatory. Stage2b unfinished at Oct8 cutoff is not run. Primary truth estimate will be computed from measured sulaco rate and measured LT/dt and compared with the WO's approximate96 single-core hours; no estimate is presented as measured duration.

## Selection, scoring, bounds and licensed sentences

L*: lowest fixed-validation all-case normalized regret among available S; then higher validation wACC, lower wRMSE, frozen order CNN-R2,roll,80k,20k,5k. L*2 order CNN2-R2,roll,20k. Selection function has no test inputs. Record completion time. Best fixed: most frequent confirmation-selection b at primary validation lead, lowest index tie. Candidate action argmins always lowest index. S/Rep contain only run arms; report cuts and unavailable metrics.

Every WO §6 metric, failed-case/drop exclusion rule, reliability rule, denominator rule and WO §§7.1–7.7 threshold and sentence condition is incorporated unchanged from WO_v5.2.md. Use covariance population normalization1/M, mean/spread decomposition exactly; all-case counterparts/exclusion counts accompany eligible metrics. CNN-cost has no state skill/response values. AAH descriptive cost-pair counterparts use historical all-case formulas alongside new eligible/all64 formulas, labelled.

Eligibility: select b from first1024 truth members; confirm paired differences on last1024 using mean−2.983*sampleSD/sqrt1024>0 against all seven competitors. Cross-check paired bootstrap20000 member resamples, quantile .01/7. Report agreement and eligible full-mean argmin disagreements. Case intervals B2000, paired case indices, all statistics/eligible mask recomputed from sampled case rows. One-sided percentile bounds use numpy.quantile(method="linear") at exact criterion levels. NaN/unavailable satisfies no criterion. KILL→PASS→otherwise precedence, sufficiency first. Stage1 uses S={CNN-20k}; no sentence licensed by Stage1.

Stage1 test200/validation100 independent truth cases,2048 members, no-action paired reference; N-last,oracle,CNN-20k M64/nulls all leads. Truth+physics+bootstrap CPU sulaco, CNN inference CUDA sulaco. Artifacts hash before their own test evaluation. Stage1 PASS/otherwise continues automatically; KILL stops and harvests. Stage2 models never touch test before Stage1 reading. Stage2b prep allowed meanwhile; truth remains awaiting sampler go.

## Existing artifacts

CNN-20k SHA256 3c67fc2cfc3a858613160cc81151c09ef45829f08bda67df00b9e78f35f5fe74.
Climatology SHA256 4513b34ab1ab674bb7c5bf295906e38334ce938ebcb729b6bfa9d97467c7499e.
Other retained source/training metadata hashes: NUMBERS §AFD_HASHES and step0_evidence.json. Copies in inputs are checked against original. New train/library/closure/checkpoint artifacts go into AFD_ARTIFACTS before their own test evaluations; none is treated as already produced by this freeze.

Figures greyscale with direct labels, markers/patterns. Standalone repository. No cloud; Qwen services unchanged.

