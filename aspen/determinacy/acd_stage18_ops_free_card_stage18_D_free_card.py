"""Run one frozen D task on a released card; do not preempt any analysis."""
import json,os,subprocess,time
from pathlib import Path
h=Path(__file__).resolve().parent;r=Path('/mnt/niva-array/work/aspen-determinacy-stage19-20261007/aspen/determinacy');o=r/'runs/stage18'
while not (o/'D_free_card_execution_pushed.json').exists():time.sleep(10)
py='/mnt/niva-array/niva-platform/.venv-cu130/bin/python'
args=[py,'-u',str(r/'acd_stage18_gpu_lease.py'),'--gpu','2','--',py,'-u',str(r/'acd_stage18_derivatives.py'),'--name','CNN-noF','--checkpoint',str(r/'runs/stage19/checkpoints/CNN-noF.pt'),'--inputs',str(o/'confirmation_inputs'),'--micro','128']
start=time.monotonic()
with (o/'D_free_card.log').open('a') as log:
 p=subprocess.run(args,cwd=r,env=dict(os.environ,OMP_NUM_THREADS='4',OPENBLAS_NUM_THREADS='1'),stdout=log,stderr=subprocess.STDOUT)
record=dict(returncode=p.returncode,seconds=time.monotonic()-start,model='CNN-noF',gpu=2,complete=(o/'derivatives/CNN-noF/complete.json').exists(),criteria_changed=False)
(o/'D_free_card.json').write_text(json.dumps(record,indent=2)+'\n')
if p.returncode:raise RuntimeError(json.dumps(record))
