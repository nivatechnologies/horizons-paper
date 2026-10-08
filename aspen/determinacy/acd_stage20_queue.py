"""Stage20-only offline Spark queue; waits for an idle GPU, never preempts jobs."""
import argparse, hashlib, json, subprocess, time, socket
from pathlib import Path
ROOT=Path('/home/todd/work/aspen-stage20-20261008')
IMAGE='nvcr.io/nvidia/pytorch:26.07-py3'
def run(part):
    marker=json.loads((ROOT/'A_pushed.json').read_text())
    contract=json.loads((ROOT/'contract.json').read_text())
    for filename,expected in contract['code_hashes'].items():
        if hashlib.sha256((ROOT/'code'/filename).read_bytes()).hexdigest()!=expected:raise RuntimeError('Code hash mismatch '+filename)
    for filename,expected in contract['checkpoints'].items():
        if hashlib.sha256((ROOT/'models'/filename).read_bytes()).hexdigest()!=expected:raise RuntimeError('Checkpoint hash mismatch '+filename)
    for filename,expected in contract['inputs'].items():
        if hashlib.sha256((ROOT/'inputs'/filename).read_bytes()).hexdigest()!=expected:raise RuntimeError('Original-panel input hash mismatch '+filename)
    tasks=[]
    if part=='B':
        for name in ['physics','CNN-F','CNN-noF']+[f'{m}-seed{i}' for i in range(1,5) for m in ['CNN-F','CNN-noF']]:
            tasks.append((name,['B','--name',name,'--estimators','/models']))
    else:
        for mode in ['fixed','rolling']:
            for j in range(1,6):
                name=f'CNN-F-E0-{mode}-seed{j}';args=['C','--name',name,'--estimator',f'/models/E0-seed{j}/selected.pt','--checkpoint','/models/CNN-F.pt']
                if mode=='rolling':args+=['--rolling']
                tasks.append((name,args))
    outcomes={}
    for name,args in tasks:
        out=ROOT/part/'inference'/name;out.mkdir(parents=True,exist_ok=True)
        if (out/'complete.json').exists():continue
        # Other stages retain ownership of their GPUs until their process exits.
        while True:
            active=subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip()
            if not active:break
            print('Waiting for existing GPU process',active,flush=True);time.sleep(60)
        if part=='B' and name!='physics':args+=['--checkpoint',f'/models/{name}.pt']
        cmd=['docker','run','--rm','--gpus','all','--network','none','--ipc=host',
             '-v',str(ROOT/'code')+':/code:ro','-v',str(ROOT/'models')+':/models:ro',
             '-v',str(ROOT/'inputs')+':/data:ro','-v',str(out)+':/out:rw',
             IMAGE,'python','-u','/code/acd_stage20_gpu.py',*args,'--data','/data','--out','/out','--micro','1024']
        started=time.monotonic()
        with (ROOT/part/(name+'.log')).open('a') as log:
            status=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT).returncode
        outcomes[name]=dict(returncode=status,seconds=time.monotonic()-started,host=socket.gethostname(),completed=(out/'complete.json').exists())
        (ROOT/part/'queue_outcomes.json').write_text(json.dumps(outcomes,indent=2)+'\n');print(name,outcomes[name],flush=True)
    (ROOT/part/'queue_complete.json').write_text(json.dumps(dict(host=socket.gethostname(),outcomes=outcomes))+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('part',choices=['B','C']);run(p.parse_args().part)
