"""Stage6 post-hoc readings. Truth is opened exclusively in scoring functions."""
import os
os.environ['JAX_PLATFORMS']='cpu'
os.environ['JAX_ENABLE_X64']='true'
os.environ['NUMBA_NUM_THREADS']='2'
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
from pathlib import Path
import json,hashlib,numpy as np
from acd_protocol import ROOT,LEADS,WINDOWS,SIGMA,TICKS,PATTERNS,physics
from acd_stats import difference_interval,r0
from acd_questions import summary,labels
from acd_stage6_forward import RAW,OUT
TERMS=['injection','mean_flow','projection','displacement','rk4_residual','raw_injection_rate','raw_mean_flow_rate']
def save(p,d):p.write_text(json.dumps(d,indent=2,allow_nan=False)+'\n')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for x in iter(lambda:f.read(1048576),b''):h.update(x)
 return h.hexdigest()
def diff(d):
 r=difference_interval(d);r['scope']='POST HOC; no frozen route license'
 if r['empty'] or r['offset']:
  r['resolution']='R-other: retain bounds and point; no directional interpretation'
 return r
def loss(s,keep,last=False,only_pattern=None):
 counts={k:0 for k in ['earlier','later','same','both_beyond']}
 percase=[];records=[]
 for c in np.flatnonzero(keep):
  eligible=np.flatnonzero(s['observation'][c,:8,0]&s['confident'][c,8,0])
  if only_pattern is not None:eligible=eligible[eligible==only_pattern]
  local={k:0 for k in counts};v=[]
  for k in eligible:
   def endpoint(a):
    if last:return int(np.flatnonzero(a)[-1])
    z=np.flatnonzero(~a);return int(z[0]) if len(z) else 8
   a,b=endpoint(s['confident'][c,k]),endpoint(s['confident'][c,8])
   cat='earlier' if a<b else 'later' if a>b else 'both_beyond' if not last and a==8 else 'same'
   counts[cat]+=1;local[cat]+=1;v.append(int(a>b)-int(a<b))
   records.append({'case':int(c),'action':int(k),'S_endpoint_index':a,'Fc_endpoint_index':b,'category':cat})
  if v:percase.append({'case':int(c),'difference':float(np.mean(v)),'shares':{k:x/len(v) for k,x in local.items()}})
 return dict(cases=len(percase),actions=len(records),counts=counts,
  case_averaged_shares={k:float(np.mean([r['shares'][k] for r in percase])) if percase else None for k in counts},
  answer_weighted_shares={k:v/len(records) if records else None for k,v in counts.items()},
  interval=diff([r['difference'] for r in percase]),endpoint='last confident tested lead' if last else 'first nonconfident tested lead, index8 beyond-grid',
  records=records,case_records=percase)
def comparisons(s,keep,obs=False):
 rows=[]
 for t,lead in enumerate(LEADS):
  seven=s['confident'][keep,1:8,t].mean(1)-s['confident'][keep,8,t]
  all_s=s['confident'][keep,:8,t].mean(1)-s['confident'][keep,8,t]
  observation=s['observation'][keep,:8,t].mean(1)-s['confident'][keep,8,t]
  rows.append(dict(lead=float(lead),seven_S_share=float(s['confident'][keep,1:8,t].mean()),all_S_share=float(s['confident'][keep,:8,t].mean()),
   observation_S_share=float(s['observation'][keep,:8,t].mean()),Fc_share=float(s['confident'][keep,8,t].mean()),
   seven_minus_Fc=diff(seven),all_minus_Fc=diff(all_s),observation_minus_Fc=diff(observation)))
 return rows
def binary(j,jbar,null):
 n=len(j);p=np.concatenate([(j[:,:8]<j[:,8,None]).mean(0),(j[:,8]>jbar).mean(0)[None]])
 modal=p>.5;conf=np.maximum(p,1-p)>=.95
 climate=np.take_along_axis(null,modal[...,None].astype(int),-1)[...,0]>=.95
 return dict(p=np.maximum(p,1-p),modal=modal,confident=conf,climate=climate,observation=conf&~climate)
def stack(rows):return {k:np.stack([r[k] for r in rows]) for k in rows[0]}
def calibration(s,truth,keep):
 rows=[]
 for t,lead in enumerate(LEADS):
  obs=s['observation'][:,:8,t];right=s['modal'][:,:8,t]==truth[:,:8,t]
  sizes=obs.sum(1);correct=(obs&right).sum(1)
  a=r0(sizes[keep],correct[keep]);a['included_excluded']=r0(sizes,correct)
  fc=s['confident'][:,8,t];fcorrect=s['modal'][:,8,t]==truth[:,8,t]
  f=r0(fc[keep].astype(int),(fc&fcorrect)[keep].astype(int))
  rows.append(dict(lead=float(lead),S=a,Fc_case_betting=f))
 return rows
