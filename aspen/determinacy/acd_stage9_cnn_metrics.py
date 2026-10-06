"""Stage9 CNN metrics; truth is opened exclusively in score()."""
import os
os.environ.update(JAX_PLATFORMS='cpu',JAX_ENABLE_X64='true',OPENBLAS_NUM_THREADS='1')
import numpy as np,json
from scipy.stats import beta
from acd_stage9_receipts import DEST,endpoint_fixed,dist
from acd_stage6_analysis import ROOT,RAW,OUT,LEADS,WINDOWS,SIGMA,binary,stack,comparisons,calibration,diff
from acd_stats import r0
def score(name,entries,summary,keep,means,costerrors,jbar):
 # Outcome labels and hidden factual states remain in scoring code on sulaco.
 actual=[]
 for c in range(200):
  with np.load(RAW/f'conf/score_{c:03d}.npz') as d:actual.append(d['actual_cost'])
 actual=np.array(actual);truth=np.concatenate([actual[:,:8]<actual[:,8,None],(actual[:,8]>jbar)[:,None]],1)
 with np.load(OUT/'scoring.npz') as d:states=d['factual'].copy()
 with np.load(ROOT/'runs/stage4b_null/states.npz') as d:climate=d['states'].mean(0)
 rows=[];skill=[]
 ts=[3] if name=='CNN-cost' else [3,5]
 for t in ts:
  c=np.flatnonzero(keep);conf=summary['confident'][:,:8,t];right=summary['modal'][:,:8,t]==truth[:,:8,t]
  acc=r0(conf[keep].sum(1),(conf&right)[keep].sum(1))
  obs=summary['observation'][:,:8,t];obsacc=r0(obs[keep].sum(1),(obs&right)[keep].sum(1))
  fc=summary['confident'][:,8,t];fc_right=summary['modal'][:,8,t]==truth[:,8,t];fc_acc=r0(fc[keep].astype(int),(fc&fc_right)[keep].astype(int))
  rows.append(dict(lead=float(LEADS[t]),confident_Fc_share=float(fc[keep].mean()),Fc_accuracy=fc_acc,Fc_case_error=1-fc_acc['case_accuracy'] if fc_acc['case_accuracy'] is not None else None,Fc_error_lower=1-fc_acc['case_upper'],Fc_error_upper=1-fc_acc['case_lower'],confident_S_share=float(conf[keep].mean()),observation_S_share=float(obs[keep].mean()),all_confident_accuracy=acc,observation_confident_accuracy=obsacc,case_confident_error=1-acc['case_accuracy'] if acc['case_accuracy'] is not None else None,error_lower=1-acc['case_upper'],error_upper=1-acc['case_lower']))
  if means is not None:
   err=np.sqrt(np.mean((means-states)**2,-1))/SIGMA
   x=means-climate;y=states-climate;den=np.sqrt(np.sum(x*x,-1)*np.sum(y*y,-1));ac=np.sum(x*y,-1)/den
   skill.append(dict(lead=float(LEADS[t]),window_mean_RMSE_over_sigma=float(err[keep][:,WINDOWS[t]].mean()),window_mean_anomaly_correlation=float(ac[keep][:,WINDOWS[t]].mean())))
 # Matched 1400 questions, seven zero-mean patterns at 2LT, same cases for all models.
 t=3;p=summary['p'][:,1:8,t];right=summary['modal'][:,1:8,t]==truth[:,1:8,t];bins=[]
 edges=[.5,.6,.7,.8,.9,.95,.99,1.]
 for lo,hi in zip(edges[:-1],edges[1:]):
  mask=(p>=lo)&((p<=hi) if hi==1 else p<hi)&keep[:,None];n=int(mask.sum());correct=int(right[mask].sum())
  lower=float(beta.ppf(.025,correct,n-correct+1)) if correct else 0.
  upper=float(beta.ppf(.975,correct+1,n-correct)) if correct<n else 1.
  bins.append(dict(lower_edge=lo,upper_edge=hi,questions=n,correct=correct,accuracy=correct/n if n else None,mean_probability=float(p[mask].mean()) if n else None,CP95=[lower,upper] if n else None,scope='pooled question CP descriptive; within-case dependence prevents independent-binomial coverage claim'))
 curves=[]
 for threshold in [.5,.55,.6,.65,.7,.75,.8,.85,.9,.95,.99]:
  mask=(p>=threshold)&keep[:,None];acc=r0(mask[keep].sum(1),(mask&right)[keep].sum(1))
  curves.append(dict(threshold=threshold,coverage=float(mask[keep].mean()),answers=int(mask.sum()),pooled_error=float(1-right[mask].mean()) if mask.any() else None,case_accuracy=acc))
 tests=[]
 for threshold in [.5,.95]:
  differences=[]
  for c in np.flatnonzero(keep):
   mask=p[c]>=threshold
   if mask.any():differences.append(float((p[c,mask]-right[c,mask]).mean()))
  interval=diff(differences)
  tests.append(dict(threshold=threshold,cases=len(differences),overconfidence_interval=interval,reject_mean_calibration=bool(not interval['empty'] and not interval['offset'] and (interval['lower']>0 or interval['upper']<0)),test='v2.3 two-sided99% case-level betting interval for case-mean modal probability minus correctness; necessary mean-calibration check, not a full conditional calibration test'))
 original=json.load(open(DEST/'receipt_analyses.json'))['A']['A2']['records'];fixed_eligible=np.zeros((200,8),bool)
 for c,k,_,_ in original:fixed_eligible[c,k]=True
 eligible=summary['observation'][:,:8,0]&summary['confident'][:,8,0,None]
 return dict(model=name,post_hoc=True,matched_cases=int(keep.sum()),matched_questions=int(keep.sum()*7),confidence_readings=rows,state_skill=skill,per_draw_cost_errors=costerrors,reliability=bins,error_coverage=curves,calibration_test=tests,comparisons=[r for r in comparisons(summary,keep) if r['lead'] in ([2] if name=='CNN-cost' else [2,3])],paired_endpoint=endpoint_fixed(summary,keep,eligible) if name!='CNN-cost' else None,paired_endpoint_fixed_posterior_cohort=endpoint_fixed(summary,keep,fixed_eligible) if name!='CNN-cost' else None)
