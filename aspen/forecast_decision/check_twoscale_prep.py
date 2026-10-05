"""Independent raw two-scale dt-check replay; no campaign/test panel access."""
import argparse,copy,json,hashlib,datetime
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1<<20),b''):h.update(block)
    return h.hexdigest()
def check(record,folder):
    assert record['status']=='PASS'
    assert record['chosen_dt']==record['rounds'][-1]['dt']
    reports=[]
    for round in record['rounds']:
        dt=round['dt'];data=[];ranges=[]
        for c in range(16):
            with np.load(folder/f'dtcheck_{dt}_{c:02d}.npz') as d:
                coarse=d['coarse'];fine=d['fine']
            assert coarse.shape==fine.shape==(8,512,3)
            assert np.isfinite(coarse).all() and np.isfinite(fine).all()
            ranges.append(np.ptp(coarse.mean(1),axis=0));data.append((coarse,fine))
        scales=np.median(ranges,axis=0)
        assert np.array_equal(scales,np.array(round['S_J']))
        changes=np.zeros(3,int);entries=[]
        for c,(coarse,fine) in enumerate(data):
            for h in range(3):
                b=int(coarse[:,:,h].mean(1).argmin())
                changes[h]+=b!=int(fine[:,:,h].mean(1).argmin())
                for k in range(8):
                    if k==b:continue
                    delta=fine[k,:,h]-fine[b,:,h]-coarse[k,:,h]+coarse[b,:,h]
                    change=abs(float(delta.mean()));se=float(delta.std(ddof=1)/np.sqrt(512))
                    threshold=max(.05*scales[h],2*se)
                    entries.append(dict(case=c,h=h+1,action=k,b=b,change=change,SE=se,
                        threshold=float(threshold),passed=bool(scales[h]>0 and change<threshold)))
        assert len(entries)==len(round['comparisons'])==336
        for got,want in zip(round['comparisons'],entries):
            for key in ['case','h','action','b','passed']:assert got[key]==want[key],key
            for key in ['change','SE','threshold']:
                assert np.isclose(got[key],want[key],rtol=1e-12,atol=1e-12),key
        assert np.array_equal(changes,round['argmin_changes'])
        passed=all(v['passed'] for v in entries);assert passed==round['passed']
        reports.append(dict(dt=dt,comparisons=len(entries),failed=sum(not v['passed'] for v in entries),
            S_J=scales.tolist(),argmin_changes=changes.tolist(),seconds=round['seconds'],passed=passed,
            maximum_change=max(v['change'] for v in entries),minimum_threshold=min(v['threshold'] for v in entries)))
    assert reports[-1]['passed']
    return reports

def main():
    folder=ROOT/'runs/twoscale';path=folder/'decision_dtcheck.json'
    record=json.loads(path.read_text());rounds=check(record,folder)
    bad=copy.deepcopy(record);bad['rounds'][-1]['comparisons'][0]['passed']=False
    try:check(bad,folder)
    except AssertionError:tamper=True
    else:raise RuntimeError('tamper accepted')
    entries=[]
    names=['runs/twoscale/decision_dtcheck.json','runs/twoscale/statecheck.json',
           'runs/twoscale/fastlib.json','runs/twoscale/sampler_check.json','runs/training_data2/closure.json',
           'runs/training_data2/base_train.npz','runs/training_data2/base_val.npz',
           'runs/training_data2/pairs.npz','runs/training_data2/cost.npz',
           'runs/training_data2/base_train.json','runs/training_data2/base_val.json',
           'runs/training_data2/pairs.json','runs/training_data2/cost.json',
           'runs/twoscale/fastlib.npz','runs/twoscale/sampler_raw.npz',
           'twoscale_data.py','twoscale_campaign.py','check_twoscale_prep.py']
    names += [str(p.relative_to(ROOT)) for p in sorted(folder.glob('dtcheck_*.npz'))]
    for name in names:
        p=ROOT/name
        if p.exists():entries.append(dict(path=name,sha256=sha(p),kind='two-scale preparation before panel evaluation'))
    for name in ['base_train','base_val','pairs','cost']:
        p=ROOT/f'runs/training_data2/{name}.npz';meta=json.loads(p.with_suffix('.json').read_text())
        assert sha(p)==meta['sha256']
    result=dict(status='PASS',tamper_rejected=tamper,checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        raw_record_sha256=sha(path),rounds=rounds,artifact_entries=entries,
        access_scope='two-scale dtcheck and training/preparation artifacts only; no campaign/test outputs')
    (folder/'dtcheck_checked.json').write_text(json.dumps(result,indent=2)+'\n')
    numbers=['## AFD_TWOSCALE_DECISION_DTCHECK','',
        'Source: `runs/twoscale/decision_dtcheck.json`; independently replayed from sixteen raw dt-check artifacts.',
        'Checker: `check_twoscale_prep.py`; evidence: `runs/twoscale/dtcheck_checked.json`.',
        '',f"Status: {result['status']}; tamper rejection: {tamper}.",'',
        '| dt | comparisons | failed | elapsed CPU wall seconds | argmin changes (1, 1.5, 2 LT_ref) | S_J |',
        '|---|---|---|---|---|---|']
    for r in rounds:numbers.append(f"| {r['dt']!r} | {r['comparisons']} | {r['failed']} | {r['seconds']!r} | {r['argmin_changes']} | {r['S_J']} |")
    numbers+=['',f"Chosen dt: {record['chosen_dt']!r}. N2 solver dt remains 0.01 under WO §4 propagation.",'',
        'Every comparison requires a strictly smaller absolute mean gap change than max(0.05*S_J, two paired standard errors).',
        'State check, sampler approval and decision-cost check remain separate gates. No two-scale panel was launched by this checker.','']
    (ROOT/'NUMBERS_TWOSCALE_PREP_FRAGMENT.md').write_text('\n'.join(numbers))
    report=['# Two-scale decision timestep check','',
        f"PASS at dt {record['chosen_dt']!r}, independently checked against raw paired costs. All {rounds[-1]['comparisons']} comparisons pass; argmin-change counts are {rounds[-1]['argmin_changes']} at leads 1, 1.5 and 2 LT_ref.",'',
        'Measured values are registered in `NUMBERS_TWOSCALE_PREP_FRAGMENT.md`. Checker and altered-record rejection both pass.',
        'No refinement propagates. The two-scale solver keeps dt 0.001; N2 and its variants keep dt 0.01.',
        'The sampler report still requires Todd’s explicit go before two-scale panels.', '']
    (ROOT/'AFD_TWOSCALE_DTCHECK_REPORT.md').write_text('\n'.join(report))
    registry=['# Two-scale preparation artifact registry fragment','',
        'Entries copied from measured local preparation artifacts for coordinator merge into AFD_ARTIFACTS.md. No test evaluation performed.','']
    registry.extend('- '+json.dumps(e) for e in entries)
    (ROOT/'AFD_TWOSCALE_ARTIFACTS_FRAGMENT.md').write_text('\n'.join(registry)+'\n')
    print('two-scale raw replay, copied training hashes and tamper rejection PASS')
if __name__=='__main__':main()