def score_saved_A(costs,s,keep,jbar,nullsd):
 # Hidden realized costs enter only this scoring function.
 actual=[]
 for c in range(200):
  with np.load(RAW/f'conf/score_{c:03d}.npz') as d:actual.append(d['actual_cost'].copy())
 actual=np.array(actual);truth=labels(actual,jbar)[:,np.r_[np.arange(8),37]]
 policies=[];horizon=[];bestnine=[]
 for t in [3,5]:
  choices=np.array([j.mean(0)[:,t].argmin() for j in costs])
  def realized(choice):
   c=np.flatnonzero(keep);chosen=actual[c,choice[c],t];baseline=actual[c,8,t]
   return dict(mean_regret=float(np.mean(chosen-actual[c,:,t].min(1))),
    worse_than_no_action_share=float(np.mean(chosen>baseline)),acting_share=float(np.mean(choice[c]!=8)),
    mean_realized_cost=float(chosen.mean()),mean_no_action_cost=float(baseline.mean()))
  policies.append(dict(lead=float(LEADS[t]),policy='E',delta_fraction=None,**realized(choices)))
  for delta in [0.,.01,.02,.05,.1]:
   selected=np.full(200,8,dtype=int);probabilities=[]
   for c,j in enumerate(costs):
    k=choices[c]
    p=float(np.mean(j[:,k,t]-j[:,8,t]<-delta*nullsd[k,t])) if k<8 else 0.
    if k<8 and p>=.95:selected[c]=k
    probabilities.append(p)
   policies.append(dict(lead=float(LEADS[t]),policy='C',delta_fraction=delta,**realized(selected)))
  conf=s['confident'][keep,:8,t];answer=np.broadcast_to(s['confident'][keep,8,t,None],conf.shape)
  opened=answer&~conf;right=s['modal'][keep,:8,t]==truth[keep,:8,t]
  horizon.append(dict(lead=float(LEADS[t]),answered_share=float(answer.mean()),answered_not_confident_share=float(opened.mean()),
   answered_not_confident_fraction_of_answered=float(opened.sum()/answer.sum()) if answer.any() else None,
   answered_not_confident_accuracy=float(right[opened].mean()) if opened.any() else None,questions=int(opened.sum()),
   answered_accuracy=float(right[answer].mean()) if answer.any() else None))
  probs=np.array([np.bincount(j[:,:,t].argmin(1),minlength=9)/len(j) for j in costs])
  modal=probs.argmax(1);conf=probs.max(1)>=.95
  correct=modal==actual[:,:,t].argmin(1)
  bestnine.append(dict(lead=float(LEADS[t]),confident_share=float(conf[keep].mean()),answers=int(conf[keep].sum()),
   accuracy=float(correct[keep&conf].mean()) if (keep&conf).any() else None,correct=int((keep&conf&correct).sum())))
 return dict(policies=policies,instance_Fc_rule=horizon,best_of_nine=bestnine)
def a_receipts():
 d=json.load(open(ROOT/'receipts/acd_stage2.json'));null=np.array(d['null']['question_probabilities']);jbar=d['null']['jbar']
 costs=[];allsummary=[];keep=[];hashes={}
 for c in range(200):
  p=RAW/f'conf/case_{c:03d}.npz'
  with np.load(p) as v:
   j=v['J'].copy();keep.append(not bool(v['excluded']))
  costs.append(j);allsummary.append(summary(j,jbar,null));hashes[str(p)]=sha(p)
 full=stack(allsummary);indices=np.r_[np.arange(8),37]
 s={k:v[:,indices] for k,v in full.items()};keep=np.array(keep)
 patterns=[]
 for k in range(8):
  patterns.append(dict(pattern=k,confidence=[dict(lead=float(lead),confident=float(s['confident'][keep,k,t].mean()),observation=float(s['observation'][keep,k,t].mean())) for t,lead in enumerate(LEADS)],loss=loss(s,keep,only_pattern=k)))
 a1=dict(comparisons=comparisons(s,keep),patterns=patterns)
 l=loss(s,keep);reentry={}
 for typ in ['S','Fc']:
  eligible=l['records'];experienced=0;reentered=0;examples=[]
  for row in eligible:
   k=row['action'] if typ=='S' else 8;c=row['case'];v=s['confident'][c,k];z=np.flatnonzero(~v)
   if len(z):
    experienced+=1
    if v[z[0]+1:].any():reentered+=1;examples.append([c,row['action']])
  reentry[typ]=dict(eligible_pairs=len(eligible),observed_losses=experienced,reentered=reentered,
   fraction_of_eligible=float(reentered/len(eligible)) if eligible else None,fraction_of_observed_losses=float(reentered/experienced) if experienced else None,
   unique_reentered_cases=len(set(x[0] for x in examples)))
 a2=dict(first_loss=l,last_confident=loss(s,keep,last=True),reentry=reentry)
 sensitivity=[]
 for count_as in [False,True]:
  v={k:x.copy() for k,x in s.items()};v['confident'][v['uncertain']]=count_as;v['observation']=v['confident']&~v['climate']
  sensitivity.append(dict(uncertain_counted='confident' if count_as else 'nonconfident',comparisons=comparisons(v,keep),loss=loss(v,keep)))
 uncertainty=[]
 for name,q in [('S',slice(0,8)),('P',slice(8,36)),('B',slice(36,37)),('Fc',slice(37,38))]:
  for t,lead in enumerate(LEADS):
   u=full['uncertain'][keep,q,t]
   uncertainty.append(dict(type=name,lead=float(lead),share=float(u.mean()),count=int(u.sum()),questions=int(u.size)))
 a3=dict(uncertainty=uncertainty,sensitivity=sensitivity)
 # Saved matched null costs provide the dimensional scale. No integrations for A.
 with np.load(ROOT/'runs/stage4b_null/null_0.16.npz') as n:
  sigmaD=(n['J'][:,:8]-n['J'][:,8,None]).std(0,ddof=1)
 a4=score_saved_A(costs,s,keep,jbar,sigmaD)
 save(OUT/'A.json',dict(panel='confirmation',post_hoc=True,licenses_frozen_route=False,cases=int(keep.sum()),A1=a1,A2=a2,A3=a3,A4=a4,source_hashes=hashes))
 print('A receipts analysis complete',flush=True)
