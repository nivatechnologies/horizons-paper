"""Two-scale decision-cost dt check and X-only training/closure, CPU sulaco."""
import argparse,json,time
import numba,numpy as np
from numba import njit,prange
from protocol import *
from physics import flow2,step2
from twoscale_prep import spin,condition
from campaign import artifact
@njit(cache=True,parallel=True)
def slowpaths(z,f,dt,nticks):
    nper=int(round(.05/dt));out=np.empty((len(z),nticks,40))
    for b in prange(len(z)):
        a=z[b].copy()
        for t in range(nticks):
            out[b,t]=a[:40]
            if t<nticks-1:
                for _ in range(nper):a=step2(a,f[b],dt)
    return out
def decision_check():
    directory=ROOT/"runs/twoscale"
    library=np.load(directory/"fastlib.npz")["Y"]
    info=json.loads((directory/"fastlib.json").read_text());sigma=info["sigma_X"]
    dt=info["dt"];rounds=[];selected=[1,2,3]
    while True:
        begins=time.monotonic();rows=[];ranges=[]
        z=spin("afd2-dtcheck",16,dt)
        hist=[z[:,:40].copy()]
        for _ in range(10):
            z=flow2(z,np.full((16,40),10.),int(round(.05/dt)),dt);hist.append(z[:,:40].copy())
        true=np.stack(hist,axis=1)
        for c in range(16):
            y=true[c]+.02*sigma*rng("afd2-dtcheck",1,c).standard_normal((11,40))
            members=y+.02*sigma*rng("afd2-dtcheck",2,c).standard_normal((512,11,40))
            idx=rng("afd2-dtcheck",5,c).integers(4096,size=512)
            fast=condition(library[idx],members,dt)
            ini=np.tile(np.concatenate([members[:,-1],fast],axis=1),(8,1))
            f=np.repeat(10+.2*patterns(),512,axis=0)
            vals=[]
            for resolution in [dt,dt/2]:
                s=slowpaths(ini,f,resolution,37).reshape(8,512,37,40)
                assert np.isfinite(s).all()
                E=.5*np.mean(s*s,axis=-1)
                vals.append(np.stack([E[...,WINDOWS[h]].mean(-1) for h in selected],axis=-1))
            coarse,fine=vals;ranges.append(np.ptp(coarse.mean(1),axis=0));rows.append(vals)
            np.savez(directory/f"dtcheck_{dt}_{c:02d}.npz",coarse=coarse,fine=fine)
            print("two-scale dtcheck",dt,c+1,flush=True)
        SJ=np.median(ranges,axis=0);entries=[];changes=np.zeros(3,dtype=int)
        for c,(coarse,fine) in enumerate(rows):
            for h,H in enumerate(selected):
                b=int(coarse[:,:,h].mean(1).argmin())
                changes[h]+=int(b!=int(fine[:,:,h].mean(1).argmin()))
                for k in range(8):
                    if k==b:continue
                    d=(fine[k,:,h]-fine[b,:,h])-(coarse[k,:,h]-coarse[b,:,h])
                    change=abs(float(d.mean()));se=float(d.std(ddof=1)/np.sqrt(512));bound=max(.05*SJ[h],2*se)
                    entries.append(dict(case=c,h=H,action=k,b=b,change=change,SE=se,
                                        threshold=float(bound),passed=bool(SJ[h]>0 and change<bound)))
        passed=all(e["passed"] for e in entries)
        rounds.append(dict(dt=dt,S_J=SJ.tolist(),argmin_changes=changes.tolist(),
                           comparisons=entries,passed=passed,seconds=time.monotonic()-begins))
        write_json(directory/"decision_dtcheck.json",dict(status="PASS" if passed else "REFINE",chosen_dt=dt if passed else None,rounds=rounds))
        if passed:break
        dt/=2
        # A refinement changes conditioning/library numerical artifacts; do not silently reuse the sampler go.
        raise RuntimeError("two-scale dt refinement requires regenerated library and sampler report before truth")
