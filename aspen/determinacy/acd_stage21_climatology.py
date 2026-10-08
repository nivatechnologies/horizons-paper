"""Stage1 climatology recipe at each shifted forcing; no hidden-history access."""
import os
os.environ.update(JAX_PLATFORMS='cpu',JAX_ENABLE_X64='true',NUMBA_NUM_THREADS='4',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
import json,time
import numpy as np
from acd_protocol import ROOT,physics,LT,LEADS
from acd_mechanism import forecast
from acd_stage21_contract import OUT,NAMES,rng,digest,verify_contract

def run():
 verify_contract();out=OUT/'climatology';out.mkdir(exist_ok=True);rows=[]
 for level in [7,9]:
  target=out/f'F{level}.npz';meta=target.with_suffix('.json')
  if meta.exists():
   d=json.loads(meta.read_text());assert digest(target)==d['sha256'];rows.append(d);continue
  begin=time.monotonic()
  initial=np.array([level+rng(NAMES[4],sub=level,case=c).standard_normal(40) for c in range(4096)])
  states=physics.flow(initial,np.full_like(initial,level),int(round(50*LT/.01)),.01)
  pred=forecast(np.c_[states,np.full(len(states),level)],.01,initial_is_last=True)
  J=pred['J'];jbar=float(J[:,8].mean());pS=(J[:,:8]<J[:,8,None]).mean(0);pF=(J[:,8]>jbar).mean(0)
  prob=np.stack([1-np.concatenate([pS,pF[None]]),np.concatenate([pS,pF[None]])],-1)
  np.savez_compressed(target,states=states,J=J,jbar=jbar,prob=prob,factual_mean=pred['state_sum'][8]/len(states))
  d=dict(forcing=level,states=len(states),jbar=jbar,probabilities=prob.tolist(),leads=LEADS.tolist(),seconds=time.monotonic()-begin,sha256=digest(target),path=str(target.relative_to(ROOT)),realized_outcome_accesses=[])
  meta.write_text(json.dumps(d,indent=2)+'\n');rows.append(d)
 (ROOT/'receipts/acd_stage21_climatology.json').write_text(json.dumps(dict(rows=rows,code_sha256=digest(__file__),realized_outcome_accesses=[]),indent=2)+'\n')
 from acd_stage21_publish import publish
 publish('climatology')
if __name__=='__main__':run()
