"""Frozen law identification, two nulls and learned field-to-query forecasts."""
import argparse
import gc
import json
import math
import time

import numpy as np
import torch

from common import CENTRE,RESULTS,RUNS,World,queries,write_json
from train import build

BOUNDS=np.array([[20.,70.],[.5,1.5],[.3*.07733,2*.07733]])
GOLD=(math.sqrt(5)-1)/2


def identify(obs,sigma_A):
    """P1x objective, three coordinate sweeps, 30 calls per coordinate per sweep."""
    n=len(obs)
    Y=torch.as_tensor(obs,device="cuda",dtype=torch.float64)
    theta=np.broadcast_to(CENTRE,(n,3)).copy()
    counts=0
    def objective(theta):
        nonlocal counts
        model=World(theta)
        wh=model.to_spec(Y[:,0]);total=torch.zeros(n,device="cuda",dtype=torch.float64)
        for k in range(1,11):
            wh=model.flow(wh,35)
            total+=((model.to_phys(wh)-Y[:,k])**2).sum((-2,-1))
        counts+=1
        result=(total/10/sigma_A**2).cpu().numpy()
        del model,wh
        return result
    for sweep in range(3):
        for j in range(3):
            a=np.full(n,BOUNDS[j,0]);b=np.full(n,BOUNDS[j,1])
            c=b-GOLD*(b-a);d=a+GOLD*(b-a)
            def obj(value):
                candidate=theta.copy();candidate[:,j]=value
                return objective(candidate)
            fc,fd=obj(c),obj(d)
            for _ in range(28):
                left=fc<fd
                b=np.where(left,d,b);a=np.where(left,a,c)
                cnew=np.where(left,b-GOLD*(b-a),d)
                dnew=np.where(left,c,a+GOLD*(b-a))
                fnew=obj(np.where(left,cnew,dnew))
                fc,fd=np.where(left,fnew,fd),np.where(left,fc,fnew)
                c,d=cnew,dnew
            theta[:,j]=.5*(a+b)
            print("identify",sweep+1,j+1,"median",np.median(theta[:,j]),flush=True)
    if counts!=270:raise RuntimeError("law search evaluation count changed")
    return theta,counts


@torch.no_grad()
def learned_forecast(arm,obs,theta,h,scale):
    model=build(arm).to("cuda")
    model.load_state_dict(torch.load(RUNS/"train"/arm/"best.pt",map_location="cuda",weights_only=True))
    model.eval();n_in=model.n_in
    theta_t=torch.as_tensor((theta-CENTRE)/np.array([6.,.1,.015466]),device="cuda",dtype=torch.float32)
    output=[]
    n=int(math.floor(h/.35));frac=(h-n*.35)/.35
    for i in range(0,len(obs),32):
        x=torch.as_tensor(obs[i:i+32,-n_in:]*scale,device="cuda",dtype=torch.float32)
        th=theta_t[i:i+len(x)]
        current=x[:,-1]
        for k in range(1,n+2):
            previous=current
            current=model(x,th)
            x=torch.cat([x[:,1:],current[:,None]],1)
            if k==n+1:
                y=(1-frac)*previous+frac*current
                output.append((y.double()/scale).cpu().numpy())
    return np.concatenate(output)


def evaluate_point(p,arms):
    if not p["chaos"]["chaotic"]:return
    point_id=p["id"]
    panel_path=RUNS/"cache"/f"{point_id}_panel.npz"
    if not panel_path.exists():return
    panel=np.load(panel_path)
    obs=panel["observations"];truth_q=panel["truth_q"]
    theta=np.broadcast_to(panel["theta"],(len(obs),3)).copy()
    h=float(panel["h"]);sigma_A=float(panel["sigma_A"])
    target=World(theta,graphs=False)
    centre_sigma=json.loads((RESULTS/"panels/centre.json").read_text())["sigma_A"]
    for arm in arms:
        out=RESULTS/"eval"/f"{point_id}_{arm}.json"
        if out.exists():continue
        t=time.monotonic();fitted=None;counts=0;identify_seconds=0.
        if arm=="persistence":
            predicted=queries(target,torch.fft.rfft2(torch.as_tensor(obs[:,-1],device="cuda",dtype=torch.float64)),theta).cpu().numpy()
        elif arm in ["centre-law","law"]:
            if arm=="law":
                fit_start=time.monotonic();fitted,counts=identify(obs,sigma_A)
                identify_seconds=time.monotonic()-fit_start
                params=fitted
            else:params=np.broadcast_to(CENTRE,theta.shape).copy()
            model=World(params)
            wh=model.to_spec(torch.as_tensor(obs[:,-1],device="cuda",dtype=torch.float64))
            end=model.advance(wh,h)
            predicted=queries(target,end,theta).cpu().numpy()
            del model,wh,end
        else:
            field=learned_forecast(arm,obs,theta,h,64/centre_sigma)
            predicted=queries(target,torch.fft.rfft2(torch.as_tensor(field,device="cuda",dtype=torch.float64)),theta).cpu().numpy()
        available=panel["query_available"].astype(bool)
        errors=np.full_like(truth_q,np.nan)
        errors[:,available]=np.abs(predicted[:,available]-truth_q[:,available])/panel["query_sigma"][available]
        raw=RUNS/"eval"/f"{point_id}_{arm}.npz"
        raw.parent.mkdir(parents=True,exist_ok=True)
        np.savez(raw,predicted=predicted,truth=truth_q,errors=errors,
                 fitted_theta=np.empty((0,3)) if fitted is None else fitted)
        means=[]
        for qi in range(4):
            means.append(float(errors[:,qi].mean()) if np.isfinite(errors[:,qi]).all() else None)
        write_json(out,dict(id=point_id,arm=arm,n=100,mean_errors=means,
                   wall_seconds=time.monotonic()-t,identify_seconds=identify_seconds,objective_evals=counts,
                   parameter_mean=None if fitted is None else fitted.mean(0).tolist(),
                   parameter_sd=None if fitted is None else fitted.std(0,ddof=1).tolist(),
                   theta=theta[0].tolist(),h=h,raw_file=str(raw.relative_to(RUNS)),
                   finite_prediction=bool(np.isfinite(predicted).all())))
        print("evaluated",point_id,arm,means,round(time.monotonic()-t,1),flush=True)
        gc.collect();torch.cuda.empty_cache()
    del target


if __name__=="__main__":
    torch.set_num_threads(4)
    parser=argparse.ArgumentParser()
    parser.add_argument("phase",choices=["nulls","law","learned","all"])
    args=parser.parse_args()
    sets={"nulls":["persistence","centre-law"],"law":["law"],"learned":["L_range-3","FNO-theta"],
          "all":["persistence","centre-law","law","L_range-3","FNO-theta"]}
    points=json.loads((RESULTS/"points.json").read_text())["points"]
    with torch.no_grad():
        for p in points:evaluate_point(p,sets[args.phase])
