"""EXPLORATORY: existing Stage-1 realized action costs, without WO gates."""
import argparse,datetime,hashlib,json
from pathlib import Path
import numpy as np
from protocol import ROOT,LEADS,rng,digest,write_json

ARMS=['N-last','N-oracle','CNN-20k','N-win','N-mis','myopic','fixed']
PAIRS=[('CNN-20k','N-last'),('N-win','N-last'),('N-win','CNN-20k')]
DIRECTORY='runs/exploratory_actual_cost'


def register(root,authorization):
    sources={}
    paths=[root/name for name in ['explore_actual_cost.py','check_explore_actual_cost.py','protocol.py','score_stage1.py']]
    paths += [root/'runs/stage1_cases.json',root/'inputs/CNN-20k.pt']
    for c in range(200):
        paths += [root/f'runs/test/cpu_{c:03d}.npz']
        for name in ['CNN-20k','N-win','N-mis']:paths += [root/f'runs/test/{name}_{c:03d}.npz',root/f'runs/test/{name}_{c:03d}.json']
    for path in paths:sources[str(path.relative_to(root))]=digest(path)
    record=dict(label='EXPLORATORY ONLY; no WO gate or reading changes',registered_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),authorization=authorization,
        planned_outputs=['runs/exploratory_actual_cost/cases.json','runs/exploratory_actual_cost/results.json','runs/exploratory_actual_cost/checker.json','NUMBERS_EXPLORATORY_ACTUAL_COST.md','AFD_EXPLORATORY_ACTUAL_COST.md'],
        source_hashes=sources,bootstrap=dict(namespace='afd-bootstrap',substream=3,case=0,member='100+j for j=0..6',draws=2000,quantiles=[.025,.975],quantile_method='numpy linear'),
        rules=dict(all_cases=True,eligibility_filter=False,decision_leads=LEADS[1:].tolist(),actions='actual_cost[:8]; index8 no-action excluded from winner/range',ties='np.argmin lowest action index',normalization='panel median across cases of the eight-action actual-cost range, recomputed within each paired case bootstrap draw',failed_cases='wrong actual-best top1; actual worst-action regret',fixed='Already-selected validation action recovered from stored Stage1 fixed_correct flags, no action is reselected'))
    target=root/DIRECTORY/'input_manifest.json';write_json(target,record)
    with (root/'AFD_ARTIFACTS.md').open('a') as stream:stream.write('\n- EXPLORATORY actual-cost comparison registered before computation: '+str(target.relative_to(root))+' SHA256 '+digest(target)+'; '+record['registered_at']+'. Existing Stage1 inputs only; no WO gate changes.\n')
    return record


def interval(values):
    if not np.isfinite(values).all():return None
    lo,hi=np.quantile(values,[.025,.975],method='linear')
    return dict(lower=float(lo),upper=float(hi))


