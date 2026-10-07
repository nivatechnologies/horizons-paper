"""Durable Stage10b artifact broker; no science data written on SSH-key host."""
import subprocess,sys,json,time,shlex
ROOT="/home/todd/work/aspen-determinacy-stage10b-20261007"
MOD=ROOT+'/aspen/determinacy'
SPARK='/home/todd/work/aspen-stage9-20261006/stage10b'
PY='/home/todd/work/aspen-determinacy-20261005/.venv/bin/python'
MODELS=['CNN-noF','CNN-F-resp-0.01','CNN-F-resp-0.1']
def remote(host,command,check=True,input=None):
 return subprocess.run(['ssh',host,command],text=True,input=input,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=check)
def stream(source,destination):
 pipe=subprocess.Popen(['ssh','192.168.88.4',source],stdout=subprocess.PIPE)
 done=subprocess.run(['ssh','sulaco',destination],stdin=pipe.stdout)
 pipe.stdout.close();assert pipe.wait()==0 and done.returncode==0
def main():
 token=sys.stdin.read().strip();assert token
 while remote('192.168.88.4','test -f '+SPARK+'/queue_complete.json',False).returncode:
  probe="import pathlib,json;p=pathlib.Path('"+SPARK+"/training');print(json.dumps({d.name:(json.loads((d/'progress.json').read_text())[-1] if (d/'progress.json').exists() else 'not started') for d in p.iterdir()}))"
  print(remote('192.168.88.4','python3 -c '+shlex.quote(probe),False).stdout,flush=True)
  time.sleep(30)
 for name in MODELS:
  trained=remote('192.168.88.4','test -f '+SPARK+'/training/'+name+'/complete.json',False).returncode==0
  inferred=remote('192.168.88.4','test -f '+SPARK+'/inference/'+name+'/complete.json',False).returncode==0
  target=MOD+'/runs/stage9_training/'+name
  remote('sulaco','mkdir -p '+target)
  if trained:stream('cd '+SPARK+'/training/'+name+' && tar cf - complete.json selected.pt terminal_loss_balance.json progress.json queue_exit.json','tar xf - -C '+target)
  if trained and remote('192.168.88.4','test -f '+SPARK+'/training/'+name+'/skips.json',False).returncode==0:
   stream('cd '+SPARK+'/training/'+name+' && tar cf - skips.json','tar xf - -C '+MOD+'/runs/stage9_training/'+name)
  if inferred:
   target=MOD+'/runs/stage9/inference/'+name;remote('sulaco','mkdir -p '+target)
   stream('cd '+SPARK+'/inference/'+name+' && tar cf - .','tar xf - -C '+target)
   r=remote('sulaco','cd '+MOD+' && '+PY+' acd_stage10b_metrics.py '+shlex.quote(name));print(r.stdout,r.stderr,flush=True)
  if not trained or not inferred:print('UNAVAILABLE',name,'trained',trained,'inferred',inferred,flush=True)
 validation="import json,pathlib,subprocess\np=pathlib.Path(\"/home/todd/work/aspen-determinacy-stage10b-20261007/aspen/determinacy\")\nbefore=json.loads((p/'numbers_acd.json').read_text())['numbers']\nsubprocess.run(['python3','acd_stage10b_render.py'],cwd=p,check=True)\nsubprocess.run(['python3','acd_numbers.py'],cwd=p,check=True)\nafter=json.loads((p/'numbers_acd.json').read_text())['numbers']\nassert all(k in after and after[k]['value']==v['value'] for k,v in before.items()),'prior values changed'\nsubprocess.run(['python3','check_acd.py'],cwd=p,check=True)\nprint('PRIOR KEYS UNCHANGED',len(before),'NEW TOTAL',len(after))\n"
 r=remote('sulaco','python3 -c '+shlex.quote(validation));print(r.stdout,r.stderr,flush=True)
 paths=['ACD_STAGE10_FAILURE.md','ACD_STAGE10B_TRAINING_FREEZE.md','acd_stage10b_train.py','acd_stage10b_queue.py','acd_stage10b_pipeline.py','acd_stage10b_metrics.py','acd_stage10b_render.py','receipts/acd_stage10_failure.json','receipts/acd_stage10b.json','ACD_STAGE10B_READING.md','acd_numbers.py','numbers_acd.json','NUMBERS_ACD.md']
 remote('sulaco','cd '+ROOT+' && git add '+' '.join(shlex.quote('aspen/determinacy/'+p) for p in paths)+" && git commit -m 'Report guarded emulator control and response-weight sweep'")
 program="import sys,os,subprocess,base64\nsecret=sys.stdin.read().strip();env=os.environ.copy()\nenv.update(GIT_CONFIG_COUNT='1',GIT_CONFIG_KEY_0='http.https://github.com/.extraheader',GIT_CONFIG_VALUE_0='Authorization: Basic '+base64.b64encode(('oauth2:'+secret).encode()).decode())\nroot=\"/home/todd/work/aspen-determinacy-stage10b-20261007\"\nurl='https://github.com/nivatechnologies/horizons-paper.git';ref='refs/heads/paper/aspen-2026-10-determinacy'\nremote=subprocess.check_output(['git','ls-remote',url,ref],cwd=root,env=env).decode().split()[0]\nsubprocess.run(['git','fetch',url,ref],cwd=root,env=env,check=True)\nif subprocess.run(['git','merge-base','--is-ancestor',remote,'HEAD'],cwd=root).returncode:\n subprocess.run(['git','rebase',remote],cwd=root,check=True)\n subprocess.run(['python3','acd_numbers.py'],cwd=root+'/aspen/determinacy',check=True)\n subprocess.run(['python3','check_acd.py'],cwd=root+'/aspen/determinacy',check=True)\n subprocess.run(['git','add','aspen/determinacy/numbers_acd.json','aspen/determinacy/NUMBERS_ACD.md'],cwd=root,check=True)\n if subprocess.run(['git','diff','--cached','--quiet'],cwd=root).returncode:subprocess.run(['git','commit','-m','Refresh guarded sweep registry after rebase'],cwd=root,check=True)\nsubprocess.run(['git','push',url,'HEAD:'+ref],cwd=root,env=env,check=True)\nhead=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root).decode().strip()\nassert subprocess.check_output(['git','ls-remote',url,ref],cwd=root,env=env).decode().split()[0]==head\nprint('VERIFIED',head)\n"
 r=remote('sulaco','python3 -c '+shlex.quote(program),input=token);print(r.stdout,r.stderr,flush=True)
 print('STAGE10B COMPLETE',flush=True)
if __name__=='__main__':main()
