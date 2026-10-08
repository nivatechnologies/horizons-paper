"""Frozen Stage18 rollout on isolated Stage21 Spark inputs; no outcome access."""
import argparse,hashlib,json,socket,subprocess,time
from pathlib import Path
ROOT=Path('/home/todd/work/aspen-stage21-20261008')
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def worker(name):
 d=json.loads((ROOT/'contract.json').read_text());assert (ROOT/'reorder_pushed.json').exists()
 for p,h in d['code_hashes'].items():assert digest(ROOT/'code'/p)==h,p
 for p,h in d['inputs'].items():assert digest(ROOT/'inputs'/p)==h,p
 row=next(r for r in d['tasks'] if r['name']==name)
 for key in ['checkpoint','estimator']:
  if row.get(key):assert digest(ROOT/row[key])==row[key+'_sha256']
 import torch
 torch.set_num_threads(4);torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False;torch.backends.cudnn.deterministic=True;torch.backends.cudnn.benchmark=False
 import acd_stage18_inference as frozen
 frozen.guarded=lambda:d;frozen.OUT=ROOT
 frozen.run(name,ROOT/'inputs',ROOT/row['checkpoint'],256,ROOT/row['estimator'],row['kind'],row['rolling'])
 p=ROOT/'inference'/name/'complete.json';done=json.loads(p.read_text());done.update(stage=21,hardware_path='DGX Spark GB10 offline pytorch26.07',host=socket.gethostname(),adapter_sha256=digest(__file__),realized_outcome_accesses=[],cases=200);p.write_text(json.dumps(done,indent=2)+'\n')
def queue():
 d=json.loads((ROOT/'contract.json').read_text());outcomes={}
 for row in d['tasks']:
  name=row['name'];out=ROOT/'inference'/name;out.mkdir(parents=True,exist_ok=True)
  if (out/'complete.json').exists():continue
  while subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip():time.sleep(60)
  start=time.monotonic()
  cmd=['docker','run','--rm','--gpus','all','--network','none','--ipc=host','-v',str(ROOT/'code')+':/code:ro','-v',str(ROOT/'models')+':/models:ro','-v',str(ROOT/'inputs')+':/inputs:ro','-v',str(ROOT/'contract.json')+':/contract.json:ro','-v',str(ROOT/'reorder_pushed.json')+':/reorder_pushed.json:ro','-v',str(out)+':/inference/'+name+':rw','-e','ACD_STAGE21_CONTAINER=1','nvcr.io/nvidia/pytorch:26.07-py3','python','-u','/code/acd_stage21_spark.py','worker','--name',name]
  with (ROOT/(name+'.log')).open('a') as log:status=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT).returncode
  outcomes[name]=dict(returncode=status,seconds=time.monotonic()-start,host=socket.gethostname(),complete=(out/'complete.json').exists());(ROOT/'queue_outcomes.json').write_text(json.dumps(outcomes,indent=2)+'\n')
 (ROOT/'queue_complete.json').write_text(json.dumps(outcomes,indent=2)+'\n')
if __name__=='__main__':
 import os
 if os.environ.get('ACD_STAGE21_CONTAINER'):ROOT=Path('/')
 p=argparse.ArgumentParser();p.add_argument('mode',choices=['queue','worker']);p.add_argument('--name');a=p.parse_args();worker(a.name) if a.mode=='worker' else queue()
