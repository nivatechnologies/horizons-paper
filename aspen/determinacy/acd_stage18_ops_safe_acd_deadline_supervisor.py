"""Restart exited continuations without preempting jobs or changing frozen criteria."""
import json,os,shutil,subprocess,time,traceback
from pathlib import Path
HOME=Path(__file__).resolve().parent
SCI=Path('/mnt/niva-array/work/aspen-determinacy-stage19-20261007/aspen/determinacy')
CPU='/mnt/niva-array/work/aspen-stage19-env-20261007/bin/python';GPU='/mnt/niva-array/niva-platform/.venv-cu130/bin/python'
ENV=dict(os.environ,ACD_INHERITED_ROOT='/mnt/niva-array/work/aspen-forecast-decision-20261005/aspen/forecast_decision',OMP_NUM_THREADS='4',OPENBLAS_NUM_THREADS='1',NUMBA_NUM_THREADS='4')
LOGS=HOME/'logs';LOGS.mkdir(exist_ok=True);jobs={};last_restart={}
def processes():
 result=[]
 for p in Path('/proc').iterdir():
  if not p.name.isdigit():continue
  try:args=(p/'cmdline').read_bytes().decode().split('\0')
  except (OSError,UnicodeError):continue
  result.append((int(p.name),args))
 return result
def alive(script,mode=None):
 for pid,args in processes():
  if pid==os.getpid():continue
  if any(Path(s).name==script for s in args if s) and (mode is None or mode in args):return pid
 return None
def ensure(key,script,python,mode=None,cwd=None,args=()):
 pid=alive(Path(script).name,mode)
 if pid:return dict(status='running',pid=pid)
 if time.monotonic()-last_restart.get(key,-1000)<60:return dict(status='retry_wait')
 last_restart[key]=time.monotonic();f=(LOGS/(key+'.log')).open('a');command=[python,'-u',str(script)]+([mode] if mode else [])+list(args)
 p=subprocess.Popen(command,cwd=cwd or SCI,env=ENV,stdin=subprocess.DEVNULL,stdout=f,stderr=subprocess.STDOUT,start_new_session=True);f.close();jobs[key]=p
 return dict(status='launched',pid=p.pid,utc=time.time())
def remote_queues():
 specs=[('192.168.88.12','C',Path('/home/todd/work/aspen-stage20-20261008'),'acd_stage20_queue.py'),('192.168.88.4','E0',Path('/home/todd/work/aspen-stage20-uniform-20261008'),'acd_stage20_uniform_queue.py'),('192.168.88.12','E1',Path('/home/todd/work/aspen-stage20-uniform-20261008'),'acd_stage20_uniform_queue.py')]
 result={}
 for host,part,root,script in specs:
  if part!='C' and not (SCI/'runs/stage20_uniform'/f'{part}_started.json').exists():continue
  command=f"test -f {root}/{part}/queue_complete.json && echo COMPLETE || (pgrep -af '^python3 -u {root}/code/{script} {part}$')"
  p=subprocess.run(['ssh','-o','BatchMode=yes','-o','ConnectTimeout=10',host,command],text=True,capture_output=True,timeout=20)
  result[host+':'+part]=dict(returncode=p.returncode,status=p.stdout.strip())
  if p.returncode or 'COMPLETE' in p.stdout:continue
  # pgrep can match its own shell; validate a numeric PID whose command starts python.
  active=any('python3 -u '+str(root)+'/code/'+script+' '+part in line and 'bash -c' not in line and 'pgrep' not in line for line in p.stdout.splitlines())
  if not active:
   q=subprocess.run(['ssh','-o','BatchMode=yes','-o','ConnectTimeout=10',host,f'nohup python3 -u {root}/code/{script} {part} >> {root}/{part}/queue.log 2>&1 < /dev/null &'],capture_output=True,text=True,timeout=20)
   result[host+':'+part]['restart_returncode']=q.returncode
 shift=Path('/mnt/niva-array/work/aspen-determinacy-stage21-20261008/aspen/determinacy/runs/stage21')
 if (shift/'spark_started.json').exists() and not (shift/'R34_inference_complete.json').exists() and not (shift/'multispark_execution_pushed.json').exists():
  host='192.168.88.4';root='/home/todd/work/aspen-stage21-20261008'
  command=f"test -f {root}/queue_complete.json && echo COMPLETE || pgrep -af '^python3 -u {root}/code/acd_stage21_spark.py queue$'"
  p=subprocess.run(['ssh','-o','BatchMode=yes','-o','ConnectTimeout=10',host,command],capture_output=True,text=True,timeout=20)
  result['Stage21-Spark']=dict(returncode=p.returncode,status=p.stdout.strip())
  if p.returncode==1 and not p.stdout.strip():
   subprocess.run(['ssh',host,f'nohup python3 -u {root}/code/acd_stage21_spark.py queue >> {root}/queue.log 2>&1 < /dev/null &'],timeout=20,check=True)
 return result
