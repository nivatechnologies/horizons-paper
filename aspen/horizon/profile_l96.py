"""Measure true nested-cohort solver costs and the [0,1 LT] myopic null."""
import json
import time
import numpy as np
import numba
from common import ROOT,GRID,BUDGETS,patterns,rng,write_json,sha
from l96 import rollout

def main():
    numba.set_num_threads(96)
    cal=json.loads((ROOT/'results/l96_calibration.json').read_text())
    sigma=cal['system']['sigma'];lam=cal['system']['lambda_mean'];delta=cal['delta']
    root=ROOT/'runs/l96/test'
    observation=np.load(root/'observations.npz');y=observation['observed'];F=observation['F_hat']
    p=patterns(0);K=8
    for c in range(200):
        z=y[c]+.02*sigma*rng('arm',0,2,c).standard_normal((256,11,40))
        last=0;seconds=0.;timings={}
        reference=np.load(root/f'case_{c:03d}.npz')['paired_cost']
        for m in BUDGETS:
            count=m-last
            initial=np.tile(z[last:m,-1],(K,1))
            force=np.repeat(F[c]+8*delta*p,count,axis=0)
            begin=time.time()
            cost,_=rollout(initial,force,lam,GRID)
            seconds+=time.time()-begin
            assert np.array_equal(cost.reshape(K,count,len(GRID)),reference[:,last:m]),'nested member reproducibility mismatch'
            timings[str(m)]=seconds;last=m
        initial=np.tile(z[:64,-1],(K,1))
        force=np.repeat(F[c]+8*delta*p,64,axis=0)
        costs,_=rollout(initial,force,lam,np.array([0.]))
        chosen=int(costs[:,0].reshape(K,64).mean(1).argmin())
        write_json(root/f'myopic_{c:03d}.json',dict(chosen=chosen,M=64,window=[0,1],git_sha=sha()))
        write_json(root/f'profile_{c:03d}.json',dict(cumulative_solver_seconds=timings,
                   basis='measured nested cohorts sharing all 16 scoring horizons; interval computation timed separately',git_sha=sha()))
        print(f'L96 sequential cost/null {c+1}/200',flush=True)

if __name__=='__main__':main()