def compute(root,manifest):
    for path,sha in manifest['source_hashes'].items():
        if digest(root/path)!=sha:raise ValueError('registered source changed: '+path)
    stored=json.loads((root/'runs/stage1_cases.json').read_text())['cases']
    fixed_set={e['b'] for row in stored for e in row['leads'] if e['fixed_correct']}
    if len(fixed_set)!=1:raise ValueError('previously validation-selected fixed action cannot be recovered')
    fixed=next(iter(fixed_set))
    if any(e['fixed_correct']!=(e['b']==fixed) for row in stored for e in row['leads']):raise ValueError('fixed-action flags disagree')
    cases=[]
    for c in range(200):
        actual=[];reference=[];choices={name:[] for name in ARMS};failed={name:[] for name in ARMS}
        with np.load(root/f'runs/test/cpu_{c:03d}.npz') as cpu:
            costs={name:cpu[name+'_cost'].mean(1) for name in ['N-last','N-oracle']}
            myopic=int(costs['N-last'][:,0].argmin())
            models={}
            for name in ['CNN-20k','N-win','N-mis']:
                with np.load(root/f'runs/test/{name}_{c:03d}.npz') as loaded:models[name]=(loaded['cost'].copy(),loaded['survivors'].copy())
            meta=json.loads((root/f'runs/test/CNN-20k_{c:03d}.json').read_text())
            if meta['checkpoint_sha256']!=manifest['source_hashes']['inputs/CNN-20k.pt']:raise ValueError('baseline checkpoint changed')
            for j,h in enumerate(range(1,8)):
                actual.append(cpu['actual_cost'][:8,h].tolist())
                b=int(cpu['truth_cost'][:8,:1024,h].mean(1).argmin());reference.append(b)
                if stored[c]['leads'][j]['b']!=b:raise ValueError('frozen reference b mismatches raw truth')
                for name in ARMS:
                    bad=False
                    if name in costs:chosen=int(costs[name][:,h].argmin())
                    elif name=='myopic':chosen=myopic
                    elif name=='fixed':chosen=fixed
                    else:
                        predicted,keep=models[name];bad=int((~keep[h]).sum())>32;chosen=-1 if bad else int(predicted[h].argmin())
                    choices[name].append(chosen);failed[name].append(bad)
        cases.append(dict(case=c,actual_cost=actual,reference_b=reference,choices=choices,failed=failed))
    leads=[]
    for j,T in enumerate(LEADS[1:]):
        energy=np.array([case['actual_cost'][j] for case in cases]);best=energy.argmin(1);ranges=np.ptp(energy,axis=1);scale=float(np.median(ranges));regrets={};arms={}
        samples=rng('afd-bootstrap',3,case=0,member=100+j).integers(200,size=(2000,200));draw_scales=np.median(ranges[samples],axis=1)
        for name in ARMS:
            choice=np.array([case['choices'][name][j] for case in cases]);bad=np.array([case['failed'][name][j] for case in cases]);chosen=energy[np.arange(200),np.maximum(choice,0)];chosen[bad]=energy[bad].max(1)
            raw=chosen-energy.min(1);regrets[name]=raw;draw_raw=raw[samples].mean(1)
            with np.errstate(divide='ignore',invalid='ignore'):draw_normalized=draw_raw/draw_scales
            arms[name]=dict(mean_regret_raw=float(raw.mean()),mean_regret_normalized=float(raw.mean()/scale) if scale>0 else None,
                regret_raw_interval=interval(draw_raw),regret_normalized_interval=interval(draw_normalized),actual_best_top1=float(np.mean((choice==best)&~bad)),actual_best_top1_count=int(np.sum((choice==best)&~bad)),failed_cases=int(bad.sum()))
        differences={}
        for left,right in PAIRS:
            values=regrets[left]-regrets[right];draw_raw=values[samples].mean(1)
            with np.errstate(divide='ignore',invalid='ignore'):draw_normalized=draw_raw/draw_scales
            differences[left+' minus '+right]=dict(mean_raw=float(values.mean()),mean_normalized=float(values.mean()/scale) if scale>0 else None,raw_interval=interval(draw_raw),normalized_interval=interval(draw_normalized))
        leads.append(dict(lead_LT=float(T),cases=200,actual_panel_median_action_range=scale,arms=arms,paired_differences=differences,
            reference_b_equals_actual_best=float(np.mean(np.array([case['reference_b'][j] for case in cases])==best)),reference_b_equals_actual_best_count=int(np.sum(np.array([case['reference_b'][j] for case in cases])==best)),resample_sha256=hashlib.sha256(samples.tobytes()).hexdigest()))
    result=dict(label=manifest['label'],computed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),input_manifest_sha256=digest(root/DIRECTORY/'input_manifest.json'),rules=manifest['rules'],bootstrap=manifest['bootstrap'],fixed_action=fixed,
        fixed_action_provenance=dict(source='runs/stage1_cases.json',source_sha256=manifest['source_hashes']['runs/stage1_cases.json'],original_selection_source='score_stage1.py',original_selection_source_sha256=manifest['source_hashes']['score_stage1.py'],selection='Mode of first1024-member primary validation truth winners, lowest-index tie; existing flags only, not reselected'),source_hashes=manifest['source_hashes'],leads=leads,WO_gates_invoked=False,WO_readings_changed=False)
    return dict(cases=cases,label='EXPLORATORY'),result


