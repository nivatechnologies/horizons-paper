"""Validation-only worker; run in a mount namespace containing no test panels."""
import argparse, datetime, hashlib, json, time
from pathlib import Path
import numpy as np
import torch
from models import Emulator, CostModel, cuda_rules

def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

def main(checkpoint,inputs,output,micro):
    cuda_rules()
    d=np.load(inputs)
    windows=d['windows']; truth=d['truth']; actions=d['actions']
    sigma=float(d['sigma']); indices=d['window_indices']
    sj=float(np.median(np.ptp(truth,axis=1)))
    if not np.isfinite(sj) or sj<=0: raise RuntimeError('unavailable validation S_J')
    ck=torch.load(checkpoint,map_location='cpu',weights_only=True)
    kind=ck.get('kind','state')
    model=CostModel() if kind=='cost' else Emulator()
    model.load_state_dict(ck['state_dict']); model.to('cuda'); model.eval()
    if float(ck['sigma'])!=sigma: raise RuntimeError('sigma mismatch')
    torch.cuda.synchronize(); start=time.monotonic()
    allcost=[]; allkeep=[]; regrets=[]
    with torch.no_grad():
        for c,win in enumerate(windows):
            prediction=np.empty((8,64),dtype=np.float64)
            alive=np.ones((8,64),dtype=bool)
            for first in range(0,512,micro):
                ids=np.arange(first,min(first+micro,512))
                ctx=torch.tensor(win[ids%64]/sigma,dtype=torch.float32,device='cuda')
                action=torch.tensor(actions[ids//64]/sigma,dtype=torch.float32,device='cuda')
                valid=np.ones(len(ids),bool); energy=np.zeros(len(ids))
                if kind=='cost':
                    p=model(ctx,action).cpu().numpy().astype(np.float64)
                    valid&=np.isfinite(p)
                else:
                    for tick in range(int(indices[-1])+1):
                        state=ctx[:,-1].cpu().numpy().astype(np.float64)*sigma
                        valid&=np.isfinite(state).all(-1)&(np.sqrt(np.mean(state*state,axis=-1))<=10*sigma)
                        if tick in indices: energy+=.5*np.mean(state*state,axis=-1)/len(indices)
                        if tick<int(indices[-1]):
                            ctx[torch.tensor(~valid,device='cuda')]=0.
                            pred=model(ctx,action)
                            ctx=torch.cat([ctx[:,1:],pred[:,None]],1)
                    p=energy
                prediction[ids//64,ids%64]=p
                alive[ids//64,ids%64]=valid
            keep=alive.all(0)
            failed=int(keep.sum())<32
            costs=prediction[:,keep].mean(1) if keep.any() else np.zeros(8)
            regret=np.ptp(truth[c])/sj if failed else (truth[c,int(costs.argmin())]-truth[c].min())/sj
            allcost.append(costs);allkeep.append(keep);regrets.append(regret)
    torch.cuda.synchronize(); charged=time.monotonic()-start
    result=dict(step=int(ck['step']),kind=kind,mean_normalized_regret=float(np.mean(regrets)),
                validation_S_J=sj,failed_cases=int(np.sum(np.sum(allkeep,axis=1)<32)),
                dropped_members=int(np.sum(~np.array(allkeep))),charged_gpu_seconds=charged,
                checkpoint_sha256=sha(checkpoint),input_sha256=sha(inputs),
                completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                cases=len(windows),members=64,microbatch=micro,
                isolation='bubblewrap: only validation inputs and selected source exposed')
    output.parent.mkdir(parents=True,exist_ok=True)
    np.savez(output.with_suffix('.npz'),cost=np.array(allcost),survivors=np.array(allkeep),regret=np.array(regrets))
    tmp=output.with_suffix('.tmp');tmp.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');tmp.replace(output)
    print(json.dumps(result),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--checkpoint',type=Path,required=True)
    p.add_argument('--inputs',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--microbatch',type=int,default=8);a=p.parse_args()
    main(a.checkpoint,a.inputs,a.output,a.microbatch)
