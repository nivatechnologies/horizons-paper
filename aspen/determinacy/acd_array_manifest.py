"""Hash local arrays for publication without staging their bytes."""
from pathlib import Path
import argparse,json,hashlib
p=argparse.ArgumentParser();p.add_argument('files',nargs='+');a=p.parse_args();rows=[]
for name in a.files:
 f=Path(name);h=hashlib.sha256()
 with f.open('rb') as stream:
  for block in iter(lambda:stream.read(8*1024*1024),b''):h.update(block)
 rows.append(dict(path=str(f),bytes=f.stat().st_size,sha256=h.hexdigest()))
print(json.dumps(dict(files=rows),indent=2))
