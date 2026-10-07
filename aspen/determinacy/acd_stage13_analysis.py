"""Stage 13: post hoc receipt analyses and CPU step-halving; truth only in score functions."""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',NUMBA_NUM_THREADS='8',JAX_PLATFORMS='cpu',JAX_ENABLE_X64='true')
import json,hashlib,time
from pathlib import Path
import numpy as np
from scipy.stats import beta,binomtest
from acd_stage6_analysis import ROOT,RAW,LEADS,WINDOWS,binary,stack,comparisons
from acd_stage9_receipts import endpoint_fixed
from acd_protocol import PATTERNS,physics
from acd_questions import labels
from acd_stats import r0,r0_f
OUT=ROOT/'runs/stage13';OUT.mkdir(parents=True,exist_ok=True)
RECEIPTS=ROOT/'receipts'
MODELS=['posterior','CNN-20k','CNN-F','CNN-F-resp']
# Illustrative selection fixed before reading records: modal earlier endpoint pair;
# tie of modal endpoint combinations resolved lexicographically, then lowest case/action.
SELECTION='Among earlier pairs, most frequent (S first loss, Fc first loss); lexicographic combination on a frequency tie; lowest case, then lowest action.'
def save(name,d): (RECEIPTS/name).write_text(json.dumps(d,indent=2,allow_nan=False)+'\n')
def frozen():
 d=json.load(open(RECEIPTS/'acd_stage2.json'))
 return d['null']['jbar'],np.array(d['null']['question_probabilities'])
def loadcosts(model):
 costs=[];valid=[];keep=[]
 for c in range(200):
  with np.load(RAW/f'conf/case_{c:03d}.npz') as d:
   keep.append(not bool(d['excluded']))
   if model=='posterior': j=d['J'].copy();v=np.isfinite(j).all()
  if model!='posterior':
   with np.load(ROOT/f'runs/stage9/inference/{model}/{c:03d}.npz') as d:
    j=d['J'].copy();v=bool(d['valid'].all()) and np.isfinite(j).all()
  costs.append(j);valid.append(v)
 return costs,np.array(valid),np.array(keep)
def nullsd():
 with np.load(ROOT/'runs/stage4b_null/null_0.16.npz') as d:
  return (d['J'][:,:8]-d['J'][:,8,None]).std(0,ddof=1)
def summaries(costs,valid,jbar,null):
 rows=[]
 for j,v in zip(costs,valid):
  s=binary(j,jbar,null[np.r_[np.arange(8),37]])
  if not v:s['confident'].fill(False);s['observation'].fill(False)
  rows.append(s)
 return stack(rows)
def choices(costs,valid,t,sd):
 e=np.full(len(costs),8,int)
 for c,j in enumerate(costs):
  if valid[c]:e[c]=j[:,:,t].mean(0).argmin()
 out={'E':e,'no_action':np.full(len(costs),8,int),'always_uniform_decrease':np.zeros(len(costs),int)}
 for delta in [0,.1]:
  ch=np.full(len(costs),8,int)
  for c,j in enumerate(costs):
   k=e[c]
   if valid[c] and k<8 and np.mean(j[:,k,t]-j[:,8,t]<-delta*sd[k,t])>=.95:ch[c]=k
  out[f'C_delta_{delta}']=ch
 return out
def decision_rows(actual,costs,valid,keep,sd):
 rows=[];records={}
 c=np.flatnonzero(keep)
 for t in [3,5]:
  baseline=actual[c,8,t];best=actual[c,:,t].min(1);den=float((baseline-best).mean())
  for name,ch in choices(costs,valid,t,sd).items():
   value=actual[c,ch[c],t];harm=value-baseline;bad=harm>0;n=len(c);nh=int(bad.sum())
   r=dict(lead=float(LEADS[t]),policy=name,cases=n,invalid_cases=int((~valid&keep).sum()),mean_improvement=float((baseline-value).mean()),mean_regret=float((value-best).mean()),mean_no_action_regret=den,capture_fraction=float((baseline-value).mean()/den),acting_share=float((ch[c]!=8).mean()),harms=nh,median_harm=float(np.median(harm[bad])) if nh else None,max_harm=float(harm[bad].max()) if nh else None,zero_harm_CP_upper=float(beta.ppf(.95,1,n)) if not nh else None,chosen_actions=np.bincount(ch[c],minlength=9).tolist())
   rows.append(r);records[(t,name)]=(ch[c],value-best,bad)
 return rows,records
