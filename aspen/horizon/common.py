"""Frozen selectors, disjoint random streams and statistical readings."""
from pathlib import Path
import json
import os
import subprocess
import numpy as np

ROOT = Path(__file__).resolve().parent
GRID = np.array([.25,.5,.75,1,1.5,2,2.5,3,4,5,6,8,10,12,16,20])
BUDGETS = (8,16,32,64,128,256)
NAMESPACES = dict(calibration=100000, truth=200000, arm=300000,
                  train=400000, val=500000, climatology=600000,
                  jitter=700000, lyapunov=800000, observation=900000)
ALPHA = .0773273136075609
KOLMO_LAMBDA = .16793280275789657

def rng(namespace, system, sub=0, case=0, member=0, action=0):
    return np.random.default_rng(np.random.SeedSequence([
        NAMESPACES[namespace], system, sub, case, member, action]))

def patterns(system):
    if system == 0:
        theta = 2*np.pi*np.arange(40)/40
        p = [-np.ones(40)] + [np.sqrt(2)*np.cos(k*theta) for k in (1,2,4,8,10)]
        p += [(-1.)**np.arange(40), (1-40*(np.arange(40)==0))/np.sqrt(39)]
    else:
        y,x = np.meshgrid(2*np.pi*np.arange(64)/64,
                          2*np.pi*np.arange(64)/64,indexing='ij')
        p = [4*np.sqrt(2)*np.cos(4*y), -2*np.sqrt(2)*np.cos(2*y),
             -8*np.sqrt(2)*np.cos(8*y), 2*np.sqrt(17)*np.cos(x)*np.cos(4*y),
             4*np.sqrt(5)*np.cos(2*x)*np.cos(4*y), 2*np.sqrt(2)*np.cos(x)*np.cos(y)]
    p = np.stack(p)
    return p / np.sqrt(np.mean(p*p,axis=tuple(range(1,p.ndim))))[(slice(None),)+(None,)*(p.ndim-1)]

def eligible(costs, namespace, system, case, sub=3, B=2000, alpha=.01):
    """costs (K,M), member-index bootstrap, observed leader, nominal bounds."""
    K,M = costs.shape
    if not np.isfinite(costs).all():
        raise ValueError('nonfinite truth costs: numerical failure')
    mean = costs.mean(1)
    best = int(mean.argmin())
    indices = rng(namespace,system,sub,case).integers(M,size=(B,M))
    bounds = []
    for j in range(K):
        if j != best:
            delta = costs[j]-costs[best]
            samples = delta[indices].mean(1)
            bounds.append(float(np.quantile(samples,alpha/(K-1))))
    return dict(eligible=all(b>0 for b in bounds),best=best,
                means=mean.tolist(),lower_bounds=bounds)

def m95(accuracies):
    return next((m for m,a in zip(BUDGETS,accuracies) if a>=.95),None)

def member_reading(paired,unpaired):
    if paired is None:
        return dict(pass_condition=False,ratio_lower_bound=None)
    ratio=(256 if unpaired is None else unpaired)/paired
    return dict(pass_condition=ratio>=3,ratio_lower_bound=ratio,
                unpaired_censored=unpaired is None)

def write_json(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_name(path.name+'.tmp')
    tmp.write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
    os.replace(tmp,path)

def sha():
    return subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
