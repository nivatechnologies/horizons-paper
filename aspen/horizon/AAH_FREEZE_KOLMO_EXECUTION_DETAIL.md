# Kolmogorov test execution detail

Written before any Kolmogorov test-panel or learned training data. Requires the numeric calibration addendum and every-action chaos gate first. No panel, criterion, noise scale or action changes.

The test panel has 30 independent base starts, 500-time-unit burn-in and eleven frames separated by0.35. Observation streams use the frozen observation namespace, system1, sub0 for starts and sub1 for noise. P1x starts from the first projected noisy frame, fits the ten remaining frames with true drag and no actions, Re bounds25..70 and30 golden-section evaluations. The positive objective normalization does not change the optimum.

Identification uses the exact inherited P1x objective and bracket updates with explicit finite-input/objective guards. A nonfinite objective stops identification for that part; no arbitrary finite parameter, dropped case or substituted fit is returned. This correctness guard is fixed before test data. All finite-case outputs must match the inherited implementation.

Test ensemble member windows use SeedSequence[namespace,1,2,case,member,action]. Each member independently perturbs all eleven observed frames with physical noise0.02*sigma. Action0 denotes shared windows for paired/jitter/misidentified/learned; unpaired uses action k+1. Truth uses the separate truth namespace with the same rule and512 members. Test member addressing is explicit rather than the calibration's original whole-array stream; calibration remains unchanged.

Baccus generates observation panels, targets, all physics arms, climatologies and learned data/training/evaluation. Sulaco computes the truth ensemble with128 processes and the unchanged Torch IFRK4, one member's six paired actions per task. Immutable shards permit restart without redrawing. Solver objective coefficients are fixedRe40 and true drag for every arm, as in the output-alignment addendum.

Before test data, fix a two-GPU schedule: physics cases0..19 on BaccusGPU0; targets/climatology/learned data/train/evaluation onGPU1, then physics cases20..29 onGPU1. This overlaps independent work without sharing GPU memory between FNO training and physics. All30 cases retain their original global IDs, windows and member seeds. Device/time metadata are reported; no case or backend selected by scores.

Paired GPU costs are computed in successive cohorts8,8,16,32,64,128, preserving nested firstM readings. Each cohort evaluates all actions and all horizons; cumulative cohort time is measured through each budget, with later budgets retained for the M95 analysis. Mean forecasts combine only first64 members, weighted by cohort size. Numerical jitter is physical-space multiplicative independent Gaussian noise1e-12 each integrator step, using a case-specific frozen jitter namespace and recorded Torch version/device. Misidentified dynamics useRe44. Myopic uses the same first64 paired members over[0,1LT]. Random regret is an exact uniform average over the six choices.

Actual controlled truth is scoring-only. Learned forecast targets are true states at the same nearest0.35 tick; Niva targets retain nearest0.01 tick. Cost windows use closed uniform output ticks. No horizon interpolation or score-denominator regularization.