def score_decisions():
 # Saved outcomes are opened only in scoring.
 actual=np.array([np.load(RAW/f'conf/score_{c:03d}.npz')['actual_cost'] for c in range(200)])
 sd=nullsd();results={};records={};keep0=None
 for model in MODELS:
  costs,valid,keep=loadcosts(model)
  if keep0 is None:keep0=keep
  assert np.array_equal(keep,keep0)
  rows,rr=decision_rows(actual,costs,valid,keep,sd)
  results[model]=dict(readings=rows,invalid_case_indices=np.flatnonzero(~valid&keep).tolist());records[model]=rr
 baseline=json.load(open(ROOT/'runs/stage9/receipt_analyses.json'))['D']
 if isinstance(baseline,dict):baseline=baseline.get('policies',baseline)
 # Verify all shared posterior quantities against prior Stage9 D.
 matched=0
 for row in results['posterior']['readings']:
  matches=[r for r in baseline if r['lead']==row['lead'] and r['policy']==row['policy']]
  if matches:
   old=matches[0]
   for k,v in old.items():
    if k in row:assert row[k]==v,(k,row[k],v)
   matched+=1
 assert matched==len(results['posterior']['readings'])
 pairs=[]
 for model in MODELS[1:]:
  for key,(ch,reg,bad) in records[model].items():
   pc,pr,pbad=records['posterior'][key];d=reg-pr;nz=d[d!=0];n01=int((~pbad&bad).sum());n10=int((pbad&~bad).sum())
   seed=int.from_bytes(hashlib.sha256(f'acd-stage13-paired-bootstrap/{model}/{key}'.encode()).digest()[:8],'little');g=np.random.default_rng(seed)
   means=np.mean(d[g.integers(0,len(d),(10000,len(d)))],1)
   pairs.append(dict(model=model,lead=float(LEADS[key[0]]),policy=key[1],chosen_option_different_share=float((ch!=pc).mean()),mean_regret_difference=float(d.mean()),nonzero_regret_differences=len(nz),positive_regret_differences=int((nz>0).sum()),exact_two_sided_sign_p=float(binomtest(int((nz>0).sum()),len(nz),.5).pvalue) if len(nz) else 1.,descriptive_paired_bootstrap_95_interval=np.quantile(means,[.025,.975]).tolist(),bootstrap_replicates=len(means),bootstrap_seed=seed,bootstrap_scope='descriptive paired case bootstrap; post hoc',posterior_only_harm=n10,model_only_harm=n01,exact_McNemar_p=float(binomtest(n01,n01+n10,.5).pvalue) if n01+n10 else 1.))
 save('acd_stage13_decisions.json',dict(post_hoc=True,licenses_frozen_route=False,invalid_rule='Any invalid draw or option forces no action for E and C; no survivor conditioning.',posterior_stage9_reproduction_rows=matched,models=results,paired_comparisons=pairs))
 print('A completed, posterior Stage9 policy reproduction exact',flush=True)
