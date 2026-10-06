"""Durable Stage10 GPU completion broker; run on SSH-key host, token on stdin.
No broker files, panel data, or model weights are written on the broker host.
"""
import sys,subprocess,time,json,os,base64
ROOT='/home/todd/work/aspen-determinacy-stage4-20261005'
MOD=ROOT+'/aspen/determinacy'
SPARK='/home/todd/work/aspen-stage9-20261006'
PY='/home/todd/work/aspen-determinacy-20261005/.venv/bin/python'
token=sys.stdin.read().strip()
assert token
def remote(host,command,check=True):
 return subprocess.run(['ssh',host,command],check=check,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
def ready(host,path):
 return remote(host,'test -f '+path,False).returncode==0
def run_sulaco(command):
 result=remote('sulaco',command)
 print(result.stdout,flush=True)
 if result.stderr:print(result.stderr,flush=True)
def push():
 env=os.environ.copy()
 env.update(GIT_CONFIG_COUNT='1',GIT_CONFIG_KEY_0='http.https://github.com/.extraheader',GIT_CONFIG_VALUE_0='Authorization: Basic '+base64.b64encode(('oauth2:'+token).encode()).decode())
 # Send the token only to the authorized repository host's Git subprocess.
 import shlex
 program="import sys,os,subprocess,base64\nsecret=sys.stdin.read().strip();env=os.environ.copy()\nenv.update(GIT_CONFIG_COUNT='1',GIT_CONFIG_KEY_0='http.https://github.com/.extraheader',GIT_CONFIG_VALUE_0='Authorization: Basic '+base64.b64encode(('oauth2:'+secret).encode()).decode())\nroot="+repr(ROOT)+"\nurl='https://github.com/nivatechnologies/horizons-paper.git';branch='paper/aspen-2026-10-determinacy'\nsubprocess.run(['git','push',url,'HEAD:refs/heads/'+branch],cwd=root,env=env,check=True)\nhead=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root).decode().strip()\nassert subprocess.check_output(['git','ls-remote',url,'refs/heads/'+branch],cwd=root,env=env).decode().split()[0]==head\nsubprocess.run(['git','update-ref','refs/remotes/origin/'+branch,head],cwd=root,check=True)\nprint('REMOTE VERIFIED',head)"
 result=subprocess.run(['ssh','sulaco','python3 -c '+shlex.quote(program)],input=token,text=True,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 print(result.stdout,result.stderr,flush=True)
def progress():
 r=remote('192.168.88.4','tail -1 '+SPARK+'/training_stage10.log',False)
 print(r.stdout.strip(),flush=True)
broker=remote('sulaco','cat '+MOD+'/acd_stage9_gpu_artifacts.py').stdout
for name in ['CNN-F-resp-0.1','CNN-F-resp-0.01']:
 while not ready('192.168.88.4',SPARK+'/training/'+name+'/complete.json'):
  progress();time.sleep(30)
 subprocess.run([sys.executable,'-c',broker,'F',name],check=True)
 subprocess.run([sys.executable,'-c',broker,'fetch',name],check=True)
 print(name,'selected-checkpoint inference/scoring complete',flush=True)
run_sulaco('cd '+MOD+' && '+PY+' acd_stage10_render.py && python3 acd_numbers.py && python3 check_acd.py')
run_sulaco('cd '+ROOT+" && git add aspen/determinacy/acd_stage10*.py aspen/determinacy/ACD_STAGE10*.md aspen/determinacy/acd_numbers.py aspen/determinacy/NUMBERS_ACD.md aspen/determinacy/numbers_acd.json aspen/determinacy/receipts/acd_stage10* && git commit -m 'Report forcing-conditioned effect-loss weight sweep'")
push()
run_sulaco('cat '+MOD+'/ACD_STAGE10_READING.md')
print('STAGE10 COMPLETE',flush=True)
