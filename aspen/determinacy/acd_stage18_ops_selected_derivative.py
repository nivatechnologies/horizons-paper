"""Complete the selected-model derivative already required by Stage18 D."""
import sys,json,subprocess,time
from pathlib import Path
r=Path('/mnt/niva-array/work/aspen-determinacy-stage19-20261007/aspen/determinacy');o=r/'runs/stage18'
if not (o/'D_selected_execution_fix_pushed.json').exists():raise RuntimeError('Wait for pushed selected-derivative execution-path fix')
sys.path.insert(0,'/mnt/niva-array/work/aspen-determinacy-stage19-l3-20261008/aspen/determinacy')
from acd_guarded_publish import publish
sys.path.insert(0,str(r))
import acd_stage18_controller as controller
assert Path(controller.__file__).resolve()==r/'acd_stage18_controller.py' and controller.OUT==o
batch=controller.batch
from acd_stage18_derivative_report import run
selection=json.loads((o/'C_selection.json').read_text());chosen=selection.get('selected')
if chosen:
 name=chosen['model'];checkpoint=o/'training'/name/'selected.pt'
 result=batch([(name+'-derivatives',[r/'acd_stage18_derivatives.py','--name',name,'--checkpoint',checkpoint,'--inputs',o/'confirmation_inputs','--micro','128'])])
 (o/'selected_D_task.json').write_text(json.dumps(result,indent=2)+'\n')
 if any(v['exit_code']!=0 for v in result.values()):raise RuntimeError('Selected derivative task FAILED; scoring and publication blocked')
 if not (o/'derivatives'/name/'complete.json').exists():raise RuntimeError('Selected-control derivative outputs incomplete; saved outputs retained for retry')
 dest='/home/todd/work/aspen-determinacy-stage18-20261007/aspen/determinacy'
 def network(args):
  while subprocess.run(list(map(str,args))).returncode:time.sleep(60)
 network(['rsync','-a',str(o/'derivatives'/name)+'/',f'sulaco:{dest}/runs/stage18/derivatives/{name}/'])
 command=f'cd {dest} && env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=2 NUMBA_NUM_THREADS=2 /home/todd/work/aspen-determinacy-20261005/.venv/bin/python -u acd_stage18_derivative_readings.py --name {name}'
 network(['ssh','-o','BatchMode=yes','sulaco',command]);network(['scp',f'sulaco:{dest}/receipts/acd_stage18_derivatives_{name}.json',r/'receipts'/f'acd_stage18_derivatives_{name}.json'])
 run();files=['runs/stage18/selected_D_task.json',f'runs/stage18/{name}-derivatives.log','receipts/acd_stage18_D.json','ACD_STAGE18_READING.md',f'receipts/acd_stage18_derivatives_{name}.json']
 publish(r,'stage18-selected-D',files,[('receipts/acd_stage18_D.json','ACD_POSTHOC_18D')],marker=o/'D_selected_pushed.json')
else:
 (o/'D_selected_pushed.json').write_text(json.dumps({'not_evaluable':'No validation-selected response model; no substitute','selection':selection})+'\n')
