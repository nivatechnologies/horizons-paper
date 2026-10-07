"""Fresh-panel reference scoring; hidden histories are opened only in score_actual."""
import os
os.environ.update(JAX_PLATFORMS='cpu',JAX_ENABLE_X64='true',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
from pathlib import Path
import json,time,hashlib,numpy as np
from acd_protocol import ROOT,LEADS,WINDOWS,PATTERNS,physics
from acd_stage19_part2_gate import freeze_ready,digest
from acd_stage6_analysis import binary,stack,comparisons,loss,calibration
from acd_stats import one_sided
OUT=ROOT/'runs/stage19'
def write(p,d):p.write_text(json.dumps(d,indent=2,allow_nan=False)+'\n')
def score_actual():
 freeze_ready()
 target=OUT/'scoring.npz'
 if target.exists():
  with np.load(target) as z:return z['actual'].copy(),z['factual'].copy()
 actual=[];states=[]
 for c in range(200):
  p=OUT/'hidden'/f'input_{c:03d}.npz'
  with np.load(p) as z:x=z['true'][-1].copy()
  with (OUT/'scoring_access.jsonl').open('a') as log:log.write(json.dumps(dict(case=c,path=str(p.relative_to(ROOT)),array='true[-1]',sha256=digest(p),time=time.time(),caller=__file__))+'\n')
  traj=physics.simulate(np.repeat(x[None],len(PATTERNS),0),8+.16*PATTERNS,.01)
  actual.append(physics.costs(traj));states.append(traj[8])
  if c%20==0:print('realized case',c,flush=True)
 np.savez_compressed(target,actual=np.array(actual),J=np.array(actual),factual=np.array(states))
 return np.array(actual),np.array(states)
def mechanism(costs,gs,terms,jbar):
 shares=[];rows=[];metrics=[]
 for J,G,v in zip(costs,gs,terms):
  D=J[:,:8]-J[:,8,None];vv=v[:,:,[1,0,4],:]
  cov=np.einsum('nkit,nkjt->kijt',vv-vv.mean(0),vv-vv.mean(0))/(len(vv)-1)
  components=np.stack([cov[:,0,0],cov[:,1,1],cov[:,2,2],2*cov[:,0,1],2*cov[:,0,2],2*cov[:,1,2]],1)/D.var(0,ddof=1)[:,None,:]
  assert np.max(np.abs(components.sum(1)-1))<1e-8
  shares.append(components)
  pg=(G<0).mean(0);pd=(D<0).mean(0)
  cg=np.maximum(pg,1-pg)>=.95;cd=np.maximum(pd,1-pd)>=.95
  classG=np.where(cg,np.where(pg>.5,-1,1),0);classD=np.where(cd,np.where(pd>.5,-1,1),0)
  f=J[:,8]-jbar
  metrics.append(dict(agreement=classG==classD,classG=classG,classD=classD,zg=np.abs(G.mean(0))/G.std(0,ddof=1),zd=np.abs(D.mean(0))/D.std(0,ddof=1),zf=np.abs(f.mean(0))/f.std(0,ddof=1)))
 m=stack(metrics);shares=np.array(shares)
 for t,lead in enumerate(LEADS):
  case=m['agreement'][:,:,t].mean(1);lower=float(one_sided(case,.01,1));gx=m['classG'][:,:,t].ravel();dy=m['classD'][:,:,t].ravel();agree=float(case.mean());chance=sum(float((gx==i).mean()*(dy==i).mean()) for i in [-1,0,1])
  n=sum(len(g) for g in gs)*len(PATTERNS[:-1]);sign=sum(int((np.sign(g[:,:,t])==np.sign((j[:,:8]-j[:,8,None])[:,:,t]/.16)).sum()) for g,j in zip(gs,costs))/n
  rows.append(dict(lead=float(lead),mean_flow_variance_share_median=float(np.median(shares[:,1:8,0,t])),three_class_agreement=agree,three_class_case_lower_99=lower,three_class_kappa=(agree-chance)/(1-chance) if chance<1 else None,per_draw_sign_agreement=float(sign),median_z_D=float(np.median(m['zd'][:,:,t])),median_z_Fc=float(np.median(m['zf'][:,t])),median_z_D_over_median_z_Fc=float(np.median(m['zd'][:,:,t])/np.median(m['zf'][:,t])),median_z_G=float(np.median(m['zg'][:,:,t])),case_three_class_agreement=case.tolist()))
 return rows

def run():
 gate=freeze_ready();frozen=json.loads((ROOT/'receipts/acd_stage2.json').read_text());jbar=frozen['null']['jbar'];null=np.array(frozen['null']['question_probabilities'])[np.r_[np.arange(8),37]]
 costs=[];gs=[];terms=[];summ=[];hashes={}
 for c in range(200):
  p=OUT/f'main_forecast_{c:03d}.npz'
  with np.load(p) as z:
   assert not bool(z['excluded']);J=z['J'].copy();costs.append(J);gs.append(z['G'].copy());terms.append(z['terms'].copy())
  summ.append(binary(J,jbar,null));hashes[str(p.relative_to(ROOT))]=digest(p)
 keep=np.ones(len(costs),bool);s=stack(summ);actual,_=score_actual();truth=np.concatenate([actual[:,:8]<actual[:,8,None],(actual[:,8]>jbar)[:,None]],1)
 accuracy=calibration(s,truth,keep);same=comparisons(s,keep);paired=loss(s,keep);mech=mechanism(costs,gs,terms,jbar)
 for r in same:
  for k in ['seven_minus_Fc','all_minus_Fc','observation_minus_Fc']:r[k]['scope']='fresh confirmation; Freeze A'
 paired['interval']['scope']='fresh confirmation; Freeze A'
 at=lambda rows,lead:next(x for x in rows if x['lead']==lead)
 c1=at(accuracy,2)['S'];c2=paired['interval'];mr=at(mech,2)
 readings=dict(C1=dict(lead=2.,**c1,confirmed=c1['status']=='PASS',bound_type='original R0: one-sided 95% case bounds; original criterion unchanged'),C2=dict(**c2,confirmed=not (c2['empty'] or c2['offset']) and c2['point']<=-.20 and c2['upper']<0,direction_confirmed=not (c2['empty'] or c2['offset']) and c2['upper']<0,pairs=paired['actions'],cases=paired['cases']),C3=[],C4=[],M1=dict(lead=2.,value=mr['mean_flow_variance_share_median'],confirmed=mr['mean_flow_variance_share_median']>=.90,interval=None,criterion='frozen median threshold; no interval specified'),M2=dict(lead=2.,value=mr['three_class_agreement'],lower=mr['three_class_case_lower_99'],upper=1.,confirmed=mr['three_class_case_lower_99']<=mr['three_class_agreement'] and mr['three_class_case_lower_99']>=.75,bound_type='one-sided 99% case betting'),M3=dict(status='DESCRIPTIVE',expected_pattern=at(mech,0)['median_z_D_over_median_z_Fc']>1 and mr['median_z_D_over_median_z_Fc']<1))
 for lead in [2.,3.]:
  r=at(same,lead)
  for key,field in [('C3','observation_minus_Fc'),('C4','seven_minus_Fc')]:
   v=r[field];confirmed=(abs(v['point'])>=.15 and (v['lower']>0 or v['upper']<0)) if key=='C3' else v['upper']<0
   confirmed=confirmed and not (v['empty'] or v['offset'])
   readings[key].append(dict(lead=lead,**v,confirmed=confirmed))
 old6=json.loads((ROOT/'receipts/acd_stage6.json').read_text());old9=json.loads((ROOT/'receipts/acd_stage9.json').read_text());old17=json.loads((ROOT/'receipts/acd_stage17.json').read_text())
 oldm=next(r for r in old9['B']['B1'] if r['lead']==2 and r['patterns']=='seven_zero_mean')
 oldt=next(r for r in old17['A']['B2'] if r['lead']==2 and r['amplitude']==.16)
 confirmation=dict(C1=next(r['R0'] for r in frozen['R0'] if r['lead']==2),C2=frozen['R2b'],C3=frozen['R2a'],C4=[dict(lead=r['lead'],**r['seven_minus_Fc']) for r in old6['A']['A1']['comparisons'] if r['lead'] in [2,3]],M1=oldm['terms']['Var_M']['median'],M2=oldt,M3=[dict(lead=float(l),ratio=float(frozen['R1m']['z_D']['median'][t]/frozen['R1m']['z_F']['median'][t])) for t,l in enumerate(LEADS)])
 resolutions=[]
 for rr in [c2]+[r for k in ['C3','C4'] for r in readings[k]]:
  if rr.get('empty') or rr.get('offset'):resolutions.append(dict(rule='R-other',reason='empty or point-offset betting interval; no confirmatory interpretation',interval=rr))
 if mr['three_class_case_lower_99']>mr['three_class_agreement']:resolutions.append(dict(rule='R-other',reason='M2 lower bound exceeds observed mean; no confirmation'))
 receipt=dict(resolutions=resolutions,confirmation_panel=confirmation,panel='fresh confirmation',freeze_b=gate,source_hashes=hashes,realized_cost_sha256=digest(OUT/'scoring.npz'),known_forcing_deferred=True,accuracy=accuracy,same_lead=same,paired_first_loss=paired,mechanism=mech,confirmatory=readings,source_code_hashes={p:digest(ROOT/p) for p in ['acd_stage19_score.py','acd_stage6_analysis.py','acd_stage9_receipts.py','acd_stage9_forward_readings.py','acd_stats.py']})
 write(ROOT/'receipts/acd_stage19_reference.json',receipt)
 text=['# Stage 19 fresh-panel readings','', 'Reference readings use the fresh panel under Freeze A and Freeze B. Known-forcing comparisons remain deferred to Part 3.','', '| Reading | Fresh value | Bound | Confirmation-panel comparison | Result |','|---|---:|---|---|---|']
 for key,rr in readings.items():
  if key=='M3':continue
  for r in rr if isinstance(rr,list) else [rr]:
   value=r.get('point',r.get('value',r.get('case_accuracy')));bound=[r.get('lower',r.get('case_lower')),r.get('upper',r.get('case_upper'))]
   text.append(f"| {key}, lead {r.get('lead','paired')} | {value} | {bound} | {confirmation[key]} | {'PASS' if r['confirmed'] else 'FAIL'} |")
 text+=['','The original R0 criterion retains its one-sided 95% bounds. M1 uses the median criterion specified in Freeze B without an invented interval. All remaining mechanism leads and crossover ratios are descriptive.','', 'Full per-lead readings and case records: receipts/acd_stage19_reference.json.']
 (ROOT/'ACD_STAGE19_READING.md').write_text('\n'.join(text)+'\n');print(json.dumps(readings,indent=2),flush=True)
if __name__=='__main__':run()
