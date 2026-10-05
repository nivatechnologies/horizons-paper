"""Stage-1 CPU truth/physics and sulaco CUDA inference, resumable per case."""
import argparse,datetime,json,time,platform
from pathlib import Path
import numba,numpy as np
from protocol import *
from physics import history,simulate,costs,identify

def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def artifact(path,kind):
    item=dict(path=str(Path(path).relative_to(ROOT)),kind=kind,sha256=digest(path),recorded_at=now())
    log=ROOT/"runs/artifact_log.jsonl";log.parent.mkdir(parents=True,exist_ok=True)
    with log.open("a") as f:f.write(json.dumps(item)+"\n")
    with (ROOT/"AFD_ARTIFACTS.md").open("a") as f:f.write("\n- "+json.dumps(item)+"\n")
def dt():
    x=json.loads((ROOT/"runs/numerics/dtcheck.json").read_text())
    if x["status"]!="PASS":raise RuntimeError("timestep not passed")
    return x["chosen_dt"]
def input_case(panel,c):
    directory=ROOT/"runs"/panel;directory.mkdir(parents=True,exist_ok=True)
    path=directory/f"input_{c:03d}.npz"
    if not path.exists():
        true,y=history("afd-observation-"+panel,c,dt())
        np.savez(path,true=true,observed=y)
        artifact(path,"case input before truth/arm evaluation")
        write_json(directory/f"input_{c:03d}.json",dict(created_at=now(),panel=panel,case=c))
    return np.load(path)
def case_cpu(panel,c):
    directory=ROOT/"runs"/panel
    target=directory/f"cpu_{c:03d}.npz"
    if target.exists():return
    record=input_case(panel,c);y=record["observed"];true=record["true"]
    tick=time.perf_counter();fhat=identify(y,dt());identify_seconds=time.perf_counter()-tick
    member_truth=y+.02*SIGMA*rng("afd-"+panel+"-truth",2,c).standard_normal((2048,11,40))
    member_arm=y+.02*SIGMA*rng("afd-"+panel+"-arm",2,c).standard_normal((64,11,40))
    p=np.vstack([patterns(),np.zeros(40)])
    result=dict(Fhat=np.array(fhat),arm_windows=member_arm)
    start=time.perf_counter()
    ini=np.tile(member_truth[:,-1],(9,1));f=np.repeat(8+.16*p,2048,axis=0)
    states=simulate(ini,f,dt()).reshape(9,2048,len(TICKS),40)
    assert np.isfinite(states).all()
    result["truth_cost"]=costs(states);result["truth_mean"]=states.mean(1)
    result["truth_var"]=np.sum(states.var(1,ddof=0),axis=-1)
    # Work integrated over [0,T+W] at solver dt, not sparsely estimated from output states.
    del states
    truth_seconds=time.perf_counter()-start
    actual=simulate(np.tile(true[-1],(9,1)),8+.16*p,dt())
    result["actual"]=actual;result["actual_cost"]=costs(actual)
    times={}
    for name,forcing in [("N-last",fhat),("N-oracle",8.)]:
        start=time.perf_counter()
        s=simulate(np.tile(member_arm[:,-1],(8,1)),np.repeat(forcing+.16*patterns(),64,axis=0),dt()).reshape(8,64,len(TICKS),40)
        result[name+"_cost"]=costs(s);result[name+"_mean"]=s.mean(1)
        result[name+"_var"]=s.var(1,ddof=0).sum(-1)
        assert np.isfinite(s).all()
        times[name]=time.perf_counter()-start
    np.savez(target,**result)
    write_json(directory/f"cpu_{c:03d}.json",dict(case=c,completed_at=now(),host=platform.node(),
               dt=dt(),identify_seconds=identify_seconds,truth_seconds=truth_seconds,
               arm_shared_all_leads_seconds=times,source_hashes={n:digest(ROOT/n) for n in ["campaign.py","physics.py","protocol.py"]}))
    artifact(target,"truth/physics output")
    print(panel,"CPU",c+1,flush=True)
