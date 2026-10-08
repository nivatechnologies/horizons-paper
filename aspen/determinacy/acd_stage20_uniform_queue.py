"""Isolated offline Spark uniform extension; no preemption of prior B/C queues."""
import argparse,hashlib,json,socket,subprocess,time
from pathlib import Path
ROOT=Path('/home/todd/work/aspen-stage20-uniform-20261008')
def run(kind):
 marker=json.loads((ROOT/'amendment_pushed.json').read_text());assert marker['commit']
 contract=json.loads((ROOT/'contract.json').read_text())
 for category,folder in [('code_hashes','code'),('checkpoints','models'),('inputs','inputs')]:
  for p,h in contract[category].items():assert hashlib.sha256((ROOT/folder/p).read_bytes()).hexdigest()==h,p
 assert (ROOT/'prior_B_C_complete.json').exists()
 names=['physics','CNN-F','CNN-noF']+[f'{m}-seed{i}' for i in range(1,5) for m in ['CNN-F','CNN-noF']] if kind=='E0' else [f'CNN-F-E1-rolling-seed{j}' for j in range(1,6)]
 outcomes={}
 for name in names:
  out=ROOT/kind/'inference'/name;out.mkdir(parents=True,exist_ok=True)
  if (out/'complete.json').exists():continue
  while subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip():time.sleep(60)
  args=['--kind',kind,'--name',name,'--models','/models','--data','/data','--out','/out']
  if kind=='E1':args+=['--seed',name.rsplit('seed',1)[1]]
  start=time.monotonic()
  cmd=['docker','run','--rm','--gpus','all','--network','none','--ipc=host','-v',str(ROOT/'code')+':/code:ro','-v',str(ROOT/'models')+':/models:ro','-v',str(ROOT/'inputs')+':/data:ro','-v',str(out)+':/out:rw','nvcr.io/nvidia/pytorch:26.07-py3','python','-u','/code/acd_stage20_uniform_gpu.py',*args]
  with (ROOT/kind/(name+'.log')).open('a') as log:status=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT).returncode
  outcomes[name]=dict(returncode=status,seconds=time.monotonic()-start,host=socket.gethostname(),completed=(out/'complete.json').exists());(ROOT/kind/'queue_outcomes.json').write_text(json.dumps(outcomes,indent=2)+'\n')
 (ROOT/kind/'queue_complete.json').write_text(json.dumps(dict(host=socket.gethostname(),outcomes=outcomes))+'\n')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('kind',choices=['E0','E1']);run(p.parse_args().kind)
