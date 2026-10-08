"""Original-panel E0 fixed/rolling scoring on Sulaco; hidden outcomes only in score()."""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',NUMBA_NUM_THREADS='2',JAX_PLATFORMS='cpu')
import argparse,hashlib,json,socket,sys
from pathlib import Path
import numpy as np

def score(args):
    if socket.gethostname()!='sulaco':raise RuntimeError('Requires sulaco scoring')
    sys.path.insert(0,str(args.science_root))
    import acd_stage9_cnn_metrics as inherited
    from acd_stage6_analysis import binary,stack,diff
    from acd_stats import r0,cp_bounds
    from acd_stage13_analysis import decision_rows,choices
    import numba
    numba.set_num_threads(2)
    out=args.outputs;inherited.DEST=out
    frozen=json.loads((args.science_root/'receipts/acd_stage2.json').read_text());jbar=frozen['null']['jbar'];null=np.asarray(frozen['null']['question_probabilities'])[np.r_[np.arange(8),37]]
    # This function alone reads realized original-panel outcomes.
    actual=np.asarray([np.load(inherited.RAW/f'conf/score_{c:03d}.npz')['actual_cost'] for c in range(200)])
    truth=actual[:,:8]<actual[:,8,None]
    with np.load(args.science_root/'runs/stage4b_null/null_0.16.npz') as d:sd=(d['J'][:,:8]-d['J'][:,8,None]).std(0,ddof=1)
    rows={};case_errors={};parity={}
    for mode in ['fixed','rolling']:
        for seed in range(1,6):
            name=f'CNN-F-E0-{mode}-seed{seed}';directory=out/'inference'/name;execution=json.loads((directory/'complete.json').read_text())
            inherited.run(name);metrics=json.loads((out/f'metrics_{name}.json').read_text());costs=[];valid=[];keep=[];summaries=[];forcing=[];physical=[];maximum=0.;changes=0
            for c in range(200):
                p=directory/f'{c:03d}.npz'
                if hashlib.sha256(p.read_bytes()).hexdigest()!=execution['output_hashes'][p.name]:raise RuntimeError('Output hash mismatch')
                with np.load(p) as d:J=d['J'].copy();v=bool(d['valid'].all()) and np.isfinite(J).all();probes=d['forcing_probes'].copy();steps=d['probe_steps'].copy()
                with np.load(inherited.RAW/f'conf/case_{c:03d}.npz') as d:keep.append(not bool(d['excluded']));physics=d['J'].copy()
                with np.load(args.inputs/f'{c:03d}.npz') as d:F=d['F'].copy()
                probes=probes.reshape(len(F),9,-1);forcing.append((probes,np.repeat(F[:,None],9,axis=1)));physical.append(physics);costs.append(J);valid.append(v)
                s=binary(J,jbar,null)
                if not v:s['confident'].fill(False);s['observation'].fill(False)
                summaries.append(s)
                if mode=='fixed':
                    with np.load(args.stage18/'runs/stage18/inference'/name/f'{c:03d}.npz') as d:prior=d['J'].copy()
                    maximum=max(maximum,float(np.max(np.abs(J-prior))));changes+=int(np.sum(binary(J,jbar,null)['confident']!=binary(prior,jbar,null)['confident']))
            keep=np.asarray(keep);summ=stack(summaries);readings=[];case_errors[name]={}
            for t in [3,5]:
                for population,sl in [('seven',slice(1,8)),('all_eight',slice(None))]:
                    conf=summ['confident'][:,:8,t][:,sl];right=summ['modal'][:,:8,t][:,sl]==truth[:,:,t][:,sl]
                    sizes=conf.sum(1);correct=(conf&right).sum(1);a=r0(sizes[keep],correct[keep]);obs=summ['observation'][:,:8,t][:,sl]
                    e=np.asarray([np.mean(conf[c]&~right[c])/np.mean(conf[c]) if sizes[c] else np.nan for c in range(len(keep))]);case_errors[name][str(t)]=e if population=='seven' else case_errors[name].get(str(t))
                    errors=[((J[:,:8,t]-J[:,8,None,t])-(P[:,:8,t]-P[:,8,None,t]))[:,sl] for J,P in zip(costs,physical)]
                    pooled=np.concatenate([errors[c].ravel() for c in np.flatnonzero(keep)]);finite=np.isfinite(pooled).all()
                    case_delta=[float((summ['p'][c,:8,t][sl]-right[c]).mean()) for c in np.flatnonzero(keep)]
                    readings.append(dict(lead=float(inherited.LEADS[t]),population=population,confident_share=float(conf[keep].mean()),observation_confident_share=float(obs[keep].mean()),accuracy=a,
                        pooled_error=None if a['answer_accuracy'] is None else 1-a['answer_accuracy'],case_error=None if a['case_accuracy'] is None else 1-a['case_accuracy'],error_bounds=[1-a['case_upper'],1-a['case_lower']],
                        equal_case_Dk_RMSE=float(np.mean([np.sqrt(np.mean(errors[c]**2)) for c in np.flatnonzero(keep)])) if finite else None,
                        equal_case_Dk_bias=float(np.mean([errors[c].mean() for c in np.flatnonzero(keep)])) if finite else None,
                        pooled_Dk_RMSE=float(np.sqrt(np.mean(pooled**2))) if finite else None,pooled_Dk_bias=float(pooled.mean()) if finite else None,
                        mean_calibration_test=diff(case_delta)))
            decisions,_=decision_rows(actual,costs,np.asarray(valid),keep,sd)
            for r in decisions:
                ch=choices(costs,np.asarray(valid),3 if r['lead']==2 else 5,sd)[r['policy']];count=int(np.sum((ch!=8)&keep));harm=r['harms'];r.update(actions_taken=count,conditional_harm_CP95=cp_bounds(harm,count) if count else [0.,1.],uniform_decrease_every_instance=bool(np.all(ch[keep]==0)))
            forcing_readings=[]
            for j,step in enumerate(steps):
                for pop,sl in [('seven',slice(1,8)),('all_eight',slice(None))]:
                    estimates=[v[0][:,sl,j].ravel() for c,v in enumerate(forcing) if keep[c]];targets=[v[1][:,sl].ravel() for c,v in enumerate(forcing) if keep[c]]
                    est=np.concatenate(estimates);tar=np.concatenate(targets);error=est-tar
                    forcing_readings.append(dict(step=int(step),population=pop,pooled_RMSE=float(np.sqrt(np.mean(error**2))),pooled_bias=float(error.mean()),equal_case_RMSE=float(np.mean([np.sqrt(np.mean((x-y)**2)) for x,y in zip(estimates,targets)])),equal_case_bias=float(np.mean([(x-y).mean() for x,y in zip(estimates,targets)])),correlation=float(np.corrcoef(est,tar)[0,1])))
            metrics.update(primary_seven_readings=readings,forcing_readings=forcing_readings,decisions=decisions)
            rows[name]=metrics
            if mode=='fixed':parity[name]=dict(max_absolute_cost_difference=maximum,confidence_classification_changes=changes)
    comparisons=[]
    for seed in range(1,6):
        for t in [3,5]:
            a=case_errors[f'CNN-F-E0-rolling-seed{seed}'][str(t)];b=case_errors[f'CNN-F-E0-fixed-seed{seed}'][str(t)];mask=np.isfinite(a)&np.isfinite(b)
            comparisons.append(dict(seed=seed,lead=float(inherited.LEADS[t]),cases=int(mask.sum()),rolling_minus_fixed=diff(a[mask]-b[mask]),population='seven zero-mean patterns; both arms give at least one confident answer; descriptive two-sided99% case betting interval'))
    result=dict(post_hoc=True,panel='original confirmation',licenses_frozen_route=False,models=rows,hardware_parity=parity,comparisons=comparisons,
        caveat='Uniform decrease can be absorbed by a re-estimated mean forcing while the action field is also supplied. Seven zero-mean patterns are primary; all-eight readings retain this caveat.',
        adapter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    args.receipt.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    lines=['','## C — E0 rolling versus E0 fixed','','Seven zero-mean patterns are primary. '+result['caveat'],'','| E0 seed | Lead (LT) | Rolling minus fixed case error | Descriptive 99% interval | Contributing cases |','|---|---:|---:|---|---:|']
    for r in comparisons:
        d=r['rolling_minus_fixed'];lines.append(f"| {r['seed']} | {r['lead']:g} | {d['point']} | [{d['lower']}, {d['upper']}] | {r['cases']} |")
    lines+=['','| Fixed pipeline | Maximum cost difference from Stage18 | Classification changes |','|---|---:|---:|']
    for n,r in parity.items():lines.append(f"| {n} | {r['max_absolute_cost_difference']} | {r['confidence_classification_changes']} |")
    args.reading.write_text(args.reading.read_text()+'\n'.join(lines)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--science-root',type=Path,required=True);p.add_argument('--stage18',type=Path,required=True);p.add_argument('--outputs',type=Path,required=True);p.add_argument('--inputs',type=Path,required=True);p.add_argument('--receipt',type=Path,required=True);p.add_argument('--reading',type=Path,required=True);score(p.parse_args())
