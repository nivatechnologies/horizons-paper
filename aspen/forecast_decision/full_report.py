"""Statistics coordinator's checked NUMBERS fragment and greyscale report."""
import argparse,copy,json
from pathlib import Path
import numpy as np
from protocol import ROOT,rng,write_json,digest
from metrics import aggregate,read_gates,license_ids,bootstrap_metrics,seed_witness_readings
from check_campaign import reject_nonfinite,equivalent
from figures import render,render_required


def sentence_check(gate,ids,stage,selected=None,repeats_ran=False):
    equivalent(ids,license_ids(gate,stage,selected=selected,repeats_ran=repeats_ran))
    if str(stage)=='1':assert not ids
    if 'S1' in ids or 'S2' in ids:
        assert any(s in ids for s in ['S10','S10b','S10c']), 'Mandatory decision-trained comparator reading absent'
        if repeats_ran:assert 'S1s' in ids
    if 'S2' in ids and gate['H1d']!='HOLDS':assert 'S7' in ids
    if 'S8+' in ids and gate['H1d']!='HOLDS':assert 'S7₂' in ids
    if 'S8' in ids and gate.get('H1e') is not None:assert 'S11' in ids
    return True


def check(rows,result,root=None,source_hashes=True):
    reject_nonfinite(rows);reject_nonfinite(result)
    expected_panel={'baseline':'test','2':'test','2b':'twoscale_test','secondary':'test2'}[result['stage']]
    if 'panel' in result:assert result['panel']==expected_panel,'stage/panel provenance mismatch'
    work_records=[]
    cases=rows['cases'];expected_count=100 if result['stage']=='secondary' else 200;assert len(cases)==expected_count;assert [r['case'] for r in cases]==list(range(expected_count))
    if root is not None and source_hashes:
        for source,expected in result['source_hashes'].items():assert digest(root/source)==expected,'source changed: '+source
    if root is not None:
        compute=result.get('compute_metadata')
        if compute is not None:
            paths=[p for p in result['source_hashes'] if p.endswith('/statistics_compute_metadata.json')]
            assert len(paths)==1;equivalent(compute,json.loads((root/paths[0]).read_text()))
            for name,receipt in compute['training'].items():
                if name!='CNN-20k':
                    hour_key='recorded_charged_phase_gpu_hours' if 'recorded_charged_phase_gpu_hours' in receipt else 'actual_charged_gpu_hours'
                    second_key='recorded_charged_phase_gpu_seconds' if 'recorded_charged_phase_gpu_seconds' in receipt else 'actual_charged_gpu_seconds'
                    equivalent(receipt[hour_key],receipt[second_key]/3600 if receipt[second_key] is not None else None)
                    if receipt.get('worker_terminal_status')=='EXTERNALLY_STOPPED':assert receipt['phase_measurement_is_lower_bound'] is True
                    if 'total_gpu_hours' in receipt:assert receipt['total_gpu_hours'] is None
        raw_panel=result.get('panel','twoscale_test' if result['stage']=='2b' else 'test')
        for name,expected in result.get('expected_checkpoint_hashes',{}).items():
            if name=='CNN-20k':equivalent(expected,digest(root/'inputs/CNN-20k.pt'))
            else:
                manifest=root/('runs/training/final_selection_stage2b.json' if result['stage']=='2b' else 'runs/training/final_selection_stage2.json')
                consumer=json.loads(manifest.read_text());assert consumer['status']=='FINAL';equivalent(expected,consumer['models'][name]['sha256'])
            for c in range(len(cases)):
                meta=root/f'runs/{raw_panel}/{name}_{c:03d}.json'
                equivalent(json.loads(meta.read_text())['checkpoint_sha256'],expected)
        for group,field in [('primary_learned_measured_seconds','primary_decision_timing'),('primary_optional_physics_measured_seconds','measured_primary_seconds')]:
            for name,record in result.get(group,{}).items():
                values=[]
                for c in range(len(cases)):
                    timing_panel='twoscale_val' if record.get('timing_panel')=='validation timing only' else raw_panel
                    meta=root/f'runs/{timing_panel}/{name}_{c:03d}.json'
                    if not meta.exists():continue
                    item=json.loads(meta.read_text());value=item.get(field,item.get('primary_timing') if field=='primary_decision_timing' else None)
                    if field=='primary_decision_timing':value=value.get('seconds') if value else None
                    if value is not None:values.append(value)
                equivalent(record['cases'],len(values));equivalent(record['mean'],float(np.mean(values)) if values else None)
        for name,record in result.get('primary_two_scale_physics_measured_seconds',{}).items():
            values=[]
            for c in range(16):
                path=root/f'runs/twoscale_val/primary_timing_{c:03d}.json'
                if not path.exists():continue
                item=json.loads(path.read_text())['timings'].get(name)
                if item and item.get('includes_cost_and_argmin'):values.append(item['seconds'])
            equivalent(record['cases'],len(values));equivalent(record['mean'],float(np.mean(values)) if values else None)
        if result.get('primary_Nlast_measured_seconds') is not None:
            values=[]
            for c in range(len(cases)):
                path=root/f'runs/{raw_panel}/work_timing_{c:03d}.json'
                if not path.exists():continue
                item=json.loads(path.read_text());work_records.append(np.asarray(item['R_W']))
                if item.get('primary_timing_includes_cost_and_argmin') and item.get('measured_primary_Nlast_seconds') is not None:values.append(item['measured_primary_Nlast_seconds'])
            equivalent(result['primary_Nlast_measured_seconds']['cases'],len(values));equivalent(result['primary_Nlast_measured_seconds']['mean'],float(np.mean(values)) if values else None)
    if root is not None:
        from protocol import WINDOWS
        raw_panel=result.get('panel','twoscale_test' if result['stage']=='2b' else 'test')
        for row in cases:
            with np.load(root/f'runs/{raw_panel}/cpu_{row["case"]:03d}.npz') as raw:
                if result['stage']=='2b':
                    num=raw['work_numerator'].mean(1);den=raw['work_denominator'].mean(1);assert np.all(den!=0);work_records.append(num/den)
                physics='N2' if result['stage']=='2b' else 'N-last'
                equivalent(row['null_choices']['myopic'],int(raw[physics+'_cost'][:,:,0].mean(1).argmin()))
                for e in row['leads']:
                    truth=raw['truth_cost'][:8,:,e['h']];b=int(truth[:,:1024].mean(1).argmin())
                    differences=truth[:,1024:]-truth[b,1024:]
                    low=differences.mean(1)-2.983*differences.std(1,ddof=1)/np.sqrt(1024)
                    equivalent(e['b'],b);equivalent(e['eligible'],bool(np.all(np.delete(low,b)>0)))
                    for name,arm in e['arms'].items():
                        assert np.allclose(arm['J'],truth.mean(1),rtol=1e-10,atol=1e-12)
                        equivalent(arm['J0'],float(raw['truth_cost'][8,:,e['h']].mean()))
                        if arm['failed']:
                            equivalent(arm['regret_raw'],float(np.ptp(truth.mean(1))))
                            if not name.endswith('-cost'):equivalent(arm['wACC'],0.)
                            assert not arm['correct']
                        else:
                            equivalent(arm['chosen'],int(np.argmin(arm['cost'])))
                            equivalent(arm['regret_raw'],float(truth.mean(1)[arm['chosen']]-truth.mean(1).min()))
                        if not arm['failed'] and name in ['N-last','N-oracle','N2','N2-offline','N2-noclosure']:
                            w=WINDOWS[e['h']];mean=raw[name+'_mean'][:8,w];variance=raw[name+'_var'][:8,w]
                            energy=((mean**2).sum(-1)+variance).mean(-1)/(2*mean.shape[-1])
                            assert np.allclose(energy,arm['cost'],rtol=1e-10,atol=1e-12),'raw state-energy identity mismatch'
    for j,panel in enumerate(result['leads']):
        entries=[r['leads'][j] for r in cases];assert all(e['T']==panel['T'] for e in entries)
        equivalent(panel['best_action_frequency'],[sum(e['b']==k for e in entries)/len(entries) for k in range(8)])
        equivalent(panel['best_differs_from_fixed'],sum(not e['fixed_correct'] for e in entries)/len(entries))
        if 'injected_work' in panel and root is not None:
            from metrics import spearman
            rw=np.mean([v[:,entries[0]['h']] for v in work_records],axis=0)
            Jmean=np.mean([e['arms'][result['arms'][0]]['J'] for e in entries],axis=0)
            equivalent(panel['injected_work'],dict(cases=len(work_records),per_action=rw.tolist(),overall=float(rw.mean()),work_truth_cost_rank_correlation=spearman(rw,Jmean)))
        for name in panel['metrics']:
            stored=panel['metrics'][name];expected=aggregate(entries,name);equivalent(stored,expected)
            vals=[e['arms'][name]['historical_case_range_realized_regret'] for e in entries]
            equivalent(stored['historical_case_range_realized_regret'],float(np.mean(vals)) if all(v is not None for v in vals) else None)
            # Independently check sum-before-square-root response aggregate.
            for subset in ['eligible','all']:
                selected=[e for e in entries if subset=='all' or e['eligible']]
                usable=[e['arms'][name] for e in selected if not e['arms'][name]['failed']]
                for prefix in ['MSRE','VRE']:
                    finite_rows=[a for a in usable if a.get(prefix+'_den') is not None and a.get(prefix+'_num') is not None]
                    numerator=sum(a[prefix+'_num'] for a in finite_rows);denominator=sum(a[prefix+'_den'] for a in finite_rows)
                    val=float(np.sqrt(numerator/denominator)) if denominator>0 else None
                    equivalent(stored[subset][prefix],val)
                split=stored[subset].get('cost_difference_split')
                if split:equivalent(split['total_MSE'],split['mean_part_MSE']+split['spread_part_MSE']+split['cross_MSE'])
            if 'bootstrap' in stored:
                samples=rng('afd2-bootstrap' if result['stage']=='2b' else 'afd-bootstrap',3,case=200 if result['stage']=='secondary' else 0,member=j+100).integers(len(cases),size=(2000,len(cases)))
                equivalent(stored['bootstrap'],bootstrap_metrics(entries,name,samples))
        if 'null_metrics' in panel:
            J=np.array([e['arms'][result['arms'][0]]['J'] for e in entries]);J0=np.array([e['arms'][result['arms'][0]]['J0'] for e in entries]);scale=float(np.median(np.ptp(J,axis=1)))
            for null,nm in panel['null_metrics'].items():
                choices=None if null=='random' else np.array([r['null_choices'][null] for r in cases])
                costs=J.mean(1) if choices is None else J[np.arange(len(cases)),choices]
                correct=np.full(len(cases),1/8) if choices is None else choices==np.array([e['b'] for e in entries])
                for subset in ['eligible','all']:
                    m=np.array([e['eligible'] for e in entries]) if subset=='eligible' else np.ones(len(cases),bool)
                    raw=float(np.mean((costs-J.min(1))[m])) if m.any() else None;den=float(np.sum((J0-J.min(1))[m]))
                    expected=dict(cases=int(m.sum()),P=float(np.mean(correct[m])) if m.any() else None,regret_raw=raw,regret=raw/scale if raw is not None and scale>0 else None,B=float(np.sum((J0-costs)[m])/den) if den>0 else None,energy_saved=float(np.mean((J0-costs)[m])) if m.any() else None)
                    expected['action_frequency']=[1/8]*8 if choices is None else [float(np.mean(choices[m]==k)) if m.any() else None for k in range(8)]
                    equivalent(nm[subset],expected)
                if 'bootstrap' in nm:
                    from metrics import bounds
                    draws=rng('afd2-bootstrap' if result['stage']=='2b' else 'afd-bootstrap',3,case=200 if result['stage']=='secondary' else 0,member=j+100).integers(len(cases),size=(2000,len(cases)))
                    resampled_scale=np.median(np.ptp(J,axis=1)[draws],axis=1)
                    for subset in ['eligible','all']:
                        mask=np.array([e['eligible'] for e in entries]) if subset=='eligible' else np.ones(len(cases),bool)
                        selected=mask[draws];count=selected.sum(1)
                        def sums(value):return np.where(selected,value[draws],0.).sum(1)
                        with np.errstate(divide='ignore',invalid='ignore'):
                            regret=sums(costs-J.min(1))/count;den=sums(J0-J.min(1));saved=sums(J0-costs);B=saved/den;B[den<=0]=np.nan
                            expected={key:bounds(value) for key,value in dict(P=sums(correct)/count,regret_raw=regret,regret=regret/resampled_scale,B=B,energy_saved=saved/count).items()}
                        equivalent(nm['bootstrap'][subset],expected)
        if 'gate' in panel:
            gate=panel['gate']
            from protocol import ORDER,ORDER2
            two=result['stage']=='2b';order=ORDER2 if two else ORDER
            S=[name for name in order if name in panel['metrics']];Rep=[name for name in (['CNN2-roll','CNN2-R2'] if two else ['CNN-80k','CNN-roll','CNN-R2']) if name in panel['metrics']]
            samples=rng('afd2-bootstrap' if two else 'afd-bootstrap',3,case=200 if result['stage']=='secondary' else 0,member=j+100).integers(len(cases),size=(2000,len(cases)))
            expected=read_gates(entries,S,Rep,samples,selected=result.get('selected'),two_scale=two)
            if not two:expected.update(seed_witness_readings(entries,expected,S,samples))
            expected['licensed_sentences']=license_ids(expected,result['stage'],selected=result.get('selected'),repeats_ran=all(a in result['arms'] for a in ['CNN-20k-s2','CNN-20k-s3']))
            equivalent(gate,expected)
            sentence_check(gate,gate['licensed_sentences'],result['stage'],result.get('selected'),repeats_ran=all(a in result['arms'] for a in ['CNN-20k-s2','CNN-20k-s3']))
    equivalent(result['primary'],next(p for p in result['leads'] if p['T']==2))
    if result['stage'] in ['baseline','secondary']:assert result['licensed_sentences']==[]
    return dict(status='PASS',cases=len(cases),leads=len(result['leads']),allcase_and_eligible_checked=True,bootstrap_checked=all('bootstrap' in m for p in result['leads'] for m in p['metrics'].values()),source_hashes_checked=root is not None and source_hashes,raw_truth_eligibility_and_cost_checked=root is not None)


