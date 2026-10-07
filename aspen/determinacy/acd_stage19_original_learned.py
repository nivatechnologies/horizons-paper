"""Original-panel L1/L2 comparison; realized arrays are opened inside scoring only."""
import os
os.environ.update(NUMBA_NUM_THREADS='2', OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
import argparse
import hashlib
import json
from pathlib import Path
import socket
import numpy as np
from acd_stats import difference_interval, cp_bounds


def score(root, nof, actual_root, decision_receipt, output):
    if socket.gethostname() != 'sulaco':
        raise RuntimeError('Original comparison outcome scoring is on Sulaco only')
    records = []
    for case in range(200):
        # Realized answers are accessed only in this scoring function.
        with np.load(actual_root/f'conf/score_{case:03d}.npz') as d:
            actual = d['actual_cost'].copy()
        with np.load(actual_root/f'conf/case_{case:03d}.npz') as d:
            if bool(d['excluded']):
                continue
        fractions, counts = [], {}
        for name, directory in [('CNN-F', root/'runs/stage9/inference/CNN-F'), ('CNN-noF', nof)]:
            with np.load(directory/f'{case:03d}.npz') as d:
                j = d['J'].copy()
                valid = d['valid'].all() and np.isfinite(j).all()
            p = (j[:, 1:8, 3] < j[:, 8, None, 3]).mean(0)
            confident = (np.maximum(p, 1-p) >= .95) & valid
            wrong = (p > .5) != (actual[1:8, 3] < actual[8, 3])
            n, errors = int(confident.sum()), int(wrong[confident].sum())
            counts[name] = dict(answers=n, wrong=errors)
            fractions.append(errors/n if n else None)
        if all(v is not None for v in fractions):
            records.append(dict(case=case, counts=counts, difference=fractions[1]-fractions[0]))
    interval = difference_interval([r['difference'] for r in records])
    decisions = json.loads(decision_receipt.read_text())
    row = next(r for r in decisions['models']['CNN-noF']['readings'] if r['lead'] == 3 and r['policy'] == 'C_delta_0')
    acting = sum(row['chosen_actions'][:8])
    result = dict(panel='original confirmation; post hoc comparison',
                  L1=dict(cases=len(records), interval=interval, case_records=records),
                  L2=dict(actions_taken=acting, harms=row['harms'], conditional_harm_CP95=list(cp_bounds(row['harms'], acting))),
                  code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: {f: v for f, v in result[k].items() if f != 'case_records'} for k in ['L1', 'L2']}, indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--root', type=Path, required=True)
    p.add_argument('--noF', type=Path, required=True)
    p.add_argument('--actual-root', type=Path, required=True)
    p.add_argument('--decision-receipt', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    score(a.root, a.noF, a.actual_root, a.decision_receipt, a.output)
