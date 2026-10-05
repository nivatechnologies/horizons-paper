"""Coordinator-side one-scale inference; never imported by training or selection.

Each invocation owns the sulaco GPU for one case only, under the shared flock.
The process exits before releasing the lock, so validation has no resident rival.
"""
import argparse, datetime, fcntl, json, time
from pathlib import Path
import numpy as np
from protocol import ROOT, SIGMA, LT, WINDOWS, TICKS, PRIMARY, patterns, digest, write_json

def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def register(checkpoint,name,panel):
    record=dict(kind='Stage2 checkpoint and inference source before own test evaluation',name=name,
                panel=panel,recorded_at=now(),checkpoint=str(checkpoint.relative_to(ROOT)),
                checkpoint_sha256=digest(checkpoint),source_hashes={n:digest(ROOT/n) for n in
                ['stage2_inference.py','models.py','protocol.py']})
    training_record=checkpoint.with_suffix('.training.json')
    if training_record.exists():
        record['training_metadata_sha256']=digest(training_record)
        record['training_metadata']=json.loads(training_record.read_text())
    normalization=checkpoint.parent/'normalization.json'
    if normalization.exists():
        record['normalization_sha256']=digest(normalization)
        record['normalization']=json.loads(normalization.read_text())
    marker=checkpoint.parent/(panel+'_registered.json')
    if marker.exists():
        previous=json.loads(marker.read_text())
        if previous['checkpoint_sha256']!=record['checkpoint_sha256']:
            raise RuntimeError('immutable checkpoint changed after registration')
        if previous['source_hashes']==record['source_hashes']:return previous
        record['previous_source_registration']=previous['source_hashes']
    with (ROOT/'AFD_ARTIFACTS.md').open('a') as f:
        fcntl.flock(f,fcntl.LOCK_EX);f.write('\n- '+json.dumps(record)+'\n');f.flush()
    write_json(marker,record)
    return record

