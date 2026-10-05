"""Validation-only worker; run in a mount namespace containing no test panels."""
import argparse, datetime, hashlib, json, time, os,platform
from pathlib import Path
import numpy as np
import torch
from models import Emulator, CostModel, cuda_rules

def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

def main(checkpoint,inputs,output,micro,model_name='unspecified'):
    cuda_rules()
    d=np.load(inputs)
    windows=d['windows']; truth=d['truth']; actions=d['actions']
    sigma=float(d['sigma']); indices=d['window_indices']
    sj=float(np.median(np.ptp(truth,axis=1)))
    if not np.isfinite(sj) or sj<=0: raise RuntimeError('unavailable validation S_J')
    ck=torch.load(checkpoint,map_location='cpu',weights_only=True)
    kind=ck.get('kind','state')
    output.parent.mkdir(parents=True,exist_ok=True)
    (output.parent/'selection_worker_identity.json').write_text(json.dumps(dict(pid=os.getpid(),model_name=model_name,
            host=platform.node(),step=int(ck['step']),boottime_seconds=time.clock_gettime(time.CLOCK_BOOTTIME)))+'\n')
    model=CostModel() if kind=='cost' else Emulator()
    model.load_state_dict(ck['state_dict'])
    if float(ck['sigma'])!=sigma: raise RuntimeError('sigma mismatch')
    start=time.monotonic();model.to('cuda');model.eval();torch.cuda.synchronize()
    allcost=[]; allkeep=[]; regrets=[]; allmean=[]
    with torch.no_grad():
        for c,win in enumerate(windows):
            prediction=np.empty((8,64),dtype=np.float64)
            alive=np.ones((8,64),dtype=bool)
            mean_states=np.empty((8,64,len(indices),40),dtype=np.float64) if kind!='cost' else None
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
                        if tick in indices:
                            energy+=.5*np.mean(state*state,axis=-1)/len(indices)
                            wi=int(np.flatnonzero(indices==tick)[0])
                            mean_states[ids//64,ids%64,wi]=state
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
            if mean_states is not None:
                allmean.append(mean_states[:,keep].mean(1) if keep.any() else np.zeros((8,len(indices),40)))
    torch.cuda.synchronize(); charged=time.monotonic()-start
    result=dict(step=int(ck['step']),kind=kind,mean_normalized_regret=float(np.mean(regrets)),
                validation_S_J=sj,failed_cases=int(np.sum(np.sum(allkeep,axis=1)<32)),
                dropped_members=int(np.sum(~np.array(allkeep))),charged_gpu_seconds=charged,
                checkpoint_sha256=sha(checkpoint),input_sha256=sha(inputs),
                completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                cases=len(windows),members=64,microbatch=micro,
                isolation='bubblewrap: only validation inputs and selected source exposed')
    output.parent.mkdir(parents=True,exist_ok=True)
    stored=dict(cost=np.array(allcost),survivors=np.array(allkeep),regret=np.array(regrets))
    if allmean:stored['mean_window']=np.array(allmean)
    np.savez(output.with_suffix('.npz'),**stored)
    tmp=output.with_suffix('.tmp');tmp.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');tmp.replace(output)
    candidates=[]
    for path in output.parent.glob('validation_*.json'):
        record=json.loads(path.read_text())
        if not np.isfinite(record['mean_normalized_regret']):continue
        candidates.append((record['mean_normalized_regret'],record['step']))
    if not candidates:raise RuntimeError('no finite checkpoint candidate')
    regret,selected_step=min(candidates)
    decision=dict(step=selected_step,mean_normalized_regret=regret,candidates=len(candidates),
                  selected_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  isolation='checkpoint choice computed inside validation-only bubblewrap namespace')
    choice_tmp=output.parent/'checkpoint_selection.json.tmp'
    choice_tmp.write_text(json.dumps(decision,indent=2,allow_nan=False)+'\n')
    choice_tmp.replace(output.parent/'checkpoint_selection.json')
    print(json.dumps(result),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--checkpoint',type=Path,required=True)
    p.add_argument('--inputs',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--microbatch',type=int,default=8);p.add_argument('--model-name',default='unspecified');a=p.parse_args()
    main(a.checkpoint,a.inputs,a.output,a.microbatch,a.model_name)
