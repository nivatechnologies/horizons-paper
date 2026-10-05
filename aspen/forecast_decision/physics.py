"""Float64 RK4 kernels and outputs. Cost predicate remains inherited."""
import numpy as np
from numba import njit, prange
from protocol import LT, OUT, TICKS, WINDOWS, patterns, rng, SIGMA

@njit(cache=True)
def rhs(x,f):
    out=np.empty(40)
    for i in range(40):
        out[i]=(x[(i+1)%40]-x[(i-2)%40])*x[(i-1)%40]-x[i]+f[i]
    return out
@njit(cache=True)
def step(x,f,dt):
    k1=rhs(x,f);k2=rhs(x+.5*dt*k1,f);k3=rhs(x+.5*dt*k2,f);k4=rhs(x+dt*k3,f)
    return x+dt/6*(k1+2*k2+2*k3+k4)
@njit(cache=True,parallel=True)
def flow(x,f,nsteps,dt):
    out=x.copy()
    for b in prange(len(x)):
        a=out[b].copy()
        for _ in range(nsteps):a=step(a,f[b],dt)
        out[b]=a
    return out
@njit(cache=True,parallel=True)
def paths(x,f,dt,nticks):
    nper=int(round(.05/dt))
    out=np.empty((len(x),nticks,40))
    for b in prange(len(x)):
        a=x[b].copy()
        for t in range(nticks):
            out[b,t]=a
            if t<nticks-1:
                for _ in range(nper):a=step(a,f[b],dt)
    return out
def history(name,case,dt=.01):
    x=8+rng(name,0,case).standard_normal((1,40))
    x=flow(x,np.full_like(x,8.),int(round(50*LT/dt)),dt)
    true=paths(x,np.full_like(x,8.),dt,11)[0]
    y=true+.02*SIGMA*rng(name,1,case).standard_normal(true.shape)
    return true,y
def simulate(initial,forcing,dt,nticks=None):
    assert abs(round(OUT/dt)*dt-OUT)<1e-12
    return paths(np.ascontiguousarray(initial),np.ascontiguousarray(forcing),dt,len(TICKS) if nticks is None else nticks)
def costs(states,windows=WINDOWS):
    energy=.5*np.mean(states*states,axis=-1)
    return np.stack([energy[...,w].mean(-1) for w in windows],axis=-1)
def identify(y,dt):
    # Exactly inherited 30-evaluation golden search, with propagated dt.
    a=np.array([6.]);b=np.array([10.]);gold=(np.sqrt(5)-1)/2
    def objective(F):
        z=simulate(y[None,0],np.repeat(F[:,None],40,axis=1),dt,11)[0]
        return np.array([np.mean((z[1:]-y[1:])**2,axis=1).sum()])
    c=b-gold*(b-a);d=a+gold*(b-a);fc=objective(c);fd=objective(d)
    for _ in range(28):
        left=fc<fd;b=np.where(left,d,b);a=np.where(left,a,c)
        cn=np.where(left,b-gold*(b-a),d);dn=np.where(left,c,a+gold*(b-a))
        new=objective(np.where(left,cn,dn))
        fc,fd=np.where(left,new,fd),np.where(left,fc,new);c,d=cn,dn
    return float(((a+b)/2)[0])
@njit(cache=True)
def rhs2(z,f):
    out=np.empty(440)
    for k in range(40):
        sy=0.
        for j in range(10):sy+=z[40+k*10+j]
        out[k]=(z[(k+1)%40]-z[(k-2)%40])*z[(k-1)%40]-z[k]+f[k]-sy
    for q in range(400):
        out[40+q]=-100*z[40+(q+1)%400]*(z[40+(q+2)%400]-z[40+(q-1)%400])-10*z[40+q]+z[q//10]
    return out
@njit(cache=True)
def step2(z,f,dt):
    k1=rhs2(z,f);k2=rhs2(z+.5*dt*k1,f);k3=rhs2(z+.5*dt*k2,f);k4=rhs2(z+dt*k3,f)
    return z+dt/6*(k1+2*k2+2*k3+k4)
@njit(cache=True,parallel=True)
def flow2(z,f,nsteps,dt):
    out=z.copy()
    for b in prange(len(z)):
        a=out[b].copy()
        for _ in range(nsteps):a=step2(a,f[b],dt)
        out[b]=a
    return out

