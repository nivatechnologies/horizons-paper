"""Sulaco-only truth ensemble: immutable per-member shards, all horizons."""
import argparse
import concurrent.futures
import json
import multiprocessing
import os
import numpy as np
import torch
from common import ROOT,GRID,rng,write_json,sha
from kolmo import costs

OBS=None
INFO=None
DELTA=None

def initialize():
    global OBS,INFO,DELTA
    torch.set_num_threads(1)
    OBS=np.load(ROOT/'runs/kolmo/test/observations.npz')['observed']
    INFO=json.loads((ROOT/'runs/kolmo/system.json').read_text())
    DELTA=json.loads((ROOT/'results/kolmo_calibration.json').read_text())['delta']

def member(task):
    c,m=task;out=ROOT/'runs/kolmo/test/truth_shards'/str(c);out.mkdir(parents=True,exist_ok=True)
    path=out/f'{m:03d}.npy'
    if path.exists():return c,m,np.load(path)
    window=OBS[c]+.02*INFO['sigma']*rng('truth',1,2,c,m).standard_normal(OBS[c].shape)
    value=costs(window[-1:],DELTA,INFO['lambda_mean'],chunk=1,horizons=GRID)[:,0]
    tmp=path.with_suffix('.tmp')
    with tmp.open('wb') as file:np.save(file,value)
    os.replace(tmp,path);return c,m,value

def main(workers):
    if not (ROOT/'AAH_FREEZE_CALIBRATION_KOLMO.md').exists():raise RuntimeError('missing numeric freeze')
    context=multiprocessing.get_context('spawn');values=np.empty((30,6,512,len(GRID)))
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers,mp_context=context,initializer=initialize) as pool:
        futures={pool.submit(member,(c,m)) for c in range(30) for m in range(512)}
        n=0
        for future in concurrent.futures.as_completed(futures):
            c,m,value=future.result();values[c,:,m]=value;n+=1
            if n%128==0:print('Kolmo truth members',n,'/15360',flush=True)
    for c in range(30):np.save(ROOT/f'runs/kolmo/test/truth_{c:03d}.npy',values[c])
    write_json(ROOT/'runs/kolmo/test/truth_complete.json',dict(git_sha=sha(),cases=30,members=512,workers=workers))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--workers',type=int,default=128);main(p.parse_args().workers)