def inference(panel,name,checkpoint,micro):
    import torch
    from models import Emulator,cuda_rules
    cuda_rules()
    ckpt=torch.load(checkpoint,map_location="cpu",weights_only=True)
    model=Emulator();model.load_state_dict(ckpt["state_dict"]);model.to("cuda");model.eval()
    artifact(checkpoint,"checkpoint before "+panel+" evaluation")
    sigma=ckpt["sigma"];a=.16*patterns()/sigma
    count=100 if panel=="val" else 200
    for c in range(count):
        directory=ROOT/"runs"/panel;path=directory/f"{name}_{c:03d}.npz"
        if path.exists():continue
        cpu=directory/f"cpu_{c:03d}.npz"
        while not cpu.exists():time.sleep(2)
        with np.load(cpu) as data:win=data["arm_windows"]
        start=time.perf_counter();allstate=np.empty((8*64,len(TICKS),40));valid=np.ones((8*64,len(TICKS)),bool)
        with torch.no_grad():
            for first in range(0,512,micro):
                ids=np.arange(first,min(512,first+micro))
                context=torch.tensor(win[ids%64]/sigma,dtype=torch.float32,device="cuda")
                action=torch.tensor(a[ids//64],dtype=torch.float32,device="cuda")
                alive=np.ones(len(ids),bool)
                for t in range(len(TICKS)):
                    state=context[:,-1].cpu().numpy().astype(np.float64)*sigma
                    alive&=np.isfinite(state).all(-1)&(np.sqrt(np.mean(state*state,axis=-1))<=10*SIGMA)
                    allstate[ids,t]=state;valid[ids,t]=alive
                    if t<len(TICKS)-1:
                        context[torch.tensor(~alive,device="cuda")]=0.
                        pred=model(context,action)
                        context=torch.cat([context[:,1:],pred[:,None]],1)
        s=allstate.reshape(8,64,len(TICKS),40);v=valid.reshape(8,64,len(TICKS)).all(0)
        # Paired drop across actions at every scoring window's last output.
        means=[];variances=[];cs=[];survivors=[]
        for w in WINDOWS:
            keep=v[:,w[-1]];survivors.append(keep)
            means.append(s[:,keep].mean(1) if keep.any() else np.zeros((8,len(TICKS),40)))
            variances.append(s[:,keep].var(1,ddof=0).sum(-1) if keep.any() else np.zeros((8,len(TICKS))))
            cs.append(costs(s[:,keep])[...,len(cs)].mean(1) if keep.any() else np.zeros(8))
        torch.cuda.synchronize()
        np.savez(path,mean=np.array(means),var=np.array(variances),cost=np.array(cs),
                 survivors=np.array(survivors))
        write_json(directory/f"{name}_{c:03d}.json",dict(case=c,completed_at=now(),
                  shared_all_leads_seconds=time.perf_counter()-start,device="cuda",microbatch=micro,
                  checkpoint_sha256=digest(checkpoint),tf32=False,deterministic_cudnn=True))
        print(panel,name,c+1,flush=True)
def main():
    p=argparse.ArgumentParser();p.add_argument("task",choices=["cpu","cnn"]);p.add_argument("--panel",default="val",choices=["val","test"]);p.add_argument("--workers",type=int,default=96);p.add_argument("--name",default="CNN-20k");p.add_argument("--checkpoint");p.add_argument("--microbatch",type=int,default=8);a=p.parse_args()
    if a.task=="cpu":
        numba.set_num_threads(a.workers)
        for c in range(100 if a.panel=="val" else 200):case_cpu(a.panel,c)
    else:
        if a.name!="CNN-20k" and a.panel=="test" and not (ROOT/"runs/stage1_reading.json").exists():
            raise RuntimeError("Stage1 reading required before Stage2 test access")
        inference(a.panel,a.name,Path(a.checkpoint) if a.checkpoint else ROOT/"inputs/CNN-20k.pt",a.microbatch)
if __name__=="__main__":main()

