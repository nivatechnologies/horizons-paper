"""Resumable execution handoffs; scientific functions remain frozen."""
import argparse
import concurrent.futures
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
OUT = ROOT/'runs/stage22'

def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def write(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    pending=path.with_suffix(path.suffix+'.pending')
    pending.write_text(json.dumps(value,indent=2,allow_nan=False)+'\n');pending.replace(path)

def configured(require_panel=True):
    import acd_stage22_panel
    record,contract,blind=acd_stage22_panel.configure()
    import acd_stage22_adapter as adapter
    def ready():
        assert (OUT/'freeze_f_pushed.json').exists()
        contract_record=json.loads((ROOT/'receipts/acd_stage22_panel_contract.json').read_text())
        assert digest(ROOT/'ACD_STAGE22_FREEZE_F.md')==contract_record['freeze_f_sha256']
        execution=json.loads((ROOT/'receipts/acd_stage22_watchdog_execution.json').read_text())
        assert (OUT/'watchdog_pushed.json').exists()
        for p,h in execution['code_hashes'].items():assert digest(ROOT/p)==h,p
        for p,h in record['freeze_e_hashes'].items():assert digest(adapter.BASE/p)==h,p
        for r in record['parameterization']['modules']:assert digest(ROOT/r['path'])==r['sha256'],r['path']
        if require_panel:
            assert (OUT/'panel_pushed.json').exists(),'Entire blind panel must be committed first'
            panel=json.loads((ROOT/'receipts/acd_stage22_part1.json').read_text())
            assert panel['status']=='blind_sampling_complete' and len(panel['cases'])==record['N']
            assert not panel['realized_outcome_accesses']
        tasks=[]
        for row in record['tasks']:
            row=dict(row)
            for key in ['checkpoint','estimator']:
                if row.get(key):row[key]=str(adapter.BASE/row[key])
            tasks.append(row)
        return dict(record,tasks=tasks)
    import acd_stage21_freeze_e
    acd_stage21_freeze_e.ready=ready
    return ready,contract,blind

def resume():
    ready,contract,blind=configured(False);blind.verify()
    receipt=json.loads((ROOT/'receipts/acd_stage22_part1.json').read_text())
    projection=receipt['timing_projection'];assert projection['passed']
    groups,reserved=blind.topology()
    assert len(groups)==projection['workers'] and all(len(g)==projection['cores_per_worker'] for g in groups)
    count=ready()['N']
    # Re-enter exactly the frozen per-case implementation, including cache hash checks.
    def queue(index):
        for c in range(index,count,len(groups)):
            log=OUT/f'worker_{c:03d}.log'
            with log.open('a') as stream:
                result=subprocess.run(['taskset','-c',','.join(map(str,groups[index])),sys.executable,
                    str(ROOT/'acd_stage22_panel.py'),'case',str(c)],stdout=stream,stderr=subprocess.STDOUT)
            write(OUT/f'worker_{c:03d}.exit.json',dict(case=c,returncode=result.returncode,utc=time.time()))
            if result.returncode:raise RuntimeError(f'Frozen case {c} failed; see {log}')
            blind.summarize('blind_sampling_running',projection)
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(groups)) as pool:list(pool.map(queue,range(len(groups))))
    blind.summarize('blind_sampling_complete',projection)
    from acd_stage21_publish import publish
    publish('panel')

def prepare():
    ready,contract,blind=configured()
    import acd_stage21_inference as frozen
    frozen.ready=ready;frozen.prepare()
    n=ready()['N']
    manifests={}
    for folder in [OUT/'inference_inputs',OUT/'A_inputs/constantF']:
        files=sorted(folder.glob('[0-9][0-9][0-9].npz'))
        assert len(files)==n
        manifests[str(folder.relative_to(ROOT))]={p.name:digest(p) for p in files}
    write(OUT/'inputs_complete.json',dict(N=n,hashes=manifests,realized_outcome_accesses=[]))

