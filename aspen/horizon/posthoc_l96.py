"""Labeled post-hoc action-frequency diagnostic; no selectors changed."""
import json
import numpy as np
from common import ROOT,GRID,write_json,sha

def main():
    root=ROOT/'runs/l96/test';cases=json.loads((root/'case_statistics.json').read_text())['cases']
    failed=[]
    for c in range(200):
        data=np.load(root/f'case_{c:03d}.npz')
        for name in data.files:
            if not np.isfinite(data[name]).all():failed.append(dict(case=c,array=name))
    if failed:raise RuntimeError(f'nonfinite solver test arrays: {failed}')
    counts=[]
    for h,T in enumerate(GRID):
        best=[r['best'][h] for r in cases if r['eligible'][h]]
        counts.append(dict(T=float(T),eligible=len(best),best_action_counts=np.bincount(best,minlength=8).tolist()))
    myopic=[json.loads((root/f'myopic_{c:03d}.json').read_text())['chosen'] for c in range(200)]
    write_json(ROOT/'results/l96_posthoc_action_frequency.json',dict(posthoc=True,criterion=False,git_sha=sha(),
         selector='final blinded Codex run1 action set, one framing',horizons=counts,
         myopic_action_counts=np.bincount(myopic,minlength=8).tolist(),solver_cases_checked_finite=200))
    print('Posthoc action frequencies retained; all200 solver cases finite.',flush=True)

if __name__=='__main__':main()
