"""Meaningful Stage6 checks: saved-map reproduction, energy identities and source immutability."""
import os
os.environ['NUMBA_NUM_THREADS']='2'
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
import json,subprocess,numpy as np
from pathlib import Path
from acd_stage6_analysis import ROOT,RAW,OUT,sha,save
from acd_protocol import physics,PATTERNS
def run():
 checks={};maxbaseline=0.;maxdev=0.;maxproj=0.;maxbudget=0.;counts={}
 for panel,amp in [('conf',.16),('dev',.64)]:
  counts[panel]={};total=0
  for c in range(200):
   with np.load(OUT/f'{panel}_{c:03d}_{amp}.npz') as z:
    j=z['J'];terms=z['terms'];D=j[:,:8]-j[:,8,None]
    assert np.isfinite(j).all() and np.isfinite(terms).all()
    maxproj=max(maxproj,float(np.max(np.abs(D-terms[:,:,2]-terms[:,:,3]))))
    maxbudget=max(maxbudget,float(np.max(np.abs(D-terms[:,:,0]-terms[:,:,1]-terms[:,:,4]))))
    n=len(j);total+=n;counts[panel][str(n)]=counts[panel].get(str(n),0)+1
    source=RAW/f'{panel}/case_{c:03d}.npz' if panel=='conf' else ROOT/f'runs/stage4_amplitude/J_0.64_{c:03d}.npz'
    with np.load(source) as old:err=float(np.max(np.abs(j-old['J'])))
    if panel=='conf':maxbaseline=max(maxbaseline,err)
    else:maxdev=max(maxdev,err)
  counts[panel]['total_draws']=total
 assert maxbaseline<1e-12 and maxdev<1e-12 and maxproj<1e-12 and maxbudget<1e-12
 # Independent instantaneous energy derivative identity at saved states, using original rhs.
 derivative=[]
 with np.load(RAW/'conf/case_000.npz') as d:xs=d['x0'][:16];F=d['theta'][:16,40]
 for x,f in zip(xs,F):
  for k in range(8):
   y=x+.01*PATTERNS[k];amp=.16;D=.5*np.mean(y*y-x*x)
   direct=np.mean(y*physics.rhs(y,f+amp*PATTERNS[k])-x*physics.rhs(x,np.full(40,f)))
   identity=-2*D+f*np.mean(y-x)+amp*np.mean(PATTERNS[k]*y)
   derivative.append(abs(direct-identity))
 assert max(derivative)<1e-12
 frozen=json.load(open(ROOT/'receipts/acd_stage2.json'));A=json.load(open(OUT/'A.json'))
 assert all(A['A1']['comparisons'][t]['observation_minus_Fc']['point']==frozen['R2a'][i]['point'] for i,t in enumerate([3,5]))
 assert abs(A['A2']['first_loss']['interval']['point']-frozen['R2b']['point'])<1e-15
 assert all(r['mean_regret']>=0 and 0<=r['acting_share']<=1 and 0<=r['worse_than_no_action_share']<=1 for r in A['A4']['policies'])
 # Historical paper, abstract, frozen scientific sources and receipts cannot be changed in this stage.
 tracked=subprocess.check_output(['git','ls-tree','-r','--name-only','92d8335:aspen/determinacy'],cwd=ROOT).decode().splitlines()
 preserved=[]
 for p in tracked:
  if p.startswith(('paper/','receipts/','sources/')) or p in ['ACD_FREEZE.md','ACD_FREEZE_CODE.md','ACD_ABSTRACT_DRAFT.md','ACD_ABSTRACT_AUDIT.md']:
   old=subprocess.check_output(['git','show','92d8335:aspen/determinacy/'+p],cwd=ROOT)
   assert (ROOT/p).read_bytes()==old,p;preserved.append(p)
 checks.update(saved_confirmation_cost_max_abs=maxbaseline,saved_development_0p64_cost_max_abs=maxdev,
  projection_split_max_abs=maxproj,three_term_budget_closure_max_abs=maxbudget,
  instantaneous_energy_derivative_max_abs=max(derivative),scoring_draw_counts=counts,
  frozen_R2a_and_R2b_reproduced=True,decision_invariants_pass=True,preserved_base_artifacts=preserved,
  post_hoc=True,new_sampling=False,new_training=False,cloud_compute=False)
 # Source archives are hashed without interpreting any truth-bearing arrays outside scoring.
 checks['source_archives']={str(RAW/f'{panel}/case_{c:03d}.npz'):sha(RAW/f'{panel}/case_{c:03d}.npz') for panel in ['conf','dev'] for c in range(200)}
 save(ROOT/'receipts/acd_stage6_verification.json',checks)
 print('Stage6 verification PASS',counts,maxbaseline,maxdev,maxproj,maxbudget,flush=True)
if __name__=='__main__':run()
