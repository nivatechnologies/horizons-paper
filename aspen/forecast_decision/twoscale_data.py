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
        if path.exists() and (out/f"full_{label}.npz").exists() and (label!="train" or (out/"X_005_train.npz").exists()):continue
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
        artifact(out/f"full_{label}.npz","two-scale full training states: solver labels only")
        if label=="train":artifact(out/"X_005_train.npz","X-only closure inputs before fit")
        print("two-scale train data",label,"complete",flush=True)
    if not count and not (out/"closure.json").exists():
        # Resume from the recorded X-only artifact, never from hidden-state tendencies.
        data=np.load(out/"X_005_train.npz");slow=data["X"];actions=data["action"]
        for b in range(len(slow)):
            X=slow[b,1:-1]
            derivative=(slow[b,2:]-slow[b,:-2])/.01
            resolved=(np.roll(X,-1,axis=-1)-np.roll(X,2,axis=-1))*np.roll(X,1,axis=-1)-X
            flat=X.reshape(-1);y=(derivative-resolved-actions[b]).reshape(-1)
            power=np.ones_like(flat)
            for p in range(7):
                moments[p]+=power.sum()
                if p<4:rhs[p]+=(power*y).sum()
                power*=flat
            count+=len(flat)
    if count:
        matrix=np.array([[moments[i+j] for j in range(4)] for i in range(4)])
        if np.linalg.matrix_rank(matrix)!=4:raise RuntimeError("rank-deficient closure")
        coefficients=np.linalg.solve(matrix,rhs)
        if not np.isfinite(coefficients).all():raise RuntimeError("nonfinite closure")
        write_json(out/"closure.json",dict(c0=float(coefficients[0]),a=coefficients[1:].tolist(),
                 X_rows=count,condition=float(np.linalg.cond(matrix)),normal_matrix=matrix.tolist(),
                 normal_rhs=rhs.tolist(),X_only=True,dt=dt))
        artifact(out/"closure.json","X-only closure before test evaluation")
def make_labels():
    directory=ROOT/"runs/twoscale";out=ROOT/"runs/training_data2"
    info=json.loads((directory/"fastlib.json").read_text());sigma=info["sigma_X"]
    gate=json.loads((directory/"decision_dtcheck.json").read_text())
    assert gate["status"]=="PASS";dt=gate["chosen_dt"]
    full=np.load(out/"full_train.npz")["state"]
    library=np.load(directory/"fastlib.npz")["Y"]
    for kind,n,ns in [("pairs",4096,"afd2-train-pairs"),("cost",16384,"afd2-train-cost")]:
        path=out/(kind+".npz")
        if path.exists():continue
        started=time.monotonic();R=rng(ns,6)
        traj=R.integers(len(full),size=n);ticks=R.integers(10,full.shape[1],size=n)
        hist=np.stack([full[i,t-10:t+1,:40] for i,t in zip(traj,ticks)])
        obs=hist+.02*sigma*rng(ns,1).standard_normal(hist.shape)
        if kind=="pairs":
            pairset=np.array([(j,k) for j in range(8) for k in range(j+1,8)])
            pair=pairset[rng(ns,4).integers(28,size=n)]
            amp=rng(ns,4,member=1).uniform(-.04,.04,size=n)
            action=10*amp[:,None,None]*patterns()[pair]
            targets=np.empty((n,2,36,40),np.float32)
            for first in range(0,n,128):
                last=min(n,first+128);m=last-first
                initial=full[traj[first:last],ticks[first:last]]
                states=slowpaths(np.repeat(initial,2,axis=0),(10+action[first:last]).reshape(-1,40),dt,37)
                if not np.isfinite(states).all():raise RuntimeError("nonfinite two-scale pair target")
                targets[first:last]=states[:,1:].reshape(m,2,36,40)
            np.savez(path,window=obs.astype(np.float32),action=action.astype(np.float32),targets=targets,
                     trajectory=traj,time_index=ticks,sigma=sigma)
        else:
            member=obs+.02*sigma*rng(ns,2).standard_normal(hist.shape)
            indices=rng(ns,5).integers(len(library),size=n)
            fast=condition(library[indices],member,dt)
            action=.2*patterns();labels=np.empty((n,8),np.float64)
            initial=np.concatenate([member[:,-1],fast],axis=1)
            for first in range(0,n,128):
                last=min(n,first+128);m=last-first
                states=slowpaths(np.repeat(initial[first:last],8,axis=0),np.tile(10+action,(m,1)),dt,36)
                if not np.isfinite(states).all():raise RuntimeError("nonfinite two-scale cost label")
                energy=.5*np.mean(states*states,axis=-1)
                labels[first:last]=energy[:,WINDOWS[PRIMARY]].mean(-1).reshape(m,8)
            centered=labels-labels.mean(1)[:,None]
            vd=float(np.mean(centered**2));vm=float(labels.mean(1).var(ddof=0))
            if not np.isfinite([vd,vm]).all() or vd<=0 or vm<=0:raise RuntimeError("invalid cost variance")
            np.savez(path,window=member.astype(np.float32),action=action.astype(np.float32),labels=labels,
                     variance_diff=vd,variance_mean=vm,trajectory=traj,time_index=ticks,sigma=sigma,
                     fastlib_index=indices)
        artifact(path,"two-scale solver training labels before model evaluation")
        write_json(out/(kind+".json"),dict(starts=n,dt=dt,seconds=time.monotonic()-started,
            sha256=digest(path),namespace=ns,sigma=sigma,source_sha256=digest(ROOT/"twoscale_data.py"),
            full_train_sha256=digest(out/"full_train.npz"),fastlib_sha256=digest(directory/"fastlib.npz")))
        print("two-scale labels",kind,"complete",flush=True)
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("task",choices=["dtcheck","train","labels"]);p.add_argument("--workers",type=int,default=96);a=p.parse_args();numba.set_num_threads(a.workers)
    if a.task=="dtcheck":decision_check()
    elif a.task=="train":make_training()
    else:make_labels()
