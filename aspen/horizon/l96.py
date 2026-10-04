"""Float64 RK4, unchanged L96 RHS, compiled trajectory batches on sulaco."""
import numpy as np
from numba import njit, prange

@njit(cache=True)
def rhs(x,forcing):
    out=np.empty(40)
    for i in range(40):
        out[i]=(x[(i+1)%40]-x[(i-2)%40])*x[(i-1)%40]-x[i]+forcing[i]
    return out

@njit(cache=True)
def step(x,forcing,dt=.01):
    k1=rhs(x,forcing)
    k2=rhs(x+.5*dt*k1,forcing)
    k3=rhs(x+.5*dt*k2,forcing)
    k4=rhs(x+dt*k3,forcing)
    return x+dt/6*(k1+2*k2+2*k3+k4)

@njit(cache=True,parallel=True)
def flow(x,forcing,nsteps):
    out=x.copy()
    for b in prange(len(x)):
        a=out[b].copy()
        for _ in range(nsteps):
            a=step(a,forcing[b])
        out[b]=a
    return out

@njit(cache=True,parallel=True)
def rollout(x,forcing,lam,horizons,W=1.,capture=False):
    B=len(x);H=len(horizons)
    end=int(np.ceil((horizons.max()+W)/lam/.01))+5
    costs=np.zeros((B,H));counts=np.zeros((B,H))
    snapshots=np.zeros((B,H,40)) if capture else np.zeros((0,0,0))
    for b in prange(B):
        a=x[b].copy()
        for s in range(end+1):
            t=s*.01
            if s%5==0:
                E=.5*np.mean(a*a)
                for h in range(H):
                    if t>=horizons[h]/lam-1e-12 and t<=(horizons[h]+W)/lam+1e-12:
                        costs[b,h]+=E;counts[b,h]+=1
            if capture:
                for h in range(H):
                    if s==int(np.rint(horizons[h]/lam/.01)):
                        snapshots[b,h]=a
            if s<end:
                a=step(a,forcing[b])
    return costs/counts,snapshots

@njit(cache=True,parallel=True)
def lyapunov(x,forcing,total=800.,tau=1.,transient=20.):
    B=len(x);out=np.empty(B)
    for b in prange(B):
        a=x[b].copy()
        p=np.sin(np.arange(40)+b+1.)
        p=p/np.sqrt(np.mean(p*p))*1e-6*np.sqrt(np.mean(a*a))
        twin=a+p;score=0.;n=0
        for r in range(int(total/tau)):
            for _ in range(int(tau/.01)):
                a=step(a,forcing[b]);twin=step(twin,forcing[b])
            d=twin-a
            nd=np.sqrt(np.mean(d*d));target=1e-6*np.sqrt(np.mean(a*a))
            if r>=int(transient/tau):
                score+=np.log(nd/target);n+=1
            twin=a+d*target/nd
        out[b]=score/(n*tau)
    return out
