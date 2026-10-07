# Stage 18 freeze — learned controls and response derivatives

Post hoc on the original confirmation panel; licenses no frozen route. Report every run and weight. Training-run ranges are separate from instance-level betting uncertainty. The prescribed validation selection in C is the only selection among models. No posterior sampling, paper/abstract edits, or AFD modification is authorized.

Execution uses only Baccus 170HX GPUs, with at most four CPU threads per job. List compute-process holders immediately before each job. Todd's later authorization permits temporarily stopping that card's known vLLM user unit, with its initial state recorded and restored by the lease helper afterward. Refuse all other compute holders. No Spark is used. Per-case outputs and hashes are resumable; selected checkpoints and training recovery state are saved on schedule. Each run writes an atomic cumulative charge heartbeat after updates and normalization microbatches. Startup and resumed work remain charged; the unfinished interval across an interruption is conservatively charged as elapsed wall time against the cap. No unscheduled fallback checkpoint is eligible: if a cap or abort occurs before a finite scheduled validation checkpoint, report a failed arm and no evaluation. Persist initial paired-loss normalizers in recovery state and reuse them on resume. Checkpoints and selected files are atomic, and recovery state is written last. Scoring opens original confirmation outcomes only inside acd_stage18_score.score on Sulaco.

## A — retained CNN-F information interventions

Use the exact retained CNN-F checkpoint and unchanged acd_stage9_cnn.run. Evaluate each draw's own noise-free history under own forcing, the instance mean forcing, constant forcing eight, and a seeded within-instance forcing permutation deliberately breaking the joint posterior. Permutation seeds use SeedSequence [namespace_id, 2, case]. The own-forcing arm compares saved costs with original GB10 CNN-F costs, reporting maximum absolute difference and all confidence-classification changes. All arms use amplitude 0.16, nine options, all eight frozen leads and windows.

## B — explicit inferred context

E0 takes eleven normalized noise-free frames, four circular convolution layers of width 256 and kernel five with GELU, global site mean and a scalar linear head predicting (F−8)/2. E1 has one additional action/sigma channel. E0 uses the pre-action history. E1 draws offsets uniformly among zero through 36 from the concatenated eleven factual frames and 36 future action frames, with either saved action branch sampled uniformly; the action field accompanies every context, including pre-onset frames. Each estimator has five seeds, sharing the seed pair for its index.

Train only on the saved acd-train-F data identified below, using MSE against normalized forcing; AdamW learning rate 1e-3, weight decay 1e-4, cosine over 5000 updates, effective batch 128, gradient clip one, FP32 with TF32 disabled and deterministic cuDNN. Save checkpoints every 500 updates; select lowest trajectory-disjoint validation forcing MSE, earliest on ties. E1 validation uses one seeded, fixed branch/offset per validation trajectory, SeedSequence [batch_seed, 1]. E0 validation uses all pre-action histories. No confirmation or development input enters training or selection.

Each estimator output is transformed back to forcing units. CNN-F∘E0 estimates once at the cutoff and holds the value fixed; CNN-F∘E1 is evaluated both once/fixed and at every learned rollout step. At the cutoff E1 sees each option's action channel, matching its training interface. All pipelines use the retained CNN-F and unchanged Stage9 windows and cost accumulation. Report forcing RMSE/bias/correlation against each draw's forcing and full F5 readings. When Stage16 checkpoints are committed, additionally pair each E0 seed with the corresponding CNN-F seed. The alignment record cites the saved-data generator, trainer and inference code; it is descriptive.

## C — response training with history-only inputs

Generate new panel-disjoint data on Sulaco, never on Baccus, using namespace acd-train-resp. F is uniform on [6,10], initial states F plus independent standard normals, 50 LT spin-up, eleven noise-free factual frames. One pattern is sampled uniformly from the eight frozen patterns and its amplitude uniformly on [−0.32,0.32]. Each trajectory has that action branch and a no-action branch, with 36 future frames each. Counts match the train/validation counts below. Store generated data hashes before training; reference window costs use only validation trajectories.

CNN-noF architecture; base loss is four-step autoregressive normalized-state MSE plus first-step MSE on both branches. Add weight w times normalized paired state-effect MSE over all 36 future ticks. Weights are 0, 0.01, 0.03, 0.1, 0.3 and 1; the initial mean base/paired ratio is measured over the first 64 seeded normalization batches using SeedSequence [batch_seed, 3]. All weights share seed-one initialization and batch order. AdamW, schedule, batch, clip and precision match the frozen Stage9 recipe: 20000 updates, checkpoints every 1000, lowest 512-trajectory first-action 12-step validation rollout state MSE, earliest on ties. The Stage10b nonfinite guard skips any update with nonfinite microbatch loss or preclip gradient norm, counts skips toward schedule, logs component losses and paired maximum prediction, aborts after more than 20 total skips or three consecutive skips, and selects among saved checkpoints. Log base and paired losses every 100 updates. Failures do not halt other jobs.

