"""Independent EXPLORATORY raw and paired-bootstrap arithmetic checker."""
import copy,hashlib,json,math
import numpy as np
from protocol import LEADS,rng,digest


def finite_tree(value):
    if isinstance(value,dict):
        for item in value.values():finite_tree(item)
    elif isinstance(value,list):
        for item in value:finite_tree(item)
    elif isinstance(value,float) and not math.isfinite(value):raise ValueError('nonfinite exploratory record')


def same(actual,expected):
    if isinstance(expected,dict):
        if not isinstance(actual,dict) or set(actual)!=set(expected):raise ValueError('exploratory key mismatch')
        for key in expected:same(actual[key],expected[key])
    elif isinstance(expected,list):
        if len(actual)!=len(expected):raise ValueError('exploratory length mismatch')
        for a,b in zip(actual,expected):same(a,b)
    elif isinstance(expected,float):
        if actual is None or not np.isclose(actual,expected,rtol=1e-12,atol=1e-12):raise ValueError('exploratory arithmetic mismatch')
    elif actual!=expected:raise ValueError('exploratory value mismatch')


def ci(values):
    if not all(math.isfinite(float(value)) for value in values):return None
    return dict(lower=float(np.quantile(values,.025,method='linear')),upper=float(np.quantile(values,.975,method='linear')))


