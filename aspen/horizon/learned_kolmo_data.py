"""Action-conditioned World D training data, disjoint namespaces and frozen sizes."""
import argparse
import json
import time
import numpy as np
import torch
from common import ROOT,rng,patterns,sha,write_json
from kolmo import KolmoAction

@torch.no_grad()
def main(device,chunk):
    torch.set_num_threads(1)
    cal=json.loads((ROOT/'results/kolmo_calibration.json').read_text())
    if not (ROOT/'AAH_FREEZE_CALIBRATION_KOLMO.md').exists():raise RuntimeError('missing freeze addendum')
    system=json.loads((ROOT/'runs/kolmo/system.json').read_text())
    delta=cal['delta'];lam=system['lambda_mean']
    out=ROOT/'runs/kolmo/learned';out.mkdir(parents=True,exist_ok=True)
    nf=int(np.ceil(25/lam/.35))+11
    for ns,n in [('train',1024),('val',64)]:
        path=out/f'{ns}.npy'
        if path.exists():raise FileExistsError(path)
        R=rng(ns,1,4);indices=R.integers(6,size=n);amplitudes=R.uniform(-2*delta,2*delta,size=n)
        action=amplitudes[:,None,None]*np.sqrt(8.)*patterns(1)[indices]
        np.save(out/f'{ns}_actions.npy',action.astype(np.float32))
        data=np.lib.format.open_memmap(path,mode='w+',dtype=np.float32,shape=(n,nf,64,64))
        begin=time.time()
        for first in range(0,n,chunk):
            last=min(n,first+chunk);m=last-first
            model=KolmoAction(np.full(m,40.),device=device)
            z=model.random_ic(rng(ns,1,case=first),m)
            z=model.flow(z,50000)
            for t in range(11):
                data[first:last,t]=model.to_phys(z).cpu().numpy().astype(np.float32)
                if t<10:z=model.flow(z,35)
            forcing=torch.as_tensor(action[first:last],device=device,dtype=torch.float64)
            model.F_hat=model.F_hat0+torch.fft.rfft2(forcing)*model.mask
            for t in range(11,nf):
                z=model.flow(z,35)
                data[first:last,t]=model.to_phys(z).cpu().numpy().astype(np.float32)
            data.flush()
            print(f'Kolmo learned {ns}: {last}/{n}',flush=True)
        write_json(out/f'{ns}.json',dict(trajectories=n,frames=nf,seconds=time.time()-begin,git_sha=sha(),chunk=chunk,device=device))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--device',default='cuda:1');p.add_argument('--chunk',type=int,default=256)
    a=p.parse_args();main(a.device,a.chunk)
