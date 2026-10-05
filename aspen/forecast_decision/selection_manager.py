import subprocess,time,json,shlex
from pathlib import Path
local=Path(__file__).resolve().parent
remote='/home/todd/work/aspen-forecast-decision-20261005/aspen/forecast_decision'
def ssh(cmd):
 p=subprocess.run(['ssh','sulaco',cmd],capture_output=True,text=True)
 if p.returncode: print(p.stderr,flush=True);p.check_returncode()
 return p.stdout
while True:
 for name in ['CNN-cost','CNN-R2','CNN2-cost','CNN2-R2']:
  input_name='validation2_inputs.npz' if name.startswith('CNN2-') else 'validation_inputs.npz'
  ready=subprocess.run(['ssh','sulaco','test -f '+remote+'/runs/selection_inputs/'+input_name])
  if ready.returncode:continue
  own=local/'runs/training'/name
  for cp in sorted(own.glob('checkpoint_*.pt')):
   step=cp.stem.split('_')[-1];ack=own/f'validation_{step}.json'
   if ack.exists() or not cp.with_suffix('.json').exists(): continue
   while ssh("pgrep -af '[p]ython campaign.py cnn' || true").strip(): time.sleep(5)
   rd=f'{remote}/runs/selection_checkpoints/{name}'
   ssh('mkdir -p '+shlex.quote(rd))
   subprocess.run(['scp',str(cp),f'sulaco:{rd}/{cp.name}'],check=True)
   args=['aa-exec','-p','chrome','--','/home/todd/.local/bin/bwrap','--ro-bind','/','/','--proc','/proc','--dev-bind','/dev','/dev','--tmpfs','/mnt','--tmpfs','/home','--tmpfs','/tmp','--dir','/tmp/worker','--ro-bind',remote+'/runs/selection_source','/tmp/worker/source','--ro-bind',remote+'/runs/selection_inputs/'+input_name,'/tmp/worker/validation_inputs.npz','--bind',rd,'/tmp/worker/out','--ro-bind','/home/todd/niva-datagen/.venv','/tmp/venv','--unsetenv','PYTHONPATH','--chdir','/tmp/worker/source','--','/tmp/venv/bin/python','selection_worker.py','--checkpoint','/tmp/worker/out/'+cp.name,'--inputs','/tmp/worker/validation_inputs.npz','--output','/tmp/worker/out/'+ack.name,'--microbatch','8']
   command='flock '+shlex.quote('/home/todd/work/aspen-forecast-decision-20261005/gpu.lock')+' '+shlex.join(args)
   print(name,step,'validation launch',flush=True)
   print(ssh(command),flush=True)
   ack_tmp=ack.with_suffix('.download')
   subprocess.run(['scp',f'sulaco:{rd}/{ack.name}',str(ack_tmp)],check=True)
   subprocess.run(['scp',f'sulaco:{rd}/{ack.with_suffix(".npz").name}',str(ack.with_suffix('.npz'))],check=True)
   if name in ['CNN-R2','CNN2-R2'] and step=='002000':
    zero=json.loads((own/'validation_000000.json').read_text())['charged_gpu_seconds']
    record=json.loads(ack_tmp.read_text());record['checkpoint_validation_gpu_seconds']=record['charged_gpu_seconds'];record['initialization_validation_gpu_seconds']=zero;record['charged_gpu_seconds']+=zero
    ack_tmp.write_text(json.dumps(record,indent=2)+'\n')
   ack_tmp.replace(ack)
   candidates=[(json.loads(x.read_text())['mean_normalized_regret'],int(x.stem.split('_')[-1])) for x in own.glob('validation_*.json')]
   regret,best=min(candidates)
   bestcp=own/f'checkpoint_{best:06d}.pt'
   import shutil
   shutil.copy2(bestcp,own/'selected.pt')
   (own/'selection.json').write_text(json.dumps(dict(step=best,mean_normalized_regret=regret,candidates=len(candidates),selected_at=time.time()),indent=2)+'\n')
   print(name,step,'selected',best,flush=True)
 time.sleep(5)
