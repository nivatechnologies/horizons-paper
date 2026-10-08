"""Copy read-only original-panel inputs/models into isolated Stage20 Spark trees."""
import hashlib,json,subprocess,socket,shlex,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SPARK=Path('/home/todd/work/aspen-stage20-20261008')
OLD=Path('/home/todd/work/aspen-stage9-20261006')
def run(cmd):
    for attempt in range(4):
        p=subprocess.run(cmd)
        if p.returncode==0:return
        if attempt<3:print('Transfer failed; retry after sixty seconds',cmd[0],flush=True);time.sleep(60)
    raise RuntimeError('Transfer failed after retries: '+cmd[0])
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    if socket.gethostname()!='baccus':raise RuntimeError('Prepare on baccus')
    stage=ROOT/'runs/stage20';stage.mkdir(parents=True,exist_ok=True);models=stage/'models';models.mkdir(exist_ok=True)
    for name in ['CNN-F','CNN-noF']:
        source=ROOT/'runs/stage19/checkpoints'/f'{name}.pt';run(['cp',str(source),str(models/f'{name}.pt')])
    for i in range(1,6):
        target=models/f'E0-seed{i}';target.mkdir(exist_ok=True);run(['cp',str(ROOT/f'runs/stage18/training/E0-seed{i}/selected.pt'),str(target/'selected.pt')])
    for i in range(1,5):
        host='sulaco'
        for m in ['CNN-F','CNN-noF']:
            name=f'{m}-seed{i}';run(['scp',host+':'+str(Path('/home/todd/work/aspen-determinacy-stage16-20261007/aspen/determinacy/runs/stage9_training')/name/'selected.pt'),str(models/f'{name}.pt')])
    files=['acd_stage20_gpu.py','acd_stage20_queue.py','acd_stage9_cnn.py','acd_stage9_train.py','acd_stage18_estimators.py']
    contract=dict(panel='original confirmation only',post_hoc=True,A_commit='5af2c1b',
        code_hashes={n:digest(ROOT/n) for n in files},checkpoints={str(p.relative_to(models)):digest(p) for p in models.rglob('*.pt')},
        hardware={'B':'192.168.88.4','C':'192.168.88.12'},container='nvcr.io/nvidia/pytorch:26.07-py3',network='none',
        mounts='Stage20 code/models and original evaluation inputs read-only; only current Stage20 output directory writable',
        inputs={p.name:digest(p) for p in (ROOT/'runs/stage18/confirmation_inputs').glob('*.npz')},
        physics='Same cyclic rhs and float64 RK4 stages, dt .01, five substeps per output; no action, own forcing; network FP32, TF32 off')
    cp=stage/'contract.json';cp.write_text(json.dumps(contract,indent=2)+'\n')
    for host,part in [('192.168.88.4','B'),('192.168.88.12','C')]:
        run(['ssh',host,'mkdir','-p',str(SPARK/'code'),str(SPARK/'models'),str(SPARK/part)])
        for n in files:run(['scp',str(ROOT/n),host+':'+str(SPARK/'code'/n)])
        run(['scp','-r',str(models)+'/.',host+':'+str(SPARK/'models')+'/'])
        run(['scp',str(cp),host+':'+str(SPARK/'contract.json')])
        snippet=f"import json,pathlib; pathlib.Path({str(SPARK/'A_pushed.json')!r}).write_text(json.dumps(dict(commit='5af2c1b')))"
        command=f'ln -sfn {OLD}/evaluation {SPARK}/inputs; python3 -c '+shlex.quote(snippet)
        run(['ssh',host,command])
        (stage/(part+'_prepared.json')).write_text(json.dumps(dict(host=host,contract_sha256=digest(cp)))+'\n')
    (ROOT/'receipts/acd_stage20_execution.json').write_text(json.dumps(contract,indent=2)+'\n')
if __name__=='__main__':main()
