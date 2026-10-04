"""Frozen L_range-style FNO extended to whole observation window and action field."""
import argparse
import json
import sys
import time
import numpy as np
import torch
from torch import nn
from common import ROOT,rng,sha,write_json
sys.path.insert(0,str(ROOT.parents[1]/'adapt_physics'))
from ap.fno import FNO2d

class ActionFNO(FNO2d):
    def __init__(self):
        super().__init__(11,modes=16,width=64,layers=4)
        self.lift=nn.Conv2d(16,64,1)
    def forward(self,frames,action):
        h=self.lift(torch.cat([frames,self.coords.expand(len(frames),-1,-1,-1),action[:,None]],1))
        for i,(s,p) in enumerate(zip(self.spec,self.pw)):
            h=s(h)+p(h)
            if i<3:h=torch.nn.functional.gelu(h)
        return frames[:,-1]+self.proj2(torch.nn.functional.gelu(self.proj1(h)))[:,0]

def main(device,microbatch):
    torch.set_num_threads(1);torch.manual_seed(0)
    out=ROOT/'runs/kolmo/learned'
    if (out/'checkpoint.pt').exists():raise FileExistsError('checkpoint exists')
    sysinfo=json.loads((ROOT/'runs/kolmo/system.json').read_text())
    physical_sigma=sysinfo['sigma'];lam=sysinfo['lambda_mean']
    inherited=json.loads((ROOT.parents[1]/'adapt_physics/results/chaos_gate.json').read_text())
    sigma=inherited['Re40']['sigma_A']/64
    noise_scale=.02*physical_sigma/sigma
    X=np.load(out/'train.npy',mmap_mode='r');A=np.load(out/'train_actions.npy')
    V=np.load(out/'val.npy',mmap_mode='r');VA=np.load(out/'val_actions.npy')
    R=rng('train',1,6);RV=rng('val',1,6)
    model=ActionFNO().to(device)
    opt=torch.optim.AdamW(model.parameters(),lr=1e-3,weight_decay=1e-4)
    schedule=torch.optim.lr_scheduler.CosineAnnealingLR(opt,30000)
    stepsLT=max(1,int(round(1/lam/.35)))
    valnoise=noise_scale*RV.standard_normal((64,11,64,64)).astype(np.float32)
    best=float('inf');begin=time.time();log=[]
    for iteration in range(1,30001):
        idx=R.integers(len(X),size=32);times=R.integers(X.shape[1]-14,size=32)
        f=np.stack([np.asarray(X[i,t:t+15]) for i,t in zip(idx,times)])/sigma
        noise=noise_scale*R.standard_normal((32,11,64,64)).astype(np.float32)
        opt.zero_grad(set_to_none=True);loss_value=0.
        for start in range(0,32,microbatch):
            end=min(32,start+microbatch);weight=(end-start)/32
            ctx=torch.tensor(f[start:end,:11]+noise[start:end],device=device,dtype=torch.float32)
            target=torch.tensor(f[start:end,11:],device=device,dtype=torch.float32)
            a=torch.tensor(A[idx[start:end]]/sigma,device=device,dtype=torch.float32)
            loss=0.
            for j in range(4):
                pred=model(ctx,a);err=((pred-target[:,j])**2).mean()
                loss=loss+err/4+(err if j==0 else 0)
                ctx=torch.cat([ctx[:,1:],pred[:,None]],1)
            if not torch.isfinite(loss):raise RuntimeError(f'nonfinite loss {iteration}')
            (loss*weight).backward();loss_value+=float(loss.detach())*weight
        torch.nn.utils.clip_grad_norm_(model.parameters(),1.);opt.step();schedule.step()
        if iteration%1000==0:
            model.eval();mse=0.
            with torch.no_grad():
                for start in range(0,64,microbatch):
                    end=min(64,start+microbatch)
                    ctx=torch.tensor(np.asarray(V[start:end,:11])/sigma+valnoise[start:end],device=device,dtype=torch.float32)
                    action=torch.tensor(VA[start:end]/sigma,device=device,dtype=torch.float32)
                    target=torch.tensor(np.asarray(V[start:end,11:11+stepsLT])/sigma,device=device,dtype=torch.float32)
                    for j in range(stepsLT):
                        pred=model(ctx,action)
                        mse+=((pred-target[:,j])**2).mean().item()*(end-start)/64/stepsLT
                        ctx=torch.cat([ctx[:,1:],pred[:,None]],1)
            log.append(dict(step=iteration,training_loss=loss_value,val_1LT=mse,seconds=time.time()-begin))
            print(log[-1],flush=True)
            if mse<best:
                best=mse
                torch.save(dict(state_dict=model.state_dict(),step=iteration,val=mse,sigma=sigma),out/'checkpoint.pt')
            write_json(out/'training.json',dict(log=log,steps_done=iteration,params=model.n_params(),best_val=best,
                       seconds=time.time()-begin,device=device,microbatch=microbatch,git_sha=sha(),
                       feature_sigma=sigma,physical_sigma=physical_sigma,normalized_noise=noise_scale))
            model.train()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--device',default='cuda:0');p.add_argument('--microbatch',type=int,default=8)
    a=p.parse_args();main(a.device,a.microbatch)
