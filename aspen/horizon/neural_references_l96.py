"""True scoring targets at neural output ticks; never used as forecasts/inputs."""
import json
import numpy as np
import numba
from common import ROOT,GRID,patterns,sha,write_json
from l96 import rollout

def main():
    numba.set_num_threads(64)
    cal=json.loads((ROOT/'results/l96_calibration.json').read_text())
    lam=cal['system']['lambda_mean'];delta=cal['delta']
    root=ROOT/'runs/l96/test';true=np.load(root/'observations.npz')['true']
    times=np.rint(GRID/lam/.05)*.05
    for c in range(200):
        _,snap=rollout(np.tile(true[c,-1],(8,1)),8+8*delta*patterns(0),lam,times*lam,capture=True)
        np.save(root/f'neural_target_{c:03d}.npy',snap)
    write_json(root/'neural_target_times.json',dict(nominal_T=GRID.tolist(),actual_times=times.tolist(),git_sha=sha(),
               purpose='score-only true target at same nearest output tick as learned predictor'))

if __name__=='__main__':main()
