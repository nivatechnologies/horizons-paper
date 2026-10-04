"""Frozen learned arm: paired windows, all-action stability drops, 21 LT rollout."""
import json
import time
import numpy as np
import torch
from common import ROOT,GRID,rng,patterns,write_json,sha
from train_l96 import Emulator

@torch.no_grad()
def main():
    torch.set_num_threads(64)
    cal=json.loads((ROOT/'results/l96_calibration.json').read_text())
    sigma=cal['system']['sigma'];lam=cal['system']['lambda_mean'];delta=cal['delta']
    learned=ROOT/'runs/l96/learned'
    if json.loads((learned/'training.json').read_text())['steps_done']!=20000:
        raise RuntimeError('full prescribed training budget has not completed')
    model=Emulator()
    checkpoint=torch.load(learned/'checkpoint.pt',map_location='cpu',weights_only=True)
    model.load_state_dict(checkpoint['state_dict']);model.eval()
    root=ROOT/'runs/l96/test';obs=np.load(root/'observations.npz')['observed']
    K=8;M=256;H=len(GRID)
    action=8*delta*patterns(0)/sigma
    targets=np.rint(GRID/lam/.05).astype(int)
    end=int(np.ceil(21/lam/.05))
    for c in range(200):
        path=root/f'neural_{c:03d}.npz'
        if path.exists():continue
        start=time.time()
        window=obs[c]+.02*sigma*rng('arm',0,2,c).standard_normal((M,11,40))
        cost=np.empty((K,M,H));snap=np.empty((K,M,H,40));valid=np.ones(M,dtype=bool)
        # Microbatches over members; each contains every candidate action.
        for first in range(0,M,256):
            last=min(M,first+256);m=last-first
            context=torch.tensor(np.tile(window[first:last]/sigma,(K,1,1)),dtype=torch.float32)
            a=torch.tensor(np.repeat(action,m,axis=0),dtype=torch.float32)
            total=np.zeros((K*m,H));counts=np.zeros(H);alive=np.ones(m,dtype=bool)
            snapshots=np.full((K*m,H,40),np.nan)
            for s in range(end+1):
                state=context[:,-1].numpy()*sigma
                stable=np.isfinite(state).all(1)&(np.sqrt(np.mean(state*state,axis=1))<=10*sigma)
                alive &= stable.reshape(K,m).all(0)
                t=s*.05
                indices=np.flatnonzero((t>=GRID/lam-1e-12)&(t<=(GRID+1)/lam+1e-12))
                if len(indices):
                    energy=.5*np.mean(state.astype(np.float64)**2,axis=1)
                    total[:,indices]+=energy[:,None];counts[indices]+=1
                for h in np.flatnonzero(targets==s):snapshots[:,h]=state
                if s<end:
                    invalid=torch.tensor(np.tile(~alive,K))
                    context[invalid]=0
                    prediction=model(context,a)
                    context=torch.cat([context[:,1:],prediction[:,None]],1)
            values=(total/counts).reshape(K,m,H)
            states=snapshots.reshape(K,m,H,40)
            values[:,~alive]=np.nan;states[:,~alive]=np.nan
            cost[:,first:last]=values;snap[:,first:last]=states;valid[first:last]=alive
        mean_snap=np.nanmean(snap[:,:64],axis=1) if valid[:64].any() else np.full((K,H,40),np.nan)
        np.savez(path,cost=cost,mean_snap=mean_snap,valid=valid,
                 actual_snapshot_times=targets*.05,checkpoint_step=checkpoint['step'])
        write_json(root/f'neural_{c:03d}.json',dict(case=c,dropped=int((~valid).sum()),
                   dropped_first64=int((~valid[:64]).sum()),seconds=time.time()-start,git_sha=sha(),threads=64))
        print(f'L96 learned case {c+1}/200 dropped={(~valid).sum()}',flush=True)
    write_json(learned/'evaluation_complete.json',dict(cases=200,git_sha=sha(),checkpoint_step=checkpoint['step']))

if __name__=='__main__':main()
