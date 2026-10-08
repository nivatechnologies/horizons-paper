"""Todd's execution reorder; frozen scoring and rollout functions stay unchanged."""
import argparse,hashlib,json,os,shlex,subprocess,sys,time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[1];OUT=ROOT/'runs/stage21'
BASE=Path('/mnt/niva-array/work/aspen-determinacy-stage19-20261007/aspen/determinacy')
PY='/mnt/niva-array/work/aspen-stage19-env-20261007/bin/python';GPU='/mnt/niva-array/niva-platform/.venv-cu130/bin/python'
BRANCH='paper/aspen-2026-10-determinacy';REMOTE=Path('/home/todd/work/aspen-stage21-20261008');HOST='192.168.88.4'
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def call(cmd,**kw):return subprocess.run(list(map(str,cmd)),check=True,**kw)
def network(cmd):
 while True:
  p=subprocess.run(list(map(str,cmd)))
  if p.returncode==0:return
  time.sleep(60)
def remote(command):return subprocess.run(['ssh','-o','BatchMode=yes','-o','ConnectTimeout=10',HOST,command],text=True,capture_output=True)
def git(*a):return subprocess.check_output(['git','-C',str(REPO),*a],text=True).strip()
def ready():
 from acd_stage21_freeze_e import ready as frozen
 d=frozen();r=json.loads((ROOT/'receipts/acd_stage21_reorder.json').read_text());marker=json.loads((OUT/'reorder_pushed.json').read_text())
 git('merge-base','--is-ancestor',marker['commit'],'origin/'+BRANCH)
 for p,h in r['code_hashes'].items():assert digest(ROOT/p)==h,p
 return d

def phases(d):
 names=['CNN-F-constantF']+[f'CNN-F-E0-fixed-seed{j}' for j in range(1,6)]+['CNN-noF']
 first=[next(r for r in d['tasks'] if r['name']==n) for n in names]
 second=[r for r in d['tasks'] if r.get('kind')=='E1']
 rest=[r for r in d['tasks'] if r not in first and r not in second]
 return first,second,rest

def registry():
 import acd_stage21_continue as old
 p=ROOT/'acd_numbers.py';s=p.read_text()
 for part,prefix in [('reference','ACD_21REF'),('R12','ACD_21R12'),('R34','ACD_21R34'),('descriptive','ACD_21DESC')]:
  line=f"    stage13_receipts.append(('receipts/acd_stage21_{part}.json', '{prefix}'))\n"
  if line not in s:s=s.replace('    for filename,prefix in stage13_receipts:',line+'    for filename,prefix in stage13_receipts:')
 p.write_text(s);return old.registry()

def publish(step,files,registered=False):
 import acd_stage21_continue as old
 if registered:files=files+registry()
 sha=old.push(step,files)
 (OUT/(step+'_pushed.json')).write_text(json.dumps(dict(commit=sha,utc=time.time()))+'\n');return sha

def reference():
 ready()
 if (OUT/'reference_pushed.json').exists():return
 call([PY,ROOT/'acd_stage21_reference.py'],cwd=ROOT)
 files=['receipts/acd_stage21_reference.json','ACD_STAGE21_READING.md']+[str(p.relative_to(ROOT)) for p in (OUT/'scoring').glob('*.jsonl')]
 publish('reference',files,True)

