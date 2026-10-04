"""Baccus FNO: shared windows, fixed objective and all-action stability."""
import argparse
import json
import time
import numpy as np
import torch
from common import ROOT,GRID,ALPHA,patterns,write_json,sha
from train_kolmo import ActionFNO
from evaluate_kolmo import member_windows
from kolmo import KolmoAction

@torch.no_grad()
def main(device,members_per_batch):
    torch.set_num_threads(1)
    info=json.loads((ROOT/'runs/kolmo/system.json').read_text());lam=info['lambda_mean'];sigma=info['sigma']
    cal=json.loads((ROOT/'results/kolmo_calibration.json').read_text());delta=cal['delta']
    learned=ROOT/'runs/kolmo/learned'
    if json.loads((learned/'training.json').read_text())['steps_done']!=30000:raise RuntimeError('training incomplete')
    ck=torch.load(learned/'checkpoint.pt',map_location=device,weights_only=True);scale=ck['sigma']
    model=ActionFNO().to(device);model.load_state_dict(ck['state_dict']);model.eval()
    root=ROOT/'runs/kolmo/test';obs=np.load(root/'observations.npz')['observed']
    K=6;M=256;H=len(GRID);end=int(np.ceil(21/lam/.35));ticks=np.rint(GRID/lam/.35).astype(int)
    action=delta*np.sqrt(8.)*patterns(1)/scale
    for c in range(30):
        path=root/f'neural_{c:03d}.npz'
        if path.exists():continue
        begin=time.time();windows=member_windows(obs[c],sigma,'arm',c,M)/scale
        costs=np.empty((K,M,H));valid=np.ones(M,dtype=bool)
        snapshot_sum=np.zeros((K,H,64,64));snapshot_members=0
        for first in range(0,M,members_per_batch):
            last=min(M,first+members_per_batch);m=last-first
            context=torch.tensor(np.tile(windows[first:last],(K,1,1,1)),dtype=torch.float32,device=device)
            a=torch.tensor(np.repeat(action,m,axis=0),dtype=torch.float32,device=device)
            objective=KolmoAction(np.full(K*m,40.),device=device)
            total=torch.zeros((K*m,H),dtype=torch.float64,device=device);counts=np.zeros(H)
            alive=torch.ones(m,dtype=torch.bool,device=device)
            snaps=torch.empty((K,m,H,64,64),dtype=torch.float32,device=device)
            for s in range(end+1):
                state=context[:,-1]*scale
                stable=torch.isfinite(state).all(dim=(-2,-1)) & (state.square().mean((-2,-1)).sqrt()<=10*sigma)
                alive &= stable.reshape(K,m).all(0)
                t=s*.35;indices=np.flatnonzero((t>=GRID/lam-1e-12)&(t<=(GRID+1)/lam+1e-12))
                if len(indices):
                    # Full learned field, deliberately no model.to_spec() projection.
                    wh=torch.fft.rfft2(state.double())
                    value=objective.grad_sq(wh)/40+ALPHA*objective._mean_sq(wh)
                    total[:,indices]+=value[:,None];counts[indices]+=1
                for h in np.flatnonzero(ticks==s):snaps[:,:,h]=state.reshape(K,m,64,64)
                if s<end:
                    context[~alive.repeat(K)]=0
                    prediction=model(context,a);context=torch.cat([context[:,1:],prediction[:,None]],1)
            keep=alive.cpu().numpy();valid[first:last]=keep
            result=(total/torch.as_tensor(counts,device=device)).cpu().numpy().reshape(K,m,H)
            result[:,~keep]=np.nan;costs[:,first:last]=result
            if first<64:
                n=min(last,64)-first;mask=alive[:n]
                if mask.any():snapshot_sum+=snaps[:,:n][:,mask].double().sum(1).cpu().numpy()
                snapshot_members+=int(mask.sum())
            del context,a,objective,total,snaps
        mean_snapshot=snapshot_sum/snapshot_members if snapshot_members else np.full((K,H,64,64),np.nan)
        np.savez(path,cost=costs,mean_snap=mean_snapshot,valid=valid,actual_snapshot_times=ticks*.35)
        write_json(path.with_suffix('.json'),dict(case=c,dropped=int((~valid).sum()),dropped_first64=int((~valid[:64]).sum()),
                   seconds=time.time()-begin,checkpoint_step=ck['step'],git_sha=sha(),device=device,members_per_batch=members_per_batch))
        print('Kolmo learned case',c+1,'/30 dropped',int((~valid).sum()),flush=True)
    write_json(learned/'evaluation_complete.json',dict(cases=30,git_sha=sha(),checkpoint_step=ck['step']))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--device',default='cuda:0');p.add_argument('--members-per-batch',type=int,default=16)
    a=p.parse_args();main(a.device,a.members_per_batch)