def correlations(v):
 out=np.empty((8,v.shape[2],v.shape[2],8))
 for k in range(8):
  for t in range(8):
   a=v[:,k,:,t];sd=a.std(0,ddof=1);cov=np.cov(a,rowvar=False)
   out[k,:,:,t]=np.divide(cov,sd[:,None]*sd[None],out=np.zeros_like(cov),where=sd[:,None]*sd[None]>0)
 return out
def mechanism(panel,amp):
 means=[];sds=[];cors=[];confs=[];zs=[];metas=[];minority=[]
 for c in range(200):
  meta=json.load(open(OUT/f'{panel}_{c:03d}_{amp}.json'))
  if meta['excluded']:continue
  with np.load(OUT/f'{panel}_{c:03d}_{amp}.npz') as d:
   v=d['terms'];j=d['J'];conf=np.maximum((j[:,:8]<j[:,8,None]).mean(0),(j[:,:8]>=j[:,8,None]).mean(0))>=.95
   mu=v.mean(0);sd=v.std(0,ddof=1)
   positive=(v>0).mean(0);minority.append(np.minimum(positive,1-positive))
   means.append(mu);sds.append(sd);cors.append(correlations(v));zs.append(np.abs(mu)/np.maximum(sd,1e-300));confs.append(conf)
  metas.append(meta)
 means=np.array(means);sds=np.array(sds);cors=np.array(cors);zs=np.array(zs);conf=np.array(confs);minority=np.array(minority)
 rows=[]
 edges=[0,1,1.645,2,3,5,None]
 for t,lead in enumerate(LEADS):
  terms=[]
  for k,name in enumerate(TERMS):
   z=zs[:,:,k,t];bins=[]
   for lo,hi in zip(edges[:-1],edges[1:]):
    selected=(z>=lo)&(z<(hi if hi is not None else np.inf))
    bins.append(dict(lower=lo,upper=hi,questions=int(selected.sum()),confident_share=float(conf[:,:,t][selected].mean()) if selected.any() else None))
   corr=np.corrcoef(np.log1p(z).ravel(),conf[:,:,t].astype(float).ravel())[0,1] if np.std(z)>0 and np.std(conf[:,:,t])>0 else None
   m=minority[:,:,k,t];signcorr=np.corrcoef(m.ravel(),conf[:,:,t].astype(float).ravel())[0,1] if np.std(m)>0 and np.std(conf[:,:,t])>0 else None
   terms.append(dict(name=name,mean_sign_disagreement=float(m.mean()),median_sign_disagreement=float(np.median(m)),confidence_sign_disagreement_correlation=float(signcorr) if signcorr is not None else None,mean_posterior_mean=float(means[:,:,k,t].mean()),median_posterior_mean=float(np.median(means[:,:,k,t])),
    mean_posterior_sd=float(sds[:,:,k,t].mean()),median_posterior_sd=float(np.median(sds[:,:,k,t])),
    median_z=float(np.median(z)),confidence_log_z_correlation=float(corr) if corr is not None else None,bins=bins))
  rows.append(dict(lead=float(lead),terms=terms,median_within_posterior_correlation=np.median(cors[:,:,:,:,t],axis=(0,1)).tolist()))
 return dict(panel='confirmation' if panel=='conf' else 'development',post_hoc=True,exploratory=panel=='dev',amplitude=amp,
  aggregation='equal case/action weighting of within-posterior means, sample sds and correlations; descriptive bins only',
  rows=rows,budget_closure_max_abs=max(x['energy_budget_closure_max_abs'] for x in metas),
  projection_closure_max_abs=max(x['projection_closure_max_abs'] for x in metas),
  saved_J_max_abs=max(x['saved_J_max_abs'] for x in metas) if panel=='conf' else None)