def partial_score(part,tasks):
 ready();target=ROOT/f'receipts/acd_stage21_{part}.json'
 if (OUT/(part+'_pushed.json')).exists():return
 import acd_stage21_score as frozen
 d=ready();names={r['name'] for r in tasks};d=dict(d,tasks=tasks)
 original_ready=frozen.ready;frozen.ready=lambda:d
 path=ROOT/'ACD_STAGE21_READING.md';previous=path.read_text() if path.exists() else '# Stage21 forcing-shift readings\n'
 try:frozen.score()
 finally:frozen.ready=original_ready
 fresh=json.loads((ROOT/'receipts/acd_stage21.json').read_text());section=path.read_text()
 keys=['R1','R2'] if part=='R12' else ['R3','R4','R4_F7_descriptive','R4_F9_descriptive'] if part=='R34' else []
 fresh['confirmatory']={k:v for k,v in fresh['confirmatory'].items() if k in keys};fresh['part']=part;fresh.setdefault('source_hashes',{})['execution_reorder']=digest(ROOT/'receipts/acd_stage21_reorder.json')
 # The original scorer only returns these tasks; no unavailable future arm is classified.
 fresh['missing_models']=[n for n in fresh['missing_models'] if n in names]
 target.write_text(json.dumps(fresh,indent=2,allow_nan=False)+'\n');(ROOT/'receipts/acd_stage21.json').unlink()
 lines=section.splitlines();table_start=lines.index('| Reading | Estimate | Interval/bound | Result |')
 filtered=[]
 for line in lines[table_start:]:
  if line.startswith('| G') or (line.startswith('| R') and not any(line.startswith('| '+k+' |') for k in keys)):continue
  filtered.append(line)
 path.write_text(previous.rstrip()+f'\n\n## {part} — frozen incremental scoring\n\n'+'\n'.join(filtered)+'\n')
 publish(part,[str(target.relative_to(ROOT)),'ACD_STAGE21_READING.md'],True)

def score_worker(part):
 d=ready();a,b,c=phases(d);partial_score(part,a if part=='R12' else b if part=='R34' else c)

def inference_manifests(part,tasks):
 files=[]
 for row in tasks:
  folder=OUT/'inference'/row['name'];files.extend(str(p.relative_to(ROOT)) for p in folder.glob('*.json'))
 files+= [str(p.relative_to(ROOT)) for p in (OUT/'priority_logs').glob(part+'*.json')]
 publish(part+'_inference',files)

def baccus_task(row,index,phase):
 from acd_stage21_inference import complete
 from acd_stage19_part2_gate import gpu_inventory
 import acd_stage19_gpu_lease as lease
 if complete(row['name']):return
 lease.OUT=OUT;lease.freeze_ready=ready
 while True:
  card=next(c for c in gpu_inventory() if c['index']==index)
  if all('VLLM' in p['process'].upper() for p in card['processes']):break
  time.sleep(60)
 with lease.lease(index) as card:
  directory=OUT/'priority_logs';directory.mkdir(exist_ok=True);start=time.monotonic();env=dict(os.environ,CUDA_VISIBLE_DEVICES=card['uuid'])
  with (directory/(phase+'_'+row['name']+'.log')).open('a') as log:r=subprocess.run([GPU,ROOT/'acd_stage21_inference.py','worker','--name',row['name']],cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT)
  (directory/(phase+'_'+row['name']+'.json')).write_text(json.dumps(dict(model=row['name'],gpu=card,seconds=time.monotonic()-start,returncode=r.returncode,phase=phase))+'\n')

def baccus(tasks,phase):
 from acd_stage21_inference import prepare,complete
 prepare()
 for i in range(0,len(tasks),3):
  with ThreadPoolExecutor(max_workers=3) as pool:
   pending=[pool.submit(baccus_task,row,k,phase) for k,row in enumerate(tasks[i:i+3])]
   for p in pending:p.result()
 missing=[r['name'] for r in tasks if not complete(r['name'])]
 (OUT/(phase+'_inference_complete.json')).write_text(json.dumps(dict(completed=[r['name'] for r in tasks if complete(r['name'])],failed=missing))+'\n')
 inference_manifests(phase,tasks)

