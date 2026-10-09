"""Generate Freeze G identities from pushed Stage18 records; document only."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
STAGE21=Path('/mnt/niva-array/work/aspen-determinacy-stage21-20261008/aspen/determinacy')
def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
def run():
    manifest=ROOT/'runs/stage18/response_data/manifest.json'
    generation=json.loads(manifest.read_text())
    pushed=json.loads((manifest.parent/'generation_pushed.json').read_text())
    assert digest(manifest)==pushed['manifest_sha256']
    for name,expected in generation['data_sha256'].items():assert digest(manifest.parent/name)==expected
    assert digest(manifest.parent/'validation_reference.npz')==generation['validation_reference_sha256']
    freeze=json.loads((ROOT/'receipts/acd_stage18_freeze.json').read_text())
    zero=ROOT/'runs/stage18/training/CNN-noF-response-0-seed1'
    meta=json.loads((zero/'complete.json').read_text());assert digest(zero/'selected.pt')==meta['selected_sha256']
    sources={n:digest(ROOT/n) for n in ['ACD_STAGE18_FREEZE.md','acd_stage18_response_train.py','acd_stage18_select.py','acd_stage18_response_controller.py','acd_stage18_charge.py','acd_stage18_gpu_lease.py','acd_stage18_inference.py','acd_stage18_score.py','acd_stats.py','acd_protocol.py','acd_stage19_l3_statistic.py','acd_stage19_part3b_score.py','acd_stage19_learned.py']}
    sources['Stage21/acd_stage21_score.py']=digest(STAGE21/'acd_stage21_score.py')
    sources['Stage21/acd_stage21_inference.py']=digest(STAGE21/'acd_stage21_inference.py')
    record=dict(stage='Stage23 Freeze G',document_only=True,training_started=False,criteria_unchanged_for_earlier_freezes=True,
        source_code_hashes=sources,freeze_generator_sha256=digest(Path(__file__)),
        generation_commit=pushed['commit'],generation_manifest_sha256=digest(manifest),data_sha256=generation['data_sha256'],validation_reference_sha256=generation['validation_reference_sha256'],
        seeds=freeze['seeds'],weight_zero=dict(model=meta['model'],checkpoint_path=str((zero/'selected.pt').relative_to(ROOT)),checkpoint_sha256=meta['selected_sha256'],selected_step=meta['selected_step'],validation_state_MSE=meta['validation_MSE']),
        Stage22_panel_hash='pending panel contract; append execution record before use, criteria unchanged',
        new_implementation_hashes='pending implementation; append and push exact code hashes before training, with recipe and criteria unchanged',
        timing_inventory='No Stage22 contract, reading, receipt, Freeze F or Stage23 run found in the local Aspen workspace inventory at preparation; no outcomes opened by this generator.')
    (ROOT/'receipts/acd_stage23_freeze.json').write_text(json.dumps(record,indent=2)+'\n')
    text='''# Stage 23 Freeze G — corrected history-only response training

This is a new freeze. It amends no earlier freeze, including Stage 18 and Freeze F. Freeze G is pushed now, before Stage 22 scoring opens any outcome. Preparation is document-only: no sampling, inference, training, derivative calculation or realized-outcome access. Stage 23 training may start only after Stage 22 is complete and published, from that branch head. Do not preempt any queued job.

Commit as Todd with no AI attribution. No cloud. AFD close-out, paper and abstract remain untouched. Every empirical number is read or computed from source records. Realized outcomes are generated or opened only inside the frozen scoring code. Compared model inference uses the Baccus 170HX path. Record process holders and GPU identity; use the existing serving lease authorization, restore initial serving state, and do not preempt other jobs. At most four CPU threads per training job.

## Rationale

Stage 18 C's validation table and saved training logs are the sources: receipts/acd_stage18_C_execution_reading.json and receipts/acd_stage18_C_training_logs.json. Its validation rule retained weight zero; every positive weight exceeded the state-error constraint, including the two guard-aborted runs evaluated at their last saved checkpoint. The prior normalizer balanced loss values rather than gradient norms. Paired gradients traversed a 36-tick autoregressive rollout while base gradients traversed four ticks, followed by a single global clip. Recorded nonfinite gradients appeared between ordinary hundred-update norm samples; the logs do not identify unrecorded intermediate norms. These are motivation for a new recipe, not a revision of the earlier result or a claim that the failure mechanism is proven.

## Recipe

Reuse the Stage 18 C history-only CNN-noF architecture, training and trajectory-disjoint validation files, normalized input interface, base loss, optimizer, schedule, effective batch, precision and validation/checkpoint rules. Generate no new data. The generation manifest and data hashes below must match the pushed manifest before every run. Seed-one initialization and batch order are exactly Stage 18 C's; the remaining seed pairs below are the corresponding frozen Stage 18 seed pairs if the conditional descriptive replication is triggered.

The architecture has eleven normalized factual frames and the action/sigma channel, no forcing channel, four circular convolution layers of width 256, kernel five and GELU, a residual output head, and the Stage 18 C parameter count. Base loss is four-step autoregressive normalized-state MSE plus first-step MSE on both branches. AdamW learning rate 1e-3, weight decay 1e-4, cosine over 20,000 scheduled updates, effective batch 128, FP32, TF32 off, deterministic cuDNN and global gradient clip one. Checkpoints every 1,000 updates, with recovery of optimizer, schedule, batch RNG, Torch RNG and cumulative GPU charge. Each run is capped at 36,000 GPU seconds, including startup and resumed work. Select the lowest finite first-action 12-step state-rollout MSE on all 512 validation trajectories, earliest on ties. A finite scheduled checkpoint remains eligible after a cap or guard abort; no unscheduled fallback checkpoint is eligible.

The paired loss is the same normalized-state paired-effect MSE (predicted action-minus-no-action state difference minus the true paired state difference) averaged over the same 36 future ticks, covering the two-LT validation window. Change only its backward graph: detach the entire rolling context after every four completed ticks, before the next segment. Forward states, targets, normalization and tick inclusion are unchanged. Gradients within each four-tick segment accumulate into the paired gradient over all segments and the full batch; no gradient crosses a segment boundary.

Accumulate base gradients g_b and paired gradients g_p separately over the full effective batch, with identical microbatch weighting. Compute their total Euclidean norms over all model parameters before combination. Replace the prior loss-value normalizer in the optimizer update with

g = g_b + w (||g_b|| / ||g_p||) g_p.

Thus the scaled paired gradient has norm w times the base gradient norm before combination and global clipping. The applied scale is w ||g_b|| / ||g_p||. Then apply the unchanged global clip at norm one and the unchanged optimizer step. This does not balance the norm of the sum when gradients align or oppose; report the post-combination preclip norm. No loss-value normalizer enters the update.

Train weights 0.01, 0.03, 0.1, 0.3 and 1, reporting every run. Weight zero is the existing Stage 18 C selected weight-zero model identified below; do not rerun it. Scaling the paired contribution to zero leaves its recipe unchanged.

Use the Stage 18 nonfinite guard: any nonfinite microbatch loss or gradient, any zero or nonfinite base or paired norm, any nonfinite applied scale or combined norm invalidates that update; discard gradients and skip opt.step. A skipped update counts toward the schedule. Abort after more than 20 total skips or three consecutive skips. Resume and charge within the same per-run cap. At every hundredth scheduled update and every skip log base loss, raw paired loss, ||g_b||, ||g_p||, applied scale and post-combination preclip norm, together with the existing skip reason, component microbatches and maximum absolute paired prediction. If a quantity cannot be reached after an earlier invalid component, record it as unavailable rather than inventing it.

## Validation selection and panel readings

Use Stage 18 C's validation selection rule unchanged: choose the smallest validation window-energy effect RMSE among weights whose selected-checkpoint validation state MSE is no more than 1.1 times weight zero's, smallest weight on ties. Effect RMSE uses all eight patterns, amplitude 0.16 and the two-LT validation window. Report every weight, including guard aborts at their eligible selected checkpoint, with the original-recipe validation state-MSE ratio and effect RMSE beside the corrected-recipe values. Training/checkpoint selection cannot use any panel input or outcome.

If selection retains weight zero, Stage 23 stops after validation. Publish validation readings and logs for every weight; run no panel inference. Otherwise evaluate only the selected seed-one model on the Stage 22 panel, with each draw's noise-free history, amplitude 0.16, nine options and all frozen leads/windows. Reuse that panel's hashed retained CNN-noF and E0-fixed inference comparators on the same Baccus 170HX path. An invalid draw invalidates its instance for that pipeline; never condition on survivors.

Q1, primary: retained CNN-noF confident-error share minus the selected model's confident-error share on the seven zero-mean patterns at two LT. Use the Freeze E contributing rule: each instance contributes only when both pipelines have at least one confident answer in that population; compute each pipeline's share of its confident answers wrong, then their difference within instance. The instance is the unit. Confirm only if the two-sided 99% v2.3 betting interval on the mean lies wholly above zero.

Q2: selected-model C(delta=0) strict-positive harms among actions taken at three LT. Use the existing E argmin and C gate, without searching among other gate-passing actions. Confirm only if the exact one-sided 95% Clopper–Pearson upper bound is below 0.05, as in B2. Record exact zero-effect ties separately. Every acted instance contributes to the conditional-on-acting denominator; instances with no action do not contribute. If there are no acted instances, report the existing Clopper–Pearson function’s convention and do not treat the criterion as passed.

Descriptive only: selected model minus E0-fixed confident-error share, paired against each of the five E0 seeds using the same contributing rule and averaged over defined seed differences within instance, on the same seven-pattern two-LT population with a two-sided 99% instance betting interval. Also report the selected model on the Part 3b fresh panel with the full Freeze E descriptive set; full-menu and restricted-menu E/C decisions; uniform-decrease action histograms; and Part D derivative readings on the original panel's draws. Report the full descriptive set pooled and by forcing where the panel has forcing strata: forcing-estimate error where applicable, state skill, draw-cost errors, confident shares/errors with bounds, calibration, same-lead differences, paired endpoint, decisions, conditional-harm bounds and action histograms. Restricted menus contain the seven zero-mean patterns plus no action; C gates only E's restricted choice, without searching other actions.

If Q1 confirms, train the four further frozen seed pairs below once each at the selected weight. Report those runs descriptively on the same panels. They enter no confirmatory reading and cannot replace seed one. No other selection among seeds is allowed.

## Execution gates and failure handling

Stage 22 panel hash is pending and must be appended to this freeze as an execution record once its panel contract exists, with criteria unchanged. Record the completed Stage 22 publication commit before Stage 23 training starts. No Stage 22 outcome is inspected to prepare this freeze.

New recipe-specific trainer, selector/inference adapter, thin scoring wrapper and launcher have not yet been implemented. Append their exact source hashes here and push them before any Stage 23 training. This execution identity addition may not change the recipe, populations, thresholds, bound types or criteria fixed above. Existing statistic functions listed below are frozen dependencies. If scoring requires new statistic code beyond a thin wrapper calling those existing functions, stop and report. Earlier scoring and inference files are not edited.

Launch each run as soon as an authorized 170HX card is free; do not wait for a complete wave or preempt queued work. Project total cost from the first 500 updates of the first run, compute the projection from the measured receipt, push an execution note and continue only within the cap. The projection does not change the schedule, cap, selection or criteria.

Fail loudly: any nonzero task return code or missing complete.json marks its phase FAILED and blocks downstream scoring and scientific-result publication for that phase. Commit each task's log next to its JSON record; report failures with log excerpts. Resume skips complete hashed outputs. Guard aborts explicitly represented in a valid completion record follow the frozen eligible-checkpoint rule; they are not silently called full training completion. Hash all inference outputs before scoring. Outcome opening and its access log occur only inside the frozen scoring path.

Publish ACD_STAGE23_READING.md and receipts/acd_stage23.json as soon as complete hashed outputs permit it. Register reported numbers, require registry PASS and preserve every prior value; push fast-forward, rebasing and repeating checks if needed. Append ACD_PIPELINE_STATUS.md after each push. Include both recipes' validation table, selected weight, loss figure in the Stage 18 C format with both gradient norms added, all skip records, GPU identity/seconds, selected steps, Q1/Q2 point/interval or bound/type/retained population/outcome when evaluated, every descriptive reading pooled and by forcing, and every failure. No interim Stage 22 scoring is authorized by this freeze.

## Computed identities

```json
'''
    text+=json.dumps(record,indent=2)+'\n```\n'
    (ROOT/'ACD_STAGE23_FREEZE_G.md').write_text(text)
    print(json.dumps(dict(freeze_sha256=digest(ROOT/'ACD_STAGE23_FREEZE_G.md'),receipt_sha256=digest(ROOT/'receipts/acd_stage23_freeze.json'),generator_sha256=digest(Path(__file__))),indent=2))
if __name__=='__main__':run()
