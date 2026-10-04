# AAH freeze — 2026-10-04

Frozen before calibration, test-panel data and learned-arm training on paper/aspen-2026-10-horizon. Governing protocol: Amendment 1 plus Todd's directly supplied Amendment 1a. Gate PASS reported to vault before execution. The MCP-served WO still returned the superseded 512 bound; exact authoritative A5 correction is recorded in AAH_GATE_AMENDMENT1A.md. Historical WO snapshot: AAH_AMENDMENT1.md. Step 0 is not rerun.

## Scope, ordering and outcomes

1. Implement/verify numerical and scoring harness without test data.
2. Measure Lorenz unperturbed Lyapunov exponent; reuse exact World D Re40 chaos result (lambda=0.16793280275789657, alpha=0.0773273136075609) with source hashes. Measure unperturbed spatial state RMS for observation noise (not the older Euclidean anomaly sigma_A).
3. Calibration: 40 Lorenz cases x512 members; 20 Kolmogorov cases x256 members. Four amplitudes ascending {0.01,0.02,0.05,0.1}; stop at first >=80% eligible at 20 LT; if none qualify, stop that system and report.
4. At selected delta, every candidate must have positive lower95% Lyapunov bound using the reused renormalized-twin estimator (64 starts, 500 time-unit unperturbed burn-in, 800 time-unit Lyapunov interval, 20 time-unit discarded transient). Stop that system on any failure.
5. Commit a calibration addendum recording measured LT/RMS/delta and chaos gates BEFORE test-panel generation or any learned training.
6. Test panels: Lorenz200, Kolmogorov30; true decision ensembles1024/512 respectively. Never silently reduce these counts.
7. Evaluate mandatory solver paired/unpaired/jitter arms, action-conditioned learned CNN/FNO, random/myopic nulls. Misidentified arm included if time permits.
8. Generate AAH NUMBERS using the existing checker infrastructure, results note, greyscale figures and session review.

Primary persistent timing, W=1 LT, M=64. Grid {0.25,0.5,0.75,1,1.5,2,2.5,3,4,5,6,8,10,12,16,20}; G is smallest grid value >=argument, unavailable beyond20. Sufficient means >=50% eligible. Sustained T_d, KILL/PASS/otherwise precedence follow A3 exactly.

M_95 is ONLY the smallest successful budget in {8,16,32,64,128,256}. Unsuccessful paired M_95 is censored and FAILS member criterion. Censored unpaired numerator is conservatively256. Criterion >=3. No extrapolation to512 or optimal arbitrary integer count.

Nominal truth eligibility: paired bootstrap2000, member resampling, one-sided quantile0.01/(K-1), all mean(C_j-C_b) lower bounds >0; b first argmin by action index. Commitment bootstrap1000 at six specified looks, quantile0.05/(6(K-1)); only empirical errors are reported, no coverage guarantee. Near-ties excluded/reported.

Removed: uncentered control variate (Amendment A6). Optional cuts chosen in stated order to fit stage-1 budget: latent emulator; W=2 sensitivity; impulsive timing. These choices are made before calibration/results. Retain full Kolmogorov panel30. Further cuts require recorded budget evidence and follow WO order. Mandatory arms never cut.

## States, observations and dynamics

Lorenz40, F8, float64 RK4 dt0.01, output0.05. Kolmogorov64² Re40, exact existing World D drag and IFRK4 dt0.01 float64, 2/3 dealiasing, output0.35. Re identifier P1x unchanged, observed11 frames. F fit [6,10],30 golden-section objective evaluations using observed11 frames.

Case starts are independently sampled initial states burned500 time units under unperturbed truth. Generate11 true historical frames ending at0. Observations iid Gaussian per point/frame with sd0.02*sigma, where sigma is measured spatial state RMS. Ensemble member adds a fresh observation-noise window to this observed window. Solvers receive last member frame; learned models receive all11 frames. Truth ensemble same sampler with true parameters, independent namespace. Actual trajectory true last historical state is used only for realized scores/forecast target. Projection to solver's dealiased subspace is existing integrator behavior.

