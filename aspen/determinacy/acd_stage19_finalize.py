"""Stage19-only receipt commit after the blind runner ends; fast-forward push only."""
from pathlib import Path
import os,time,json,subprocess,sys
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[1];OUT=ROOT/'runs/stage19'
def git(*args):return subprocess.check_output(['git',*args],cwd=REPO,text=True).strip()
def check():subprocess.run([sys.executable,str(ROOT/'check_acd.py')],cwd=ROOT,check=True)
def finish(pid):
 while Path(f'/proc/{pid}').exists():
  if Path(f'/proc/{pid}/stat').read_text().split()[2]=='Z':break
  time.sleep(30)
 path=ROOT/'receipts/acd_stage19_part1.json'
 if not path.exists():
  path.write_text(json.dumps(dict(stage='19 Part1',status='runner_failed_before_timing_receipt',runner_log='/tmp/acd_stage19_part1.log',realized_outcome_accesses=[],emulator_runs=[]),indent=2)+'\n')
 data=json.loads(path.read_text());status=data['status']
 if status not in ['blind_sampling_complete','timing_gate_stopped']:
  data['status']='runner_failed_resumable';data['failure_log']='/tmp/acd_stage19_part1.log';path.write_text(json.dumps(data,indent=2)+'\n')
 access=ROOT/'ACD_STAGE19_ACCESS.jsonl';access.write_text(''.join(p.read_text() for p in sorted(OUT.glob('access_*.jsonl'))))
 md='# Stage 19 Part1 status\n\n'+json.dumps({'status':data['status'],'timing_projection':data.get('timing_projection'),'gates':data.get('gates'),'wall_seconds':data.get('wall_seconds'),'realized_outcome_accesses':data['realized_outcome_accesses'],'emulator_runs':data['emulator_runs']},indent=2)+'\n\nStep0 passed. Known-forcing contract is frozen independently of the pending Stage15C commit. Comparison with Stage15C remains pending; its implementation will not change this contract.\n'
 (ROOT/'ACD_STAGE19_STATUS.md').write_text(md)
 check()
 paths=['aspen/determinacy/'+n for n in ['acd_stage19_finalize.py','receipts/acd_stage19_part1.json','ACD_STAGE19_ACCESS.jsonl','ACD_STAGE19_STATUS.md']]
 subprocess.run(['git','add','--',*paths],cwd=REPO,check=True)
 subprocess.run(['git','-c','user.name=Todd Peterson','-c','user.email=todd@nivatech.io','commit','-m','Record Stage 19 blind panel timing and sampling outcomes'],cwd=REPO,check=True)
 for retry in range(5):
  subprocess.run(['git','fetch','origin','paper/aspen-2026-10-determinacy'],cwd=REPO,check=True)
  subprocess.run(['git','rebase','FETCH_HEAD'],cwd=REPO,check=True);check()
  p=subprocess.run(['git','push','origin','HEAD:paper/aspen-2026-10-determinacy'],cwd=REPO)
  if p.returncode==0:
   (OUT/'final_commit.txt').write_text(git('rev-parse','HEAD')+'\n');return
 raise RuntimeError('Remote changed repeatedly; no force push attempted')
if __name__=='__main__':finish(int(sys.argv[1]))
