"""Generate solver labels on sulaco CPU, from panel-disjoint retained train."""
import argparse,json,time
import numba,numpy as np
from protocol import *
from physics import simulate
from campaign import artifact,dt
def main(workers):
    numba.set_num_threads(workers)
    base=np.load(ROOT/"inputs/base_train.npz")["state"]
    directory=ROOT/"runs/training_data";directory.mkdir(parents=True,exist_ok=True)
    # Independent pairs, uniform trajectory and eligible history start.
    for kind,n,ns in [("pairs",4096,"afd-train-pairs"),("cost",16384,"afd-train-cost")]:
        path=directory/(kind+".npz")
        if path.exists():continue
        start=time.perf_counter();R=rng(ns,6)
        b=R.integers(len(base),size=n);t=R.integers(10,base.shape[1],size=n)
        hist=np.stack([base[i,j-10:j+1] for i,j in zip(b,t)]).astype(np.float64)
        obs=hist+.02*SIGMA*rng(ns,1).standard_normal(hist.shape)
        if kind=="pairs":
            pairs=np.array([(j,k) for j in range(8) for k in range(j+1,8)])
            pair=pairs[rng(ns,4).integers(28,size=n)]
            amp=rng(ns,4,member=1).uniform(-.04,.04,size=n)
            action=8*amp[:,None,None]*patterns()[pair]
            targets=np.empty((n,2,36,40),dtype=np.float32)
            for first in range(0,n,128):
                last=min(n,first+128)
                s=simulate(np.repeat(hist[first:last,-1],2,axis=0),
                           (8+action[first:last]).reshape(-1,40),dt(),37)
                targets[first:last]=s[:,1:].reshape(last-first,2,36,40)
            np.savez(path,window=obs.astype(np.float32),action=action.astype(np.float32),
                     targets=targets,trajectory=b,time_index=t)
        else:
            member=obs+.02*SIGMA*rng(ns,2).standard_normal(hist.shape)
            action=.16*patterns()
            labels=np.empty((n,8),dtype=np.float64)
            for first in range(0,n,128):
                last=min(n,first+128);m=last-first
                s=simulate(np.repeat(member[first:last,-1],8,axis=0),np.tile(8+action,(m,1)),dt(),36)
                energy=.5*np.mean(s*s,axis=-1)
                labels[first:last]=energy[:,WINDOWS[PRIMARY]].mean(-1).reshape(m,8)
            centered=labels-labels.mean(1)[:,None]
            variance_diff=float(np.mean(centered**2));variance_mean=float(labels.mean(1).var(ddof=0))
            if not variance_diff>0 or not variance_mean>0:raise RuntimeError("zero training variance")
            np.savez(path,window=member.astype(np.float32),action=action.astype(np.float32),
                     labels=labels,variance_diff=variance_diff,variance_mean=variance_mean,
                     trajectory=b,time_index=t)
        artifact(path,"training data before any model evaluation")
        write_json(directory/(kind+".json"),dict(starts=n,seconds=time.perf_counter()-start,
                   dt=dt(),sha256=digest(path),namespace=ns))
        print(kind,"complete",flush=True)
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--workers",type=int,default=96);main(p.parse_args().workers)