Run1 action formulas unchanged; after curl conversion, normalize Kolmogorov VORTICITY forcing patterns to unit grid RMS; multiply by delta*RMS(-4cos4y)=delta*sqrt8. Lorenz forcing patterns unit RMS, multiplied by8delta. One fixed positive delta for comparisons. No post-result sign/phase selection.

Cost Lorenz energy0.5*mean(x²); Kolmogorov true total budget nu*mean(|grad omega|²)+alpha*mean(omega²). Include uniformly spaced outputs t in closed[T,T+W]. For single-time ACC snapshot, select nearest integrator step to T*LT, record actual time. No interpolation of horizon criteria/accuracy. Nonfinite state is numerical failure, not a near-tie.

Climatology at each action: true trajectory50 LT spin-up +500 LT sampled every output step. ACC at grid T from Niva64 ensemble mean and true realized controlled trajectory, anomalies subtract action climatology. Mean across all cases/actions. Zero truth anomaly norm: mark unavailable and report; forecast anomaly norm below1e-12 times truth norm: ACC0. T_f first ACC<0.2; no crossing censored and cannot PASS/KILL.

## Disjoint reproducible randomness

numpy SeedSequence from [namespace,system,substream,case,member,action], system0=Lorenz,1=Kolmogorov.
Namespace bases: calibration100000, test-truth200000, test-arm300000, learned-train400000, learned-val500000, climatology600000, jitter700000, lyapunov800000, observation900000.
Substream codes: initial0, observational1, member2, bootstrap3, action4, tangent5.
Panel cases use calibration namespace or separate observation namespace initial case draws; test-truth and test-arm member draws never overlap. Paired arms share test-arm member draws exactly; unpaired adds action index to seed. Jitter independent per action/integrator step, multiplicative iid Gaussian1e-12 in physical state, then solver projection. Truth-bootstrap independent from arm-bootstrap via namespace.

## Learned-arm implementation choices fixed before training

Kolmogorov FNO: L_range recipe width64,modes16,layers4, periodic coordinate channels, residual forecast; extend observation lift to11frames and one normalized action-field channel. Whole window required by A7 overrides old eight-frame input count. AdamW lr1e-3, wd1e-4, cosine schedule, grad clip1, batch32, one seed0,30000steps, four-step unroll loss from existing recipe. Data1024 trajectories25LT, action uniform K, signed fractional amplitude uniform[-2delta,2delta]. Validation64 separate trajectories,1LT rollout error, checkpoints every1000steps. If memory requires batch microbatches, effective batch32 preserved and reported.

Lorenz CNN:11state channels plus action channel; periodic conv1d layers:12->256->256->256->256->1 with kernels5,5,5,5,1, GELU and residual next-state output (about1M parameters). AdamW same lr/wd/schedule/clipping; batch128, four-step unroll;20000steps, one seed0; data2048 trajectories25LT, validation64, checkpoint minimum1LT rollout error every1000steps.

Learned stability: any nonfinite or RMS>10unperturbed sigma unstable; drop member for all actions; >50% drop scores decision wrong. Report surviving sample counts and drop rates; response/forecast metrics for undefined cases unavailable rather than invented. No strongest-practice claim.

Normalized expected regret: (truth cost chosen-min)/(max-min); realized same on actual trajectory; zero denominator unavailable. Response fidelity: across action-pair differences correlation and RMS-relative error per case/horizon, report aggregation and undefined zero response. Partial correlations descriptive unit(arm,T), no inferential p-values.

## Machines and provenance

Baccus Kolmogorov solver development, nontruth arms and FNO training; sulaco192.168.88.228 Lorenz and brute-force truth/calibration ensembles. Key SSH confirmed. No Qwen services stopped; shared GPUs use available memory only. Sulaco task checkout under /home/todd/work/aspen-horizon-20261004, task-specific numpy/numba env; existing niva-datagen interpreter read-only for torch CPU truth ensembles if needed. Machine/interpreter/version/thread/batch/cost metadata retained.

Source attribution: candidate action selector blinded Codex run1 with recorded run2/Claude overlap; horizon/window/objective/arm selectors amended WO author (role attribution to Claude, history unverified); amended A5 Todd; implementation choices executing agent frozen before data. Test data and training remain prohibited until the post-calibration freeze addendum is committed.
