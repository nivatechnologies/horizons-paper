"""Coordinator CPU truth-work replay and measured primary physics timing."""
import argparse,time,json
import numba,numpy as np
from numba import njit,prange
from protocol import *
from physics import rhs,step,simulate,identify
from campaign import dt
@njit(cache=True)
def quadrature(x,F,u,dt):
    k1=rhs(x,F);x2=x+.5*dt*k1;k2=rhs(x2,F)
    x3=x+.5*dt*k2;k3=rhs(x3,F);x4=x+dt*k3
    avg=(x+2*x2+2*x3+x4)/6
    base=0.;action=0.
    for i in range(40):
        base+=8*avg[i]/40
        action+=u[i]*avg[i]/40
    return dt*base,dt*action
@njit(cache=True,parallel=True)
def works(initial,forcing,actions,ends,dt):
    result=np.empty((len(initial),len(ends),2))
    last=int(np.ceil(ends[-1]/dt))
    for b in prange(len(initial)):
        x=initial[b].copy();base=0.;action=0.;nextend=0
        for s in range(last):
            t=s*dt
            while nextend<len(ends) and ends[nextend]<=t+dt+1e-12:
                remainder=max(0.,ends[nextend]-t)
                wb,wa=quadrature(x,forcing[b],actions[b],remainder)
                result[b,nextend,0]=base+wb;result[b,nextend,1]=action+wa
                nextend+=1
            wb,wa=quadrature(x,forcing[b],actions[b],dt)
            base+=wb;action+=wa;x=step(x,forcing[b],dt)
    return result
def main(workers):
    numba.set_num_threads(workers)
    ends=(LEADS+1)*LT
    # JIT warm-up is excluded from reported per-decision time.
    works(np.zeros((1,40)),np.full((1,40),8.),np.zeros((1,40)),ends,dt())
    for c in range(200):
        dest=ROOT/f"runs/test/work_timing_{c:03d}.json"
        if dest.exists():continue
        inp=np.load(ROOT/f"runs/test/input_{c:03d}.npz");y=inp["observed"]
        members=y+.02*SIGMA*rng("afd-test-truth",2,c).standard_normal((2048,11,40))
        u=np.repeat(.16*patterns(),2048,axis=0)
        work=works(np.tile(members[:,-1],(8,1)),8+u,u,ends,dt()).reshape(8,2048,len(LEADS),2)
        mean=work.mean(1);den=mean[...,0]
        ratios=np.divide(mean[...,1],den,out=np.full_like(den,np.nan),where=den!=0)
        if not np.isfinite(ratios).all():raise RuntimeError("undefined injected-work ratio")
        measurement=None
        if c<16:
            windows=y+.02*SIGMA*rng("afd-test-arm",2,c).standard_normal((64,11,40))
            start=time.perf_counter();Fhat=identify(y,dt())
            # Measure integration through T+W, including final fractional step.
            nstep=int(np.floor(3*LT/dt()));x=np.tile(windows[:,-1],(8,1))
            f=np.repeat(Fhat+.16*patterns(),64,axis=0)
            from physics import flow
            x=flow(x,f,nstep,dt())
            remainder=3*LT-nstep*dt()
            if remainder>0:x=flow(x,f,1,remainder)
            assert np.isfinite(x).all()
            measurement=time.perf_counter()-start
        write_json(dest,dict(case=c,dt=dt(),work_base=mean[...,0].tolist(),
             work_action=mean[...,1].tolist(),R_W=ratios.tolist(),
             rule="ratio of member-mean integrated work per case/action, then average cases",
             measured_primary_Nlast_seconds=measurement,primary_seconds_case_sample=c<16,
             integrator="same RK4 stages, exact endtime via partial quadrature without changing sampled trajectory",
             source_hash=digest(ROOT/"work_timing.py")))
        print("work",c+1,flush=True)
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--workers",type=int,default=96);main(p.parse_args().workers)

