"""Freeze C known-forcing and descriptive readings. Outcomes opened only in score()."""
import os
os.environ.update(ACD_INHERITED_ROOT='/mnt/niva-array/work/aspen-forecast-decision-20261005/aspen/forecast_decision',JAX_PLATFORMS='cpu',JAX_ENABLE_X64='true',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',NUMBA_NUM_THREADS='2')
import json,numpy as np
from pathlib import Path
from acd_protocol import ROOT,LEADS
from acd_stage19_part3a_contract import sha,write
from acd_stage6_analysis import binary,stack,comparisons,loss,calibration
from acd_stats import difference_interval,cp_bounds
from acd_stage9_receipts import dist
from acd_stage19_learned import model_inputs
from acd_stage13_analysis import choices
from acd_stage17_events import error_bounds
os.environ['NUMBA_NUM_THREADS']='2'
OUT=ROOT/'runs/stage19'

def gate():
 r=json.loads((OUT/'freeze_c_pushed.json').read_text());assert r['freeze_sha256']==sha(ROOT/'ACD_STAGE19_FREEZE_C.md')
 contract=json.loads((ROOT/'receipts/acd_stage19_freeze_c.json').read_text())
 for p,h in contract['code_hashes'].items():assert sha(ROOT/p)==h,p
 for p,h in contract['knownF_forecast_hashes'].items():assert sha(ROOT/p)==h,p
 return contract

def correlation(theta,J):
 result=[]
 for t in [3,5]:
  values=np.concatenate([J[:,8:9,t],J[:,:8,t]-J[:,8,None,t]],axis=1)
  result.append(dict(lead=float(LEADS[t]),J8=float(np.corrcoef(theta[:,-1],values[:,0])[0,1]),D=[float(np.corrcoef(theta[:,-1],values[:,k])[0,1]) for k in range(1,values.shape[1])]))
 return result

def panel(Js,jbar,null,truth,keep):
 example=binary(Js[int(np.flatnonzero(keep)[0])],jbar,null)
 s=stack([binary(j,jbar,null) if included else {key:np.zeros_like(value) for key,value in example.items()} for j,included in zip(Js,keep)]);rows=[]
 for t,l in enumerate(LEADS):
  rhos=[];cs=[];zd=[];zf=[]
  for j in [v for v,k in zip(Js,keep) if k]:
   d=j[:,:8,t]-j[:,8,None,t];va=j[:,:8,t].var(0,ddof=1);vf=j[:,8,t].var(ddof=1)
   cov=np.mean((j[:,:8,t]-j[:,:8,t].mean(0))*(j[:,8,None,t]-j[:,8,t].mean()),axis=0)*len(j)/(len(j)-1)
   rhos.extend(cov/np.sqrt(va*vf));cs.extend(d.var(0,ddof=1)/(va+vf));zd.extend(np.abs(d.mean(0))/d.std(0,ddof=1));f=j[:,8,t]-jbar;zf.append(abs(f.mean())/f.std(ddof=1))
  rows.append(dict(lead=float(l),S8_confident_share=float(s['confident'][keep,:8,t].mean()),S7_confident_share=float(s['confident'][keep,1:8,t].mean()),observation_S_share=float(s['observation'][keep,:8,t].mean()),Fc_confident_share=float(s['confident'][keep,8,t].mean()),rho=dist(np.asarray(rhos)),c=dist(np.asarray(cs)),z_D=dist(np.asarray(zd)),z_F=dist(np.asarray(zf))))
 accuracy=calibration({key:value[keep] for key,value in s.items()},truth[keep],np.ones(int(keep.sum()),bool))
 for reading in accuracy:reading['S'].pop('included_excluded',None)
 for t,row in enumerate(accuracy):
  m=s['confident'][keep,8,t];right=s['modal'][keep,8,t]==truth[keep,8,t];n=int(m.sum());correct=int((m&right).sum());row['Fc_CP_one_sided95']=dict(answers=n,correct=correct,accuracy=correct/n if n else None,bounds=list(cp_bounds(correct,n)) if n else None)
 return dict(population=int(keep.sum()),accuracy=accuracy,shares=rows,comparisons=[r for r in comparisons(s,keep) if r['lead'] in [2,3]],paired_first_loss=loss(s,keep)),s

def score():
 contract=gate();frozen=json.loads((ROOT/'receipts/acd_stage2.json').read_text());jbar=frozen['null']['jbar'];null=np.array(frozen['null']['question_probabilities'])[np.r_[np.arange(8),37]]
 # The existing realized cache is opened exclusively in this scoring function.
 cache=OUT/'scoring.npz';assert sha(cache)==contract['realized_cache_sha256']
 with np.load(cache) as z:actual=z['actual'].copy()
 with (OUT/'scoring_access.jsonl').open('a') as log:log.write(json.dumps(dict(caller=__file__,path=str(cache.relative_to(ROOT)),purpose='Freeze C known-forcing accuracy and descriptive fresh-panel replications',sha256=sha(cache)))+'\n')
 truth=np.concatenate([actual[:,:8]<actual[:,8,None],(actual[:,8]>jbar)[:,None]],axis=1)
 Js=[];known=[];keep=[];std=[];corr=[]
 for c in range(len(actual)):
  with np.load(OUT/f'main_forecast_{c:03d}.npz') as z:j=z['J'].copy();theta=z['theta'].copy();assert not bool(z['excluded'])
  Js.append(j);std.append(float(theta[:,-1].std(ddof=1)));corr.append(correlation(theta,j))
  with np.load(OUT/f'knownF_forecast_{c:03d}.npz') as z:known.append(z['J'].copy());keep.append(not bool(z['excluded']))
 keep=np.asarray(keep);assert np.flatnonzero(~keep).tolist()==contract['knownF_excluded']
 k,s=panel(known,jbar,null,truth,keep);main,ms=panel(Js,jbar,null,truth,keep)
 k1=k['paired_first_loss']['interval'];k2=[dict(lead=r['lead'],**r['seven_minus_Fc']) for r in k['comparisons']];k3=next(r['S'] for r in k['accuracy'] if r['lead']==2)
 coupling=[dict(lead=float(LEADS[t]),J8=dist(np.array([r[i]['J8'] for r in corr])),D=dist(np.array([r[i]['D'] for r in corr]).ravel())) for i,t in enumerate([3,5])]
 descriptivecoupling=[dict(lead=float(LEADS[t]),J8=dist(np.array([r[i]['J8'] for r,q in zip(corr,keep) if q])),D=dist(np.array([r[i]['D'] for r,q in zip(corr,keep) if q]).ravel())) for i,t in enumerate([3,5])]
 intervals=[]
 for t in [3,5]:
  for q,values in [('seven_S',s['confident'][:,1:8,t].mean(1)-ms['confident'][:,1:8,t].mean(1)),('Fc',s['confident'][:,8,t].astype(float)-ms['confident'][:,8,t])]:intervals.append(dict(lead=float(LEADS[t]),quantity=q,population=int(keep.sum()),direction='known-forcing minus main posterior',interval=difference_interval(values[keep])))
 models={m:model_inputs(m,jbar,null) for m in ['posterior','CNN-20k','CNN-F','CNN-noF']}
 seed=contract['seeds']['ids']['acd-stage19-ties'];tieorder=np.random.default_rng(np.random.SeedSequence(seed)).permutation(len(actual)*8);tierank=np.argsort(tieorder)
 matching={};selected={};transfer=[]
 for name,(costs,means,valid,summary,physics) in models.items():
  assert valid.all(),'R-other: invalid saved model; no survivor conditioning'
  matching[name]=[];selected[name]=[]
  for t in [3,5]:
   p=summary['p'][:,:8,t];wrong=summary['modal'][:,:8,t]!=truth[:,:8,t]
   for group,ks in [('all_eight',np.arange(8)),('seven_zero_mean',np.arange(1,8))]:
    ids=np.array([c*8+k for c in range(len(actual)) for k in ks]);order=ids[np.lexsort((tierank[ids],-p.ravel()[ids]))]
    for coverage in [.5,.7]:
     n=int(round(coverage*len(order)));mask=np.zeros(p.size,bool);mask[order[:n]]=True;mask=mask.reshape(p.shape)
     matching[name].append(dict(lead=float(LEADS[t]),patterns=group,coverage=coverage,population=len(actual),questions=len(ids),answers=n,selected_case_action_ids=order[:n].tolist(),pooled_error=float(wrong[mask].mean()),**error_bounds(mask,wrong)))
   for policy,ch in choices(costs,valid,t,np.zeros((8,len(LEADS)))).items():
    if policy not in ['E','C_delta_0']:continue
    acted=np.flatnonzero(ch!=8);probs=np.array([(costs[c][:,ch[c],t]<costs[c][:,8,t]).mean() for c in acted]);d=actual[acted,ch[acted],t]-actual[acted,8,t]
    selected[name].append(dict(lead=float(LEADS[t]),policy=policy,population=len(actual),actions=int(len(acted)),expected_harms=float((1-probs).sum()),realized_harms=int((d>=0).sum()),strict_positive_harms=int((d>0).sum()),zero_effect_ties=int((d==0).sum()),predicted_benefit_probabilities=probs.tolist(),acted_case_indices=acted.tolist(),definition='Stage17C non-lowering D>=0; strict positive Part2 counts and ties separate'))
  if name in ['CNN-F','CNN-noF']:
   grid=np.logspace(-3,0,41);rows=[];t=3
   for c,(j,pj) in enumerate(zip(costs,physics)):
    d=pj[:,:8,t]-pj[:,8,None,t];dh=j[:,:8,t]-j[:,8,None,t];mse=((dh-d)**2).mean(0);bounds=(np.abs(d)[:,:,None]<=grid).mean(0)+mse[:,None]/grid**2
    rows.extend([dict(case=c,action=a,minimized_bound=float(v),error_MSE=float(mse[a])) for a,v in enumerate(bounds.min(1))])
   b=np.array([r['minimized_bound'] for r in rows]);transfer.append(dict(model=name,lead=float(LEADS[t]),case_actions=rows,median_minimized_bound=float(np.median(b)),share_bound_below_0_05=float((b<.05).mean()),share_bound_at_least_one=float((b>=1).mean())))
 confirmed=lambda r:r['upper']<0 and not(r['empty'] or r['offset'])
 r=dict(freeze='C',fresh_panel=True,licenses_frozen_route=False,known_forcing=k,main_on_knownF_cohort=main,main_all_forcing_correlations=coupling,main_matched_forcing_correlations=descriptivecoupling,main_forcing_sd=dist(np.asarray(std)[keep]),paired_share_differences=intervals,K1=dict(**k1,confirmed=confirmed(k1)),K2=dict(rows=k2,confirmed=all(confirmed(x) for x in k2)),K3=dict(**k3,confirmed=k3['status']=='PASS',bound_type='original R0 one-sided95% case betting'),K4=dict(population=len(actual),D_median=coupling[0]['D']['median'],J8_median=coupling[0]['J8']['median'],confirmed=abs(coupling[0]['D']['median'])<=.05 and coupling[0]['J8']['median']>=.30,bound_type='median thresholds; no interval'),descriptive=dict(realized_counts_previously_reported_in_part2=True,matching=matching,selected_action=selected,transfer=transfer,ranking=dict(namespace='acd-stage19-ties',seed=seed,tie_order=tieorder.tolist(),rule='descending modal probability; ties by one fixed seeded permutation; exact integer counts by round, unchanged corrected Stage15A')),
 first_panel=dict(known_forcing=json.loads((ROOT/'receipts/acd_stage15_knownF.json').read_text()),variance=json.loads((ROOT/'receipts/acd_stage15_sensitivity.json').read_text()),matching=json.loads((ROOT/'receipts/acd_stage15_matching.json').read_text()),selected_action=json.loads((ROOT/'receipts/acd_stage17.json').read_text())['C'],transfer=json.loads((ROOT/'receipts/acd_stage17.json').read_text())['D']),resolutions=[],realized_cache_sha256=sha(cache))
 # Avoid duplicating per-case sampler/covariance records from already registered first-panel receipts.
 for key in ['known_forcing','variance']:
  r['first_panel'][key].pop('cases' if key=='known_forcing' else 'case_records',None)
 variance=json.loads((ROOT/'receipts/acd_stage19_part3a_variance.json').read_text());r['variance']=variance;r['V1']=variance['V1'];r['V2']=variance['V2'];write(ROOT/'receipts/acd_stage19_part3a.json',r)
if __name__=='__main__':score()
