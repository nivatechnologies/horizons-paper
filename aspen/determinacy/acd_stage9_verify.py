"""Numerical invariants and independent central-FD check of the Stage9 JVP."""
import os
os.environ.update(JAX_PLATFORMS='cpu',JAX_ENABLE_X64='true',NUMBA_NUM_THREADS='2',OPENBLAS_NUM_THREADS='1')
import json,numpy as np,hashlib,subprocess
from acd_protocol import ROOT,PATTERNS,physics
from acd_stage6_forward import RAW
from acd_stage9_receipts import DEST
def run():
 with np.load(RAW/'conf/case_000.npz') as d:x=d['x0'][:4].copy();f=d['theta'][:4,40].copy()
 with np.load(DEST/'forward_000.npz') as d:g=d['G'][:4].copy();saved=d['J'][:4,0,8]
 eps=1e-5;plus=physics.costs(physics.simulate(np.repeat(x,9,0),(f[:,None,None]+eps*PATTERNS[None]).reshape(-1,40),.01)).reshape(4,9,8)
 minus=physics.costs(physics.simulate(np.repeat(x,9,0),(f[:,None,None]-eps*PATTERNS[None]).reshape(-1,40),.01)).reshape(4,9,8)
 fd=(plus[:,:8]-minus[:,:8])/(2*eps)
 relative=float(np.max(np.abs(fd[:,:,:6]-g[:,:,:6])/(1+np.abs(g[:,:,:6]))))
 assert relative<1e-4,relative
 base_error=float(np.max(np.abs(plus[:,8]-saved)));assert base_error<1e-12,base_error
 a=json.load(open(DEST/'receipt_analyses.json'));assert a['A']['A2']['counts']['earlier']==788
 assert a['A']['A2']['counts']['later']==374;assert a['A']['A2']['pairs']==1332
 for r in a['D']:
  assert sum(r['chosen_actions'])==200
  if r['harms']==0:assert abs(r['zero_harm_CP_upper']-(1-.05**(1/200)))<1e-13
 old=json.loads(subprocess.check_output(['git','show','c36418d:aspen/determinacy/numbers_acd.json'],cwd=ROOT))
 current=json.load(open(ROOT/'numbers_acd.json'));assert all(current['numbers'][k]==v for k,v in old['numbers'].items())
 subprocess.run(['git','diff','--exit-code','c36418d','--','aspen/determinacy/paper','aspen/determinacy/ACD_ABSTRACT_DRAFT.md'],cwd=ROOT,check=True)
 report=dict(prior_numbers_unchanged=len(old['numbers']),paper_and_abstract_unchanged=True,status='PASS',central_fd_epsilon=eps,central_fd_max_relative_error_through_3LT=relative,factual_amplitude_invariance_max_abs=base_error,paired_endpoint_reproduced=True,policy_histograms_checked=True,zero_harm_CP_formula_checked=True,source_sha256=hashlib.sha256(__import__('pathlib').Path(__file__).read_bytes()).hexdigest())
 (DEST/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
if __name__=='__main__':run()
