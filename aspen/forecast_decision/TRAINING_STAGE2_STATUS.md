# Stage 2 training worker status

Authoritative measured progress snapshots and source paths: `TRAINING_STAGE2_STATUS.json`. These are training and validation readings only. They license no outcome sentence.

CNN-roll and CNN-resp continue their existing exactly 10,000-update runs on Baccus GPU 0 and 1. CNN-cost and CNN-R2 were launched on GPU 2 with microbatch 8; the effective batch remains 128. The latter two use separate 10 GPU-hour fallback caps. Qwen services were left running.

Validation selection uses fixed 100-case, 64-member validation inputs on sulaco CUDA. `selection_worker.py` computes all-case normalized regret, paired member drops and worst regret for failed cases. Candidates tie by earliest update. The coordinator controller in `selection_manager.py` copies only model checkpoints and validation acknowledgements. It waits for baseline inference to finish and uses the shared `gpu.lock`. Every selector worker masks `/home` and `/mnt` through bubblewrap, exposing only selected source, fixed validation inputs and the current model checkpoint directory. The existing AppArmor chrome profile supplies user-namespace permission; no policy or sysctl was changed.

CNN2 support reads measured sigma from base_train.npz, initializes fine-tuning from CNN2-20k.pt, uses two-scale RNG namespaces, and subtracts the base model's actual charged GPU seconds from the CNN2-R2 seven-hour reservation. Before CNN2-R2 launch, place the base training_complete.json at training_data2/CNN2-20k.training.json. Two-scale validation selection still requires its own approved and generated validation panel.

Future launches snapshot source files and SHA256 hashes per model. Current workers were launched before that improvement. Charging now starts before CUDA model allocation for future launches; existing progress clocks exclude setup before their charging boundary. Preserve their launch/controller timestamps when reconciling conservative total budgets.

No test output, Stage 1 reading or old AAH test dataset was read by this training agent. Syntax checks passed for train.py, selection_worker.py and launch_training.sh.

`training_scheduler.py` waits for existing mandatory workers, then schedules CNN2-20k and the checkpoint-selected two-scale models, and queues optional Stage 2 base models after GPU 2 is free. Two-scale checkpoint-selected workers wait for fixed validation inputs before allocation. CNN2-roll is deferred pending measured feasibility; no cuts have been applied. Validation initialization charge is explicitly added to the first scheduled R2 acknowledgement.
