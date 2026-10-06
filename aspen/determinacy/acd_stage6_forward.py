"""Post-hoc Stage6: forward-only CPU kernels, never opens truth or invokes inference fits."""
import os
os.environ['JAX_PLATFORMS']='cpu'
os.environ['JAX_ENABLE_X64']='true'
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
os.environ.setdefault('NUMBA_NUM_THREADS','32')
from pathlib import Path
import numpy as np
from numba import njit,prange
from acd_protocol import physics,PATTERNS,LEADS,WINDOWS,TICKS,SIGMA,ROOT
RAW=Path('/home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs')
OUT=ROOT/'runs/stage6'
OUT.mkdir(exist_ok=True,parents=True)
DT=.01
WEIGHTS=np.zeros((8,len(TICKS)))
for t,w in enumerate(WINDOWS):WEIGHTS[t,w]=1/len(w)
@njit(cache=True)
def stages(x,f):
 a=physics.rhs(x,f);bstate=x+.5*DT*a;b=physics.rhs(bstate,f)
 cstate=x+.5*DT*b;c=physics.rhs(cstate,f);dstate=x+DT*c;d=physics.rhs(dstate,f)
 return np.stack((x,bstate,cstate,dstate)),x+DT/6*(a+2*b+2*c+d)
@njit(cache=True,parallel=True)
def forward(xinit,F,amp,patterns,weights):
 n=len(F);nt=weights.shape[1];ns=(nt-1)*5
 J=np.zeros((n,9,8));block=np.zeros((n,9,8));terms=np.zeros((n,8,7,8));sumstate=np.zeros((n,nt,40))
 for b in prange(n):
  factual=np.empty((nt,40));sub=np.empty((ns,4,40));x=xinit[b].copy();f=np.full(40,F[b])
  for st in range(ns+1):
   if st%5==0:factual[st//5]=x
   if st<ns:sub[st],x=stages(x,f)
  sumstate[b]=factual
  for k in range(9):
   action=np.empty((nt,40));cis=np.zeros(nt);cfs=np.zeros(nt)
   x=xinit[b].copy();ci=0.;cf=0.;f=F[b]+amp*patterns[k]
   for st in range(ns+1):
    if st%5==0:
     tick=st//5;action[tick]=x;cis[tick]=ci;cfs[tick]=cf
    if st<ns:
     xs,xnext=stages(x,f)
     gi=np.empty(4);gf=np.empty(4)
     for z in range(4):
      gi[z]=amp*np.sum(patterns[k]*xs[z])/40
      gf[z]=F[b]*np.mean(xs[z]-sub[st,z])
     ki=np.empty(4);kf=np.empty(4)
     ki[0]=-2*ci+gi[0];kf[0]=-2*cf+gf[0]
     ki[1]=-2*(ci+.5*DT*ki[0])+gi[1];kf[1]=-2*(cf+.5*DT*kf[0])+gf[1]
     ki[2]=-2*(ci+.5*DT*ki[1])+gi[2];kf[2]=-2*(cf+.5*DT*kf[1])+gf[2]
     ki[3]=-2*(ci+DT*ki[2])+gi[3];kf[3]=-2*(cf+DT*kf[2])+gf[3]
     ci+=DT/6*(ki[0]+2*ki[1]+2*ki[2]+ki[3]);cf+=DT/6*(kf[0]+2*kf[1]+2*kf[2]+kf[3])
     x=xnext
   for tick in range(nt):
    energy=.5*np.mean(action[tick]**2);eb=.5*np.mean(action[tick,:10]**2)
    for t in range(8):
     w=weights[t,tick];J[b,k,t]+=w*energy;block[b,k,t]+=w*eb
     if k<8:
      dx=action[tick]-factual[tick]
      projection=np.mean(factual[tick]*dx);displacement=.5*np.mean(dx*dx)
      D=energy-.5*np.mean(factual[tick]**2)
      terms[b,k,0,t]+=w*cis[tick]
      terms[b,k,1,t]+=w*cfs[tick]
      terms[b,k,2,t]+=w*projection
      terms[b,k,3,t]+=w*displacement
      terms[b,k,4,t]+=w*(D-cis[tick]-cfs[tick])
      terms[b,k,5,t]+=w*amp*np.sum(patterns[k]*action[tick])/40
      terms[b,k,6,t]+=w*F[b]*np.mean(dx)
 return J,block,terms,sumstate
def null():
 target=OUT/'null_block.npz'
 if target.exists():return
 with np.load(ROOT/'runs/stage4b_null/states.npz') as d:x=d['states'].copy()
 # Identical saved null states, no new climatological spin-up.
 js=[];blocks=[]
 for first in range(0,len(x),128):
  v=x[first:first+128]
  trajectory=physics.simulate(np.repeat(v,9,axis=0),(8+.16*PATTERNS)[None].repeat(len(v),axis=0).reshape(-1,40),DT).reshape(len(v),9,len(TICKS),40)
  js.append(physics.costs(trajectory));blocks.append(np.stack([(.5*np.mean(trajectory[...,w,:10]**2,axis=-1)).mean(-1) for w in WINDOWS],-1))
 J=np.concatenate(js);blk=np.concatenate(blocks)
 np.savez_compressed(target,J=J,block=blk,jbar_block=blk[:,8].mean(),sd_D=(J[:,:8]-J[:,8,None]).std(0,ddof=1))
 print('saved-state null block complete',flush=True)
def case(panel,c,amp):
 import json,time
 target=OUT/f'{panel}_{c:03d}_{amp}.npz'
 if target.exists():
  with np.load(target) as cached:
   if cached["terms"].shape[2]==7:return
 started=time.perf_counter()
 with np.load(RAW/f'{panel}/case_{c:03d}.npz') as d:
  x=d['x0'].copy();theta=d['theta'].copy();saved=d['J'].copy();excluded=bool(d['excluded'])
 J,blk,terms,state=forward(x,theta[:,40],amp,PATTERNS,WEIGHTS)
 delta=J[:,:8]-J[:,8,None]
 check={'case':c,'panel':panel,'amplitude':amp,'draws':len(x),'excluded':excluded,
  'projection_closure_max_abs':float(np.max(np.abs(delta-terms[:,:,2]-terms[:,:,3]))),
  'energy_budget_closure_max_abs':float(np.max(np.abs(terms[:,:,4]))),'saved_J_max_abs':float(np.max(np.abs(J-saved))) if amp==.16 else None,
  'seconds':time.perf_counter()-started}
 if amp==.16 and check['saved_J_max_abs']>1e-12:raise RuntimeError('Forward map mismatch '+str(check))
 if check['projection_closure_max_abs']>1e-12:raise RuntimeError('Projection identity mismatch')
 # Retain all per-draw costs/contributions. State posterior mean suffices for skill scoring.
 np.savez_compressed(target,J=J,block=blk,terms=terms,factual_mean=state.mean(0))
 target.with_suffix('.json').write_text(json.dumps(check,indent=2)+'\n')
 print(panel,c,len(x),'seconds',round(check['seconds'],2),flush=True)
def run():
 null()
 for panel,amp in [('conf',.16),('dev',.64)]:
  for c in range(200):case(panel,c,amp)
if __name__=='__main__':run()
