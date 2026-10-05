"""Coordinator Stage 2b CPU truth/physics. Explicit sampler GO required."""
import argparse,json,time,platform
import numba,numpy as np
from numba import njit,prange
from protocol import ROOT,LT,WINDOWS,patterns,rng,write_json,digest
from physics import flow2,step2,rhs2
from twoscale_prep import condition
from twoscale_data import slowpaths
from campaign import artifact,now
W2=WINDOWS[:4]
@njit(cache=True)
def closure_rhs(x,f,a):
    out=np.empty(40)
    for k in range(40):
        q=x[k]
        out[k]=(x[(k+1)%40]-x[(k-2)%40])*x[(k-1)%40]-q+f[k]+a[0]*q+a[1]*q*q+a[2]*q*q*q
    return out
@njit(cache=True)
def closure_step(x,f,a):
    dt=.01
    k1=closure_rhs(x,f,a);k2=closure_rhs(x+dt/2*k1,f,a)
    k3=closure_rhs(x+dt/2*k2,f,a);k4=closure_rhs(x+dt*k3,f,a)
    return x+dt/6*(k1+2*k2+2*k3+k4)
@njit(cache=True,parallel=True)
def closure_paths(x,f,a,nticks):
    out=np.empty((len(x),nticks,40))
    for b in prange(len(x)):
        q=x[b].copy()
        for t in range(nticks):
            out[b,t]=q
            if t<nticks-1:
                for _ in range(5):q=closure_step(q,f[b],a)
    return out

@njit(cache=True)
def work_step2(z,f,action,dt):
    k1=rhs2(z,f);q2=z+dt/2*k1;k2=rhs2(q2,f)
    q3=z+dt/2*k2;k3=rhs2(q3,f);q4=z+dt*k3;k4=rhs2(q4,f)
    integral_x=dt/6*(z[:40]+2*q2[:40]+2*q3[:40]+q4[:40])
    return z+dt/6*(k1+2*k2+2*k3+k4),np.mean(action*integral_x),10*np.mean(integral_x)

@njit(cache=True,parallel=True)
def injected_work2(initial,action,dt,endpoints):
    # Integrate at solver resolution, with partial endpoint steps; output-grid averaging is not used.
    numer=np.empty((len(initial),len(endpoints)));denom=np.empty_like(numer)
    for b in prange(len(initial)):
        z=initial[b].copy();t=0.;wn=0.;wd=0.;h=0
        f=10+action[b]
        while h<len(endpoints):
            nxt,dwn,dwd=work_step2(z,f,action[b],dt)
            while h<len(endpoints) and endpoints[h]<=t+dt+1e-12:
                partial=max(0.,endpoints[h]-t)
                end,pwn,pwd=work_step2(z,f,action[b],partial)
                numer[b,h]=wn+pwn
                denom[b,h]=wd+pwd
                h+=1
            wn+=dwn
            wd+=dwd
            z=nxt;t+=dt
    return numer,denom

def identify2(y,a):
    lo=4.;hi=16.;g=(np.sqrt(5)-1)/2
    def objective(f):
        z=closure_paths(y[None,0],np.full((1,40),f),a,11)[0]
        return float(np.mean((z[1:]-y[1:])**2,axis=1).sum())
    c=hi-g*(hi-lo);d=lo+g*(hi-lo);fc=objective(c);fd=objective(d)
    for _ in range(28):
        if fc<fd:
            hi=d;d=c;fd=fc;c=hi-g*(hi-lo);fc=objective(c)
        else:
            lo=c;c=d;fc=fd;d=lo+g*(hi-lo);fd=objective(d)
    return (lo+hi)/2

def metadata():
    folder=ROOT/"runs/twoscale"
    # A coordinator creates this only after the user explicitly approves the report.
    go=json.loads((folder/"sampler_go.json").read_text())
    assert go.get("approved") is True and go.get("approved_by")=="Todd"
    assert go["sampler_check_sha256"]==digest(folder/"sampler_check.json")
    sampler=json.loads((folder/"sampler_check.json").read_text())
    assert sampler["fastlib_sha256"]==digest(folder/"fastlib.npz")
    assert sampler["sampler_raw_sha256"]==digest(folder/"sampler_raw.npz")
    gate=json.loads((folder/"decision_dtcheck.json").read_text());assert gate["status"]=="PASS"
    info=json.loads((folder/"fastlib.json").read_text())
    assert info["sha256"]==sampler["fastlib_sha256"]
    assert info["sigma_X"]==sampler["sigma_X"] and info["sigma_Y"]==sampler["sigma_Y"]
    state=json.loads((folder/"statecheck.json").read_text())
    assert state["status"]=="PASS"
    assert info["dt"]==gate["chosen_dt"]==state["chosen_dt"]==sampler["dt"]
    cl=json.loads((ROOT/"runs/training_data2/closure.json").read_text())
    assert cl["X_only"] and cl["dt"]==gate["chosen_dt"]
    return info,gate["chosen_dt"],cl

