"""Stage 9 receipt analyses; hidden outcomes opened only by score()."""
import os
os.environ.update(JAX_PLATFORMS='cpu',JAX_ENABLE_X64='true',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
import json,numpy as np,arviz as az
from scipy.stats import beta
from acd_stage6_analysis import RAW,OUT,ROOT,LEADS,stack,binary,comparisons,loss,calibration,sha
from acd_questions import labels
from acd_stats import r0
DEST=ROOT/'runs/stage9';DEST.mkdir(exist_ok=True,parents=True)
def dist(v):
 return dict(min=float(np.min(v)),q25=float(np.quantile(v,.25)),median=float(np.median(v)),q75=float(np.quantile(v,.75)),max=float(np.max(v)),mean=float(np.mean(v)))
def endpoint_fixed(s,keep,eligible,last=False):
 records=[];cases=[];counts=dict(earlier=0,later=0,same=0,S_beyond=0,Fc_beyond=0,both_beyond=0)
 for c in np.flatnonzero(keep):
  d=[];local=dict(earlier=0,later=0,same=0)
  for k in np.flatnonzero(eligible[c]):
   def ep(a):
    z=np.flatnonzero(a if last else ~a)
    return int(z[-1] if last else z[0]) if len(z) else (-1 if last else 8)
   a,b=ep(s['confident'][c,k]),ep(s['confident'][c,8])
   cat='earlier' if a<b else 'later' if a>b else 'same';counts[cat]+=1;local[cat]+=1
   if not last:
    counts['S_beyond']+=a==8;counts['Fc_beyond']+=b==8;counts['both_beyond']+=(a==8 and b==8)
   d.append(int(a>b)-int(a<b));records.append([int(c),int(k),a,b])
  if d:cases.append(dict(case=int(c),difference=float(np.mean(d)),**{k:v/len(d) for k,v in local.items()}))
 from acd_stage6_analysis import diff
 return dict(pairs=len(records),cases=len(cases),counts=counts,case_averaged={k:float(np.mean([r[k] for r in cases])) for k in ['earlier','later','same']},pooled={k:counts[k]/len(records) for k in ['earlier','later','same']},interval=diff([r['difference'] for r in cases]),records=records)
def score(costs,s,keep,jbar,sd):
 # Truth and realized outcomes are confined to this scoring function.
 actual=[]
 for c in range(200):
  with np.load(RAW/f'conf/score_{c:03d}.npz') as d:actual.append(d['actual_cost'])
 actual=np.array(actual);truth=labels(actual,jbar)[:,np.r_[np.arange(8),37]]
 threshold=[]
 for h in [.90,.95,.99]:
  v={k:a.copy() for k,a in s.items()};v['confident']=s['p']>=h;v['climate']=s['climate_p']>=h;v['observation']=v['confident']&~v['climate']
  eligible=v['observation'][:,:8,0]&v['confident'][:,8,0,None]
  threshold.append(dict(threshold=h,first_loss=endpoint_fixed(v,keep,eligible),last_confident=endpoint_fixed(v,keep,eligible,True),same_lead=[r for r in comparisons(v,keep) if r['lead'] in [2,3]],accuracy=[r for r in calibration(v,truth,keep) if r['lead'] in [2,3]]))
 # Frozen global horizon rule through 3 LT (all tested lead windows in range).
 answer=np.broadcast_to(keep[:,None,None],(200,8,6));right=s['modal'][:,:8,:6]==truth[:,:8,:6]
 instance_answer=answer&s['confident'][:,8,None,:6]
 horizon=dict(instance_Fc_rule=dict(answers=int(instance_answer.sum()),correct=int((instance_answer&right).sum()),accuracy=float(right[instance_answer].mean())),answers=int(answer.sum()),correct=int((answer&right).sum()),accuracy=float(right[answer].mean()),definition='all eight S questions at tested leads 0 through 3 LT; global horizon rule')
 policies=[]
 for t in [3,5]:
  choice=np.array([j[:,:,t].mean(0).argmin() for j in costs])
  choices={'E':choice,'no_action':np.full(200,8),'always_uniform_decrease':np.zeros(200,dtype=int)}
  for frac in [0,.01,.02,.05,.1]:
   selected=np.full(200,8,dtype=int)
   for c,j in enumerate(costs):
    k=choice[c]
    if k<8 and np.mean(j[:,k,t]-j[:,8,t]<-frac*sd[k,t])>=.95:selected[c]=k
   choices[f'C_delta_{frac}']=selected
  c=np.flatnonzero(keep)
  for name,ch in choices.items():
   ch=ch.astype(int);v=actual[c,ch[c],t];base=actual[c,8,t];harm=v-base;bad=harm>0;nh=int(bad.sum());n=len(c)
   policies.append(dict(lead=float(LEADS[t]),policy=name,cases=n,acting_share=float((ch[c]!=8).mean()),mean_improvement=float((base-v).mean()),mean_regret=float((v-actual[c,:,t].min(1)).mean()),chosen_actions=np.bincount(ch[c],minlength=9).tolist(),harms=nh,harm_rate=nh/n,median_harm=float(np.median(harm[bad])) if nh else None,max_harm=float(harm[bad].max()) if nh else None,zero_harm_CP_upper=float(beta.ppf(.95,1,n)) if not nh else None))
 return threshold,horizon,policies
def run():
 frozen=json.load(open(ROOT/'receipts/acd_stage2.json'));jbar=frozen['null']['jbar'];null=np.array(frozen['null']['question_probabilities'])[np.r_[np.arange(8),37]]
 costs=[];rows=[];keep=[];essrows=[];hashes={}
 for c in range(200):
  p=RAW/f'conf/case_{c:03d}.npz'
  with np.load(p) as d:j=d['J'].copy();keep.append(not bool(d['excluded']))
  costs.append(j);s=binary(j,jbar,null);indicator=np.concatenate([j[:,:8]<j[:,8,None],(j[:,8]>jbar)[:,None]],axis=1)
  # Modal answer indicator, chain-major saved scoring draws; constant events get total count.
  indicator=indicator==s['modal'][None]
  shaped=indicator.reshape(4,len(j)//4,9,8).astype(float)
  ess=np.asarray(az.ess({'event':shaped},method='bulk')['event'])
  ess[indicator.max(0)==indicator.min(0)]=len(j)
  pt=(indicator.sum(0)+.5)/(len(j)+1);se=np.sqrt(pt*(1-pt)/ess)
  s['se']=se;s['uncertain']=np.abs(s['p']-.95)<2*se
  s['climate_p']=np.take_along_axis(null,s['modal'][...,None].astype(int),-1)[...,0]
  rows.append(s);essrows.append(ess);hashes[str(p)]=sha(p)
  if c%20==0:print('receipt case',c,flush=True)
 s=stack(rows);keep=np.array(keep);ess=np.array(essrows)
 eligible=s['observation'][:,:8,0]&s['confident'][:,8,0,None]
 assert int(eligible[keep].sum())==1332
 precision=[]
 for t,lead in enumerate(LEADS):
  for name,idx in [('S',slice(0,8)),('Fc',slice(8,9))]:
   mask=eligible&keep[:,None] if name=='S' else (eligible.any(1)&keep)[:,None]
   ee=ess[:,idx,t][mask];ss=s['se'][:,idx,t][mask];u=s['uncertain'][:,idx,t][mask]
   precision.append(dict(lead=float(lead),type=name,questions=len(ee),ESS=dist(ee),MC_se=dist(ss),threshold_uncertain_count=int(u.sum()),threshold_uncertain_share=float(u.mean())))
 variants=[]
 for direction in ['S_earlier_Fc_later','S_later_Fc_earlier']:
  v={k:a.copy() for k,a in s.items()}
  v['confident'][:,:8][s['uncertain'][:,:8]]=direction=='S_later_Fc_earlier'
  v['confident'][:,8][s['uncertain'][:,8]]=direction=='S_earlier_Fc_later'
  variants.append(dict(direction=direction,result=endpoint_fixed(v,keep,eligible)))
 with np.load(ROOT/'runs/stage4b_null/null_0.16.npz') as d:sd=(d['J'][:,:8]-d['J'][:,8,None]).std(0,ddof=1)
 sweep,horizon,policies=score(costs,s,keep,jbar,sd)
 b1=[];shares=[]
 for c in range(200):
  if not keep[c]:continue
  with np.load(OUT/f'conf_{c:03d}_0.16.npz') as d:
   v=d['terms'][:,:,[1,0,4],:];dd=d['J'][:,:8]-d['J'][:,8,None]
   cov=np.einsum('nkit,nkjt->kijt',v-v.mean(0),v-v.mean(0))/(len(v)-1);var=dd.var(0,ddof=1)
   components=np.stack([cov[:,0,0],cov[:,1,1],cov[:,2,2],2*cov[:,0,1],2*cov[:,0,2],2*cov[:,1,2]],axis=1)/var[:,None,:]
   assert np.max(np.abs(components.sum(1)-1))<1e-8
   shares.append(components)
 shares=np.array(shares)
 for t,lead in enumerate(LEADS):
  for name,ix in [('uniform',slice(0,1)),('seven_zero_mean',slice(1,8))]:
   b1.append(dict(lead=float(lead),patterns=name,terms={n:dist(shares[:,ix,k,t].ravel()) for k,n in enumerate(['Var_M','Var_I','Var_Res','2Cov_M_I','2Cov_M_Res','2Cov_I_Res'])}))
 result=dict(post_hoc=True,licenses_frozen_route=False,A=dict(A1=dict(precision=precision,worst_case=variants,eligibility='fixed original 1332 pairs; threshold flips do not select a new cohort'),A2=endpoint_fixed(s,keep,eligible),A3=sweep,A4=horizon),B=dict(B1=b1),D=policies,source_hashes=hashes)
 (DEST/'receipt_analyses.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
 print('receipt analyses COMPLETE',flush=True)
if __name__=='__main__':run()
