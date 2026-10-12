"""Descriptive-only adapters to frozen Part3b inference and Stage18 JVP kernels."""
from acd_stage23_common import *
import argparse,subprocess,time
sys.path.insert(0,str(FROZEN18))

def run(part):
 cfg=ready();sel=json.loads((OUT/'selection.json').read_text())['selected'];checkpoint=OUT/'training'/sel['model']/'selected.pt';assert digest(checkpoint)==sel['checkpoint_sha256']
 name='CNN-noF-response-corrected-selected'
 if part=='part3b':
  import acd_stage18_inference as frozen
  frozen.OUT=OUT/'fresh19';frozen.guarded=ready
  inputs=FROZEN18/'runs/stage19/inference_inputs'
  frozen.run(name,inputs,checkpoint,256)
  folder=frozen.OUT/'inference'/name
 else:
  import acd_stage18_derivatives as frozen
  frozen.OUT=OUT/'original';frozen.guarded=ready
  inputs=FROZEN18/'runs/stage18/confirmation_inputs'
  frozen.run(name,checkpoint,inputs,128,False,None)
  folder=frozen.OUT/'derivatives'/name
 meta=json.loads((folder/'complete.json').read_text());hashes=meta.get('output_hashes') or json.loads((folder/'hashes.json').read_text())
 expected=len(list(inputs.glob('[0-9][0-9][0-9].npz')));assert len(hashes)==expected and all(digest(folder/p)==h for p,h in hashes.items())
 write(OUT/f'{part}_inference_complete.json',dict(cases=expected,model=name,checkpoint_sha256=digest(checkpoint),output_folder=str(folder),kernel_sha256=digest(Path(frozen.__file__)),output_hashes=hashes,scope='descriptive only',realized_outcome_accesses=[]))

def launch(part,index):
 import acd_stage18_gpu_lease as lease
 from acd_stage19_part2_gate import gpu_inventory
 lease.OUT=OUT;lease.freeze_ready=ready
 while True:
  card=next(c for c in gpu_inventory() if c['index']==index)
  if all('VLLM' in p['process'].upper() for p in card['processes']):break
  time.sleep(60)
 with lease.lease(index) as card:
  env=dict(os.environ,CUDA_VISIBLE_DEVICES=card['uuid'],OMP_NUM_THREADS='4',OPENBLAS_NUM_THREADS='4')
  folder=OUT/'task_logs';folder.mkdir(exist_ok=True)
  with (folder/f'{part}.log').open('a') as log:p=subprocess.run([GPU,'-u',__file__,'--part',part,'--worker'],cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT)
  row=dict(part=part,gpu=card,returncode=p.returncode,utc=time.time());write(folder/f'{part}.json',row)
  if p.returncode or not (OUT/f'{part}_inference_complete.json').exists():write(OUT/f'FAILED_{part}.json',row);raise RuntimeError('Descriptive phase failed')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--part',choices=['part3b','derivative'],required=True);p.add_argument('--gpu',type=int);p.add_argument('--worker',action='store_true');a=p.parse_args();run(a.part) if a.worker else launch(a.part,a.gpu)