def cost2(states):
    energy=.5*np.mean(states*states,axis=-1)
    return np.stack([energy[...,w].mean(-1) for w in W2],axis=-1)

def input_case2(panel,c,dt,sigma):
    folder=ROOT/"runs"/(panel+"2");folder.mkdir(parents=True,exist_ok=True)
    path=folder/f"input_{c:03d}.npz"
    if not path.exists():
        ns="afd2-observation-"+panel
        z=.01*rng(ns,0,c).standard_normal((1,440));z[:,:40]+=10
        z=flow2(z,np.full((1,40),10.),int(np.ceil(50*LT/dt)),dt)
        full=[z[0].copy()]
        for _ in range(10):
            z=flow2(z,np.full((1,40),10.),round(.05/dt),dt);full.append(z[0].copy())
        true=np.stack(full)
        observed=true[:,:40]+.02*sigma*rng(ns,1,c).standard_normal((11,40))
        np.savez(path,true=true[:,:40],observed=observed,full_true=true)
        artifact(path,"two-scale case input before truth/arm evaluation")
    return np.load(path)

def case_cpu2(panel,c):
    info,dt,cl=metadata();sigma=info["sigma_X"]
    folder=ROOT/"runs"/(panel+"2");target=folder/f"cpu_{c:03d}.npz"
    if target.exists():return
    record=input_case2(panel,c,dt,sigma);y=record["observed"]
    library=np.load(ROOT/"runs/twoscale/fastlib.npz")["Y"]
    ns="afd2-"+panel+"-truth";arm_ns="afd2-"+panel+"-arm"
    members=y+.02*sigma*rng(ns,2,c).standard_normal((2048,11,40))
    indices=rng(ns,5,c).integers(len(library),size=2048)
    start=time.perf_counter();fast=condition(library[indices],members,dt)
    initial=np.concatenate([members[:,-1],fast],axis=1)
    p=np.vstack([patterns(),np.zeros(40)])
    states=slowpaths(np.tile(initial,(9,1)),np.repeat(10+.2*p,2048,axis=0),dt,37).reshape(9,2048,37,40)
    if not np.isfinite(states).all():raise RuntimeError("nonfinite two-scale truth")
    result=dict(truth_cost=cost2(states),truth_mean=states.mean(1),truth_var=states.var(1,ddof=0).sum(-1),
                fastlib_index=indices)
    del states
    work_start=time.perf_counter()
    wn,wd=injected_work2(np.tile(initial,(8,1)),np.repeat(.2*patterns(),2048,axis=0),dt,LT*(np.array([0.,1.,1.5,2.])+1))
    result["work_numerator"]=wn.reshape(8,2048,4);result["work_denominator"]=wd.reshape(8,2048,4)
    work_seconds=time.perf_counter()-work_start
    truth_seconds=time.perf_counter()-start
    actual=slowpaths(np.tile(record["full_true"][-1],(9,1)),10+.2*p,dt,37)
    result.update(actual=actual,actual_cost=cost2(actual))
    arm=y+.02*sigma*rng(arm_ns,2,c).standard_normal((64,11,40))
    result["arm_windows"]=arm
    a=np.array(cl["a"]);start=time.perf_counter();fhat=identify2(y,a)
    id_seconds=time.perf_counter()-start;result["Fhat"]=np.array(fhat)
    times={}
    zero=np.zeros(3);fhat_no=identify2(y,zero)
    result["Fhat_noclosure"]=np.array(fhat_no)
    for name,f,a_used in [("N2",fhat,a),("N2-offline",cl["c0"],a),("N2-noclosure",fhat_no,zero)]:
        start=time.perf_counter()
        s=closure_paths(np.tile(arm[:,-1],(8,1)),np.repeat(f+.2*patterns(),64,axis=0),a_used,37).reshape(8,64,37,40)
        if not np.isfinite(s).all():raise RuntimeError("nonfinite "+name)
        result[name+"_cost"]=cost2(s);result[name+"_mean"]=s.mean(1);result[name+"_var"]=s.var(1,ddof=0).sum(-1)
        times[name]=time.perf_counter()-start
    np.savez(target,**result)
    write_json(folder/f"cpu_{c:03d}.json",dict(case=c,panel=panel,completed_at=now(),host=platform.node(),
        dt=dt,physics_dt=.01,sigma=sigma,truth_seconds=truth_seconds,work_seconds=work_seconds,identify_seconds=id_seconds,
        arm_shared_all_leads_seconds=times,closure_sha256=digest(ROOT/"runs/training_data2/closure.json"),
        sampler_go_sha256=digest(ROOT/"runs/twoscale/sampler_go.json"),
        source_hashes={f:digest(ROOT/f) for f in ["twoscale_campaign.py","twoscale_data.py","physics.py","protocol.py","twoscale_prep.py"]}))
    artifact(target,"two-scale truth/physics output")
    print(panel,"two-scale CPU",c+1,flush=True)

