"""Generate Freeze B only after the complete Part 1 hash receipt is pushed."""
import json
from acd_stage19_part2_gate import ROOT, OUT, digest, part1_ready

CONTRACT = '''# Stage 19 Freeze B — fresh-panel mechanism and learned readings

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

'''


def build():
    commit, receipt = part1_ready(verify_remote=False)
    stage9 = json.loads((ROOT / 'receipts/acd_stage9.json').read_text())
    nof_path = OUT / 'part2_provenance/CNN-noF.complete.json'
    nof = json.loads(nof_path.read_text())
    names = ['acd_stats.py', 'acd_stage6_analysis.py', 'acd_stage9_receipts.py',
             'acd_stage9_forward_readings.py', 'acd_stage17.py',
             'acd_stage9_cnn.py', 'acd_stage9_cnn_metrics.py',
             'acd_stage13_analysis.py', 'acd_stage19_part2_gate.py',
             'acd_stage19_gpu_lease.py',
             'acd_stage19_freeze_b.py']
    # Adapters must exist before freezing their exact code.
    names += ['acd_stage19_inference.py', 'acd_stage19_score.py', 'acd_stage19_learned.py']
    missing = [n for n in names if not (ROOT / n).is_file()]
    if missing:
        raise RuntimeError('Required implementation missing before Freeze B: ' + ', '.join(missing))
    provenance = dict(
        part1_commit=commit, part1_receipt_sha256=digest(ROOT / 'receipts/acd_stage19_part1.json'),
        code_hashes={n: digest(ROOT / n) for n in names},
        checkpoints={
            'CNN-F': stage9['F']['CNN-F']['selected_sha256'],
            'CNN-noF': nof['selected_sha256'],
            'CNN-20k': stage9['C']['CNN-20k']['execution']['checkpoint_sha256']},
        CNN_noF_provenance_sha256=digest(nof_path),
        known_forcing_excluded_cases=receipt['gates']['knownF']['excluded'],
        known_forcing_excluded_count=len(receipt['gates']['knownF']['excluded']),
        known_forcing_readings='Deferred to Part 3; this exclusion does not remove a main-posterior case',
        realized_outcome_accesses=receipt['realized_outcome_accesses'],
        emulator_runs_before_freeze=receipt['emulator_runs'])
    exclusion_note = ('The known-forcing arm excluded ' +
                      str(provenance['known_forcing_excluded_count']) +
                      ' instance after its frozen retry gates. Its readings remain deferred to Part 3.\n\n')
    (ROOT / 'ACD_STAGE19_FREEZE_B.md').write_text(CONTRACT + exclusion_note + '```json\n' +
                                                json.dumps(provenance, indent=2) + '\n```\n')
    (ROOT / 'receipts/acd_stage19_freeze_b.json').write_text(
        json.dumps(provenance, indent=2) + '\n')


if __name__ == '__main__':
    build()
