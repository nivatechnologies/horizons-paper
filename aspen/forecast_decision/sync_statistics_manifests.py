"""Read-only consumer-manifest transfer from Baccus to sulaco.

Only public FINAL selection metadata and inference completion metadata leave
Baccus. No test output is ever copied into a training/selection machine.
"""
import argparse,datetime,json,subprocess,time
from pathlib import Path
from protocol import ROOT,digest,write_json


def sync(root,destination):
    from compute_metadata import collect
    write_json(root/'runs/statistics_compute_metadata.json',collect(root))
    records=[]
    for rel in ['runs/training/final_selection_stage2.json','runs/training/final_selection_stage2b.json','runs/stage2_inference/manifest.json','runs/statistics_compute_metadata.json','runs/final_scope_authorization.json','runs/training/compute_stage2.json','runs/training/compute_stage2b.json']:
        source=root/rel
        if not source.exists():continue
        data=json.loads(source.read_text())
        if 'final_selection' in rel and data.get('status')!='FINAL':continue
        target=destination+'/'+rel
        subprocess.run(['rsync','--mkpath',str(source),target],check=True,capture_output=True)
        records.append(dict(path=rel,sha256=digest(source)))
    return records


def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--destination',default='sulaco:/home/todd/work/aspen-forecast-decision-20261005/aspen/forecast_decision');p.add_argument('--watch',action='store_true');a=p.parse_args()
    while True:
        stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
        try:records=sync(a.root,a.destination);status=dict(status='SYNCED' if records else 'WAITING',at=stamp,files=records,direction='Baccus public manifests to sulaco only')
        except Exception as exc:status=dict(status='RETRY',at=stamp,error=repr(exc))
        write_json(a.root/'runs/statistics_manifest_sync.json',status)
        if not a.watch:print(json.dumps(status));return
        time.sleep(30)
if __name__=='__main__':main()