def score_withheld_instance():
 jbar,null=frozen();costs,valid,keep=loadcosts('posterior');s=summaries(costs,valid,jbar,null);sd=nullsd()
 # Truth access confined to scoring.
 actual=np.array([np.load(RAW/f'conf/score_{c:03d}.npz')['actual_cost'] for c in range(200)])
 rows=[]
 for t in [3,5]:
  for group,ks in [('all_eight',np.arange(8)),('seven_zero_mean',np.arange(1,8))]:
   confidence=s['confident'][keep][:,ks,t];real=(actual[:,:8]-actual[:,8,None])[keep][:,ks,t]
   mean=np.array([(j[:,:8,t]-j[:,8,None,t]).mean(0) for j in costs])[keep][:,ks]
   absolute=np.abs(real);confmedian=float(np.median(absolute[confidence]));withheld=~confidence
   groups={}
   for label,mask in [('confident',confidence),('not_confident',withheld)]:
    groups[label]=dict(questions=int(mask.sum()),**{kind:dict(zip(['q25','median','q75'],map(float,np.quantile(values[mask],[.25,.5,.75])))) for kind,values in [('realized_absolute_effect',absolute),('posterior_mean_absolute_effect',np.abs(mean)),('realized_absolute_effect_over_climate_sd',absolute/sd[ks,t])]})
   rows.append(dict(lead=float(LEADS[t]),patterns=group,groups=groups,not_confident_exceeds_confident_median_share=float((absolute[withheld]>confmedian).mean()),not_confident_beneficial_share=float((real[withheld]<0).mean())))
 save('acd_stage13_withheld.json',dict(post_hoc=True,descriptive=True,readings=rows))
 from collections import Counter
 records=json.load(open(ROOT/'runs/stage9/receipt_analyses.json'))['A']['A2']['records']
 earlier=[r for r in records if r[2]<r[3]];counts=Counter((r[2],r[3]) for r in earlier)
 combination=min(counts,key=lambda a:(-counts[a],a));c,k,a,b=min(r for r in earlier if (r[2],r[3])==combination)
 j=costs[c];variables={'Fc':j[:,8]-jbar,'S':j[:,k]-j[:,8]}
 series={name:dict(q05=np.quantile(v,.05,axis=0).tolist(),q25=np.quantile(v,.25,axis=0).tolist(),median=np.median(v,axis=0).tolist(),q75=np.quantile(v,.75,axis=0).tolist(),q95=np.quantile(v,.95,axis=0).tolist(),modal_probability=s['p'][c,8 if name=='Fc' else k].tolist(),realized=(actual[c,8]-jbar if name=='Fc' else actual[c,k]-actual[c,8]).tolist()) for name,v in variables.items()}
 save('acd_stage13_instance.json',dict(post_hoc=True,illustrative=True,selection_rule=SELECTION,eligible_pairs=len(records),earlier_pairs=len(earlier),combination_count=counts[combination],case=c,action=k,S_first_loss_index=a,Fc_first_loss_index=b,S_first_loss_lead=float(LEADS[a]) if a<len(LEADS) else None,Fc_first_loss_lead=float(LEADS[b]) if b<len(LEADS) else None,leads=list(map(float,LEADS)),series=series))
 print('C/D completed',c,k,flush=True)
def forecast_dt(theta,dt):
 # First-frame posterior state; recompute the observation window at the new dt.
 x=physics.simulate(theta[:,:40],np.repeat(theta[:,40,None],40,axis=1),dt,11)[:,-1]
 initial=np.repeat(x[:,None,:],len(PATTERNS),axis=1).reshape(-1,40)
 forcing=(theta[:,40,None,None]+.16*PATTERNS[None]).reshape(-1,40)
 j=physics.costs(physics.simulate(initial,forcing,dt))
 return j.reshape(len(theta),len(PATTERNS),len(LEADS))
def forward_dt():
 start=time.time()
 with np.load(ROOT/'runs/stage4b_null/states.npz') as d:x=d['states'].copy()
 p=OUT/'dt_null.npz'
 if not p.exists():
  chunks=[]
  for first in range(0,len(x),64):
   xx=x[first:first+64];initial=np.repeat(xx[:,None],9,axis=1).reshape(-1,40)
   forcing=np.broadcast_to(8+.16*PATTERNS,(len(xx),9,40)).reshape(-1,40)
   chunks.append(physics.costs(physics.simulate(initial,forcing,.005)).reshape(len(xx),9,8))
  np.savez_compressed(p,J=np.concatenate(chunks))
 directory=OUT/'dt';directory.mkdir(exist_ok=True)
 for c in range(200):
  p=directory/f'{c:03d}.npz'
  if not p.exists():
   with np.load(RAW/f'conf/case_{c:03d}.npz') as d:theta=d['theta'].copy()
   j=np.concatenate([forecast_dt(theta[first:first+64],.005) for first in range(0,len(theta),64)])
   np.savez_compressed(p,J=j)
  print('dt case',c,'elapsed',time.time()-start,flush=True)
 score_dt();finalize_dt()
