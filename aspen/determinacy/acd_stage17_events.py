"""Stage 17 B/D; run only after Stage 15A is present in Git HEAD."""
from acd_stage17 import *
from acd_stats import r0,difference_interval,log_capital_max
import subprocess

def committed_15a():
 files=subprocess.check_output(['git','ls-tree','-r','--name-only','HEAD'],cwd=ROOT.parents[1],text=True).splitlines()
 candidates=[p for p in files if p.startswith('aspen/determinacy/receipts/') and 'stage15' in p.lower() and p.endswith('.json')]
 if not candidates:raise RuntimeError('Stage 15A receipt not committed; B and D await its receipt and ranking definitions')
 # Require an explicit A-specific receipt or an A section in the combined receipt.
 verified=[]
 for candidate in candidates:
  content=json.loads(subprocess.check_output(['git','show','HEAD:'+candidate],cwd=ROOT.parents[1],text=True))
  if 'stage15a' in candidate.lower() or 'A' in content:
   verified.append(dict(path=candidate,sha256=sha(ROOT.parents[1]/candidate)))
 if not verified:raise RuntimeError('Stage 15 receipt exists but no committed A section')
 return verified

def pooled_error_bounds(mask,wrong):
 n=mask.sum(1).astype(float);e=(mask&wrong).sum(1).astype(float);contributing=n>0
 if not contributing.any():return [0.,1.]
 n=n[contributing]/mask.shape[1];e=e[contributing]/mask.shape[1]
 threshold=np.log(1/.05)
 def rejected(q,direction):
  return log_capital_max((e-q*n+1)/2,.5,direction,.05)>=threshold
 def invert(direction):
  low,high=0,1000
  if direction==1:
   if not rejected(0.,1):return 0.
   while low<high:
    mid=(low+high+1)//2
    if rejected(mid/1000,1):low=mid
    else:high=mid-1
  else:
   if not rejected(1.,-1):return 1.
   while low<high:
    mid=(low+high)//2
    if rejected(mid/1000,-1):high=mid
    else:low=mid+1
  return low/1000
 return [invert(1),invert(-1)]
def error_bounds(mask,wrong):
 a=r0(mask.sum(1),(mask&~wrong).sum(1))
 return dict(pooled_error_bounds_one_sided95=pooled_error_bounds(mask,wrong),case_error=1-a['case_accuracy'] if a['case_accuracy'] is not None else None,case_error_lower95=1-a['case_upper'],case_error_upper95=1-a['case_lower'],accuracy_receipt=a)
def reliability(p,y,edges):
 rows=[]
 for lo,hi in zip(edges[:-1],edges[1:]):
  mask=(p>=lo)&((p<=hi) if hi==1 else p<hi);n=int(mask.sum());correct=int(y[mask].sum())
  lower=float(beta.ppf(.025,correct,n-correct+1)) if correct else 0.
  upper=float(beta.ppf(.975,correct+1,n-correct)) if correct<n else 1.
  rows.append(dict(lower_edge=lo,upper_edge=hi,questions=n,events=correct,mean_probability=float(p[mask].mean()) if n else None,event_share=correct/n if n else None,descriptive_CP95=[lower,upper] if n else None))
 return rows

