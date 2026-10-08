"""Run the frozen, panel-disjoint Stage18 C data generator on sulaco CPU."""
import fcntl,json,subprocess,time
from pathlib import Path
r=Path('/mnt/niva-array/work/aspen-determinacy-stage19-20261007/aspen/determinacy');o=r/'runs/stage18'
s='/home/todd/work/aspen-determinacy-stage18-20261007/aspen/determinacy';py='/home/todd/work/aspen-determinacy-20261005/.venv/bin/python'
def checked(args):
 while True:
  p=subprocess.run(args)
  if not p.returncode:return
  if p.returncode!=255 and args[0]!='rsync':raise RuntimeError(f'Failed command: {args[0]}, returncode {p.returncode}')
  time.sleep(60)
with open('/tmp/acd_stage18_data_parallel.lock','w') as lock:
 fcntl.flock(lock,fcntl.LOCK_EX)
 if not (o/'C_data_ready_for_commit.json').exists():
  if not (o/'C_implementation_pushed.json').exists():raise RuntimeError('Frozen C implementation must be pushed')
  checked(['ssh','sulaco',f'cd {s} && env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=4 NUMBA_NUM_THREADS=4 {py} -u acd_stage18_data.py > runs/stage18/C_generation.log 2>&1'])
  checked(['rsync','-a',f'sulaco:{s}/runs/stage18/response_data/',str(o/'response_data')+'/'])
  checked(['scp',f'sulaco:{s}/receipts/acd_stage18_response_data.json',str(r/'receipts/acd_stage18_response_data.json')])
  (o/'C_data_ready_for_commit.json').write_text(json.dumps(dict(utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),host='sulaco',training_still_waits_for_D=True))+'\n')
