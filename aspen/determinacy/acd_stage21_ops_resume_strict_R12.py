"""Handoff existing workers without interrupting them, after note publication."""
import json,os,signal,subprocess,time
from pathlib import Path
H=Path(__file__).resolve().parent;R=Path('/mnt/niva-array/work/aspen-determinacy-stage21-20261008/aspen/determinacy');O=R/'runs/stage21'
while not (O/'R12_execution_note_pushed.json').exists() or not (O/'execution_support_pushed.json').exists():time.sleep(60)
workers={1507389:'CNN-F-E0-fixed-seed2',1507402:'CNN-F-E0-fixed-seed1',1507411:'CNN-F-constantF'}
start=time.monotonic();outcomes=[]
while workers:
 for pid,name in list(workers.items()):
  stat=Path('/proc')/str(pid)/'stat'
  if not stat.exists():raise RuntimeError('Existing worker disappeared before its exit status could be recorded: '+name)
  fields=stat.read_text().split()
  if fields[2]!='Z':continue
  rc=os.waitstatus_to_exitcode(int(fields[51]));record=dict(model=name,returncode=rc,phase='R12_recovery',seconds=time.monotonic()-start,timing_scope='handoff observation interval; partial runtime before handoff excluded',exit_status_source=str(stat))
  (O/'priority_logs'/('R12_recovery_'+name+'.json')).write_text(json.dumps(record)+'\n');outcomes.append(record);del workers[pid]
 if workers:time.sleep(60)
(O/'R12_worker_handoff.json').write_text(json.dumps(outcomes,indent=2)+'\n')
for pid in (1507227,1507228,1353087):
 try:os.kill(pid,signal.SIGKILL)
 except ProcessLookupError:pass
for record in O.glob('gpu_service_recovery_*.json'):
 state=json.loads(record.read_text())
 if state['was_active']:subprocess.run(['systemctl','--user','start',state['unit']],check=True)
 record.unlink()
subprocess.run(['systemctl','--user','restart','aspen-deadline-supervisor.service'],check=True)
