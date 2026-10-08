"""Durable Stage21 coordinator; blind CPU steps precede frozen, queued inference."""
import json,os,subprocess,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[1];OUT=ROOT/'runs/stage21'
BASE=Path('/mnt/niva-array/work/aspen-determinacy-stage19-20261007/aspen/determinacy')
PY='/mnt/niva-array/work/aspen-stage19-env-20261007/bin/python';GPU='/mnt/niva-array/niva-platform/.venv-cu130/bin/python'
BRANCH='paper/aspen-2026-10-determinacy'
def call(*cmd,**kw):return subprocess.run(list(map(str,cmd)),check=True,**kw)
def git(*cmd):return subprocess.check_output(['git','-C',str(REPO),*cmd],text=True).strip()
def push(step,files):
 git('add','-f',*[str(ROOT/p) for p in files]);git('commit','-m',f'Record Stage21 {step}')
 while True:
  git('fetch','origin',BRANCH);git('rebase','FETCH_HEAD')
  call(PY,ROOT/'check_acd.py',cwd=ROOT,stdout=subprocess.DEVNULL)
  commit=git('rev-parse','HEAD');p=ROOT/'ACD_PIPELINE_STATUS.md'
  p.write_text(p.read_text()+f'\nStage21 | {step} | {commit} | {time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())} | See Stage21 receipts; prior queues remain unchanged.\n')
  git('add',str(p));git('commit','-m',f'Record Stage21 {step} pipeline status')
  if subprocess.run(['git','-C',str(REPO),'push','origin','HEAD:'+BRANCH]).returncode==0:break
  time.sleep(60)
 return commit

def registry():
 primary=json.loads((ROOT/'numbers_acd.json').read_text())
 before={k:v['value'] for k,v in primary['numbers'].items()}
 for name in primary.get('additional_registries',[]):before.update({k:v['value'] for k,v in json.loads((ROOT/name).read_text())['numbers'].items()})
 p=ROOT/'acd_numbers.py';s=p.read_text()
 for name,prefix in [('acd_stage21_summary.json','ACD_21S'),('acd_stage21_climatology.json','ACD_21N'),('acd_stage21.json','ACD_21')]:
  line=f"    stage13_receipts.append(('receipts/{name}', '{prefix}'))\n"
  if line not in s:s=s.replace('    for filename,prefix in stage13_receipts:',line+'    for filename,prefix in stage13_receipts:')
 marker="omit=('source_hashes','code_hashes','reproduction_checks','invalid_cases') if filename.endswith('acd_stage20_A.json') else "
 add="omit=('source_hashes','code_hashes','records','case_records','case_indices','case_mean_differences','per_seed') if 'acd_stage21' in filename else ('source_hashes','code_hashes','reproduction_checks','invalid_cases') if filename.endswith('acd_stage20_A.json') else "
 s=s.replace(marker,add)
 old="    d=build();(ROOT/'numbers_acd.json').write_text(json.dumps(d,separators=(',', ':'),allow_nan=False)+'\\n');(ROOT/'NUMBERS_ACD.md').write_text(render(d));print('NUMBERS',len(d['numbers']))"
 new="""    d=build()
    stage21={k:v for k,v in d['numbers'].items() if k.startswith('ACD_21')}
    core={k:v for k,v in d['numbers'].items() if not k.startswith('ACD_21')}
    primary=dict(d,numbers=core,additional_registries=['numbers_acd_stage21.json'])
    supplemental=dict(schema=d['schema'],source_hashes={k:v for k,v in d['source_hashes'].items() if 'stage21' in k},numbers=stage21)
    (ROOT/'numbers_acd.json').write_text(json.dumps(primary,separators=(',', ':'),allow_nan=False)+'\\n')
    (ROOT/'numbers_acd_stage21.json').write_text(json.dumps(supplemental,separators=(',', ':'),allow_nan=False)+'\\n')
    (ROOT/'NUMBERS_ACD.md').write_text(render(dict(d,numbers=core)))
    (ROOT/'NUMBERS_ACD_STAGE21.md').write_text(render(supplemental))
    print('NUMBERS',len(d['numbers']))"""
 if old in s:s=s.replace(old,new)
 p.write_text(s)
 p=ROOT/'check_acd.py';s=p.read_text()
 old="    if not (ROOT/'numbers_acd.json').exists() or json.loads((ROOT/'numbers_acd.json').read_text())!=expected:errors.append('numbers_acd.json differs from regenerated receipts')\n    if not (ROOT/'NUMBERS_ACD.md').exists() or (ROOT/'NUMBERS_ACD.md').read_text()!=render(expected):errors.append('NUMBERS_ACD.md differs from regenerated receipts')"
 new="""    primary=json.loads((ROOT/'numbers_acd.json').read_text())
    loaded=dict(primary);loaded['numbers']=dict(primary['numbers'])
    shards=loaded.pop('additional_registries',[])
    for name in shards:
        supplemental=json.loads((ROOT/name).read_text())
        if set(loaded['numbers'])&set(supplemental['numbers']):errors.append('Duplicate supplemental registry keys')
        loaded['numbers'].update(supplemental['numbers'])
        markdown=ROOT/'NUMBERS_ACD_STAGE21.md'
        if not markdown.exists() or markdown.read_text()!=render(supplemental):errors.append('Supplemental registry Markdown differs')
    if loaded!=expected:errors.append('Receipt registries differ from regenerated receipts')
    if not (ROOT/'NUMBERS_ACD.md').exists() or (ROOT/'NUMBERS_ACD.md').read_text()!=render(primary):errors.append('NUMBERS_ACD.md differs from regenerated receipts')"""
 if old in s:s=s.replace(old,new)
 p.write_text(s)
 call(PY,ROOT/'acd_numbers.py',cwd=ROOT)
 # Reload the modified generator in a clean process for exact prior-value comparison.
 snapshot=OUT/'prior_registry_values.json';snapshot.write_text(json.dumps(before,separators=(',',':')))
 code="import json;from acd_numbers import build;from pathlib import Path;p=Path('runs/stage21/prior_registry_values.json');a=json.loads(p.read_text());b=build()['numbers'];assert all(k in b and b[k]['value']==v for k,v in a.items());print('Prior values unchanged',len(a),'combined keys',len(b))"
 call(PY,'-c',code,cwd=ROOT);call(PY,ROOT/'check_acd.py',cwd=ROOT)
 return ['acd_numbers.py','check_acd.py','numbers_acd.json','numbers_acd_stage21.json','NUMBERS_ACD.md','NUMBERS_ACD_STAGE21.md']

