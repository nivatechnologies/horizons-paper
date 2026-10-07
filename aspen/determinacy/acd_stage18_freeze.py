"""Compute Stage18 seeds, architecture/data/code identities and freeze text."""
import hashlib
import json
from pathlib import Path
import numpy as np
from acd_stage18_estimators import Estimator
from acd_stage9_cnn import Emulator, ForcingModel

ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    namespace = 'acd-stage18-seeds'
    identity = int.from_bytes(hashlib.sha256(namespace.encode()).digest()[:8], 'little')
    seeds = []
    for i, sequence in enumerate(np.random.SeedSequence(identity).spawn(5), 1):
        values = sequence.generate_state(2)
        seeds.append(dict(index=i, torch_seed=int(values[0]), batch_seed=int(values[1])))
    files = sorted(ROOT.glob('acd_stage18_*.py'))
    files += [ROOT/name for name in ['acd_stage9_cnn.py', 'acd_stage9_train.py', 'acd_stage9_cnn_metrics.py',
                                    'acd_stage9_receipts.py', 'acd_stage6_analysis.py', 'acd_stage13_analysis.py',
                                    'acd_protocol.py', 'acd_stats.py']]
    files.append(ROOT/'acd_stage19_part2_gate.py')
    data = ROOT/'runs/stage18/data'
    counts = {}
    for name in ['train', 'val']:
        with np.load(data/(name+'.npz')) as d:
            counts[name] = len(d['H'])
    checkpoint_dir = ROOT/'runs/stage19/checkpoints'
    record = dict(namespace=namespace, namespace_id=identity, seeds=seeds,
                  code_hashes={p.name: digest(p) for p in files},
                  training_data_sha256={name+'.npz': digest(data/(name+'.npz')) for name in counts},
                  trajectory_counts=counts, retained_checkpoints={name: digest(checkpoint_dir/(name+'.pt'))
                                                               for name in ['CNN-F', 'CNN-noF', 'CNN-20k']},
                  parameter_counts={name: sum(p.numel() for p in model.parameters())
                                    for name, model in [('E0', Estimator()), ('E1', Estimator(True)),
                                                        ('CNN-noF', Emulator()), ('CNN-F', ForcingModel())]},
                  response_namespace='acd-train-resp', estimator_updates=5000,
                  matched_estimator_stage16_indices=[dict(estimator_run=i, CNN_F_stored_index=i-1)
                                                     for i in range(1, 6)],
                  estimator_checkpoint_spacing=500, response_updates=20000,
                  response_checkpoint_spacing=1000, per_run_gpu_seconds_cap=36000,
                  response_weights=[0., .01, .03, .1, .3, 1.], extra_seed_trigger='both pooled and equal-case confident S errors at 2 LT below retained CNN-noF', post_hoc=True, licenses_frozen_route=False)
    (ROOT/'receipts/acd_stage18_freeze.json').write_text(json.dumps(record, indent=2)+'\n')
    text = '''# Stage 18 freeze — learned controls and response derivatives

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

'''
    text += '```json\n'+json.dumps(record, indent=2)+'\n```\n'
    (ROOT/'ACD_STAGE18_FREEZE.md').write_text(text)


if __name__ == '__main__':
    run()
