"""Durable coordinator, reads finalized checkpoints and writes completion manifest.

No training/selection process imports this module or has access to its outputs.
"""
import json, shlex, subprocess, time
from pathlib import Path
from protocol import ROOT, digest, write_json
REMOTE='/home/todd/work/aspen-forecast-decision-20261005/aspen/forecast_decision'
GPU_LOCK='/home/todd/work/aspen-forecast-decision-20261005/gpu.lock'
PYTHON='/home/todd/niva-datagen/.venv/bin/python'
NUMBA='/home/todd/work/aspen-horizon-20261004/.venv/lib/python3.12/site-packages'
NAMES=['CNN-20k','CNN-5k','CNN-80k','CNN-20k-s2','CNN-20k-s3','CNN-roll','CNN-resp','CNN-R2','CNN-cost']
DIRECTORY=ROOT/'runs/stage2_inference'
DIRECTORY.mkdir(parents=True,exist_ok=True)
def run(args):
    return subprocess.run(args,check=True,capture_output=True,text=True).stdout

def cuts():
    path=DIRECTORY/'cuts.json'
    return json.loads(path.read_text()).get('models',[]) if path.exists() else []

def copy_final(name):
    if name=='CNN-20k':source=ROOT/'inputs/CNN-20k.pt';metadata=None
    else:
        training=ROOT/'runs/training'/name;complete=training/'training_complete.json';source=training/'selected.pt'
        if not complete.exists() or not source.exists():return None
        metadata=json.loads(complete.read_text())
        expected=metadata.get('selected_hash')
        if not expected or expected!=digest(source):return None
        if name in ['CNN-roll','CNN-resp'] and metadata['last_step']!=metadata['prescribed_updates']:
            raise RuntimeError(name+' did not complete its frozen update count')
    destination=ROOT/'runs/evaluation_checkpoints'/name/'selected.pt';destination.parent.mkdir(parents=True,exist_ok=True)
    if destination.exists() and digest(destination)!=digest(source):raise RuntimeError('final artifact mutated: '+name)
    if not destination.exists():
        import shutil
        shutil.copy2(source,destination)
        run(['ssh','sulaco','mkdir -p '+shlex.quote(REMOTE+'/runs/evaluation_checkpoints/'+name)])
        run(['scp',str(destination),'sulaco:'+REMOTE+'/runs/evaluation_checkpoints/'+name+'/selected.pt'])
        if metadata is not None:
            write_json(destination.with_suffix('.training.json'),metadata)
            run(['scp',str(destination.with_suffix('.training.json')),'sulaco:'+REMOTE+'/runs/evaluation_checkpoints/'+name+'/selected.training.json'])
    if name!='CNN-20k':
        normalization=ROOT/'runs/training'/name/'normalization.json'
        if normalization.exists():
            run(['scp',str(normalization),'sulaco:'+REMOTE+'/runs/evaluation_checkpoints/'+name+'/normalization.json'])
    return destination

def evaluate(name,checkpoint,panel,count):
    remote_cp=REMOTE+'/runs/evaluation_checkpoints/'+name+'/selected.pt'
    for case in range(count):
        # Snapshot metadata only; never send any test output to training/selection.
        target=REMOTE+'/runs/'+panel+'/'+name+f'_{case:03d}.npz'
        ready=subprocess.run(['ssh','sulaco','test -f '+shlex.quote(REMOTE+'/runs/'+panel+f'/cpu_{case:03d}.npz')],capture_output=True)
        if ready.returncode:return False
        done=subprocess.run(['ssh','sulaco','test -f '+shlex.quote(target)],capture_output=True)
        needs_timing=(panel=='test' and case<16 and name=='CNN-20k')
        if done.returncode==0 and not needs_timing:continue
        arguments=[PYTHON,'stage2_inference.py','--name',name,'--checkpoint',remote_cp,
                   '--panel',panel,'--case',str(case),'--microbatch','8']
        command='cd '+shlex.quote(REMOTE)+' && flock '+shlex.quote(GPU_LOCK)+' env PYTHONPATH='+shlex.quote(NUMBA)+' '+shlex.join(arguments)
        print(run(['ssh','sulaco',command]),flush=True)
    return True

def main():
    authorization_path=ROOT/'runs/stage2_authorization.json'
    if not authorization_path.exists():raise RuntimeError('root-issued Stage2 authorization required')
    authorization=json.loads(authorization_path.read_text())
    if authorization.get('authorized') is not True or authorization.get('authority')!='WO v5.2 §9':
        raise RuntimeError('Stage2 continuation not authorized')
    for name in ['stage2_inference.py','models.py','protocol.py']:
        run(['scp',str(ROOT/name),'sulaco:'+REMOTE+'/'+name])
    manifest_path=DIRECTORY/'manifest.json'
    manifest=json.loads(manifest_path.read_text()) if manifest_path.exists() else dict(stage=2,arms={},complete=False,
       test_access_agents=['/root/stage2_inference'],frozen_selection_manifest='runs/training/final_selection_stage2.json')
    while True:
        excluded=cuts();manifest['cut_models']=excluded
        for name in NAMES:
            if name in excluded:continue
            record=manifest['arms'].get(name,{})
            checkpoint=copy_final(name)
            if checkpoint is None:continue
            panels=['test'] if name=='CNN-cost' else ['test','test2']
            record['checkpoint_sha256']=digest(checkpoint)
            for panel in panels:
                if panel=='test2' and (DIRECTORY/'cut_secondary.json').exists():
                    record[panel]='cut';continue
                if record.get(panel)=='complete':continue
                if evaluate(name,checkpoint,panel,200 if panel=='test' else 100):record[panel]='complete'
                manifest['arms'][name]=record;write_json(manifest_path,manifest)
            record['complete']=all(record.get(p) in ['complete','cut'] for p in panels)
            manifest['arms'][name]=record;write_json(manifest_path,manifest)
        manifest['complete']=all(n in excluded or manifest['arms'].get(n,{}).get('complete',False) for n in NAMES)
        manifest['updated_at']=time.time();write_json(manifest_path,manifest)
        if manifest['complete']:break
        time.sleep(30)
if __name__=='__main__':main()