def main():
 while not (OUT/'panel_pushed.json').exists():time.sleep(60)
 if not (OUT/'climatology_pushed.json').exists():call(PY,ROOT/'acd_stage21_climatology.py',cwd=ROOT)
 if not (OUT/'freeze_e_pushed.json').exists():
  panel=json.loads((ROOT/'receipts/acd_stage21_part1.json').read_text())
  summary={k:panel[k] for k in ['stage','environment','timing_projection','gates','wall_seconds']}
  summary['instances']=len(panel['cases']);summary['realized_outcome_accesses']=[]
  (ROOT/'receipts/acd_stage21_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
  registry_files=registry()
  files=['acd_stage21_continue.py','acd_stage21_freeze_e.py','acd_stage21_inference.py','acd_stage21_score.py','receipts/acd_stage21_summary.json']+registry_files
  push('execution and blind-step registry',files)
  call(PY,ROOT/'acd_stage21_freeze_e.py',cwd=ROOT)
  commit=push('Freeze E',['ACD_STAGE21_FREEZE_E.md','receipts/acd_stage21_freeze_e.json'])
  from acd_stage21_contract import digest
  (OUT/'freeze_e_pushed.json').write_text(json.dumps(dict(commit=commit,sha256=digest(ROOT/'ACD_STAGE21_FREEZE_E.md')))+'\n')
 # Queue behind all named earlier workloads. Read their completion records only.
 while True:
  l3=all((BASE/f'runs/stage19/inference/{m}-seed{i}/complete.json').exists() for i in range(1,5) for m in ['CNN-F','CNN-noF'])
  repair=(BASE/'runs/stage19/part3b/inference_ready.json').exists()
  d=(BASE/'receipts/acd_stage18_D.json').exists()
  c=(BASE/'runs/stage18/C_reading_ready.json').exists() and (BASE/'receipts/acd_stage18.json').exists()
  twenty=all((BASE/f'runs/stage20/{p}_published.json').exists() for p in ['B','C'])
  (OUT/'queue_status.json').write_text(json.dumps(dict(waiting=dict(L3=not l3,Part3b=not repair,Stage18D=not d,Stage18C=not c,Stage20=not twenty)),indent=2)+'\n')
  if l3 and repair and d and c and twenty:break
  time.sleep(60)
 if not (OUT/'inference_complete.json').exists():
  call(GPU,'-u',ROOT/'acd_stage21_inference.py','controller',cwd=ROOT)
  files=[str(p.relative_to(ROOT)) for p in (OUT/'inference').rglob('*.json')]+[str(p.relative_to(ROOT)) for p in (OUT/'inference_logs').glob('*.json')]
  # Manifests bind every large prediction before scoring; no outcome has been opened.
  push('inference',files)
 call(PY,'-u',ROOT/'acd_stage21_score.py',cwd=ROOT)
 files=registry()+['receipts/acd_stage21.json','ACD_STAGE21_READING.md']
 files += [str(p.relative_to(ROOT)) for p in (OUT/'scoring').glob('*.jsonl')]
 push('scoring',files)
if __name__=='__main__':
 try:main()
 except Exception:
  failure=traceback.format_exc();print(failure,flush=True)
  (OUT/'coordinator_failure.json').write_text(json.dumps(dict(error=failure))+'\n')
  raise
