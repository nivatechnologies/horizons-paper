"""Freeze C provenance and namespace checks; never opens outcomes or computes readings."""
from pathlib import Path
import hashlib,json,re,subprocess
ROOT=Path(__file__).resolve().parent
EXPECTED='3436c492cc71fba647822d5e37e363ae135e75742227dc4ddaf38fb99f4882c3'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,r):p.write_text(json.dumps(r,indent=2,allow_nan=False)+'\n')
def compare():
 paths=['acd_stage19_knownF.py','acd_stage15_knownF_source.py'];hashes={p:sha(ROOT/p) for p in paths}
 source=(ROOT/'acd_stage15_knownF.py').read_text();imports='import acd_stage15_knownF_source as known' in source
 r=dict(byte_identical=(ROOT/paths[0]).read_bytes()==(ROOT/paths[1]).read_bytes(),expected_sha256=EXPECTED,hashes=hashes,import_path_verified=imports,stage15_scoring_sha256=sha(ROOT/'acd_stage15_knownF.py'),passed=all(h==EXPECTED for h in hashes.values()) and imports)
 write(ROOT/'receipts/acd_stage19_part3a_comparison.json',r)
 if not r['passed']:raise RuntimeError('R-other: known-forcing implementation differs; K1–K3 withheld pending Todd ruling')
 return r

def seeds():
 names=['acd-stage19-sensitivity','acd-stage19-ties'];ids={s:int.from_bytes(hashlib.sha256(s.encode()).digest()[:8],'little') for s in names}
 prior=set()
 for p in ROOT.glob('*.py'):prior.update(re.findall(r'acd-[A-Za-z0-9_-]+',p.read_text()))
 prior.difference_update(names)
 roots={int.from_bytes(hashlib.sha256(s.encode()).digest()[:8],'little') for s in prior}
 # Also check numeric roots actually recorded by the original protocol and addenda.
 for p in (ROOT/'receipts').glob('*freeze*.json'):
  r=json.loads(p.read_text())
  def walk(v):
   if isinstance(v,dict):
    for k,x in v.items():
     if k in ['namespace_id','seed','id'] and isinstance(x,int):roots.add(x)
     elif k=='ids' and isinstance(x,dict):roots.update(z for z in x.values() if isinstance(z,int))
     else:walk(x)
   elif isinstance(v,list):
    for x in v:walk(x)
  walk(r)
 leaves=[(i,0,0,0,0,0) for i in ids.values()]
 assert len(set(ids.values()))==len(ids) and not set(ids.values())&roots
 assert len(leaves)==len(set(leaves))
 return dict(ids=ids,id_rule='first eight SHA256 bytes, little endian; SeedSequence(namespace ID)',prior_namespace_literals=sorted(prior),prior_root_count=len(roots),new_leaves=leaves,root_disjoint=True,leaves_unique=True)
if __name__=='__main__':compare()
