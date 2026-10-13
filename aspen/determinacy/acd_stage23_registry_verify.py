from pathlib import Path
import json,sys,hashlib,subprocess,re
r=Path(__file__).resolve().parent;sys.path.insert(0,str(r));import acd_numbers
prior=json.loads(Path(__import__('os').environ.get('ACD_STAGE23_PRIOR_REGISTRY','/tmp/acd_stage23_prior_numbers.json')).read_text())
p=r/'receipts/acd_stage23.json';d=json.loads(p.read_text());n=acd_numbers.build()['numbers'];assert all(k in n and n[k]==v for k,v in prior.items())
d['registry_verification']=dict(prior_key_count=len(prior),final_key_count=0,prior_keys_unchanged=True,prior_registry_snapshot_sha256=hashlib.sha256(Path(__import__('os').environ.get('ACD_STAGE23_PRIOR_REGISTRY','/tmp/acd_stage23_prior_numbers.json')).read_bytes()).hexdigest(),prior_commit='4f4c8e8')
info=subprocess.check_output(['pdfinfo',str(r/'figures/F_stage23_training_losses.pdf')],text=True);match=re.search(r'Page size:\s+([0-9.]+) x ([0-9.]+) pts',info);assert match;d['figure_page_sizes_points']={'F_stage23_training_losses':dict(width=float(match[1]),height=float(match[2]))}
d['freeze_g_sha256']=hashlib.sha256((r/'ACD_STAGE23_FREEZE_G.md').read_bytes()).hexdigest()
p.write_text(json.dumps(d,indent=2,allow_nan=False)+'\n')
n=acd_numbers.build()['numbers'];d['registry_verification']['final_key_count']=len(n);p.write_text(json.dumps(d,indent=2,allow_nan=False)+'\n')
acd_numbers.write();n=acd_numbers.build()['numbers'];assert len(n)==d['registry_verification']['final_key_count'];assert all(k in n and n[k]==v for k,v in prior.items())
# Discard obsolete physical shards, retaining all their entries in the new partition.
primary=json.loads((r/'numbers_acd.json').read_text());keep=set(primary['additional_registries'])
for f in r.glob('numbers_acd_*.json'):
 if f.name not in keep:
  md=r/('NUMBERS_ACD_'+f.name.removeprefix('numbers_acd_').removesuffix('.json').upper()+'.md');f.unlink()
  if md.exists():md.unlink()
print('PRIOR KEYS UNCHANGED',len(prior),'FINAL',len(n),'NEW',len(n)-len(prior))