while True:
 snapshot={'utc':time.time(),'jobs':{}}
 try:
  # Keep the existing deferred Stage18 script available across a reboot.
  if not Path('/tmp/acd_stage18_after_B.py').exists():shutil.copy2(HOME/'acd_stage18_after_B.py','/tmp/acd_stage18_after_B.py')
  fresh=SCI/'runs/stage19';repair=fresh/'part3b';twenty=SCI/'runs/stage20';uniform=SCI/'runs/stage20_uniform';eighteen=SCI/'runs/stage18';shift=Path('/mnt/niva-array/work/aspen-determinacy-stage21-20261008/aspen/determinacy/runs/stage21')
  if not (fresh/'L3_pushed.json').exists():snapshot['jobs']['L3']='Awaiting scored receipt publication; see dedicated L3 publisher log'
  if not (repair/'inference_ready.json').exists():snapshot['jobs']['Part3b_inference']=ensure('part3b-inference',SCI/'acd_stage19_part3b_inference.py',GPU,'controller')
  elif not (repair/'scoring_ready_for_publication.json').exists() and not alive('acd_stage19_part3b_inference.py','controller') and not alive('acd_stage19_part3b_score.py'):snapshot['jobs']['Part3b_score']=ensure('part3b-score',HOME/'acd_deadline_part3b_score.py',CPU)
  if not (repair/'published.json').exists():snapshot['jobs']['Part3b_publish']=ensure('part3b-publish',HOME/'acd_deadline_part3b_publish.py',CPU)
  if not (twenty/'C_published.json').exists():snapshot['jobs']['Stage20C']=ensure('stage20-C',HOME/'acd_deadline_stage20.py',GPU,cwd=Path('/mnt/niva-array/work/aspen-determinacy-stage20-20261008/aspen/determinacy'))
  if not (uniform/'published.json').exists():snapshot['jobs']['Stage20_uniform']=ensure('stage20-uniform',HOME/'acd_deadline_uniform.py',GPU,cwd=Path('/mnt/niva-array/work/aspen-determinacy-stage20-20261008/aspen/determinacy'))
  if (shift/'R12_inference_complete.json').exists() and not (shift/'R12_recovery_complete.json').exists():
   prior=json.loads((shift/'R12_inference_complete.json').read_text())
   if prior.get('failed'):snapshot['jobs']['Stage21_R12_recovery']=ensure('stage21-R12-recovery',HOME/'acd_deadline_stage21_R12_recovery.py',CPU,cwd=shift.parents[1])
  if (shift/'parallel_descriptive_execution_pushed.json').exists() and not (shift/'descriptive_pushed.json').exists():snapshot['jobs']['Stage21_descriptive_parallel']=ensure('stage21-descriptive-parallel',HOME/'acd_deadline_stage21.py',CPU,'descriptive_parallel',cwd=shift.parents[1])
  if not all((shift/n).exists() for n in ('R34_pushed.json','descriptive_pushed.json')):snapshot['jobs']['Stage21']=ensure('stage21',HOME/'acd_deadline_stage21.py',CPU,'controller',cwd=shift.parents[1])
  if (HOME/'stage18_safe_handoff_pushed.json').exists() and not (eighteen/'safe_handoff.json').exists():snapshot['jobs']['Stage18_safe_handoff']=ensure('stage18-safe-handoff',HOME/'acd_stage18_safe_handoff.py',CPU)
  if not (eighteen/'C_implementation_pushed.json').exists():snapshot['jobs']['Stage18_prepare']=ensure('stage18-prepare',HOME/'acd_deadline_stage18_prepare.py',CPU)
  if not (eighteen/'D_reading_ready.json').exists() and not alive('acd_stage18_after_B.py'):snapshot['jobs']['Stage18_after21']=ensure('stage18-release',HOME/'acd_deadline_stage21.py',CPU,'release_stage18',cwd=shift.parents[1])
  if (eighteen/'D_reading_ready.json').exists() and not (eighteen/'D_pushed.json').exists():snapshot['jobs']['Stage18D_publish']=ensure('stage18-D-publish',HOME/'acd_deadline_stage18_publish.py',CPU,'D')
  if (eighteen/'C_data_ready_for_commit.json').exists() and not (eighteen/'response_data/generation_pushed.json').exists():snapshot['jobs']['Stage18C_data_publish']=ensure('stage18-C-data',HOME/'acd_deadline_stage18_publish.py',CPU,'data')
  if (eighteen/'D_pushed.json').exists() and (eighteen/'response_data/generation_pushed.json').exists() and not (eighteen/'C_reading_ready.json').exists():snapshot['jobs']['Stage18C_train']=ensure('stage18-C-train',SCI/'acd_stage18_response_controller.py',GPU)
  if (eighteen/'C_reading_ready.json').exists() and not (eighteen/'C_pushed.json').exists():snapshot['jobs']['Stage18C_publish']=ensure('stage18-C-publish',HOME/'acd_deadline_stage18_publish.py',GPU,'C')
  if (eighteen/'C_pushed.json').exists() and not (eighteen/'D_selected_pushed.json').exists():snapshot['jobs']['Stage18_selected_derivative']=ensure('stage18-selected-D',HOME/'acd_deadline_stage18_selected_derivative.py',GPU)
  if (shift/'parallel_descriptive_execution_pushed.json').exists() and not (eighteen/'C_data_ready_for_commit.json').exists():snapshot['jobs']['Stage18C_CPU_prepare']=ensure('stage18-C-CPU-prepare',HOME/'acd_deadline_stage18_data_parallel.py',CPU)
  if not (HOME/'stage16_aggregate_pushed.json').exists():snapshot['jobs']['Stage16_aggregate']=ensure('stage16-aggregate',HOME/'publish_stage16_aggregate.py',CPU)
  snapshot['remote_queues']=remote_queues()
 except Exception:snapshot['failure']=traceback.format_exc();print(snapshot['failure'],flush=True)
 pending=HOME/'status.tmp.json';pending.write_text(json.dumps(snapshot,indent=2)+'\n');pending.replace(HOME/'status.json')
 time.sleep(60)
