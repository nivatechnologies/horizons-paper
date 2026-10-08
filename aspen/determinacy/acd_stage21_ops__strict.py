"""Execution-only failure gates; no rollout or scoring definition changes."""
import json,time
from pathlib import Path

def install(f):
 original_manifests=f.inference_manifests
 def validate(phase,tasks):
  from acd_stage21_inference import complete
  failures=[]
  logs=f.OUT/'priority_logs'
  for task in tasks:
   name=task['name'];record=logs/(phase+'_'+name+'.json')
   if record.exists() and json.loads(record.read_text()).get('returncode')!=0:failures.append(dict(task=name,cause='nonzero returncode',log=str(record.with_suffix('.log'))))
   if not (f.OUT/'inference'/name/'complete.json').exists() or not complete(name):failures.append(dict(task=name,cause='missing or invalid complete.json'))
  if phase=='R34':
   p=f.OUT/'spark_queue_outcomes.json'
   if p.exists():
    outcomes=json.loads(p.read_text())
    def walk(x):
     if isinstance(x,dict):
      if 'returncode' in x and x['returncode']!=0:failures.append(dict(cause='Spark nonzero returncode',record=x))
      for v in x.values():walk(v)
     elif isinstance(x,list):
      for v in x:walk(v)
    walk(outcomes)
  report=dict(phase=phase,status='FAILED' if failures else 'COMPLETE',failures=failures,utc=time.time())
  (f.OUT/(phase+'_execution_gate.json')).write_text(json.dumps(report,indent=2)+'\n')
  if failures:
   p=f.ROOT/'ACD_PIPELINE_STATUS.md'
   p.write_text(p.read_text()+f'\nStage21 | {phase} | pending failure-record publication | {time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())} | FAILED: '+json.dumps(failures)+'; scoring and result publication blocked.\n')
   files=[str((f.OUT/(phase+'_execution_gate.json')).relative_to(f.ROOT))]
   for ext in ('json','log'):files.extend(str(p.relative_to(f.ROOT)) for p in logs.glob(phase+'*.'+ext))
   from acd_guarded_publish import publish
   publish(f.ROOT,'stage21-'+phase+'-FAILED',files,marker=f.OUT/(phase+'_failure_pushed.json'),status_message='FAILED: nonzero task return code or incomplete output; scoring and result publication blocked.')
   raise RuntimeError(json.dumps(report))
  return report
 def manifests(phase,tasks):
  if phase=='R34':
   outcomes=json.loads((f.OUT/'spark_queue_outcomes.json').read_text())
   for row in tasks:
    name=row['name'];f.network(['scp',f.HOST+':'+str(f.REMOTE/(name+'.log')),f.OUT/'priority_logs'/('R34_'+name+'.log')])
    if name in outcomes:(f.OUT/'priority_logs'/('R34_'+name+'.json')).write_text(json.dumps(dict(outcomes[name],model=name,phase=phase))+'\n')
  validate(phase,tasks)
  files=[]
  for row in tasks:files.extend(str(p.relative_to(f.ROOT)) for p in (f.OUT/'inference'/row['name']).glob('*.json'))
  for ext in ('json','log'):files.extend(str(p.relative_to(f.ROOT)) for p in (f.OUT/'priority_logs').glob(phase+'*.'+ext))
  files.append(str((f.OUT/(phase+'_execution_gate.json')).relative_to(f.ROOT)))
  f.publish(phase+'_inference',files)
 f.inference_manifests=manifests
 return validate
