from pathlib import Path
import json,hashlib
r=Path(__file__).resolve().parent;o=r/'runs/stage23'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
folders={};name='CNN-noF-response-corrected-selected'
for panel,folder,count in [('stage22',o/'fresh22/inference'/name,json.loads((o/'inference_complete.json').read_text())['cases']),('part3b',o/'fresh19/inference'/name,json.loads((o/'part3b_inference_complete.json').read_text())['cases']),('original_derivative',o/'original/derivatives'/name,json.loads((o/'derivative_inference_complete.json').read_text())['cases'])]:
 meta=json.loads((folder/'complete.json').read_text());hashes=meta.get('output_hashes') or json.loads((folder/'hashes.json').read_text());assert len(hashes)==count
 records=[]
 for path,h in sorted(hashes.items()):
  f=folder/path;assert sha(f)==h,(panel,path);records.append(dict(path=str(f),bytes=f.stat().st_size,sha256=h))
 folders[panel]=dict(cases=count,complete_sha256=sha(folder/'complete.json'),files=records)
record=dict(stage=23,arrays_untracked=True,output_panels=folders,source_code_sha256=sha(Path(__file__)))
(r/'receipts/acd_stage23_outputs.json').write_text(json.dumps(record,indent=2)+'\n')
print('ALL HASHED OUTPUTS VERIFIED', {k:v['cases'] for k,v in folders.items()})
