import sys,argparse
from pathlib import Path
r=Path('/mnt/niva-array/work/aspen-determinacy-stage21-20261008/aspen/determinacy')
sys.path.insert(0,'/mnt/niva-array/work/aspen-determinacy-stage19-l3-20261008/aspen/determinacy');sys.path.insert(0,str(r))
from acd_guarded_publish import publish
import acd_stage21_priority as f
original_call=f.call
HERE=Path(__file__).resolve().parent
prefixes={'reference':'ACD_21REF','R12':'ACD_21R12','R34':'ACD_21R34','descriptive':'ACD_21DESC'}
def guarded(step,files,registered=False):
 receipts=[(f'receipts/acd_stage21_{step}.json',prefixes[step])] if registered else []
 import importlib,acd_guarded_publish
 importlib.reload(acd_guarded_publish)
 result=acd_guarded_publish.publish(r,'stage21-'+step,files,receipts,marker=f.OUT/(step+'_pushed.json'))
 return result['commit']
def call(args,**kwargs):
 if len(args)>2 and Path(str(args[1])).name=='acd_stage21_priority.py' and str(args[2])=='score':
  args=[args[0],HERE/'acd_deadline_stage21.py',*args[2:]]
 return original_call(args,**kwargs)
from acd_deadline_stage21_strict import install
validate=install(f)
original_spark=f.spark
def spark(tasks):
 import time
 while f.remote('test -f /home/todd/work/aspen-stage20-uniform-20261008/E0/queue_complete.json').returncode:time.sleep(60)
 return original_spark(tasks)
f.spark=spark
from acd_deadline_stage21_multispark import install as install_multispark
install_multispark(f,validate)
from acd_deadline_stage21_sulaco_score import install as install_sulaco_score
install_sulaco_score(f)
f.publish=guarded;f.call=call
original_baccus=f.baccus
def baccus(tasks,phase):
 if phase!='descriptive':return original_baccus(tasks,phase)
 import fcntl
 with open('/tmp/acd_stage21_descriptive_inference.lock','w') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  return original_baccus(tasks,phase)
f.baccus=baccus
p=argparse.ArgumentParser();p.add_argument('mode',choices=['controller','score','release_stage18','descriptive_parallel']);p.add_argument('--part');a=p.parse_args()
def remaining_controller():
 d=f.ready();a,b,c=f.phases(d)
 failed=f.OUT/'R12_inference_complete.json'
 import json
 if failed.exists() and json.loads(failed.read_text()).get('failed'):
  import time
  while not (f.OUT/'R12_recovery_complete.json').exists():time.sleep(60)
  validate('R12_recovery',a)
  started=f.OUT/'spark_started.json'
  if started.exists() and not (f.OUT/'multispark_execution_pushed.json').exists():
   pid=json.loads(started.read_text())['pid'];f.remote('kill -CONT '+str(pid))
  f.spark(b);f.call([f.PY,HERE/'acd_deadline_stage21.py','score','--part','R34'],cwd=r)
  f.baccus(c,'descriptive')
  from acd_stage21_inference import complete
  (f.OUT/'inference_complete.json').write_text(json.dumps(dict(completed=[x['name'] for x in d['tasks'] if complete(x['name'])],failed=[x['name'] for x in d['tasks'] if not complete(x['name'])]))+'\n')
  f.call([f.PY,HERE/'acd_deadline_stage21.py','score','--part','descriptive'],cwd=r)
 else:f.controller()
def release():
 import time
 while not (f.OUT/'descriptive_pushed.json').exists():time.sleep(60)
 first,second,third=f.phases(f.ready())
 validate('R12_recovery',first);validate('descriptive',third)
 import json,time
 (f.OUT/'Stage18_released.json').write_text(json.dumps(dict(utc=time.time(),criteria_changed=False,R34_runs_in_parallel_on_Sparks=True))+'\n')
 stage18=f.BASE/'runs/stage18'
 if not (stage18/'B_pushed.json').exists():raise RuntimeError('Stage18 B publication required')
 f.call([f.PY,'-u',HERE/'acd_stage18_after_B.py'],cwd=f.BASE)
def score():
 tasks=dict(zip(('R12','R34','descriptive'),f.phases(f.ready())))[a.part]
 validate('R12_recovery' if a.part=='R12' else a.part,tasks)
 f.score_worker(a.part)
def descriptive_parallel():
 if not (f.OUT/'parallel_descriptive_execution_pushed.json').exists():raise RuntimeError('Parallel execution note must be pushed before dispatch')
 if not (f.OUT/'R12_recovery_complete.json').exists():raise RuntimeError('R12 must finish first')
 first,second,tasks=f.phases(f.ready())
 validate('R12_recovery',first)
 f.baccus(tasks,'descriptive')
 f.call([f.PY,HERE/'acd_deadline_stage21.py','score','--part','descriptive'],cwd=r)

remaining_controller() if a.mode=='controller' else score() if a.mode=='score' else descriptive_parallel() if a.mode=='descriptive_parallel' else release()
