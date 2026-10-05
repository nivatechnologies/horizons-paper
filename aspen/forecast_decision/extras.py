"""Optional one-scale sensitivity/4D-Var and independent secondary panel. CPU only."""
import argparse, datetime, json, os, platform, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import numba
import numpy as np
from numba import njit
from scipy.optimize import minimize
from protocol import ROOT, LT, SIGMA, TICKS, LEADS, WINDOWS, PRIMARY, patterns, rng, digest, write_json
from physics import rhs, step, history, simulate, costs, identify, flow
from campaign import dt, artifact

def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def access(panel,case):
    record=dict(identity='one_scale_extras physics/data worker; no training or selection',host=platform.node(),pid=os.getpid(),time=now(),panel=panel,case=case,access='raw operational windows/observations only; no Stage1 reading')
    with (ROOT/'runs/extras_access.jsonl').open('a') as f: f.write(json.dumps(record)+'\n')
@njit(cache=True)
def vjp(x,g):
    out=-g.copy()
    for i in range(40):
        out[(i+1)%40]+=g[i]*x[(i-1)%40]
        out[(i-2)%40]-=g[i]*x[(i-1)%40]
        out[(i-1)%40]+=g[i]*(x[(i+1)%40]-x[(i-2)%40])
    return out
@njit(cache=True)
def rkback(x,F,h,g):
    k1=rhs(x,F); b=x+h*.5*k1;k2=rhs(b,F);c=x+h*.5*k2;k3=rhs(c,F);d=x+h*k3
    adj=g.copy();a1=h/6*g;a2=h/3*g;a3=h/3*g;a4=h/6*g
    gd=vjp(d,a4);adj+=gd;a3+=h*gd
    gc=vjp(c,a3);adj+=gc;a2+=h*.5*gc
    gb=vjp(b,a2);adj+=gb;a1+=h*.5*gb
    adj+=vjp(x,a1)
    return adj
