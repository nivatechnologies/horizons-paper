"""Stage9 authorized amplitude truth scoring and response readings."""
import os
os.environ.update(JAX_PLATFORMS='cpu',JAX_ENABLE_X64='true',NUMBA_NUM_THREADS='24',OPENBLAS_NUM_THREADS='1')
import numpy as np,json,time
from acd_stage9_receipts import DEST,dist,endpoint_fixed
from acd_stage6_analysis import ROOT,RAW,OUT,LEADS,WINDOWS,PATTERNS,physics,binary,stack,comparisons,calibration
def score_actual(amp):
 p=DEST/f'scoring_{amp}.npz'
 if not p.exists():
  actual=[]
  for c in range(200):
   with np.load(RAW/f'conf/truth/input_{c:03d}.npz') as d:x=d['true'][-1].copy()
   actual.append(physics.costs(physics.simulate(np.repeat(x[None],9,0),8+amp*PATTERNS,.01)))
  np.savez_compressed(p,J=np.array(actual))
 with np.load(p) as d:return d['J'].copy()
def run():
 frozen=json.load(open(ROOT/'receipts/acd_stage2.json'));jbar=frozen['null']['jbar']
 results=[];amps=[]
 for ai,amp in enumerate([.04,.64]):
  with np.load(ROOT/f'runs/stage4b_null/null_{amp}.npz') as d:jn=d['J']
  p=np.concatenate([(jn[:,:8]<jn[:,8,None]).mean(0),(jn[:,8]>jbar).mean(0)[None]])
  null=np.stack([1-p,p],-1)
  summaries=[];keep=[];metrics=[];allG=[];allD=[]
  for c in range(200):
   with np.load(RAW/f'conf/case_{c:03d}.npz') as d:keep.append(not bool(d['excluded']))
   with np.load(DEST/f'forward_{c:03d}.npz') as d:G=d['G'].copy();J=d['J'][:,ai].copy()
   D=J[:,:8]-J[:,8,None];allG.append(G);allD.append(D);summaries.append(binary(J,jbar,null))
   pp=(G<0).mean(0);qq=(D<0).mean(0);cg=np.maximum(pp,1-pp)>=.95;cd=np.maximum(qq,1-qq)>=.95
   gsd=G.std(0,ddof=1);dsd=D.std(0,ddof=1)
   corr=np.empty((8,8))
   for k in range(8):
    for t in range(8):corr[k,t]=np.corrcoef(G[:,k,t],D[:,k,t]/amp)[0,1]
   metrics.append(dict(sign=(np.sign(G)==np.sign(D/amp)).mean(0),corr=corr,relative=np.median(np.abs(D/amp-G)/np.maximum(np.abs(G),1e-12),0),pg=pp,pd=qq,cg=cg,cd=cd,classG=np.where(cg,np.where(pp>.5,-1,1),0),classD=np.where(cd,np.where(qq>.5,-1,1),0),zg=np.abs(G.mean(0))/gsd,zd=np.abs(D.mean(0))/dsd))
  keep=np.array(keep);s=stack(summaries);m=stack(metrics)
  flatG=np.concatenate([g for g,k in zip(allG,keep) if k]);flatD=np.concatenate([d for d,k in zip(allD,keep) if k])/amp
  for t,lead in enumerate(LEADS):
   x=m['cg'][keep,:,t].ravel();y=m['cd'][keep,:,t].ravel();observed=float((x==y).mean());chance=float(x.mean()*y.mean()+(1-x.mean())*(1-y.mean()))
   gx=m['classG'][keep,:,t].ravel();dy=m['classD'][keep,:,t].ravel();agree3=float((gx==dy).mean());chance3=sum(float((gx==i).mean()*(dy==i).mean()) for i in [-1,0,1])
   results.append(dict(amplitude=amp,three_class_agreement=agree3,three_class_cohen_kappa=(agree3-chance3)/(1-chance3) if chance3<1 else None,classification_definition='negative-confident / non-confident / positive-confident; binary-confidence results also retained',lead=float(lead),per_draw_sign_agreement=float((np.sign(flatG[:,:,t])==np.sign(flatD[:,:,t])).mean()),pooled_per_draw_correlation=float(np.corrcoef(flatG[:,:,t].ravel(),flatD[:,:,t].ravel())[0,1]),pooled_median_relative_difference=float(np.median(np.abs(flatD[:,:,t]-flatG[:,:,t])/np.maximum(np.abs(flatG[:,:,t]),1e-12))),within_pair_correlation=dist(m['corr'][keep,:,t].ravel()),median_relative_difference=float(np.median(m['relative'][keep,:,t])),relative_definition='equal case/action median of per-draw |D/a-G|/max(|G|,1e-12)',confidence_classification_agreement=observed,cohen_kappa=(observed-chance)/(1-chance) if chance<1 else None,median_z_G=float(np.median(m['zg'][keep,:,t])),median_z_D=float(np.median(m['zd'][keep,:,t])),probability_difference=dist((m['pd']-m['pg'])[keep,:,t].ravel())))
  real=score_actual(amp);truth=np.concatenate([real[:,:8]<real[:,8,None],(real[:,8]>jbar)[:,None]],1)
  eligible=s['observation'][:,:8,0]&s['confident'][:,8,0,None]
  amps.append(dict(amplitude=amp,comparisons=comparisons(s,keep),accuracy=calibration(s,truth,keep),first_loss=endpoint_fixed(s,keep,eligible),null_source=f'runs/stage4b_null/null_{amp}.npz'))
 (DEST/'forward_readings.json').write_text(json.dumps(dict(B2=results,B3=amps,post_hoc=True,licenses_frozen_route=False),indent=2,allow_nan=False)+'\n')
 print('B2/B3 complete',flush=True)
if __name__=='__main__':run()