def hidden_sensitivity2():
    info,dt,_=metadata()
    folder=ROOT/"runs/test2"
    for c in range(50):
        path=folder/f"hidden_oracle_{c:03d}.npz"
        if path.exists():continue
        record=input_case2("test",c,dt,info["sigma_X"])
        ns="afd2-test-oracle";start=time.perf_counter()
        members=record["observed"]+.02*info["sigma_X"]*rng(ns,2,c).standard_normal((1024,11,40))
        fast=record["full_true"][-1,40:]+.02*info["sigma_Y"]*rng(ns,5,c).standard_normal((1024,400))
        initial=np.concatenate([members[:,-1],fast],axis=1)
        actions=np.vstack([patterns(),np.zeros(40)])
        states=slowpaths(np.tile(initial,(9,1)),np.repeat(10+.2*actions,1024,axis=0),dt,37).reshape(9,1024,37,40)
        if not np.isfinite(states).all():raise RuntimeError("nonfinite hidden sensitivity truth")
        np.savez(path,truth_cost=cost2(states),truth_mean=states.mean(1),truth_var=states.var(1,ddof=0).sum(-1))
        artifact(path,"reported hidden-state sensitivity, excluded from gates")
        write_json(path.with_suffix(".json"),dict(case=c,members=1024,dt=dt,seconds=time.perf_counter()-start,
            namespace=ns,sha256=digest(path),reported_only=True))
        print("hidden sensitivity",c+1,flush=True)

@njit(cache=True,parallel=True)
def climatology_means2(initial,forcing,dt,nsteps):
    result=np.zeros((len(initial),40))
    for b in prange(len(initial)):
        z=initial[b].copy();total=np.zeros(40)
        for _ in range(nsteps):
            z=step2(z,forcing[b],dt);total+=z[:40]
        result[b]=total/nsteps
    return result

def climatology2():
    _,dt,_=metadata();path=ROOT/"runs/twoscale/climatology.npy"
    if path.exists():return
    start=time.perf_counter();z=.01*rng("afd2-climatology",0).standard_normal((8,440));z[:,:40]+=10
    forcing=10+.2*patterns()
    z=flow2(z,forcing,int(np.ceil(50*LT/dt)),dt)
    steps=int(np.ceil(500*LT/dt))
    means=climatology_means2(z,forcing,dt,steps)
    if not np.isfinite(means).all():raise RuntimeError("nonfinite two-scale climatology")
    np.save(path,means);artifact(path,"two-scale per-action climatology before forecast evaluation")
    write_json(path.with_suffix(".json"),dict(dt=dt,steps=steps,LT_ref=LT,averaged_LT_ref=steps*dt/LT,
        seconds=time.perf_counter()-start,sha256=digest(path),namespace="afd2-climatology"))

