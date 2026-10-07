"""Freeze C adapter to unchanged Stage15D nested-RK4 gradients; no truth access."""
import os
os.environ.update(ACD_INHERITED_ROOT='/mnt/niva-array/work/aspen-forecast-decision-20261005/aspen/forecast_decision',JAX_PLATFORMS='cpu',JAX_ENABLE_X64='true',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
import json,time,sys,hashlib
from pathlib import Path
import numpy as np
import jax.numpy as jp
import acd_stage15_sensitivity as original
from acd_protocol import ROOT,LEADS
from acd_stage19_part3a_contract import sha,write
OUT=ROOT/'runs/stage19/part3a_sensitivity';OUT.mkdir(parents=True,exist_ok=True)

def gate():
 marker=ROOT/'runs/stage19/freeze_c_pushed.json'
 if not marker.exists():raise RuntimeError('Freeze C push required')
 r=json.loads(marker.read_text());assert r['freeze_sha256']==sha(ROOT/'ACD_STAGE19_FREEZE_C.md')
 contract=json.loads((ROOT/'receipts/acd_stage19_freeze_c.json').read_text())
 assert sha(Path(original.__file__))==contract['code_hashes']['acd_stage15_sensitivity.py']
 return contract

def calculate(c):
 gate();p=OUT/f'case_{c:03d}.json';source=ROOT/f'runs/stage19/main_forecast_{c:03d}.npz'
 if p.exists():
  r=json.loads(p.read_text());assert r['source_sha256']==sha(source);assert r['unchanged_gradient_source_sha256']==sha(Path(original.__file__));return r
 begin=time.monotonic()
 with np.load(source) as z:theta=z['theta'].copy();assert not bool(z['excluded'])
 mean=theta.mean(0);cov=np.cov(theta,rowvar=False,ddof=1)
 gj,gg=map(np.asarray,original.gradients(jp.asarray(mean)))
 r=dict(unchanged_gradient_source_sha256=sha(Path(original.__file__)),case=c,draws=len(theta),dimension=theta.shape[1],posterior_mean=mean.tolist(),posterior_covariance=cov.tolist(),J8_linearized_variance=np.einsum('ti,ij,tj->t',gj,cov,gj).tolist(),G_linearized_variance=np.einsum('kti,ij,ktj->kt',gg,cov,gg).tolist(),source_sha256=sha(source),seconds=time.monotonic()-begin)
 write(p,r);print('sensitivity',c,r['seconds'],flush=True);return r

def pilot():
 gate();begin=time.monotonic();rows=[calculate(c) for c in range(5)];wall=time.monotonic()-begin
 # Include compilation and pilot costs conservatively, using a single worker on four CPU cores.
 projection=sum(r['seconds'] for r in rows)/len(rows)*200
 namespace='acd-stage19-sensitivity';seed=int.from_bytes(hashlib.sha256(namespace.encode()).digest()[:8],'little')
 selected=list(range(200)) if projection<=4*3600 else sorted(map(int,np.random.default_rng(np.random.SeedSequence(seed)).choice(200,40,replace=False)))
 r=dict(pilot_cases=[x['case'] for x in rows],pilot_seconds=[x['seconds'] for x in rows],pilot_wall_seconds=wall,projected_seconds=projection,projected_hours=projection/3600,cores=sorted(os.sched_getaffinity(0)),workers=1,limit_hours=4,case_set=selected,namespace=namespace,seed=seed,all_instances=projection<=4*3600,ratios_computed=False,source_code_sha256=sha(Path(original.__file__)))
 write(ROOT/'receipts/acd_stage19_part3a_timing.json',r)

def run():
 gate();marker=ROOT/'runs/stage19/part3a_timing_pushed.json';assert marker.exists(),'Timing and case list must be committed and pushed before ratios'
 timing=json.loads((ROOT/'receipts/acd_stage19_part3a_timing.json').read_text());assert json.loads(marker.read_text())['receipt_sha256']==sha(ROOT/'receipts/acd_stage19_part3a_timing.json')
 rows=[]
 for c in timing['case_set']:
  r=calculate(c)
  with np.load(ROOT/f'runs/stage19/main_forecast_{c:03d}.npz') as z:J=z['J'];G=z['G']
  vj=J[:,8].var(0,ddof=1);vg=G.var(0,ddof=1);assert np.all(vj>0) and np.all(vg>0)
  r=dict(r,J8_empirical_variance=vj.tolist(),G_empirical_variance=vg.tolist(),J8_ratio=(np.asarray(r['J8_linearized_variance'])/vj).tolist(),G_ratio=(np.asarray(r['G_linearized_variance'])/vg).tolist());rows.append(r)
 summaries=[]
 for t,l in enumerate(LEADS):
  j=np.array([r['J8_ratio'][t] for r in rows]);g=np.array([r['G_ratio'] for r in rows])[:,:,t]
  summaries.append(dict(lead=float(l),J8_ratio=dict(zip(['q25','median','q75'],map(float,np.quantile(j,[.25,.5,.75])))),G_ratio=dict(zip(['q25','median','q75'],map(float,np.quantile(g,[.25,.5,.75]))))))
 tested=[r for r in summaries if r['lead']<=3]
 r=dict(cases=timing['case_set'],population=len(rows),summary=summaries,first_lead_median_outside_half_to_two={q:next((r['lead'] for r in summaries if not .5<=r[q]['median']<=2),None) for q in ['J8_ratio','G_ratio']},V1=all(.5<=next(r for r in summaries if r['lead']==2)[q]['median']<=2 for q in ['J8_ratio','G_ratio']),V2=all(.5<=r[q]['median']<=2 for r in tested for q in ['J8_ratio','G_ratio']),case_records=rows,unchanged_gradient_source_sha256=sha(Path(original.__file__)))
 write(ROOT/'receipts/acd_stage19_part3a_variance.json',r)
if __name__=='__main__':{'pilot':pilot,'run':run}[sys.argv[1]]()
