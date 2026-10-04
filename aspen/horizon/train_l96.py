"""Frozen periodic action-conditioned residual CNN; independent validation."""
import json
import time
import numpy as np
import torch
from torch import nn
from common import ROOT,rng,write_json,sha

class Emulator(nn.Module):
    def __init__(self):
        super().__init__()
        sizes=[12,256,256,256,256,1]
        layers=[]
        for i in range(5):
            k=5 if i<4 else 1
            layers.append(nn.Conv1d(sizes[i],sizes[i+1],k,padding=k//2,padding_mode='circular'))
            if i<4:layers.append(nn.GELU())
        self.net=nn.Sequential(*layers)
    def forward(self,frames,action):
        return frames[:,-1]+self.net(torch.cat([frames,action[:,None]],1))[:,0]

def main():
    torch.set_num_threads(16);torch.manual_seed(0)
    cal=json.loads((ROOT/'results/l96_calibration.json').read_text())
    sigma=cal['system']['sigma'];lam=cal['system']['lambda_mean']
    out=ROOT/'runs/l96/learned'
    if (out/'checkpoint.pt').exists():raise FileExistsError('checkpoint exists')
    train=np.load(out/'train.npz');val=np.load(out/'val.npz')
    X=train['state']/sigma;A=train['action']/sigma
    V=val['state']/sigma;VA=val['action']/sigma
    R=rng('train',0,6);RV=rng('val',0,6)
    noise=.02*RV.standard_normal((64,11,40))
    vctx=torch.tensor(V[:,:11]+noise,dtype=torch.float32)
    va=torch.tensor(VA,dtype=torch.float32)
    stepsLT=max(1,int(round(1/lam/.05)))
    target=torch.tensor(V[:,11:11+stepsLT],dtype=torch.float32)
    model=Emulator();opt=torch.optim.AdamW(model.parameters(),lr=1e-3,weight_decay=1e-4)
    scheduler=torch.optim.lr_scheduler.CosineAnnealingLR(opt,20000)
    best=float('inf');begin=time.time();log=[]
    for iteration in range(1,20001):
        b=R.integers(len(X),size=128);t=R.integers(X.shape[1]-14,size=128)
        frames=np.stack([X[i,j:j+15] for i,j in zip(b,t)])
        ctx=torch.tensor(frames[:,:11]+.02*R.standard_normal((128,11,40)),dtype=torch.float32)
        action=torch.tensor(A[b],dtype=torch.float32)
        targets=torch.tensor(frames[:,11:],dtype=torch.float32)
        loss=0.
        for j in range(4):
            pred=model(ctx,action)
            error=((pred-targets[:,j])**2).mean()
            loss=loss+error/4+(error if j==0 else 0)
            ctx=torch.cat([ctx[:,1:],pred[:,None]],1)
        if not torch.isfinite(loss):raise RuntimeError(f'nonfinite training loss at {iteration}')
        opt.zero_grad();loss.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),1.)
        opt.step();scheduler.step()
        if iteration%1000==0:
            model.eval()
            with torch.no_grad():
                ctx=vctx.clone();mse=0.
                for j in range(stepsLT):
                    pred=model(ctx,va);mse+=((pred-target[:,j])**2).mean().item()/stepsLT
                    ctx=torch.cat([ctx[:,1:],pred[:,None]],1)
            row=dict(step=iteration,training_loss=float(loss),val_1LT=mse,seconds=time.time()-begin)
            log.append(row);print(row,flush=True)
            if mse<best:
                best=mse
                torch.save(dict(state_dict=model.state_dict(),step=iteration,val=mse,sigma=sigma),out/'checkpoint.pt')
            write_json(out/'training.json',dict(log=log,steps_done=iteration,params=sum(p.numel() for p in model.parameters()),
                       best_val=best,seconds=time.time()-begin,git_sha=sha(),threads=16))
            model.train()

if __name__=='__main__':
    main()
