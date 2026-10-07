"""Resumable Stage18 A/B GPU queue; per-arm scoring remains on Sulaco."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import time
from acd_stage18_inference import ROOT, OUT, guarded, digest

GPU = '/mnt/niva-array/niva-platform/.venv-cu130/bin/python'
SOURCE = 'sulaco:/home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/'


def command(gpu, name, args):
    log = (OUT/(name+'.log')).open('a')
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='4')
    return subprocess.Popen([GPU, '-u', str(ROOT/'acd_stage18_gpu_lease.py'), '--gpu', str(gpu), '--',
                             GPU, '-u', *map(str, args)], cwd=ROOT, env=env, stdin=subprocess.DEVNULL,
                            stdout=log, stderr=subprocess.STDOUT, start_new_session=True)


def batch(tasks):
    """Each wave uses three cards; failures are recorded and do not stop other jobs."""
    outcomes = {}
    for b in range(0, len(tasks), 3):
        jobs = [(name, command(i, name, args)) for i, (name, args) in enumerate(tasks[b:b+3])]
        for name, job in jobs:
            status = job.wait()
            outcomes[name] = dict(exit_code=status, finished_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
            target = OUT/'controller_outcomes.json'
            previous = json.loads(target.read_text()) if target.exists() else {}
            previous.update(outcomes)
            target.write_text(json.dumps(previous, indent=2)+'\n')
    return outcomes


def run(part):
    freeze = guarded()
    # Recovery lane order: learned fresh-panel scoring is committed before Stage18.
    if not (OUT/'stage19_learned_pushed.json').exists():
        raise RuntimeError('Stage19 learned step has not been pushed')
    OUT.mkdir(parents=True, exist_ok=True)
    checkpoint = OUT/'checkpoints/CNN-F.pt'
    if not checkpoint.exists():
        checkpoint.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(['scp', SOURCE+'runs/stage9_training/CNN-F/selected.pt', str(checkpoint)], check=True)
    if digest(checkpoint) != freeze['retained_checkpoints']['CNN-F']:
        raise RuntimeError('Retained CNN-F checkpoint differs from freeze')
    if part == 'A':
        source = OUT/'confirmation_inputs'
        source.mkdir(exist_ok=True)
        subprocess.run(['rsync', '-a', SOURCE+'runs/stage9/evaluation_inputs/', str(source)+'/'], check=True)
        subprocess.run([GPU, str(ROOT/'acd_stage18_inference.py'), 'prepare_A'], check=True, cwd=ROOT)
        tasks = [(f'CNN-F-{arm}', [ROOT/'acd_stage18_inference.py', 'run', '--name', f'CNN-F-{arm}',
                                  '--data', OUT/'A_inputs'/arm, '--checkpoint', checkpoint, '--micro', '256'])
                 for arm in ['ownF', 'meanF', 'constantF', 'permutedF']]
        batch(tasks)
    elif part == 'B':
        tasks = []
        for seed in freeze['seeds']:
            for kind in ['E0', 'E1']:
                name = f'{kind}-seed{seed["index"]}'
                tasks.append((name, [ROOT/'acd_stage18_estimators.py', '--kind', kind, '--seed-index', seed['index'],
                                    '--torch-seed', seed['torch_seed'], '--batch-seed', seed['batch_seed'],
                                    '--data', OUT/'data', '--out', OUT/'training'/name, '--micro', '128']))
        batch(tasks)
        tasks = []
        for seed in freeze['seeds']:
            for kind, rolling in [('E0', False), ('E1', False), ('E1', True)]:
                estimator = OUT/'training'/f'{kind}-seed{seed["index"]}'/'selected.pt'
                name = f'CNN-F-{kind}-{"rolling" if rolling else "fixed"}-seed{seed["index"]}'
                args = [ROOT/'acd_stage18_inference.py', 'run', '--name', name, '--data', OUT/'confirmation_inputs',
                        '--checkpoint', checkpoint, '--estimator', estimator, '--estimator-kind', kind, '--micro', '256']
                if rolling:
                    args.append('--rolling')
                if estimator.exists():
                    tasks.append((name, args))
        batch(tasks)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('part', choices=['A', 'B'])
    run(p.parse_args().part)
