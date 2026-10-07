"""Stage10b offline Spark queue; one GPU job at a time, failures do not stop queue."""
import json,subprocess,time,traceback
from pathlib import Path
ROOT=Path('/home/todd/work/aspen-stage9-20261006')
NEW=ROOT/'stage10b'
IMAGE='nvcr.io/nvidia/pytorch:26.07-py3'
def container(mounts,command):
 return subprocess.run(['docker','run','--rm','--gpus','all','--network','none','--ipc=host']+[x for source,target,mode in mounts for x in ['-v',str(source)+':'+target+':'+mode]]+[IMAGE,'python','-u']+command).returncode
def main():
 failure=json.loads((NEW/'code/acd_stage10_failure.json').read_text())
 models=[('CNN-noF',0.),('CNN-F-resp-0.01',.01)]
 for name,weight in models:
  out=NEW/'training'/name;out.mkdir(parents=True,exist_ok=True)
  prior=failure['accounting_gpu_seconds'] if name==failure['model'] else 0
  code=container([(NEW/'code/acd_stage10b_train.py','/acd_stage10b_train.py','ro'),(ROOT/'code/acd_stage10_loss_balance.py','/acd_stage10_loss_balance.py','ro'),(ROOT/'training/data','/data','ro'),(out,'/out','rw')],['/acd_stage10b_train.py','--name',name,'--resp-weight',str(weight),'--prior-charge',str(prior),'--data','/data','--out','/out'])
  (out/'queue_exit.json').write_text(json.dumps(dict(model=name,returncode=code,completed=(out/'complete.json').exists()))+'\n')
  if code:print('TRAINING FAILURE; continuing queue:',name,code,flush=True)
 for name,weight in models:
  out=NEW/'training'/name
  if not (out/'complete.json').exists():continue
  dest=NEW/'inference'/name;dest.mkdir(parents=True,exist_ok=True)
  code=container([(ROOT/'code/acd_stage9_cnn.py','/code/acd_stage9_cnn.py','ro'),(ROOT/'code/acd_stage9_train.py','/code/acd_stage9_train.py','ro'),(ROOT/'evaluation','/data','ro'),(out/'selected.pt','/checkpoint/selected.pt','ro'),(dest,'/out','rw')],['/code/acd_stage9_cnn.py','--name',name,'--checkpoint','/checkpoint/selected.pt','--data','/data','--out','/out','--micro','1024'])
  (dest/'queue_exit.json').write_text(json.dumps(dict(model=name,returncode=code,completed=(dest/'complete.json').exists()))+'\n')
  if code:print('INFERENCE FAILURE; continuing queue:',name,code,flush=True)
 (NEW/'queue_complete.json').write_text(json.dumps(dict(completed=True,models=[name for name,_ in models]))+'\n')
if __name__=='__main__':main()