Validation selection chooses the smallest-effect-RMSE weight among those with validation state MSE no more than 1.1 times weight zero; smallest weight on ties. Effect RMSE is evaluated over all eight patterns, amplitude 0.16, two-LT validation window, with no panel input. Evaluate weight zero and selected weight on all original confirmation draws using F5. If selected weight's pooled and equal-case confident intervention-sign errors at two LT are both below retained CNN-noF's respective values, train and report four further matched seeds of both selected and weight zero. The conditional extra-seed trigger uses only the specified original-panel comparison, not validation selection.

## D — actual learned rollout derivatives

Differentiate window energy with respect to amplitude at zero through actual autoregressive rollouts using torch.func.jvp, FP32 network states and float64 energy accumulation. Run CNN-20k, CNN-F with own forcing, retained CNN-noF, E0 seed-one pipeline, and the C-selected model. Compare with saved Stage9 physics G for identical draws/actions/leads. Report pooled per-draw sign agreement; normalized RMS error with physics pooled RMS as denominator; posterior three-class agreement and Cohen kappa at the frozen 0.95 confidence threshold; median absolute posterior mean divided by posterior SD; per-pair mean squared derivative error; posterior near-zero mass at gamma 0.05, 0.1, 0.2 and 0.5 times the Stage11 climatological tangent SD. No realized outcome is read for derivatives.

## Readings and sequence

At two and three LT report all specified state and draw-cost errors, S confident/error shares with case betting bounds and pooled error, calibration, fixed 1332-pair endpoint, E/C decisions, conditional-on-acting Clopper–Pearson bounds and action histograms. An invalid draw invalidates that entire case for that model; never condition on survivors. Publish A and B first, then D for available models, then C. The selected-C derivative necessarily follows C selection; append that D row after C. F21 is greyscale with marker distinctions and posterior reference lines.

R-other: the extra-seed trigger's unspecified confident-error aggregation is read conservatively: both pooled and equal-case errors must improve before spending additional GPU time; initial weight-zero and selected results are always reported. Estimator budgets were unspecified, so the implementation caps each run at the same 36000 GPU seconds as the retained emulator recipe; capped/incomplete runs are reported. C uses that same cap. The request's “uniform pattern” is read as uniformly sampling among the eight patterns, preserving the stated eight-pattern validation selection. New C arrays cannot have hashes before generation; their frozen recipe and generator hash are fixed here, and their generated manifest hashes must be recorded and pushed before C training. Estimator run indices are ordinal one through five; Stage16 stored indices are zero through four, with zero the retained Stage9 model. Pair E0 run one with retained CNN-F (stored index zero), run two with index one, run three with index two, run four with index three and run five with index four. Report all five pairs without selection; D's seed-one pipeline is E0 run one. The seed namespace and generated initialization/order seeds remain unchanged. No result is inferred from an unavailable arm.

## Computed identities