def score_forward(block_s,keep,jbar):
 # Newly authorized hidden-state forward integrations remain inside scorer.
 target=OUT/'scoring.npz'
 if not target.exists():
  actualblock=[];states=[]
  for c in range(200):
   with np.load(RAW/f'conf/truth/input_{c:03d}.npz') as d:x=d['true'][-1].copy()
   traj=physics.simulate(np.repeat(x[None],9,axis=0),8+.16*PATTERNS,.01)
   actualblock.append(np.stack([(.5*np.mean(traj[:,w,:10]**2,axis=-1)).mean(-1) for w in WINDOWS],-1))
   states.append(traj[8])
  np.savez_compressed(target,block=np.array(actualblock),factual=np.array(states))
 with np.load(target) as d:actual=d['block'];actualstate=d['factual']
 truth=np.concatenate([actual[:,:8]<actual[:,8,None],(actual[:,8]>jbar)[:,None]],axis=1)
 cal=calibration(block_s,truth,keep)
 with np.load(ROOT/'runs/stage4b_null/states.npz') as d:climate=d['states'].mean(0)
 error=[];ac=[];pc=[]
 for c in range(200):
  with np.load(OUT/f'conf_{c:03d}_0.16.npz') as d:mean=d['factual_mean']
  real=actualstate[c];error.append(np.sqrt(np.mean((mean-real)**2,axis=-1))/SIGMA)
  x=mean-climate;y=real-climate;ac.append(np.sum(x*y,axis=-1)/np.sqrt(np.sum(x*x,axis=-1)*np.sum(y*y,axis=-1)))
  x=mean-mean.mean(-1,keepdims=True);y=real-real.mean(-1,keepdims=True)
  pc.append(np.sum(x*y,axis=-1)/np.sqrt(np.sum(x*x,axis=-1)*np.sum(y*y,axis=-1)))
 error=np.array(error);ac=np.array(ac);pc=np.array(pc);rows=[]
 for t,lead in enumerate(LEADS):
  tick=int(WINDOWS[t][0]);w=WINDOWS[t]
  rows.append(dict(lead=float(lead),tick=tick,time=float(TICKS[tick]*.05),RMSE_over_sigma=float(error[keep,tick].mean()),
   spatial_anomaly_correlation=float(ac[keep,tick].mean()),spatial_demeaned_pattern_correlation=float(pc[keep,tick].mean()),
   window_mean_RMSE_over_sigma=float(error[keep][:,w].mean()),window_mean_spatial_anomaly_correlation=float(ac[keep][:,w].mean())))
 return cal,dict(rows=rows,anomaly_origin='sitewise mean of saved 4096 null states; cosine of state anomalies; spatial-demeaned pattern correlation also shown',time_definition='first saved tick in each inherited lead window; window averages also reported',sigma=SIGMA)
def b_readings():
 with np.load(OUT/'null_block.npz') as d:
  n=d['block'];jbar=float(d['jbar_block'])
  p=np.concatenate([(n[:,:8]<n[:,8,None]).mean(0),(n[:,8]>jbar).mean(0)[None]])
  null=np.stack((1-p,p),-1);base=d['J']
 with np.load(ROOT/'runs/stage4b_null/null_0.16.npz') as d:nullmatch=float(np.max(np.abs(d['J']-base)))
 post=[];keep=[]
 for c in range(200):
  keep.append(not json.load(open(OUT/f'conf_{c:03d}_0.16.json'))['excluded'])
  with np.load(OUT/f'conf_{c:03d}_0.16.npz') as d:post.append(binary(d['block'],jbar,null))
 s=stack(post);keep=np.array(keep)
 cal,skill=score_forward(s,keep,jbar)
 result=dict(B1=dict(confirmation=mechanism('conf',.16),development_amplitude_0p64=mechanism('dev',.64)),
  B2=dict(observable='energy of sites0..9, normalized by10',jbar=jbar,climatological_probabilities=null.tolist(),
   null_full_energy_reproduction_max_abs=nullmatch,comparisons=comparisons(s,keep),calibration=cal,loss=loss(s,keep)),
  B3=skill)
 save(OUT/'B.json',result);print('B forward/scoring analyses complete',flush=True)
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('part',choices=['A','B']);args=p.parse_args()
 a_receipts() if args.part=='A' else b_readings()
