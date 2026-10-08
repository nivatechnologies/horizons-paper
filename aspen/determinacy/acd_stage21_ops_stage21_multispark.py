"""Execution-only matched-seed dispatch to Todd's authorized local GB10 hosts."""
import concurrent.futures,json,subprocess,time,shlex
from pathlib import Path
REMOTE='/home/todd/work/aspen-stage21-20261008'
KEY='/home/todd/.ssh/id_ed25519_todd_192_168_88_248_20261008'
HOSTS={'192.168.88.4':[1,2],'192.168.88.12':[3,4],'192.168.88.248':[5]}
def flags(host):return ['-i',KEY,'-o','IdentitiesOnly=yes'] if host.endswith('.248') else []
def execute(host,command,check=True):
 while True:
  p=subprocess.run(['ssh',*flags(host),'-o','BatchMode=yes','-o','ConnectTimeout=15',host,command],text=True,capture_output=True)
  if p.returncode==255:print('SSH retry after 60 seconds',host,p.stderr,flush=True);time.sleep(60);continue
  if check and p.returncode:raise RuntimeError(host+' '+p.stderr+' '+p.stdout)
  return p

def transfer(host,source,dest,upload=True):
 remote=host+':'+dest
 cmd=['rsync','-a','-e',shlex.join(['ssh',*flags(host),'-o','BatchMode=yes','-o','ConnectTimeout=15'])]
 cmd += [str(source),remote] if upload else [remote,str(source)]
 while subprocess.run(cmd).returncode:time.sleep(60)

def install(f,validate):
 def run_host(host,tasks,contract):
  root=f.OUT/'multispark';root.mkdir(exist_ok=True)
  old_outcomes=execute(host,'cat '+REMOTE+'/queue_outcomes.json',False)
  previous_records=json.loads(old_outcomes.stdout) if old_outcomes.returncode==0 else {}
  execute(host,'mkdir -p '+REMOTE+'/code '+REMOTE+'/models '+REMOTE+'/inputs')
  for name in contract['code_hashes']:transfer(host,f.ROOT/name,REMOTE+'/code/'+name)
  transfer(host,str(f.OUT/'spark_models')+'/',REMOTE+'/models/')
  transfer(host,str(f.OUT/'inference_inputs')+'/',REMOTE+'/inputs/')
  selected=dict(contract,tasks=tasks,hardware='DGX Spark GB10; fixed and rolling for each seed on same host; criteria unchanged')
  file=root/(host+'.contract.json');file.write_text(json.dumps(selected,indent=2)+'\n')
  transfer(host,file,REMOTE+'/contract.json');transfer(host,f.OUT/'reorder_pushed.json',REMOTE+'/reorder_pushed.json')
  # Original dispatch parent is stopped between tasks; completed outputs are reused.
  if host.endswith('.4'):
   old=f.OUT/'spark_started.json'
   if old.exists():
    pid=json.loads(old.read_text())['pid'];execute(host,'kill -TERM '+str(pid)+'; kill -CONT '+str(pid),False)
  if host.endswith('.248'):
   before=execute(host,'systemctl --user is-active tensorfold-single.service',False)
   execute(host,'systemctl --user stop tensorfold-single.service')
   (root/'tensorfold_lease.json').write_text(json.dumps(dict(host=host,service='tensorfold-single.service',previous_state=before.stdout.strip(),authorized_by='Todd',utc=time.time(),restore_after_queue=True))+'\n')
  # No other job is stopped. The unchanged offline queue itself waits for a free GPU.
  execute(host,'rm -f '+REMOTE+'/queue_complete.json; nohup python3 -u '+REMOTE+'/code/acd_stage21_spark.py queue >> '+REMOTE+'/queue.log 2>&1 < /dev/null &')
  while execute(host,'test -f '+REMOTE+'/queue_complete.json',False).returncode:time.sleep(60)
  q=execute(host,'cat '+REMOTE+'/queue_outcomes.json');outcomes=json.loads(q.stdout)
  for task in tasks:
   name=task['name'];dest=f.OUT/'inference'/name;dest.mkdir(parents=True,exist_ok=True)
   transfer(host,str(dest)+'/',REMOTE+'/inference/'+name+'/',False)
   logfile=f.OUT/'priority_logs'/('R34_'+name+'.log');transfer(host,logfile,REMOTE+'/'+name+'.log',False)
   record=outcomes.get(name,previous_records.get(name))
   if record is None:
    # Reused completed output: preserve the original task log and record that no new launch occurred.
    raise RuntimeError('Completed output has no recorded process exit status: '+host+' '+name)
   record=dict(record,model=name,phase='R34',execution_host=host)
   logfile.with_suffix('.json').write_text(json.dumps(record)+'\n')
  if host.endswith('.248'):
   execute(host,'systemctl --user start tensorfold-single.service')
   lease=json.loads((root/'tensorfold_lease.json').read_text());lease.update(restored_utc=time.time());(root/'tensorfold_lease.json').write_text(json.dumps(lease)+'\n')
  return outcomes
 def spark(tasks):
  seal=f.OUT/'multispark_execution_pushed.json'
  if not seal.exists():raise RuntimeError('Multispark execution note must be pushed before dispatch')
  contract=json.loads((f.OUT/'spark_contract.json').read_text())
  names={t['name'] for t in tasks};rows=[t for t in contract['tasks'] if t['name'] in names]
  all_outcomes={}
  with concurrent.futures.ThreadPoolExecutor(max_workers=len(HOSTS)) as pool:
   jobs={host:pool.submit(run_host,host,[t for t in rows if t['seed'] in seeds],contract) for host,seeds in HOSTS.items()}
   for host,job in jobs.items():all_outcomes[host]=job.result()
  (f.OUT/'spark_queue_outcomes.json').write_text(json.dumps(all_outcomes,indent=2)+'\n')
  validate('R34',tasks)
  (f.OUT/'R34_inference_complete.json').write_text(json.dumps(dict(completed=[t['name'] for t in tasks],failed=[],hardware=HOSTS,criteria_changed=False))+'\n')
  files=[]
  for t in tasks:
   files += [str(p.relative_to(f.ROOT)) for p in (f.OUT/'inference'/t['name']).glob('*.json')]
   files += [str((f.OUT/'priority_logs'/('R34_'+t['name']+suffix)).relative_to(f.ROOT)) for suffix in ['.json','.log']]
  files += [str((f.OUT/'R34_execution_gate.json').relative_to(f.ROOT)),str((f.OUT/'spark_queue_outcomes.json').relative_to(f.ROOT))]
  f.publish('R34_inference',files)
 f.spark=spark