def run(name):
 frozen=json.load(open(ROOT/'receipts/acd_stage2.json'));jbar=frozen['null']['jbar'];null=np.array(frozen['null']['question_probabilities'])[np.r_[np.arange(8),37]]
 rows=[];keep=[];means=[];errs=[];invalid=[]
 directory=DEST/'inference'/name
 for c in range(200):
  with np.load(RAW/f'conf/case_{c:03d}.npz') as d:physicsJ=d['J'].copy();excluded=bool(d['excluded'])
  if name=='posterior':J=physicsJ;valid=True
  else:
   with np.load(directory/f'{c:03d}.npz') as d:J=d['J'].copy();valid=bool(d['valid'].all());means.append(d['factual_mean'].copy())
  s=binary(J,jbar,null)
  if name=='CNN-cost':
   unavailable=[t for t in range(8) if t!=3];s['confident'][:,unavailable]=False;s['observation'][:,unavailable]=False
  if not valid:s['confident'].fill(False);s['observation'].fill(False);invalid.append(c)
  rows.append(s);keep.append(not excluded)
  if name!='posterior':
   for t in ([3] if name=='CNN-cost' else [3,5]):
    for kind,error in [('J8',J[:,8,t]-physicsJ[:,8,t]),('Jk',J[:,:8,t]-physicsJ[:,:8,t]),('Dk',(J[:,:8,t]-J[:,8,None,t])-(physicsJ[:,:8,t]-physicsJ[:,8,None,t]))]:
     errs.append(dict(case=c,lead=float(LEADS[t]),quantity=kind,bias=float(error.mean()),RMSE=float(np.sqrt(np.mean(error**2))),MAE=float(np.abs(error).mean())))
 s=stack(rows);keep=np.array(keep)
 costs=[]
 for t in ([3] if name=='CNN-cost' else [3,5]):
  for kind in ['J8','Jk','Dk']:
   selected=[r for r in errs if r['lead']==LEADS[t] and r['quantity']==kind]
   if selected:costs.append(dict(lead=float(LEADS[t]),quantity=kind,**{key:dist(np.array([r[key] for r in selected])) for key in ['bias','RMSE','MAE']},weighting='equal cases; each case metric uses every saved draw and each action equally'))
 if name=='posterior':
  for c in range(200):
   with np.load(OUT/f'conf_{c:03d}_0.16.npz') as d:means.append(d['factual_mean'])
 result=score(name,None,s,keep,np.array(means) if name!='CNN-cost' else None,costs,jbar);result['invalid_cases']=invalid
 if name!='posterior':result['execution']=json.load(open(directory/'complete.json'))
 (DEST/f'metrics_{name}.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
if __name__=='__main__':
 import sys;run(sys.argv[1])
