"""Stage23 execution identities and frozen dependency paths."""
from pathlib import Path
import os,sys,json,hashlib
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'runs/stage23'
FROZEN18=Path(os.environ.get('ACD_STAGE23_FROZEN18','/mnt/niva-array/work/aspen-determinacy-stage19-20261007/aspen/determinacy'))
PANEL22=Path(os.environ.get('ACD_STAGE23_PANEL22','/mnt/niva-array/work/aspen-determinacy-stage22-20261010/aspen/determinacy'))
GPU='/mnt/niva-array/niva-platform/.venv-cu130/bin/python'
CPU='/mnt/niva-array/work/aspen-stage19-env-20261007/bin/python'
def digest(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
def write(path,value):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);p=path.with_suffix(path.suffix+'.pending');p.write_text(json.dumps(value,indent=2,allow_nan=False)+'\n');p.replace(path)
def ready():
 if not (OUT/'execution_pushed.json').exists():raise RuntimeError('Stage23 execution identities not pushed')
 cfg=json.loads((ROOT/'receipts/acd_stage23_execution.json').read_text())
 for p,h in cfg['code_hashes'].items():
  if digest(ROOT/p)!=h:raise RuntimeError('Stage23 code hash differs: '+p)
 for p,h in cfg['frozen18_code_hashes'].items():
  if digest(FROZEN18/p)!=h:raise RuntimeError('Stage18 dependency hash differs: '+p)
 assert Path(os.environ.get('ACD_STAGE23_CLEANUP_MARKER',cfg['cleanup_marker'])).exists()
 return cfg