def complete(name,verify=True):
    folder=OUT/'inference'/name
    if not (folder/'complete.json').exists():return False
    record=json.loads((ROOT/'receipts/acd_stage22_freeze_f.json').read_text())
    d=json.loads((folder/'complete.json').read_text())
    hashes=json.loads((folder/'hashes.json').read_text())
    assert d['cases']==record['N'] and set(hashes)=={f'{i:03d}.npz' for i in range(record['N'])}
    task=next(r for r in record['tasks'] if r['name']==name)
    assert d['checkpoint_sha256']==task['checkpoint_sha256']
    assert d.get('estimator_sha256')==task.get('estimator_sha256')
    if verify:assert all(digest(folder/p)==h for p,h in hashes.items()),name
    return True

def worker(name):
    ready,contract,blind=configured();r=next(t for t in ready()['tasks'] if t['name']==name)
    for key in ['checkpoint','estimator']:
        if r.get(key):assert digest(r[key])==r[key+'_sha256'],key
    import acd_stage21_inference as frozen
    frozen.ready=ready;frozen.worker(name)
    assert complete(name)

def slot(index):
    ready,contract,blind=configured()
    from acd_stage19_part2_gate import gpu_inventory
    import acd_stage19_gpu_lease as lease
    lease.OUT=OUT;lease.freeze_ready=ready
    while True:
        if (OUT/'FAILED.json').exists():return
        with (OUT/'claims.lock').open('w') as lock:
            fcntl.flock(lock,fcntl.LOCK_EX)
            path=OUT/'claims.json';claims=json.loads(path.read_text()) if path.exists() else {}
            pending=[r for r in ready()['tasks'] if not complete(r['name'],False) and r['name'] not in claims]
            if not pending:return
            row=pending[0];name=row['name'];claims[name]=dict(pid=os.getpid(),gpu=index,started=time.time())
            write(path,claims)
        logdir=OUT/'inference_logs';logdir.mkdir(exist_ok=True)
        begin=time.monotonic();result=None
        try:
            while True:
                card=next(c for c in gpu_inventory() if c['index']==index)
                if all('VLLM' in p['process'].upper() for p in card['processes']):break
                time.sleep(60)
            with lease.lease(index) as card:
                with (logdir/(name+'.log')).open('a') as log:
                    result=subprocess.run([sys.executable,str(Path(__file__).resolve()),'worker','--name',name],
                        env=dict(os.environ,CUDA_VISIBLE_DEVICES=card['uuid']),stdout=log,stderr=subprocess.STDOUT)
            success=result.returncode==0 and complete(name)
            write(logdir/(name+'.json'),dict(name=name,returncode=result.returncode,gpu=card,
                  seconds=time.monotonic()-begin,complete=success,utc=time.time()))
            if not success:
                write(OUT/'FAILED.json',dict(phase='inference',task=name,returncode=result.returncode,
                      log=str(logdir/(name+'.log')),reason='Nonzero return code or incomplete/hash-invalid output',utc=time.time()))
                return
        except Exception as e:
            write(OUT/'FAILED.json',dict(phase='inference',task=name,reason=str(e),utc=time.time()))
            raise
        finally:
            with (OUT/'claims.lock').open('w') as lock:
                fcntl.flock(lock,fcntl.LOCK_EX)
                claims=json.loads((OUT/'claims.json').read_text());claims.pop(name,None);write(OUT/'claims.json',claims)