def fragment_name(stage):return 'NUMBERS_FULL_METRICS_'+{'baseline':'BASELINE','2':'STAGE2','2b':'STAGE2B','secondary':'SECONDARY'}.get(stage,stage.upper())+'.md'


def report(result):
    def v(x):return 'unavailable' if x is None else f'{x:.6g}'
    lines=['# Aspen full descriptive metrics','',f"Statistics stage: {result['stage']}. Source: {fragment_name(result['stage'])} checked JSON record.",'',
           '| Lead (LT) | Arm | Eligible P | All-case P | wACC | wRMSE | MSRE | VRE | All-case regret | B |',
           '|---|---|---|---|---|---|---|---|---|---|']
    for p in result['leads']:
        for name,m in p['metrics'].items():
            e=m['eligible'];a=m['all'];lines.append('| '+' | '.join([v(p['T']),name]+[v(x) for x in [e['P'],a['P'],e['wACC'],e['wRMSE'],e['MSRE'],e['VRE'],a['regret'],a['B']]])+' |')
    lines+=['','Failed cases have wrong top-1, worst regret and ACC zero; excluded metrics carry counts in the checked record. Response metrics are ratios of sums, with paired case bootstrap.','',
            'Realized regret is reported in raw energy, as the panel median range counterpart, and as the historical per-case range descriptive ratio. No new threshold uses these descriptive ratios.','',
            'Complete cost mean/spread decomposition, all-case counterparts, action use, work and bootstrap intervals are in the named NUMBERS fragment.','']
    if result['stage'] in ['baseline','secondary']:lines+=['This descriptive baseline report licenses no headline sentence.','']
    return '\n'.join(lines)


