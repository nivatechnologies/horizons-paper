"""Stage18 C queue after pushed data and implementation addendum; no truth access."""
import json
import subprocess
import time
from pathlib import Path
from acd_stage18_controller import ROOT, OUT, GPU, batch
from acd_stage18_inference import guarded, digest

SULACO = '/home/todd/work/aspen-determinacy-stage18-20261007/aspen/determinacy'
CPU = '/home/todd/work/aspen-determinacy-20261005/.venv/bin/python'


def retry(args):
    while True:
        p = subprocess.run(list(map(str, args)))
        if p.returncode == 0:
            return
        if p.returncode != 255:
            raise RuntimeError(f'command failed: {p.returncode}: {args[0]}')
        time.sleep(60)


def name(weight, seed):
    return f'CNN-noF-response-{weight:g}-seed{seed}'


def training_task(weight, seed):
    model = name(weight, seed['index'])
    return model, [ROOT/'acd_stage18_response_train.py', '--name', model,
                   '--data', OUT/'response_data', '--out', OUT/'training'/model,
                   '--micro', '128', '--torch-seed', seed['torch_seed'],
                   '--batch-seed', seed['batch_seed'], '--response-weight', weight]


def infer_score(models):
    tasks = []
    for model in dict.fromkeys(models):
        checkpoint = OUT/'training'/model/'selected.pt'
        if not checkpoint.exists():
            continue
        tasks.append((model, [ROOT/'acd_stage18_inference.py', 'run', '--name', model,
                              '--data', OUT/'confirmation_inputs', '--checkpoint', checkpoint,
                              '--micro', '256']))
    outcomes = batch(tasks)
    completed = []
    for model, _ in tasks:
        source = OUT/'inference'/model
        if not (source/'complete.json').exists():
            continue
        retry(['rsync', '-a', str(source)+'/', f'sulaco:{SULACO}/runs/stage18/inference/{model}/'])
        command = (f'cd {SULACO} && env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=2 '
                   f'NUMBA_NUM_THREADS=2 {CPU} -u acd_stage18_score.py {model} '
                   f'> runs/stage18/score_{model}.log 2>&1')
        try:
            retry(['ssh', '-o', 'BatchMode=yes', 'sulaco', command])
        except RuntimeError as failure:
            (OUT/f'C_score_failure_{model}.json').write_text(json.dumps({'model': model, 'reason': str(failure)})+'\n')
            continue
        retry(['scp', f'sulaco:{SULACO}/receipts/acd_stage18_{model}.json',
               ROOT/'receipts'/f'acd_stage18_{model}.json'])
        completed.append(model)
    return completed, outcomes


def main():
    # The parent must push the controller/selector addendum before this script runs.
    addendum = json.loads((OUT/'C_implementation_pushed.json').read_text())
    for filename, sha in addendum['code_hashes'].items():
        if digest(ROOT/filename) != sha:
            raise RuntimeError('C implementation differs from pushed addendum: '+filename)
    freeze = guarded()
    json.loads((OUT/'response_data/generation_pushed.json').read_text())
    initial = freeze['seeds'][0]
    outcomes = batch([training_task(w, initial) for w in [0., .01, .03, .1, .3, 1.]])
    # Selection itself is GPU work and must use the same serving lease as training.
    selection = batch([('C-validation-selection', [ROOT/'acd_stage18_select.py',
                       '--data', OUT/'response_data', '--training', OUT/'training',
                       '--settings', OUT/'confirmation_inputs/settings.json', '--micro', '128'])])
    selection_path = OUT/'C_selection.json'
    result = (json.loads(selection_path.read_text()) if selection_path.exists()
              else {'selected': None, 'status': 'selection failed; no model selected'})
    chosen = result.get('selected')
    models = [name(0., initial['index'])]
    if chosen:
        models.append(chosen['model'])
    completed, inference = infer_score(models)
    trigger = False
    comparisons = {}
    if chosen and chosen['model'] in completed:
        fresh = json.loads((ROOT/'receipts'/f"acd_stage18_{chosen['model']}.json").read_text())
        previous = json.loads((ROOT/'receipts/acd_stage10b.json').read_text())['models']['CNN-noF']
        new = next(r['all_confident_accuracy'] for r in fresh['confidence_readings'] if r['lead'] == 2.)
        old = next(r['all_confident_accuracy'] for r in previous['confidence_readings'] if r['lead'] == 2.)
        comparisons = {key: {'selected_error': 1-new[key], 'retained_noF_error': 1-old[key]}
                       for key in ['answer_accuracy', 'case_accuracy']}
        trigger = all(new[key] > old[key] for key in comparisons)
    if trigger:
        weights = list(dict.fromkeys([0., chosen['weight']]))
        outcomes.update(batch([training_task(w, seed) for seed in freeze['seeds'][1:] for w in weights]))
        more, extra = infer_score([name(w, seed['index']) for seed in freeze['seeds'][1:] for w in weights])
        completed += more
        inference.update(extra)
    status = dict(training_outcomes=outcomes, selection_outcome=selection,
                  completed_models=completed, inference_outcomes=inference,
                  extra_seed_trigger=trigger, trigger_comparisons=comparisons,
                  rule='both pooled and case-averaged confident S error improve at 2 LT')
    (OUT/'C_reading_ready.json').write_text(json.dumps(status, indent=2)+'\n')
    print(json.dumps(status, indent=2), flush=True)


if __name__ == '__main__':
    main()
