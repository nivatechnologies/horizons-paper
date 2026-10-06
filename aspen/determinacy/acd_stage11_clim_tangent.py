"""Post hoc descriptive frozen-null tangent check; sulaco CPU, no truth access."""
import os
os.environ.update(JAX_PLATFORMS='cpu',JAX_ENABLE_X64='true',NUMBA_NUM_THREADS='8',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
import argparse,json,hashlib,time
from pathlib import Path
import numpy as np
from acd_stage9_forward import tangent_forward,W,PATTERNS
from acd_protocol import ROOT,LEADS
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(states):
 start=time.monotonic()
 with np.load(states) as d:
  print('saved state fields',d.files,flush=True)
  x=d['x'] if 'x' in d else d['states']
 assert x.shape==(4096,40) and x.dtype==np.float64
 g=tangent_forward(x,np.full(len(x),8.,dtype=np.float64),PATTERNS[:8],W)
 rows=[]
 for k in range(8):
  for j,t in enumerate(LEADS):
   a=g[:,k,j];sd=float(a.std(ddof=1));mean=float(a.mean())
   rows.append(dict(pattern=k,lead=float(t),mean=mean,standard_deviation=sd,standard_error=sd/np.sqrt(len(a)),mean_over_sd=mean/sd,negative_share=float(np.mean(a<0))))
 receipt=dict(scope='Post hoc climatological, descriptive; licenses no frozen route. Finite-ensemble estimates do not prove invariant-measure shift symmetry.',states=len(x),F=8.,dtype=str(x.dtype),dt=.01,source_states=str(states),source_states_sha256=sha(states),source_null_receipt='receipts/acd_stage4b_null.json',source_code_hashes={p:sha(ROOT/p) for p in ['acd_stage11_clim_tangent.py','acd_stage9_forward.py','acd_protocol.py']},rows=rows,elapsed_cpu_run_seconds=time.monotonic()-start,truth_access=False)
 (ROOT/'receipts/acd_stage11_clim_tangent.json').write_text(json.dumps(receipt,indent=2,allow_nan=False)+'\n')
 print('finished',receipt['elapsed_cpu_run_seconds'],flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--states',type=Path,required=True);run(p.parse_args().states)
