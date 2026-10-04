"""CPU FFT implementation of the existing World D IFRK4 scheme and constants.

Constants and forcing are constructed by KolmoAction; only the FFT/array backend
changes. No physics, numerical order, dealiasing, time step or precision changes.
"""
import numpy as np
from scipy.fft import rfft2,irfft2
from kolmo import KolmoAction

class CPUWorldD:
    def __init__(self,Re=40.,delta=0.,actions=None,workers=8):
        reference=KolmoAction(Re,delta,actions,device='cpu')
        for name in ('KX','KY','K2','K2inv','mask','E','E2','F_hat'):
            setattr(self,name,getattr(reference,name).numpy())
        self.Re=np.atleast_1d(Re);self.alpha=reference.alpha
        self.dt=reference.dt;self.workers=workers
        self.w=np.full_like(self.K2,2.);self.w[:,0]=1.;self.w[:,-1]=1.
    def to_spec(self,x):
        return rfft2(np.asarray(x,dtype=np.float64),workers=self.workers)*self.mask
    def to_phys(self,x):
        return irfft2(x,s=(64,64),workers=self.workers)
    def set_dt(self,dt):
        self.dt=float(dt)
        self.E=np.exp((-self.K2[None]/self.Re[:,None,None]-self.alpha)*dt/2).astype(np.complex128)
        self.E2=self.E*self.E
    def rhs(self,x):
        psi=x*self.K2inv
        u=self.to_phys(1j*self.KY*psi);v=self.to_phys(-1j*self.KX*psi)
        wx=self.to_phys(1j*self.KX*x);wy=self.to_phys(1j*self.KY*x)
        return -rfft2(u*wx+v*wy,workers=self.workers)*self.mask+self.F_hat
    def step(self,x):
        E,E2,dt=self.E,self.E2,self.dt
        k1=dt*self.rhs(x)
        k2=dt*self.rhs(E*(x+.5*k1))
        k3=dt*self.rhs(E*x+.5*k2)
        k4=dt*self.rhs(E2*x+E*k3)
        return E2*x+(E2*k1+2*E*(k2+k3)+k4)/6
    def flow(self,x,n):
        for _ in range(n):x=self.step(x)
        return x
    def budget(self,x):
        square=self.w*np.abs(x)**2/64**4
        return np.sum(square*self.K2,axis=(-2,-1))/self.Re+self.alpha*np.sum(square,axis=(-2,-1))

def costs_cpu(initial,delta,lam,chunk=64,workers=8,horizons=None):
    horizons=np.asarray([20.] if horizons is None else horizons)
    M=len(initial);K=6;H=len(horizons)
    result=np.empty((K,M,H))
    end=int(np.ceil((horizons.max()+1)/lam/.01))+35
    for first in range(0,M,chunk):
        z=initial[first:first+chunk];m=len(z)
        model=CPUWorldD(np.full(K*m,40.),delta,np.repeat(np.arange(K),m),workers)
        x=model.to_spec(np.tile(z,(K,1,1)))
        total=np.zeros((K*m,H));counts=np.zeros(H)
        for s in range(end+1):
            if s%35==0:
                t=s*.01
                h=np.flatnonzero((t>=horizons/lam-1e-12)&(t<=(horizons+1)/lam+1e-12))
                if len(h):
                    value=model.budget(x)
                    total[:,h]+=value[:,None];counts[h]+=1
            if s<end:x=model.step(x)
        result[:,first:first+m]=(total/counts).reshape(K,m,H)
        print(f'CPU truth cohort completed {first+m}/{M}',flush=True)
    if not np.isfinite(result).all():raise ValueError('nonfinite CPU truth costs')
    return result
