"""Invoke unchanged frozen scoring; publication stays with the guarded publisher."""
import json,sys,time,platform,hashlib
from pathlib import Path
import acd_stage21_priority as f
part=sys.argv[1]
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
d=f.ready();tasks=dict(zip(('R12','R34','descriptive'),f.phases(d)))[part]
marker=f.OUT/(part+'_pushed.json')
if marker.exists():marker.unlink()
f.publish=lambda *args,**kwargs:None
start=time.monotonic();f.partial_score(part,tasks)
(f.OUT/(part+'_sulaco_execution.json')).write_text(json.dumps(dict(host=platform.node(),elapsed_seconds=time.monotonic()-start,scorer_sha256=digest(f.ROOT/'acd_stage21_score.py'),priority_sha256=digest(f.ROOT/'acd_stage21_priority.py'),criteria_changed=False,device='CPU',case_order_unchanged=True),indent=2)+'\n')