def spark(tasks):
 from acd_stage21_inference import prepare,complete
 prepare();files=['acd_stage21_spark.py','acd_stage18_inference.py','acd_stage18_estimators.py','acd_stage9_cnn.py','acd_stage9_train.py'];models=OUT/'spark_models';models.mkdir(exist_ok=True);rows=[]
 for source in tasks:
  row=dict(source)
  for key in ['checkpoint','estimator']:
   p=ROOT/row[key];target=models/p.name
   if not target.exists():call(['cp',p,target])
   assert digest(target)==row[key+'_sha256'];row[key]='models/'+p.name
  rows.append(row)
 contract=dict(tasks=rows,code_hashes={p:digest(ROOT/p) for p in files},inputs={p.name:digest(p) for p in (OUT/'inference_inputs').glob('*') if p.suffix in ['.npz','.json']},hardware='Both E1 fixed and rolling, every seed, on Spark1 GB10; frozen criteria unchanged.')
 p=OUT/'spark_contract.json';p.write_text(json.dumps(contract,indent=2)+'\n')
 while remote('test -f /home/todd/work/aspen-stage20-20261008/B/queue_complete.json').returncode:time.sleep(60)
 network(['ssh',HOST,'mkdir','-p',REMOTE/'code',REMOTE/'models',REMOTE/'inputs'])
 for f in files:network(['scp',ROOT/f,HOST+':'+str(REMOTE/'code'/f)])
 network(['rsync','-a',str(models)+'/',HOST+':'+str(REMOTE/'models')+'/']);network(['rsync','-a',str(OUT/'inference_inputs')+'/',HOST+':'+str(REMOTE/'inputs')+'/']);network(['scp',p,HOST+':'+str(REMOTE/'contract.json')]);network(['scp',OUT/'reorder_pushed.json',HOST+':'+str(REMOTE/'reorder_pushed.json')])
 if not (OUT/'spark_started.json').exists():
  while True:
   q=remote(f'nohup python3 -u {REMOTE}/code/acd_stage21_spark.py queue > {REMOTE}/queue.log 2>&1 < /dev/null & echo $!')
   if not q.returncode:break
   time.sleep(60)
  (OUT/'spark_started.json').write_text(json.dumps(dict(host=HOST,pid=q.stdout.strip()))+'\n')
 while remote('test -f '+str(REMOTE/'queue_complete.json')).returncode:time.sleep(60)
 network(['rsync','-a',HOST+':'+str(REMOTE/'inference')+'/',str(OUT/'inference')+'/']);network(['scp',HOST+':'+str(REMOTE/'queue_outcomes.json'),OUT/'spark_queue_outcomes.json'])
 (OUT/'R34_inference_complete.json').write_text(json.dumps(dict(completed=[r['name'] for r in tasks if complete(r['name'])],failed=[r['name'] for r in tasks if not complete(r['name'])],hardware=HOST))+'\n');inference_manifests('R34',tasks)

def controller():
 d=ready();a,b,c=phases(d)
 # L3 and Part3b remain ahead of Stage21; only Stage18 D/C is moved behind it.
 while not (BASE/'runs/stage19/part3b/inference_ready.json').exists():time.sleep(60)
 baccus(a,'R12');call([PY,ROOT/'acd_stage21_priority.py','score','--part','R12'],cwd=ROOT)
 spark(b);call([PY,ROOT/'acd_stage21_priority.py','score','--part','R34'],cwd=ROOT)
 baccus(c,'descriptive')
 from acd_stage21_inference import complete
 (OUT/'inference_complete.json').write_text(json.dumps(dict(completed=[r['name'] for r in d['tasks'] if complete(r['name'])],failed=[r['name'] for r in d['tasks'] if not complete(r['name'])]))+'\n')
 call([PY,ROOT/'acd_stage21_priority.py','score','--part','descriptive'],cwd=ROOT)

def release_stage18():
 ready()
 while not (OUT/'inference_complete.json').exists():time.sleep(60)
 stage18=BASE/'runs/stage18';marker=stage18/'B_pushed.json'
 if not marker.exists():marker.write_bytes((stage18/'B_publication.json').read_bytes())
 call(['python','-u','/tmp/acd_stage18_after_B.py'],cwd=BASE)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('mode',choices=['reference','controller','score','release_stage18']);p.add_argument('--part',choices=['R12','R34','descriptive']);a=p.parse_args()
 try: reference() if a.mode=='reference' else controller() if a.mode=='controller' else score_worker(a.part) if a.mode=='score' else release_stage18()
 except Exception:
  import traceback
  failure=traceback.format_exc();OUT.mkdir(exist_ok=True);(OUT/('priority_failure_'+a.mode+'.json')).write_text(json.dumps(dict(error=failure,utc=time.time()))+'\n');print(failure,flush=True);raise
