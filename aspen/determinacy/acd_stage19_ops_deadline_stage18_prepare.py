import sys,json
from pathlib import Path
sys.path.insert(0,'/mnt/niva-array/work/aspen-determinacy-stage19-l3-20261008/aspen/determinacy')
from acd_guarded_publish import publish
r=Path('/mnt/niva-array/work/aspen-determinacy-stage19-20261007/aspen/determinacy');out=r/'runs/stage18'
d=publish(r,'stage18-execution',['acd_stage18_response_controller.py','acd_stage18_derivative_report.py','ACD_STAGE18_C_EXECUTION.md','receipts/acd_stage18_C_execution.json'],marker=out/'C_implementation_publication.json')
code=json.loads((r/'receipts/acd_stage18_C_execution.json').read_text())['code_hashes'];(out/'C_implementation_pushed.json').write_text(json.dumps(dict(commit=d['commit'],code_hashes=code))+'\n')
