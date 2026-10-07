"""Stage16 two-host observer; training and evaluation do not wait for coverage."""
import json,subprocess,time,traceback
from pathlib import Path
SPARK='/home/todd/work/aspen-stage9-20261006/stage16'
MOD='/home/todd/work/aspen-determinacy-stage16-20261007/aspen/determinacy'
PY='/home/todd/work/aspen-determinacy-20261005/.venv/bin/python'
STATE=Path('/tmp/acd_stage16_recovery_scored.json')
def ssh(host,cmd):return subprocess.run(['ssh',host,cmd],check=True,stdout=subprocess.PIPE,text=True)
def copy_outputs(host,name,source,target):
 dest=MOD+'/'+target+'/'+name;ssh('sulaco','mkdir -p '+dest)
 p=subprocess.Popen(['ssh',host,'tar cf - -C '+SPARK+'/'+source+'/'+name+' .'],stdout=subprocess.PIPE)
 q=subprocess.run(['ssh','sulaco','tar xf - -C '+dest],stdin=p.stdout);p.stdout.close();assert p.wait()==0 and q.returncode==0

def main():
 freeze=json.loads(ssh('sulaco','cat '+MOD+'/receipts/acd_stage16_freeze.json').stdout)
 done=json.loads(STATE.read_text()) if STATE.exists() else {}
 while len(done)<len(freeze['runs']):
  for r in freeze['runs']:
   name=r['name'];host=r['host']
   if name in done:continue
   try:
    probe=subprocess.run(['ssh',host,'cat '+SPARK+'/inference/'+name+'/queue_exit.json'],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True)
    if probe.returncode:continue
    terminal=json.loads(probe.stdout)
    copy_outputs(host,name,'training','runs/stage9_training')
    copy_outputs(host,name,'inference','runs/stage9/inference')
    if terminal['completed']:
     q=ssh('sulaco','cd '+MOD+' && '+PY+' acd_stage16_metrics.py '+name)
     print(q.stdout,flush=True)
     report=ssh('sulaco','cd '+MOD+' && '+PY+' acd_stage16_report_run.py '+name)
     print(report.stdout,flush=True)
     status='scored_ready_to_commit'
    else:status='failed_ready_to_commit'
    record=dict(status=status,model=name,host=host,terminal=terminal,receipt_path='runs/stage16/metrics_'+name+'.json',training_path='runs/stage9_training/'+name+'/complete.json')
    done[name]=record;STATE.write_text(json.dumps(done,indent=2)+'\n');print(json.dumps(record),flush=True)
   except Exception:
    # A transient transport or scoring failure in one run never holds another run.
    print(json.dumps(dict(status='retry_later',model=name,host=host)),flush=True);traceback.print_exc()
  time.sleep(30)
if __name__=='__main__':main()
