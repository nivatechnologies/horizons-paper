"""Receipt-specific registry supplement; existing registry code and files unchanged."""
from pathlib import Path
import json,hashlib,re,subprocess,sys
ROOT=Path('/mnt/niva-array/work/aspen-determinacy-stage23-20261012/aspen/determinacy')
RECEIPT='receipts/acd_stage23_closeout.json'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rows(d):
 out={}
 def walk(v,key,path):
  if isinstance(v,dict):
   for k,x in v.items():walk(x,key+'_'+k,path+'.'+k)
  elif isinstance(v,list):
   for i,x in enumerate(v):walk(x,key+'_'+str(i),path+f'[{i}]')
  elif isinstance(v,(int,float)) and not isinstance(v,bool):
   key=re.sub('[^A-Z0-9_]+','_',key.upper()).strip('_');assert key not in out
   out[key]=dict(value=v,receipt=RECEIPT,receipt_path=path)
 walk(d,'ACD_STAGE23_CLOSEOUT','$');return dict(schema=1,source_hashes={RECEIPT:sha(ROOT/RECEIPT)},numbers=dict(sorted(out.items())))
def render(d):
 lines=['# Stage23 closeout numbers — dedicated receipt registry','', 'This supplement registers closeout values without modifying existing registry files or frozen code. Existing prior keys are checked by check_acd.py; this supplement is checked by check_acd_stage23_closeout.py.','', '| Key | Full precision | Receipt | Receipt path |','|---|---:|---|---|']
 for k,v in d['numbers'].items():lines.append(f"| {k} | {repr(v['value'])} | {v['receipt']} | {v['receipt_path']} |")
 return '\n'.join(lines)+'\n'
def write():
 primary=json.loads((ROOT/'numbers_acd.json').read_text());old=dict(primary['numbers']);files=[ROOT/'numbers_acd.json',ROOT/'NUMBERS_ACD.md']
 for name in primary['additional_registries']:
  p=ROOT/name;old.update(json.loads(p.read_text())['numbers']);files.extend([p,ROOT/('NUMBERS_ACD_'+name.removeprefix('numbers_acd_').removesuffix('.json').upper()+'.md')])
 before={str(p.relative_to(ROOT)):sha(p) for p in files}
 d=json.loads((ROOT/RECEIPT).read_text());d['stage']=23
 d['registry_verification']=dict(prior_key_count=len(old),closeout_key_count=0,combined_key_count=0,prior_registry_files_sha256=before,prior_keys_unchanged=True,scope='Dedicated closeout supplement; no existing registry code or file changes.')
 (ROOT/RECEIPT).write_text(json.dumps(d,indent=2,allow_nan=False)+'\n');new=rows(d)
 assert not set(new['numbers'])&set(old)
 d['registry_verification'].update(closeout_key_count=len(new['numbers']),combined_key_count=len(old)+len(new['numbers']))
 (ROOT/RECEIPT).write_text(json.dumps(d,indent=2,allow_nan=False)+'\n');new=rows(d);assert len(new['numbers'])==d['registry_verification']['closeout_key_count']
 (ROOT/'numbers_acd_stage23_closeout.json').write_text(json.dumps(new,separators=(',',':'),allow_nan=False)+'\n')
 (ROOT/'NUMBERS_ACD_STAGE23_CLOSEOUT.md').write_text(render(new))
 assert all(sha(ROOT/p)==h for p,h in before.items())
 print('PRIOR',len(old),'CLOSEOUT',len(new['numbers']),'COMBINED',len(old)+len(new['numbers']))
if __name__=='__main__':write()
