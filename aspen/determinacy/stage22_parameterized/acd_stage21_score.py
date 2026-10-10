"""Stage21 scoring: the sole opener of hidden histories and realized costs."""
import os
os.environ.update(JAX_PLATFORMS='cpu',JAX_ENABLE_X64='true',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',NUMBA_NUM_THREADS='4')
import json,time
import numpy as np
from acd_protocol import ROOT,LEADS,WINDOWS,PATTERNS,physics
from acd_stage21_contract import OUT,SIGMA,assignments,digest
from acd_stage21_freeze_e import ready
from acd_stage6_analysis import binary,stack,loss,calibration
from acd_stage19_l3_statistic import pair_statistic
from acd_stage19_part3b_score import seed_average
from acd_stage19_learned import metrics
from acd_stats import difference_interval

def all_pattern_pair(fixed, rolling, truth, tick):
    masks=[s['confident'][:,:8,tick] for s in (fixed,rolling)]
    wrong=[s['modal'][:,:8,tick]!=truth[:,:8,tick] for s in (fixed,rolling)]
    counts=[m.sum(1) for m in masks]
    defined=(counts[0]>0)&(counts[1]>0)
    rates=[np.divide((m&w).sum(1),n,out=np.zeros(len(n)),where=n>0) for m,w,n in zip(masks,wrong,counts)]
    values=rates[1]-rates[0]
    return dict(case_differences=[float(v) if ok else None for v,ok in zip(values,defined)],contributing_cases=int(defined.sum()),interval=difference_interval(values[defined]) if defined.any() else None)

def pattern_group_rows(costs, physical, summary, truth, keep, leads):
    from acd_stats import r0
    rows=[]
    for t,lead in enumerate(leads):
        for group,sl in [('uniform_decrease',slice(0,1)),('seven_zero_mean',slice(1,8))]:
            conf=summary['confident'][:,sl,t];right=summary['modal'][:,sl,t]==truth[:,sl,t]
            accuracy=r0(conf[keep].sum(1),(conf&right)[keep].sum(1))
            errors=[((j[:,:8]-j[:,8,None])-(p[:,:8]-p[:,8,None]))[:,sl,t].ravel() for j,p,k in zip(costs,physical,keep) if k]
            finite=all(np.isfinite(x).all() for x in errors)
            pooled=np.concatenate(errors) if errors and finite else None
            rows.append(dict(lead=float(lead),population=group,confident_share=float(conf[keep].mean()),share_wrong=None if accuracy['answer_accuracy'] is None else 1-accuracy['answer_accuracy'],accuracy=accuracy,equal_case_Dk_bias=float(np.mean([x.mean() for x in errors])) if pooled is not None else None,pooled_Dk_bias=float(pooled.mean()) if pooled is not None else None,equal_case_Dk_RMSE=float(np.mean([np.sqrt(np.mean(x*x)) for x in errors])) if pooled is not None else None,pooled_Dk_RMSE=float(np.sqrt(np.mean(pooled*pooled))) if pooled is not None else None,invalid_errors=not finite))
    return rows

def score_actual():
 ready();directory=OUT/'scoring';directory.mkdir(exist_ok=True);path=directory/'actual.npz'
 if path.exists():
  with np.load(path) as z:return z['actual'].copy(),z['factual'].copy()
 actual=[];factual=[]
 for c,f in enumerate(assignments()):
  hidden=OUT/'hidden'/f'input_{c:03d}.npz'
  with np.load(hidden) as z:x=z['true'][-1].copy()
  with (directory/'access.jsonl').open('a') as log:log.write(json.dumps(dict(case=c,caller=__file__,path=str(hidden.relative_to(ROOT)),sha256=digest(hidden),utc=time.time()))+'\n')
  trajectory=physics.simulate(np.repeat(x[None],9,0),f+.16*PATTERNS,.01)
  actual.append(physics.costs(trajectory));factual.append(trajectory[8])
 tmp=path.with_suffix('.tmp.npz');np.savez_compressed(tmp,actual=np.array(actual),factual=np.array(factual));tmp.replace(path)
 return np.array(actual),np.array(factual)

def clean(x):
 if isinstance(x,dict):return {k:clean(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return [clean(v) for v in x]
 if isinstance(x,(float,np.floating)) and not np.isfinite(x):return None
 return x

def score():
 frozen=ready();actual,factual=score_actual();levels=assignments();climates={};physical=[];posterior_means=[];keep=[];fstdev=[];post_f=[]
 for f in [7,9]:
  with np.load(OUT/'climatology'/f'F{f}.npz') as z:
   j=z['J'].copy();climates[f]=dict(jbar=float(z['jbar']),null=z['prob'].copy(),sd=(j[:,:8]-j[:,8,None]).std(0,ddof=1),mean=z['states'].mean(0))
 for c in range(N):
  with np.load(OUT/f'main_forecast_{c:03d}.npz') as z:
   physical.append(z['J'].copy());posterior_means.append(z['factual_mean'].copy());keep.append(not bool(z['excluded']));post_f.append(z['theta'][:,40].copy());fstdev.append(float(post_f[-1].std(ddof=1)))
 keep=np.array(keep);summaries={};results={};missing=[]
 import acd_stage19_learned as inherited
 inherited.SIGMA=SIGMA
 original_endpoint=inherited.endpoint_fixed
 def safe_endpoint(summary,keep_mask,eligible):
  if np.any(eligible[keep_mask]):return original_endpoint(summary,keep_mask,eligible)
  return dict(pairs=0,cases=0,counts=dict(earlier=0,later=0,same=0),case_averaged=dict(earlier=None,later=None,same=None),pooled=dict(earlier=None,later=None,same=None),interval=difference_interval([]),records=[])
 inherited.endpoint_fixed=safe_endpoint
 def inputs(name):
  costs=[];means=[];valid=[];summary=[]
  if name!='posterior':
   from acd_stage21_inference import complete
   if not complete(name):return None
  for c,f in enumerate(levels):
   if name=='posterior':j=physical[c];m=posterior_means[c];v=np.isfinite(j).all()
   else:
    with np.load(OUT/'inference'/name/f'{c:03d}.npz') as z:j=z['J'].copy();m=z['factual_mean'].copy();v=bool(z['valid'].all()) and np.isfinite(j).all()
    assert j.shape==physical[c].shape
   s=binary(j,climates[f]['jbar'],climates[f]['null'])
   if not v or not keep[c]:s['confident'].fill(False);s['observation'].fill(False)
   costs.append(j);means.append(m);valid.append(v);summary.append(s)
  return costs,np.array(means),np.array(valid),stack(summary),physical
 p=inputs('posterior');summaries['posterior']=p[3]
 fixed=p[3]['observation'][:,:8,0]&p[3]['confident'][:,8,0,None]
 names=['posterior']+[r['name'] for r in frozen['tasks']]
 for name in names:
  data=p if name=='posterior' else inputs(name)
  if data is None:missing.append(name);continue
  summaries[name]=data[3];arms={}
  for label,selection in [('pooled',keep),('F7',keep&(levels==7)),('F9',keep&(levels==9))]:
   ids=np.flatnonzero(selection)
   if not len(ids):arms[label]=dict(cases=0,evaluable=False);continue
   costs=[data[0][i] for i in ids];means=data[1][ids];valid=data[2][ids];s={k:v[ids] for k,v in data[3].items()};phys=[physical[i] for i in ids]
   jbar=np.array([climates[levels[i]]['jbar'] for i in ids])[:,None]
   climate=np.array([climates[levels[i]]['mean'] for i in ids])[:,None,:]
   # Reported decisions are E and C(delta=0), whose gates do not depend on sd.
   row=metrics(name,costs,means,valid,s,phys,actual[ids],factual[ids],jbar,climate,climates[7]['sd'],fixed[ids])
   group_truth=np.concatenate([actual[ids,:8]<actual[ids,8,None],(actual[ids,8]>jbar)[:,None]],1)
   row['pattern_group_readings']=pattern_group_rows(costs,phys,s,group_truth,np.ones(len(ids),dtype=bool),LEADS)
   row['decisions']=[r for r in row['decisions'] if r['policy'] in ['E','C_delta_0']]
   row.update(stage=21,population=label,case_indices=ids.tolist(),posterior_forcing_std=dict(zip(['q25','median','q75'],map(float,np.quantile(np.array(fstdev)[ids],[.25,.5,.75])))))
   estimate=[];target=[];true=[]
   task=next((r for r in frozen['tasks'] if r['name']==name),None)
   for c in ids:
    if task and task.get('estimator'):
     with np.load(OUT/'inference'/name/f'{c:03d}.npz') as z:est=z['estimated_F_at_cutoff'].copy()
     own=np.repeat(post_f[c],9)
    else:
     own=post_f[c];est=own.copy()
     if task and task.get('arm')=='meanF':est.fill(own.mean())
     if task and task.get('arm')=='constantF':est.fill(8.)
    if task is None or name.startswith('CNN-F'):
     estimate.append(est);target.append(own);true.append(np.full_like(est,levels[c]))
   if estimate:
    e=np.concatenate(estimate);o=np.concatenate(target);t=np.concatenate(true)
    row['forcing_error']={key:dict(RMSE=float(np.sqrt(np.mean((e-v)**2))),bias=float(np.mean(e-v)),correlation=float(np.corrcoef(e,v)[0,1]) if np.std(e)>0 and np.std(v)>0 else None) for key,v in [('against_draw_forcing',o),('against_true_forcing',t)]}
   else:row['forcing_error']=None
   arms[label]=row
  results[name]=arms
 truth=np.concatenate([actual[:,:8]<actual[:,8,None],(actual[:,8]>np.array([climates[f]['jbar'] for f in levels])[:,None])[:,None]],1)
 reference=calibration(summaries['posterior'],truth,keep)
 g1=next(r['S'] for r in reference if r['lead']==2.)
 g2=loss(summaries['posterior'],keep)
 readings=dict(G1=dict(**g1,confirmed=g1['status']=='PASS',bound_type='Original R0, one-sided95% instance betting'),G2=dict(**g2['interval'],confirmed=not(g2['interval']['empty'] or g2['interval']['offset']) and g2['interval']['upper']<0,pairs=g2['actions'],cases=g2['cases']))
 for reading,comparator,kind,tick,lower_only in [('R1','CNN-F-constantF','E0',3,False),('R2','CNN-noF','E0',3,False),('R3',None,'E1',5,True),('R4',None,'E1',5,True)]:
  pairs=[]
  for j in range(1,6):
   fixed_name=f'CNN-F-{kind}-fixed-seed{j}';other=comparator or f'CNN-F-{kind}-rolling-seed{j}'
   if fixed_name in summaries and other in summaries:pairs.append((all_pattern_pair if reading=='R4' else pair_statistic)(summaries[fixed_name],summaries[other],truth,tick))
  readings[reading]=seed_average(pairs,alpha=.05 if lower_only else .01,lower_only=lower_only)
 for label,level in [('F7',7),('F9',9)]:
  ids=np.flatnonzero(keep&(levels==level));pairs=[]
  for j in range(1,6):
   a=f'CNN-F-E1-fixed-seed{j}';b=f'CNN-F-E1-rolling-seed{j}'
   if a in summaries and b in summaries:pairs.append(all_pattern_pair({k:v[ids] for k,v in summaries[a].items()},{k:v[ids] for k,v in summaries[b].items()},truth[ids],5))
  readings['R4_'+label+'_descriptive']=seed_average(pairs,alpha=.05,lower_only=True)
  readings['R4_'+label+'_descriptive']['descriptive']=True
 receipt=clean(dict(stage=21,freeze_e_sha256=digest(ROOT/'ACD_STAGE21_FREEZE_E.md'),excluded_cases=np.flatnonzero(~keep).tolist(),models=results,confirmatory=readings,missing_models=missing,reference_accuracy=reference,reference_paired=g2,realized_sha256=digest(OUT/'scoring/actual.npz'),resolutions=[]))
 (ROOT/'receipts/acd_stage21.json').write_text(json.dumps(receipt,indent=2,allow_nan=False)+'\n')
 lines=['# Stage21 forcing-shift panel readings','','All pipelines are reported. No frozen-route license. The reference LT/windows are held fixed; thresholds and observation-dependence use the instance-specific forcing climatology. Training-seed variation is separate from instance uncertainty.','','| Reading | Estimate | Interval/bound | Result |','|---|---:|---|---|']
 for key,r in readings.items():
  q=r.get('interval') or r
  lines.append(f"| {key} | {q.get('point',q.get('case_accuracy'))} | {q.get('lower',q.get('case_lower'))}, {q.get('upper',q.get('case_upper'))} | {'PASS' if r.get('confirmed') else 'not evaluable' if r.get('evaluable') is False else 'FAIL'} |")
 lines+=['','| Pipeline | Population | Lead | S share | Pooled S error | Case S error | E regret | C regret |','|---|---|---:|---:|---:|---:|---:|---:|']
 for name,groups in results.items():
  for group,m in groups.items():
   for r in m.get('confidence_readings',[]):
    decisions={x['policy']:x for x in m['decisions'] if x['lead']==r['lead']}
    lines.append(f"| {name} | {group} | {r['lead']} | {r['confident_S_share']} | {r['pooled_confident_error']} | {r['case_confident_error']} | {decisions['E']['mean_regret']} | {decisions['C_delta_0']['mean_regret']} |")
 lines+=['','State skill, forcing errors against both draw and true forcing, cost errors, bounds, calibration, same-lead differences, endpoints and decision action/harm records are retained in receipts/acd_stage21.json. Every invalid draw invalidates its pipeline instance. Excluded posterior cases are withheld.']
 (ROOT/'ACD_STAGE21_READING.md').write_text('\n'.join(lines)+'\n')
if __name__=='__main__':score()
