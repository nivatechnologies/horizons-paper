"""Exact inherited P1x objective/search, with a fail-closed finite guard."""
import numpy as np
import torch
from kolmo import KolmoAction
from common import ALPHA

@torch.no_grad()
def identify(Y,w,alpha,sA,device,lo=25.,hi=70.,n_eval=30):
    if alpha!=ALPHA:raise ValueError('identifier drag differs from frozen truth family')
    if not np.isfinite(Y).all() or not np.isfinite(sA) or sA<=0:raise ValueError('invalid identification inputs')
    n=Y.shape[1];observed=torch.as_tensor(Y,device=device)
    def objective(re):
        model=KolmoAction(re,device=device);state=model.to_spec(observed[0])
        total=torch.zeros(n,dtype=torch.float64,device=device)
        for k in range(1,w):
            state=model.flow(state,35)
            total+=((model.to_phys(state).double()-observed[k])**2).sum((-2,-1))
        result=(total/(w-1)/sA**2).cpu().numpy()
        if not np.isfinite(result).all():raise RuntimeError('P1x nonfinite objective: stop identification, no substitution')
        return result
    golden=(np.sqrt(5)-1)/2;a=np.full(n,lo);b=np.full(n,hi)
    c=b-golden*(b-a);d=a+golden*(b-a);fc=objective(c);fd=objective(d);evaluations=2
    while evaluations<n_eval:
        left=fc<fd;b=np.where(left,d,b);a=np.where(left,a,c)
        newc=np.where(left,b-golden*(b-a),d);newd=np.where(left,c,a+golden*(b-a))
        new=objective(np.where(left,newc,newd))
        fc,fd=np.where(left,new,fd),np.where(left,fc,new)
        c,d=newc,newd;evaluations+=1
    return (a+b)/2,evaluations,evaluations*(w-1)*35
