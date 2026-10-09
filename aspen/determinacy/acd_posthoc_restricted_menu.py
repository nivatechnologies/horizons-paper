"""POST HOC saved-cost scoring only; realized arrays opened and logged in score()."""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1')
import hashlib, json, time
from pathlib import Path
import numpy as np
from scipy.stats import beta

ROOT = Path(__file__).resolve().parent
WORK = Path('/home/todd/work')
ORIGINAL = WORK/'aspen-determinacy-20261005/aspen/determinacy/runs/conf'
LEADS = (2., 3.)
TICKS = (3, 5)

def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1048576), b''): h.update(b)
    return h.hexdigest()

def read(path, key):
    with np.load(path, allow_pickle=False) as z: return z[key].copy()

def policies(j, valid, tick, menu):
    # Ordered menu preserves np.argmin's first-option tie rule.
    choice = int(menu[np.argmin(j[:,menu,tick].mean(0))]) if valid else 8
    gated = choice if choice != 8 and np.mean(j[:,choice,tick]-j[:,8,tick] < 0) >= .95 else 8
    return {'E':choice, 'C_delta_0':gated}

def rows(costs, valid, keep, actual, menu, label):
    ids=np.flatnonzero(keep); result=[]
    for lead,tick in zip(LEADS,TICKS):
        selections=[policies(j,v,tick,menu) for j,v in zip(costs,valid)]
        baseline=actual[ids,8,tick]
        oracle=actual[ids][:,menu,tick].min(1)
        den=float(np.mean(baseline-oracle))
        for policy in ('E','C_delta_0'):
            selected=np.array([s[policy] for s in selections])[ids]
            value=actual[ids,selected,tick]; effect=value-baseline
            acting=selected!=8; harmful=acting&(effect>0)
            n=int(acting.sum()); h=int(harmful.sum())
            probs=np.array([np.mean(costs[c][:,k,tick]-costs[c][:,8,tick]<0)
                            for c,k,a in zip(ids,selected,acting) if a])
            bounds=[float(beta.ppf(.05,h,n-h+1)) if h else 0.,
                    float(beta.ppf(.95,h+1,n-h)) if h<n else 1.] if n else [0.,1.]
            result.append(dict(post_hoc=True, menu=label, lead=lead, policy=policy,
                cases=len(ids), invalid_cases=int(np.sum(~valid&keep)), actions_taken=n,
                strict_positive_harms=h, harm_per_action=h/n if n else None,
                conditional_harm_CP_one_sided95=bounds, zero_effect_ties=int(np.sum(acting&(effect==0))),
                expected_harms=float(np.sum(1-probs)), mean_regret=float(np.mean(value-oracle)),
                mean_improvement=float(np.mean(baseline-value)), mean_no_action_regret=den,
                capture_fraction=float(np.mean(baseline-value)/den) if den else None,
                chosen_actions=np.bincount(selected,minlength=9).tolist(),
                case_indices=ids.tolist(), selected_actions=selected.tolist()))
    return result

def specifications():
    f=ROOT/'runs/fresh'; s=WORK/'aspen-stage21-scoring-20261008/aspen/determinacy/runs/stage21'
    original_models={'posterior':None,
        'CNN-F':WORK/'aspen-determinacy-stage18-20261007/aspen/determinacy/runs/stage9/inference/CNN-F',
        'CNN-noF':WORK/'aspen-determinacy-stage10b-20261007/aspen/determinacy/runs/stage9/inference/CNN-noF'}
    fresh_names=['CNN-F','CNN-noF']+[f'CNN-F-E0-fixed-seed{i}' for i in range(1,6)]
    shift_names=['CNN-F-constantF','CNN-noF']+[f'CNN-F-{kind}-{mode}-seed{i}'
        for kind,modes in [('E0',['fixed']),('E1',['fixed','rolling'])] for mode in modes for i in range(1,6)]
    return [('original',ORIGINAL,original_models,None),
            ('part3b_fresh',f,dict(posterior=None,**{n:f/'inference'/n for n in fresh_names}),f/'scoring.npz'),
            ('stage21',s,dict(posterior=None,**{n:s/'inference'/n for n in shift_names}),s/'scoring/actual.npz')]

