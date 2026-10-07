"""Stage 15D full-covariance linearized-variance diagnostic; no outcome access."""
import os
os.environ.update(JAX_PLATFORMS='cpu',JAX_ENABLE_X64='true',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',XLA_FLAGS='--xla_cpu_multi_thread_eigen=false')
import json,hashlib,time
from pathlib import Path
import numpy as np
import jax
jax.config.update('jax_enable_x64',True)
import jax.numpy as jp
from acd_protocol import ROOT,PATTERNS,TICKS,WINDOWS,LEADS
from acd_stage6_forward import RAW
from acd_posterior import history,step
FORWARD=Path(os.environ.get('ACD_STAGE9_FORWARD_ROOT','/home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9'))
OUT=ROOT/'runs/stage15_sensitivity';OUT.mkdir(parents=True,exist_ok=True)
W=np.zeros((len(TICKS),len(LEADS)))
for t,w in enumerate(WINDOWS):W[w,t]=1/len(w)
def costs(theta,a):
 x=history(theta,.01)[-1];z=jp.broadcast_to(x,(len(PATTERNS),len(x)));f=theta[-1]+a*jp.asarray(PATTERNS)
 def tick(z,w):
  energy=.5*jp.mean(z*z,-1)
  # Differentiate every stage of this exact RK4 map, including the observation history.
  z=jax.lax.fori_loop(0,5,lambda _,v:jax.vmap(lambda state,forcing:step(state,forcing,.01))(v,f),z)
  return z,energy[:,None]*w
 _,values=jax.lax.scan(tick,z,jp.asarray(W));return values.sum(0)
def tangent(theta):return jax.jvp(lambda a:costs(theta,a)[:8],(jp.array(0.,dtype=jp.float64),),(jp.array(1.,dtype=jp.float64),))[1]
@jax.jit
def gradients(theta):return jax.jacfwd(lambda v:costs(v,jp.array(0.,dtype=jp.float64))[8])(theta),jax.jacfwd(tangent)(theta)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run():
 namespace='acd-stage15-sensitivity';seed=int.from_bytes(hashlib.sha256(namespace.encode()).digest()[:8],'little');rng=np.random.default_rng(np.random.SeedSequence(seed));selected=np.sort(rng.choice(200,40,replace=False));rows=[]
 for c in selected:
  c=int(c);target=OUT/f'case_{c:03d}.json'
  if target.exists():rows.append(json.loads(target.read_text()));continue
  start=time.monotonic();source=RAW/f'conf/case_{c:03d}.npz';forward=FORWARD/f'forward_{c:03d}.npz'
  with np.load(source) as d:theta=d['theta'].copy();J=d['J'].copy();excluded=bool(d['excluded'])
  if excluded:raise RuntimeError('R-other: fixed sensitivity case excluded; retain selection and report, do not substitute')
  with np.load(forward) as d:G=d['G'].copy()
  assert theta.shape[0]==G.shape[0]==J.shape[0]
  mean=theta.mean(0);cov=np.cov(theta,rowvar=False,ddof=1);gj,gg=map(np.asarray,gradients(jp.asarray(mean)))
  predj=np.einsum('ti,ij,tj->t',gj,cov,gj);predg=np.einsum('kti,ij,ktj->kt',gg,cov,gg);varj=J[:,8].var(0,ddof=1);varg=G.var(0,ddof=1)
  assert np.all(varj>0) and np.all(varg>0),'R-other: zero empirical variance; ratio undefined'
  row=dict(case=c,draws=len(theta),dimension=theta.shape[1],posterior_mean=mean.tolist(),posterior_covariance=cov.tolist(),J8_linearized_variance=predj.tolist(),J8_empirical_variance=varj.tolist(),J8_ratio=(predj/varj).tolist(),G_linearized_variance=predg.tolist(),G_empirical_variance=varg.tolist(),G_ratio=(predg/varg).tolist(),source_sha256=sha(source),tangent_source_sha256=sha(forward),seconds=time.monotonic()-start)
  target.write_text(json.dumps(row,indent=2,allow_nan=False)+'\n');rows.append(row);print(c,row['seconds'],flush=True)
 summaries=[]
 for t,lead in enumerate(LEADS):
  j=np.array([r['J8_ratio'][t] for r in rows]);g=np.array([r['G_ratio'] for r in rows])[:,:,t]
  summaries.append(dict(lead=float(lead),J8_ratio=dict(zip(['q25','median','q75'],map(float,np.quantile(j,[.25,.5,.75])))),G_ratio=dict(zip(['q25','median','q75'],map(float,np.quantile(g,[.25,.5,.75])))),G_by_pattern=[dict(pattern=k,**dict(zip(['q25','median','q75'],map(float,np.quantile(g[:,k],[.25,.5,.75]))))) for k in range(g.shape[1])]))
 outside={q:next((r['lead'] for r in summaries if not .5<=r[q]['median']<=2),None) for q in ['J8_ratio','G_ratio']}
 receipt=dict(post_hoc=True,descriptive=True,licenses_frozen_route=False,namespace=namespace,seed=seed,cases=selected.tolist(),covariance='full sample covariance of all first-frame state coordinates and forcing, ddof1; no diagonal approximation; includes state-forcing cross terms',derivative='nested forward-mode JAX AD through identical float64 RK4 stages and observation history; gradient of amplitude-JVP at zero',summary=summaries,first_lead_median_outside_half_to_two=outside,case_records=rows,source_code_hashes={str(p):sha(p) for p in [Path(__file__),ROOT/'acd_posterior.py']})
 (ROOT/'receipts/acd_stage15_sensitivity.json').write_text(json.dumps(receipt,indent=2,allow_nan=False)+'\n')
 lines=['# Stage 15D linearized variance','','Post hoc, descriptive; licenses no frozen route. No realized outcomes opened. Full covariance includes forcing and its cross-covariances with all state coordinates. Ratios compare gradient–covariance–gradient variance to the empirical saved-draw variance. G summary weights every selected case/action equally.','','| Lead | J8 ratio median | J8 q25 | J8 q75 | G ratio median | G q25 | G q75 |','|---|---:|---:|---:|---:|---:|---:|']
 for r in summaries:lines.append('| '+' | '.join(map(str,[r['lead'],r['J8_ratio']['median'],r['J8_ratio']['q25'],r['J8_ratio']['q75'],r['G_ratio']['median'],r['G_ratio']['q25'],r['G_ratio']['q75']]))+' |')
 lines+=['','First tested lead with median ratio outside the frozen range: '+str(outside)+'.',''];(ROOT/'ACD_STAGE15_SENSITIVITY.md').write_text('\n'.join(lines))
if __name__=='__main__':run()
