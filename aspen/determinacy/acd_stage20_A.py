"""Original-panel all-lead scoring; saved outputs only, outcomes only in score()."""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', NUMBA_NUM_THREADS='2', JAX_PLATFORMS='cpu')
import argparse, hashlib, io, json, socket, sys, time
from pathlib import Path
import numpy as np

def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def score(args):
    if socket.gethostname() != 'sulaco': raise RuntimeError('Scoring requires sulaco CPU')
    sys.path.insert(0,str(args.science_root))
    from acd_stage6_analysis import binary, stack, RAW, LEADS
    from acd_stats import r0
    import numba
    numba.set_num_threads(2)
    output=args.output; output.mkdir(parents=True, exist_ok=True)
    frozen=json.loads((args.science_root/'receipts/acd_stage2.json').read_text())
    jbar=frozen['null']['jbar']; null=np.asarray(frozen['null']['question_probabilities'])[np.r_[np.arange(8),37]]
    # Hidden outcomes are read exclusively within this scoring function.
    actual=np.asarray([np.load(RAW/f'conf/score_{c:03d}.npz')['actual_cost'] for c in range(200)])
    truth=actual[:,:8]<actual[:,8,None]
    specifications=[('posterior',None)]+[(n,args.science_root/'runs/stage9/inference'/n) for n in ['CNN-F','CNN-noF']]
    specifications += [(f'{m}-seed{i}',args.science_root/'runs/stage9/inference'/f'{m}-seed{i}') for i in range(1,5) for m in ['CNN-F','CNN-noF']]
    specifications += [(f'CNN-F-{e}-{mode}-seed{i}',args.pipeline_root/'runs/stage18/inference'/f'CNN-F-{e}-{mode}-seed{i}') for e,mode in [('E0','fixed'),('E1','fixed'),('E1','rolling')] for i in range(1,6)]
    result=dict(post_hoc=True, panel='original confirmation', licenses_frozen_route=False,
                construction='Stage9 F5 binary and r0 functions unchanged; lead loop extends to every frozen lead. Invalid instances give no confident answers; errors retain all draws, never survivors.',
                error_weighting='equal-case RMSE: mean of per-case root mean squared errors; pooled RMSE: root mean over every saved draw/action squared error; bias: corresponding signed means',
                code_hashes={n:digest(args.science_root/n) for n in ['acd_stage6_analysis.py','acd_stats.py','acd_stage9_cnn_metrics.py']},
                adapter_sha256=digest(__file__),models={}, R_other=[])
    for name,directory in specifications:
        target=output/f'{name}.json'
        if target.exists(): result['models'][name]=json.loads(target.read_text()); continue
        begin=time.monotonic(); summaries=[]; kept=[]; invalid=[]; source_hashes={}; errors={g:[] for g in ['all_eight','seven']}
        for case in range(len(actual)):
            p=RAW/f'conf/case_{case:03d}.npz'
            with np.load(p) as d: physics=d['J'].copy(); kept.append(not bool(d['excluded']))
            if directory is None: J=physics; valid=True
            else:
                path=directory/f'{case:03d}.npz'; blob=path.read_bytes(); source_hashes[str(path)]=hashlib.sha256(blob).hexdigest()
                with np.load(io.BytesIO(blob)) as d: J=d['J'].copy(); valid=bool(d['valid'].all()) and bool(np.isfinite(J).all())
            if J.shape != physics.shape: raise RuntimeError(f'Unmatched draw/option/lead dimensions {name} {case}')
            s=binary(J,jbar,null)
            if not valid: s['confident'].fill(False); s['observation'].fill(False); invalid.append(case)
            summaries.append(s)
            err=(J[:,:8]-J[:,8,None])-(physics[:,:8]-physics[:,8,None])
            for g,sl in [('all_eight',slice(None)),('seven',slice(1,8))]:
                v=err[:,sl,:]
                errors[g].append(dict(n=v.shape[0]*v.shape[1],sum=v.sum(axis=(0,1)),square=(v*v).sum(axis=(0,1))))
        summary=stack(summaries); keep=np.asarray(kept); rows=[]
        for t,lead in enumerate(LEADS):
            for g,sl in [('all_eight',slice(None)),('seven',slice(1,8))]:
                conf=summary['confident'][:,:8,t][:,sl]; right=summary['modal'][:,:8,t][:,sl]==truth[:,:,t][:,sl]
                a=r0(conf[keep].sum(1),(conf&right)[keep].sum(1))
                valid_errors=[v for c,v in enumerate(errors[g]) if keep[c]]
                finite=all(np.isfinite(v['sum'][t]) and np.isfinite(v['square'][t]) for v in valid_errors)
                row=dict(lead=float(lead),population=g,confident_S_share=float(conf[keep].mean()),
                         accuracy=a,pooled_error=None if a['answer_accuracy'] is None else 1-a['answer_accuracy'],
                         case_error=None if a['case_accuracy'] is None else 1-a['case_accuracy'],
                         case_error_lower=1-a['case_upper'],case_error_upper=1-a['case_lower'],
                         equal_case_Dk_RMSE=float(np.mean([np.sqrt(v['square'][t]/v['n']) for v in valid_errors])) if finite else None,
                         equal_case_Dk_bias=float(np.mean([v['sum'][t]/v['n'] for v in valid_errors])) if finite else None,
                         pooled_Dk_RMSE=float(np.sqrt(sum(v['square'][t] for v in valid_errors)/sum(v['n'] for v in valid_errors))) if finite else None,
                         pooled_Dk_bias=float(sum(v['sum'][t] for v in valid_errors)/sum(v['n'] for v in valid_errors)) if finite else None)
                rows.append(row)
        refpaths=[args.science_root/'runs/stage16'/f'metrics_{name}.json', args.science_root/'runs/stage9'/f'metrics_{name}.json',args.pipeline_root/'runs/stage18'/f'metrics_{name}.json']
        reference=next((p for p in refpaths if p.exists()),None); checks=[]
        if reference:
            prior=json.loads(reference.read_text())
            for old in prior['confidence_readings']:
                new=next(r for r in rows if r['population']=='all_eight' and r['lead']==old['lead'])
                if new['accuracy']!=old['all_confident_accuracy'] or new['confident_S_share']!=old['confident_S_share']:
                    raise RuntimeError(f'Stage9 F5 reproduction mismatch {name} {old["lead"]}')
                checks.append(dict(lead=old['lead'],exact=True))
        else: raise RuntimeError('Missing prior metrics '+name)
        model=dict(rows=rows,matched_cases=int(keep.sum()),invalid_cases=invalid,source_hashes=source_hashes,
                   reference_metrics=str(reference),reference_sha256=digest(reference),reproduction_checks=checks,seconds=time.monotonic()-begin)
        target.write_text(json.dumps(model,indent=2,allow_nan=False)+'\n'); result['models'][name]=model
        print(json.dumps(dict(model=name,seconds=model['seconds'],completed_models=len(result['models']))),flush=True)
    (output/'acd_stage20_A.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    lines=['# Stage20 context retention diagnostics','','Post hoc on the original confirmation panel; licenses no frozen route.','','## A — saved-output error by lead','',result['construction'],'',result['error_weighting'],'','Case error bounds use the unchanged v2.3 one-sided case betting construction; cases with no confident answer do not contribute. The pooled error is descriptive. Every existing F5 confidence row reproduced exactly.','','| Model | Lead (LT) | Population | Confident share | Pooled error | Case error | Case bounds | Equal-case D RMSE | Equal-case D bias | Pooled D RMSE | Pooled D bias |','|---|---:|---|---:|---:|---:|---|---:|---:|---:|---:|']
    def fmt(x): return 'not evaluable' if x is None else f'{x:.8g}'
    for name,m in result['models'].items():
        for r in m['rows']:
            vals=[name,fmt(r['lead']),r['population'],fmt(r['confident_S_share']),fmt(r['pooled_error']),fmt(r['case_error']),f"[{fmt(r['case_error_lower'])}, {fmt(r['case_error_upper'])}]",*[fmt(r[k]) for k in ['equal_case_Dk_RMSE','equal_case_Dk_bias','pooled_Dk_RMSE','pooled_Dk_bias']]]
            lines.append('| '+' | '.join(vals)+' |')
    (output/'ACD_STAGE20_READING.md').write_text('\n'.join(lines)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--science-root',type=Path,required=True);p.add_argument('--pipeline-root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);score(p.parse_args())
