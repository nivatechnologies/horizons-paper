"""Render the completed frozen scoring receipt without repeating scoring."""
import sys,json,time
from pathlib import Path
r=Path('/mnt/niva-array/work/aspen-determinacy-stage19-20261007/aspen/determinacy');o=r/'runs/stage19/part3b'
assert (o/'inference_ready.json').exists()
sys.path.insert(0,str(r))
import acd_stage19_part3b_report as report
original=report.f
def format_receipt(value):
 if isinstance(value,dict):value=value['mean']
 return original(value)
report.f=format_receipt
assert (r/'receipts/acd_stage19_part3b.json').exists()
report.render()
(o/'scoring_ready_for_publication.json').write_text(json.dumps({'utc':time.time(),'rendered_existing_frozen_scoring_receipt':True})+'\n')
