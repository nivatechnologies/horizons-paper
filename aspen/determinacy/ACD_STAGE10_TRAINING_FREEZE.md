# Stage 10 training freeze — effect-loss weight sweep

Todd's TRAIN GO, 2026-10-06. Branch paper/aspen-2026-10-determinacy, base eeed4b057703cfb4fe1523dc0e660971f2bd02fa. Post hoc on confirmation, licenses no frozen route. Report every model; no selection among sweep weights. No paper or abstract edits. No posterior, MAP or RML sampling, no cloud, no AFD close-out modifications; Qwen services untouched.

Train only CNN-F-resp-0.1 and CNN-F-resp-0.01. The architecture, interface, corrected Stage9 data, seed, batch order, normalization samples, optimizer, FP32 settings, schedule, validation and checkpoint rule are identical to CNN-F-resp. The sole objective change is multiplication of the normalized paired-difference term by 0.1 or 0.01.

Architecture: eleven normalized history frames plus action/sigma plus (F-8)/2, circular residual CNN, widths13,256,256,256,256,1; 1,000,961 parameters. Fresh Torch seed61006, batch RNG6100601, normalization RNG6100602. Same4096 training/512 validation trajectories in namespace acd-train-F, F uniform[6,10], 50reference-LT spin-up at own F, noise-free frames, same frozen patterns and shared amplitudes uniform[-.32,.32], randomly oriented unordered pairs. Reuse the exact saved Stage9 train/val files, not regenerated data.

Loss: four-step autoregressive normalized-state MSE plus first-step MSE, plus alpha*(normal_base/normal_difference)*36-tick paired-state-difference MSE. The two new alpha values are0.1 and0.01; retained Stage9 CNN-F-resp alpha1 and CNN-F alpha0 are reported alongside. Normalizers are those of the identical initial model on the first64 fixed batches of128 training starts. Exact normal_base0.35864407243207097, normal_difference0.05537332111271098; the trainer recomputes and asserts bitwise-identical Python float values before updates.

Training: AdamW lr.001, wd.0001, gradient norm clip1, cosine over20,000 updates, effective/microbatch128, FP32, TF32off, deterministic cuDNN. Checkpoints every1000updates; lowest512-trajectory validation12-step (nominal1LT) state-rollout MSE, earliest on ties, first paired branch. Separate36,000-second GPU wall-time caps, including initialization, normalization, validation and terminal diagnostics. Same120-second-plus-recent-update reserve. If capped, select among saved checkpoints by that rule and disclose unequal updates; no adjustment or cross-weight selection.

GPU: authorized local Spark192.168.88.4, spark-89d8, NVIDIA GB10 UUID GPU-5b6bcf9b-45f4-8957-87c8-95977c27ca05. Offline installed nvcr.io/nvidia/pytorch:26.07-py3 image sha256:15b8de8baabe68e46afc51e88f3ccad5042013bafe8f244ec082ce0bb06d47e3, Torch2.13.0a0+9186a08b2c.nv26.07. Containers network-disabled. Training mounts only standalone trainer/diagnostic code, saved training-only data read-only and the new model output directory. No development or confirmation inputs/outcomes or AFD records mounted.

Terminal loss balance: evaluate the final trained model, even if it differs from the selected checkpoint, on64 batches of128 starts from the saved training data, sampled with RNG6100602 exactly as for initial normalization. No gradients or updates. Report unweighted base and difference losses, coefficient alpha*normal_base/normal_difference, weighted difference loss, weighted_difference/base ratio and weighted_difference/(base+weighted_difference). For retained alpha1, read its end-of-training checkpoint020000 and measure the same probe by inference only; retain the original Stage9 receipt unchanged. These diagnostics never select a checkpoint.

Evaluation: unchanged Stage9 F5 code, after each within-model validation selection. All273,520 saved confirmation draws, own noise-free H0..10 and own F_s, a.16, nine options, same windows and eight leads. Spark inference only; sulaco CPU scoring exclusively opens realized outcomes. Report factual ensemble-mean window RMSE/sigma and anomaly correlation at2/3LT; pooled per-draw and equal-case J8/Jk/Dk errors; S/Fc confidence and observation confidence; case-averaged confident accuracy with v2.3 bounds; matched seven-pattern reliability/error-coverage and prescribed case-level betting calibration test; seven-pattern same-lead differences2/3LT; model-specific paired first-loss and original1332-pair fixed-cohort endpoint. Same invalid-case rules and smaller inference microbatches on OOM. CNN-F, resp1, resp0.1 and resp0.01 reported side by side, with posterior reference. Paper and abstract untouched.

Inherited R-other interpretations: all results post hoc and exploratory; no frozen-route or familywise license. Reliability Clopper–Pearson bars remain descriptive for clustered questions; calibration uses independent cases. Validation nominal1LT means12 output ticks. Difference normalization preserves the Stage9 recipe, not an assertion of exact AFD base-objective reuse. Fixed-cohort endpoint is additional descriptive reporting. No new resolution has fired at freeze.

Data SHA256:
- train.npz: 0eb4b167907fde9809da788ba41d9845fa7e60314c7e48efd5f3095ce3c62eb8
- val.npz: 6e46c7754b18c487e8e0c59f5138f9cef0cba8bfabdb441e84f5cf43943a47e3

Code SHA256:
- acd_stage10_train.py: d893bcd2749d5d2f08dc7e7dcd861b4e366331ced375b4edad6327ee382449f4
- acd_stage10_loss_balance.py: 90b6628509df76fec5e8174a184ed07531db6dc356140e58fdb7f276366ade7a
- acd_stage9_train.py: 9c36418c45ab0727d2c4294b96bed1102b85d65d269636f6c9b38e3573605269
- acd_stage9_cnn.py: 3ca018b1dc35c5cb9734787e852240e7517d88007515692d27fd882f3c13d434
- acd_stage9_cnn_metrics.py: 471e2363945e25a1f8ee0920c3955bc1a3c41d899de5a164b4369e2299fe859d
- acd_stage9_gpu_artifacts.py: 41d2aeb91793f0508aa4466800a5b8809664bd65acdf70bd60f0046d41707971
