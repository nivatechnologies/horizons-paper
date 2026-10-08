"""Materialize committed run receipts and call the unchanged frozen renderer."""
import hashlib,json,shutil,subprocess,sys
from pathlib import Path
SOURCE=Path('/mnt/niva-array/work/aspen-publication-stage21-R12-execution-correction/aspen/determinacy')
ROOT=Path('/mnt/niva-array/work/aspen-stage16-aggregate-20261008/aspen/determinacy')
ROOT.mkdir(parents=True,exist_ok=True)
for p in ('receipts','figures','runs/stage16','runs/stage9','runs/stage9_training'):(ROOT/p).mkdir(parents=True,exist_ok=True)
script=SOURCE/'acd_stage16_render.py';shutil.copy2(script,ROOT/script.name)
for n in ('acd_stage16_freeze.json','acd_stage9.json','acd_stage13_decisions.json'):shutil.copy2(SOURCE/'receipts'/n,ROOT/'receipts'/n)
provenance={}
for p in sorted((SOURCE/'receipts').glob('acd_stage16_run_*.json')):
 d=json.loads(p.read_text());name=d['run'];provenance[p.name]=hashlib.sha256(p.read_bytes()).hexdigest()
 (ROOT/'runs/stage16'/('metrics_'+name+'.json')).write_text(json.dumps(d['metrics'])+'\n')
 out=ROOT/'runs/stage9_training'/name;out.mkdir(exist_ok=True);(out/'complete.json').write_text(json.dumps(d['training'])+'\n')
p=json.loads((SOURCE/'receipts/acd_stage9.json').read_text())['C']['posterior'];(ROOT/'runs/stage9/metrics_posterior.json').write_text(json.dumps(p)+'\n')
subprocess.run([sys.executable,ROOT/script.name],check=True,cwd=ROOT)
receipt=ROOT/'receipts/acd_stage16.json';d=json.loads(receipt.read_text());assert all(s['scored_runs']==s['planned_runs'] for s in d['model_summaries'].values());d['committed_source_hashes']=provenance;d['aggregation_code_sha256']=hashlib.sha256(script.read_bytes()).hexdigest();receipt.write_text(json.dumps(d,indent=2,allow_nan=False)+'\n')
shutil.copy2(Path(__file__),ROOT/Path(__file__).name)
print(json.dumps(d['model_summaries'],indent=2))
