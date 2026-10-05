import os,subprocess,json,time
from pathlib import Path
root=Path('/home/todd/work/aspen-determinacy-20261005/aspen/determinacy');python='/home/todd/work/aspen-determinacy-20261005/.venv/bin/python'
logs=root/'runs/conf/joblogs';logs.mkdir(parents=True,exist_ok=True)
env=dict(os.environ,OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
status=root/'runs/conf/supervisor.json'
def save(**v):status.write_text(json.dumps(dict(time=time.time(),**v),indent=2)+'\n')
def launch(name,cores,script,args,threads):
 e=dict(env,NUMBA_NUM_THREADS=str(threads));f=(logs/(name+'.log')).open('w');p=subprocess.Popen(['taskset','-c',cores,python,script,*args],cwd=root,env=e,stdout=f,stderr=subprocess.STDOUT);return (name,p,f)
def finish(jobs,phase):
 codes=[]
 for name,p,f in jobs:
  code=p.wait();f.close();codes.append(dict(name=name,code=code));save(phase=phase,completed=codes)
 if any(c['code'] for c in codes):raise RuntimeError(str(codes))
# All observations are generated only by workers which verify the pushed freezes.
jobs=[launch('cpu_'+str(i),f'{128+i*8}-{135+i*8}','acd_confirmation.py',['cpu','--worker',str(i),'--workers','16'],8) for i in range(16)]
cnn=launch('cnn','120-121','acd_cnn_ensemble.py',['--microbatch','8'],2)
save(phase='ordinary_and_cnn',cpu_pids=[p.pid for _,p,_ in jobs],cnn_pid=cnn[1].pid)
finish(jobs,'ordinary_cpu');finish([cnn],'ordinary_cnn')
finish([launch('score','128-135','acd_confirmation.py',['score'],8)],'scoring')
jobs=[launch('measure_'+str(i),f'{128+i*4}-{131+i*4}','acd_confirmation.py',['measure','--worker',str(i),'--workers','32'],4) for i in range(32)]
save(phase='measure',pids=[p.pid for _,p,_ in jobs]);finish(jobs,'measure')
finish([launch('analysis','128-135','acd_confirmation_analysis.py',[],8)],'analysis')
finish([launch('verify','128-135','acd_stage2_check.py',[],8)],'verify')
save(phase='COMPLETE')
