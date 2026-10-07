"""Offline Spark Stage16 alternating queue; each failed run is reported."""
import hashlib,json,subprocess,traceback,time,socket
from pathlib import Path
ROOT=Path('/home/todd/work/aspen-stage9-20261006')
STAGE=ROOT/'stage16'
IMAGE='nvcr.io/nvidia/pytorch:26.07-py3'
def container(mounts,command):
 return subprocess.run(['docker','run','--rm','--gpus','all','--network','none','--ipc=host']+[x for source,target,mode in mounts for x in ['-v',str(source)+':'+target+':'+mode]]+[IMAGE,'python','-u']+command).returncode

def main():
 freeze=json.loads((STAGE/'code/acd_stage16_freeze.json').read_text())
 assert (STAGE/'freeze_push_verified.json').exists()
 for filename in ['acd_stage16_train.py','acd_stage16_queue.py']:
  assert hashlib.sha256((STAGE/'code'/filename).read_bytes()).hexdigest()==freeze['code_hashes'][filename]
 for filename in ['acd_stage9_cnn.py','acd_stage9_train.py']:
  assert hashlib.sha256((ROOT/'code'/filename).read_bytes()).hexdigest()==freeze['code_hashes'][filename]
 for name,expected in freeze['data_sha256'].items():assert hashlib.sha256((ROOT/'training/data'/name).read_bytes()).hexdigest()==expected
 host=json.loads((STAGE/'host_assignment.json').read_text())['host']
 for run in freeze['runs']:
  if run['host']!=host:continue
  name=run['name'];out=STAGE/'training'/name;out.mkdir(parents=True,exist_ok=True)
  try:
   if not (out/'queue_exit.json').exists() and not (out/'complete.json').exists():
    args=['/trainer.py','--name',name,'--data','/data','--out','/out','--torch-seed',str(run['torch_seed']),'--batch-seed',str(run['batch_seed'])]
    if run['conditioned']:args+=['--conditioned']
    started=time.monotonic()
    code=container([(STAGE/'code/acd_stage16_train.py','/trainer.py','ro'),(ROOT/'training/data','/data','ro'),(out,'/out','rw')],args)
    (out/'queue_exit.json').write_text(json.dumps(dict(model=name,host=host,returncode=code,completed=(out/'complete.json').exists(),launcher_elapsed_seconds=time.monotonic()-started))+'\n')
   # Selected checkpoint can be scored even when the model ends at its frozen cap/guard limit.
   if not (out/'selected.pt').exists():
    dest=STAGE/'inference'/name;dest.mkdir(parents=True,exist_ok=True)
    (dest/'queue_exit.json').write_text(json.dumps(dict(model=name,host=host,completed=False,reason='no selected checkpoint'))+'\n')
    print('NO SELECTED CHECKPOINT',name,flush=True);continue
   dest=STAGE/'inference'/name;dest.mkdir(parents=True,exist_ok=True)
   if not (dest/'queue_exit.json').exists():
    code=container([(ROOT/'code/acd_stage9_cnn.py','/code/acd_stage9_cnn.py','ro'),(ROOT/'code/acd_stage9_train.py','/code/acd_stage9_train.py','ro'),(ROOT/'evaluation','/data','ro'),(out/'selected.pt','/checkpoint/selected.pt','ro'),(dest,'/out','rw')],['/code/acd_stage9_cnn.py','--name',name,'--checkpoint','/checkpoint/selected.pt','--data','/data','--out','/out','--micro','1024'])
    (dest/'queue_exit.json').write_text(json.dumps(dict(model=name,host=host,returncode=code,completed=(dest/'complete.json').exists()))+'\n')
  except Exception:
   (out/'queue_error.txt').write_text(traceback.format_exc());traceback.print_exc()
 (STAGE/'queue_complete.json').write_text(json.dumps(dict(completed=True,host=host,runs=[r['name'] for r in freeze['runs'] if r['host']==host]))+'\n')
if __name__=='__main__':main()
