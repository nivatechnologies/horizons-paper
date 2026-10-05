"""Forecast outputs and covariance mechanism, no truth access."""
import os
os.environ['JAX_PLATFORMS']='cpu'
os.environ['JAX_ENABLE_X64']='true'
import numpy as np
from acd_protocol import physics,PATTERNS,TICKS
def forecast(theta,h,actions=None,chunk=64,initial_is_last=False):
    actions=list(range(9)) if actions is None else list(actions)
    all_cost=[];x0s=[];sumstate=np.zeros((len(actions),len(TICKS),40));sumsquare=np.zeros((len(TICKS),40));divergence=np.zeros((len(actions),len(TICKS)))
    for first in range(0,len(theta),chunk):
        t=theta[first:first+chunk];b=len(t)
        x0=t[:,:40] if initial_is_last else physics.simulate(t[:,:40],np.repeat(t[:,40,None],40,axis=1),h,11)[:,-1];x0s.append(x0)
        initial=np.repeat(x0,len(actions),axis=0)
        forcing=(t[:,40,None,None]+.16*PATTERNS[None,actions]).reshape(-1,40)
        states=physics.simulate(initial,forcing,h).reshape(b,len(actions),len(TICKS),40)
        all_cost.append(physics.costs(states));sumstate+=states.sum(axis=0)
        if 8 in actions:
            no=actions.index(8);sumsquare+=(states[:,no]**2).sum(axis=0)
            divergence+=np.sqrt(np.mean((states-states[:,no,None])**2,axis=-1)).sum(axis=0)
    return dict(J=np.concatenate(all_cost),x0=np.concatenate(x0s),state_sum=sumstate,
                factual_square_sum=sumsquare,divergence_sum=divergence,count=len(theta))
def mechanism(j):
    factual=j[:,8,:];action=j[:,:8,:];diff=action-factual[:,None,:]
    va=np.var(action,axis=0,ddof=1);vf=np.var(factual,axis=0,ddof=1)
    cov=np.mean((action-action.mean(0))*(factual-factual.mean(0))[:,None,:],axis=0)*len(j)/(len(j)-1)
    with np.errstate(divide='ignore',invalid='ignore'):
        rho=cov/np.sqrt(va*vf);cancel=np.var(diff,axis=0,ddof=1)/(va+vf)
        z=np.abs(diff.mean(0))/diff.std(0,ddof=1)
    return dict(rho=rho,cancellation=cancel,z_D=z,variance_action=va,variance_factual=vf)
