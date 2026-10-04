# AEA freeze — Amendment 1b, pre-data

Authority: full work order through Amendment 1b, source snapshot WO_AMENDMENT1B_SOURCE.md; affected gate AEA_GATE_AMENDMENT1B.md. Branch paper/aspen-2026-10-evidence. GB10 Spark 192.168.88.4. Stage 1 is Kolmogorov only. Existing Step 0 files are immutable.

## Fixed scope and cuts

One GB10 stage-1 execution. Apply allowed cuts in order before data: omit 45° points, ensemble disagreement, then context identifiability I. Preserve all four final queries, centre, every 0°/90° point, L_range-3, FNO-θ, law and both nulls. Cut analyses are reported unavailable, not evidence against a baseline.

## Truth, coordinates and streams

- Reuse World D 64² pseudo-spectral IFRK4, 2/3 dealiasing, dt=.01, float64. Velocity body force A sin(4y)e_x, vorticity source -4A cos(4y). Mean velocity zero. Alpha centre is exactly .07733 from this WO, not the old calibration's extra digits.
- Centre (40,1,.07733); half-ranges (6,.1,.015466). u=(theta-centre)/half-range. Box [-1,1]³. Training conditions uniform independently in all three coordinates.
- Seeds in common.py: block bases 7,100,000 training; 7,200,000 validation; 7,300,000 sensitivity; 7,400,000 attractor; 7,500,000 test; 7,600,000 identification; 7,700,000 chaos; 7,800,000 noise; 7,900,000 bootstrap; 8,000,000 optimizer; 8,100,000 numerical QA. Substreams reserve offsets 0..99,999 in each block, use stable point index, and never depend on gate outcome or task scheduling. No identification randomness is needed for deterministic search; its block stays reserved.
- Initial-state generator is unchanged Kolmogorov.random_ic. Burn-in 500 time units at each trajectory's own theta. Sensitivity uses 64 independent centre-attractor states. Test uses 100 independent trajectories with observation-window endpoint 200 time units after burn-in; first of 11 frames at 196.5, then spacing .35. Noise stream is separate from initial conditions.
- Attractor statistics: 100 independent trajectories after 500 burn-in, flow the point's lead h first, then collect 10 samples per trajectory spaced 1.4, exactly 1,000 endpoint samples. Query sigma is sample standard deviation (ddof=1). Full-field sigma_A is sqrt(mean(||omega-mean_field||²)); harness white-noise SD per grid entry is .02 sigma_A/64. Training scaling and noise use the centre sigma_A; test noise uses point sigma_A.

## Sensitivity and gates

- Inherited chaos estimator: 64 starts, 500 burn-in, renormalized twins over 800 time units, tau=1, first20 discarded, perturbation1e-6 relative RMS. Point λ is mean across starts; 95% interval mean±1.96 SD/sqrt64. Gate lower bound must be strictly positive and trajectories finite. All three parameters are duplicated correctly for twin batches. No substitution of failed points.
- Centre chaos first. Fixed h_c=.5/λ_c. Paired +/- .1 in each u coordinate, same 64 centre initial states, both evaluate at h_c. Include the explicit parameter factors in the final queries when differentiating. Mean difference / .2 gives each g. |g|<1e-8 makes a query unusable.
- Directions, bisection, projection and realized D_g/D_perp exactly Amendment 1. Ray-angle labels and actual displacement are both retained. All generated 0°/90° points undergo the inherited chaos gate. Centre shared reference is computed once. Report g at each passing point with fixed local h and independent paired sensitivity states; this reported gradient never changes the directions.
- Commit numeric centre/sensitivity/test-point/chaos results as a freeze addendum before panel data and learned training. Chaos-failed points excluded; no alternate direction or amplitude. If fewer than three evaluable queries remain, outcome otherwise; report feasibility and retain mandatory arms on available points. A failed centre chaos gate blocks that system's dependent experiment.

## Queries and arm evaluation

