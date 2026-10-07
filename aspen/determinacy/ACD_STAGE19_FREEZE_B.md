# Stage 19 Freeze B — fresh-panel mechanism and learned readings

This freeze supplements Freeze A's C1–C4. The original confirmation-panel analyses were post hoc; the following fresh-panel readings are fixed before any emulator reads the fresh draws and before any realized outcome is computed. This stage licenses no frozen route. Report every specified reading and every model, without selection among results.

Except where explicitly descriptive or otherwise specified, each confirmatory reading uses the v2.3 betting construction at the 1% level, with the instance as unit. Preserve the reference-panel code's definitions, ordering, censoring, invalid-draw rules and omission of instances with no contributing answers. Report the number contributing to each reading. Keep case-level uncertainty separate from training-seed variation.

## Mechanism

- M1: at 2 LT, for patterns 1–7, the median over retained case–action pairs of the mean-flow contribution to within-pair Var(D) must be at least 0.90. Compute the variance terms using the Stage 9 B1 code path in acd_stage9_receipts.py, including residuals and covariance terms. This is the specified median criterion; no additional inferential bound or test is invented. Report 1 and 3 LT descriptively.
- M2: classify G and D(0.16)/0.16 by their posterior sign probabilities using the unchanged Stage 9 B2 / Stage 17A three-class definition (confident negative, non-confident, confident positive). Average the eight action agreement indicators within each retained instance at 2 LT. Apply acd_stats.one_sided with alpha=0.01 for a lower bound; the criterion is a lower bound at least 0.75. Other leads, Cohen's kappa and pooled per-draw sign agreement are descriptive.
- M3, descriptive: at every lead, report median z_D divided by median z_F, using the existing absolute posterior mean divided by posterior standard deviation definitions. The expected pattern is a ratio above 1 at lead 0 and below 1 at 2 LT. Report the observed pattern without adding a confirmatory test.

## Learned models and construction

Use the retained CNN-F, retained CNN-noF and CNN-20k checkpoint hashes recorded below. Inference follows acd_stage9_cnn.run: each draw's own noise-free eleven-frame history reconstructed from its sampled first-frame state and forcing; each draw's own forcing channel for CNN-F only; amplitude 0.16, nine options, all eight leads and the frozen windows. Use every draw retained by the Part 1 gates, including full-draw rescored cases. Do not substitute the old panel's draw count or fixed eligibility cohort for fresh-panel quantities.

Inference outputs are resumable per case. Validate completed files on restart and hash each new output before scoring reads it. Do not condition on finite survivors. A model with any invalid draw or option takes no action under E and C for that instance; confidence readings use the existing invalid-case rule. Record every invalid case. Use only a Baccus 170HX with no compute process, checking and recording process holders immediately before each job. Todd subsequently authorized temporarily stopping the Baccus vLLM services and restoring them after GPU work. The Stage 19 GPU lease helper records the original service state, stops only the service for the GPU being used, refuses any other compute-process holder, and restores the service afterward. Training is not authorized in this part.

- L1, primary learned reading: at 2 LT, on patterns 1–7, include each retained instance for which both CNN-F and CNN-noF provide at least one confident intervention-sign answer. Within each model and instance, compute the fraction of its confident answers that are wrong. Form d_c as the CNN-noF fraction minus the CNN-F fraction. Use acd_stats.difference_interval at alpha=0.01 on the ordered instance-level differences. Confirmed only if the two-sided 99% interval lies wholly above zero.
- L2: for CNN-noF's C(delta=0) policy at 3 LT, report harmful actions among actions taken and the exact one-sided 95% Clopper–Pearson lower bound. Confirmed only if that lower bound exceeds 0.05. Use the existing Stage 9 decision rule and strict harm definition; also record exact ties with no action separately. Cases with no action do not enter the conditional denominator.
- L3, descriptive: after Stage 16 selects and commits its checkpoints under its frozen recipe, evaluate every seed identically. Include the retained seed and four new seeds for each model. For each matched seed index, report whether CNN-noF's pooled confident intervention-sign error at 2 LT exceeds CNN-F's, and report the count across all five pairs. Pending checkpoints remain pending, rather than treating missing runs as failures or selecting a subset.

