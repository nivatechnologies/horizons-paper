"""Durable authorized execution, with calibration/chaos barriers before data."""
import json
import os
import shlex
import subprocess
import time
from pathlib import Path
from common import ROOT,write_json

REPO=ROOT.parents[1]
REMOTE='/home/todd/work/aspen-horizon-20261004'
TORCH='/home/todd/niva-datagen/.venv/bin/python'

def run(args,**kwargs):
    print('Running:',shlex.join(map(str,args)),flush=True)
    return subprocess.run(args,cwd=REPO,check=True,**kwargs)

def ssh(command):return run(['ssh','sulaco',command])

def start(args,log,env=None):
    file=(ROOT/'runs'/log).open('w')
    return subprocess.Popen(args,cwd=REPO,stdout=file,stderr=subprocess.STDOUT,env=env)

def copy_cal():
    run(['rsync','-a',f'sulaco:{REMOTE}/aspen/horizon/runs/kolmo/calibration.json',str(ROOT/'results/kolmo_calibration.json')])

def main():
    (ROOT/'runs').mkdir(exist_ok=True)
    while True:
        ready=subprocess.run(['ssh','sulaco',f'test -f {REMOTE}/aspen/horizon/runs/kolmo/calibration.json'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        if ready.returncode==0:break
        time.sleep(30)
    copy_cal();cal=json.loads((ROOT/'results/kolmo_calibration.json').read_text())
    if cal['delta'] is None:
        write_json(ROOT/'results/kolmo_execution_status.json',dict(status='STOP_CALIBRATION_FAIL',calibration=cal))
        print('STOP Kolmogorov: no allowed amplitude clears calibration.',flush=True);return
    source=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()
    env=dict(os.environ,AAH_SOURCE_SHA=source)
    run([str(REPO/'.venv/bin/python'),str(ROOT/'chaos_kolmo.py'),'--device','cuda:0'],env=env)
    cal=json.loads((ROOT/'results/kolmo_calibration.json').read_text())
    gates=json.loads((ROOT/'results/kolmo_action_chaos.json').read_text())
    if cal['status']!='READY_FOR_CALIBRATION_FREEZE_ADDENDUM' or len(gates['gates'])!=6 or not all(g['chaotic'] for g in gates['gates']):
        write_json(ROOT/'results/kolmo_execution_status.json',dict(status='STOP_ACTION_CHAOS',calibration=cal,gates=gates))
        print('STOP Kolmogorov: action chaos gate failed.',flush=True);return
    info=json.loads((ROOT/'runs/kolmo/system.json').read_text())
    text='# Kolmogorov numeric calibration addendum\n\nFrozen after calibration/chaos and before any test-panel or learned-training data.\n\n'
    text+=f"Selected smallest allowed amplitude delta={cal['delta']}. Base lambda={info['lambda_mean']}; total-state RMS sigma={info['sigma']}. Noise uses0.02*sigma, not inherited anomaly sigma_A.\n\n"
    text+='| Delta | Eligible /20 |\n|---|---|\n'
    text+=''.join(f"| {r['delta']} | {r['eligible']} /20 |\n" for r in cal['rows'])
    text+='\n| Action | Lambda mean |95% interval |\n|---|---|---|\n'
    text+=''.join(f"| {g['action']} | {g['lambda_mean']} | {g['lambda_ci95']} |\n" for g in gates['gates'])
    text+='\nAll six strictly positive lower95% bounds pass. Full64-start values retained in source JSON. Seeds, full-window FNO adaptation, objective, grids and optional cuts remain as frozen. Test mechanics are fixed in AAH_FREEZE_KOLMO_EXECUTION_DETAIL.md. No test-derived change.\n'
    freeze=ROOT/'AAH_FREEZE_CALIBRATION_KOLMO.md'
    if freeze.exists():raise FileExistsError('numeric calibration freeze already exists; do not overwrite')
    freeze.write_text(text)
    paths=[str(p.relative_to(REPO)) for p in [freeze,ROOT/'results/kolmo_calibration.json',ROOT/'results/kolmo_action_chaos.json']]
    run(['git','add',*paths]);run(['git','commit','--only','-m','freeze calibrated Kolmogorov amplitude and all-action chaos gates',*paths])
    source=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip();env=dict(os.environ,AAH_SOURCE_SHA=source)
    run(['rsync','-a','--exclude=runs/','--exclude=__pycache__/',str(ROOT)+'/',f'sulaco:{REMOTE}/aspen/horizon/'])
    run([str(REPO/'.venv/bin/python'),str(ROOT/'evaluate_kolmo.py'),'--part','prepare','--device','cuda:0'],env=env)
    run(['rsync','-a',str(ROOT/'runs/kolmo/test/observations.npz'),f'sulaco:{REMOTE}/aspen/horizon/runs/kolmo/test/'])
    remote=f'cd {REMOTE} && AAH_SOURCE_SHA={source} OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 {TORCH} aspen/horizon/truth_kolmo.py --workers 128'
    truth=start(['ssh','sulaco',remote],'kolmo_truth_remote.log',env=env)
    arms=start([str(REPO/'.venv/bin/python'),str(ROOT/'evaluate_kolmo.py'),'--part','arms','--device','cuda:0','--start-case','0','--stop-case','20'],'kolmo_arms.log',env=env)
    write_json(ROOT/'runs/kolmo/launch_manifest.json',dict(source_sha=source,truth_pid=truth.pid,arms_pid=arms.pid))
    run([str(REPO/'.venv/bin/python'),str(ROOT/'evaluate_kolmo.py'),'--part','targets','--device','cuda:1'],env=env)
    run([str(REPO/'.venv/bin/python'),str(ROOT/'climatology_kolmo.py'),'--device','cuda:1'],env=env)
    run([str(REPO/'.venv/bin/python'),str(ROOT/'learned_kolmo_data.py'),'--device','cuda:1','--chunk','256'],env=env)
    run([str(REPO/'.venv/bin/python'),str(ROOT/'train_kolmo.py'),'--device','cuda:1','--microbatch','32'],env=env)
    run([str(REPO/'.venv/bin/python'),str(ROOT/'evaluate_kolmo_neural.py'),'--device','cuda:1','--members-per-batch','16'],env=env)
    run([str(REPO/'.venv/bin/python'),str(ROOT/'evaluate_kolmo.py'),'--part','arms','--device','cuda:1','--start-case','20','--stop-case','30'],env=env)
    for name,proc in [('truth',truth),('arms',arms)]:
        status=proc.wait()
        if status:raise RuntimeError(f'{name} failed exit{status}; see retained log')
    run(['rsync','-a',f'sulaco:{REMOTE}/aspen/horizon/runs/kolmo/test/',str(ROOT/'runs/kolmo/test')+'/'])
    run([str(REPO/'.venv/bin/python'),str(ROOT/'analyze_kolmo.py'),'--workers','16'],env=env)
    write_json(ROOT/'results/kolmo_execution_status.json',dict(status='COMPLETE',source_sha=source))
    print('Kolmogorov mandatory execution complete.',flush=True)

if __name__=='__main__':
    try:main()
    except Exception as exc:
        write_json(ROOT/'results/kolmo_execution_error.json',dict(error=repr(exc)))
        raise
