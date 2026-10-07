"""Recover the CPU launch environment without changing any learned reading."""
import json
import os
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parent
OUT = ROOT/'runs/stage19'
CPU = '/mnt/niva-array/work/aspen-stage19-env-20261007/bin/python'


def run():
    while not (ROOT/'receipts/acd_stage19_learned.json').exists():
        state = json.loads((OUT/'lane2_status.json').read_text())
        complete = all((OUT/'inference'/name/'complete.json').exists()
                       for name in ['CNN-F', 'CNN-noF', 'CNN-20k'])
        if complete and state['status'] == 'failed_resumable':
            env = dict(os.environ, NUMBA_NUM_THREADS='2', OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1',
                       ACD_INHERITED_ROOT='/mnt/niva-array/work/aspen-forecast-decision-20261005/aspen/forecast_decision')
            launcher = "import acd_stage19_learned as m,os,numba;os.environ['NUMBA_NUM_THREADS']='2';numba.set_num_threads(2);m.score()"
            subprocess.run([CPU, '-u', '-c', launcher], cwd=ROOT, env=env, check=True)
            (OUT/'lane2_status.json').write_text(json.dumps(dict(status='learned_readings_ready_for_registry_and_commit',
                                   runtime_recovery=state, time=time.time()), indent=2)+'\n')
            return
        time.sleep(20)


if __name__ == '__main__':
    run()
