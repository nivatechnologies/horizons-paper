import subprocess,time,json,shlex
from pathlib import Path
local=Path(__file__).resolve().parent
remote='/home/todd/work/aspen-forecast-decision-20261005/aspen/forecast_decision'
def guard_path(name):return local/'GUARD_STATUS'/(name+'.json')
def ssh(cmd,name=None):
 p=subprocess.Popen(['ssh','sulaco',cmd],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 while p.poll() is None:
  guard=guard_path(name) if name else None
  if guard and guard.exists() and json.loads(guard.read_text()).get('stop_requested',False):
   pattern='selection_worker.py.*--model-name '+name+'$'
   subprocess.run(['ssh','sulaco',"pkill -TERM -f "+shlex.quote(pattern)],capture_output=True)
   p.terminate();p.wait(timeout=10)
   return None
  time.sleep(.25)
 stdout,stderr=p.communicate()
 if p.returncode:print(stderr,flush=True);raise RuntimeError('ssh command failed: '+stderr)
 return stdout
while True:
 for name in ['CNN-cost','CNN-R2','CNN2-cost','CNN2-R2','CNN-roll','CNN-80k','CNN-5k','CNN2-20k','CNN2-roll']:
  input_name='validation2_inputs.npz' if name.startswith('CNN2-') else 'validation_inputs.npz'
  ready=subprocess.run(['ssh','sulaco','test -f '+remote+'/runs/selection_inputs/'+input_name])
  if ready.returncode:continue
  own=local/'runs/training'/name
  guard=local/'GUARD_STATUS'/name/'status.json'
  guard_alt=local/'GUARD_STATUS'/(name+'.json')
  if not guard.exists():guard=guard_alt
  if guard.exists() and not json.loads(guard.read_text()).get('selection_allowed',True):continue
  if name not in ['CNN-cost','CNN-R2','CNN2-cost','CNN2-R2'] and not (own/'final_validation_request.json').exists():continue
  for cp in sorted(own.glob('checkpoint_*.pt')):
   step=cp.stem.split('_')[-1];ack=own/f'validation_{step}.json'
   if ack.exists() or not cp.with_suffix('.json').exists(): continue
   while ssh("pgrep -af '[p]ython campaign.py cnn' || true").strip(): time.sleep(5)
   rd=f'{remote}/runs/selection_checkpoints/{name}'
   ssh('mkdir -p '+shlex.quote(rd))
   subprocess.run(['scp',str(cp),f'sulaco:{rd}/{cp.name}'],check=True)
   args=['aa-exec','-p','chrome','--','/home/todd/.local/bin/bwrap','--ro-bind','/','/','--proc','/proc','--dev-bind','/dev','/dev','--tmpfs','/mnt','--tmpfs','/home','--tmpfs','/tmp','--dir','/tmp/worker','--ro-bind',remote+'/runs/selection_source','/tmp/worker/source','--ro-bind',remote+'/runs/selection_inputs/'+input_name,'/tmp/worker/validation_inputs.npz','--bind',rd,'/tmp/worker/out','--ro-bind','/home/todd/niva-datagen/.venv','/tmp/venv','--unsetenv','PYTHONPATH','--chdir','/tmp/worker/source','--','/tmp/venv/bin/python','selection_worker.py','--checkpoint','/tmp/worker/out/'+cp.name,'--inputs','/tmp/worker/validation_inputs.npz','--output','/tmp/worker/out/'+ack.name,'--microbatch','8']
   args+=['--model-name',name]
   command='flock '+shlex.quote('/home/todd/work/aspen-forecast-decision-20261005/gpu.lock')+' '+shlex.join(args)
   print(name,step,'validation launch',flush=True)
   started=time.clock_gettime(time.CLOCK_BOOTTIME)
   reservation=own/'selection_in_progress.json'
   reservation.write_text(json.dumps(dict(active=True,step=int(step),
        started_local_boottime_seconds=started,launch_boottime_seconds=started,clock_host='baccus',
        bound_label='remote selector command reservation wall upper bound; not measured GPU time'))+'\n')
   worker_stdout=ssh(command,name)
   if worker_stdout is None:
    reservation_tmp=reservation.with_suffix('.tmp')
    reservation_tmp.write_text(json.dumps(dict(active=False,aborted=True,step=int(step),clock_host='baccus',
        launch_boottime_seconds=started,reservation_wall_seconds=time.clock_gettime(time.CLOCK_BOOTTIME)-started,
        actual_selector_gpu_seconds=None,bound_label='remote selector reservation upper bound; GPU timer unavailable after guard stop'))+'\n')
    reservation_tmp.replace(reservation)
    print(name,step,'selector stopped by guard',flush=True);continue
   print(worker_stdout,flush=True)
   reported=[json.loads(line) for line in worker_stdout.splitlines() if line.startswith('{')]
   finished=time.clock_gettime(time.CLOCK_BOOTTIME)
   ack_tmp=ack.with_suffix('.download')
   subprocess.run(['scp',f'sulaco:{rd}/{ack.name}',str(ack_tmp)],check=True)
   subprocess.run(['scp',f'sulaco:{rd}/{ack.with_suffix(".npz").name}',str(ack.with_suffix('.npz'))],check=True)
   raw_ack=json.loads(ack_tmp.read_text());raw_ack['selector_reservation_wall_seconds']=finished-started
   raw_ack['selector_reservation_bound_label']='remote command wall upper bound; not measured GPU time'
   ack_tmp.write_text(json.dumps(raw_ack,indent=2)+'\n')
   if name in ['CNN-R2','CNN2-R2'] and step=='002000':
    zero=json.loads((own/'validation_000000.json').read_text())['charged_gpu_seconds']
    record=json.loads(ack_tmp.read_text());record['checkpoint_validation_gpu_seconds']=record['charged_gpu_seconds'];record['initialization_validation_gpu_seconds']=zero;record['charged_gpu_seconds']+=zero
    ack_tmp.write_text(json.dumps(record,indent=2)+'\n')
   ack_tmp.replace(ack)
   reservation_tmp=reservation.with_suffix('.tmp')
   reservation_tmp.write_text(json.dumps(dict(active=False,step=int(step),clock_host='baccus',
        launch_boottime_seconds=started,started_local_boottime_seconds=started,
        reservation_wall_seconds=finished-started,actual_selector_gpu_seconds=reported[-1]['charged_gpu_seconds'],
        bound_label='remote selector command reservation wall upper bound; not measured GPU time'))+'\n')
   reservation_tmp.replace(reservation)
   subprocess.run(['scp',f'sulaco:{rd}/checkpoint_selection.json',str(own/'selection.json')],check=True)
   decision=json.loads((own/'selection.json').read_text());best=decision['step']
   bestcp=own/f'checkpoint_{best:06d}.pt'
   import shutil
   shutil.copy2(bestcp,own/'selected.pt')
   print(name,step,'selected',best,flush=True)
 time.sleep(5)
