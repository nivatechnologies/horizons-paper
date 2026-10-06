"""Authorized Stage9 CPU forward JVP and amplitude forecasts; no truth access."""
import os
os.environ.update(JAX_PLATFORMS='cpu',JAX_ENABLE_X64='true',NUMBA_NUM_THREADS='8',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
import jax,jax.numpy as jp,numpy as np,time,json
from acd_protocol import ROOT,PATTERNS,WINDOWS,TICKS,physics
from acd_stage6_forward import RAW
OUT=ROOT/'runs/stage9';OUT.mkdir(parents=True,exist_ok=True)
W=np.zeros((len(TICKS),8))
for t,w in enumerate(WINDOWS):W[w,t]=1/len(w)
def rhs(x,f):return (jp.roll(x,-1,-1)-jp.roll(x,2,-1))*jp.roll(x,1,-1)-x+f
def step(x,f):
 k1=rhs(x,f);k2=rhs(x+.005*k1,f);k3=rhs(x+.005*k2,f);k4=rhs(x+.01*k3,f)
 return x+.01/6*(k1+2*k2+2*k3+k4)
@jax.jit
def tangent(x,F):
 def costs(a):
  z=jp.broadcast_to(x[:,None,:],(len(x),8,40));f=F[:,None,None]+a*jp.asarray(PATTERNS[:8])[None]
  def tick(z,w):
   energy=.5*jp.mean(z*z,-1)
   for _ in range(5):z=step(z,f)
   return z,energy[:,:,None]*w
  _,v=jax.lax.scan(tick,z,jp.asarray(W))
  return v.sum(0)
 return jax.jvp(costs,(jp.array(0.,dtype=jp.float64),),(jp.array(1.,dtype=jp.float64),))

from numba import njit,prange
@njit(cache=True)
def rhs_jvp(x,v,p):
 out=np.empty(40)
 for i in range(40):
  out[i]=(v[(i+1)%40]-v[(i-2)%40])*x[(i-1)%40]+(x[(i+1)%40]-x[(i-2)%40])*v[(i-1)%40]-v[i]+p[i]
 return out
@njit(cache=True)
def rk4_jvp(x,v,f,p):
 k1=physics.rhs(x,f);v1=rhs_jvp(x,v,p)
 k2=physics.rhs(x+.005*k1,f);v2=rhs_jvp(x+.005*k1,v+.005*v1,p)
 k3=physics.rhs(x+.005*k2,f);v3=rhs_jvp(x+.005*k2,v+.005*v2,p)
 k4=physics.rhs(x+.01*k3,f);v4=rhs_jvp(x+.01*k3,v+.01*v3,p)
 return x+.01/6*(k1+2*k2+2*k3+k4),v+.01/6*(v1+2*v2+2*v3+v4)
@njit(cache=True,parallel=True)
def tangent_forward(x,F,patterns,weights):
 g=np.zeros((len(x),8,8))
 for b in prange(len(x)):
  for k in range(8):
   xx=x[b].copy();v=np.zeros(40);f=np.full(40,F[b])
   for t in range(len(weights)):
    z=np.mean(xx*v)
    for lead in range(8):g[b,k,lead]+=z*weights[t,lead]
    for _ in range(5):xx,v=rk4_jvp(xx,v,f,patterns[k])
 return g

def run():
 with np.load(RAW/'conf/case_000.npz') as check:
  xx=check['x0'][:8];ff=check['theta'][:8,40]
 _,reference=tangent(xx,ff);got=tangent_forward(xx,ff,PATTERNS[:8],W)
 error=float(np.max(np.abs(got-np.asarray(reference))))
 assert error<1e-9,error
 (OUT/'jvp_implementation_check.json').write_text(json.dumps(dict(max_abs_difference=error,reference='JAX jvp of identical float64 RK4 cost map',production='explicit forward-mode JVP propagated through all RK4 stages',draws=8,patterns=8,leads=8),indent=2)+'\n')
 print('JVP check',error,flush=True)
 for c in range(200):
  target=OUT/f'forward_{c:03d}.npz'
  if target.exists():continue
  start=time.monotonic()
  with np.load(RAW/f'conf/case_{c:03d}.npz') as d:x=d['x0'].copy();F=d['theta'][:,40].copy()
  gg=[];jj=[]
  for b in range(0,len(x),256):
   xx=x[b:b+256];ff=F[b:b+256];g=tangent_forward(xx,ff,PATTERNS[:8],W);gg.append(g)
   values=[]
   for amp in [.04,.64]:
    tr=physics.simulate(np.repeat(xx,9,0),(ff[:,None,None]+amp*PATTERNS[None]).reshape(-1,40),.01)
    values.append(physics.costs(tr).reshape(len(xx),9,8))
   jj.append(np.stack(values,1))
  G=np.concatenate(gg);J=np.concatenate(jj)
  np.savez_compressed(target,G=G,J=J,amplitudes=np.array([.04,.64]))
  print(c,len(x),round(time.monotonic()-start,2),flush=True)
if __name__=='__main__':run()
