"""World D solver reuse with frozen action forcing and window scoring."""
import sys
from pathlib import Path
import numpy as np
import torch

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'adapt_physics'))
from ap.solver import KolmoDrag,lyapunov
from common import patterns,ALPHA

class KolmoAction(KolmoDrag):
    def __init__(self,Re=40.,delta=0.,actions=None,device='cpu'):
        super().__init__(np.atleast_1d(Re),alpha=ALPHA,device=device)
        if actions is not None:
            q=patterns(1)[np.asarray(actions)]*delta*np.sqrt(8.)
            self.F_hat=self.F_hat0+torch.fft.rfft2(torch.as_tensor(q,device=device,dtype=torch.float64))*self.mask

@torch.no_grad()
def costs(initial,delta,lam,device='cpu',chunk=64,horizons=None):
    """initial (M,64,64), paired by action; returns costs (K,M,H)."""
    horizons=np.asarray([20.] if horizons is None else horizons)
    M=len(initial);K=6;H=len(horizons)
    result=np.empty((K,M,H))
    end=int(np.ceil((horizons.max()+1)/lam/.01))+35
    for start in range(0,M,chunk):
        z=initial[start:start+chunk];m=len(z)
        q=np.repeat(np.arange(K),m)
        model=KolmoAction(np.full(K*m,40.),delta,q,device)
        wh=model.to_spec(np.tile(z,(K,1,1)))
        total=torch.zeros((K*m,H),device=device,dtype=torch.float64)
        counts=np.zeros(H)
        for s in range(end+1):
            if s%35==0:
                t=s*.01
                indices=np.flatnonzero((t>=horizons/lam-1e-12)&(t<=(horizons+1)/lam+1e-12))
                if len(indices):
                    visc,drag=model.budget(wh)
                    v=visc+drag
                    for h in indices:
                        total[:,h]+=v;counts[h]+=1
            if s<end:
                wh=model.step(wh)
        c=(total/torch.as_tensor(counts,device=device)).cpu().numpy()
        if not np.isfinite(c).all():
            raise ValueError('nonfinite Kolmogorov truth calibration')
        result[:,start:start+m]=c.reshape(K,m,H)
    return result
