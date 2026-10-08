"""Queued Freeze D adapter to unchanged Stage18 rollouts; no realized access."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from acd_stage19_part3b_contract import ROOT, OUT, ready, digest

WORK = OUT/'part3b'


def complete(name):
    directory = OUT/'inference'/name
    if not (directory/'complete.json').exists():
        return False
    row = json.loads((directory/'complete.json').read_text())
    manifest = json.loads((directory/'hashes.json').read_text())
    count = len(list((OUT/'inference_inputs').glob('[0-9][0-9][0-9].npz')))
    if row['cases'] != count or len(manifest) != count:
        raise RuntimeError('Incomplete final manifest: '+name)
    if any(digest(directory/p) != h for p,h in manifest.items()):
        raise RuntimeError('Output hash mismatch: '+name)
    return True


def worker(name):
    freeze = ready()
    row = next(r for r in freeze['tasks'] if r['name'] == name)
    for label in ['checkpoint', 'estimator']:
        if row.get(label) and digest(ROOT/row[label]) != row[label+'_sha256']:
            raise RuntimeError('Selected file hash differs: '+label)
    import acd_stage18_inference as inherited
    old = inherited.guarded()
    # Scientific functions are unchanged. Redirect only the contract accessor
    # and output root; the Stage18 freeze and outputs remain untouched.
    inherited.guarded = lambda: old
    inherited.OUT = OUT
    data = OUT/'inference_inputs'
    if row.get('arm'):
        prepared = WORK/'A_inputs'
        if not prepared.exists():
            raise RuntimeError('Diagnostic inputs are not prepared')
        data = prepared/row['arm']
    start = time.monotonic()
    inherited.run(name, data, ROOT/row['checkpoint'], 256,
                  ROOT/row['estimator'] if row['estimator'] else None,
                  row.get('kind'), row.get('rolling', False))
    target = OUT/'inference'/name/'complete.json'
    result = json.loads(target.read_text())
    result.update(fresh_panel=True, freeze_d=json.loads((OUT/'freeze_d_pushed.json').read_text()),
                  elapsed_seconds=time.monotonic()-start,
                  adapter_sha256=digest(__file__), realized_outcomes_opened=False)
    target.write_text(json.dumps(result, indent=2)+'\n')


def run_task(index, row):
    if complete(row['name']):
        return
    from acd_stage19_part2_gate import gpu_inventory
    while True:
        card = next(c for c in gpu_inventory() if c['index'] == index)
        if all('VLLM' in p['process'].upper() for p in card['processes']):
            break
        time.sleep(60)
    import acd_stage19_gpu_lease as leases
    # Replace the network-refresh gate only, avoiding concurrent FETCH_HEAD.
    leases.freeze_ready = ready
    with leases.lease(index) as card:
        env = dict(os.environ, CUDA_VISIBLE_DEVICES=card['uuid'], OMP_NUM_THREADS='1',
                   OPENBLAS_NUM_THREADS='1')
        with (WORK/(row['name']+'.log')).open('a') as log:
            result = subprocess.run([sys.executable, __file__, 'worker', '--name', row['name']],
                                    cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
    receipt = dict(model=row['name'], exit_code=result.returncode, gpu=card,
                   utc=datetime.now(timezone.utc).isoformat())
    (WORK/(row['name']+'_exit.json')).write_text(json.dumps(receipt, indent=2)+'\n')


def controller():
    freeze = ready()
    WORK.mkdir(exist_ok=True)
    # The complete eight-run L3 manifests are required before any repair begins.
    while not all(complete(f'{m}-seed{i}') for i in range(1,5) for m in ['CNN-F','CNN-noF']):
        (WORK/'queue_status.json').write_text(json.dumps(dict(status='waiting_for_L3_inference',
                utc=datetime.now(timezone.utc).isoformat()))+'\n')
        time.sleep(60)
    import acd_stage18_inference as inherited
    old = inherited.guarded()
    inherited.guarded = lambda: old
    inherited.OUT = WORK
    link = WORK/'confirmation_inputs'
    if not link.exists():
        link.symlink_to(OUT/'inference_inputs', target_is_directory=True)
    inherited.prepare_A()
    phases = [[r for r in freeze['tasks'] if r.get('kind') == 'E0' and 'stored_index' not in r],
              [r for r in freeze['tasks'] if r.get('kind') == 'E1'],
              [r for r in freeze['tasks'] if 'arm' in r],
              [r for r in freeze['tasks'] if 'stored_index' in r]]
    for phase in phases:
        for b in range(0, len(phase), 3):
            with ThreadPoolExecutor(max_workers=3) as pool:
                jobs = [pool.submit(run_task, index, row) for index,row in enumerate(phase[b:b+3])]
                for job in jobs:
                    job.result()
    (WORK/'inference_ready.json').write_text(json.dumps(dict(
        complete=[r['name'] for r in freeze['tasks'] if complete(r['name'])],
        failed=[r['name'] for r in freeze['tasks'] if not complete(r['name'])],
        utc=datetime.now(timezone.utc).isoformat()))+'\n')
    # A separate CPU scoring executable is the sole realized-cache reader.
    python = '/mnt/niva-array/work/aspen-stage19-env-20261007/bin/python'
    subprocess.run([python, '-u', str(ROOT/'acd_stage19_part3b_score.py')], cwd=ROOT, check=True)
    (WORK/'scoring_ready_for_publication.json').write_text(json.dumps(dict(
        utc=datetime.now(timezone.utc).isoformat()))+'\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['controller','worker'])
    parser.add_argument('--name')
    args = parser.parse_args()
    controller() if args.mode == 'controller' else worker(args.name)
