"""Persistent Stage22 operational watchdog; criteria and scientific code unchanged."""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'runs/stage22'
REMOTE='/home/todd/work/aspen-stage22-panel-20261010'
CPU='/home/todd/work/aspen-determinacy-20261005/.venv/bin/python'
GPU='/mnt/niva-array/niva-platform/.venv-cu130/bin/python'
ENV=['env','ACD_STAGE22_BASE=/home/todd/work/aspen-stage21-scoring-20261008/aspen/determinacy',
     'ACD_INHERITED_ROOT=/home/todd/work/aspen-forecast-decision-20261005/aspen/forecast_decision',
     'ACD_STAGE21_PRIOR_CONF=/home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs/conf']
BASE='/mnt/niva-array/work/aspen-determinacy-stage21-20261008/aspen/determinacy'

def write(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix(path.suffix+'.pending');tmp.write_text(json.dumps(value,indent=2)+'\n');tmp.replace(path)

def event(kind,**fields):
    with (OUT/'watchdog_events.jsonl').open('a') as stream:
        stream.write(json.dumps(dict(utc=time.time(),kind=kind,**fields))+'\n')
    print(kind,json.dumps(fields),flush=True)

def call(args,timeout=120):
    return subprocess.run(list(map(str,args)),capture_output=True,text=True,timeout=timeout)

def remote(args,timeout=120):
    import shlex
    return call(['ssh','-o','BatchMode=yes','-o','ConnectTimeout=15','sulaco',shlex.join(list(map(str,args)))],timeout)

def active(unit,remote_host=False):
    r=remote(['systemctl','--user','is-active',unit+'.service']) if remote_host else call(['systemctl','--user','is-active',unit+'.service'])
    return r.returncode==0

def start_cpu(unit,mode):
    remote(['systemctl','--user','reset-failed',unit+'.service'])
    r=remote(['systemd-run','--user','--unit='+unit,'--property=WorkingDirectory='+REMOTE,
          '--property=StandardOutput=append:'+REMOTE+'/'+mode+'.log',
          '--property=StandardError=append:'+REMOTE+'/'+mode+'.log',
          *ENV,CPU,'-u',REMOTE+'/acd_stage22_runtime.py',mode])
    if r.returncode:raise RuntimeError(r.stderr)
    event('cpu_service_started',unit=unit,mode=mode)

def start_local(unit,args):
    call(['systemctl','--user','reset-failed',unit+'.service'])
    r=call(['systemd-run','--user','--unit='+unit,'--property=WorkingDirectory='+str(ROOT),
         '--property=StandardOutput=append:'+str(OUT/(unit+'.log')),
         '--property=StandardError=append:'+str(OUT/(unit+'.log')),*args])
    if r.returncode:raise RuntimeError(r.stderr)
    event('local_service_started',unit=unit)

def sync(source,destination,exclude=()):
    r=call(['rsync','-a',*[x for e in exclude for x in ['--exclude',e]],source,destination],timeout=3600)
    if r.returncode:raise ConnectionError(r.stderr)

def block(reason,**fields):
    write(OUT/'FAILED.json',dict(reason=reason,utc=time.time(),**fields))
    event('FAILED',reason=reason,**fields)

def restore_interrupted_lease(gpu):
    record=OUT/f'gpu_service_recovery_{gpu}.json'
    if not record.exists():return
    data=json.loads(record.read_text())
    expected={0:'qwen3.8-vllm-mtp@card-a.service',1:'qwen3.8-vllm-mtp@card-b.service',2:'qwen3.8-vllm-mtp@card-c.service'}
    assert data['unit']==expected[gpu]
    if data['was_active']:
        result=call(['systemctl','--user','start',data['unit']])
        if result.returncode:raise RuntimeError('Authorized GPU service restoration failed: '+result.stderr)
    record.unlink();event('interrupted_gpu_lease_restored',gpu=gpu,unit=data['unit'])

def gpu_progress(claims,state):
    result=call(['nvidia-smi','--query-gpu=index,utilization.gpu','--format=csv,noheader,nounits'])
    if result.returncode:return
    utilization={int(line.split(',')[0]):int(line.split(',')[1]) for line in result.stdout.splitlines()}
    previous=state.get('gpu_progress',{});current={}
    for name,claim in claims.items():
        files=list((OUT/'inference'/name).glob('[0-9][0-9][0-9].npz'))
        last=max([p.stat().st_mtime for p in files]+[claim['started']])
        ticks=0
        for process in Path('/proc').glob('[0-9]*'):
            try:
                command=(process/'cmdline').read_bytes().replace(b'\0',b' ').decode(errors='replace')
                if str(ROOT/'acd_stage22_runtime.py') not in command or '--name '+name+' ' not in command:continue
                stat=(process/'stat').read_text().rsplit(')',1)[1].split();ticks+=int(stat[11])+int(stat[12])
            except (OSError,ValueError):pass
        row=dict(cpu_ticks=ticks,files=len(files),last=last,gpu=claim['gpu'],utilization=utilization[claim['gpu']])
        current[name]=row;old=previous.get(name,{})
        if time.time()-last>20*60 and utilization[claim['gpu']]==0 and old.get('cpu_ticks')==ticks and old.get('files')==len(files):
            restarts=state.setdefault('gpu_restarts',{}).get(name,0)
            if restarts>=3:block('Repeated stalled inference execution',task=name)
            else:
                record=dict(task=name,status='FAILED execution stall; same frozen task will resume',gpu=claim['gpu'],utc=time.time())
                write(OUT/'inference_logs'/(name+'.watchdog_attempt.json'),record)
                call(['systemctl','--user','stop','aspen-stage22-gpu-'+str(claim['gpu'])+'.service'])
                state['gpu_restarts'][name]=restarts+1;event('stalled_gpu_execution_stopped_for_resume',**record)
    state['gpu_progress']=current

def publication(step):
    marker=OUT/(step+'_pushed.json')
    if not marker.exists() and not active('aspen-stage22-publish-'+step):
        start_local('aspen-stage22-publish-'+step,[sys.executable,str(ROOT/'acd_stage22_watchdog_publish.py'),step])

def stale_decision(previous,current,stale_seconds):
    if current['workers']:
        old={p['pid']:p['cpu_ticks'] for p in previous.get('workers',[])}
        if any(old.get(p['pid'],-1)!=p['cpu_ticks'] for p in current['workers']):return False
    return current['utc']-current['last_output_mtime']>stale_seconds

def tick(state):
    probe=remote([CPU,REMOTE+'/acd_stage22_probe.py'])
    if probe.returncode:
        event('network_retry',error=probe.stderr[-1000:]);return state
    health=json.loads(probe.stdout);n=json.loads((ROOT/'receipts/acd_stage22_freeze_f.json').read_text())['N']
    write(OUT/'watchdog_health.json',health)
    if (OUT/'FAILED.json').exists():
        publication('failure');return dict(state,last_probe=health,phase='FAILED')
    if (OUT/'results_pushed.json').exists():return dict(state,last_probe=health,phase='COMPLETE')
    phase='blind_sampling'
    if not (OUT/'panel_pushed.json').exists():
        workers=[p for p in health['workers'] if ' case ' in p['command']]
        controllers=[p for p in health['workers'] if ' run ' in p['command'] or ' resume ' in p['command']]
        if health['cases_done']==n:
            if not controllers:publication('panel')
        elif not workers and not controllers:
            assert health['timing'] and health['timing']['passed'],'No passed timing gate; blocked'
            count=state.get('cpu_restarts',0)
            if count>=3:block('Repeated CPU-controller failure; dependent phases blocked',health=health)
            elif any(term in text for text in health['failed_logs'].values() for term in ['AssertionError','R-other:','nonfinite']):
                block('Frozen scientific/hash gate failed; no criteria changed',health=health)
            else:
                start_cpu('aspen-stage22-resume','resume');state['cpu_restarts']=count+1
        elif stale_decision(state.get('last_probe',{}),health,20*60):
            # Require two consecutive no-CPU-progress probes. Never kill active computation.
            if state.get('stale_probe',False):
                if state.get('cpu_restarts',0)>=3:block('Repeated stalled CPU phase',health=health)
                else:
                    for unit in ['aspen-stage22-blind','aspen-stage22-resume']:
                        remote(['systemctl','--user','stop',unit+'.service'])
                    state['cpu_restarts']=state.get('cpu_restarts',0)+1
                    start_cpu('aspen-stage22-resume','resume');event('stalled_stage22_service_restarted')
                state['stale_probe']=False
            else:state['stale_probe']=True
        else:state['stale_probe']=False
    elif not health['inputs_complete']:
        phase='prepare_inputs'
        sync(str(OUT/'panel_pushed.json'),'sulaco:'+REMOTE+'/runs/stage22/')
        if active('aspen-stage22-prepare',True):
            if stale_decision(state.get('last_probe',{}),health,20*60) and state.get('phase')=='prepare_inputs':
                remote(['systemctl','--user','stop','aspen-stage22-prepare.service'])
                event('stalled_preparation_restarted_at_next_probe')
        else:
            if state.get('prepare_starts',0)>=3:block('Repeated input preparation failure')
            else:start_cpu('aspen-stage22-prepare','prepare');state['prepare_starts']=state.get('prepare_starts',0)+1
    elif not (OUT/'inference_verified.json').exists():
        phase='inference'
        if not (OUT/'inputs_transferred.json').exists():
            sync('sulaco:'+REMOTE+'/runs/stage22/inference_inputs/',str(OUT/'inference_inputs')+'/')
            sync('sulaco:'+REMOTE+'/runs/stage22/A_inputs/',str(OUT/'A_inputs')+'/')
            sync('sulaco:'+REMOTE+'/runs/stage22/inputs_complete.json',str(OUT)+'/')
            expected=json.loads((OUT/'inputs_complete.json').read_text())
            assert expected['N']==n
            from acd_stage22_runtime import digest
            for folder,hashes in expected['hashes'].items():
                assert len(hashes)==n and all(digest(ROOT/folder/p)==h for p,h in hashes.items())
            write(OUT/'inputs_transferred.json',dict(N=n,utc=time.time()))
        from acd_stage22_runtime import complete
        tasks=json.loads((ROOT/'receipts/acd_stage22_freeze_f.json').read_text())['tasks']
        if all(complete(r['name'],False) for r in tasks):
            assert all(complete(r['name']) for r in tasks)
            write(OUT/'inference_verified.json',dict(N=n,tasks=[r['name'] for r in tasks],utc=time.time()))
            publication('inference')
        else:
            claims_path=OUT/'claims.json';claims=json.loads(claims_path.read_text()) if claims_path.exists() else {}
            with (OUT/'claims.lock').open('w') as lock:
                fcntl.flock(lock,fcntl.LOCK_EX)
                for name,claim in list(claims.items()):
                    try:command=Path('/proc')/str(claim['pid'])/'cmdline';live=b'acd_stage22_runtime.py' in command.read_bytes()
                    except OSError:live=False
                    if not live:
                        claims.pop(name)
                        event('orphaned_gpu_claim_released',task=name,attempt_status='FAILED: interrupted execution; retry preserves frozen task and completed outputs')
                write(claims_path,claims)
            for gpu in range(3):
                unit='aspen-stage22-gpu-'+str(gpu)
                if not active(unit):
                    restore_interrupted_lease(gpu)
                    start_local(unit,[ 'env','ACD_STAGE22_BASE='+BASE,GPU,'-u',str(ROOT/'acd_stage22_runtime.py'),'slot','--gpu',str(gpu)])
            gpu_progress(claims,state)
    elif not health['scoring_complete']:
        phase='scoring'
        if not (OUT/'inference_pushed.json').exists():publication('inference')
        else:
            sync(str(OUT/'inference')+'/','sulaco:'+REMOTE+'/runs/stage22/inference/')
            sync(str(OUT/'inference_verified.json'),'sulaco:'+REMOTE+'/runs/stage22/')
            if active('aspen-stage22-score',True):
                if stale_decision(state.get('last_probe',{}),health,20*60) and state.get('phase')=='scoring':
                    remote(['systemctl','--user','stop','aspen-stage22-score.service'])
                    event('stalled_scoring_restarted_at_next_probe')
            else:
                if state.get('score_starts',0)>=2:block('Repeated frozen scoring failure; no publication')
                else:start_cpu('aspen-stage22-score','score');state['score_starts']=state.get('score_starts',0)+1
    else:
        phase='publishing_results'
        publication('results')
    return dict(state,last_probe=health,phase=phase,utc=time.time())

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    with (OUT/'watchdog.lock').open('w') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        path=OUT/'watchdog_state.json';state=json.loads(path.read_text()) if path.exists() else {}
        event('watchdog_started',pid=os.getpid(),host=os.uname().nodename)
        while True:
            try:
                state=tick(state);write(path,state)
                if state.get('phase')=='COMPLETE':event('stage22_complete');return
            except (ConnectionError,subprocess.TimeoutExpired) as e:event('network_retry',error=str(e))
            except (AssertionError,ValueError,KeyError) as e:block('Integrity or frozen execution assertion failed',exception=repr(e))
            except Exception as e:event('operational_retry',exception=repr(e))
            time.sleep(60)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--self-test',action='store_true');a=p.parse_args()
    if a.self_test:
        old=dict(workers=[dict(pid=1,cpu_ticks=10)])
        now=dict(workers=[dict(pid=1,cpu_ticks=11)],utc=5000,last_output_mtime=0)
        assert not stale_decision(old,now,1200)
        now['workers'][0]['cpu_ticks']=10
        assert stale_decision(old,now,1200)
        now['last_output_mtime']=4990
        assert not stale_decision(old,now,1200)
        print('Watchdog recovery decision tests PASS; no jobs or outcomes opened')
    else:main()
