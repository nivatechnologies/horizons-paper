"""Generate POST HOC tables and isolated numerical registry from the effect receipt."""
from pathlib import Path
import json,hashlib,re
ROOT=Path(__file__).resolve().parent
RECEIPT='receipts/acd_stage23_pattern_breakdown.json'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def build():
 d=json.loads((ROOT/RECEIPT).read_text());lines=['# Stage 23 per-pattern effect breakdown','', 'Every value and table is POST HOC and descriptive. No pass rule or confirmation applies. No realized outcomes were opened.','', 'D1 repeats the closeout training batch. It is in-sample for weight zero and every corrected-recipe weight, and is not training data for retained CNN-noF or CNN-F. The initial state is untrained. D2 is the response-model validation set used for checkpoint and weight selection. CNN-F has true forcing supplied.','']
 for ds,models in d['datasets'].items():
  lines += [f'## {ds}: POST HOC, descriptive','', '| Model | Pattern-0 RMSE | Seven-pattern RMSE | Pattern-0 predict-zero RMSE | Seven-pattern predict-zero RMSE |','|---|---:|---:|---:|---:|']
  for name,e in models.items():
   p=e['pooled'];a=p['pattern_0'];b=p['seven_zero_mean'];lines.append(f"| {name} | {a['effect_RMSE']:.9g} | {b['effect_RMSE']:.9g} | {a['predict_zero_RMSE']:.9g} | {b['predict_zero_RMSE']:.9g} |")
  lines.append('')
 lines+=['## Full per-pattern tables: POST HOC, descriptive','']
 for ds,models in d['datasets'].items():
  for name,e in models.items():
   lines += [f'### {ds}: {name} — POST HOC, descriptive','', '| Pattern or pool | RMSE | Bias | Sign agreement | Correlation | Predict-zero RMSE |','|---|---:|---:|---:|---:|---:|']
   for label,m in list(e['per_pattern'].items())+list(e['pooled'].items()):
    vals=[m[k] for k in ['effect_RMSE','mean_bias','sign_agreement','correlation','predict_zero_RMSE']];lines.append('| '+label+' | '+' | '.join('unavailable' if v is None else format(v,'.12g') for v in vals)+' |')
   lines.append('')
 lines+=['## Reproduction: POST HOC, descriptive execution checks','', '| Dataset | Model | Maximum absolute difference | Exact reproduction |','|---|---|---:|---|']
 for a in d['reproduction']:lines.append(f"| {a['dataset']} | {a['model']} | {a['maximum_absolute_difference']!r} | {a['exact']} |")
 lines += ['', f"Script: acd_stage23_pattern_breakdown.py; SHA-256 {sha(ROOT/'acd_stage23_pattern_breakdown.py')}. Full precision values, batch indices and model/data/code hashes: {RECEIPT}.",'']
 (ROOT/'ACD_STAGE23_PATTERN_BREAKDOWN.md').write_text('\n'.join(lines))
 numbers={}
 def walk(v,k,p):
  if isinstance(v,dict):
   for name,x in v.items():walk(x,k+'_'+name,p+'.'+name)
  elif isinstance(v,list):
   for i,x in enumerate(v):walk(x,k+'_'+str(i),p+f'[{i}]')
  elif isinstance(v,(int,float)) and not isinstance(v,bool):
   key=re.sub('[^A-Z0-9_]+','_',k.upper());assert key not in numbers;numbers[key]=dict(value=v,receipt=RECEIPT,receipt_path=p)
 walk(d,'ACD_STAGE23_PATTERN_BREAKDOWN','$')
 primary=json.loads((ROOT/'numbers_acd.json').read_text());prior=dict(primary['numbers']);files=[ROOT/'numbers_acd.json',ROOT/'NUMBERS_ACD.md']
 for name in primary['additional_registries']+['numbers_acd_stage23_closeout.json']:
  p=ROOT/name;prior.update(json.loads(p.read_text())['numbers']);files.append(p)
  md=ROOT/('NUMBERS_ACD_'+name.removeprefix('numbers_acd_').removesuffix('.json').upper()+'.md')
  if md.exists():files.append(md)
 assert not set(prior)&set(numbers)
 registry=dict(schema=1,source_hashes={RECEIPT:sha(ROOT/RECEIPT)},numbers=numbers,prior_key_count=len(prior),combined_key_count=len(prior)+len(numbers),prior_registry_files_sha256={str(p.relative_to(ROOT)):sha(p) for p in files})
 (ROOT/'numbers_acd_stage23_pattern_breakdown.json').write_text(json.dumps(registry,separators=(',',':'))+'\n')
 (ROOT/'NUMBERS_ACD_STAGE23_PATTERN_BREAKDOWN.md').write_text('# POST HOC descriptive pattern-breakdown numbers\n\n| Key | Value | Receipt path |\n|---|---:|---|\n'+'\n'.join(f"| {k} | {v['value']!r} | {v['receipt_path']} |" for k,v in numbers.items())+'\n')
 print('PRIOR',len(prior),'NEW',len(numbers),'COMBINED',registry['combined_key_count'])
def check():
 import acd_stage23_closeout_registry as old
 old.RECEIPT=RECEIPT
 expected=old.rows(json.loads((ROOT/RECEIPT).read_text()))['numbers']
 # Numeric traversal is identical; the new registry has its own key namespace.
 expected={k.replace('ACD_STAGE23_CLOSEOUT','ACD_STAGE23_PATTERN_BREAKDOWN',1):v for k,v in expected.items()}
 reg=json.loads((ROOT/'numbers_acd_stage23_pattern_breakdown.json').read_text())
 assert reg['numbers']==expected
 assert reg['source_hashes'][RECEIPT]==sha(ROOT/RECEIPT)
 for p,h in reg['prior_registry_files_sha256'].items():assert sha(ROOT/p)==h,p
 print('PATTERN REGISTRY PASS; prior registry files byte-identical')
if __name__=='__main__':build();check()