```json
{
  "namespace": "acd-stage18-seeds",
  "namespace_id": 1300663595214357452,
  "seeds": [
    {
      "index": 1,
      "torch_seed": 1973631741,
      "batch_seed": 3521043623
    },
    {
      "index": 2,
      "torch_seed": 2799994744,
      "batch_seed": 1378675625
    },
    {
      "index": 3,
      "torch_seed": 3320683030,
      "batch_seed": 2120846709
    },
    {
      "index": 4,
      "torch_seed": 4208116273,
      "batch_seed": 1552295955
    },
    {
      "index": 5,
      "torch_seed": 459775654,
      "batch_seed": 666108171
    }
  ],
  "code_hashes": {
    "acd_stage18_charge.py": "521a957dd49bf7ddf21b2827a4e9847a0e732c4ca8ee2b7f9b4a658a823d4a50",
    "acd_stage18_controller.py": "c869dbbc8393210a8b3a5e912a31e49f7fc29130930bec8d2942c12439817e6c",
    "acd_stage18_data.py": "8ac51783c4346c9d5e69944706999b2e88e4fb6837e4d22648373f3f44790438",
    "acd_stage18_derivative_readings.py": "88233dcee14c56eaf5b998060bea4b43c640e61aa248b520d0a11149e64b2c62",
    "acd_stage18_derivatives.py": "14171011c76c7e169c2b9c99ccb0e358ce803f8f2af2288ac1471ed6bc157861",
    "acd_stage18_estimators.py": "3e3d00143ecd874a3680378870683c0ccc875c3badbb098202b222de05eee4bc",
    "acd_stage18_freeze.py": "b690e52a61070347fb3c19253fa2e9bd3f3f1481ddad25e406a1b827c0ab092f",
    "acd_stage18_gpu_lease.py": "2cf41aa25d77c947f2e886d3e7303c51d526eeec8ce92696172ed6dbba456507",
    "acd_stage18_inference.py": "a6ea2847438a23a3290fa12c91535423413f31e8f3b3bd578d93735fa4a0fcb7",
    "acd_stage18_response_train.py": "9173c05d651d3339492d02147dec4d9b6f007f306b58bbbb7d8994abf18d88df",
    "acd_stage18_score.py": "14b2e75612b0527973a13ff1d8cb051782660d321d935c607c431fa8f8a364df",
    "acd_stage18_select.py": "e0e68bd34ec978a862e448a69595b99a10491ae1b2fc3ebf992b362717be9aa4",
    "acd_stage9_cnn.py": "3ca018b1dc35c5cb9734787e852240e7517d88007515692d27fd882f3c13d434",
    "acd_stage9_train.py": "9c36418c45ab0727d2c4294b96bed1102b85d65d269636f6c9b38e3573605269",
    "acd_stage9_cnn_metrics.py": "471e2363945e25a1f8ee0920c3955bc1a3c41d899de5a164b4369e2299fe859d",
    "acd_stage9_receipts.py": "966a21bc72ef4b3c8ede354a1246fb5d01c4b3df440ef19902ec032a688b456c",
    "acd_stage6_analysis.py": "c9fa8c1f9e211f8e7ea47ec63947bff3693258c738c377ce7874b425bba58cd8",
    "acd_stage13_analysis.py": "ffe50e4894aa97eb6de690abc996c1a8589ec8be926af0100f077b2220be289b",
    "acd_protocol.py": "160eabe8ccee07d0de17576a441b6fef1a93e1d5dbb68f2df9eb118a1eaad000",
    "acd_stats.py": "1c97d51262a7546b70320c1207de554eff6f9b6a58b00428a2640f5ead6f685a",
    "acd_stage19_part2_gate.py": "518e5890d5ac88f210a47a304ae9fd7cb47986ff444b3d078dc13ffc76b1a001"
  },
  "training_data_sha256": {
    "train.npz": "0eb4b167907fde9809da788ba41d9845fa7e60314c7e48efd5f3095ce3c62eb8",
    "val.npz": "6e46c7754b18c487e8e0c59f5138f9cef0cba8bfabdb441e84f5cf43943a47e3"
  },
  "trajectory_counts": {
    "train": 4096,
    "val": 512
  },
  "retained_checkpoints": {
    "CNN-F": "f883730e8df0798c07effbb1d51b05a646bea6f688b2a4bc74b9edf4ca104e8b",
    "CNN-noF": "4bfef787a80269dada0acd7ca74ef84eb6442a580c706a57333c55dc647b1f67",
    "CNN-20k": "3c67fc2cfc3a858613160cc81151c09ef45829f08bda67df00b9e78f35f5fe74"
  },
  "parameter_counts": {
    "E0": 998401,
    "E1": 999681,
    "CNN-noF": 999681,
    "CNN-F": 1000961
  },
  "response_namespace": "acd-train-resp",
  "estimator_updates": 5000,
  "matched_estimator_stage16_indices": [
    {
      "estimator_run": 1,
      "CNN_F_stored_index": 0
    },
    {
      "estimator_run": 2,
      "CNN_F_stored_index": 1
    },
    {
      "estimator_run": 3,
      "CNN_F_stored_index": 2
    },
    {
      "estimator_run": 4,
      "CNN_F_stored_index": 3
    },
    {
      "estimator_run": 5,
      "CNN_F_stored_index": 4
    }
  ],
  "estimator_checkpoint_spacing": 500,
  "response_updates": 20000,
  "response_checkpoint_spacing": 1000,
  "per_run_gpu_seconds_cap": 36000,
  "response_weights": [
    0.0,
    0.01,
    0.03,
    0.1,
    0.3,
    1.0
  ],
  "extra_seed_trigger": "both pooled and equal-case confident S errors at 2 LT below retained CNN-noF",
  "post_hoc": true,
  "licenses_frozen_route": false
}
```
