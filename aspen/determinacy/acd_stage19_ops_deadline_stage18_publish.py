import sys,json,argparse,time,hashlib
from pathlib import Path
sys.path.insert(0,'/mnt/niva-array/work/aspen-determinacy-stage19-l3-20261008/aspen/determinacy')
from acd_guarded_publish import publish
r=Path('/mnt/niva-array/work/aspen-determinacy-stage19-20261007/aspen/determinacy');out=r/'runs/stage18'
p=argparse.ArgumentParser();p.add_argument('part',choices=['D','data','C']);a=p.parse_args()
if a.part=='D':
 files=['receipts/acd_stage18_D.json','ACD_STAGE18_READING.md','acd_stage18_derivative_report.py']
 files += [str(p.relative_to(r)) for p in (r/'receipts').glob('acd_stage18_derivatives_*.json')]
 publish(r,'stage18-D',files,[('receipts/acd_stage18_D.json','ACD_POSTHOC_18D')],marker=out/'D_pushed.json')
elif a.part=='data':
 manifest=out/'response_data/manifest.json'
 d=json.loads(manifest.read_text())
 for name,h in d['data_sha256'].items():assert hashlib.sha256((out/'response_data'/name).read_bytes()).hexdigest()==h
 assert hashlib.sha256((out/'response_data/validation_reference.npz').read_bytes()).hexdigest()==d['validation_reference_sha256']
 result=publish(r,'stage18-C-data',['receipts/acd_stage18_response_data.json','runs/stage18/response_data/manifest.json'],[('receipts/acd_stage18_response_data.json','ACD_POSTHOC_18Cdata')],marker=out/'C_data_publication.json')
 (out/'response_data/generation_pushed.json').write_text(json.dumps(dict(commit=result['commit'],manifest_sha256=hashlib.sha256(manifest.read_bytes()).hexdigest()))+'\n')
else:
 sys.path.insert(0,str(r));from acd_stage18_report import run
 status=json.loads((out/'C_reading_ready.json').read_text());names=status['completed_models'];run('C',names)
 models={n:json.loads((r/'receipts'/f'acd_stage18_{n}.json').read_text()) for n in names}
 training={p.parent.name:json.loads(p.read_text()) for p in (out/'training').glob('CNN-noF-response-*/complete.json')}
 result=dict(post_hoc=True,licenses_frozen_route=False,models=models,training=training,execution=status,selection=json.loads((out/'C_selection.json').read_text()) if (out/'C_selection.json').exists() else None)
 (r/'receipts/acd_stage18_C.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
 files=['receipts/acd_stage18_C.json','ACD_STAGE18_READING.md'];files += [f'receipts/acd_stage18_{n}.json' for n in names]
 publish(r,'stage18-C',files,[('receipts/acd_stage18_C.json','ACD_POSTHOC_18C')],marker=out/'C_pushed.json')