def inference2(panel,name,checkpoint,micro):
    import torch
    from models import Emulator,CostModel,cuda_rules
    metadata()
    if panel=="test" and not (ROOT/"runs/stage1_reading.json").exists():
        raise RuntimeError("Stage 1 reading required before Stage 2b test access")
    cuda_rules();ck=torch.load(checkpoint,map_location="cpu",weights_only=True)
    sigma=ck["sigma"];is_cost=name=="CNN2-cost"
    model=CostModel() if is_cost else Emulator();model.load_state_dict(ck["state_dict"])
    model.to("cuda");model.eval();artifact(checkpoint,"checkpoint before two-scale "+panel+" evaluation")
    folder=ROOT/"runs"/(panel+"2")
    for c in range(100 if panel=="val" else 200):
        path=folder/f"{name}_{c:03d}.npz"
        if path.exists():continue
        cpu=folder/f"cpu_{c:03d}.npz"
        if not cpu.exists():raise RuntimeError("two-scale CPU panel incomplete")
        with np.load(cpu) as data:win=data["arm_windows"]
        start=time.perf_counter();actions=.2*patterns()/sigma
        if is_cost:
            values=np.empty(512)
        else:
            states=np.empty((512,37,40));valid=np.ones((512,37),bool)
        with torch.no_grad():
            for first in range(0,512,micro):
                ids=np.arange(first,min(512,first+micro))
                context=torch.tensor(win[ids%64]/sigma,dtype=torch.float32,device="cuda")
                act=torch.tensor(actions[ids//64],dtype=torch.float32,device="cuda")
                if is_cost:
                    values[ids]=model(context,act).reshape(-1).cpu().numpy()
                else:
                    alive=np.ones(len(ids),bool)
                    for t in range(37):
                        state=context[:,-1].cpu().numpy().astype(np.float64)*sigma
                        alive&=np.isfinite(state).all(-1)&(np.sqrt(np.mean(state*state,axis=-1))<=10*sigma)
                        states[ids,t]=state;valid[ids,t]=alive
                        if t<36:
                            context[torch.tensor(~alive,device="cuda")]=0.
                            pred=model(context,act);context=torch.cat([context[:,1:],pred[:,None]],1)
        if is_cost:
            values=values.reshape(8,64);keep=np.isfinite(values).all(0)
            output=dict(cost=values[:,keep].mean(1) if keep.any() else np.zeros(8),survivors=keep)
        else:
            st=states.reshape(8,64,37,40);v=valid.reshape(8,64,37).all(0)
            means=[];variances=[];cs=[];survivors=[]
            for h,w in enumerate(W2):
                keep=v[:,w[-1]];survivors.append(keep)
                means.append(st[:,keep].mean(1) if keep.any() else np.zeros((8,37,40)))
                variances.append(st[:,keep].var(1,ddof=0).sum(-1) if keep.any() else np.zeros((8,37)))
                cs.append(cost2(st[:,keep])[...,h].mean(1) if keep.any() else np.zeros(8))
            output=dict(mean=np.array(means),var=np.array(variances),cost=np.array(cs),survivors=np.array(survivors))
        torch.cuda.synchronize();np.savez(path,**output)
        write_json(folder/f"{name}_{c:03d}.json",dict(case=c,completed_at=now(),device="cuda",microbatch=micro,
            checkpoint_sha256=digest(checkpoint),sigma=sigma,tf32=False,deterministic_cudnn=True,
            shared_all_leads_seconds=time.perf_counter()-start))
        print(panel,name,c+1,flush=True)

if __name__=="__main__":
    from pathlib import Path
    p=argparse.ArgumentParser();p.add_argument("task",choices=["cpu","cnn","climate","oracle"],default="cpu",nargs="?");p.add_argument("--panel",choices=["val","test"],default="val");p.add_argument("--workers",type=int,default=96)
    p.add_argument("--name");p.add_argument("--checkpoint",type=Path);p.add_argument("--microbatch",type=int,default=8);args=p.parse_args()
    if args.task=="oracle":
        numba.set_num_threads(args.workers);hidden_sensitivity2()
    elif args.task=="climate":
        numba.set_num_threads(args.workers);climatology2()
    elif args.task=="cnn":inference2(args.panel,args.name,args.checkpoint,args.microbatch)
    else:
        numba.set_num_threads(args.workers);metadata()
        artifact(ROOT/"runs/training_data2/closure.json","X-only closure before two-scale panel evaluation")
        artifact(ROOT/"runs/twoscale/fastlib.npz","conditioned fast library before two-scale panel evaluation")
        for c in range(100 if args.panel=="val" else 200):case_cpu2(args.panel,c)
