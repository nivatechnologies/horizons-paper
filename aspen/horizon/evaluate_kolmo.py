"""Baccus: frozen test observations, controlled targets and physics arms."""
import argparse
import json
import time
import numpy as np
import torch
from common import ROOT,GRID,BUDGETS,ALPHA,rng,patterns,write_json,sha
from kolmo import KolmoAction
from identify_kolmo import identify

def member_windows(y,sigma,namespace,case,M,action=0):
    return np.stack([y+.02*sigma*rng(namespace,1,2,case,m,action).standard_normal(y.shape) for m in range(M)])

@torch.no_grad()
def rollout(initial,re,delta,lam,device,jitter=False,case=0,neural_targets=False,horizons=None):
    # initial (K,M,64,64); objective uses true benchmark coefficients.
    horizons=GRID if horizons is None else np.asarray(horizons)
    K,M=initial.shape[:2];H=len(horizons);actions=np.repeat(np.arange(K),M)
    model=KolmoAction(np.full(K*M,re),delta,actions,device)
    wh=model.to_spec(initial.reshape(K*M,64,64))
    total=torch.zeros((K*M,H),dtype=torch.float64,device=device);counts=np.zeros(H)
    times=np.rint(horizons/lam/(.35 if neural_targets else .01))*(.35 if neural_targets else .01)
    ticks=np.rint(times/.01).astype(int)
    snapshot=np.empty((K,H,64,64));end=int(np.ceil((horizons.max()+1)/lam/.01))+35
    gen=torch.Generator(device=device)
    gen.manual_seed(int(rng('jitter',1,case=case).integers(2**63-1)))
    for s in range(end+1):
        if s%35==0:
            t=s*.01;indices=np.flatnonzero((t>=horizons/lam-1e-12)&(t<=(horizons+1)/lam+1e-12))
            if len(indices):
                value=model.grad_sq(wh)/40+ALPHA*model._mean_sq(wh)
                total[:,indices]+=value[:,None];counts[indices]+=1
        for h in np.flatnonzero(ticks==s):
            states=model.to_phys(wh).reshape(K,M,64,64)
            snapshot[:,h]=states[:,:min(M,64)].mean(1).cpu().numpy()
        if s<end:
            wh=model.step(wh)
            if jitter:
                physical=model.to_phys(wh)
                perturbation=torch.randn(physical.shape,dtype=torch.float64,device=device,generator=gen)
                wh=model.to_spec(physical*(1+1e-12*perturbation))
    costs=(total/torch.as_tensor(counts,device=device)).cpu().numpy().reshape(K,M,H)
    if not np.isfinite(costs).all() or not np.isfinite(snapshot).all():raise RuntimeError('nonfinite solver test evidence')
    return costs,snapshot,times

@torch.no_grad()
def main(device,part):
    torch.set_num_threads(1)
    if not (ROOT/'AAH_FREEZE_CALIBRATION_KOLMO.md').exists():raise RuntimeError('missing numeric calibration freeze')
    cal=json.loads((ROOT/'results/kolmo_calibration.json').read_text())
    if cal['status']!='READY_FOR_CALIBRATION_FREEZE_ADDENDUM':raise RuntimeError('calibration/chaos did not clear')
    info=json.loads((ROOT/'runs/kolmo/system.json').read_text())
    lam=info['lambda_mean'];sigma=info['sigma'];delta=cal['delta']
    out=ROOT/'runs/kolmo/test';out.mkdir(parents=True,exist_ok=True)
    if part=='prepare':
        if (out/'observations.npz').exists():raise FileExistsError('test panel already generated')
        model=KolmoAction(np.full(30,40.),device=device)
        z=model.random_ic(rng('observation',1),30);z=model.flow(z,50000)
        frames=[]
        for t in range(11):
            frames.append(model.to_phys(z).cpu().numpy())
            if t<10:z=model.flow(z,35)
        true=np.stack(frames,1)
        observed=true+.02*sigma*rng('observation',1,1).standard_normal(true.shape)
        estimates,evals,steps=identify(observed.transpose(1,0,2,3),11,ALPHA,64*sigma,device)
        np.savez(out/'observations.npz',true=true,observed=observed,Re_hat=estimates)
        write_json(out/'observation_metadata.json',dict(git_sha=sha(),sigma=sigma,delta=delta,lambda_mean=lam,
                   identifier='P1x, true drag, Re bounds25..70,30evals',evals=evals,steps=steps))
        print('Kolmo test observations ready',flush=True);return
    data=np.load(out/'observations.npz')
    for c in range(30):
        path=out/f'{part}_{c:03d}.npz'
        if path.exists():continue
        begin=time.time();payload={};timings={}
        if part=='targets':
            initial=np.broadcast_to(data['true'][c,-1],(6,1,64,64)).copy()
            values,snap,times=rollout(initial,40.,delta,lam,device)
            _,net_snap,net_times=rollout(initial,40.,delta,lam,device,neural_targets=True)
            payload.update(actual_cost=values[:,0],actual_snap=snap,neural_target=net_snap,
                           actual_times=times,neural_times=net_times)
        else:
            paired=member_windows(data['observed'][c],sigma,'arm',c,256)[:,-1]
            for arm in ['paired','unpaired','jitter','misidentified']:
                tick=time.time()
                if arm=='unpaired':
                    initial=np.stack([member_windows(data['observed'][c],sigma,'arm',c,256,k+1)[:,-1] for k in range(6)])
                else:initial=np.tile(paired,(6,1,1,1))
                re=44. if arm=='misidentified' else float(data['Re_hat'][c])
                if arm=='paired':
                    cohorts=[];snapshots=[];previous=0;elapsed=0.;profile={}
                    for budget in BUDGETS:
                        cohort_start=time.time()
                        v,snap,times=rollout(initial[:,previous:budget],re,delta,lam,device)
                        cohorts.append(v)
                        if budget<=64:snapshots.append((budget-previous,snap))
                        elapsed+=time.time()-cohort_start;profile[str(budget)]=elapsed;previous=budget
                    values=np.concatenate(cohorts,axis=1)
                    snap=sum(n*s for n,s in snapshots)/64
                    payload['paired_solver_cumulative_seconds']=np.array([profile[str(m)] for m in BUDGETS])
                    myopic,_,_=rollout(initial[:,:64],re,delta,lam,device,horizons=[0.])
                    payload['myopic_cost']=myopic[:,:,0]
                    payload['myopic_chosen']=int(myopic[:,:,0].mean(1).argmin())
                else:
                    values,snap,times=rollout(initial,re,delta,lam,device,jitter=arm=='jitter',case=c)
                payload[arm+'_cost']=values;payload[arm+'_mean_snap']=snap
                timings[arm]=time.time()-tick
        np.savez(path,**payload)
        write_json(path.with_suffix('.json'),dict(case=c,git_sha=sha(),seconds=time.time()-begin,timings=timings,device=device))
        print('Kolmo',part,'case',c+1,'/30',flush=True)
    write_json(out/f'{part}_complete.json',dict(cases=30,git_sha=sha()))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--device',default='cuda:0');p.add_argument('--part',choices=['prepare','targets','arms'],required=True)
    a=p.parse_args();main(a.device,a.part)
