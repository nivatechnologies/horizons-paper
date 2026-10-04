"""Independent action-conditioned training/validation trajectories on sulaco."""
import json
import time
import numpy as np
import numba
from numba import njit,prange
from common import ROOT,patterns,rng,write_json,sha
from l96 import flow,step

@njit(cache=True,parallel=True)
def trajectory(x,f,nframes):
    out=np.empty((len(x),nframes,40),dtype=np.float32)
    for b in prange(len(x)):
        a=x[b].copy()
        for t in range(nframes):
            out[b,t]=a
            for _ in range(5):
                a=step(a,f[b])
    return out

def main():
    numba.set_num_threads(96)
    cal=json.loads((ROOT/'results/l96_calibration.json').read_text())
    if not (ROOT/'AAH_FREEZE_CALIBRATION_L96.md').exists():
        raise RuntimeError('calibration freeze not committed')
    delta=cal['delta'];lam=cal['system']['lambda_mean']
    out=ROOT/'runs/l96/learned';out.mkdir(parents=True,exist_ok=True)
    for ns,n in [('train',2048),('val',64)]:
        path=out/f'{ns}.npz'
        if path.exists():
            raise FileExistsError(path)
        start=time.time()
        x=8+rng(ns,0).standard_normal((n,40))
        x=flow(x,np.full_like(x,8.),50000)
        history=[x.copy()]
        for _ in range(10):
            x=flow(x,np.full_like(x,8.),5);history.append(x.copy())
        R=rng(ns,0,4);k=R.integers(8,size=n);amp=R.uniform(-2*delta,2*delta,size=n)
        action=8*amp[:,None]*patterns(0)[k]
        post=trajectory(x,8+action,int(np.ceil(25/lam/.05))+1)
        pre=np.stack(history,1).astype(np.float32)
        data=np.concatenate([pre[:,:-1],post],axis=1)
        np.savez(path,state=data,action=action.astype(np.float32),index=k,amplitude=amp)
        write_json(out/f'{ns}.json',dict(trajectories=n,frames=data.shape[1],seconds=time.time()-start,git_sha=sha()))
        print('L96 learned data',ns,data.shape,flush=True)

if __name__=='__main__':
    main()
