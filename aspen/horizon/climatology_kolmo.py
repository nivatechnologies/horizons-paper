"""True controlled action means:50LT spin-up then500LT output average."""
import argparse
import json
import numpy as np
import torch
from common import ROOT,rng,write_json,sha
from kolmo import KolmoAction

@torch.no_grad()
def main(device):
    torch.set_num_threads(1)
    if not (ROOT/'AAH_FREEZE_CALIBRATION_KOLMO.md').exists():raise RuntimeError('missing numeric freeze')
    delta=json.loads((ROOT/'results/kolmo_calibration.json').read_text())['delta']
    lam=json.loads((ROOT/'runs/kolmo/system.json').read_text())['lambda_mean']
    model=KolmoAction(np.full(6,40.),delta,np.arange(6),device)
    state=model.random_ic(rng('climatology',1),6)
    state=model.flow(state,int(round(50/lam/.01)))
    samples=int(np.floor(500/lam/.35));total=torch.zeros((6,64,64),dtype=torch.float64,device=device)
    for _ in range(samples):
        state=model.flow(state,35);total+=model.to_phys(state)
    path=ROOT/'runs/kolmo/test/climatology.npy'
    np.save(path,(total/samples).cpu().numpy())
    write_json(path.with_suffix('.json'),dict(git_sha=sha(),samples=samples,spin_LT=50,average_LT=500,device=device))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--device',default='cuda:1');main(p.parse_args().device)
