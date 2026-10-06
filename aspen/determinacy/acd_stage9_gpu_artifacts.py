"""Stage9 GPU broker. Execute via stdin on SSH-key host; no broker files written."""
import subprocess,json,argparse,shlex
SPARK='192.168.88.4';REMOTE='/home/todd/work/aspen-stage9-20261006'
SULACO='/home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy'
def stream(source,destination):
 pipe=subprocess.Popen(['ssh',SPARK,source],stdout=subprocess.PIPE)
 done=subprocess.run(['ssh','sulaco',destination],stdin=pipe.stdout)
 pipe.stdout.close();assert pipe.wait()==0 and done.returncode==0
def transfer_model(name):
 data=subprocess.check_output(['ssh',SPARK,'cat',f'{REMOTE}/training/{name}/complete.json'])
 receipt=json.loads(data);assert receipt['charged_gpu_seconds']<=receipt['cap_seconds'],receipt
 target=f'{SULACO}/runs/stage9_training/{name}'
 subprocess.run(['ssh','sulaco',f'mkdir -p {target}'],check=True)
 stream(f'cd {REMOTE}/training/{name} && tar cf - complete.json selected.pt progress.json',f'tar xf - -C {target}')
 command=f"docker run --rm --gpus all --network none --ipc=host -v {REMOTE}/code:/code:ro -v {REMOTE}/evaluation:/data:ro -v {REMOTE}/training/{name}:/checkpoint:ro -v {REMOTE}/inference:/out nvcr.io/nvidia/pytorch:26.07-py3 python -u /code/acd_stage9_cnn.py --name {name} --checkpoint /checkpoint/selected.pt --data /data --out /out/{name} --micro 1024"
 subprocess.run(['ssh',SPARK,command],check=True)
def fetch_inference(name):
 target=f'{SULACO}/runs/stage9/inference/{name}'
 subprocess.run(['ssh','sulaco',f'mkdir -p {target}'],check=True)
 stream(f'cd {REMOTE}/inference/{name} && tar cf - .',f'tar xf - -C {target}')
 command=f"cd {SULACO} && /home/todd/work/aspen-determinacy-20261005/.venv/bin/python acd_stage9_cnn_metrics.py {shlex.quote(name)}"
 subprocess.run(['ssh','sulaco',command],check=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('part',choices=['F','fetch']);p.add_argument('name');a=p.parse_args()
 transfer_model(a.name) if a.part=='F' else fetch_inference(a.name)
