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
 result=publish(r,'stage21-'+step,files,receipts,marker=f.OUT/(step+'_pushed.json'))
 return result['commit']
def call(args,**kwargs):
 if len(args)>2 and Path(str(args[1])).name=='acd_stage21_priority.py' and str(args[2])=='score':
  args=[args[0],HERE/'acd_deadline_stage21.py',*args[2:]]
 return original_call(args,**kwargs)
original_spark=f.spark
def spark(tasks):
 import time
 while f.remote('test -f /home/todd/work/aspen-stage20-uniform-20261008/E0/queue_complete.json').returncode:time.sleep(60)
 return original_spark(tasks)
f.spark=spark
f.publish=guarded;f.call=call
p=argparse.ArgumentParser();p.add_argument('mode',choices=['controller','score','release_stage18']);p.add_argument('--part');a=p.parse_args()
f.controller() if a.mode=='controller' else f.score_worker(a.part) if a.mode=='score' else f.release_stage18()
