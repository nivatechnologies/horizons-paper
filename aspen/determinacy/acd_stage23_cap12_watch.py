"""Apply the one-run cap amendment without interrupting other GPU jobs."""
from acd_stage23_common import *
import subprocess,time
sys.path.insert(0,str(FROZEN18))

def main():
 cfg=ready();amend=json.loads((ROOT/'receipts/acd_stage23_cap_amendment.json').read_text());model=amend['model'];directory=OUT/'training'/model;complete=directory/'complete.json'
 if (OUT/'cap12_completed.json').exists():return
 initial=directory/'complete_initial_cap.json'
 while not complete.exists() and not initial.exists():time.sleep(30)
 if complete.exists() and json.loads(complete.read_text()).get('cap_seconds')==amend['new_cap_seconds']:
  write(OUT/'cap12_completed.json',dict(model=model,status='Resumed watcher found completed authorized continuation',final=json.loads(complete.read_text())));return
 previous=json.loads((initial if initial.exists() else complete).read_text())
 if previous.get('abort') or previous.get('step',0)>=20000 or not previous.get('capped'):
  write(OUT/'cap12_completed.json',dict(model=model,status='No continuation: frozen guard abort or completed schedule',previous=previous));return
 # Let the original serving lease finish before acquiring a second lease for the same run.
 while any(json.loads(p.read_text()).get('model')==model for p in OUT.glob('active_gpu_*.json')):time.sleep(5)
 resume=directory/'resume.pt'
 if not resume.exists():raise RuntimeError('No frozen resumable scheduled checkpoint')
 import torch
 saved=torch.load(resume,map_location='cpu',weights_only=False);step=saved['step'];del saved
 record=dict(model=model,previous_terminal_step=previous['step'],resumed_checkpoint_step=step,unsaved_updates_replayed=previous['step']-step,previous_charged_gpu_seconds=previous['charged_gpu_seconds'],resume_sha256=digest(resume),criteria_unchanged=True,budget_changed=True)
 write(OUT/'cap12_resume_record.json',record)
 if complete.exists() and not initial.exists():complete.rename(initial)
 # Existing completed metadata is retained and all time remains charged by the frozen Charge class.
 import acd_stage18_gpu_lease as lease
 from acd_stage19_part2_gate import gpu_inventory
 lease.OUT=OUT;lease.freeze_ready=ready
 while True:
  cards=[c for c in gpu_inventory() if all('VLLM' in p['process'].upper() for p in c['processes'])]
  if cards:break
  time.sleep(60)
 original_index=amend['original_gpu_index'];card=next((c for c in cards if c['index']==original_index),cards[0]);seed=cfg['seeds'][0]
 with lease.lease(card['index']) as actual:
  env=dict(os.environ,CUDA_VISIBLE_DEVICES=actual['uuid'],OMP_NUM_THREADS='4',OPENBLAS_NUM_THREADS='4')
  args=[GPU,'-u',str(ROOT/'acd_stage23_cap12_train.py'),'--name',model,'--data',str(FROZEN18/'runs/stage18/response_data'),'--out',str(directory),'--micro','128','--torch-seed',str(seed['torch_seed']),'--batch-seed',str(seed['batch_seed']),'--response-weight',str(amend['weight'])]
  with (OUT/'task_logs'/'cap12_resume.log').open('a') as log:result=subprocess.run(args,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT)
 row=dict(returncode=result.returncode,complete=complete.exists(),gpu=actual,resume_record=record,utc=time.time());write(OUT/'task_logs/cap12_resume.json',row)
 if result.returncode or not complete.exists():write(OUT/'cap12_FAILED.json',row);raise RuntimeError('Authorized budget continuation failed')
 final=json.loads(complete.read_text());assert final['cap_seconds']==amend['new_cap_seconds']
 row.update(final=final);write(OUT/'cap12_completed.json',row)
 # Correct the operational completion metadata to the final result; retain the first-cap record separately.
 outcomes=OUT/'training_outcomes.json'
 if outcomes.exists():
  d=json.loads(outcomes.read_text());d[model]['cap_continuation']=row;d[model]['selected_step']=final['selected_step'];write(outcomes,d)
if __name__=='__main__':
 try:main()
 except Exception as e:write(OUT/'cap12_FAILED.json',dict(reason=str(e),utc=time.time()));raise