def score():
    ready,contract,blind=configured();freeze=ready()
    assert not (OUT/'FAILED.json').exists()
    assert all(complete(r['name']) for r in freeze['tasks'])
    import acd_stage21_score as frozen
    frozen.ready=ready
    import numpy as np
    import inspect
    original_load=np.load
    def logged_load(path,*args,**kwargs):
        result=original_load(path,*args,**kwargs)
        if Path(path).resolve()==(OUT/'scoring/actual.npz').resolve():
            frame=inspect.stack()[1]
            assert frame.function=='score_actual' and Path(frame.filename).name=='acd_stage21_score.py'
            assert result['actual'].shape[0]==freeze['N'] and result['factual'].shape[0]==freeze['N']
            with (OUT/'scoring/access.jsonl').open('a') as log:
                log.write(json.dumps(dict(path=str(path),sha256=digest(path),caller=frame.filename,function=frame.function,utc=time.time()))+'\n')
        return result
    np.load=logged_load
    frozen.score()  # Realized outcomes are opened solely inside this frozen scorer.
    data=json.loads((ROOT/'receipts/acd_stage21.json').read_text())
    assert not data['missing_models']
    retained=data['models']['posterior']['pooled']['case_indices']
    assert len(retained)+len(data['excluded_cases'])==freeze['N']
    from acd_stage22_R56 import score as additional
    extra=additional(data,freeze['tasks'])
    np.load=original_load
    original=json.loads((Path(os.environ['ACD_STAGE22_BASE'])/'receipts/acd_stage21_R12_recovery.json').read_text())
    data.update(stage=22,assigned_n=freeze['N'],freeze_f_sha256=digest(ROOT/'ACD_STAGE22_FREEZE_F.md'),
        confirmatory=dict(R2_S22=data['confirmatory']['R2'],**{k:extra[k] for k in ['R5_S22','R6_S22']}),
        descriptive_R5_by_forcing=extra['R5_by_forcing'],descriptive_R6_by_forcing=extra['R6_by_forcing'],
        first_panel_R2=dict(reading=original['confirmatory']['R2'],receipt_sha256=digest(Path(os.environ['ACD_STAGE22_BASE'])/'receipts/acd_stage21_R12_recovery.json')))
    from acd_stage19_part3b_score import seed_average
    import acd_stage22_adapter as adapter
    levels=frozen.assignments();data['descriptive_R2_by_forcing']={}
    for label,level in [('F7',7),('F9',9)]:
        ids=[i for i,f in enumerate(levels) if f==level]
        pairs=[dict(case_differences=[p['case_differences'][i] for i in ids]) for p in data['confirmatory']['R2_S22']['per_seed']]
        data['descriptive_R2_by_forcing'][label]=seed_average(pairs,alpha=.01,lower_only=False)
    write(ROOT/'receipts/acd_stage22.json',data)
    lines=['# Stage22 fresh forcing-shift panel readings','','Fixed assigned panel; exclusions withheld, no pooling with Stage21. All frozen pipelines reported.','',
        '| Reading | Point | Interval/bound | Type | Outcome |','|---|---:|---|---|---|']
    for label,row in [('Stage21 R2 (unchanged)',original['confirmatory']['R2']),*data['confirmatory'].items()]:
        q=row.get('interval',row)
        if 'per_seed' in row and 'interval' not in row:
            for seed in row['per_seed']:lines.append(f"| {label}, seed {seed['seed']} | {seed['point']} | {seed['lower']}, {seed['upper']} | {seed['bound_type']} | {'PASS' if seed['confirmed'] else 'FAIL'} |")
            lines.append(f"| {label}, every-seed criterion | | | | {'PASS' if row['confirmed'] else 'FAIL'} |")
        else:lines.append(f"| {label} | {q.get('point')} | {q.get('lower')}, {q.get('upper')} | {q.get('bound_type')} | {'PASS' if row.get('confirmed') else 'FAIL'} |")
    lines+=['','## Full descriptive readings','','The receipt contains every pipeline, pooled and by forcing, state skill, forcing errors, per-draw costs, confidence/error bounds, calibration, same-lead comparisons, paired endpoints, decision harm bounds and action histograms. The following inherited table is descriptive throughout.','',
        '| Pipeline |'+(ROOT/'ACD_STAGE21_READING.md').read_text().split('| Pipeline |',1)[1]]
    (ROOT/'ACD_STAGE22_READING.md').write_text('\n'.join(lines)+'\n')
    write(OUT/'scoring_complete.json',dict(N=freeze['N'],receipt_sha256=digest(ROOT/'receipts/acd_stage22.json'),utc=time.time()))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['resume','prepare','worker','slot','score']);p.add_argument('--name');p.add_argument('--gpu',type=int)
    a=p.parse_args()
    {'resume':resume,'prepare':prepare,'worker':lambda:worker(a.name),'slot':lambda:slot(a.gpu),'score':score}[a.mode]()
