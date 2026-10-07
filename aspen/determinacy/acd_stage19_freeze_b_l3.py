"""Render the L3 addendum from a read-only timing inventory and code hashes."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def generate():
    inventory = json.loads((ROOT / 'receipts/acd_stage19_l3_timing_inventory.json').read_text())
    if inventory['new_seed_fresh_evaluations']:
        raise RuntimeError('Fresh-panel new-seed evaluation exists; addendum withheld')
    original = json.loads((ROOT / 'receipts/acd_stage19_freeze_b.json').read_text())
    paths = ['acd_stage19_freeze_b_l3.py', 'acd_stage19_l3_statistic.py',
             'acd_stage19_inference.py', 'acd_stage9_cnn.py', 'acd_stage9_train.py',
             'acd_stage19_learned.py', 'acd_stage6_analysis.py',
             'acd_stage13_analysis.py', 'acd_stage9_receipts.py', 'acd_stats.py',
             'acd_protocol.py', 'acd_stage19_part2_gate.py']
    hashes = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in paths}
    for p in ['acd_stage19_inference.py', 'acd_stage9_cnn.py', 'acd_stats.py']:
        assert hashes[p] == original['code_hashes'][p], p
    text = '''# Stage 19 Freeze B addendum — training-seed replication

Freeze B's original L3 pooled-error count remains descriptive and unchanged. This addendum adds confirmatory fresh-panel readings using only the four new matched seed pairs. The retained pair, stored index zero, was already tested by L1 and does not enter either new criterion. This stage licenses no frozen route.

## Step 0 — timing inventory

The inventory was completed before this document was written. Confirmation-panel inference already has partial new-seed outputs, disclosed below. No completed confirmation evaluation or new-seed score was found. No new-seed fresh-panel evaluation was found. Todd will judge whether the disclosed confirmation-panel timing preserves the freeze status. Under Step 0's continuation rule, absence of fresh-panel new-seed evaluations permits this addendum to proceed.

| Selected new run | Host | Selected step | Confirmation case files written | Status |
|---|---|---:|---:|---|
'''
    for run in inventory['selected_new_runs']:
        evaluation = next(e for e in inventory['new_seed_evaluations'] if e['run'] == run['run'])
        text += f"| {run['run']} | {run['host']} | {run['selected_step']} | {evaluation['written_case_count']} | partial inference; not scored or reported |\n"
    text += '''
Every other new Stage16 run has no selected checkpoint in this snapshot. Retained index-zero CNN-F and CNN-noF have selected checkpoints and were evaluated on both panels. The inventory records checkpoint hashes and every partial case-file path. Fresh inference directories contain only the retained models. No realized arrays were opened for the inventory.

## L3a — primary

Pair CNN-F seed i with CNN-noF seed i for stored indices i = 1, 2, 3, 4, using every run committed by Stage16 under its frozen recipe. For each pair and each fresh instance, compute the L1 difference exactly: seven zero-mean patterns at 2 LT; CNN-noF's share of confident answers wrong minus CNN-F's share. Each model uses its own confident-answer denominator. An instance-pair contributes only if both models give at least one confident answer. Preserve the invalid-draw rule and the Stage9 F5 inference construction.

Within each instance, average those differences over the new pairs for which they are defined. An instance contributes if at least one pair defines the difference. In ascending instance order, apply acd_stats.difference_interval at alpha = 0.01 to the instance means. This is the two-sided 99% v2.3 betting interval with the instance as unit. L3a is confirmed only if the interval lies wholly above zero. An empty or offset interval licenses no confirmation.

## L3b — required

The per-pair L1 point estimate must be positive in at least three of the four new pairs. L3 is confirmed only if both L3a and L3b hold. Stored index zero enters neither criterion. Never select a subset of seeds.

## Failed and missing runs

If any of the eight new runs fails under Stage16's frozen recipe, including a cap, an abort or no eligible checkpoint, L3a and L3b are not evaluable. A saved checkpoint from such a run does not restore confirmatory evaluability. Report every available pair descriptively without substitution. Pending runs remain pending. A pair with no contributing instances has no positive point estimate.

## Descriptive readings

For every stored index 0–4, report the L1 statistic with its two-sided 99% interval; pooled and case-averaged confident intervention-sign error with the existing v2.3 bounds for both models, retaining all-eight and seven-pattern fields; CNN-noF C(delta=0) harms among actions taken at 3 LT with its exact one-sided 95% Clopper–Pearson lower bound; whether its E and C(delta=0) policies each choose uniform decrease in every instance; and state anomaly correlation at 2 and 3 LT. Preserve the original strict-positive harm definition and report exact zero-effect ties separately. Report Freeze B's original pooled-error count across all five pairs descriptively. Keep seed variation separate from case-level uncertainty.

## Execution gate and code provenance

After this execution-gate amendment is committed and pushed, new-seed fresh-panel inference may begin for each Stage16 run as soon as that run's selected checkpoint is committed. Use only available resources without preempting Stage16 or Stage18 jobs. Resolve each selected checkpoint hash from its committed Stage16 receipt; pair by stored seed index. Use the Stage19 Part2 inference and Stage9 F5 scientific paths unchanged by the hashes below. Separate per-seed output directories must carry their checkpoint provenance, and completed per-case outputs must be written and hashed before scoring reads them. Any additional executable checkpoint/name adapter must be hashed and pushed before execution. Do not alter Stage16 or Stage18 training, checkpoints or queues.

The current learned scorer includes the already committed additive audit diagnostics from commit 4613502: per-case L1 numerator/denominator records and exact zero-effect tie counts. Its L1 computation is unchanged. Its current hash is recorded here; the inference and betting implementation hashes match Freeze B.

No realized outcome may be opened and no L3 reading may be scored until all eight new runs are committed and their fresh-panel inference is complete. Only then do realized outcomes enter inside Stage19 scoring code from the existing fresh-panel scoring cache. After that gate is satisfied, write receipts/acd_stage19_L3.json and the L3 section of ACD_STAGE19_READING.md. Register every reported number, retain every prior registry value, and push fast-forward. This addendum does not launch inference or scoring and does not edit the paper or abstract.

## Execution-gate amendment record

Todd authorized this amendment after the original addendum was pushed. It replaces the all-runs-before-inference gate with a per-run committed-selected-checkpoint gate, while retaining the all-runs-committed and all-inference-complete gate before any realized outcome is opened or any L3 reading is scored. Every seed uses the unchanged Stage19 Part2 inference path, separate per-seed outputs and per-case hashes. Stage16 and Stage18 jobs must not be preempted. L3a, L3b, every criterion, the failed-run rule and the original descriptive L3 count remain unchanged. The original Step0 inventory remains the historical snapshot; this amendment does not revise it.

## Inventory and hashes

Inventory:

```json
'''
    text += json.dumps(inventory, indent=2) + '\n```\n\nCode hashes:\n\n```json\n'
    text += json.dumps(hashes, indent=2) + '\n```\n'
    (ROOT / 'ACD_STAGE19_FREEZE_B_L3.md').write_text(text)


if __name__ == '__main__':
    generate()