def markdown(result,checker):
    def f(value):return 'unavailable' if value is None else f'{value:.8g}'
    def bounds(record):return 'unavailable' if record is None else '['+f(record['lower'])+', '+f(record['upper'])+']'
    out=['# EXPLORATORY — existing Stage1 actual-cost comparison','',
        'All cases, all frozen decision leads. These exploratory results do not change WO eligibility, gates, readings or licensed sentences. No-action index8 is excluded from the eight-action winner and range. Ties use the lowest action index. Fixed action is the previously validation-selected null; it was not reselected.','',
        'EXPLORATORY regret: chosen realized energy minus minimum realized energy. Normalized regret divides by the panel median eight-action realized energy range. Each paired case bootstrap draw recomputes that median; intervals use numpy linear quantiles 0.025 and 0.975. Positive paired differences mean the first arm has greater regret.','',
        '| EXPLORATORY lead (LT) | Arm | Mean raw regret | Mean normalized regret | Raw regret 95% interval | Normalized regret 95% interval | Failed cases |','|---|---|---|---|---|---|---|']
    for lead in result['leads']:
        for name,m in lead['arms'].items():out.append('| '+' | '.join([f(lead['lead_LT']),name,f(m['mean_regret_raw']),f(m['mean_regret_normalized']),bounds(m['regret_raw_interval']),bounds(m['regret_normalized_interval']),str(m['failed_cases'])])+' |')
    out+=['','| EXPLORATORY lead (LT) | Arm | Choice equals realized-cost argmin, all cases | Matching cases / all cases |','|---|---|---|---|']
    for lead in result['leads']:
        for name,m in lead['arms'].items():out.append('| '+f(lead['lead_LT'])+' | '+name+' | '+f(m['actual_best_top1'])+' | '+str(m['actual_best_top1_count'])+' / '+str(lead['cases'])+' |')
    out+=['','Reference b is the frozen first1024-member conditional-truth winner, not the single realized trajectory winner.','',
        '| EXPLORATORY lead (LT) | Frozen reference b equals realized-cost argmin | Matching cases / all cases | Realized panel median action range |','|---|---|---|---|']
    for lead in result['leads']:out.append('| '+f(lead['lead_LT'])+' | '+f(lead['reference_b_equals_actual_best'])+' | '+str(lead['reference_b_equals_actual_best_count'])+' / '+str(lead['cases'])+' | '+f(lead['actual_panel_median_action_range'])+' |')
    out+=['','| EXPLORATORY lead (LT) | First arm minus second arm | Mean raw difference | Raw 95% interval | Mean normalized difference | Normalized 95% interval |','|---|---|---|---|---|---|']
    for lead in result['leads']:
        for name,m in lead['paired_differences'].items():out.append('| '+' | '.join([f(lead['lead_LT']),name,f(m['mean_raw']),bounds(m['raw_interval']),f(m['mean_normalized']),bounds(m['normalized_interval'])])+' |')
    out+=['','Independent checker: '+checker['status']+'. Finite tampering and NaN are rejected. Numerical source: NUMBERS_EXPLORATORY_ACTUAL_COST.md.','']
    return '\n'.join(out)


def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--authorization',required=True);p.add_argument('--register-only',action='store_true');a=p.parse_args()
    manifest=register(a.root,a.authorization)
    if a.register_only:return
    cases,result=compute(a.root,manifest)
    write_json(a.root/DIRECTORY/'cases.json',cases);write_json(a.root/DIRECTORY/'results.json',result)
    from check_explore_actual_cost import check,tamper_checks
    checker=check(a.root,cases,result);checker.update(tamper_checks(a.root,cases,result));write_json(a.root/DIRECTORY/'checker.json',checker)
    write_json(a.root/DIRECTORY/'output_manifest.json',dict(label='EXPLORATORY',files={str((a.root/DIRECTORY/name).relative_to(a.root)):digest(a.root/DIRECTORY/name) for name in ['input_manifest.json','cases.json','results.json','checker.json']}))
    (a.root/'AFD_EXPLORATORY_ACTUAL_COST.md').write_text(markdown(result,checker))
    (a.root/'NUMBERS_EXPLORATORY_ACTUAL_COST.md').write_text('# NUMBERS — EXPLORATORY actual-cost comparison\n\nNo WO reading changes.\n\n```json\n'+json.dumps(dict(result=result,checker=checker,artifact_hashes=json.loads((a.root/DIRECTORY/'output_manifest.json').read_text())['files']),indent=2,allow_nan=False)+'\n```\n')
    print(json.dumps(checker),flush=True)
if __name__=='__main__':main()
