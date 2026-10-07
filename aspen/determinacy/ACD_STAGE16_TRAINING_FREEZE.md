# Stage16 training-seed replication freeze

Post hoc on confirmation; licenses no frozen route. Every seed is reported; no selection among seeds. Starts only after Stage10b results and this freeze have been committed and pushed. Stage15 work is untouched.

Seed derivation: SHA256 UTF-8 namespace interpreted as little-endian uint32 entropy; SeedSequence.spawn; each child generate_state(2, uint32), Torch first, batch second. Namespace: acd-stage16-seeds.

| Run | Torch initialization seed | Batch-order seed |
|---|---:|---:|
| CNN-F-seed1 | 3882383094 | 3967431003 |
| CNN-noF-seed1 | 3882383094 | 3967431003 |
| CNN-F-seed2 | 3708113526 | 2573923054 |
| CNN-noF-seed2 | 3708113526 | 2573923054 |
| CNN-F-seed3 | 4071409045 | 2861947773 |
| CNN-noF-seed3 | 4071409045 | 2861947773 |
| CNN-F-seed4 | 2253596644 | 411620442 |
| CNN-noF-seed4 | 2253596644 | 411620442 |

## Fixed recipe

{
  "training_trajectories": 4096,
  "validation_trajectories": 512,
  "updates": 20000,
  "effective_batch": 128,
  "microbatch": 128,
  "learning_rate": 0.001,
  "weight_decay": 0.0001,
  "gradient_clip": 1,
  "checkpoint_every": 1000,
  "validation_steps": 12,
  "cap_seconds": 36000,
  "optimizer": "AdamW",
  "schedule": "cosine",
  "dtype": "FP32",
  "TF32": false,
  "deterministic_cudnn": true,
  "loss": "four-step autoregressive normalized-state MSE plus first-step MSE",
  "guard": "skip nonfinite microbatch loss or total preclip gradient norm; count skipped schedule steps; abort above twenty total skips or three consecutive; report every run",
  "checkpoint_rule": "lowest validation rollout MSE across all saved validation trajectories and all twelve steps; earliest on ties",
  "parameter_counts": {
    "CNN-F": 1000961,
    "CNN-noF": 999681
  }
}

Same saved acd-train-F training and validation data; SHA-256s:
{
  "train.npz": "0eb4b167907fde9809da788ba41d9845fa7e60314c7e48efd5f3095ce3c62eb8",
  "val.npz": "6e46c7754b18c487e8e0c59f5138f9cef0cba8bfabdb441e84f5cf43943a47e3"
}

The retained Stage9 CNN-F and Stage10b CNN-noF are the baseline runs. Training-run variation is reported separately from case-level betting bounds. A failure does not stop the alternating queue. Offline pytorch:26.07 on both authorized local Spark GB10 hosts; seeds one and two on 192.168.88.4, seeds three and four on 192.168.88.12; network disabled; training container sees trainer read-only, training/validation data read-only, and its own output directory writable. No panel input or outcome is mounted for training.

## Evaluation

unchanged Stage9 F5 inference; all saved confirmation draws, own noise-free histories, own F only for CNN-F, amplitude 0.16, nine options, eight leads; sulaco-only outcome scoring; fixed posterior eligible cohort; E and C delta zero; Stage15 A matched coverage added after its committed ranking definition; training and evaluation do not wait for it; no selection among seeds

Coverage contract:
{
  "status": "deferred until Stage15A ranking definition is committed",
  "training_dependency": false
}

## Code hashes

| Path | SHA-256 |
|---|---|
| acd_stage16_freeze.py | fb03d466d600fc08058b7016f7da28e19feed64a2ea80cf6af18805f870b7dfe |
| acd_stage16_train.py | cf35add3b06ce8323b82f290cb2da55efa1c08a17159e179945dfeaad7ca650f |
| acd_stage16_queue.py | 30edf32097addb68cac67e78ac6f890f2ea15009f38ddbe65b1897b0711f598b |
| acd_stage16_metrics.py | 7b86814a7e4dc3b0bf8892f8e319c8b9bff1608ff4bb24363ad563937307b7c6 |
| acd_stage16_render.py | 6727e198916846204a8f88086c64ef7991336af2b07e788f566f50e45a93c551 |
| acd_stage16_pipeline.py | 92484cc0e98f1ba9f88d0bea6f7a87d104dc7e280f27402395283f1c0da3be64 |
| acd_stage9_cnn.py | 3ca018b1dc35c5cb9734787e852240e7517d88007515692d27fd882f3c13d434 |
| acd_stage9_train.py | 9c36418c45ab0727d2c4294b96bed1102b85d65d269636f6c9b38e3573605269 |
| acd_stage10b_metrics.py | 92bf8b6dcb424d19d54dfe2b143131b6fd919d8e114bd39aa49af0865ea0eeda |
| acd_stage13_analysis.py | ffe50e4894aa97eb6de690abc996c1a8589ec8be926af0100f077b2220be289b |
| acd_stats.py | 1c97d51262a7546b70320c1207de554eff6f9b6a58b00428a2640f5ead6f685a |
| acd_protocol.py | 160eabe8ccee07d0de17576a441b6fef1a93e1d5dbb68f2df9eb118a1eaad000 |