def score_dt():
 jbar,oldnull=frozen()
 with np.load(OUT/'dt_null.npz') as d:nullj=d['J'].copy()
 lab=labels(nullj,jbar);newnull=np.stack([(lab==a).mean(0) for a in range(8)],-1)
 oldcost,valid,keep=loadcosts('posterior');newcost=[];truthold=[];truthnew=[]
 true_dir=RAW/'conf/truth'
 # Opening first-frame hidden true states occurs exclusively inside this scoring function.
 for c in range(200):
  with np.load(OUT/f'dt/{c:03d}.npz') as d:newcost.append(d['J'].copy())
  with np.load(RAW/f'conf/score_{c:03d}.npz') as d:truthold.append(d['actual_cost'].copy())
  with np.load(true_dir/f'input_{c:03d}.npz') as d:true=d['true'][0].copy()
  truthnew.append(forecast_dt(np.r_[true,8][None],.005)[0])
 old=summaries(oldcost,valid,jbar,oldnull);new=summaries(newcost,valid,jbar,newnull)
 actual=np.array(truthnew);oldactual=np.array(truthold)
 oldlab=labels(oldactual,jbar);newlab=labels(actual,jbar)
 rows=[];groups={'S':slice(0,8),'P':slice(8,36),'B':slice(36,37),'Fc':slice(37,38)}
 fullold=[];fullnew=[]
 from acd_confirmation_analysis import basic
 for jo,jn in zip(oldcost,newcost):fullold.append(basic(jo,jbar,oldnull));fullnew.append(basic(jn,jbar,newnull))
 fullold=stack(fullold);fullnew=stack(fullnew)
 for t,l in enumerate(LEADS):
  for name,ks in groups.items():
   changed=total=0
   for c,(jo,jn) in enumerate(zip(oldcost,newcost)):
    if keep[c]:
     ao=labels(jo,jbar)[:,ks,t];an=labels(jn,jbar)[:,ks,t];changed+=int((ao!=an).sum());total+=ao.size
   rows.append(dict(lead=float(l),type=name,draw_answer_changes=changed,draw_answers=total,draw_answer_changed_share=changed/total,confidence_changed_count=int((fullold['confident'][keep,ks,t]!=fullnew['confident'][keep,ks,t]).sum()),confidence_changed_share=float((fullold['confident'][keep,ks,t]!=fullnew['confident'][keep,ks,t]).mean()),realized_answer_changed_count=int((oldlab[keep,ks,t]!=newlab[keep,ks,t]).sum()),realized_answer_changed_share=float((oldlab[keep,ks,t]!=newlab[keep,ks,t]).mean())))
 accuracy=[]
 for t,l in enumerate(LEADS):
  for name,ks in groups.items():
   conf=fullnew['confident'][keep,ks,t];obs=fullnew['observation'][keep,ks,t];right=fullnew['modal'][keep,ks,t]==newlab[keep,ks,t]
   for selection,mask in [('all_confident',conf),('observation_confident',obs)]:
    accuracy.append(dict(lead=float(l),type=name,selection=selection,accuracy=r0(mask.sum(1),(mask&right).sum(1))))
 eligible=new['observation'][:,:8,0]&new['confident'][:,8,0,None]
 endpoint=endpoint_fixed(new,keep,eligible)
 oldeligible=old['observation'][:,:8,0]&old['confident'][:,8,0,None]
 baseline=endpoint_fixed(old,keep,oldeligible)
 fixed=endpoint_fixed(new,keep,oldeligible)
 save('acd_stage13_dt.json',dict(post_hoc=True,dt=.005,baseline_dt=.01,float64=True,first_frame_restart=True,all_saved_draws=sum(len(j) for j in newcost),null_states=len(nullj),changes=rows,Table2_accuracy=accuracy,paired_first_loss=endpoint,paired_fixed_original_cohort=fixed,baseline_paired_first_loss=baseline,paired_point_change=endpoint['interval']['point']-baseline['interval']['point'],seven_pattern_comparisons=[r for r in comparisons(new,keep) if r['lead'] in [2,3]],null_question_probabilities=newnull.tolist()))
 print('B completed',flush=True)
def finalize_dt():
 d=json.load(open(RECEIPTS/'acd_stage13_dt.json'));table=[]
 for l in LEADS:
  sr=next(r['accuracy'] for r in d['Table2_accuracy'] if r['lead']==l and r['type']=='S' and r['selection']=='observation_confident')
  fr=next(r['accuracy'] for r in d['Table2_accuracy'] if r['lead']==l and r['type']=='Fc' and r['selection']=='all_confident')
  n=fr['answers'];correct=round(n*fr['answer_accuracy']) if n else 0
  fc=r0_f(correct,n)
  table.append(dict(lead=float(l),S_case_accuracy=sr['case_accuracy'],S_one_sided95_lower=sr['case_lower'],S_answers=sr['answers'],S_cases=sr['cases'],Fc_accuracy=fr['answer_accuracy'],Fc_one_sided95_lower=fc['lower'] if 'lower' in fc else fc.get('accuracy_lower'),Fc_answers=n,Fc_exact=fc))
 d['Table2']=table;save('acd_stage13_dt.json',d)
if __name__=='__main__':
 import sys
 {'A':score_decisions,'CD':score_withheld_instance,'B':forward_dt,'finalize':finalize_dt}[sys.argv[1]]()
