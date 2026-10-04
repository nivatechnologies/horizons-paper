"""Frozen truth and solver arms; requires committed system calibration addendum."""
import argparse
import json
import time
import numpy as np
import numba
from common import ROOT,GRID,patterns,rng,sha,write_json
from l96 import flow,rollout

def identify(y):
    a=np.full(len(y),6.);b=np.full(len(y),10.)
    golden=(np.sqrt(5)-1)/2
    def objective(F):
        forcing=np.repeat(F[:,None],40,axis=1)
        z=y[:,0].copy();loss=np.zeros(len(y))
        for t in range(1,11):
            z=flow(z,forcing,5)
            loss+=np.mean((z-y[:,t])**2,axis=1)
        return loss
    c=b-golden*(b-a);d=a+golden*(b-a)
    fc=objective(c);fd=objective(d)
    for _ in range(28):
        left=fc<fd;b=np.where(left,d,b);a=np.where(left,a,c)
        cn=np.where(left,b-golden*(b-a),d)
        dn=np.where(left,c,a+golden*(b-a))
        new=objective(np.where(left,cn,dn))
        fc,fd=np.where(left,new,fd),np.where(left,fc,new)
        c,d=cn,dn
    return (a+b)/2

def main(workers):
    numba.set_num_threads(workers)
    calibration=json.loads((ROOT/'results'/'l96_calibration.json').read_text())
    if calibration['status']!='READY_FOR_CALIBRATION_FREEZE_ADDENDUM':
        raise RuntimeError('L96 calibration did not clear chaos gates')
    addendum=ROOT/'AAH_FREEZE_CALIBRATION_L96.md'
    if not addendum.exists():
        raise RuntimeError('missing calibration freeze addendum')
    out=ROOT/'runs'/'l96'/'test';out.mkdir(parents=True,exist_ok=True)
    if (out/'observations.npz').exists():
        raise FileExistsError('test panel already exists')
    system=calibration['system'];lam=system['lambda_mean'];sigma=system['sigma'];delta=calibration['delta']
    start=time.time()
    X=8+rng('observation',0).standard_normal((200,40))
    X=flow(X,np.full_like(X,8.),50000)
    window=[X.copy()]
    for _ in range(10):
        X=flow(X,np.full_like(X,8.),5);window.append(X.copy())
    true=np.stack(window,1)
    y=true+.02*sigma*rng('observation',0,1).standard_normal(true.shape)
    estimate=identify(y)
    np.savez(out/'observations.npz',observed=y,true=true,F_hat=estimate)
    p=patterns(0);K=8
    for c in range(200):
        payload={};timings={}
        # Actual controlled trajectories, only for targets and realized costs.
        actual_cost,actual_snap=rollout(np.tile(true[c,-1],(K,1)),8+8*delta*p,lam,GRID,capture=True)
        payload.update(actual_cost=actual_cost,actual_snap=actual_snap)
        for arm,M,F in [('truth',1024,8.),('paired',256,estimate[c]),
                        ('unpaired',256,estimate[c]),('jitter',256,estimate[c]),
                        ('misidentified',256,8.8)]:
            tick=time.time()
            ns='truth' if arm=='truth' else 'arm'
            if arm=='unpaired':
                windows=np.stack([y[c]+.02*sigma*rng(ns,0,2,c,action=k+1).standard_normal((M,11,40)) for k in range(K)])
            else:
                z=y[c]+.02*sigma*rng(ns,0,2,c).standard_normal((M,11,40))
                windows=np.broadcast_to(z,(K,M,11,40))
            initial=windows[:,:,-1].reshape(K*M,40).copy()
            forcing=np.broadcast_to(F+8*delta*p[:,None],(K,M,40)).reshape(K*M,40).copy()
            seeds=None
            if arm=='jitter':
                seeds=np.array([rng('jitter',0,0,c,m,k).integers(0,2**31-1) for k in range(K) for m in range(M)],dtype=np.int64)
            vals,snap=rollout(initial,forcing,lam,GRID,capture=arm!='truth',jitterseeds=seeds)
            payload[arm+'_cost']=vals.reshape(K,M,len(GRID))
            if arm!='truth':
                payload[arm+'_mean_snap']=snap.reshape(K,M,len(GRID),40)[:,:64].mean(1)
            timings[arm]=time.time()-tick
        np.savez(out/f'case_{c:03d}.npz',**payload)
        write_json(out/f'case_{c:03d}.json',dict(case=c,F_hat=float(estimate[c]),timings=timings,git_sha=sha()))
        print(f'L96 test case {c+1}/200 complete',flush=True)
    write_json(out/'solver_complete.json',dict(cases=200,seconds=time.time()-start,git_sha=sha()))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--workers',type=int,default=128)
    main(p.parse_args().workers)