For every model report descriptively at 2 and 3 LT: state ACC and RMSE/sigma, per-draw J_8 and D errors against the same draw's physics, confident shares, pooled and equal-case confident-answer errors and their existing bounds, the mean-calibration test, the fresh-panel paired endpoint, E and C decisions, harms conditional on acting with exact bounds, action counts and histograms, and whether CNN-noF chooses uniform decrease in every retained instance. Preserve the original Stage 9 metric definitions through Stage 19 adapters and record adapter hashes before launch. Place every fresh-panel reading beside its original confirmation-panel value with its population and bound type.

## Deferred comparisons and access

The known-forcing comparison, linearized-variance check and Stage 18 repairs require a separate Part 3 freeze after their original confirmation-panel results report. Do not score the Part 1 known-forcing arm or run Stage 18 repairs on the fresh draws in Part 2. Continue to preserve the independently frozen known-forcing sampling contract.

Realized outcomes are computed and opened only inside Stage 19 scoring code on Baccus CPU after this freeze is committed and pushed. The recovery order permits posterior reference scoring independently of emulator inference. Learned-model scoring reads emulator outputs only after those outputs are hashed. No scoring occurs in this freeze generator or in inference. No paper or abstract is edited. Only Stage 19 paths are committed.

## Provenance

The known-forcing arm excluded 1 instance after its frozen retry gates. Its readings remain deferred to Part 3.

```json
{
  "part1_commit": "d90618973b0e40412a7ec8bd3c22e4b0afb86c41",
  "part1_receipt_sha256": "3126cdc7dd54cbca7322d098fa8eaf64cd15fa9f79eee75d924c90567e3befe0",
  "code_hashes": {
    "acd_stats.py": "1c97d51262a7546b70320c1207de554eff6f9b6a58b00428a2640f5ead6f685a",
    "acd_stage6_analysis.py": "c9fa8c1f9e211f8e7ea47ec63947bff3693258c738c377ce7874b425bba58cd8",
    "acd_stage9_receipts.py": "966a21bc72ef4b3c8ede354a1246fb5d01c4b3df440ef19902ec032a688b456c",
    "acd_stage9_forward_readings.py": "dafabb9c61a7bc5a8fec30344b524b3a5161b68fb8e67ce5cbe938d99190c969",
    "acd_stage17.py": "354fff3254b441ba8c271c8d426525d7302d6f7b7e98d682bf37a6aa2733a4ae",
    "acd_stage9_cnn.py": "3ca018b1dc35c5cb9734787e852240e7517d88007515692d27fd882f3c13d434",
    "acd_stage9_cnn_metrics.py": "471e2363945e25a1f8ee0920c3955bc1a3c41d899de5a164b4369e2299fe859d",
    "acd_stage13_analysis.py": "ffe50e4894aa97eb6de690abc996c1a8589ec8be926af0100f077b2220be289b",
    "acd_stage19_part2_gate.py": "518e5890d5ac88f210a47a304ae9fd7cb47986ff444b3d078dc13ffc76b1a001",
    "acd_stage19_gpu_lease.py": "5e09e6e6284bfb35df35a9431400caf2936973f3819657f80659360f3f4fcadc",
    "acd_stage19_freeze_b.py": "2d915292ce7ec3776544f6505122b1d5af84282488d7da901e7daa3280808666",
    "acd_stage19_inference.py": "591f6ce4989b19be4bbda36e6ffa39ecf34940bc513a1770e361b00ee1a7ef6d",
    "acd_stage19_score.py": "87e0bc98e9352fdc532f842ac2b5f2eb335eb9f8ba8d613045bcc428cef73ecd",
    "acd_stage19_learned.py": "63492818dd11bb5a4e294c515aaa462d9b1559fd32ee436fb69783f19e7dec26"
  },
  "checkpoints": {
    "CNN-F": "f883730e8df0798c07effbb1d51b05a646bea6f688b2a4bc74b9edf4ca104e8b",
    "CNN-noF": "4bfef787a80269dada0acd7ca74ef84eb6442a580c706a57333c55dc647b1f67",
    "CNN-20k": "3c67fc2cfc3a858613160cc81151c09ef45829f08bda67df00b9e78f35f5fe74"
  },
  "CNN_noF_provenance_sha256": "0b146f7c70bc1adff83db48c99eb32408915d8b8b62099ed5c86c068a33243e6",
  "known_forcing_excluded_cases": [
    8
  ],
  "known_forcing_excluded_count": 1,
  "known_forcing_readings": "Deferred to Part 3; this exclusion does not remove a main-posterior case",
  "realized_outcome_accesses": [],
  "emulator_runs_before_freeze": []
}
```
