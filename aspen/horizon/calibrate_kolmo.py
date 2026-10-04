"""Run Kolmogorov brute-force calibration ensembles on sulaco CPU."""
import argparse
import concurrent.futures
import multiprocessing
import time
import numpy as np
import torch
from common import ROOT,rng,eligible,write_json,sha
from kolmo import costs

def case_run(c,delta,chunk):
    torch.set_num_threads(1)
    out=ROOT/'runs'/'kolmo'
    system=__import__('json').loads((out/'system.json').read_text())
    y=np.load(out/'observations.npz')['observed'][c,-1]
    initial=y+.02*system['sigma']*rng('calibration',1,2,c).standard_normal((256,64,64))
    begin=time.time()
    values=costs(initial,delta,system['lambda_mean'],chunk=chunk)[:,:,0]
    result=eligible(values,'calibration',1,c)
    result.update(case=c,delta=delta,seconds=time.time()-begin,git_sha=sha())
    write_json(out/f'calibration_delta{delta}_case{c}.json',result)
    print(f'Kolmo delta={delta} case={c+1}/20 eligible={result["eligible"]} seconds={result["seconds"]:.1f}',flush=True)
    return result

def main(workers,chunk):
    out=ROOT/'runs'/'kolmo'
    if (out/'calibration.json').exists():
        raise FileExistsError('calibration already exists')
    begin=time.time();rows=[];chosen=None
    context=multiprocessing.get_context('spawn')
    for delta in (.01,.02,.05,.1):
        with concurrent.futures.ProcessPoolExecutor(max_workers=workers,mp_context=context) as pool:
            tasks=[pool.submit(case_run,c,delta,chunk) for c in range(20)]
            panel=[task.result() for task in tasks]
        n=sum(r['eligible'] for r in panel)
        rows.append(dict(delta=delta,eligible=n,total=20,fraction=n/20,cases=panel))
        write_json(out/'calibration_progress.json',dict(rows=rows,git_sha=sha()))
        if n>=16:
            chosen=delta;break
    status='CALIBRATION_FAIL' if chosen is None else 'AWAITING_ACTION_CHAOS_ON_BACCUS'
    write_json(out/'calibration.json',dict(status=status,delta=chosen,rows=rows,
               seconds=time.time()-begin,git_sha=sha(),workers=workers,chunk=chunk))
    print('Kolmo calibration',status,'delta',chosen,flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--workers',type=int,default=16)
    p.add_argument('--chunk',type=int,default=64)
    a=p.parse_args();main(a.workers,a.chunk)
