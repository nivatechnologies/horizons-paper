"""Inherited FNO learned recipes with exactly the frozen histories/channels/data."""
import argparse
import json
import math
import time

import numpy as np
import torch

from common import CENTRE,RANGE,ROOT,RESULTS,RUNS,SEEDS,rng,write_json
from ap.fno import FNO2d


class ParamFNO(FNO2d):
    def __init__(self,n_in=4):
        super().__init__(n_in=n_in,re_channel=False)
        self.lift=torch.nn.Conv2d(n_in+4+3,64,1)

    def forward(self,frames,theta):
        coords=self.coords.expand(len(frames),-1,-1,-1)
        channels=theta.float()[:,:,None,None].expand(-1,-1,64,64)
        h=self.lift(torch.cat([frames,coords,channels],1))
        for k,(s,p) in enumerate(zip(self.spec,self.pw)):
            h=s(h)+p(h)
            if k<len(self.spec)-1:h=torch.nn.functional.gelu(h)
        return frames[:,-1]+self.proj2(torch.nn.functional.gelu(self.proj1(h)))[:,0]


def build(arm):
    return FNO2d(8) if arm=="L_range-3" else ParamFNO(4)


def loss_fn(model,x,y,theta):
    losses=[]
    for k in range(4):
        p=model(x,theta)
        losses.append(((p-y[:,k])**2).mean())
        x=torch.cat([x[:,1:],p[:,None]],1)
    return losses[0]+sum(losses)/4


def batch(X,T,it,k,n_in,noise,scale):
    f=np.stack([np.asarray(X[i,j:j+n_in+4]) for i,j in zip(it,k)]).astype(np.float32)*scale
    return (torch.from_numpy(f[:,:n_in]+noise).to("cuda"),
            torch.from_numpy(f[:,n_in:]).to("cuda"),
            torch.as_tensor((T[it]-CENTRE)/RANGE,device="cuda",dtype=torch.float32))


def main(arm,steps=30000,qa=False):
    if not qa and steps!=30000:raise ValueError("Frozen budget is 30000")
    torch.manual_seed(SEEDS["optimizer"])
    model=build(arm).to("cuda")
    n_in=model.n_in
    if qa:
        x=torch.randn(32,n_in,64,64,device="cuda")
        y=torch.randn(32,4,64,64,device="cuda")
        theta=torch.randn(32,3,device="cuda")
        opt=torch.optim.AdamW(model.parameters(),lr=1e-3,weight_decay=1e-4)
        torch.cuda.synchronize();t=time.monotonic()
        for i in range(5):
            loss=loss_fn(model,x,y,theta);opt.zero_grad(set_to_none=True)
            loss.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),1.0);opt.step()
        torch.cuda.synchronize()
        print(json.dumps(dict(arm=arm,params=model.n_params(),n_in=n_in,seconds_per_step=(time.monotonic()-t)/5)),flush=True)
        return
    out=RUNS/"train"/arm
    if (out/"info.json").exists():
        print("already trained",arm,flush=True);return
    out.mkdir(parents=True,exist_ok=True)
    cache=RUNS/"cache"
    X=np.load(cache/"training.npy",mmap_mode="r");T=np.load(cache/"training_theta.npy")
    V=np.load(cache/"validation.npy",mmap_mode="r");TV=np.load(cache/"validation_theta.npy")
    sigma=json.loads((RESULTS/"panels/centre.json").read_text())["sigma_A"]
    scale=64/sigma
    tr=rng("training",100);nr=rng("noise",10000)
    vr=rng("validation",100);vnr=rng("noise",20000)
    vi=vr.integers(0,len(V),512);vk=vr.integers(0,V.shape[1]-n_in-4+1,512)
    vn=(vnr.standard_normal((512,n_in,64,64))*.02).astype(np.float32)
    opt=torch.optim.AdamW(model.parameters(),lr=1e-3,weight_decay=1e-4)
    sched=torch.optim.lr_scheduler.LambdaLR(opt,lambda s:.5*(1+math.cos(math.pi*min(s,steps)/steps)))
    start_step=0;best=float("inf");best_step=None;curve=[];elapsed=0.
    resume=out/"resume.pt"
    if resume.exists():
        ck=torch.load(resume,map_location="cuda",weights_only=False)
        model.load_state_dict(ck["model"]);opt.load_state_dict(ck["opt"]);sched.load_state_dict(ck["sched"])
        tr.bit_generator.state=ck["tr_rng"];nr.bit_generator.state=ck["noise_rng"]
        start_step=ck["step"];best=ck["best"];best_step=ck["best_step"];curve=ck["curve"];elapsed=ck["elapsed"]
    t=time.monotonic();running=0.
    for step in range(start_step+1,steps+1):
        it=tr.integers(0,len(X),32);k=tr.integers(0,X.shape[1]-n_in-4+1,32)
        noise=(nr.standard_normal((32,n_in,64,64))*.02).astype(np.float32)
        x,y,theta=batch(X,T,it,k,n_in,noise,scale)
        loss=loss_fn(model,x,y,theta)
        if not torch.isfinite(loss):raise RuntimeError(f"nonfinite training loss at {step}")
        opt.zero_grad(set_to_none=True);loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(),1.0);opt.step();sched.step()
        running+=float(loss.detach())
        if step%100==0:print(arm,"step",step,"seconds",round(elapsed+time.monotonic()-t,1),flush=True)
        if step%1000==0:
            model.eval();vl=0.
            with torch.no_grad():
                for i in range(0,512,64):
                    x,y,theta=batch(V,TV,vi[i:i+64],vk[i:i+64],n_in,vn[i:i+64],scale)
                    vl+=float(loss_fn(model,x,y,theta))*len(x)
            model.train();vl/=512
            curve.append(dict(step=step,train_loss=running/1000,val_loss=vl,seconds=elapsed+time.monotonic()-t))
            running=0.
            if vl<best:
                best,best_step=vl,step;torch.save(model.state_dict(),out/"best.pt")
            ck=dict(model=model.state_dict(),opt=opt.state_dict(),sched=sched.state_dict(),
                    tr_rng=tr.bit_generator.state,noise_rng=nr.bit_generator.state,step=step,
                    best=best,best_step=best_step,curve=curve,elapsed=elapsed+time.monotonic()-t)
            torch.save(ck,out/"resume.tmp");(out/"resume.tmp").replace(resume)
            write_json(out/"progress.json",dict(arm=arm,**curve[-1],best_step=best_step,best_val=best))
    write_json(out/"info.json",dict(arm=arm,n_in=n_in,param_channels=0 if arm=="L_range-3" else 3,
               params=model.n_params(),steps=steps,batch=32,unroll=4,best_val=best,best_step=best_step,
               train_seconds=elapsed+time.monotonic()-t,curve=curve))
    print("TRAIN COMPLETE",arm,flush=True)


if __name__=="__main__":
    torch.set_num_threads(4)
    p=argparse.ArgumentParser();p.add_argument("arm",choices=["L_range-3","FNO-theta"])
    p.add_argument("--qa",action="store_true");a=p.parse_args()
    main(a.arm,qa=a.qa)
