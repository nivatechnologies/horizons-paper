"""Fast-forward Stage21-only publication; no other stage file is staged."""
import json,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[1]
PYTHON='/mnt/niva-array/work/aspen-stage19-env-20261007/bin/python'
BRANCH='paper/aspen-2026-10-determinacy'
def git(*args):return subprocess.check_output(['git','-C',str(REPO),*args],text=True).strip()
def publish(step):
 files=[]
 if step=='contract':files=[p for p in ROOT.glob('acd_stage21_*.py')]+[ROOT/'ACD_STAGE21_PANEL_CONTRACT.md',ROOT/'receipts/acd_stage21_contract.json']
 elif step in ['timing','panel']:
  files=[ROOT/'receipts/acd_stage21_part1.json',ROOT/'ACD_STAGE21_ACCESS.jsonl']
  for pattern in ['observed_*.npz','main_sample_*.npz','main_sample_*.json','main_forecast_*.npz','main_*.json','case_*.json']:
   files+=sorted((ROOT/'runs/stage21').glob(pattern))
 elif step=='climatology':files=[ROOT/'receipts/acd_stage21_climatology.json']+sorted((ROOT/'runs/stage21/climatology').glob('*'))
 else:raise ValueError(step)
 assert files and all(p.exists() for p in files)
 assert all('stage21' in p.name.lower() or str(p).startswith(str(ROOT/'runs/stage21')) for p in files)
 git('config','user.name','Todd');git('config','user.email',git('log','-1','--format=%ae'))
 git('add','-f',*[str(p) for p in files]);git('commit','-m',f'Record Stage21 {step}')
 while True:
  git('fetch','origin',BRANCH)
  p=subprocess.run(['git','-C',str(REPO),'rebase','FETCH_HEAD'])
  if p.returncode:raise RuntimeError('Stage21 rebase requires reconciliation; no other stage modified')
  subprocess.run([PYTHON,str(ROOT/'check_acd.py')],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
  commit=git('rev-parse','HEAD')
  status=ROOT/'ACD_PIPELINE_STATUS.md'
  status.write_text(status.read_text()+f'\nStage21 | {step} | {commit} | {time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())} | No realized-outcome access; Freeze E and emulator/scoring work remain.\n')
  git('add',str(status));git('commit','-m',f'Record Stage21 {step} publication status')
  pushed=subprocess.run(['git','-C',str(REPO),'push','origin','HEAD:'+BRANCH])
  if pushed.returncode==0:break
  time.sleep(60)
 marker=ROOT/'runs/stage21'/f'{step}_pushed.json';marker.parent.mkdir(parents=True,exist_ok=True)
 data=dict(commit=commit,publication=git('rev-parse','HEAD'))
 if step=='contract':
  from acd_stage21_contract import digest
  data['contract_sha256']=digest(ROOT/'ACD_STAGE21_PANEL_CONTRACT.md')
 marker.write_text(json.dumps(data,indent=2)+'\n');print(json.dumps(dict(step=step,**data)),flush=True)
if __name__=='__main__':
 import sys
 publish(sys.argv[1])
