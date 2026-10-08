"""Retry infrastructure-failed inference; preserve the published failure receipt."""
import sys,json,shutil,time,fcntl
from pathlib import Path
r=Path('/mnt/niva-array/work/aspen-determinacy-stage21-20261008/aspen/determinacy');o=r/'runs/stage21'
sys.path.insert(0,'/mnt/niva-array/work/aspen-determinacy-stage19-l3-20261008/aspen/determinacy');sys.path.insert(0,str(r))
import acd_stage21_priority as f
from acd_guarded_publish import publish
old=json.loads((o/'R12_inference_complete.json').read_text());assert old['failed']
original_receipt=(r/'receipts/acd_stage21_R12.json').read_bytes()
original_marker=(o/'R12_pushed.json').read_bytes()
def publication(step,files,registered=False):
 if step=='R12':
  target=r/'receipts/acd_stage21_R12_recovery.json';shutil.copy2(r/'receipts/acd_stage21_R12.json',target)
  files=[str(target.relative_to(r)) if n=='receipts/acd_stage21_R12.json' else n for n in files]
  receipts=[('receipts/acd_stage21_R12_recovery.json','ACD_21R12_RECOVERY')]
 else:receipts=[]
 return publish(r,'stage21-'+step+'-recovery',files,receipts,marker=o/(step+'_recovery_pushed.json'))['commit']
f.publish=publication
first=f.phases(f.ready())[0];f.baccus(first,'R12_recovery')
from acd_stage21_inference import complete
if not all(complete(t['name']) for t in first):raise RuntimeError('R12 infrastructure retry incomplete; preserve outputs and retry')
with open('/tmp/acd_stage21_scoring.lock','w') as lock:
 fcntl.flock(lock,fcntl.LOCK_EX)
 (o/'R12_pushed.json').unlink()
 try:f.partial_score('R12',first)
 finally:
  (o/'R12_pushed.json').write_bytes(original_marker)
  (r/'receipts/acd_stage21_R12.json').write_bytes(original_receipt)
(o/'R12_recovery_complete.json').write_text(json.dumps({'utc':time.time(),'original_failure_receipt_preserved':True,'criterion_changed':False})+'\n')
