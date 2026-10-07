"""Resume Stage 17 B/D only when Stage 15A is committed; no protected run access."""
import os,sys,time,json,base64,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]
PYTHON=sys.executable
BRANCH='paper/aspen-2026-10-determinacy'
UPSTREAM='refs/stage17/upstream'
URL='https://github.com/nivatechnologies/horizons-paper.git'
def main():
 token=sys.stdin.read().strip()
 if not token:raise RuntimeError('Missing authenticated Git credential')
 header='AUTHORIZATION: basic '+base64.b64encode(('oauth2:'+token).encode()).decode()
 def git(*args,**kwargs):return subprocess.check_output(['git','-C',str(REPO),*args],text=True,**kwargs)
 def authgit(*args):subprocess.run(['git','-c','http.extraheader='+header,'-C',str(REPO),*args],check=True)
 while True:
  authgit('fetch',URL,BRANCH+':'+UPSTREAM)
  files=git('ls-tree','-r','--name-only',UPSTREAM).splitlines();candidates=[p for p in files if p.startswith('aspen/determinacy/receipts/') and 'stage15' in p.lower() and p.endswith('.json')]
  ready=any('stage15a' in p.lower() or 'A' in json.loads(git('show',UPSTREAM+':'+p)) for p in candidates)
  if ready:break
  print('Waiting for committed Stage 15A; A/C/E complete. Stage 15D requirement recorded; protected runs untouched.',flush=True)
  time.sleep(60)
 prior=json.loads(git('show',UPSTREAM+':aspen/determinacy/numbers_acd.json'))['numbers']
 # Rebase only this worktree. On conflict, leave a reviewable state; never force push.
 subprocess.run(['git','-C',str(REPO),'rebase',UPSTREAM],check=True)
 env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',NUMBA_NUM_THREADS='4',PYTHONPATH=str(ROOT))
 for script in ['acd_stage17_events.py','acd_stage17_render.py','acd_numbers.py','check_acd.py']:
  subprocess.run([PYTHON,script],cwd=ROOT,env=env,check=True)
 now=json.loads((ROOT/'numbers_acd.json').read_text())['numbers']
 assert all(now.get(k)==v for k,v in prior.items()),'prior registry entry changed'
 paths=['acd_stage17_events.py','receipts/acd_stage17.json','ACD_STAGE17_READING.md','ACD_METHODS_WINDOWS_BETTING.md','figures/F20_transfer_paper.pdf','figures/F20_transfer_paper.png','numbers_acd.json','NUMBERS_ACD.md','acd_numbers.py']
 subprocess.run(['git','-C',str(ROOT),'add','--',*paths],check=True)
 subprocess.run(['git','-C',str(REPO),'-c','user.name=Todd Peterson','-c','user.email=todd@nivatech.io','commit','-m','Complete Stage 17 event scores and response transfer diagnostics'],check=True)
 # Normal push rejects any race; no force option is used.
 authgit('push',URL,'HEAD:refs/heads/'+BRANCH)
 print('Stage 17 complete '+git('rev-parse','HEAD').strip(),flush=True)
if __name__=='__main__':main()
