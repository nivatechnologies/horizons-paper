"""Publish only Stage22 panel paths and start the blind pilot after its contract."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,time
r=Path('/mnt/niva-array/work/aspen-determinacy-stage22-20261010/aspen/determinacy');o=r/'runs/stage22'
dest='/home/todd/work/aspen-stage22-panel-20261010'
sys.path.insert(0,'/mnt/niva-array/work/aspen-determinacy-stage19-l3-20261008/aspen/determinacy')
from acd_guarded_publish import publish

def network(args):
 while subprocess.run(list(map(str,args))).returncode:time.sleep(60)
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def upload():
 network(['ssh','sulaco','mkdir','-p',dest])
 files=['acd_stage22_adapter.py','acd_stage22_panel.py','ACD_STAGE22_FREEZE_F.md','receipts/acd_stage22_freeze_f.json','runs/stage22/freeze_f_pushed.json']
 for name in files:
  network(['ssh','sulaco','mkdir','-p',str(Path(dest)/Path(name).parent)])
  network(['scp',r/name,'sulaco:'+str(Path(dest)/name)])
 network(['rsync','-a',str(r/'stage22_parameterized')+'/',f'sulaco:{dest}/stage22_parameterized/'])

def execution():
 assert (o/'freeze_f_pushed.json').exists()
 if not (o/'panel_launcher_pushed.json').exists():
  d=dict(panel_launcher_sha256=digest(r/'acd_stage22_panel.py'),publisher_sha256=digest(r/'acd_stage22_panel_publish.py'),
         purpose='Panel paths and fresh namespaces; unchanged count-parameterized Stage21 blind sampler. Criteria unchanged.',
         case_count_source='receipts/acd_stage22_freeze_f.json $.N',
         source_freeze_commit=json.loads((o/'freeze_f_pushed.json').read_text())['commit'],realized_outcome_accesses=[])
  (r/'receipts/acd_stage22_panel_launcher.json').write_text(json.dumps(d,indent=2)+'\n')
  p=r/'ACD_STAGE22_FREEZE_F.md'
  p.write_text(p.read_text()+'\n## Panel-launcher execution record\n\nCriteria unchanged. No sampling or outcome access preceded this record.\n\n```json\n'+json.dumps(d,indent=2)+'\n```\n')
  publish(r,'stage22-panel-launcher',['acd_stage22_panel.py','acd_stage22_panel_publish.py','receipts/acd_stage22_panel_launcher.json','ACD_STAGE22_FREEZE_F.md'],
          marker=o/'panel_launcher_pushed.json',status_message='Stage22 panel-path/namespace launcher hashed before sampling; panel contract next; criteria unchanged.')
 upload()
 env=f'env ACD_STAGE22_BASE=/home/todd/work/aspen-stage21-scoring-20261008/aspen/determinacy ACD_INHERITED_ROOT=/home/todd/work/aspen-forecast-decision-20261005/aspen/forecast_decision ACD_STAGE21_PRIOR_CONF=/home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf'
 network(['ssh','sulaco',f'cd {dest} && {env} /home/todd/work/aspen-determinacy-20261005/.venv/bin/python -u acd_stage22_panel.py contract'])
 network(['scp',f'sulaco:{dest}/ACD_STAGE22_PANEL_CONTRACT.md',r/'ACD_STAGE22_PANEL_CONTRACT.md'])
 network(['scp',f'sulaco:{dest}/receipts/acd_stage22_panel_contract.json',r/'receipts/acd_stage22_panel_contract.json'])
 if not (o/'panel_contract_pushed.json').exists():
  publish(r,'stage22-panel-contract',['ACD_STAGE22_PANEL_CONTRACT.md','receipts/acd_stage22_panel_contract.json'],marker=o/'panel_contract_pushed.json',
          status_message='Stage22 blind contract pushed; exact software verified; starting first-five cost pilot on sulaco CPU, no realized outcomes.')
 network(['scp',o/'panel_contract_pushed.json',f'sulaco:{dest}/runs/stage22/panel_contract_pushed.json'])
 network(['ssh','sulaco',f'systemd-run --user --unit=aspen-stage22-blind --property=WorkingDirectory={dest} --property=StandardOutput=append:{dest}/blind.log --property=StandardError=append:{dest}/blind.log {env} /home/todd/work/aspen-determinacy-20261005/.venv/bin/python -u {dest}/acd_stage22_panel.py run'])
 (o/'blind_started.json').write_text(json.dumps(dict(host='sulaco',unit='aspen-stage22-blind.service',utc=time.time()))+'\n')

def result(step):
 assert step in ['timing','panel']
 network(['rsync','-a',f'sulaco:{dest}/receipts/acd_stage22_part1.json',str(r/'receipts')+'/'])
 network(['scp',f'sulaco:{dest}/ACD_STAGE21_ACCESS.jsonl',r/'ACD_STAGE22_ACCESS.jsonl'])
 network(['rsync','-a','--exclude','hidden/',f'sulaco:{dest}/runs/stage22/',str(o)+'/'])
 d=json.loads((r/'receipts/acd_stage22_part1.json').read_text())
 assert d['realized_outcome_accesses']==[]
 expected=5 if step=='timing' else json.loads((r/'receipts/acd_stage22_freeze_f.json').read_text())['N']
 assert len(d['cases'])==expected
 files=['receipts/acd_stage22_part1.json','ACD_STAGE22_ACCESS.jsonl']
 for row in d['cases']:
  assert digest(r/row['observations']['path'])==row['observations']['sha256']
  files.append(row['observations']['path'])
  for report in row['arms'].values():
   for name,h in report['files'].items():assert digest(r/name)==h;files.append(name)
 files+= [str(p.relative_to(r)) for p in o.glob('worker_*.log')]
 status='Stage22 first-five timing gate '+('PASS; blind sampling continues.' if d['timing_projection']['passed'] else 'FAILED; no further cases authorized.') if step=='timing' else 'Stage22 blind assigned panel complete and hashed; inference next, scoring blocked until every required task completes.'
 publish(r,'stage22-'+step,sorted(set(files)),marker=o/(step+'_pushed.json'),status_message=status)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('step',choices=['execution','timing','panel']);a=p.parse_args()
 try:execution() if a.step=='execution' else result(a.step)
 except AssertionError:
  import traceback
  (o/'publication_assertion_failure.log').write_text(traceback.format_exc());sys.exit(42)
