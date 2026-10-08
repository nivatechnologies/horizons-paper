"""Durable launch order for already frozen D code, then C generation only."""
import json,subprocess,time,os,sys
from pathlib import Path
r=Path('/mnt/niva-array/work/aspen-determinacy-stage19-20261007/aspen/determinacy');o=r/'runs/stage18'
s='/home/todd/work/aspen-determinacy-stage18-20261007/aspen/determinacy';py='/home/todd/work/aspen-determinacy-20261005/.venv/bin/python';gpu='/mnt/niva-array/niva-platform/.venv-cu130/bin/python'
sys.path.insert(0,str(r))
from acd_stage18_controller import batch

def attempt(args):
 while True:
  p=subprocess.run(args)
  if p.returncode==0:return
  if p.returncode!=255:raise RuntimeError(f'Command failed {p.returncode}: {args[0]}')
  time.sleep(60)

while not (o/'B_pushed.json').exists():time.sleep(30)
tasks=[]
for name,checkpoint,conditioned,estimator in [
 ('CNN-20k',r/'runs/stage19/checkpoints/CNN-20k.pt',False,None),
 ('CNN-F',o/'checkpoints/CNN-F.pt',True,None),
 ('CNN-noF',r/'runs/stage19/checkpoints/CNN-noF.pt',False,None),
 ('CNN-F-E0-fixed-seed1',o/'checkpoints/CNN-F.pt',True,o/'training/E0-seed1/selected.pt')]:
 args=[r/'acd_stage18_derivatives.py','--name',name,'--checkpoint',checkpoint,'--inputs',o/'confirmation_inputs','--micro','128']
 if conditioned:args.append('--conditioned')
 if estimator:args+=['--estimator',estimator]
 tasks.append((name+'-derivatives',args))
result=batch(tasks)
attempt(['scp',str(o/'freeze_pushed.json'),f'sulaco:{s}/runs/stage18/freeze_pushed.json'])
for name,_,_,_ in [
 ('CNN-20k',None,None,None),('CNN-F',None,None,None),('CNN-noF',None,None,None),('CNN-F-E0-fixed-seed1',None,None,None)]:
 if not (o/'derivatives'/name/'complete.json').exists():continue
 attempt(['rsync','-a',str(o/'derivatives'/name)+'/',f'sulaco:{s}/runs/stage18/derivatives/{name}/'])
 command=f'cd {s} && env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=2 NUMBA_NUM_THREADS=2 {py} -u acd_stage18_derivative_readings.py --name {name} > runs/stage18/derivative_score_{name}.log 2>&1'
 attempt(['ssh','-o','BatchMode=yes','sulaco',command])
 attempt(['scp',f'sulaco:{s}/receipts/acd_stage18_derivatives_{name}.json',str(r/'receipts'/f'acd_stage18_derivatives_{name}.json')])
subprocess.run(['python',str(r/'acd_stage18_derivative_report.py')],cwd=r,check=True)
(o/'D_reading_ready.json').write_text(json.dumps({'outcomes':result,'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())},indent=2)+'\n')
while not (o/'D_pushed.json').exists():time.sleep(30)
command=f'cd {s} && env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=4 NUMBA_NUM_THREADS=4 {py} -u acd_stage18_data.py > runs/stage18/C_generation.log 2>&1'
attempt(['ssh','-o','BatchMode=yes','sulaco',command])
attempt(['rsync','-a',f'sulaco:{s}/runs/stage18/response_data/',str(o/'response_data')+'/'])
attempt(['scp',f'sulaco:{s}/receipts/acd_stage18_response_data.json',str(r/'receipts/acd_stage18_response_data.json')])
(o/'C_data_ready_for_commit.json').write_text(json.dumps({'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())})+'\n')