def check(root,case_record,result,raw=True):
    finite_tree(case_record);finite_tree(result)
    cases=case_record['cases'];assert len(cases)==200 and [r['case'] for r in cases]==list(range(200))
    assert result['WO_gates_invoked'] is False and result['WO_readings_changed'] is False
    assert result['rules']['all_cases'] is True and result['rules']['eligibility_filter'] is False
    assert result['bootstrap']==dict(namespace='afd-bootstrap',substream=3,case=0,member='100+j for j=0..6',draws=2000,quantiles=[.025,.975],quantile_method='numpy linear')
    assert len(result['leads'])==7 and [r['lead_LT'] for r in result['leads']]==LEADS[1:].tolist()
    arms=['N-last','N-oracle','CNN-20k','N-win','N-mis','myopic','fixed'];pairs=[('CNN-20k','N-last'),('N-win','N-last'),('N-win','CNN-20k')]
    if raw:
        manifest_path=root/'runs/exploratory_actual_cost/input_manifest.json';manifest=json.loads(manifest_path.read_text())
        same(result['input_manifest_sha256'],digest(manifest_path));same(result['source_hashes'],manifest['source_hashes'])
        for path,sha in result['source_hashes'].items():same(digest(root/path),sha)
        originals=json.loads((root/'runs/stage1_cases.json').read_text())['cases'];fixed=result['fixed_action']
        chosen_fixed={e['b'] for row in originals for e in row['leads'] if e['fixed_correct']}
        assert chosen_fixed=={fixed} and all(e['fixed_correct']==(e['b']==fixed) for row in originals for e in row['leads'])
        for c,row in enumerate(cases):
            with np.load(root/f'runs/test/cpu_{c:03d}.npz') as cpu:
                same(row['actual_cost'],cpu['actual_cost'][:8,1:8].T.tolist())
                winners=np.argmin(np.mean(cpu['truth_cost'][:8,:1024,1:8],axis=1),axis=0).tolist();same(row['reference_b'],winners)
                same(winners,[e['b'] for e in originals[c]['leads']])
                for name in ['N-last','N-oracle']:
                    selected=np.argmin(np.mean(cpu[name+'_cost'],axis=1),axis=0);same(row['choices'][name],selected[1:8].tolist());same(row['failed'][name],[False]*7)
                myopic=int(np.argmin(np.mean(cpu['N-last_cost'][:,:,0],axis=1)));same(row['choices']['myopic'],[myopic]*7);same(row['choices']['fixed'],[fixed]*7)
                same(row['failed']['myopic'],[False]*7);same(row['failed']['fixed'],[False]*7)
            for name in ['CNN-20k','N-win','N-mis']:
                with np.load(root/f'runs/test/{name}_{c:03d}.npz') as learned:
                    failures=(np.count_nonzero(~learned['survivors'],axis=1)>32)[1:8]
                    predicted=np.argmin(learned['cost'][1:8],axis=1);predicted[failures]=-1
                    same(row['choices'][name],predicted.tolist());same(row['failed'][name],failures.tolist())
            meta=json.loads((root/f'runs/test/CNN-20k_{c:03d}.json').read_text());same(meta['checkpoint_sha256'],result['source_hashes']['inputs/CNN-20k.pt'])
    for j,lead in enumerate(result['leads']):
        energy=np.asarray([row['actual_cost'][j] for row in cases]);lowest=np.min(energy,axis=1);highest=np.max(energy,axis=1);range_=highest-lowest;scale=float(np.median(range_));best=np.argmin(energy,axis=1)
        assert lead['cases']==200;assert set(lead['arms'])==set(arms)
        same(lead['actual_panel_median_action_range'],scale)
        same(lead['reference_b_equals_actual_best'],sum(row['reference_b'][j]==int(best[c]) for c,row in enumerate(cases))/200)
        same(lead['reference_b_equals_actual_best_count'],sum(row['reference_b'][j]==int(best[c]) for c,row in enumerate(cases)))
        selections=rng('afd-bootstrap',3,case=0,member=100+j).integers(200,size=(2000,200));same(lead['resample_sha256'],hashlib.sha256(selections.tobytes()).hexdigest())
        raw_regret={};draw_raw={};draw_norm={};draw_scale=np.asarray([np.median(range_[indices]) for indices in selections])
        for name in arms:
            values=np.asarray([highest[c]-lowest[c] if row['failed'][name][j] else energy[c,row['choices'][name][j]]-lowest[c] for c,row in enumerate(cases)])
            raw_regret[name]=values;draw_raw[name]=np.asarray([np.mean(values[indices]) for indices in selections])
            with np.errstate(divide='ignore',invalid='ignore'):draw_norm[name]=draw_raw[name]/draw_scale
            same(lead['arms'][name],dict(mean_regret_raw=float(np.mean(values)),mean_regret_normalized=float(np.mean(values)/scale) if scale>0 else None,
                regret_raw_interval=ci(draw_raw[name]),regret_normalized_interval=ci(draw_norm[name]),actual_best_top1=sum(not row['failed'][name][j] and row['choices'][name][j]==int(best[c]) for c,row in enumerate(cases))/200,actual_best_top1_count=sum(not row['failed'][name][j] and row['choices'][name][j]==int(best[c]) for c,row in enumerate(cases)),failed_cases=sum(row['failed'][name][j] for row in cases)))
        assert set(lead['paired_differences'])=={a+' minus '+b for a,b in pairs}
        for left,right in pairs:
            differences=raw_regret[left]-raw_regret[right];replicates=np.asarray([np.mean(differences[indices]) for indices in selections])
            with np.errstate(divide='ignore',invalid='ignore'):normalized=replicates/draw_scale
            same(lead['paired_differences'][left+' minus '+right],dict(mean_raw=float(np.mean(differences)),mean_normalized=float(np.mean(differences)/scale) if scale>0 else None,raw_interval=ci(replicates),normalized_interval=ci(normalized)))
    return dict(status='PASS',label='EXPLORATORY',all_cases=200,decision_leads=7,arms=7,raw_source_and_choices_checked=raw,paired_bootstrap_draws=2000,normalization_recomputed_per_draw=True,WO_gates_invoked=False,checker_source_sha256=digest(root/'check_explore_actual_cost.py'))


def tamper_checks(root,cases,result):
    bad=copy.deepcopy(result);bad['leads'][0]['arms']['CNN-20k']['mean_regret_raw']+=.01
    try:check(root,cases,bad,raw=False)
    except (AssertionError,ValueError):pass
    else:raise AssertionError('finite exploratory tamper accepted')
    bad=copy.deepcopy(result);bad['leads'][0]['paired_differences']['CNN-20k minus N-last']['mean_raw']=float('nan')
    try:check(root,cases,bad,raw=False)
    except (AssertionError,ValueError):pass
    else:raise AssertionError('NaN exploratory tamper accepted')
    return dict(finite_tamper_rejected=True,NaN_rejected=True)
