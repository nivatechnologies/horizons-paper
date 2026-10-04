"""Execute only frozen L96 calibration and chaos gates; never generate test data."""
import argparse
from pathlib import Path
import time
import socket
import numpy as np
import numba
from common import ROOT, patterns, rng, write_json, sha, eligible
from l96 import flow, rollout, lyapunov

def main(workers):
    numba.set_num_threads(workers)
    out=ROOT/'runs'/'l96';out.mkdir(parents=True,exist_ok=True)
    if (out/'calibration.json').exists():
        raise FileExistsError('calibration already exists; do not overwrite')
    start=time.time();F=np.full((64,40),8.)
    states=8+rng('lyapunov',0).standard_normal((64,40))
    states=flow(states,F,50000)
    lam=lyapunov(states,F)
    mean=float(lam.mean());se=float(lam.std(ddof=1)/8)
    sigma=float(np.sqrt(np.mean(states*states)))
    system=dict(lambda_mean=mean,lambda_ci95=[mean-1.96*se,mean+1.96*se],
                lambda_per_start=lam.tolist(),sigma=sigma,git_sha=sha(),host=socket.gethostname(),
                numba_threads=workers)
    write_json(out/'system.json',system)
    print('L96 base chaos/RMS',system['lambda_mean'],sigma,flush=True)
    if mean-1.96*se<=0:
        write_json(out/'calibration.json',dict(status='STOP_BASE_CHAOS',system=system,git_sha=sha()))
        return
    p=patterns(0);K=len(p);M=512
    X=8+rng('calibration',0).standard_normal((40,40))
    X=flow(X,np.full_like(X,8.),50000)
    windows=[X.copy()]
    for _ in range(10):
        X=flow(X,np.full_like(X,8.),5);windows.append(X.copy())
    true=np.stack(windows,1)
    observed=true+.02*sigma*rng('calibration',0,1).standard_normal(true.shape)
    rows=[];chosen=None
    for delta in (.01,.02,.05,.1):
        panel=[]
        for c in range(40):
            z=observed[c,-1]+.02*sigma*rng('calibration',0,2,c).standard_normal((M,40))
            initial=np.broadcast_to(z,(K,M,40)).reshape(K*M,40).copy()
            forcing=np.broadcast_to(8+8*delta*p[:,None,:],(K,M,40)).reshape(K*M,40).copy()
            costs,_=rollout(initial,forcing,mean,np.array([20.]))
            result=eligible(costs[:,0].reshape(K,M),'calibration',0,c)
            panel.append(result)
            print(f'L96 delta={delta} case={c+1}/40 eligible={result["eligible"]}',flush=True)
        n=sum(r['eligible'] for r in panel)
        rows.append(dict(delta=delta,eligible=n,total=40,fraction=n/40,cases=panel))
        write_json(out/'calibration_progress.json',dict(rows=rows,git_sha=sha()))
        if n>=32:
            chosen=delta;break
    result=dict(status='CALIBRATION_FAIL' if chosen is None else 'CALIBRATED',delta=chosen,
                rows=rows,system=system,seconds=time.time()-start,git_sha=sha())
    write_json(out/'calibration.json',result)
    if chosen is None:
        print('L96 CALIBRATION FAIL: no allowed amplitude qualified',flush=True);return
    gates=[]
    for k in range(K):
        forcing=np.broadcast_to(8+8*chosen*p[k],(64,40)).copy()
        z=flow(states,forcing,50000)
        values=lyapunov(z,forcing)
        avg=float(values.mean());err=float(values.std(ddof=1)/8)
        gate=dict(action=k,lambda_mean=avg,lambda_ci95=[avg-1.96*err,avg+1.96*err],
                  chaotic=avg-1.96*err>0,per_start=values.tolist())
        gates.append(gate)
        write_json(out/'action_chaos.json',dict(delta=chosen,gates=gates,git_sha=sha()))
        print('L96 action chaos',k,gate['lambda_ci95'],flush=True)
        if not gate['chaotic']:
            result['status']='STOP_ACTION_CHAOS';break
    else:
        result['status']='READY_FOR_CALIBRATION_FREEZE_ADDENDUM'
    result['seconds']=time.time()-start
    write_json(out/'calibration.json',result)

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--workers',type=int,default=128)
    main(a.parse_args().workers)
