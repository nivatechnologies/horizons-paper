"""Execution-only relocation of frozen Stage21 scoring to sulaco CPU."""
import json,subprocess,time,shlex,fcntl
from pathlib import Path
REMOTE=Path('/home/todd/work/aspen-stage21-scoring-20261008/aspen/determinacy')
PYTHON='/home/todd/work/aspen-determinacy-20261005/.venv/bin/python'
def checked(command):
 while True:
  p=subprocess.run(list(map(str,command)),text=True,capture_output=True)
  if p.returncode==255 or ('connection' in p.stderr.lower() and 'rsync' in str(command[0])):
   print('Sulaco connection retry in 60 seconds',p.stderr,flush=True);time.sleep(60);continue
  if p.returncode:raise RuntimeError(p.stdout+'\n'+p.stderr)
  return p

def install(f):
 def score_unlocked(part,tasks):
  f.ready()
  if (f.OUT/(part+'_pushed.json')).exists():return
  repo=REMOTE.parents[1]
  bundle=Path('/mnt/niva-array/work/aspen-deadline-20261008/stage21-sulaco.bundle')
  checked(['rsync','-a',bundle,'sulaco:'+str(repo/'stage21-sulaco.bundle')])
  checked(['ssh','sulaco','git -C '+str(repo)+' fetch '+str(repo/'stage21-sulaco.bundle')+' refs/remotes/origin/paper/aspen-2026-10-determinacy:refs/remotes/origin/paper/aspen-2026-10-determinacy'])
  # Transfer code/guards and required checkpoints as bytes; no scientific definition changes.
  for pattern in ('*.py','ACD_STAGE21*.md'):
   files=list(f.ROOT.glob(pattern))
   checked(['rsync','-a',*files,'sulaco:'+str(REMOTE)+'/'])
  freezes=list((f.ROOT/'receipts').glob('acd_stage21_freeze*.json'))+[f.ROOT/'receipts/acd_stage21_reorder.json']
  checked(['ssh','sulaco','mkdir -p '+str(REMOTE/'runs/stage21')+' '+str(REMOTE/'receipts')])
  checked(['rsync','-a',*freezes,'sulaco:'+str(REMOTE/'receipts')+'/'])
  for name in ('checkpoints','climatology'):
   checked(['rsync','-a',str(f.OUT/name)+'/','sulaco:'+str(REMOTE/'runs/stage21'/name)+'/'])
  checked(['rsync','-a',*list(f.OUT.glob('*pushed.json')),*list(f.OUT.glob('main_forecast_*.npz')),'sulaco:'+str(REMOTE/'runs/stage21')+'/'])
  checked(['ssh','sulaco','mkdir -p '+str(REMOTE/'runs/stage21/scoring')])
  # Only the existing realized cache is transferred; it is opened solely by frozen.score_actual().
  checked(['rsync','-a',f.OUT/'scoring/actual.npz','sulaco:'+str(REMOTE/'runs/stage21/scoring/actual.npz')])
  for task in tasks:
   name=task['name'];checked(['rsync','-a',str(f.OUT/'inference'/name)+'/','sulaco:'+str(REMOTE/'runs/stage21/inference'/name)+'/'])
  checked(['rsync','-a',f.ROOT/'ACD_STAGE21_READING.md','sulaco:'+str(REMOTE/'ACD_STAGE21_READING.md')])
  runner=Path(__file__).with_name('stage21_sulaco_score_worker.py')
  checked(['rsync','-a',runner,'sulaco:'+str(REMOTE/runner.name)])
  command=shlex.join(['env','ACD_INHERITED_ROOT=/home/todd/work/aspen-forecast-decision-20261005/aspen/forecast_decision','JAX_PLATFORMS=cpu','JAX_ENABLE_X64=true','OPENBLAS_NUM_THREADS=1',PYTHON,str(REMOTE/runner.name),part])
  result=checked(['ssh','sulaco',command]);print(result.stdout,flush=True)
  for name in [f'receipts/acd_stage21_{part}.json','ACD_STAGE21_READING.md',f'runs/stage21/{part}_sulaco_execution.json']:
   checked(['rsync','-a','sulaco:'+str(REMOTE/name),str(f.ROOT/name)])
  f.publish(part,[f'receipts/acd_stage21_{part}.json','ACD_STAGE21_READING.md',f'runs/stage21/{part}_sulaco_execution.json'],True)
 def score(part,tasks):
  with open('/tmp/acd_stage21_scoring.lock','w') as lock:
   fcntl.flock(lock,fcntl.LOCK_EX)
   return score_unlocked(part,tasks)
 f.partial_score=score
