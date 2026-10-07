"""Stage18 retained-panel scoring on Sulaco only; inherited Stage9 F5 readings."""
import os
os.environ.update(JAX_PLATFORMS='cpu', JAX_ENABLE_X64='true', OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', NUMBA_NUM_THREADS='2')
import argparse
import json
import shutil
import socket
from pathlib import Path
import numpy as np
from acd_protocol import ROOT, LEADS
import acd_stage9_cnn_metrics as inherited
from acd_stage13_analysis import decision_rows, choices
from acd_stage6_analysis import binary, stack
from acd_stats import cp_bounds
os.environ['NUMBA_NUM_THREADS'] = '2'
import numba
numba.set_num_threads(2)
OUT = ROOT/'runs/stage18'


def score(name):
    if socket.gethostname() != 'sulaco':
        raise RuntimeError('Stage18 realized outcomes may be opened only by scoring on Sulaco')
    source = ROOT/'runs/stage9/receipt_analyses.json'
    target = OUT/'receipt_analyses.json'
    if not target.exists():
        shutil.copyfile(source, target)
    inherited.DEST = OUT
    inherited.run(name)
    result = json.loads((OUT/f'metrics_{name}.json').read_text())
    # All realized costs are opened in this scoring-only function.
    actual = np.asarray([np.load(inherited.RAW/f'conf/score_{c:03d}.npz')['actual_cost'] for c in range(200)])
    with np.load(ROOT/'runs/stage4b_null/null_0.16.npz') as data:
        null_j = data['J'].copy()
    sd = (null_j[:, :8]-null_j[:, 8, None]).std(0, ddof=1)
    costs, valid, keep = [], [], []
    forcing_errors = []
    for case in range(200):
        with np.load(inherited.RAW/f'conf/case_{case:03d}.npz') as data:
            keep.append(not bool(data['excluded']))
        with np.load(OUT/'inference'/name/f'{case:03d}.npz') as data:
            costs.append(data['J'].copy())
            valid.append(bool(data['valid'].all()) and np.isfinite(data['J']).all())
            if 'estimated_F_at_cutoff' in data:
                estimate = data['estimated_F_at_cutoff'].copy()
                with np.load(OUT/'confirmation_inputs'/f'{case:03d}.npz') as inputs:
                    forcing = np.repeat(inputs['F'], 9)
                forcing_errors.append(np.column_stack([estimate, forcing]))
    readings, _ = decision_rows(actual, costs, np.asarray(valid), np.asarray(keep), sd)
    for row in readings:
        tick = int(np.flatnonzero(np.asarray(LEADS) == row['lead'])[0])
        ch = choices(costs, np.asarray(valid), tick, sd)[row['policy']]
        acted = (ch != 8) & keep
        bad = (actual[np.arange(200), ch, tick] > actual[:, 8, tick]) & acted
        count, harm = int(acted.sum()), int(bad.sum())
        row.update(actions_taken=count, harm_conditional_on_acting=harm/count if count else None,
                   conditional_harm_CP95=list(cp_bounds(harm, count)) if count else [0., 1.],
                   uniform_decrease_every_instance=bool(np.all(ch[np.asarray(keep)] == 0)))
    result['decisions'] = readings
    if forcing_errors:
        values = np.concatenate(forcing_errors)
        error = values[:, 0]-values[:, 1]
        result['forcing_estimate_error'] = dict(RMSE=float(np.sqrt(np.mean(error**2))), bias=float(error.mean()),
                                               correlation=float(np.corrcoef(values.T)[0, 1]),
                                               population='each retained draw/action at the cutoff equally')
    if name == 'CNN-F-ownF':
        maximum = 0.
        changes = 0
        jbar = json.loads((ROOT/'receipts/acd_stage2.json').read_text())['null']['jbar']
        null = np.asarray(json.loads((ROOT/'receipts/acd_stage2.json').read_text())['null']['question_probabilities'])[np.r_[np.arange(8), 37]]
        for case, predicted in enumerate(costs):
            with np.load(ROOT/'runs/stage9/inference/CNN-F'/f'{case:03d}.npz') as data:
                original = data['J'].copy()
            maximum = max(maximum, float(np.max(np.abs(predicted-original))))
            changes += int(np.sum(binary(predicted, jbar, null)['confident'] != binary(original, jbar, null)['confident']))
        result['GB10_reproduction'] = dict(max_absolute_cost_difference=maximum, confidence_classification_changes=changes)
    path = ROOT/'receipts'/f'acd_stage18_{name}.json'
    path.write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    print(json.dumps(dict(model=name, confidence=result['confidence_readings'], decisions=readings), indent=2), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('name')
    score(parser.parse_args().name)
