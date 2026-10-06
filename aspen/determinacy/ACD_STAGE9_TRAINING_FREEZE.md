# Stage 9 training freeze

Todd authorized two new forcing-conditioned emulators on 2026-10-06, and authorized the local Spark 192.168.88.4 as an alternative GPU host. Post hoc; licenses no frozen route. No paper or abstract edits.

Architecture: CNN-20k circular residual convolutional network, channel widths 13,256,256,256,256,1; first four convolutions width5 with GELU, final width1; residual adds last input frame. Inputs are eleven noise-free frames / sigma, action field / sigma and constant (F-8)/2. Parameters 1,000,961 versus CNN-20k 999,681; the sole increase is 1,280 weights for the extra input channel.

Data: new namespace acd-train-F, SHA256 UTF8 name first eight bytes little-endian namespace ID, SeedSequence [namespace ID, split role], roles train0 and validation1. 4,096 independent training trajectories and 512 independent validation trajectories; F uniformly [6,10], initial F plus independent standard normal coordinates, 50 LT spin-up at own F, dt .01 float64 RK4. Eleven factual frames spaced .05 precede action. Each trajectory has a uniform unordered pair of distinct frozen patterns; each unordered pair is randomly oriented, making both action branches marginally uniform over all eight patterns; one amplitude uniform [-.32,.32] shared by both actions. Store 36 future .05-spaced states for each action. All data noise-free. First action branch supplies the base loss and validation. No development or confirmation panel file is accessed by the data generator or training container.

CNN-F base loss: mean normalized-state MSE over four autoregressive steps plus first-step MSE. CNN-F-resp identical base recipe plus normalized paired-difference MSE, uniform over 36 predicted ticks, between rollouts from the same start under both actions. Like AFD response training, normalization uses the identical initial model and first64 batches of128 paired starts. Additional difference weight = initial mean base loss / initial mean paired-difference loss. No epsilon or panel-dependent adjustment.

Both models: fresh Torch seed61006, identical training batch RNG seed6100601 and normalization RNG seed6100602; effective batch128, microbatch128 (smaller on allocation failure), FP32 (TF32 off), AdamW lr1e-3 wd1e-4, gradient norm clip1, cosine over20,000 updates. No warm-start from any selected AFD checkpoint. Checkpoints every1,000 updates. Select lowest validation one-LT nominal state-rollout MSE over12 future .05-spaced ticks on all512 validation trajectories, first action; earliest checkpoint wins ties. Maximum charged wall GPU time36,000 seconds EACH, including initialization, normalization and validation. Reserve120 seconds plus recent worst update duration before starting an update. If capped, select saved checkpoint with lowest prescribed validation MSE, report completed updates and cap; no panel-dependent selection.

Training GPU: Spark NVIDIA GB10, host spark-89d8, 192.168.88.4, installed nvcr.io/nvidia/pytorch:26.07-py3 container, network disabled. Training mounts only the new training/validation data, standalone trainer and model output directory. No ACD panel or AFD close-out file is mounted. Qwen services are untouched.

Exact evaluation after checkpoint selection: a=.16, all273,520 saved confirmation draws with their own noise-free H0..10, own F channel, nine options including no action, same frozen windows and all eight leads. FP32 network, float64 energy accumulation, paired factual/action J and D. At2/3 LT compare per-draw costs against the same draw's saved physics costs, ensemble-mean factual state window RMSE/sigma and spatial anomaly correlation against truth inside scoring code. Confident-answer error is averaged within case, with v2.3 one-sided betting bounds. Seven-pattern matched reliability on same200 cases at2LT, modal-probability bins [.5,.6,.7,.8,.9,.95,.99,1] (right edge inclusive only last), pooled two-sided95% Clopper–Pearson intervals labelled descriptive because questions cluster by case. Calibration test: bounded case-mean (predicted modal probability minus correctness), two-sided99% v2.3 betting interval on that signed difference; reject perfect mean calibration only if interval excludes zero. Error-versus-coverage threshold grid .5,.55,.6,.65,.7,.75,.8,.85,.9,.95,.99; case betting accuracy accompanies confident errors. Confidence and observation-confidence use .95 and frozen modal-specific null probability. Same-lead seven-pattern S minus Fc uses case-level betting99% intervals at2/3LT; paired first-loss uses original per-model lead0 eligibility and tested-grid censoring. Invalid or exploded draw: do not condition on survivors; case answers non-confident and report excluded/invalid totals.

Resolution R-other: the new response-loss combination is specified as base loss plus initial-loss-normalized paired difference; it is not represented as an exact reuse of the AFD fine-tuning objective, whose base term was a36-tick rollout loss. Validation is a nominal one-LT12-step rollout (0.6 physical time), explicit grid approximation.

Code SHA256:
- acd_stage9_train.py: 545fdfea81d30ff7f32bbb6f460287419631c5eaab8093b97d7bd012f109d1b3
- acd_stage9_training_data.py: 4dfc519dc36d8ffe6bd97a38a401b4628ed175a02864ac904b95aa0dd8842364
- acd_stage9_cnn.py: 3ca018b1dc35c5cb9734787e852240e7517d88007515692d27fd882f3c13d434

## Pre-checkpoint corrective amendment

The first generator used sorted unordered pairs and therefore biased the first action branch. The initial CNN-F run was stopped before a scheduled checkpoint, discarded, and its full container GPU duration is charged against CNN-F’s36,000-second total. Regenerated data randomly orient each pair; both branches are marginally uniform over all eight patterns. No development or confirmation result was consulted. All prescribed training restarts from the frozen fresh seed on the corrected dataset. CNN-F-resp had not started. Microbatch128 uses the available GB10 capacity at the same effective batch128; both models use identical microbatch and batch ordering. R-other records this implementation correction; the discarded run licenses no finding.

Superseding code SHA256 (prior listed hashes are the discarded implementation):
- acd_stage9_training_data.py: 0d821e33f48847c2c8ec7737640718fd1d0720909fc182d148f9b41d6731a5c4
- acd_stage9_train.py: 9c36418c45ab0727d2c4294b96bed1102b85d65d269636f6c9b38e3573605269
- acd_stage9_cnn.py: 3ca018b1dc35c5cb9734787e852240e7517d88007515692d27fd882f3c13d434
- acd_stage9_cnn_metrics.py: 85afbef88254f8f7ad8180d216904cf7bdf28a6f5127b4cdec3e9d79e72b40c8

## Additional matched-cohort descriptive reading, before trained-model evaluation

Alongside the previously frozen model-specific lead0-eligible paired endpoint, also report the endpoint on the original posterior1332-pair cohort. This prevents a model-dependent eligibility change from silently altering a between-model comparison. Both are labelled post hoc and license no route; training and checkpoint selection remain unchanged. Superseding scoring code hash: 8b7d0509dbd521b021706a51a2afb34b44a0bc873394bb09ebf3dc21a0321f49.

Cost-error reporting also retains pooled per-draw bias, RMSE, MAE and signed-error quartiles alongside equal-case summaries. This changes no input, model, checkpoint selection or primary statistical procedure. Scoring code SHA256 before trained-model evaluation: 0c7f05db09899247f198b75b16efb09a5b911ec9228448870be70af498d256cf.