def rollout(model,win,sigma,amplitude,micro,last):
    import torch
    state=np.empty((512,last+1,40),dtype=np.float64)
    valid=np.ones((512,last+1),dtype=bool)
    a=amplitude*patterns()/sigma
    with torch.no_grad():
        for first in range(0,512,micro):
            ids=np.arange(first,min(512,first+micro))
            context=torch.tensor(win[ids%64]/sigma,dtype=torch.float32,device='cuda')
            action=torch.tensor(a[ids//64],dtype=torch.float32,device='cuda')
            alive=np.ones(len(ids),dtype=bool)
            for tick in range(last+1):
                x=context[:,-1].cpu().numpy().astype(np.float64)*sigma
                alive &= np.isfinite(x).all(-1)&(np.sqrt(np.mean(x*x,axis=-1))<=10*SIGMA)
                state[ids,tick]=x;valid[ids,tick]=alive
                if tick<last:
                    context[torch.tensor(~alive,device='cuda')]=0.
                    pred=model(context,action)
                    context=torch.cat([context[:,1:],pred[:,None]],1)
    return state.reshape(8,64,last+1,40),valid.reshape(8,64,last+1).all(0)

def state_summary(state,valid):
    means=[];variances=[];cost=[];survivors=[]
    # Response state moments are computed first, then costs, with each lead's paired survivors.
    for window in WINDOWS:
        keep=valid[:,window[-1]];survivors.append(keep)
        means.append(state[:,keep].mean(1) if keep.any() else np.zeros((8,state.shape[2],40)))
        variances.append(state[:,keep].var(1,ddof=0).sum(-1) if keep.any() else np.zeros((8,state.shape[2])))
    for window,keep in zip(WINDOWS,survivors):
        cost.append(.5*np.mean(state[:,keep][:,:,window,:]**2,axis=(1,2,3)) if keep.any() else np.zeros(8))
    return dict(mean=np.array(means),var=np.array(variances),cost=np.array(cost),survivors=np.array(survivors))

def cost_prediction(model,win,sigma,amplitude,micro):
    import torch
    prediction=np.empty((8,64),dtype=np.float64)
    a=amplitude*patterns()/sigma
    with torch.no_grad():
        for first in range(0,512,micro):
            ids=np.arange(first,min(512,first+micro))
            context=torch.tensor(win[ids%64]/sigma,dtype=torch.float32,device='cuda')
            action=torch.tensor(a[ids//64],dtype=torch.float32,device='cuda')
            prediction[ids//64,ids%64]=model(context,action).cpu().numpy().astype(np.float64)
    keep=np.isfinite(prediction).all(0)
    return dict(cost=prediction[:,keep].mean(1) if keep.any() else np.zeros(8),
                survivors=keep,rawprediction=prediction.T)

def main(name,checkpoint,panel,case,micro):
    control=ROOT/'runs/campaign_control.json'
    if control.exists() and json.loads(control.read_text()).get('execution')=='stop':
        print('Campaign stop: no new case evaluation',flush=True);return
    if panel!='test' and panel!='test2':raise RuntimeError('test evaluator cannot select models')
    authorization_path=ROOT/'runs/stage2_authorization.json'
    if not authorization_path.exists():raise RuntimeError('root-issued Stage2 authorization required')
    authorization=json.loads(authorization_path.read_text())
    if authorization.get('authorized') is not True or authorization.get('authority')!='WO v5.2 §9':
        raise RuntimeError('Stage2 continuation not authorized')
    if authorization.get('stage1_reading_sha256')!=digest(ROOT/'runs/stage1_reading.json'):
        raise RuntimeError('Stage1 reading does not match root authorization')
    checkpoint=checkpoint.resolve()
    record=register(checkpoint,name,panel)
    directory=ROOT/'runs'/panel;target=directory/f'{name}_{case:03d}.npz'
    existing=target.exists() and target.with_suffix('.json').exists()
    if existing:
        meta=json.loads(target.with_suffix('.json').read_text())
        if meta['checkpoint_sha256']!=record['checkpoint_sha256']:raise RuntimeError('checkpoint mismatch on resume')
        if panel!='test' or case>=16 or meta.get('primary_decision_timing') is not None:return
    with np.load(directory/f'cpu_{case:03d}.npz') as data:win=data['arm_windows']
    import torch
    from models import Emulator,CostModel,cuda_rules
    cuda_rules();checkpoint_data=torch.load(checkpoint,map_location='cpu',weights_only=True)
    kind=checkpoint_data.get('kind','state');sigma=float(checkpoint_data['sigma'])
    if sigma!=SIGMA:raise RuntimeError('one-scale checkpoint sigma mismatch')
    model=CostModel() if kind=='cost' else Emulator()
    model.load_state_dict(checkpoint_data['state_dict']);model.to('cuda');model.eval()
    amplitude=.32 if panel=='test2' else .16
    # Warmup removes backend/kernel initialization from steady-state per-decision measurement.
    with torch.no_grad():model(torch.zeros((micro,11,40),device='cuda'),torch.zeros((micro,40),device='cuda'))
    torch.cuda.synchronize()
    timing=None
    if panel=='test' and case<16:
        start=time.perf_counter()
        if kind=='cost':timed=cost_prediction(model,win,sigma,amplitude,micro)
        else:
            s,v=rollout(model,win,sigma,amplitude,micro,int(np.ceil(3*LT/.05)))
            keep=v[:,WINDOWS[PRIMARY][-1]]
            predicted=.5*np.mean(s[:,keep][:,:,WINDOWS[PRIMARY],:]**2,axis=(1,2,3)) if keep.any() else np.zeros(8)
            timed=dict(cost=predicted,survivors=keep)
        choice=int(np.argmin(timed['cost']))
        torch.cuda.synchronize();timing=dict(seconds=time.perf_counter()-start,choice=choice,
            survivors=int(timed['survivors'].sum()),includes='input transfer, FP32 inference, paired drops, cost mean and argmin',
            state_through_tick=None if kind=='cost' else int(np.ceil(3*LT/.05)),checkpoint_load_excluded=True)
    if existing:
        meta['primary_decision_timing']=timing
        meta['timing_source_hashes']=record['source_hashes']
        write_json(target.with_suffix('.json'),meta)
        print(panel,name,case,'timing completed',flush=True)
        return
    start=time.perf_counter()
    if kind=='cost':result=cost_prediction(model,win,sigma,amplitude,micro)
    else:
        s,v=rollout(model,win,sigma,amplitude,micro,len(TICKS)-1)
        result=state_summary(s,v)
    torch.cuda.synchronize();elapsed=time.perf_counter()-start
    tmp=target.with_suffix('.partial.npz');np.savez(tmp,**result);tmp.replace(target)
    write_json(target.with_suffix('.json'),dict(case=case,panel=panel,name=name,kind=kind,
        completed_at=now(),shared_all_leads_seconds=elapsed,primary_decision_timing=timing,
        device='cuda',microbatch=micro,checkpoint_sha256=record['checkpoint_sha256'],
        source_hashes=record['source_hashes'],tf32=False,deterministic_cudnn=True))
    print(panel,name,case,'completed',flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--name',required=True);p.add_argument('--checkpoint',type=Path,required=True)
    p.add_argument('--panel',choices=['test','test2'],required=True);p.add_argument('--case',type=int,required=True)
    p.add_argument('--microbatch',type=int,default=8);a=p.parse_args();main(a.name,a.checkpoint,a.panel,a.case,a.microbatch)