def score_events():
 # All saved realized outcomes are read only inside this scoring function.
 sources=committed_15a();costs_by={m:prior.loadcosts(m) for m in MODELS};n=len(costs_by['posterior'][0]);actual=[]
 for c in range(n):
  with np.load(RAW/f'conf/score_{c:03d}.npz') as f:actual.append(f['actual_cost'])
 actual=np.array(actual);jbar=prior.frozen()[0];edges=[0,.05,.2,.4,.6,.8,.95,1.]
 results={};differences=[];transfer=[];scatter={};reference={}
 for model,(costs,valid,keep) in costs_by.items():
  if not valid[keep].all():raise RuntimeError('R-other: invalid case present; event score requires explicit probability contract without survival conditioning')
  cases=np.flatnonzero(keep);modelrows=[]
  for t in [3,5]:
   js=[costs[c][:,:,t] for c in cases];ps=[costs_by['posterior'][0][c][:,:,t] for c in cases]
   pF=np.array([(j[:,8]>jbar).mean() for j in js]);yF=actual[cases,8,t]>jbar
   r=np.array([(j[:,:8]<j[:,8,None]).mean(0) for j in js]);truth=actual[cases,:8,t]<actual[cases,8,None,t]
   fcvalues=(pF-yF)**2
   row=dict(lead=float(LEADS[t]),forecast=dict(case_Brier=float(fcvalues.mean()),case_scores=fcvalues.tolist(),reliability=reliability(pF,yF,edges)),benefit={},risk_coverage=[])
   reference[(model,t,'forecast')]=fcvalues
   fcmodal=np.maximum(pF,1-pF)[:,None];fcwrong=((pF>.5)!=yF)[:,None]
   for threshold in THRESHOLDS:
    mask=fcmodal>=threshold
    row['risk_coverage'].append(dict(patterns='forecast',threshold=threshold,coverage=float(mask.mean()),answers=int(mask.sum()),pooled_error=float(fcwrong[mask].mean()) if mask.any() else None,**error_bounds(mask,fcwrong)))
   for label,sl in [('seven_zero_mean',slice(1,None)),('all_eight',slice(None))]:
    values=((r[:,sl]-truth[:,sl])**2).mean(1);reference[(model,t,label)]=values
    row['benefit'][label]=dict(case_Brier=float(values.mean()),case_scores=values.tolist(),reliability=reliability(r[:,sl],truth[:,sl],edges))
    modal=np.maximum(r[:,sl],1-r[:,sl]);wrong=(r[:,sl]>.5)!=truth[:,sl]
    for threshold in THRESHOLDS:
     mask=modal>=threshold
     row['risk_coverage'].append(dict(patterns=label,threshold=threshold,coverage=float(mask.mean()),answers=int(mask.sum()),pooled_error=float(wrong[mask].mean()) if mask.any() else None,**error_bounds(mask,wrong)))
   j8err=[j[:,8]-p[:,8] for j,p in zip(js,ps)]
   pool=np.concatenate(j8err);realerr=np.array([j[:,8].mean() for j in js])-actual[cases,8,t]
   modal=np.maximum(r,1-r);wrong=(r>.5)!=truth;mask=modal>=.95
   row['frontier']=dict(per_draw_J8_RMSE=float(np.sqrt(np.mean(pool**2))),per_draw_J8_bias=float(pool.mean()),equal_case_J8_RMSE=float(np.mean([np.sqrt(np.mean(e**2)) for e in j8err])),equal_case_J8_bias=float(np.mean([e.mean() for e in j8err])),ensemble_mean_J8_RMSE_against_realized=float(np.sqrt(np.mean(realerr**2))),ensemble_mean_J8_bias_against_realized=float(realerr.mean()),forecast_Brier=float(fcvalues.mean()),pooled_confident_S_error=float(wrong[mask].mean()) if mask.any() else None,**error_bounds(mask,wrong),benefit_Brier_seven=row['benefit']['seven_zero_mean']['case_Brier'],benefit_Brier_all_eight=row['benefit']['all_eight']['case_Brier'])
   modelrows.append(row)
   if model!='posterior':
    diagnostic=[];grid=np.logspace(-3,0,41)
    for c,j,p in zip(cases,js,ps):
     D=p[:,:8]-p[:,8,None];Dh=j[:,:8]-j[:,8,None];mse=((Dh-D)**2).mean(0);gap=np.abs((Dh<0).mean(0)-(D<0).mean(0));bounds=(np.abs(D)[:,:,None]<=grid).mean(0)+mse[:,None]/grid**2
     ix=bounds.argmin(1)
     diagnostic.extend([dict(case=int(c),action=k,error_MSE=float(mse[k]),probability_difference=float(gap[k]),minimized_bound=float(bounds[k,ix[k]]),minimizing_radius=float(grid[ix[k]])) for k in range(D.shape[1])])
    gaps=np.array([x['probability_difference'] for x in diagnostic]);b=np.array([x['minimized_bound'] for x in diagnostic])
    transfer.append(dict(model=model,lead=float(LEADS[t]),median_probability_difference=float(np.median(gaps)),p90_probability_difference=float(np.quantile(gaps,.9)),median_minimized_bound=float(np.median(b)),share_bound_below_0_05=float((b<.05).mean()),share_bound_at_least_one=float((b>=1).mean()),case_actions=diagnostic))
    scatter[model,t]=(b,gaps)
  results[model]=modelrows
 for model in MODELS:
  if model=='posterior':continue
  for t in [3,5]:
   for event in ['forecast','seven_zero_mean','all_eight']:
    differences.append(dict(model=model,lead=float(LEADS[t]),event=event,interval=difference_interval(reference[model,t,event]-reference['posterior',t,event])))
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 fig,axs=plt.subplots(1,2,figsize=(10,4))
 for ax,t in zip(axs,[3,5]):
  for model,marker in zip([m for m in MODELS if m!='posterior'],['s','^','x','+']):
   b,g=scatter[model,t];ax.scatter(b,g,s=12,marker=marker,color='0.3',alpha=.45,label=model)
  maximum=max(float(scatter[m,t][0].max()) for m in MODELS if m!='posterior');ax.plot([0,maximum],[0,maximum],':',lw=.6,color='0.5');ax.set(xlabel='minimized bound',ylabel='absolute probability difference',title=str(float(LEADS[t]))+' LT',ylim=(0,1));ax.legend(fontsize=7)
 fig.tight_layout();dest=ROOT/'figures/F20_transfer_paper';fig.savefig(str(dest)+'.pdf');fig.savefig(str(dest)+'.png',dpi=180);plt.close(fig)
 return dict(models=results,Brier_differences=differences,Stage15A_committed_paths=sources,reliability_scope='pooled Clopper–Pearson intervals are descriptive because actions share cases',frontier_scope='CNN-F and CNN-noF have no development-panel runs; no equivalence margin independent of confirmation outcomes is available. This is a descriptive frontier, not an equivalence test.'),dict(rows=transfer,radius_grid=grid.tolist(),bound_definition='P(|D|<=r)+mean_draw((Dhat-D)^2)/r^2; minimum over fixed log grid; bounds >=1 are vacuous',figure_page_points=[720,288])
if __name__=='__main__':
 d=json.loads(RECEIPT.read_text());d['B'],d['D']=score_events();d['resolutions']=[s for s in d['resolutions'] if 'remain pending' not in s];save(d)
