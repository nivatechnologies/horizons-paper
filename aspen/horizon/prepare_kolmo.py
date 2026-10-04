"""Generate calibration-only observations on Baccus; no test data."""
import argparse
import time
import numpy as np
import torch
from common import ROOT,rng,write_json,sha,KOLMO_LAMBDA
from kolmo import KolmoAction

@torch.no_grad()
def main(device):
    torch.set_num_threads(1)
    out=ROOT/'runs'/'kolmo';out.mkdir(parents=True,exist_ok=True)
    if (out/'observations.npz').exists():
        raise FileExistsError('calibration observations already exist')
    begin=time.time()
    model=KolmoAction(device=device)
    z=model.random_ic(rng('lyapunov',1),64)
    z=model.flow(z,50000)
    rms=[]
    for _ in range(20):
        z=model.flow(z,140);rms.append(model._mean_sq(z).cpu().numpy())
    sigma=float(np.sqrt(np.mean(rms)))
    z=model.random_ic(rng('calibration',1),20)
    z=model.flow(z,50000)
    windows=[model.to_phys(z).cpu().numpy()]
    for _ in range(10):
        z=model.flow(z,35);windows.append(model.to_phys(z).cpu().numpy())
    true=np.stack(windows,1)
    y=true+.02*sigma*rng('calibration',1,1).standard_normal(true.shape)
    np.savez(out/'observations.npz',observed=y,true=true)
    write_json(out/'system.json',dict(lambda_mean=KOLMO_LAMBDA,sigma=sigma,
               inherited_lambda_source='adapt_physics/results/chaos_gate.json:Re40',
               dt=.01,output=.35,precision='float64',seconds=time.time()-begin,git_sha=sha()))
    print('Kolmogorov calibration observations prepared, sigma=',sigma,flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--device',default='cuda:0')
    main(p.parse_args().device)