Final four queries and formulas are recorded verbatim in CODEX_QUERIES.md. Error query time is exactly h=.5/λ(theta_test) after last observation. Solver takes whole .01 steps plus a final shorter IFRK4 step; learned outputs on .35 grid use linear interpolation between bracketing predicted fields (including last observation at time0). Apply scalar queries to the resulting state, not interpolated scalar values. No horizon rounding.

All arms are evaluated against the same physical functional q_theta_test: explicit Re, A, alpha factors in these dissipation/power diagnostics are evaluator constants shared across predictions and truth, and are not injected into L_range's field inputs or law identification. This measures state-forecast error for the named physical query at that test point. FNO-θ additionally receives true parameters in its input by design. Report this evaluation convention with the results.

Persistence holds the raw last observed frame; spectral spatial derivatives and zero-mean velocity follow the final formulas. For solver forecasts the noisy frame is projected through inherited to_spec. The centre null uses centre dynamics. Law predicts from the projected last frame with fitted theta. Identification uses all11 raw noisy frames; same P1x misfit, normalized by sigma_A², projected first frame, summed over the other10 frames. Coordinate golden section: Re then A then alpha, three sweeps, exactly30 objective evaluations per coordinate/sweep; midpoint final bracket; bounds [20,70], [.5,1.5], [.3*.07733,2*.07733]. No gradient or test-truth input.

## Learned recipes

- Same 1,024 training conditions and trajectories, 200 frames each after500 burn-in; validation128 conditions,100 frames, disjoint stream. Last8 frames for L_range; last4 plus normalized parameter channels u_Re,u_A,u_alpha for FNO-θ. Width64,16 modes in both ky half planes,4 layers,periodic coordinate channels,residual output,projection128. Only FNO-θ's parameter-channel count changes from1 to3. Input lift sizes follow inherited8/4 histories.
- Each learned arm:30,000 optimizer steps, batch32,4-step autoregressive loss (first-step MSE plus mean of4 MSEs), AdamW lr1e-3, weight decay1e-4, cosine decay to0,no warmup,clip1.0. Seed0 mapped to reserved optimizer block. No extra ensemble seeds after the prescribed cut.
- Validation512 fixed noisy windows every1,000 steps; minimum validation loss checkpoint. Parameters float32/complex64; truth float64. Validation noise and sampled windows use disjoint validation substreams. Training minibatches/noise use disjoint training/noise offsets. No early truncation, panel-based selection or reduced width to satisfy a budget.

## Statistics and readings

Point error mean over100 normalized absolute errors; state-resampling percentile95% intervals with B=2000 and bootstrap block. σ_q below1e-12*|meanq| excludes the query/point. Nonfinite or zero σ produces unavailable normalized errors under overarching unavailable rule; no epsilon. Losing0°/90° makes query non-evaluable. Ratio unavailable if either endpoint error exactly0. Unavailable ratios count toward neither clause. Constant-vector/nonfinite Spearman unavailable and satisfies no correlation clause.

Use evaluable queries×{0°,90°,centre}, excluding unavailable/gated-out query/points. No per-state correlation substitution. If fewer3 evaluable queries, otherwise. Else KILL before PASS. KILL if both learned arms each have >=3 symmetric ratios<=1.3, or both have |rho_g-rho_perp|<.15. PASS if one same learned arm has>=3 R>=2 and rho_g>=.6,rho_perp<=.3, and law>=3 R<=1.3. Otherwise Todd decides. Boundaries inclusive except strict .15.

Report Euclidean displacement and Mahalanobis-to-training-distribution distance (from centre, training sample covariance in u; not projected-distance covariance); ensemble and I cut. Partial correlation controlling λ*h=.5 is unavailable as a constant control, reported explicitly; it supplies no additional evidence. Greyscale figures with markers,line styles and direct labels. All numbers trace to AEA sections and source hashes with inherited NUMBERS table/checker extended; negative tamper check must fail.

CUDA graphs may cache blocks of the unchanged IFRK4 operations for speed; verify against eager inherited solver and a scalar-parameter reference before production. No altered time step, precision, Lyapunov horizon or reduced start count. Resumable phases retain config/source hashes and refuse overwrite of completed products. Runtime timestamps preserve Spark's clock; durations use monotonic timing.
