"""Baccus-only queue controller. Reads training progress and validation readiness only."""
import argparse,datetime,json,shutil,subprocess,time,shlex
from pathlib import Path
ROOT=Path(__file__).resolve().parent
REMOTE='/home/todd/work/aspen-forecast-decision-20261005/aspen/forecast_decision'
ACTIVE={}

def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def complete(name):return (ROOT/'runs/training'/name/'training_complete.json').exists()
def run_record(name):
    return json.loads((ROOT/'runs/training'/name/'training_complete.json').read_text())
def has_val2():
    r=subprocess.run(['ssh','sulaco','test -f '+REMOTE+'/runs/selection_inputs/validation2_inputs.npz'])
    return r.returncode==0
def launch(name,gpu,micro):
    capacity=subprocess.run(['ssh','baccus','nvidia-smi --query-gpu=index,name,memory.total,memory.used --format=csv,noheader'],check=True,capture_output=True,text=True).stdout
    directory=ROOT/'runs/training'/name;directory.mkdir(parents=True,exist_ok=True)
    (directory/'scheduler_capacity.txt').write_text(now()+'\n'+capacity)
    log=directory/'scheduler.log'
    command='nohup bash '+shlex.quote(str(ROOT/'launch_training.sh'))+' '+shlex.quote(name)+' '+str(gpu)+' '+str(micro)
    command+=' > '+shlex.quote(str(log))+' 2>&1 < /dev/null & echo $!'
    process=subprocess.run(['ssh','baccus',command],check=True,capture_output=True,text=True)
    pid=int(process.stdout.strip());ACTIVE[name]=(pid,gpu)
    (directory/'detached_worker_pid.txt').write_text(str(pid)+'\n')
    print(now(),'launch',name,'GPU',gpu,'microbatch',micro,flush=True)

def main(cuts):
    done=set();queue=['CNN-5k','CNN-80k','CNN-20k-s2','CNN-20k-s3']
    for path in (ROOT/'runs/training').glob('*/detached_worker_pid.txt'):
        name=path.parent.name
        if complete(name):continue
        pid=int(path.read_text());check=subprocess.run(['ssh','baccus','ps -p '+str(pid)+' -o args='],capture_output=True,text=True)
        if ('--name '+name+' ') in check.stdout or ('launch_training.sh '+name+' ') in check.stdout:
            gpu=1 if name in ['CNN2-20k','CNN2-R2'] else 0 if name=='CNN2-cost' else 2
            ACTIVE[name]=(pid,gpu)
    while True:
        control=ROOT/'runs/campaign_control.json'
        if control.exists() and json.loads(control.read_text()).get('execution')=='stop':
            print(now(),'root stop: no further launches',flush=True);return
        cutfile=ROOT/'runs/training/cuts.json'
        if cutfile.exists():cuts.update(json.loads(cutfile.read_text()).get('cuts',[]))
        for name,(pid,gpu) in list(ACTIVE.items()):
            running=subprocess.run(['ssh','baccus','kill -0 '+str(pid)],capture_output=True)
            if running.returncode==0:continue
            del ACTIVE[name]
            if not complete(name):
                raise RuntimeError(f'{name} failed without completion receipt; inspect training-only scheduler.log')
            record=run_record(name)
            if record['charged_gpu_seconds']>record['cap_seconds']:
                raise RuntimeError(f'{name} exceeded cap; halt scheduling')
            done.add(name);print(now(),'complete',name,flush=True)
        # Mandatory two-scale base first; it does not require panel truth.
        if complete('CNN-resp') and not complete('CNN2-20k') and 'CNN2-20k' not in ACTIVE:
            if not (ROOT/'runs/training_data2/base_train.npz').exists():
                raise RuntimeError('two-scale base training inputs missing')
            launch('CNN2-20k',1,64)
        if complete('CNN2-20k'):
            base=ROOT/'runs/training/CNN2-20k'
            data=ROOT/'runs/training_data2'
            if not (data/'CNN2-20k.pt').exists():
                shutil.copy2(base/'selected.pt',data/'CNN2-20k.pt')
                shutil.copy2(base/'training_complete.json',data/'CNN2-20k.training.json')
            if has_val2() and not complete('CNN2-R2') and 'CNN2-R2' not in ACTIVE:
                launch('CNN2-R2',1,64)
        # Await validation readiness before allocating GPU to checkpoint-selected workers.
        if complete('CNN-roll') and has_val2() and not complete('CNN2-cost') and 'CNN2-cost' not in ACTIVE:
            launch('CNN2-cost',0,64)
        # Optional Stage2 models use GPU2 only after its two mandatory workers finish.
        if complete('CNN-cost') and complete('CNN-R2') and not any(gpu==2 for _,gpu in ACTIVE.values()):
            remaining=[name for name in queue if name not in cuts and not complete(name)]
            if remaining:launch(remaining[0],2,64)
        status=dict(recorded_at=now(),active={n:dict(remote_baccus_pid=pid,gpu=g,detached=True) for n,(pid,g) in ACTIVE.items()},
                    completed=sorted(done),cuts=sorted(cuts),
                    pending_two_scale_validation=not has_val2(),
                    test_access='none; controller reads no test outputs')
        target=ROOT/'runs/training/scheduler_status.json'
        tmp=target.with_suffix('.tmp');tmp.write_text(json.dumps(status,indent=2)+'\n');tmp.replace(target)
        if all(complete(n) for n in ['CNN2-20k','CNN2-R2','CNN2-cost']) and all(n in cuts or complete(n) for n in queue):break
        time.sleep(30)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cut',action='append',default=[])
    a=p.parse_args();main(set(a.cut))
