"""Preserve closed-campaign training checkpoints without modifying live workers."""
import datetime,hashlib,json,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'runs/training/closure'

def main():
    manifest=OUT/'ongoing_retention.json'
    data=json.loads(manifest.read_text()) if manifest.exists() else {'versions':{},'current_paths':{}}
    while True:
        for source in sorted((ROOT/'runs/training').glob('*/*.pt')):
            if source.name.startswith('checkpoint_') and not source.with_suffix('.json').exists():continue
            raw=source.read_bytes();sha=hashlib.sha256(raw).hexdigest()
            # Reject observed byte changes; retention makes no completion/selection inference.
            if hashlib.sha256(source.read_bytes()).hexdigest()!=sha:continue
            archive=OUT/'checkpoint_versions'/(sha+'.pt')
            archive.parent.mkdir(parents=True,exist_ok=True)
            if not archive.exists():
                temporary=archive.with_suffix('.tmp');temporary.write_bytes(raw);temporary.replace(archive)
            if hashlib.sha256(archive.read_bytes()).hexdigest()!=sha:raise RuntimeError('archive hash mismatch')
            key=str(source.relative_to(ROOT))
            data['versions'].setdefault(sha,dict(sha256=sha,bytes=len(raw),archive=str(archive.relative_to(ROOT)),
                first_retained_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),original_paths=[],
                interpretation='byte-consistent observed source version; retention only, not a completion or scientific-selection claim'))
            if key not in data['versions'][sha]['original_paths']:data['versions'][sha]['original_paths'].append(key)
            data['current_paths'][key]=sha
        data['recorded_at']=datetime.datetime.now(datetime.timezone.utc).isoformat()
        data['purpose']='retention only; no scientific selection or interpretation; no deletion'
        temporary=manifest.with_suffix('.tmp');temporary.write_text(json.dumps(data,indent=2)+'\n');temporary.replace(manifest)
        time.sleep(5)

if __name__=='__main__':main()
