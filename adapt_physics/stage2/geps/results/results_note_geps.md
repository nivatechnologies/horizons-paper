## GEPS as a learned adaptive opponent (script-generated: stage2/geps/geps_analysis.py @ f9cb469)

**Frozen reading:** NOT STATED: both reading components hold, but GEPS-range trained 35 of about 2,500 step-matched epochs (the WO's 8 h cap; a spec error), so the reading cannot answer its question.

**Caveat:** Every GEPS run trained unclipped: the released train.py:158 calls clip_grad_norm_ after optimizer.zero_grad() (train.py:157), so clipping never applies, and the wrapper copies that order. The published lr 1e-2 was not tested with working clipping, so this result cannot tell whether GEPS needs the lower lr (1e-3, used here) or only working clipping.

| Re | better budget | GEPS-range (epochs trained) | H | H - GEPS (95%) | holds |
|---|---|---|---|---|---|
| 50 | 500 | 0.20 (35 epochs; val change over last two checks +0.0081 (+3.46%)) | 3.24 | 3.04 [2.79, 3.31] | True |
| 56 | 500 | 0.15 (35 epochs; val change over last two checks +0.0081 (+3.46%)) | 3.12 | 2.97 [2.74, 3.19] | True |

First N = 50 states of the fresh World D panels, w = 11, eps 0.1, future frames; margin 0.25 with the 95% paired interval excluding 0 (crossed bootstrap over trajectories and H's seeds; GEPS one seed). Scope reduced by Todd's ruling (feasibility); see GEPS_GATE.md and geps_freeze.yaml.

| Re | arm | source | restricted mean (95%) | S(1) | S(3) | retention |
|---|---|---|---|---|---|---|
| 50 | GEPS_range_adapt500 | GEPS (this WO) | 0.20 [0.16, 0.24] | 0.00 | 0.00 | 0.06 |
| 50 | GEPS_range_adapt5000 | GEPS (this WO) | 0.20 [0.16, 0.24] | 0.00 | 0.00 | 0.06 |
| 50 | GEPS_range_noadapt | GEPS (this WO) | 0.19 [0.16, 0.22] | 0.00 | 0.00 | 0.06 |
| 50 | H | Part A (same states) | 3.24 [2.97, 3.52] | 1.00 | 0.42 | 0.99 |
| 50 | O | Part A (same states) | 3.28 [2.99, 3.60] | 1.00 | 0.44 | 1.00 |
| 50 | persistence | Part A (same states) | 0.11 [0.10, 0.12] | 0.00 | 0.00 | 0.03 |
| 50 | L0 | Part A (same states) | 0.53 [0.49, 0.57] | 0.00 | 0.00 | 0.16 |
| 50 | L_range | Part A (same states) | 1.74 [1.56, 1.94] | 0.87 | 0.07 | 0.53 |
| 50 | L_range_wide | Part A (same states) | 2.17 [1.95, 2.43] | 1.00 | 0.14 | 0.66 |
| 50 | FNO_Re_true | Part A (same states) | 2.21 [2.02, 2.45] | 0.97 | 0.15 | 0.68 |
| 50 | FNO_Re_id | Part A (same states) | 2.20 [2.01, 2.42] | 0.97 | 0.15 | 0.67 |
| 50 | L_ft | Part A (same states) | 0.76 [0.70, 0.83] | 0.14 | 0.00 | 0.23 |
| 56 | GEPS_range_adapt500 | GEPS (this WO) | 0.15 [0.13, 0.17] | 0.00 | 0.00 | 0.05 |
| 56 | GEPS_range_adapt5000 | GEPS (this WO) | 0.15 [0.13, 0.17] | 0.00 | 0.00 | 0.05 |
| 56 | H | Part A (same states) | 3.12 [2.88, 3.36] | 1.00 | 0.49 | 0.99 |
| 56 | O | Part A (same states) | 3.14 [2.90, 3.39] | 1.00 | 0.50 | 1.00 |
| 56 | persistence | Part A (same states) | 0.11 [0.10, 0.12] | 0.00 | 0.00 | 0.04 |
| 56 | L0 | Part A (same states) | 0.36 [0.34, 0.38] | 0.00 | 0.00 | 0.12 |
| 56 | L_range | Part A (same states) | 1.47 [1.31, 1.64] | 0.87 | 0.01 | 0.47 |
| 56 | L_range_wide | Part A (same states) | 1.93 [1.72, 2.18] | 1.00 | 0.10 | 0.61 |
| 56 | FNO_Re_true | Part A (same states) | 1.59 [1.47, 1.72] | 0.94 | 0.01 | 0.51 |
| 56 | FNO_Re_id | Part A (same states) | 1.61 [1.48, 1.73] | 0.95 | 0.01 | 0.51 |
| 56 | L_ft | Part A (same states) | 0.72 [0.67, 0.78] | 0.06 | 0.00 | 0.23 |

GEPS training (validation RelativeL2 on the 64 fixed windows; persistence = the no-change forecast on the same windows):

| run | lr | epochs | best val (epoch) | persistence | val curve (epoch:loss) | status |
|---|---|---|---|---|---|---|
| ARCHIVED_geps_range_s0_lr0.01_collapsed | 0.01 | 51 | 0.7266750 (50) | 0.7266750 | 0:0.7266754 50:0.7266750 | collapsed to persistence; val change over last two checks -0.0000 (-0.00%); evaluated: no (collapsed to persistence; archived, never evaluated) |
| geps_range_s0_lr0.001 | 0.001 | 35 | 0.2308721 (30) | 0.7266750 | 0:0.5644766 2:0.4354147 4:0.4316104 6:0.3483525 8:0.3495376 10:0.3225729 12:0.3084703 14:0.2874763 16:0.2953822 18:0.2635087 20:0.2680462 22:0.2648376 24:0.2621697 26:0.2441865 28:0.2554978 30:0.2308721 32:0.2349526 34:0.2430717 | trained; val change over last two checks +0.0081 (+3.46%); evaluated: yes |
| geps_range_wide_s0 | 0.01 | 1 |  (None) | 0.7796857 | 0:nan | diverged; evaluated: no (diverged) |
| geps_range_wide_s0_lr0.001 | 0.001 | 51 | 0.2857823 (50) | 0.7796857 | 0:0.6149940 50:0.2857823 | trained; val change over last two checks -0.3292 (-53.53%); evaluated: no (cut) |

| cost (batch 1, Spark GB10) | steps | n timed | wall median s | adapt median s | forecast median s |
|---|---|---|---|---|---|
| GEPS_range_adapt500 | 500 | 20 | 65.4 | 64.7 | 0.6 |
| GEPS_range_adapt5000 | 5000 | 3 | 648.0 | 647.4 | 0.6 |

Post-freeze follow-up, GEPS-range trained longer (seed 1 on Baccus; not a substitute for the frozen reading):

| Re | checkpoint (val) | budgets | GEPS 500 / 5,000 | H - GEPS (95%) | frozen H - GEPS (epochs) |
|---|---|---|---|---|---|
| 50 | seed 1, epoch 130 (0.1620) | 500 | 0.46 /  | 2.78 [2.58, 2.99] | 3.04 (35) |
| 56 | seed 1, epoch 130 (0.1620) | 500 | 0.29 /  | 2.83 [2.63, 3.03] | 2.97 (35) |
