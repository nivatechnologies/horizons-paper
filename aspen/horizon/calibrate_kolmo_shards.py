"""Frozen calibration, parallelized over members using unchanged Torch solver."""
import argparse
import concurrent.futures
import json
import multiprocessing
import os
import time
import numpy as np
import torch
from common import ROOT,rng,eligible,write_json,sha
from kolmo import costs

OBS=None
SYSTEM=None

def initialize():
    global OBS,SYSTEM
    torch.set_num_threads(1)
    SYSTEM=json.loads((ROOT/'runs/kolmo/system.json').read_text())
    OBS=np.load(ROOT/'runs/kolmo/observations.npz')['observed'][:,-1]

def member(task):
    c,m,delta=task
    out=ROOT/'runs/kolmo/calibration_shards'/str(delta)/str(c)
    out.mkdir(parents=True,exist_ok=True)
    path=out/f'{m:03d}.npy'
    if path.exists():return c,m,np.load(path)
    # Recreate the exact original whole-ensemble random array before slicing.
    noise=rng('calibration',1,2,c).standard_normal((256,64,64))
    initial=OBS[c]+.02*SYSTEM['sigma']*noise[m:m+1]
    value=costs(initial,delta,SYSTEM['lambda_mean'],chunk=1)[:,0,0]
    tmp=path.with_suffix('.tmp')
    with tmp.open('wb') as file:np.save(file,value)
    os.replace(tmp,path)
    return c,m,value

def main(workers):
    root=ROOT/'runs/kolmo';begin=time.time();rows=[];chosen=None
    if (root/'calibration.json').exists():raise FileExistsError('completed calibration exists')
    context=multiprocessing.get_context('spawn')
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers,mp_context=context,initializer=initialize) as pool:
        for delta in (.01,.02,.05,.1):
            values=np.empty((20,6,256))
            tasks={pool.submit(member,(c,m,delta)) for c in range(20) for m in range(256)}
            completed=0
            for future in concurrent.futures.as_completed(tasks):
                c,m,value=future.result();values[c,:,m]=value;completed+=1
                if completed%128==0:
                    print(f'Kolmo delta={delta} members={completed}/5120',flush=True)
            panel=[eligible(values[c],'calibration',1,c) for c in range(20)]
            count=sum(row['eligible'] for row in panel)
            rows.append(dict(delta=delta,eligible=count,total=20,fraction=count/20,cases=panel))
            write_json(root/'calibration_progress.json',dict(rows=rows,git_sha=sha(),backend='unchanged Torch IFRK4, member-sharded'))
            print(f'Kolmo delta={delta} eligible={count}/20',flush=True)
            if count>=16:
                chosen=delta;break
    write_json(root/'calibration.json',dict(status='CALIBRATION_FAIL' if chosen is None else 'AWAITING_ACTION_CHAOS_ON_BACCUS',
               delta=chosen,rows=rows,seconds=time.time()-begin,git_sha=sha(),workers=workers,chunk=1,
               backend='unchanged Torch IFRK4, member-sharded'))
    print('Kolmo calibration complete delta=',chosen,flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--workers',type=int,default=128)
    main(p.parse_args().workers)
