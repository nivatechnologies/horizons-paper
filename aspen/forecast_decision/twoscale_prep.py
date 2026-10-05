"""Two-scale state check, independent fast library, twins and sampler report."""
import argparse,time,datetime,json
import numba,numpy as np
from numba import njit,prange
from protocol import *
from physics import flow2,step2
@njit(cache=True)
def fast_rhs(y,x):
    out=np.empty(400)
    for q in range(400):
        out[q]=-100*y[(q+1)%400]*(y[(q+2)%400]-y[(q-1)%400])-10*y[q]+x[q//10]
    return out
@njit(cache=True,parallel=True)
def condition(init,histories,dt):
    out=init.copy()
    for b in prange(len(out)):
        y=out[b].copy();nper=int(round(.05/dt))
        for frame in range(10):
            for s in range(nper):
                a=s/nper;d=1/nper
                x=histories[b,frame]*(1-a)+histories[b,frame+1]*a
                xm=histories[b,frame]*(1-a-.5*d)+histories[b,frame+1]*(a+.5*d)
                xe=histories[b,frame]*(1-a-d)+histories[b,frame+1]*(a+d)
                k1=fast_rhs(y,x);k2=fast_rhs(y+dt/2*k1,xm)
                k3=fast_rhs(y+dt/2*k2,xm);k4=fast_rhs(y+dt*k3,xe)
                y=y+dt/6*(k1+2*k2+2*k3+k4)
        out[b]=y
    return out
def spin(name,n,dt):
    z=.01*rng(name,0).standard_normal((n,440));z[:,:40]+=10
    return flow2(z,np.full((n,40),10.),int(np.ceil(50*LT/dt)),dt)
def correlations(mean,actual):
    spread=mean.std();spread2=actual.std()
    return float(np.corrcoef(mean.reshape(-1),actual.reshape(-1))[0,1]) if spread>0 and spread2>0 else None
def main(workers):
    numba.set_num_threads(workers);directory=ROOT/"runs/twoscale";directory.mkdir(parents=True,exist_ok=True)
    begin=time.monotonic()
    dt=.001;rounds=[]
    while True:
        z=spin("afd2-statecheck",16,dt)
        coarse=flow2(z,np.full((16,40),10.),int(round(.1/dt)),dt)
        fine=flow2(z,np.full((16,40),10.),int(round(.1/(dt/2))),dt/2)
        sigma=float(np.sqrt(np.mean(z[:,:40]**2)))
        difference=float(np.max(np.abs(coarse[:,:40]-fine[:,:40])))
        passed=difference<=1e-6*sigma
        rounds.append(dict(dt=dt,sigma_X=sigma,max_abs_X_difference=difference,
                           threshold=1e-6*sigma,passed=passed))
        write_json(directory/"statecheck.json",dict(status="PASS" if passed else "REFINE",rounds=rounds,
                   chosen_dt=dt if passed else None))
        if passed:break
        dt/=2
    path=directory/"fastlib.npz"
    if not path.exists():
        library=spin("afd2-fastlib",4096,dt)
        np.savez(path,Y=library[:,40:],X=library[:,:40])
    library=np.load(path);sigmax=float(np.sqrt(np.mean(library["X"]**2)));sigmay=float(np.sqrt(np.mean(library["Y"]**2)))
    write_json(directory/"fastlib.json",dict(states=4096,sha256=digest(path),sigma_X=sigmax,sigma_Y=sigmay,dt=dt))
    z=spin("afd2-twin",16,dt)
    histories=[z.copy()]
    for _ in range(10):
        z=flow2(z,np.full((16,40),10.),int(round(.05/dt)),dt);histories.append(z.copy())
    true=np.stack(histories,axis=1)
    observed=true[:,:,:40]+.02*sigmax*rng("afd2-twin",1).standard_normal((16,11,40))
    members=observed[:,None]+.02*sigmax*rng("afd2-twin",2).standard_normal((16,64,11,40))
    indices=rng("afd2-twin",5).integers(4096,size=16*64)
    conditioned=condition(library["Y"][indices],members.reshape(-1,11,40),dt)
    draws=-conditioned.reshape(16,64,40,10).sum(-1)
    realized=-true[:,-1,40:].reshape(16,40,10).sum(-1)
    mean=draws.mean(1);error=mean-realized;spread=draws.std(1,ddof=1)
    err=float(np.sqrt(np.mean(error*error)));sd=float(np.sqrt(np.mean(spread*spread)))
    ratio=sd/err if err>0 else None
    corr=correlations(mean,realized)
    np.savez(directory/"sampler_raw.npz",draws=draws,realized=realized,members=members,conditioned=conditioned,
             true= true,observed=observed)
    state_ratios=[];state_corr=[]
    for c in range(16):
        e=np.sqrt(np.mean(error[c]**2))
        state_ratios.append(float(np.sqrt(np.mean(spread[c]**2))/e) if e>0 else None)
        state_corr.append(correlations(mean[c],realized[c]))
    write_json(directory/"sampler_check.json",dict(states=16,draws_per_state=64,ratio_spread_to_mean_error=ratio,
        rms_draw_spread=sd,rms_mean_error=err,mean_realized_correlation=corr,
        state_ratios=state_ratios,state_correlations=state_corr,sigma_X=sigmax,sigma_Y=sigmay,
        fastlib_sha256=digest(path),sampler_raw_sha256=digest(directory/"sampler_raw.npz"),
        dt=dt,seconds=time.monotonic()-begin,status="AWAITING_TODD_GO_FOR_TRUTH",
        produced_at=datetime.datetime.now(datetime.timezone.utc).isoformat()))
    # Error-growth twins: shared library draws, X noise perturbation on second history.
    h0=observed.copy()
    h1=h0+.02*sigmax*rng("afd2-twin",5,member=1).standard_normal(h0.shape)
    idx=indices.reshape(16,64)[:,0]
    y0=condition(library["Y"][idx],h0,dt);y1=condition(library["Y"][idx],h1,dt)
    base=np.concatenate([h0[:,-1],y0],1);twin=np.concatenate([h1[:,-1],y1],1)
    curve=[]
    for t in range(len(TICKS[:37])):
        rmse=np.sqrt(np.mean((base[:,:40]-twin[:,:40])**2,axis=1))/sigmax
        a=base[:,:40]-base[:,:40].mean(1)[:,None]
        b=twin[:,:40]-twin[:,:40].mean(1)[:,None]
        acc=np.sum(a*b,axis=1)/np.sqrt(np.sum(a*a,axis=1)*np.sum(b*b,axis=1))
        curve.append(dict(time=t*.05,lead_ref=t*.05/LT,median_normalized_RMSE=float(np.median(rmse)),
                          median_ACC=float(np.median(acc))))
        base=flow2(base,np.full((16,40),10.),int(round(.05/dt)),dt)
        twin=flow2(twin,np.full((16,40),10.),int(round(.05/dt)),dt)
    write_json(directory/"twins.json",dict(curve=curve,crossings={str(th):next((r["lead_ref"] for r in curve if r["median_ACC"]<th),None) for th in [.9,.5]}))
    print("sampler report ready",ratio,corr,flush=True)
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--workers",type=int,default=64);main(p.parse_args().workers)

