"""Nonpreempting Stage23 queue: launch each run as soon as a card is free."""
from acd_stage23_common import *
import argparse,threading,subprocess,time,collections,fcntl
sys.path.insert(0,str(FROZEN18))

def name(weight,index):return f'CNN-noF-response-{weight:g}-seed{index}'
def training_tasks(cfg,weights,seeds):
 return [dict(name=name(w,s['index']),weight=w,seed=s) for s in seeds for w in weights]
def slots(tasks):
 import acd_stage18_gpu_lease as lease
 from acd_stage19_part2_gate import gpu_inventory
 lease.OUT=OUT;lease.freeze_ready=ready
 pending=collections.deque(tasks);lock=threading.Lock();outcomes={}
 def worker(index):
  while True:
   with lock:
    if not pending:return
    task=pending.popleft()
   model=task['name'];directory=OUT/'training'/model;complete=directory/'complete.json';record=OUT/'task_logs'/f'{model}.json';record.parent.mkdir(parents=True,exist_ok=True)
   if complete.exists():
    meta=json.loads(complete.read_text());outcomes[model]=dict(returncode=0,complete=True,selected_step=meta.get('selected_step'));continue
   while True:
    card=next(c for c in gpu_inventory() if c['index']==index)
    if all('VLLM' in p['process'].upper() for p in card['processes']):break
    write(OUT/f'waiting_gpu_{index}.json',dict(gpu=card,waiting_model=model,utc=time.time()));time.sleep(60)
   begin=time.monotonic()
   try:
    with lease.lease(index) as card:
     env=dict(os.environ,CUDA_VISIBLE_DEVICES=card['uuid'],OMP_NUM_THREADS='4',OPENBLAS_NUM_THREADS='4',ACD_STAGE23_FROZEN18=str(FROZEN18))
     args=[GPU,'-u',str(ROOT/'acd_stage23_train.py'),'--name',model,'--data',str(FROZEN18/'runs/stage18/response_data'),'--out',str(directory),'--micro','128','--torch-seed',str(task['seed']['torch_seed']),'--batch-seed',str(task['seed']['batch_seed']),'--response-weight',str(task['weight'])]
     with (OUT/'task_logs'/f'{model}.log').open('a') as f:child=subprocess.Popen(args,cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT)
     write(OUT/f'active_gpu_{index}.json',dict(model=model,pid=child.pid,gpu=card,utc=time.time()))
     while child.poll() is None:
      progress=directory/'progress.json'
      if progress.exists() and not (OUT/'timing.json').exists() and model==tasks[0]['name']:
       rows=json.loads(progress.read_text());row=next((x for x in rows if x['step']==500),None)
       if row:write(OUT/'timing.json',dict(model=model,pilot_updates=row['step'],charged_gpu_seconds=row['charged_gpu_seconds'],projected_seconds=row['charged_gpu_seconds']/row['step']*20000,projection_rule='charged seconds at first 500 scheduled updates times 20000/500; cap unchanged',cap_seconds=36000,source=str(progress),utc=time.time()))
      time.sleep(5)
     rc=child.returncode
    meta=json.loads(complete.read_text()) if complete.exists() else None
    row=dict(task=task,gpu=card,returncode=rc,complete=complete.exists(),seconds=time.monotonic()-begin,selected_step=None if meta is None else meta.get('selected_step'),utc=time.time())
    if rc or meta is None or meta.get('selected_step') is None:write(OUT/f'FAILED_{model}.json',dict(reason='Nonzero trainer return code, missing completion, or no eligible checkpoint',**row))
   except Exception as e:
    row=dict(task=task,returncode=1,complete=False,error=str(e),utc=time.time());write(OUT/f'FAILED_{model}.json',row)
   write(record,row)
   with lock:outcomes[model]=row;write(OUT/'training_outcomes.json',outcomes)
   (OUT/f'active_gpu_{index}.json').unlink(missing_ok=True)
 threads=[threading.Thread(target=worker,args=(i,)) for i in range(3)]
 for t in threads:t.start()
 for t in threads:t.join()
 return outcomes

def gpu_step(script):
 import acd_stage18_gpu_lease as lease
 from acd_stage19_part2_gate import gpu_inventory
 lease.OUT=OUT;lease.freeze_ready=ready
 while True:
  cards=[c for c in gpu_inventory() if all('VLLM' in p['process'].upper() for p in c['processes'])]
  if cards:break
  time.sleep(60)
 with lease.lease(cards[0]['index']) as card:
  env=dict(os.environ,CUDA_VISIBLE_DEVICES=card['uuid'],OMP_NUM_THREADS='4',OPENBLAS_NUM_THREADS='4')
  with (OUT/'task_logs'/f'{script}.log').open('a') as f:p=subprocess.run([GPU,'-u',str(ROOT/script)],cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT)
  write(OUT/'task_logs'/f'{script}.json',dict(returncode=p.returncode,gpu=card,utc=time.time()))
  if p.returncode:write(OUT/'FAILED.json',dict(phase=script,returncode=p.returncode));raise RuntimeError('Phase failed: '+script)

def main():
 cfg=ready();OUT.mkdir(parents=True,exist_ok=True)
 with (OUT/'controller.lock').open('w') as f:
  fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)
  tasks=training_tasks(cfg,cfg['weights'],cfg['seeds'][:1]);slots(tasks)
  if list(OUT.glob('FAILED_*.json')):write(OUT/'FAILED.json',dict(phase='training',failures=[p.name for p in OUT.glob('FAILED_*.json')]));return
  gpu_step('acd_stage23_select.py')
  selected=json.loads((OUT/'selection.json').read_text())['selected']
  if selected['weight']==0:
   write(OUT/'validation_reading_ready.json',dict(selected=selected,panel_inference='not run because validation retained weight zero',training_complete=True));return
  gpu_step('acd_stage23_panel.py')
  # CPU scoring and descriptive follow-ups use the frozen scoring wrapper on Sulaco.
  write(OUT/'cpu_handoff_ready.json',dict(selected=selected,inference_complete=True,score_script='acd_stage23_score.py',host='sulaco',remaining=['CPU scoring','publication','conditional descriptive seed replication','Part3b and derivative descriptive follow-ups']))
if __name__=='__main__':main()