@njit(cache=True,parallel=True)
def train_paths(z,f,dt,n005):
    nper=int(round(.005/dt));n05=(n005-1)//10+1
    slow=np.empty((len(z),n005,40))
    full=np.empty((len(z),n05,440))
    for b in prange(len(z)):
        a=z[b].copy()
        for t in range(n005):
            slow[b,t]=a[:40]
            if t%10==0:full[b,t//10]=a
            if t<n005-1:
                for _ in range(nper):a=step2(a,f[b],dt)
    return slow,full
def make_training():
    directory=ROOT/"runs/twoscale";out=ROOT/"runs/training_data2";out.mkdir(parents=True,exist_ok=True)
    info=json.loads((directory/"fastlib.json").read_text())
    gate=json.loads((directory/"decision_dtcheck.json").read_text())
    assert gate["status"]=="PASS"
    dt=gate["chosen_dt"];n005=int(np.ceil(25*LT/.05))*10+1
    moments=np.zeros(7);rhs=np.zeros(4);count=0
    for ns,n,label in [("afd2-train",2048,"train"),("afd2-train-val",64,"val")]:
        path=out/f"base_{label}.npz"
        if path.exists():continue
        start=time.monotonic();z=spin(ns,n,dt);hist=[z.copy()]
        for _ in range(10):
            z=flow2(z,np.full((n,40),10.),int(round(.05/dt)),dt);hist.append(z.copy())
        history=np.stack(hist,axis=1)
        R=rng(ns,4);k=R.integers(8,size=n);amp=R.uniform(-.04,.04,size=n)
        action=10*amp[:,None]*patterns()[k]
        slow,full=train_paths(z,10+action,dt,n005)
        assert np.isfinite(slow).all() and np.isfinite(full).all()
        state=np.concatenate([history[:,:-1,:40],full[:,:,:40]],axis=1).astype(np.float32)
        np.savez(path,state=state,action=action.astype(np.float32),index=k,amplitude=amp,sigma=info["sigma_X"])
        np.savez(out/f"full_{label}.npz",state=np.concatenate([history[:,:-1],full],axis=1))
        if label=="train":
            # All closure quantities derive from X only. Y never enters this residual.
            np.savez(out/"X_005_train.npz",X=slow,action=action)
            for b in range(n):
                X=slow[b,1:-1]
                derivative=(slow[b,2:]-slow[b,:-2])/.01
                resolved=(np.roll(X,-1,axis=-1)-np.roll(X,2,axis=-1))*np.roll(X,1,axis=-1)-X
                residual=derivative-resolved-action[b]
                flat=X.reshape(-1);y=residual.reshape(-1)
                power=np.ones_like(flat)
                for p in range(7):
                    moments[p]+=power.sum()
                    if p<4:rhs[p]+=(power*y).sum()
                    power*=flat
                count+=len(flat)
        write_json(out/f"base_{label}.json",dict(trajectories=n,dt=dt,seconds=time.monotonic()-start,
                   sigma=info["sigma_X"],sha256=digest(path)))
        artifact(path,"two-scale base training X before test evaluation")
        print("two-scale train data",label,"complete",flush=True)
    if count:
        matrix=np.array([[moments[i+j] for j in range(4)] for i in range(4)])
        if np.linalg.matrix_rank(matrix)!=4:raise RuntimeError("rank-deficient closure")
        coefficients=np.linalg.solve(matrix,rhs)
        if not np.isfinite(coefficients).all():raise RuntimeError("nonfinite closure")
        write_json(out/"closure.json",dict(c0=float(coefficients[0]),a=coefficients[1:].tolist(),
                 X_rows=count,condition=float(np.linalg.cond(matrix)),normal_matrix=matrix.tolist(),
                 normal_rhs=rhs.tolist(),X_only=True,dt=dt))
        artifact(out/"closure.json","X-only closure before test evaluation")
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("task",choices=["dtcheck","train"]);p.add_argument("--workers",type=int,default=96);a=p.parse_args();numba.set_num_threads(a.workers)
    if a.task=="dtcheck":decision_check()
    else:make_training()

