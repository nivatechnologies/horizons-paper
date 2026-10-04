"""Frozen training/validation and independent attractor/test blocks."""
import argparse
import gc
import json
import time

import numpy as np
import torch

from common import CENTRE, RANGE, RESULTS, RUNS, World, queries, rng, write_json
from ap.solver import obs_noise


def learned_data(name):
    out = RUNS/"cache"
    out.mkdir(parents=True, exist_ok=True)
    n, nf, base = (1024,200,0) if name=="training" else (128,100,0)
    manifest = RESULTS/f"data_{name}.json"
    if manifest.exists():
        print("already complete",name,flush=True)
        return
    params = CENTRE+RANGE*rng(name,base).uniform(-1,1,(n,3))
    # Different substreams for parameter draws and ICs.
    prototype = World([CENTRE])
    initial = prototype.random_ic(rng(name,base+1),n)
    X = np.lib.format.open_memmap(out/f"{name}.npy",mode="w+",dtype=np.float32,shape=(n,nf,64,64))
    t = time.monotonic()
    for i in range(0,n,128):
        m = World(params[i:i+128])
        wh = m.flow(initial[i:i+128],50000)
        for k in range(nf):
            wh = m.flow(wh,35)
            X[i:i+len(wh),k] = m.to_phys(wh).cpu().numpy()
        X.flush()
        print(name, i+len(wh), "seconds",round(time.monotonic()-t,1),flush=True)
        del m,wh
        gc.collect();torch.cuda.empty_cache()
    np.save(out/f"{name}_theta.npy",params)
    write_json(manifest,dict(name=name,n=n,n_frames=nf,params_file=f"{name}_theta.npy",
               conditions="uniform-independent-3-parameter-box",burn=500,dt=.01,delta=.35,
               seconds=time.monotonic()-t))


def point_data(point):
    point_id = point["id"]
    path = RESULTS/"panels"/f"{point_id}.json"
    cache = RUNS/"cache"
    cache.mkdir(parents=True,exist_ok=True)
    if path.exists():
        return json.loads(path.read_text())
    if not point["chaos"]["chaotic"]:
        return None
    index = point["index"]
    theta = np.asarray(point["theta"])
    h = .5/point["chaos"]["lam"]
    t = time.monotonic()
    m = World(np.broadcast_to(theta,(100,3)).copy())
    wh = m.random_ic(rng("attractor",index),100)
    wh = m.flow(wh,50000)
    wh = m.advance(wh,h)
    qs,fields = [],[]
    for k in range(10):
        if k:
            wh = m.flow(wh,140)
        qs.append(queries(m,wh).cpu().numpy())
        fields.append(m.to_phys(wh).cpu().numpy())
    Q = np.concatenate(qs)
    F = np.concatenate(fields)
    sigma_A = float(np.sqrt(((F-F.mean(0))**2).sum((-2,-1)).mean()))
    means, sigmas = Q.mean(0), Q.std(0,ddof=1)
    available = np.isfinite(sigmas) & (sigmas>0) & ~(sigmas<1e-12*np.abs(means))
    np.save(cache/f"{point_id}_attractor_queries.npy",Q)
    del F,fields,Q,qs
    wh = m.random_ic(rng("test",index),100)
    wh = m.flow(wh,50000)
    wh = m.flow(wh,19650)
    frames = []
    for k in range(11):
        if k:
            wh = m.flow(wh,35)
        frames.append(m.to_phys(wh).cpu().numpy())
    clean = np.stack(frames,axis=1)
    observations = clean+obs_noise(rng("noise",index),clean.shape,sigma_A)
    end = m.advance(wh,h)
    truth_q = queries(m,end).cpu().numpy()
    np.savez(cache/f"{point_id}_panel.npz",observations=observations,truth_q=truth_q,
             theta=theta,query_sigma=sigmas,query_mean=means,query_available=available,
             h=h,sigma_A=sigma_A)
    summary = dict(id=point_id,index=index,theta=theta.tolist(),h=h,
                  query_mean=means.tolist(),query_sigma=sigmas.tolist(),
                  query_available=available.tolist(),sigma_A=sigma_A,n_states=100,n_attractor=1000,
                  burn=500,post_burn_endpoint=200,seconds=time.monotonic()-t)
    write_json(path,summary)
    print("panel complete",point_id,summary,flush=True)
    del m,wh,end
    gc.collect();torch.cuda.empty_cache()
    return summary


def main():
    points = json.loads((RESULTS/"points.json").read_text())
    panels = []
    for p in points["points"]:
        panel = point_data(p)
        if panel is not None:
            panels.append(panel)
    sufficient = []
    by_id = {p["id"]:p for p in panels}
    for qi,good in enumerate(points["evaluable_by_chaos"]):
        sufficient.append(bool(good and all(by_id[f"q{qi}_{a}"]["query_available"][qi] for a in ["0","90"])))
    write_json(RESULTS/"panel_feasibility.json",dict(evaluable=sufficient,n_evaluable=sum(sufficient)))
    if sum(sufficient)<3:
        print("INSUFFICIENT PANEL: otherwise; do not train",flush=True)
        return
    learned_data("training")
    learned_data("validation")


if __name__=="__main__":
    torch.set_num_threads(4)
    parser=argparse.ArgumentParser()
    parser.add_argument("phase",choices=["all","training","validation"])
    args=parser.parse_args()
    if args.phase=="all":main()
    else:learned_data(args.phase)
