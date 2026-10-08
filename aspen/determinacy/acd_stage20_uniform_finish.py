"""Queue uniform extension after both original Stage20 Spark queues and publish."""
import hashlib,json,os,shlex,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[1]
BASE=Path('/mnt/niva-array/work/aspen-determinacy-stage19-20261007/aspen/determinacy');CACHE=BASE/'runs/stage20_uniform'
REMOTE=Path('/home/todd/work/aspen-stage20-uniform-20261008');PRIOR=Path('/home/todd/work/aspen-stage20-20261008')
PY='/mnt/niva-array/work/aspen-stage19-env-20261007/bin/python';BRANCH='paper/aspen-2026-10-determinacy'
def call(cmd,**kw):return subprocess.run(list(map(str,cmd)),check=True,**kw)
def network(cmd):
 while True:
  p=subprocess.run(list(map(str,cmd)))
  if p.returncode==0:return
  time.sleep(60)
def ssh(host,command):return subprocess.run(['ssh','-o','BatchMode=yes','-o','ConnectTimeout=10',host,command],text=True,capture_output=True)
def git(*a):return subprocess.check_output(['git','-C',str(REPO),*a],text=True).strip()
def setup():
 frozen=json.loads((ROOT/'receipts/acd_stage20_B_uniform_amendment.json').read_text());marker=json.loads((CACHE/'amendment_pushed.json').read_text())
 git('merge-base','--is-ancestor',marker['commit'],'origin/'+BRANCH)
 for p,h in frozen['code_hashes'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
 models=CACHE/'models';models.mkdir(parents=True,exist_ok=True)
 for rel,h in frozen['checkpoints'].items():
  source=BASE/'runs/stage20/models'/rel if not rel.startswith('E1-') else BASE/'runs/stage18/training'/rel
  assert hashlib.sha256(source.read_bytes()).hexdigest()==h,rel
  target=models/rel;target.parent.mkdir(parents=True,exist_ok=True)
  if not target.exists():call(['cp',source,target])
 for host in ['192.168.88.4','192.168.88.12']:
  network(['ssh',host,'mkdir','-p',REMOTE/'code',REMOTE/'models',REMOTE/'inputs'])
  for p in frozen['code_hashes']:network(['scp',ROOT/p,host+':'+str(REMOTE/'code'/p)])
  network(['rsync','-a',str(models)+'/',host+':'+str(REMOTE/'models')+'/'])
  network(['rsync','-a',str(BASE/'runs/stage18/confirmation_inputs')+'/',host+':'+str(REMOTE/'inputs')+'/'])
  network(['scp',ROOT/'receipts/acd_stage20_B_uniform_amendment.json',host+':'+str(REMOTE/'contract.json')])
  network(['scp',CACHE/'amendment_pushed.json',host+':'+str(REMOTE/'amendment_pushed.json')])
def publish():
 import acd_stage20_finish as old
 before=json.loads((ROOT/'numbers_acd.json').read_text())
 old.add_registry('B_uniform');p=ROOT/'acd_numbers.py';s=p.read_text();s=s.replace("filename.endswith(('acd_stage20_B.json','acd_stage20_C.json'))","filename.endswith(('acd_stage20_B.json','acd_stage20_C.json','acd_stage20_B_uniform.json'))")
 s=s.replace("'executions','records','case_records','output_hashes','invalid_cases'","'executions','records','case_records','output_hashes','invalid_cases','source_hashes'")
 p.write_text(s);call([PY,ROOT/'acd_numbers.py']);after=json.loads((ROOT/'numbers_acd.json').read_text());assert all(after['numbers'][k]['value']==v['value'] for k,v in before['numbers'].items());call([PY,ROOT/'check_acd.py'])
 files=['receipts/acd_stage20_B_uniform.json','ACD_STAGE20_READING.md','figures/F22_readability_paper.pdf','figures/F22_readability_paper.png','acd_numbers.py','numbers_acd.json','NUMBERS_ACD.md']
 git('add',*[str(ROOT/p) for p in files]);git('commit','-m','Report Stage20 uniform-decrease context diagnostics');git('fetch','origin',BRANCH);git('rebase','FETCH_HEAD');call([PY,ROOT/'check_acd.py']);sha=git('rev-parse','HEAD')
 p=ROOT/'ACD_PIPELINE_STATUS.md';p.write_text(p.read_text()+f'\nStage20 | B uniform extension | {sha} | {time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())} | Every step/branch and direct uniform D errors reported; registry PASS.\n');git('add',str(p));git('commit','-m','Record Stage20 uniform publication status');network(['git','-C',REPO,'push','origin','HEAD:'+BRANCH]);(CACHE/'published.json').write_text(json.dumps(dict(commit=sha))+'\n')
def main():
 CACHE.mkdir(parents=True,exist_ok=True);setup()
 while True:
  done={host:ssh(host,'test -f '+str(PRIOR/part/'queue_complete.json')).returncode==0 for host,part in [('192.168.88.4','B'),('192.168.88.12','C')]}
  (CACHE/'queue_status.json').write_text(json.dumps(dict(waiting_for_prior_queues=done,utc=time.time()))+'\n')
  if all(done.values()):break
  time.sleep(60)
 p=CACHE/'prior_B_C_complete.json';p.write_text(json.dumps(dict(utc=time.time(),prior_queues=done))+'\n')
 for host,kind in [('192.168.88.4','E0'),('192.168.88.12','E1')]:
  network(['scp',p,host+':'+str(REMOTE/p.name)])
  if not (CACHE/(kind+'_started.json')).exists():
   while True:
    q=ssh(host,f'mkdir -p {REMOTE}/{kind}; nohup python3 -u {REMOTE}/code/acd_stage20_uniform_queue.py {kind} > {REMOTE}/{kind}/queue.log 2>&1 < /dev/null & echo $!')
    if not q.returncode:break
    time.sleep(60)
   (CACHE/(kind+'_started.json')).write_text(json.dumps(dict(host=host,pid=q.stdout.strip()))+'\n')
 while not all(ssh(h,'test -f '+str(REMOTE/k/'queue_complete.json')).returncode==0 for h,k in [('192.168.88.4','E0'),('192.168.88.12','E1')]):time.sleep(60)
 for host,kind in [('192.168.88.4','E0'),('192.168.88.12','E1')]:network(['rsync','-a',host+':'+str(REMOTE/kind)+'/',str(CACHE/kind)+'/'])
 while not all((BASE/f'runs/stage20/{p}_published.json').exists() for p in ['B','C']):time.sleep(60)
 network(['ssh','sulaco','mkdir','-p',REMOTE]);network(['scp',ROOT/'acd_stage20_uniform_readings.py','sulaco:'+str(REMOTE/'readings.py')])
 cmd=['/home/todd/work/aspen-determinacy-20261005/.venv/bin/python',str(REMOTE/'readings.py'),'costs','--science-root','/home/todd/work/aspen-determinacy-stage16-20261007/aspen/determinacy','--stage18','/home/todd/work/aspen-determinacy-stage18-20261007/aspen/determinacy','--stage20-c',str(PRIOR/'C'),'--receipt',str(REMOTE/'direct_costs.json')]
 network(['ssh','sulaco',shlex.join(cmd)]);network(['scp','sulaco:'+str(REMOTE/'direct_costs.json'),CACHE/'direct_costs.json'])
 call([PY,ROOT/'acd_stage20_uniform_readings.py','aggregate','--outputs',CACHE,'--inputs',BASE/'runs/stage18/confirmation_inputs','--costs',CACHE/'direct_costs.json','--base-receipt',ROOT/'receipts/acd_stage20_B.json','--receipt',ROOT/'receipts/acd_stage20_B_uniform.json','--figures',ROOT/'figures','--reading',ROOT/'ACD_STAGE20_READING.md']);publish()
if __name__=='__main__':
 try:main()
 except Exception:
  import traceback
  CACHE.mkdir(parents=True,exist_ok=True);failure=traceback.format_exc();(CACHE/'failure.json').write_text(json.dumps(dict(error=failure))+'\n');print(failure,flush=True);raise
