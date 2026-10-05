"""Frozen Baccus training worker. Mount namespace exposes no test outputs."""
import argparse,time,json,os,math
from pathlib import Path
import numpy as np,torch
from models import Emulator,CostModel,cuda_rules
from protocol import RECIPE,LT,SIGMA,rng,WINDOWS,PRIMARY,write_json,digest
def main(name,data,out,micro):
    cuda_rules();torch.manual_seed(0);out.mkdir(parents=True,exist_ok=True)
    recipe=RECIPE[name];kind=recipe["kind"];updates=recipe["updates"];cap=recipe["cap_hours"]*3600
    two=name.startswith("CNN2-")
    sigma=float(np.load(data/"base_train.npz")["sigma"]) if two else SIGMA
    checkpoint=data/("CNN2-20k.pt" if two else "CNN-20k.pt")
    base_gpu_seconds=0.
    if two and kind=="r2":
        base_gpu_seconds=float(json.loads((data/"CNN2-20k.training.json").read_text())["charged_gpu_seconds"])
        cap-=base_gpu_seconds
        if not np.isfinite(cap) or cap<=0: raise RuntimeError("base consumed CNN2-R2 cap")
    model=CostModel() if kind=="cost" else Emulator()
    if kind in ["roll","resp","r2"]:
        ck=torch.load(checkpoint,map_location="cpu",weights_only=True)
        model.load_state_dict(ck["state_dict"]);sigma=ck["sigma"]
    if "s2" in name or "s3" in name:
        ns="afd-cnn-seed2" if "s2" in name else "afd-cnn-seed3"
        seed=int(rng(ns,6).integers(2**31));torch.manual_seed(seed);model=Emulator()
        R=rng(ns,6,member=1)
    else:
        R=rng("afd2-train" if two and kind=="base" else "afd2-train-pairs" if two else "afd-train-recipe",6)
    torch.cuda.synchronize();begin=time.monotonic()
    model.to("cuda");opt=torch.optim.AdamW(model.parameters(),lr=1e-3 if kind in ["base","cost"] else 1e-4,weight_decay=1e-4)
    initial_lr=opt.param_groups[0]["lr"]
    if kind=="base":
        train=np.load(data/"base_train.npz");val=np.load(data/"base_val.npz")
        X=train["state"]/sigma;A=train["action"]/sigma
        V=val["state"]/sigma;VA=val["action"]/sigma
        # Base training stream is inherited unchanged for 5k/80k.
        if name in ["CNN-5k","CNN-80k"]:R=np.random.default_rng(np.random.SeedSequence([400000,0,6,0,0,0]))
        RV=rng("afd2-train-val",6) if two else np.random.default_rng(np.random.SeedSequence([500000,0,6,0,0,0]))
        vctx=torch.tensor(V[:,:11]+.02*RV.standard_normal((64,11,40)),dtype=torch.float32,device="cuda")
        va=torch.tensor(VA,dtype=torch.float32,device="cuda")
        vtarget=torch.tensor(V[:,11:11+round(LT/.05)],dtype=torch.float32,device="cuda")
    elif kind=="cost":
        train=np.load(data/"cost.npz")
        X=train["window"]/sigma;A=train["action"]/sigma
        target=train["labels"];vd=float(train["variance_diff"]);vm=float(train["variance_mean"])
        if not (np.isfinite(vd) and np.isfinite(vm) and vd>0 and vm>0):
            raise RuntimeError("invalid cost normalization")
    else:
        train=np.load(data/"pairs.npz")
        X=train["window"]/sigma;A=train["action"]/sigma;target=train["targets"]/sigma
    def pair_loss(indices,grad=False):
        ctx=torch.tensor(np.repeat(X[indices],2,axis=0),dtype=torch.float32,device="cuda")
        act=torch.tensor(A[indices].reshape(-1,40),dtype=torch.float32,device="cuda")
        tar=torch.tensor(target[indices].reshape(-1,36,40),dtype=torch.float32,device="cuda")
        roll=ctx.sum()*0;diff=ctx.sum()*0
        for t in range(36):
            pred=model(ctx,act)
            if kind in ["roll","resp"] or t+1 in WINDOWS[PRIMARY]:
                error=((pred-tar[:,t])**2).mean()
                roll=roll+error/(36 if kind in ["roll","resp"] else len(WINDOWS[PRIMARY]))
                if kind in ["roll","resp"]:
                    delta=(pred.reshape(-1,2,40)[:,0]-pred.reshape(-1,2,40)[:,1])-(tar[:,t].reshape(-1,2,40)[:,0]-tar[:,t].reshape(-1,2,40)[:,1])
                    diff=diff+(delta**2).mean()/36
            ctx=torch.cat([ctx[:,1:],pred[:,None]],1)
        return roll,diff
    torch.cuda.synchronize();normal_roll=normal_diff=None
    if kind in ["roll","resp"]:
        Rnorm=rng("afd2-train-pairs" if two else "afd-train-recipe",6);losses=[]
        model.eval()
        with torch.no_grad():
            for _ in range(64):
                ids=Rnorm.integers(len(X),size=128);r=d=0.
                for first in range(0,128,micro):
                    ix=ids[first:first+micro];a,b=pair_loss(ix)
                    r+=a.item()*len(ix)/128;d+=b.item()*len(ix)/128
                losses.append([r,d])
        normal_roll,normal_diff=np.mean(losses,axis=0)
        if not normal_roll>0 or not normal_diff>0:raise RuntimeError("invalid paired normalization")
        write_json(out/"normalization.json",dict(roll=float(normal_roll),difference=float(normal_diff),
                   batches=64,paired_data_sha256=digest(data/"pairs.npz")))
        model.train()
    best=float("inf");recent=[];log=[];selection_seconds=0.;completed_updates=0;selection_reserve=0.
    if kind=="r2":
        path=out/"checkpoint_000000.pt"
        torch.save(dict(state_dict=model.state_dict(),step=0,sigma=sigma,kind=kind),path)
        write_json(out/"checkpoint_000000.json",dict(step=0,sha256=digest(path),charged_gpu_seconds=0.,status="AWAITING_VALIDATION"))
    for iteration in range(1,updates+1):
        torch.cuda.synchronize();elapsed=time.monotonic()-begin+selection_seconds
        if elapsed+(max(recent) if recent else 0)+selection_reserve>=cap:
            if kind in ["base","roll","resp"]:raise RuntimeError(f"cap prevents prescribed updates: {iteration-1}/{updates}")
            break
        before=time.monotonic();opt.zero_grad()
        ids=R.integers(len(X),size=128)
        if kind=="base":
            times=R.integers(X.shape[1]-14,size=128)
            frames=np.stack([X[i,j:j+15] for i,j in zip(ids,times)])
            contexts=frames[:,:11]+.02*R.standard_normal((128,11,40))
        total=0.
        for first in range(0,128,micro):
            ix=ids[first:first+micro];weight=len(ix)/128
            if kind=="base":
                ctx=torch.tensor(contexts[first:first+micro],dtype=torch.float32,device="cuda")
                act=torch.tensor(A[ix],dtype=torch.float32,device="cuda")
                tar=torch.tensor(frames[first:first+micro,11:],dtype=torch.float32,device="cuda")
                loss=ctx.sum()*0
                for t in range(4):
                    pred=model(ctx,act);err=((pred-tar[:,t])**2).mean()
                    loss=loss+err/4+(err if t==0 else 0)
                    ctx=torch.cat([ctx[:,1:],pred[:,None]],1)
            elif kind=="cost":
                ctx=torch.tensor(np.repeat(X[ix],8,axis=0),dtype=torch.float32,device="cuda")
                act=torch.tensor(np.tile(A,(len(ix),1)),dtype=torch.float32,device="cuda")
                prediction=model(ctx,act).reshape(-1,8)
                tar=torch.tensor(target[ix],dtype=torch.float32,device="cuda")
                pmean=prediction.mean(1);tmean=tar.mean(1)
                loss=((prediction-pmean[:,None]-tar+tmean[:,None])**2).mean()/vd+((pmean-tmean)**2).mean()/vm
            else:
                roll,diff=pair_loss(ix)
                loss=roll if kind=="r2" else roll/normal_roll+(diff/normal_diff if kind=="resp" else 0)
            if not torch.isfinite(loss):raise RuntimeError("nonfinite loss")
            (loss*weight).backward();total+=loss.item()*weight
        torch.nn.utils.clip_grad_norm_(model.parameters(),1.)
        fraction=(iteration-1)/updates if kind in ["base","roll","resp"] else elapsed/cap
        opt.param_groups[0]["lr"]=initial_lr*.5*(1+math.cos(math.pi*min(1,fraction)))
        opt.step();torch.cuda.synchronize()
        completed_updates=iteration
        recent.append(time.monotonic()-before);recent=recent[-32:]
        if iteration%100==0:
            row=dict(step=iteration,loss=total,charged_gpu_seconds=time.monotonic()-begin+selection_seconds,
                     recent_update_seconds=float(np.median(recent)),
                     projected_full_recipe_seconds=float(np.median(recent)*updates) if updates<100000000 else None)
            log.append(row);write_json(out/"progress.json",dict(name=name,log=log,cap_seconds=cap))
            print(row,flush=True)
        if kind=="base" and iteration%1000==0:
            model.eval()
            with torch.no_grad():
                ctx=vctx.clone();mse=0.
                for t in range(len(vtarget[0])):
                    pred=model(ctx,va);mse+=((pred-vtarget[:,t])**2).mean().item()/len(vtarget[0])
                    ctx=torch.cat([ctx[:,1:],pred[:,None]],1)
            if mse<best:
                best=mse
                torch.save(dict(state_dict=model.state_dict(),step=iteration,sigma=sigma,val=mse),out/"selected.pt")
            model.train()
        if kind in ["r2","cost"] and iteration%2000==0:
            path=out/f"checkpoint_{iteration:06d}.pt"
            torch.save(dict(state_dict=model.state_dict(),step=iteration,sigma=sigma,kind=kind),path)
            write_json(out/f"checkpoint_{iteration:06d}.json",dict(step=iteration,sha256=digest(path),
                       charged_gpu_seconds=time.monotonic()-begin+selection_seconds,status="AWAITING_VALIDATION"))
            # Charge/follow actual selection costs before next block, keeping total under cap.
            ack=out/f"validation_{iteration:06d}.json"
            while not ack.exists():
                if time.monotonic()-begin+selection_seconds>=cap:break
                time.sleep(5)
            if ack.exists():
                selected_charge=float(json.loads(ack.read_text())["charged_gpu_seconds"])
                selection_seconds+=selected_charge
                selection_reserve=max(selection_reserve,2*selected_charge+5.)
            if time.monotonic()-begin+selection_seconds>=cap:break
    else:
        iteration=updates
    if kind in ["roll","resp"]:
        torch.save(dict(state_dict=model.state_dict(),step=updates,sigma=sigma),out/"selected.pt")
    write_json(out/"training_complete.json",dict(name=name,kind=kind,last_step=completed_updates,
               prescribed_updates=updates,charged_gpu_seconds=time.monotonic()-begin+selection_seconds,
               selection_gpu_seconds=selection_seconds,
               base_gpu_seconds_in_individual_cap=base_gpu_seconds,
               gpu_name=torch.cuda.get_device_name(0),microbatch=micro,cap_seconds=cap,log=log,
               selected_hash=digest(out/"selected.pt") if (out/"selected.pt").exists() else None,
               isolation="bubblewrap: no /mnt, /home, test outputs or result reports"))
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--name",required=True);p.add_argument("--data",type=Path,required=True);p.add_argument("--out",type=Path,required=True);p.add_argument("--microbatch",type=int,default=64);a=p.parse_args();main(a.name,a.data,a.out,a.microbatch)