@njit(cache=True,nogil=True)
def objective(x,F,window,h):
    nper=int(round(.05/h)); n=10*nper
    states=np.empty((n+1,40));states[0]=x
    for s in range(n):states[s+1]=step(states[s],F,h)
    val=0.;adj=np.zeros(40)
    for s in range(n,-1,-1):
        if s%nper==0:
            diff=states[s]-window[s//nper];val+=np.sum(diff*diff)/440.;adj+=2*diff/440.
        if s>0:adj=rkback(states[s-1],F,h,adj)
    return val,adj

def fit_member(window,F,h):
    tick=time.perf_counter()
    opt=minimize(objective,window[0].copy(),args=(np.full(40,F),window,h),jac=True,method='L-BFGS-B',options={'maxiter':200})
    good=bool(opt.success and np.isfinite(opt.fun) and np.isfinite(opt.x).all())
    # Include instability anywhere on fitted history as an operational member failure.
    states=np.empty((11,40));states[0]=opt.x
    x=opt.x.copy()
    for t in range(1,11):
        for _ in range(int(round(.05/h))):x=step(x,np.full(40,F),h)
        states[t]=x
    good &= bool(np.isfinite(states).all() and (np.sqrt(np.mean(states**2,axis=-1))<=10*SIGMA).all())
    return states[-1],good,dict(success=bool(opt.success),iterations=int(opt.nit),evaluations=int(opt.nfev),seconds=time.perf_counter()-tick,message=str(opt.message))

def summarize(s,alive):
    valid=np.isfinite(s).all(-1)&(np.sqrt(np.mean(s*s,axis=-1))<=10*SIGMA)
    valid=np.logical_and.accumulate(valid,axis=-1).all(0)&alive[:,None]
    means=[];vars=[];cs=[];survivors=[]
    for w in WINDOWS:
        keep=valid[:,w[-1]];survivors.append(keep)
        means.append(s[:,keep].mean(1) if keep.any() else np.zeros((8,len(TICKS),40)))
        vars.append(s[:,keep].var(1,ddof=0).sum(-1) if keep.any() else np.zeros((8,len(TICKS))))
        cs.append(costs(s[:,keep])[...,len(cs)].mean(1) if keep.any() else np.zeros(8))
    return dict(mean=np.array(means),var=np.array(vars),cost=np.array(cs),survivors=np.array(survivors))

def arm(panel,c,name,fit_workers):
    dest=ROOT/f'runs/{panel}/{name}_{c:03d}.npz'
    if dest.exists():return
    access(panel,c)
    with np.load(ROOT/f'runs/{panel}/cpu_{c:03d}.npz') as cpu:
        windows=cpu['arm_windows']
    with np.load(ROOT/f'runs/{panel}/input_{c:03d}.npz') as inp: observed=inp['observed']
    tick=time.perf_counter();F=identify(observed,dt());identify_seconds=time.perf_counter()-tick;fits=[];alive=np.ones(64,bool)
    if name=='N-win':
        with ThreadPoolExecutor(max_workers=fit_workers) as pool: result=list(pool.map(lambda w:fit_member(w,F,dt()),windows))
        initial=np.array([r[0] for r in result]);alive=np.array([r[1] for r in result]);fits=[r[2] for r in result]
        initial[~alive]=8.
    else:initial=windows[:,-1];F*=1.1
    fit_seconds=time.perf_counter()-tick-identify_seconds
    primary_seconds=None
    if c<16:
        # Execute and score through exact primary horizon before full secondary leads.
        primary_states=simulate(np.tile(initial,(8,1)),np.repeat(F+.16*patterns(),64,axis=0),dt(),36).reshape(8,64,36,40)
        energy=.5*np.mean(primary_states*primary_states,axis=-1)
        keep=alive & np.isfinite(primary_states).all((0,2,3)) & (np.sqrt(2*energy)<=10*SIGMA).all((0,2))
        if keep.sum()>=32: chosen=int(energy[:,keep][:,:,WINDOWS[PRIMARY]].mean((1,2)).argmin())
        else: chosen=None
        end=3*LT; n=int(np.floor(end/dt()));f=np.repeat(F+.16*patterns(),64,axis=0)
        z=flow(primary_states[:,:,-1].reshape(512,40),f,n-int(round(1.75/dt())),dt());rem=end-n*dt()
        if rem>0:z=flow(z,f,1,rem)
        primary_seconds=time.perf_counter()-tick
    s=simulate(np.tile(initial,(8,1)),np.repeat(F+.16*patterns(),64,axis=0),dt()).reshape(8,64,len(TICKS),40)
    result=summarize(s,alive);np.savez(dest,**result)
    write_json(dest.with_suffix('.json'),dict(case=c,panel=panel,arm=name,completed_at=now(),host=platform.node(),source_sha256=digest(ROOT/'extras.py'),dt=dt(),identify_seconds=identify_seconds,fit_seconds=fit_seconds,measured_primary_seconds=primary_seconds,primary_timing_includes_identification_fit_cost_and_argmin=c<16,shared_all_leads_seconds=time.perf_counter()-tick,fits=fits,dropped_by_lead=(64-result['survivors'].sum(1)).tolist()))
    artifact(dest,'optional physics arm output');print(panel,name,c,flush=True)

def secondary(c):
    panel='test2';directory=ROOT/'runs/test2';directory.mkdir(parents=True,exist_ok=True);dest=directory/f'cpu_{c:03d}.npz'
    if dest.exists():return
    access(panel,c);h=dt();inp=directory/f'input_{c:03d}.npz'
    if not inp.exists():
        true,y=history('afd-observation-test2',c,h);np.savez(inp,true=true,observed=y);artifact(inp,'secondary case input before evaluation')
    else:
        with np.load(inp) as data:true=data['true'];y=data['observed']
    truth=y+.02*SIGMA*rng('afd-test2-truth',2,c).standard_normal((2048,11,40))
    windows=y+.02*SIGMA*rng('afd-test2-arm',2,c).standard_normal((64,11,40))
    tick=time.perf_counter();F=identify(y,h);p=np.vstack([patterns(),np.zeros(40)])
    s=simulate(np.tile(truth[:,-1],(9,1)),np.repeat(8+.32*p,2048,axis=0),h).reshape(9,2048,len(TICKS),40)
    assert np.isfinite(s).all()
    result=dict(Fhat=np.array(F),arm_windows=windows,truth_cost=costs(s),truth_mean=s.mean(1),truth_var=s.var(1,ddof=0).sum(-1));del s
    truth_seconds=time.perf_counter()-tick
    actual=simulate(np.tile(true[-1],(9,1)),8+.32*p,h);result.update(actual=actual,actual_cost=costs(actual))
    times={}
    for name,forcing in [('N-last',F),('N-oracle',8.)]:
        start=time.perf_counter();s=simulate(np.tile(windows[:,-1],(8,1)),np.repeat(forcing+.32*patterns(),64,axis=0),h).reshape(8,64,len(TICKS),40)
        assert np.isfinite(s).all();result[name+'_cost']=costs(s);result[name+'_mean']=s.mean(1);result[name+'_var']=s.var(1,ddof=0).sum(-1);times[name]=time.perf_counter()-start
    np.savez(dest,**result);artifact(dest,'secondary truth/physics output')
    from work_timing import works
    u=np.repeat(.32*patterns(),2048,axis=0);work=works(np.tile(truth[:,-1],(8,1)),8+u,u,(LEADS+1)*LT,h).reshape(8,2048,len(LEADS),2).mean(1)
    ratios=work[...,1]/work[...,0];assert np.isfinite(ratios).all()
    write_json(directory/f'work_timing_{c:03d}.json',dict(case=c,dt=h,work_base=work[...,0].tolist(),work_action=work[...,1].tolist(),R_W=ratios.tolist(),source_hash=digest(ROOT/'extras.py')))
    write_json(dest.with_suffix('.json'),dict(case=c,completed_at=now(),host=platform.node(),dt=h,delta=.04,truth_seconds=truth_seconds,shared_all_leads_seconds=times,source_sha256=digest(ROOT/'extras.py')))
    print('test2',c,flush=True)

def benchmark(fit_workers):
    # Independent preflight case; no panel access, outcomes or model selection.
    _,y=history('afd-dtcheck',100,dt());F=identify(y,dt());windows=y+.02*SIGMA*rng('afd-dtcheck',2,100).standard_normal((64,11,40))
    objective(windows[0,0],np.full(40,F),windows[0],dt())
    # Exact adjoint compared with centered finite differences, independent point.
    val,g=objective(windows[0,0],np.full(40,F),windows[0],dt());eps=1e-6;fd=np.empty(40)
    for i in range(40):
        d=np.zeros(40);d[i]=eps;fd[i]=(objective(windows[0,0]+d,np.full(40,F),windows[0],dt())[0]-objective(windows[0,0]-d,np.full(40,F),windows[0],dt())[0])/(2*eps)
    err=float(np.max(np.abs(fd-g)));assert err<1e-6
    tick=time.perf_counter()
    with ThreadPoolExecutor(max_workers=fit_workers) as pool: result=list(pool.map(lambda w:fit_member(w,F,dt()),windows))
    seconds=time.perf_counter()-tick
    write_json(ROOT/'runs/extras_benchmark.json',dict(completed_at=now(),host=platform.node(),fit_workers=fit_workers,members=64,seconds=seconds,successful=sum(r[1] for r in result),max_gradient_absolute_error=err,projected_200case_fit_seconds=200*seconds,source_sha256=digest(ROOT/'extras.py')))
    print(json.dumps(dict(seconds=seconds,successful=sum(r[1] for r in result),projection_seconds=200*seconds)),flush=True)
def main():
    p=argparse.ArgumentParser();p.add_argument('task',choices=['benchmark','arms','secondary']);p.add_argument('--workers',type=int,default=96);p.add_argument('--fit-workers',type=int,default=32);p.add_argument('--panel',default='test',choices=['test','val']);p.add_argument('--name',default='N-win',choices=['N-win','N-mis']);p.add_argument('--first',type=int,default=0);p.add_argument('--last',type=int);a=p.parse_args();numba.set_num_threads(a.workers)
    if a.task=='benchmark':benchmark(a.fit_workers)
    elif a.task=='arms':
        for c in range(a.first,a.last if a.last is not None else (200 if a.panel=='test' else 100)):arm(a.panel,c,a.name,a.fit_workers)
    else:
        for c in range(a.first,a.last if a.last is not None else 100):secondary(c)
if __name__=='__main__':main()
