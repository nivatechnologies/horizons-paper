"""Statistics-coordinator adapter. No training, checkpoint or L* selection.

Opens only requested test arrays and already-fixed case rows. Explicit test
access authorization is required. Baseline mode never opens Stage-1 reading.
"""
import argparse,copy,datetime,json,shutil
from pathlib import Path
import numpy as np
from protocol import ROOT,LEADS,WINDOWS,LT,SIGMA,rng,digest,write_json,ORDER,ORDER2
from metrics import aggregate,enrich_state_entry,read_gates,license_ids,bootstrap_metrics,seed_witness_readings
from check_campaign import reject_nonfinite


def assemble(root,case_path,names,authorization,stage='baseline',selected=None,two_scale=False,intervals=False):
    if not authorization:raise ValueError('explicit coordinator test-access authorization required')
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    log=root/'runs/statistics_access.jsonl';log.parent.mkdir(parents=True,exist_ok=True)
    with log.open('a') as f:f.write(json.dumps(dict(at=now,authorized_at=authorization,role='statistics coordinator only',case_rows=str(case_path),arms=names,stage=stage))+'\n')
    if stage not in ['baseline','2','2b']:raise ValueError('unsupported statistics stage')
    rows=copy.deepcopy(json.loads(case_path.read_text())['cases'])
    climate=np.load(root/'inputs/climatology.npy');sigma=SIGMA
    if two_scale:raise NotImplementedError('two-scale raw schema requires explicit sigma/climatology paths before access')
    fixed_set={e['b'] for r in rows for e in r['leads'] if e['fixed_correct']}
    if len(fixed_set)!=1:raise ValueError('cannot recover single already-selected fixed action from stored case rows')
    fixed_action=next(iter(fixed_set))
    work=[];timing=[];learned_timing={name:[] for name in names if name.startswith('CNN')};optional_physics_timing={};sources={str(case_path.relative_to(root)):digest(case_path)}
    for name in ['assemble_metrics.py','metrics.py','full_report.py','protocol.py']:
        sha=digest(root/name);snapshot=root/'runs/statistics_sources'/sha/name;snapshot.parent.mkdir(parents=True,exist_ok=True)
        if not snapshot.exists():shutil.copyfile(root/name,snapshot)
        sources[str(snapshot.relative_to(root))]=sha
    sources['inputs/climatology.npy']=digest(root/'inputs/climatology.npy')
    for row in rows:
        c=row['case'];path=root/f'runs/test/cpu_{c:03d}.npz'
        with np.load(path) as loaded:cpu={k:loaded[k] for k in loaded.files}
        sources[str(path.relative_to(root))]=digest(path);cpu['climatology']=climate
        row['null_choices']=dict(myopic=int(cpu['N-last_cost'][:,:,0].mean(1).argmin()),fixed=fixed_action)
        networks={}
        for name in names:
            if name.startswith('CNN') or (root/f'runs/test/{name}_{c:03d}.npz').exists():
                p=root/f'runs/test/{name}_{c:03d}.npz'
                with np.load(p) as loaded:networks[name]={k:loaded[k] for k in loaded.files}
                sources[str(p.relative_to(root))]=digest(p)
                meta_path=p.with_suffix('.json')
                if meta_path.exists():
                    meta=json.loads(meta_path.read_text());pt=meta.get('primary_decision_timing')
                    if meta.get('primary_timing_includes_identification_fit_cost_and_argmin') and meta.get('measured_primary_seconds') is not None:
                        optional_physics_timing.setdefault(name,[]).append(meta['measured_primary_seconds']);sources[str(meta_path.relative_to(root))]=digest(meta_path)
                    if pt is not None:
                        learned_timing.setdefault(name,[]).append(pt['seconds']);sources[str(meta_path.relative_to(root))]=digest(meta_path)
        for entry in row['leads']:
            h=entry['h'];w=WINDOWS[h];point=int(np.argmin(np.abs(np.arange(cpu['actual'].shape[1])*.05-entry['T']*LT)))
            truth=cpu['truth_cost'][:8,:,h].mean(1)
            if not np.allclose(truth,entry['arms']['N-last']['J'],rtol=1e-10,atol=1e-12):raise ValueError('stored cases mismatch raw truth')
            active=[name for name in names if not name.endswith('-cost') or entry['T']==2]
            for name in active:
                net=networks.get(name)
                if name not in entry['arms']:
                    if net is None:
                        cost=cpu[name+'_cost'][:,:,h].mean(1);dropped=0;failed=False
                    else:
                        keep=net['survivors'] if name.endswith('-cost') else net['survivors'][h]
                        dropped=int((~keep).sum());failed=dropped>32;cost=net['cost'] if name.endswith('-cost') else net['cost'][h]
                    chosen=-1 if failed else int(cost.argmin())
                    entry['arms'][name]=dict(chosen=chosen,correct=not failed and chosen==entry['b'],failed=failed,dropped=dropped,cost=cost.tolist(),J=truth.tolist(),J0=float(cpu['truth_cost'][8,:,h].mean()),regret_raw=float(np.ptp(truth)) if failed else float(truth[chosen]-truth.min()))
                if name.endswith('-cost'):
                    arm=entry['arms'][name];arm.update(wACC=None,wRMSE=None,pointACC=None,MSRE_num=None,MSRE_den=None,VRE_num=None,VRE_den=None,cost_difference_split=None)
                    realized=cpu['actual_cost'][:8,h];arm['realized_regret_raw']=float(np.ptp(realized)) if arm['failed'] else float(realized[arm['chosen']]-realized.min());arm['realized_cost_range']=float(np.ptp(realized))
                else:enrich_state_entry(entry,name,cpu,net,w,point,sigma)
            entry['arms']={name:entry['arms'][name] for name in active}
        wp=root/f'runs/test/work_timing_{c:03d}.json'
        if wp.exists():
            item=json.loads(wp.read_text());work.append(item);sources[str(wp.relative_to(root))]=digest(wp)
            if item.get('primary_timing_includes_cost_and_argmin') and item.get('measured_primary_Nlast_seconds') is not None:timing.append(item['measured_primary_Nlast_seconds'])
        if (c+1)%25==0:print('enriched',c+1,flush=True)
    panels=[]
    for j,T in enumerate(LEADS[1:]):
        entries=[r['leads'][j] for r in rows]
        actual_scale=float(np.median([e['arms'][names[0]]['realized_cost_range'] for e in entries]))
        for e in entries:
            for arm in e['arms'].values():
                arm['realized_regret']=arm['realized_regret_raw']/actual_scale if actual_scale>0 else None
                den=arm['realized_cost_range'];arm['historical_case_range_realized_regret']=arm['realized_regret_raw']/den if den>0 else None
        active=list(entries[0]['arms']);models={name:aggregate(entries,name) for name in active}
        samples=rng('afd-bootstrap',3,member=j+100).integers(len(entries),size=(2000,len(entries)))
        if intervals:
            for name in active:models[name]['bootstrap']=bootstrap_metrics(entries,name,samples)
        nulls={}
        J=np.asarray([e['arms'][names[0]]['J'] for e in entries]);J0=np.asarray([e['arms'][names[0]]['J0'] for e in entries]);mask=np.array([e['eligible'] for e in entries]);scale=float(np.median(np.ptp(J,axis=1)))
        for null in ['random','myopic','fixed']:
            choices=None if null=='random' else np.array([r['null_choices'][null] for r in rows])
            cost=J.mean(1) if choices is None else J[np.arange(len(rows)),choices]
            correct=np.full(len(rows),1/8) if choices is None else choices==np.array([e['b'] for e in entries])
            nulls[null]={}
            for subset,m in [('eligible',mask),('all',np.ones(len(rows),bool))]:
                den=float(np.sum((J0-J.min(1))[m]));raw=float(np.mean((cost-J.min(1))[m])) if m.any() else None
                nulls[null][subset]=dict(cases=int(m.sum()),P=float(np.mean(correct[m])) if m.any() else None,regret_raw=raw,regret=raw/scale if raw is not None and scale>0 else None,B=float(np.sum((J0-cost)[m])/den) if den>0 else None,energy_saved=float(np.mean((J0-cost)[m])) if m.any() else None,action_frequency=[1/8]*8 if choices is None else [float(np.mean(choices[m]==k)) if m.any() else None for k in range(8)])
        if intervals:
            from metrics import bounds
            sampled_scale=np.median(np.ptp(J,axis=1)[samples],axis=1)
            for null in nulls:
                choices=None if null=='random' else np.array([r['null_choices'][null] for r in rows])
                costs=J.mean(1) if choices is None else J[np.arange(len(rows)),choices]
                correct=np.full(len(rows),1/8) if choices is None else choices==np.array([e['b'] for e in entries])
                nulls[null]['bootstrap']={}
                for subset,m in [('eligible',mask),('all',np.ones(len(rows),bool))]:
                    sm=m[samples];count=sm.sum(1)
                    def sums(a):return np.where(sm,a[samples],0.).sum(1)
                    with np.errstate(divide='ignore',invalid='ignore'):
                        raw=sums(costs-J.min(1))/count;den=sums(J0-J.min(1));saved=sums(J0-costs)
                        benefit=saved/den;benefit[den<=0]=np.nan
                        nulls[null]['bootstrap'][subset]={k:bounds(v) for k,v in dict(P=sums(correct)/count,regret_raw=raw,regret=raw/sampled_scale,B=benefit,energy_saved=saved/count).items()}
        panel=dict(T=float(T),metrics=models,null_metrics=nulls,fixed_action=fixed_action,realized_panel_median_range=actual_scale,
                   best_action_frequency=[sum(e['b']==k for e in entries)/len(entries) for k in range(8)],
                   best_differs_from_fixed=sum(not e['fixed_correct'] for e in entries)/len(entries))
        for name in active:
            vals=[e['arms'][name]['historical_case_range_realized_regret'] for e in entries]
            panel['metrics'][name]['historical_case_range_realized_regret']=float(np.mean(vals)) if all(v is not None for v in vals) else None
        if work:
            h=entries[0]['h'];rw=np.mean([np.array(v['R_W'])[:,h] for v in work],axis=0)
            from metrics import spearman
            panel['injected_work']=dict(cases=len(work),per_action=rw.tolist(),overall=float(rw.mean()),work_truth_cost_rank_correlation=spearman(rw,np.mean([e['arms'][names[0]]['J'] for e in entries],axis=0)))
        if stage!='baseline' and T==2:
            S=[n for n in ORDER if n in active];Rep=[n for n in ['CNN-80k','CNN-roll','CNN-R2'] if n in active]
            gate=read_gates(entries,S,Rep,samples,selected=selected)
            gate.update(seed_witness_readings(entries,gate,S,samples))
            gate['licensed_sentences']=license_ids(gate,stage,selected=selected,repeats_ran=all(a in names for a in ['CNN-20k-s2','CNN-20k-s3']))
            panel['gate']=gate
        panels.append(panel);print('aggregated lead',T,flush=True)
    public_compute=root/'runs/statistics_compute_metadata.json';compute_metadata=None
    if public_compute.exists():
        compute_metadata=json.loads(public_compute.read_text());sha=digest(public_compute)
        snapshot=root/'runs/statistics_sources'/sha/public_compute.name;snapshot.parent.mkdir(parents=True,exist_ok=True)
        if not snapshot.exists():shutil.copyfile(public_compute,snapshot)
        sources[str(snapshot.relative_to(root))]=sha
    output=dict(stage=stage,selected=selected,role='statistics coordinator',test_access_authorization=authorization,created_at=now,arms=names,source_hashes=sources,
                leads=panels,primary=next(p for p in panels if p['T']==2),primary_Nlast_measured_seconds=dict(cases=len(timing),mean=float(np.mean(timing)) if timing else None),
                compute_metadata=compute_metadata,
                primary_optional_physics_measured_seconds={name:dict(cases=len(values),mean=float(np.mean(values)) if values else None,includes='identification, fit if applicable, integration, drop, cost and argmin') for name,values in optional_physics_timing.items()},
                primary_learned_measured_seconds={name:dict(cases=len(values),mean=float(np.mean(values)) if values else None,checkpoint_load_excluded=True) for name,values in learned_timing.items()},
                realized_normalization='raw energy; panel median realized action range counterpart; historical per-case realized action range descriptive ratio',
                licensed_sentences=[] if stage=='baseline' else next(p for p in panels if p['T']==2)['gate']['licensed_sentences'])
    reject_nonfinite(output)
    return rows,output


def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--cases',type=Path);p.add_argument('--arms',nargs='+',default=['N-last','N-oracle','CNN-20k']);p.add_argument('--authorization',required=True);p.add_argument('--stage',default='baseline');p.add_argument('--selected');p.add_argument('--intervals',action='store_true');a=p.parse_args()
    rows,result=assemble(a.root,a.cases or a.root/'runs/stage1_cases.json',a.arms,a.authorization,a.stage,a.selected,intervals=a.intervals)
    write_json(a.root/f'runs/{a.stage}_metrics_cases.json',dict(cases=rows));write_json(a.root/f'runs/{a.stage}_metrics.json',result)
    print('assembled metrics',a.stage,flush=True)
if __name__=='__main__':main()
