"""Write Freeze F only after the exact full-receipt reproduction gate."""
from pathlib import Path
import argparse,hashlib,json,math
import acd_stage22_adapter as adapter
HERE=Path(__file__).resolve().parent
BASE=adapter.BASE
LATEST=Path('/mnt/niva-array/work/aspen-publication-stage18-selected-D/aspen/determinacy')
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def generate(n):
    gate=json.loads((HERE/'receipts/acd_stage22_reproduction.json').read_text())
    assert gate['N']==200 and gate['all_exact']
    assert gate['code']['adapter_sha256']==digest(HERE/'acd_stage22_adapter.py')
    for row in gate['results']:
        assert row['exact'] and row['different_values']==0
    for row in gate['code']['modules']:
        assert digest(HERE/row['path'])==row['sha256']
        assert digest(BASE/Path(row['baseline_path']).name)==row['baseline_sha256']
    assert n>0 and n%2==0
    freeze=json.loads((BASE/'receipts/acd_stage21_freeze_e.json').read_text())
    amendment=json.loads((BASE/'receipts/acd_stage21_freeze_e_amendment.json').read_text())
    for p,h in dict(freeze['code_hashes'],**amendment['code_hashes']).items():assert digest(BASE/p)==h,p
    tasks=[]
    names=['CNN-noF','CNN-F-constantF']+[f'CNN-F-E0-fixed-seed{k}' for k in range(1,6)]
    for name in names:
        row=dict(next(t for t in freeze['tasks'] if t['name']==name))
        for key in ['checkpoint','estimator']:
            if row.get(key):assert digest(BASE/row[key])==row[key+'_sha256']
        tasks.append(row)
    for k in range(1,6):
        row=dict(next(t for t in tasks if t['name']==f'CNN-F-E0-fixed-seed{k}'))
        row.update(name=f'CNN-F-E0-rolling-seed{k}',rolling=True)
        tasks.append(row)
    prior=json.loads((BASE/'receipts/acd_stage21_R12_recovery.json').read_text())
    interval=prior['confirmatory']['R2']['interval']
    original_n=len(json.loads((BASE/'receipts/acd_stage21_contract.json').read_text())['forcing_by_case'])
    half=(interval['upper']-interval['lower'])/2
    scaled=half*math.sqrt(original_n/n)
    namespaces=['acd-stage22-'+s for s in ['assign','instances','observation','sampler']]
    ids={s:int.from_bytes(hashlib.sha256(s.encode()).digest()[:8],'little') for s in namespaces}
    old=json.loads((BASE/'receipts/acd_stage21_contract.json').read_text())
    old_names=set(old['earlier_names'])|set(old['namespace_ids'])
    roots={int.from_bytes(hashlib.sha256(s.encode()).digest()[:8],'little') for s in old_names}
    assert not set(ids.values())&roots and len(set(ids.values()))==len(ids)
    leaves=[(ids[namespaces[0]],0,0,0,0,0)]
    for c in range(n):
        leaves.extend([(ids[namespaces[1]],0,0,c,0,0),(ids[namespaces[2]],0,1,c,0,0)])
        leaves.extend((ids[namespaces[3]],0,0,c,m,0) for m in range(128))
        leaves.extend((ids[namespaces[3]],0,s,c,m,0) for s in [1,2] for m in range(4))
    assert len(leaves)==len(set(leaves))
    climatology={str(BASE/f'runs/stage21/climatology/F{f}.npz'):digest(BASE/f'runs/stage21/climatology/F{f}.npz') for f in [7,9]}
    r=dict(N=n,forcing_counts={str(f):n//2 for f in [7,9]},tasks=tasks,
           rationale_R2=dict(source='receipts/acd_stage21_R12_recovery.json',key='$.confirmatory.R2.interval',point=interval['point'],original_assigned_n=original_n,half_width=half,scaled_half_width=scaled,half_point=interval['point']/2,scaling='half_width * sqrt(original_assigned_n / N)'),
           rationale_R5_R6=dict(source='receipts/acd_stage20_C.json',sha256=digest(LATEST/'receipts/acd_stage20_C.json'),scope='Original confirmation panel; post hoc E0 rolling versus E0 fixed, seven-pattern errors and gate harms.'),
           namespaces=ids,root_disjoint=True,leaves_unique=True,leaf_count=len(leaves),climatology=climatology,
           freeze_e_hashes=dict(freeze['code_hashes'],**amendment['code_hashes']),parameterization=gate['code'],reproduction=gate['results'],new_code_hashes={name:digest(HERE/name) for name in ['acd_stage22_adapter.py','acd_stage22_R56.py','acd_stage22_freeze.py']},
           criterion_changes=[],hardware='Baccus 170HX for all compared inference; sulaco CPU for sampling and scoring',
           resolutions=[dict(rule='R-other',detail='Case count N supplied by Stage22 adapter; count-only source changes beyond panel path, criteria unchanged. Same adapter applies to Stage23 scoring on this panel.')])
    (HERE/'receipts/acd_stage22_freeze_f.json').write_text(json.dumps(r,indent=2)+'\n')
    text='''# Stage22 Freeze F — fresh forcing-shift panel

Earlier freezes are unchanged. The Stage21 R2 result remains FAIL; this panel is neither pooled with it nor substituted for it. Start only after the prior queue, including Stage18 D/C, is complete and published. Freeze G was pushed before any Stage22 outcome is scored.

R2-S22: Retained CNN-noF minus CNN-F-E0-fixed confident-error share, on the seven zero-mean patterns at 2 LT. Each seed/instance requires at least one confident answer from both pipelines. Average the defined seed differences within each instance. Retain instances with at least one defined pair. The instance is the unit. Confirm only if the two-sided 99% v2.3 interval lies wholly above zero.

R5-S22: CNN-F-E0-rolling minus CNN-F-E0-fixed confident-error share, on the seven zero-mean patterns at 2 LT. Pair rolling seed k with fixed seed k. The contributing rule, seed averaging and instance unit are the same as R2. Confirm only if the two-sided 99% v2.3 interval lies wholly above zero. The existing Stage18 rolling path already accepts E0; no rollout logic changes are needed.

R6-S22: CNN-F-E0-rolling C(delta=0) harm conditional on acting at 3 LT, for each E0 seed. Use the exact one-sided 95% Clopper-Pearson lower bound and Freeze B L2 threshold (above 0.05), with strict-positive harms and zero-effect ties recorded separately. Confirm only if every seed passes. Only a thin wrapper around existing frozen statistic functions is authorized.

Panel size, balance and code-computed precision rationale are recorded below. Fixed n: no interim scoring, no extension after failure, no pooling with Stage21. Excluded instances are withheld and never replaced. Assignment follows the Stage21 permutation rule with only count and fresh namespaces changed. Posterior priors, NUTS settings, initialization, gates, thinning, full-draw rescoring and single warm-up retry stay unchanged. First-five timing uses the same worker layout and wall-time cap as Stage21.

Pipelines are retained CNN-noF, E0 fixed and rolling for every frozen E0 seed. Retained constant-eight CNN-F and posterior are descriptive only. No other confirmatory reading is added. All compared pipelines use the Baccus 170HX path. Frozen climatology is reused by hash. No earlier queue is preempted.

A failed E0-fixed seed makes R2-S22 and R5-S22 not evaluable. A failed E0-rolling seed makes R5-S22 and R6-S22 not evaluable. Available results remain descriptive. A nonzero task return code or missing complete.json marks the phase FAILED and blocks scoring/publication. Every task log is committed beside its execution JSON.

Execution reading (R-other): case count is the sole additional execution change beyond panel path; criteria unchanged. Parameterized copies leave earlier files untouched. N=200 with Stage21 namespaces must reproduce every value in all three committed Stage21 receipts exactly, including provenance and descriptive entries. Empty diffs, logged scoring-cache access, remaining literal inventory, case-coverage assertions, adapter hashes and line-level diffs are recorded with this freeze. Any differing value or failed assertion stops execution. Stage23 uses this same parameterization on the Stage22 panel.

The panel contract must be pushed before the first observation is generated. No outcome is generated or opened outside frozen scoring. Publication reports every required reading pooled and by forcing, with the full Freeze E descriptive set and uniform-decrease choice histogram.

'''
    (HERE/'ACD_STAGE22_FREEZE_F.md').write_text(text+'```json\n'+json.dumps(r,indent=2)+'\n```\n\n## Line-level count diff\n\n```diff\n'+(HERE/'ACD_STAGE22_PARAMETERIZATION.diff').read_text()+'```\n')
    return r
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--N',type=int,required=True);a=p.parse_args();generate(a.N)
