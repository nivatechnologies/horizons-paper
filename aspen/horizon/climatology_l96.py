"""Frozen true per-action climatology, independent namespace."""
import json
import numpy as np
from numba import njit,prange
from common import ROOT,patterns,rng,write_json,sha
from l96 import flow,step

@njit(cache=True,parallel=True)
def mean_run(x,f,nsteps):
    means=np.zeros_like(x)
    for b in prange(len(x)):
        a=x[b].copy();count=0
        for s in range(nsteps):
            a=step(a,f[b])
            if (s+1)%5==0:
                means[b]+=a;count+=1
        means[b]/=count
    return means

def main():
    cal=json.loads((ROOT/'results/l96_calibration.json').read_text())
    lam=cal['system']['lambda_mean'];delta=cal['delta']
    f=8+8*delta*patterns(0)
    x=8+rng('climatology',0).standard_normal((8,40))
    x=flow(x,f,int(round(50/lam/.01)))
    means=mean_run(x,f,int(round(500/lam/.01)))
    out=ROOT/'runs/l96/test'
    np.save(out/'climatology.npy',means)
    write_json(out/'climatology.json',dict(spinup_LT=50,average_LT=500,git_sha=sha()))
    print('L96 action climatology complete',flush=True)

if __name__=='__main__':main()
