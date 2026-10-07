"""Durable ordered Lane 2 runner: pushed freeze, histories, parallel GPU inference, CPU scoring."""
import os
import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'runs/stage19'
CPU = '/mnt/niva-array/work/aspen-stage19-env-20261007/bin/python'
GPU = '/mnt/niva-array/niva-platform/.venv-cu130/bin/python'
INHERITED = '/mnt/niva-array/work/aspen-forecast-decision-20261005/aspen/forecast_decision'


def state(status, **extra):
    target = OUT / 'lane2_status.json'
    tmp = target.with_suffix('.tmp.json')
    tmp.write_text(json.dumps(dict(status=status, time=time.time(), **extra), indent=2)+'\n')
    tmp.replace(target)


def run():
    env = dict(os.environ, ACD_INHERITED_ROOT=INHERITED, OPENBLAS_NUM_THREADS='1',
               OMP_NUM_THREADS='1', NUMBA_NUM_THREADS='4')
    while not (OUT / 'freeze_b_pushed.json').exists():
        state('waiting_for_pushed_freeze_b')
        time.sleep(60)
    state('preparing_own_draw_histories')
    subprocess.run([CPU, '-u', str(ROOT/'acd_stage19_inference.py'), 'prepare'],
                   cwd=ROOT, env=env, check=True)
    jobs = []
    for index, name in enumerate(['CNN-F', 'CNN-noF', 'CNN-20k']):
        logfile = (OUT / f'inference_{name}.log').open('a')
        command = [GPU, '-u', str(ROOT/'acd_stage19_gpu_lease.py'), '--gpu', str(index), '--',
                   GPU, '-u', str(ROOT/'acd_stage19_inference.py'), 'run', '--model', name,
                   '--checkpoint', str(OUT/'checkpoints'/f'{name}.pt'), '--micro', '256']
        job = subprocess.Popen(command, cwd=ROOT, env=env, stdin=subprocess.DEVNULL,
                               stdout=logfile, stderr=subprocess.STDOUT, start_new_session=True)
        jobs.append((name, job, logfile))
    state('inference_running', jobs={name: job.pid for name, job, _ in jobs})
    outcomes = {}
    for name, job, logfile in jobs:
        outcomes[name] = job.wait()
        logfile.close()
    state('inference_finished', exit_codes=outcomes)
    if any(outcomes.values()):
        raise RuntimeError('One or more model inference jobs failed; see per-model logs')
    # Scoring is a separate CPU process; all model files have hashes by this point.
    subprocess.run([CPU, '-u', str(ROOT/'acd_stage19_learned.py')], cwd=ROOT, env=env, check=True)
    state('learned_readings_ready_for_registry_and_commit')


if __name__ == '__main__':
    try:
        run()
    except BaseException as error:
        state('failed_resumable', error=repr(error))
        raise
