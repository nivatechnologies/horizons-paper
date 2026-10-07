"""Stage16 two-host monitor; training does not depend on matched coverage."""
import json,subprocess,time
from pathlib import Path
HOSTS=['192.168.88.4','192.168.88.12']
SPARK='/home/todd/work/aspen-stage9-20261006/stage16'
MOD='/home/todd/work/aspen-determinacy-stage16-20261007/aspen/determinacy'
PY='/home/todd/work/aspen-determinacy-20261005/.venv/bin/python'
def ssh(host,cmd):return subprocess.run(['ssh',host,cmd],check=True,stdout=subprocess.PIPE,text=True)
def main():
 freeze=json.loads(ssh('sulaco','cat '+MOD+'/receipts/acd_stage16_freeze.json').stdout)
 done=set()
 while len(done)<len(freeze['runs']):
  for r in freeze['runs']:
   name=r['name'];host=r['host']
   if name in done:continue
   if subprocess.run(['ssh',host,'test -f '+SPARK+'/inference/'+name+'/queue_exit.json'],stdout=subprocess.DEVNULL).returncode:continue
   for source,target in [('training','runs/stage9_training'),('inference','runs/stage9/inference')]:
    dest=MOD+'/'+target+'/'+name;ssh('sulaco','mkdir -p '+dest)
    p=subprocess.Popen(['ssh',host,'tar cf - -C '+SPARK+'/'+source+'/'+name+' .'],stdout=subprocess.PIPE)
    q=subprocess.run(['ssh','sulaco','tar xf - -C '+dest],stdin=p.stdout);p.stdout.close();assert p.wait()==0 and q.returncode==0
   q=ssh('sulaco','cd '+MOD+' && '+PY+' acd_stage16_metrics.py '+name)
   print(q.stdout,flush=True)
   ssh('sulaco','mkdir -p '+MOD+'/runs/stage16')
   print(json.dumps(dict(receipt_path='runs/stage16/metrics_'+name+'.json',training_path='runs/stage9_training/'+name+'/complete.json')),flush=True)
   print(json.dumps(dict(status='scored_ready_to_commit',model=name,host=host)),flush=True);done.add(name)
  time.sleep(30)
if __name__=='__main__':main()
