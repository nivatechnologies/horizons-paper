"""Durable Stage9 GPU completion broker; run on SSH-key host, token on stdin.
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
def publish(title):
 run_sulaco('cd '+MOD+' && '+PY+' acd_stage9_verify.py && '+PY+' acd_stage9_render.py && python3 acd_numbers.py && python3 check_acd.py && python3 acd_stage9_vault.py')
 import shlex
 run_sulaco('cd '+ROOT+' && git add aspen/determinacy/acd_stage9*.py aspen/determinacy/ACD_STAGE9*.md aspen/determinacy/NUMBERS_ACD.md aspen/determinacy/numbers_acd.json aspen/determinacy/receipts/acd_stage9* aspen/determinacy/figures/F1{1,2,3,4}* && git commit -m '+shlex.quote(title))
 push()
def progress():
 for filename in ['inference.log','training_corrected.log']:
  r=remote('192.168.88.4','tail -1 '+SPARK+'/'+filename,False)
  print(filename,r.stdout.strip(),flush=True)
# Existing-model watcher performs transfer and scoring first.
while True:
 try:
  data=json.loads(remote('sulaco','cat '+MOD+'/receipts/acd_stage9.json').stdout)
  if all('reliability' in data['C'].get(n,{}) for n in ['CNN-20k','CNN-cost']):break
 except (subprocess.CalledProcessError,json.JSONDecodeError,KeyError):pass
 progress();time.sleep(30)
time.sleep(10)
publish('Report Stage 9 statistics, mechanism, existing models and decisions')
print('A-E INTERIM COMMITTED AND PUSHED; F continues',flush=True)
broker=remote('sulaco','cat '+MOD+'/acd_stage9_gpu_artifacts.py').stdout
for name in ['CNN-F','CNN-F-resp']:
 while not ready('192.168.88.4',SPARK+'/training/'+name+'/complete.json'):
  progress();time.sleep(30)
 subprocess.run([sys.executable,'-c',broker,'F',name],check=True)
 subprocess.run([sys.executable,'-c',broker,'fetch',name],check=True)
 print(name,'selected-checkpoint inference/scoring complete',flush=True)
publish('Complete Stage 9 forcing-conditioned emulator evaluation')
run_sulaco('cd '+MOD+" && python3 -c \"import json;d=json.load(open('receipts/acd_stage9.json'));print(json.dumps({'F':d['F'],'C':{n:{k:v for k,v in r.items() if k in ['confidence_readings','state_skill','calibration_test','comparisons','execution']} for n,r in d['C'].items()},'resolutions':d['resolutions']},indent=2))\"")
print('STAGE9 COMPLETE',flush=True)
