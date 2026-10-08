"""Shifted-panel adapter to frozen Stage9/18 GPU rollouts, without realized access."""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',NUMBA_NUM_THREADS='4')
import argparse,json,time,subprocess,sys
from pathlib import Path
import numpy as np
from acd_protocol import ROOT,physics,PATTERNS,WINDOWS,SIGMA
from acd_stage21_contract import OUT,digest
from acd_stage21_freeze_e import ready

def prepare():
 d=ready();target=OUT/'inference_inputs';target.mkdir(exist_ok=True)
 settings=dict(sigma=float(SIGMA),patterns=PATTERNS.tolist(),windows=[w.tolist() for w in WINDOWS])
 (target/'settings.json').write_text(json.dumps(settings,indent=2)+'\n')
 for c in range(200):
  output=target/f'{c:03d}.npz';source=OUT/f'main_forecast_{c:03d}.npz'
  if not output.exists():
   with np.load(source) as z:theta=z['theta'].copy()
   f=theta[:,40];h=physics.simulate(theta[:,:40],np.repeat(f[:,None],40,1),.01,11)
   tmp=output.with_suffix('.tmp.npz');np.savez_compressed(tmp,H=h,F=f);tmp.replace(output)
   output.with_suffix('.json').write_text(json.dumps(dict(source_sha256=digest(source),sha256=digest(output)))+'\n')
 for arm in ['meanF','constantF']:
  folder=OUT/'A_inputs'/arm;folder.mkdir(parents=True,exist_ok=True)
  (folder/'settings.json').write_bytes((target/'settings.json').read_bytes())
  for c in range(200):
   output=folder/f'{c:03d}.npz'
   if output.exists():continue
   with np.load(target/f'{c:03d}.npz') as z:h,f=z['H'].copy(),z['F'].copy()
   f.fill(f.mean() if arm=='meanF' else 8.)
   np.savez_compressed(output,H=h,F=f)

def complete(name):
 folder=OUT/'inference'/name
 if not (folder/'complete.json').exists():return False
 d=json.loads((folder/'complete.json').read_text());hashes=json.loads((folder/'hashes.json').read_text())
 return d['cases']==200 and len(hashes)==200 and all(digest(folder/p)==h for p,h in hashes.items())

def worker(name):
 d=ready();r=next(x for x in d['tasks'] if x['name']==name)
 import acd_stage18_inference as original
 original.guarded=lambda:d;original.OUT=OUT
 source=OUT/'inference_inputs'
 if r.get('arm') in ['meanF','constantF']:source=OUT/'A_inputs'/r['arm']
 original.run(name,source,ROOT/r['checkpoint'],256,ROOT/r['estimator'] if r['estimator'] else None,r.get('kind'),r.get('rolling',False))
 folder=OUT/'inference'/name;record=json.loads((folder/'complete.json').read_text())
 record.update(stage=21,hardware_path='Baccus 170HX',adapter_sha256=digest(__file__),realized_outcome_accesses=[])
 (folder/'complete.json').write_text(json.dumps(record,indent=2)+'\n');assert complete(name)

def controller():
 d=ready();prepare()
 from acd_stage19_part2_gate import gpu_inventory
 import acd_stage19_gpu_lease as lease
 # Redirect lease logging and freeze verification only; inherited files/queues are unchanged.
 lease.OUT=OUT;lease.freeze_ready=ready
 for r in d['tasks']:
  if complete(r['name']):continue
  while True:
   cards=gpu_inventory()
   eligible=[c for c in cards if all('VLLM' in p['process'].upper() for p in c['processes'])]
   if eligible:break
   time.sleep(60)
  with lease.lease(eligible[0]['index']) as card:
   env=dict(os.environ,CUDA_VISIBLE_DEVICES=card['uuid'])
   folder=OUT/'inference_logs';folder.mkdir(exist_ok=True)
   begin=time.monotonic()
   with (folder/(r['name']+'.log')).open('a') as log:
    result=subprocess.run([sys.executable,__file__,'worker','--name',r['name']],cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT)
   (folder/(r['name']+'.json')).write_text(json.dumps(dict(gpu=card,seconds=time.monotonic()-begin,exit_code=result.returncode),indent=2)+'\n')
 (OUT/'inference_complete.json').write_text(json.dumps(dict(complete=[r['name'] for r in d['tasks'] if complete(r['name'])],failed=[r['name'] for r in d['tasks'] if not complete(r['name'])]))+'\n')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('mode',choices=['worker','controller']);p.add_argument('--name');a=p.parse_args()
 worker(a.name) if a.mode=='worker' else controller()
