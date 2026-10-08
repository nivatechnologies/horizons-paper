"""Committed seed checkpoint adapter to the unchanged Part 2 inference function.
No scoring or realized-outcome access. Serving leases restore their prior state.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import fcntl
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
OUT = ROOT/'runs/stage19'
ORIGINAL = '591f6ce4989b19be4bbda36e6ffa39ecf34940bc513a1770e361b00ee1a7ef6d'
UNITS = {0:'qwen3.8-vllm-mtp@card-a.service',1:'qwen3.8-vllm-mtp@card-b.service',2:'qwen3.8-vllm-mtp@card-c.service'}


def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def receipt(name):
    path = Path('aspen/determinacy/receipts')/f'acd_stage16_run_{name}.json'
    data = subprocess.check_output(['git','show',f'HEAD:{path}'],cwd=REPO)
    local = ROOT/'receipts'/path.name
    if data != local.read_bytes():raise RuntimeError('Receipt differs from committed file')
    commit = subprocess.check_output(['git','log','-1','--format=%H','--',str(path)],cwd=REPO,text=True).strip()
    subprocess.run(['git','merge-base','--is-ancestor',commit,'refs/remotes/origin/paper/aspen-2026-10-determinacy'],cwd=REPO,check=True)
    return json.loads(data),commit


def worker(name, checkpoint):
    if digest(ROOT/'acd_stage19_inference.py') != ORIGINAL:raise RuntimeError('Part 2 inference changed')
    record,commit=receipt(name)
    expected=record['training']['selected_sha256']
    if digest(checkpoint)!=expected:raise RuntimeError('Seed checkpoint hash mismatch')
    import acd_stage19_inference as frozen
    contract=json.loads((ROOT/'receipts/acd_stage19_freeze_b.json').read_text())
    # Only the checkpoint/name allowlist is extended. The frozen run function,
    # model construction, histories, rollout, windows, atomic writes and hashes
    # execute unchanged. No receipt or frozen file is overwritten.
    def loads(s,*a,**kw):
        value=json.loads(s,*a,**kw)
        if value==contract:
            value=dict(value,checkpoints=dict(value['checkpoints'],**{name:expected}))
        return value
    frozen.json=SimpleNamespace(loads=loads,dumps=json.dumps)
    original_gate=frozen.freeze_ready
    def serialized_gate():
        # The inherited gate refreshes FETCH_HEAD. Serialize that metadata
        # operation across seed workers; release before any network rollout.
        lock=OUT/'L3_gate.lock'
        with lock.open('a') as handle:
            fcntl.flock(handle,fcntl.LOCK_EX)
            return original_gate()
    frozen.freeze_ready=serialized_gate
    target=OUT/'inference'/name
    target.mkdir(parents=True,exist_ok=True)
    provenance=dict(model=name,selected_checkpoint_sha256=expected,stage16_commit=commit,
                    inference_source_sha256=ORIGINAL,adapter_sha256=digest(__file__),
                    realized_outcomes_opened=False,utc=datetime.now(timezone.utc).isoformat())
    (target/'seed_provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
    frozen.run(name,checkpoint,256)


def occupied(index):
    from acd_stage19_part2_gate import gpu_inventory
    return next(c for c in gpu_inventory() if c['index']==index)


def active(unit):
    return subprocess.run(['systemctl','--user','is-active','--quiet',unit]).returncode==0


def lane(index,names):
    unit=UNITS[index]
    lease_dir=OUT/'L3_execution';lease_dir.mkdir(exist_ok=True)
    for name in names:
        target=OUT/'inference'/name
        if (target/'complete.json').exists():
            manifest=json.loads((target/'hashes.json').read_text())
            if len(manifest)!=len(list((OUT/'inference_inputs').glob('[0-9][0-9][0-9].npz'))):raise RuntimeError('Incomplete case manifest')
            if any(digest(target/p)!=h for p,h in manifest.items()):raise RuntimeError('Output hash mismatch')
            continue
        while True:
            card=occupied(index)
            if all('VLLM' in p['process'].upper() for p in card['processes']):break
            time.sleep(60)
        was_active=active(unit)
        recovery=lease_dir/f'gpu_recovery_{index}.json'
        recovery.write_text(json.dumps(dict(gpu=card,unit=unit,was_active=was_active,model=name,
            authorization='Todd authorized stopping Baccus vLLM and restoring after GPU work.',
            utc=datetime.now(timezone.utc).isoformat()),indent=2)+'\n')
        try:
            if was_active:subprocess.run(['systemctl','--user','stop',unit],check=True)
            for _ in range(60):
                if occupied(index)['available']:break
                time.sleep(1)
            else:raise RuntimeError('GPU did not become free')
            checkpoint=OUT/'L3_checkpoints'/name/'selected.pt'
            env=dict(os.environ,CUDA_VISIBLE_DEVICES=card['uuid'],OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1')
            with (lease_dir/(name+'.log')).open('a') as log:
                result=subprocess.run([sys.executable,__file__,'worker','--name',name,'--checkpoint',str(checkpoint)],
                    env=env,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT)
            (lease_dir/(name+'_exit.json')).write_text(json.dumps(dict(model=name,returncode=result.returncode,
                gpu=card,utc=datetime.now(timezone.utc).isoformat()),indent=2)+'\n')
        finally:
            if was_active:
                subprocess.run(['systemctl','--user','start',unit],check=True)
                if not active(unit):raise RuntimeError('Serving restoration failed')
            recovery.unlink()


def controller():
    subprocess.run(['git','fetch','origin','paper/aspen-2026-10-determinacy'],cwd=REPO,check=True)
    subprocess.run(['git','merge-base','--is-ancestor','HEAD','FETCH_HEAD'],cwd=REPO,check=True)
    from acd_stage19_part2_gate import freeze_ready
    freeze_ready()
    names=[f'{m}-seed{i}' for i in range(1,5) for m in ['CNN-F','CNN-noF']]
    for name in names:
        record,_=receipt(name)
        checkpoint=OUT/'L3_checkpoints'/name/'selected.pt'
        checkpoint.parent.mkdir(parents=True,exist_ok=True)
        if not checkpoint.exists():
            source='/home/todd/work/aspen-determinacy-stage16-20261007/aspen/determinacy/runs/stage9_training/'+name+'/selected.pt'
            while True:
                result=subprocess.run(['scp','-q','sulaco:'+source,str(checkpoint)])
                if result.returncode==0:break
                time.sleep(60)
        if digest(checkpoint)!=record['training']['selected_sha256']:raise RuntimeError('Checkpoint hash mismatch')
    with ThreadPoolExecutor(max_workers=2) as pool:
        tasks=[pool.submit(lane,index,names[offset::2]) for offset,index in enumerate([1,2])]
        for task in tasks:task.result()


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['controller','worker']);p.add_argument('--name');p.add_argument('--checkpoint',type=Path)
    a=p.parse_args()
    controller() if a.mode=='controller' else worker(a.name,a.checkpoint)
