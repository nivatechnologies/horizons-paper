"""Resume CPU scoring after inference completion if its parent exited."""
import subprocess,json,time
from pathlib import Path
r=Path('/mnt/niva-array/work/aspen-determinacy-stage19-20261007/aspen/determinacy');o=r/'runs/stage19/part3b'
assert (o/'inference_ready.json').exists()
subprocess.run(['/mnt/niva-array/work/aspen-stage19-env-20261007/bin/python','-u',r/'acd_stage19_part3b_score.py'],cwd=r,check=True)
(o/'scoring_ready_for_publication.json').write_text(json.dumps({'utc':time.time(),'resumed_after_parent_exit':True})+'\n')