def verify_full(panel,name,data):
    if panel=='original':
        source='acd_stage10b_decisions.json' if name=='CNN-noF' else 'acd_stage13_decisions.json'
        old=json.loads((ROOT/'receipts'/source).read_text())['models'][name]['readings']
    elif panel=='part3b_fresh' and name!='posterior':
        source='acd_stage19_part3b.json';old=json.loads((ROOT/'receipts'/source).read_text())['models'][name]['decisions']
    elif panel=='part3b_fresh':
        source='acd_stage19_learned.json';old=json.loads((ROOT/'receipts'/source).read_text())['models'][name]['decisions']
    else:
        source='acd_stage21_R12_recovery.json' if name=='posterior' or 'E1' not in name else 'acd_stage21_R34.json'
        old=json.loads((ROOT/'receipts'/source).read_text())['models'][name]['pooled']['decisions']
    checks=0
    for row in data:
        previous=next(x for x in old if x['lead']==row['lead'] and x['policy']==row['policy'])
        for key in ['mean_regret','mean_improvement','capture_fraction','chosen_actions']:
            assert row[key]==previous[key],(panel,name,key,row[key],previous[key])
            checks+=1
        assert row['strict_positive_harms']==previous['harms']
    if panel=='original':
        prior=json.loads((ROOT/'receipts/acd_stage17.json').read_text())['C']['models'][name]['selected']
        for row in data:
            previous=next(x for x in prior if x['lead']==row['lead'] and x['policy']==row['policy'])
            assert row['expected_harms']==previous['expected_harms']
            assert row['conditional_harm_CP_one_sided95']==previous['harm_conditional_CP_one_sided95']
            checks+=2
    return dict(receipt='receipts/'+source,exact_checks=checks)

def score():
    log=ROOT/'runs/posthoc_restricted_menu/access.jsonl';log.parent.mkdir(parents=True,exist_ok=True)
    access=[];panels={}
    def realized(path,key,panel):
        record=dict(panel=panel,caller=__file__,path=str(path),array=key,sha256=digest(path),utc=time.time())
        with log.open('a') as f:f.write(json.dumps(record)+'\n')
        access.append(record)
        return read(path,key)
    for panel,base,models,cache in specifications():
        files=sorted(base.glob('case_*.npz' if panel=='original' else 'main_forecast_*.npz'))
        keep=np.array([not bool(read(p,'excluded')) for p in files])
        actual=np.array([realized(base/f'score_{c:03d}.npz','actual_cost',panel) for c in range(len(files))]) if cache is None else realized(cache,'actual',panel)
        assert len(actual)==len(files)
        panel_rows={}
        for name,directory in models.items():
            costs=[];valid=[];hashes=[]
            for c,p in enumerate(files):
                path=p if directory is None else directory/f'{c:03d}.npz'
                j=read(path,'J');v=np.isfinite(j).all()
                if directory is not None:v=v and bool(read(path,'valid').all())
                costs.append(j);valid.append(v);hashes.append(digest(path))
            valid=np.array(valid)
            full=rows(costs,valid,keep,actual,np.arange(9),'full')
            reproduction=verify_full(panel,name,full)
            restricted=rows(costs,valid,keep,actual,np.arange(1,9),'restricted')
            panel_rows[name]=dict(full=full,restricted=restricted,full_menu_reproduction=reproduction,input_hashes=hashes)
            print(panel,name,'complete',flush=True)
        panels[panel]=panel_rows
    receipt=dict(post_hoc=True,licenses_frozen_route=False,code_sha256=digest(__file__),panels=panels,
        realized_access=access,definitions=dict(menu='indices 1 through 7 and no action index 8; uniform decrease index 0 removed',
        invalid='any nonfinite draw/option or invalid flag forces no action; no survivor conditioning',
        expected_harms='sum over acted instances of 1 minus the share of draws with D < 0',
        harms='strict-positive realized D; exact-zero acted ties recorded separately',
        bounds='exact one-sided 95% Clopper-Pearson lower and upper conditional on acting',
        oracle='minimum realized cost over the same menu as the policy'))
    (ROOT/'receipts/acd_posthoc_restricted_menu.json').write_text(json.dumps(receipt,indent=2,allow_nan=False)+'\n')
    lines=['# POST HOC restricted-menu decisions','','POST HOC throughout; licenses no frozen route. Saved predictions and realized caches only. No integration, inference or sampling.',
        '',f'Scoring script: acd_posthoc_restricted_menu.py; SHA-256 `{receipt["code_sha256"]}`. Every realized-cache access is logged in the receipt and runs/posthoc_restricted_menu/access.jsonl.',
        '',*list(receipt['definitions'].values())]
    for panel,models in panels.items():
        lines += ['',f'## POST HOC — {panel}','','| POST HOC pipeline | Lead | Policy | Menu | Actions | Strict-positive harms | Harms/action | CP lower | CP upper | Expected harms | Regret | Capture | Histogram (indices 0–8) |',
                  '|---|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|']
        for name,data in models.items():
            for full,restricted in zip(data['full'],data['restricted']):
                for r in [full,restricted]:
                    vals=[name,r['lead'],r['policy'],r['menu'],r['actions_taken'],r['strict_positive_harms'],r['harm_per_action'],*r['conditional_harm_CP_one_sided95'],r['expected_harms'],r['mean_regret'],r['capture_fraction'],r['chosen_actions']]
                    lines.append('| '+' | '.join(str(x) if not isinstance(x,float) else f'{x:.8g}' for x in vals)+' |')
    (ROOT/'ACD_POSTHOC_RESTRICTED_MENU.md').write_text('\n'.join(lines)+'\n')

if __name__=='__main__':score()