def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--stage',default='baseline');p.add_argument('--figures',action='store_true');a=p.parse_args()
    cases_path=a.root/f'runs/{a.stage}_metrics_cases.json';result_path=a.root/f'runs/{a.stage}_metrics.json'
    rows=json.loads(cases_path.read_text());result=json.loads(result_path.read_text());checked=check(rows,result,a.root)
    bad=copy.deepcopy(result);bad['primary']['metrics'][result['arms'][0]]['eligible']['P']+=.01
    try:check(rows,bad,source_hashes=False)
    except (ValueError,AssertionError):pass
    else:raise AssertionError('finite tamper accepted')
    bad=copy.deepcopy(result);bad['primary']['metrics'][result['arms'][0]]['eligible']['P']=float('nan')
    try:check(rows,bad,source_hashes=False)
    except (ValueError,AssertionError):pass
    else:raise AssertionError('NaN tamper accepted')
    checked.update(tamper_rejected=True,NaN_rejected=True)
    if result['stage']=='2':checked.update(final_abstract_sentence_set='OPEN pending combined Stage2b scope check',final_sentence_set_closed=False)
    write_json(a.root/f'runs/{a.stage}_metrics_checker.json',checked)
    fragment='# NUMBERS full metrics\n\nChecked measured descriptions; this file is a NUMBERS fragment for campaign registration.\n\n```json\n'+json.dumps(result,indent=2,allow_nan=False)+'\n```\n\nChecker: '+json.dumps(checked,sort_keys=True)+'\n'
    fragment+='\n| Artifact | SHA256 |\n|---|---|\n'
    for path in [cases_path,result_path,a.root/f'runs/{a.stage}_metrics_checker.json']:fragment+=f'| {path.relative_to(a.root)} | {digest(path)} |\n'
    (a.root/fragment_name(result['stage'])).write_text(fragment);(a.root/f'AFD_{a.stage.upper()}_FULL_METRICS.md').write_text(report(result))
    if a.figures:
        paths=render(result['leads'],a.root/f'runs/figures/{a.stage}')+render_required(result['leads'],a.root/f'runs/figures/{a.stage}',selected=result.get('selected'),two_scale=result['stage']=='2b');write_json(a.root/f'runs/{a.stage}_figure_artifacts.json',{str(Path(p).relative_to(a.root)):digest(p) for p in paths})
    if result['stage'] in ['2','2b']:
        from result_note import stage2_note,licensed_text
        write_json(a.root/f'runs/{a.stage}_licensed_sentences.json',dict(sentences=licensed_text(result),source=str(result_path.relative_to(a.root))))
        (a.root/f'AFD_STAGE{a.stage.upper()}_READING.md').write_text(stage2_note(result,checked))
    print(json.dumps(checked))
if __name__=='__main__':main()
