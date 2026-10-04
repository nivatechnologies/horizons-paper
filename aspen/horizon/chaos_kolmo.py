"""Every-action World D chaos gate at calibrated amplitude, on Baccus."""
import argparse
import json
import time
import numpy as np
import torch
from common import ROOT,rng,write_json,sha
from kolmo import KolmoAction,lyapunov

@torch.no_grad()
def main(device):
    torch.set_num_threads(1)
    cal=json.loads((ROOT/'results/kolmo_calibration.json').read_text())
    if cal['delta'] is None:raise RuntimeError('no admissible calibrated delta')
    delta=cal['delta'];gates=[];begin=time.time()
    out=ROOT/'results'
    for k in range(6):
        model=KolmoAction(np.full(64,40.),delta,actions=k,device=device)
        states=model.random_ic(rng('lyapunov',1,case=k+1),64)
        states=model.flow(states,50000)
        values=lyapunov(model,states,800.,rng=rng('lyapunov',1,sub=5,case=k+1))
        mean=float(values.mean());se=float(values.std(ddof=1)/8)
        gate=dict(action=k,lambda_mean=mean,lambda_ci95=[mean-1.96*se,mean+1.96*se],
                  chaotic=mean-1.96*se>0,per_start=values.tolist())
        gates.append(gate)
        write_json(out/'kolmo_action_chaos.json',dict(gates=gates,delta=delta,seconds=time.time()-begin,git_sha=sha()))
        print('Kolmo action chaos',k,gate['lambda_ci95'],flush=True)
        if not gate['chaotic']:
            cal['status']='STOP_ACTION_CHAOS';break
    else:
        cal['status']='READY_FOR_CALIBRATION_FREEZE_ADDENDUM'
    write_json(out/'kolmo_calibration.json',cal)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--device',default='cuda:0')
    main(p.parse_args().device)
