"""Freeze D inventory and hashed contract; no draw or outcome arrays are read."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
OUT = ROOT/'runs/stage19'


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def tasks():
    rows = []
    checkpoint = ROOT/'runs/stage18/checkpoints/CNN-F.pt'
    for kind, rolling in [('E0', False), ('E1', False), ('E1', True)]:
        for j in range(1, 6):
            name = f'CNN-F-{kind}-{"rolling" if rolling else "fixed"}-seed{j}'
            rows.append(dict(name=name, first_panel_name=name, kind=kind, rolling=rolling,
                             seed=j, checkpoint=str(checkpoint.relative_to(ROOT)),
                             estimator=f'runs/stage18/training/{kind}-seed{j}/selected.pt'))
    for arm in ['meanF', 'constantF', 'permutedF']:
        rows.append(dict(name=f'CNN-F-{arm}', first_panel_name=f'CNN-F-{arm}', arm=arm,
                         checkpoint=str(checkpoint.relative_to(ROOT)), estimator=None))
    # Estimator j is paired with stored CNN-F index j-1. Index zero is P0(1).
    for i in range(1, 5):
        receipt = ROOT/f'receipts/acd_stage16_run_CNN-F-seed{i}.json'
        if not receipt.exists():
            continue
        rel = str(receipt.relative_to(REPO))
        committed = subprocess.check_output(['git', 'show', f'HEAD:{rel}'], cwd=REPO)
        if committed != receipt.read_bytes():
            raise RuntimeError('Stage16 receipt is not committed')
        rows.append(dict(name=f'CNN-F-E0-matched-seed{i+1}', first_panel_name=None,
                         kind='E0', rolling=False, seed=i+1, stored_index=i,
                         checkpoint=f'runs/stage19/L3_checkpoints/CNN-F-seed{i}/selected.pt',
                         estimator=f'runs/stage18/training/E0-seed{i+1}/selected.pt'))
    return rows


def inventory():
    names = {r['name'] for r in tasks()}
    names.update(f'{kind}-seed{j}' for kind in ['E0', 'E1'] for j in range(1, 6))
    names.add('CNN-F-ownF')
    found = []
    for base in [OUT/'inference', OUT/'part3b', OUT/'A_inputs']:
        if not base.exists():
            continue
        for p in base.rglob('*'):
            if p.is_file() and (base.name != 'inference' or any(n in p.parts for n in names)):
                found.append(str(p.relative_to(ROOT)))
    for p in (ROOT/'receipts').glob('*stage19*'):
        if 'part3b' in p.name and 'freeze' not in p.name:
            found.append(str(p.relative_to(ROOT)))
    return dict(utc=datetime.now(timezone.utc).isoformat(),
                stage18_models_run_on_fresh_draws=[], fresh_outputs_or_scores=sorted(found),
                fresh_inference_names=sorted(p.name for p in (OUT/'inference').iterdir()),
                realized_arrays_opened=False)


def ready():
    record = json.loads((OUT/'freeze_d_pushed.json').read_text())
    contract = json.loads((ROOT/'receipts/acd_stage19_freeze_d.json').read_text())
    if digest(ROOT/'ACD_STAGE19_FREEZE_D.md') != record['sha256']:
        raise RuntimeError('Freeze D changed')
    subprocess.run(['git', 'merge-base', '--is-ancestor', record['commit'],
                    'refs/remotes/origin/paper/aspen-2026-10-determinacy'], cwd=REPO, check=True)
    for name, expected in contract['code_hashes'].items():
        if digest(ROOT/name) != expected:
            raise RuntimeError('Freeze D code changed: '+name)
    return contract


def freeze():
    snapshot = inventory()
    if snapshot['fresh_outputs_or_scores']:
        raise RuntimeError('Stage18 fresh outputs already exist: '+str(snapshot))
    rows = tasks()
    for row in rows:
        row['checkpoint_sha256'] = digest(ROOT/row['checkpoint'])
        row['estimator_sha256'] = digest(ROOT/row['estimator']) if row['estimator'] else None
        if row['estimator']:
            complete = ROOT/Path(row['estimator']).parent/'complete.json'
            if row['estimator_sha256'] != json.loads(complete.read_text())['selected_sha256']:
                raise RuntimeError('Estimator differs from selected checkpoint')
    code = ['acd_stage19_part3b_contract.py', 'acd_stage19_part3b_inference.py',
            'acd_stage19_part3b_score.py', 'acd_stage19_part3b_report.py',
            'acd_stage18_inference.py', 'acd_stage18_estimators.py', 'acd_stage9_cnn.py',
            'acd_stage9_train.py', 'acd_stage19_inference.py', 'acd_stage19_learned.py',
            'acd_stage19_l3_statistic.py', 'acd_stage19_score.py', 'acd_stage13_analysis.py',
            'acd_stage6_analysis.py', 'acd_stage9_receipts.py', 'acd_stats.py', 'acd_protocol.py',
            'acd_stage19_gpu_lease.py', 'acd_stage19_part2_gate.py']
    result = dict(inventory=snapshot, tasks=rows, code_hashes={p:digest(ROOT/p) for p in code},
                  references={name:json.loads((ROOT/'receipts/acd_stage19_freeze_b.json').read_text())['checkpoints'][name]
                              for name in ['CNN-F','CNN-noF']},
                  first_panel_receipt_hashes={p.name:digest(p) for p in
                    [ROOT/'receipts/acd_stage18_A.json', ROOT/'receipts/acd_stage18_B.json']},
                  criteria=dict(B1_alpha=.01, B1_direction='lower > 0', B2_alpha=.05,
                                B2_upper_strictly_below=.05, B2_harm='realized D > 0',
                                B3_alpha=.05, B3_direction='one-sided lower > 0'),
                  inference_order=['E0 fixed', 'E1 fixed and rolling', 'A diagnostics', 'matched E0/CNN-F seeds'],
                  no_preemption=True, fresh_panel=True, licenses_frozen_route=False)
    (ROOT/'receipts/acd_stage19_freeze_d.json').write_text(json.dumps(result, indent=2)+'\n')
    text = '''# Stage 19 Freeze D — inferred-context repair

This freeze is written after Stage18 A/B were pushed and before any Stage18 diagnostic arm, estimator or pipeline runs on the fresh panel. It licenses no frozen route. Stage18 D/C are outside its scope and require a later Part3c freeze.

## Timing inventory

The inventory below was obtained before writing this document. No Stage18 arm, E0/E1 estimator, fixed pipeline or rolling pipeline has run on any fresh draw; no fresh output or score exists for them. The retained CNN-F and CNN-noF Part2 outputs and L3 seed inference are existing references, not new repair outputs. No realized array was opened for inventory.

## Pipelines and unchanged paths

P0(j) uses the retained CNN-F, stored index zero, with E0 seed j estimating forcing once from each draw's own noise-free eleven-frame pre-action history at the cutoff; that estimate remains fixed. P1f(j) uses E1 once and held fixed; P1r(j) re-estimates E1 from the current rolling window at every learned step. Every estimator seed is reported. All pipelines use amplitude 0.16, nine options, eight leads and the frozen windows. The Stage18 B rollout functions execute unchanged: acd_stage18_inference.run, acd_stage18_estimators.Estimator and acd_stage9_cnn.run. Only input/output destinations and the checkpoint/name allowlist are adapted to Stage19; no Stage18 file is modified. Existing Stage19 noise-free histories are reused by hash. Stage19 Part2 CNN-F and CNN-noF outputs remain unchanged by hash.

B1, primary: for each E0 seed and fresh instance at 2 LT, take CNN-noF seven-pattern confident wrong share minus P0's. Use exactly L1's own-confident-denominator rule, implemented by acd_stage19_l3_statistic.pair_statistic. Both models must give at least one confident answer for that instance-pair. Average over defined seed differences within each instance; keep an instance if any seed defines it. In ascending instance order, acd_stats.difference_interval(alpha=0.01) gives the two-sided 99% v2.3 betting interval. Confirm only if the lower endpoint exceeds zero; empty or offset intervals cannot confirm.

B2: for every E0 seed, at 3 LT the P0 C(delta=0) policy's exact one-sided 95% Clopper–Pearson upper bound on strictly positive harm among acted instances must be below 0.05. The policy uses unchanged acd_stage13_analysis.choices and decision_rows. Harm means realized D strictly greater than zero, as in L2; exact zero-effect ties are reported separately. acd_stats.cp_bounds supplies the one-sided limits. All seeds must satisfy the criterion.

B3: at 3 LT, within each E1 seed and instance take P1r seven-pattern confident wrong share minus P1f, using the same contributing rule. Average defined seeds within instances. Map each difference to (d+1)/2 and apply acd_stats.one_sided(alpha=0.05, direction=1), then map back by 2*lower-1. Confirm only if this one-sided 95% lower bound exceeds zero. This uses the same v2.3 instance betting construction, without a two-tail allocation.

An invalid draw invalidates its instance for that pipeline; never condition on surviving draws. Such an instance gives no confident answer and E/C takes no action. Failed or unavailable seed pipelines make the affected confirmatory reading not evaluable, with all available seeds still reported descriptively; never select or substitute a seed.

## Descriptive readings

For every pipeline/seed at 2 and 3 LT report forcing-estimate RMSE, bias and correlation against each draw's forcing; state anomaly correlation and RMSE/sigma; pooled and equal-case per-draw J8/Jk/Dk errors against that same draw's physics; confidence shares; pooled and case-averaged confident errors and v2.3 bounds; mean calibration; own-fresh-cohort paired endpoint; E and C(delta=0) regret, capture, actions, strictly positive harms, exact conditional-harm bounds, ties and action histograms; and whether uniform decrease is chosen in every instance. Reuse acd_stage19_learned.model_inputs and metrics, preserving their scientific functions by hash. The forcing-estimate reading is at the cutoff, draw/action pooled, as in Stage18 B; rolling-estimator trajectory errors are not inferred from the cutoff record.

Also report P0 minus retained CNN-F under B1's construction, with a two-sided 99% interval, descriptively. No equivalence claim is made: near this panel size the construction cannot provide a narrow equivalence interval even when all differences vanish.

Repeat the Stage18 A posterior-mean forcing, constant forcing eight and seeded within-instance permutation diagnostics using unchanged Stage18 seeds and preparation path. Permutation deliberately breaks the joint posterior. Pair E0 seed j with CNN-F stored index j-1 for every committed Stage16 CNN-F checkpoint, as in Stage18's freeze; report these pairings descriptively. First-panel readings use only committed Stage18 receipts; a first-panel pairing not yet reported is shown as pending, never fabricated.

## Execution and scoring gate

After this freeze is committed and pushed, Baccus 170HX inference queues behind all L3 seed inference and any active Stage16/18 jobs. No job is preempted. P0 seeds run first, then P1f/P1r, then A diagnostics, followed by matched-seed descriptive pipelines. Jobs resume per case; outputs and manifests are written atomically and hashed before scoring. Temporary Baccus vLLM leases follow Todd's existing stop-and-restore authorization. No realized outcome is opened during inference. Scoring runs only in Stage19 scoring code on Baccus CPU from the existing realized cache, with at most four threads. It does not create new realized outcomes. Store Part3b receipt and append the reading; retain every prior registry value and push fast-forward.

## Inventory, checkpoints and code hashes

```json
'''
    (ROOT/'ACD_STAGE19_FREEZE_D.md').write_text(text+json.dumps(result, indent=2)+'\n```\n')


if __name__ == '__main__':
    freeze()
