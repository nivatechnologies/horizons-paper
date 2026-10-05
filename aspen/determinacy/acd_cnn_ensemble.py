"""Standalone frozen CNN-20k inference; observations only, sulaco GPU only."""
import os
os.environ['JAX_PLATFORMS']='cpu'
os.environ['JAX_ENABLE_X64']='true'
import argparse,time,json
import numpy as np
import torch
from torch import nn
from acd_protocol import ROOT,INHERITED,SIGMA,NOISE,PATTERNS,WINDOWS,TICKS,physics,rng,load_observed,digest,save_json,resolution
from acd_confirmation import verify_freeze,event

class Emulator(nn.Module):
    def __init__(self):
        super().__init__();sizes=[12,256,256,256,256,1];layers=[]
        for i in range(5):
            k=5 if i<4 else 1
            layers.append(nn.Conv1d(sizes[i],sizes[i+1],k,padding=k//2,padding_mode='circular'))
            if i<4:layers.append(nn.GELU())
        self.net=nn.Sequential(*layers)
    def forward(self,frames,action):
        return frames[:,-1]+self.net(torch.cat([frames,action[:,None]],1))[:,0]

def predict(model,windows,sigma,micro):
    last=int(WINDOWS[3][-1]);energies=np.empty((128*9,last+1));valid=np.ones(128*9,bool)
    with torch.inference_mode():
        for first in range(0,128*9,micro):
            ids=np.arange(first,min(128*9,first+micro))
            # Action-major layout, identical encoding to inherited campaign.inference.
            context=torch.tensor(windows[ids%128]/sigma,dtype=torch.float32,device='cuda')
            action=torch.tensor(.16*PATTERNS[ids//128]/sigma,dtype=torch.float32,device='cuda')
            alive=np.ones(len(ids),bool)
            for t in range(last+1):
                state=context[:,-1].cpu().numpy().astype(np.float64)*sigma
                alive &= np.isfinite(state).all(-1)&(np.sqrt(np.mean(state*state,axis=-1))<=10*SIGMA)
                energies[ids,t]=.5*np.mean(state*state,axis=-1)
                if t<last:
                    context[torch.tensor(~alive,device='cuda')]=0
                    pred=model(context,action)
                    context=torch.cat([context[:,1:],pred[:,None]],1)
            valid[ids]=alive
    shared=valid.reshape(9,128).all(0)
    J=energies.reshape(9,128,last+1)[:,:,WINDOWS[3]].mean(-1).T
    return J[shared],shared

def run(micro):
    verify_freeze();torch.set_num_threads(1)
    torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
    torch.backends.cudnn.deterministic=True;torch.backends.cudnn.benchmark=False
    checkpoint=INHERITED/'inputs/CNN-20k.pt'
    ckpt=torch.load(checkpoint,map_location='cpu',weights_only=True)
    assert ckpt['step']==20000 and ckpt['sigma']==SIGMA
    model=Emulator();model.load_state_dict(ckpt['state_dict']);model.eval();cut=False
    try:model.to('cuda')
    except torch.cuda.OutOfMemoryError:
        cut=True;resolution('R-gpu','CNN model cannot fit','Cut R6; Qwen left running')
    for c in range(200):
        directory=ROOT/'runs/conf';p=directory/f'cnn_{c:03d}.npz';receipt=p.with_suffix('.json')
        if receipt.exists():continue
        while not (directory/f'case_{c:03d}.json').exists():time.sleep(2)
        start=time.perf_counter();y=load_observed('conf',c)
        windows=np.array([y+NOISE*rng('acd-sampler-conf',0,c,m).standard_normal(y.shape) for m in range(128)])
        current=micro
        while not cut:
            try:
                J,shared=predict(model,windows,SIGMA,current);break
            except torch.cuda.OutOfMemoryError:
                torch.cuda.empty_cache()
                if current<=1:
                    cut=True;resolution('R-gpu',f'CNN case {c} does not fit at microbatch1','Cut R6; Qwen left running');break
                current=max(1,current//2)
                resolution('R-gpu',f'CNN case {c} GPU memory shortage',dict(microbatch=current))
        if cut:
            save_json(receipt,dict(case=c,status='CUT R-gpu',checkpoint_sha256=digest(checkpoint)))
            event(c,'cnn_written_and_hashed',[receipt])
        else:
            torch.cuda.synchronize();np.savez(p,J_2LT=J,valid=shared)
            save_json(receipt,dict(case=c,status='COMPLETE',members=int(shared.sum()),microbatch=current,
                                  seconds=time.perf_counter()-start,checkpoint_sha256=digest(checkpoint),
                                  sha256=digest(p),lead=2,device='cuda',tf32=False,deterministic_cudnn=True))
            event(c,'cnn_written_and_hashed',[p,receipt]);micro=current
        print('CNN',c,'cut' if cut else int(shared.sum()),'micro',current,flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--microbatch',type=int,default=2);a=p.parse_args();run(a.microbatch)
