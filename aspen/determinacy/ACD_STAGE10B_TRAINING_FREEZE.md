# Stage 10b training and evaluation freeze

Post hoc on confirmation; licenses no frozen route. All models are reported, without selecting among models or weights. Training and inference use the authorized local Spark NVIDIA GB10 and the existing offline pytorch:26.07 image; Docker network is disabled. Realized outcomes are opened only by scoring functions on sulaco CPU. Qwen services and AFD close-out files are untouched.

## Queue and control
Queue: CNN-noF, CNN-F-resp-0.01, CNN-F-resp-0.1. A model failure does not stop the queue.
CNN-noF uses the CNN-20k circular residual architecture: eleven normalized frames plus action/sigma, twelve inputs, no forcing channel. Its only architectural difference from CNN-F is the absent constant forcing channel. Four hidden circular convolutions of width 256 and kernel 5 with GELU, followed by a one-channel kernel-1 convolution; residual to the last frame. Its parameter count is computed from the architecture. Its difference from CNN-20k is the training data and recipe.
All three models use the identical saved acd-train-F noise-free train/validation trajectories, independent of every panel. Forcing is uniform on [6,10]; input normalizers, starts, targets and action sampling remain exactly those of Stage 9. Training inputs are only train.npz and val.npz. Torch seed 61006; batch RNG 6100601; frozen normalization and terminal-probe RNG 6100602.
AdamW learning rate 1e-3, weight decay 1e-4, FP32; cosine over 20000 scheduled updates; gradient clip 1; effective batch and microbatch 128. Base loss is four-step autoregressive normalized-state MSE plus first-step MSE. Sweep weights multiply the frozen normalized paired-difference loss by 0.01 or 0.1; all response normalizers must exactly reproduce the Stage 9 values. CNN-noF has base loss only; its paired component is logged as zero and no response normalization probe is used.
Validation uses the unchanged Stage 9 twelve-output-tick state-rollout MSE over the saved validation set. Checkpoints every 1000 scheduled updates; choose the lowest validation MSE, earliest on ties. No panel inputs or outcomes enter training, validation, normalization or checkpoint selection. Cap 36000 charged GPU seconds per model, including discarded attempts.
The discarded response-0.1 charge is 5847 seconds. See ACD_STAGE10_FAILURE.md for the accounting resolution. No checkpoint of that discarded run is evaluated.
## Nonfinite guard
For each microbatch, nonfinite loss discards all gradients for that update and skips optimizer step. After backward, compute the total gradient norm before clipping; a nonfinite norm also zeroes gradients and skips optimizer step. Every skip logs scheduled step, each computed microbatch’s base and paired losses, gradient norm (null if backward was not reached), and maximum absolute paired-rollout prediction. Uncomputed microbatches are not imputed. Nonfinite log scalars are represented as strings in valid JSON.
Each skipped update still advances the fixed cosine schedule. Abort a model after more than 20 total skipped updates or three consecutive skips, then select among its saved checkpoints by the same validation criterion. Report scheduled, completed and skipped updates separately. Every 100 scheduled steps, all models log base and paired components separately. Retained CNN-F and alpha-1 CNN-F-resp were trained without this guard. If a guarded model skips no updates, explicitly report that the guard changed no optimizer update.
## Evaluation
After training and checkpoint selection, use unchanged acd_stage9_cnn.py (Stage 9 F5): every saved confirmation draw, its own noise-free eleven-frame history and own forcing for conditioned models, action amplitude 0.16, nine options and all eight leads. CNN-noF follows the existing unconditioned CNN-20k path; no forcing channel is supplied. Smaller inference microbatches follow the existing memory fallback. No realized outcome is mounted on Spark.
Score on sulaco CPU using unchanged Stage 9 metrics and additional receipt-level three-LT matched reliability if required. Report posterior, CNN-20k, CNN-F, alpha-1 CNN-F-resp and all guarded models side by side: state skill, pooled and equal-case cost errors, confident and observation-confident shares, case-level betting accuracy/error bounds and descriptive pooled errors, seven-pattern reliability/coverage/calibration, same-lead comparisons, model-specific and fixed posterior-cohort paired endpoints. Bounds retain their own estimands; case-level bounds are not attached to pooled point errors.
Run the unchanged Stage 10 terminal training-only loss-balance probe on each sweep’s final model, independently of checkpoint selection; save/hash terminal.pt and selected.pt separately.
## Data hashes

| File | SHA-256 |
|---|---|
| train.npz | 0eb4b167907fde9809da788ba41d9845fa7e60314c7e48efd5f3095ce3c62eb8 |
| val.npz | 6e46c7754b18c487e8e0c59f5138f9cef0cba8bfabdb441e84f5cf43943a47e3 |

## Frozen code hashes

| Code | SHA-256 |
|---|---|
| acd_stage10b_train.py | b20c74a92f7c27960681e98a816a27c5500dfe36d6e3cafeb7401d87ee7d72d1 |
| acd_stage10b_queue.py | c2e4016b0b907c0848c6c0c19f0403f9fc3795bff2bd625740786bb1ba753700 |
| acd_stage10_loss_balance.py | 90b6628509df76fec5e8174a184ed07531db6dc356140e58fdb7f276366ade7a |
| acd_stage9_cnn.py | 3ca018b1dc35c5cb9734787e852240e7517d88007515692d27fd882f3c13d434 |
| acd_stage9_train.py | 9c36418c45ab0727d2c4294b96bed1102b85d65d269636f6c9b38e3573605269 |
| acd_stage9_cnn_metrics.py | 471e2363945e25a1f8ee0920c3955bc1a3c41d899de5a164b4369e2299fe859d |
| acd_stage9_receipts.py | 966a21bc72ef4b3c8ede354a1246fb5d01c4b3df440ef19902ec032a688b456c |
| acd_stage6_analysis.py | c9fa8c1f9e211f8e7ea47ec63947bff3693258c738c377ce7874b425bba58cd8 |
| acd_stats.py | 1c97d51262a7546b70320c1207de554eff6f9b6a58b00428a2640f5ead6f685a |
