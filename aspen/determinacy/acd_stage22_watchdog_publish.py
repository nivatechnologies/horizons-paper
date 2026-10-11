"""Stage22-only publication handoffs, serialized with the existing publisher."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'runs/stage22'
sys.path.insert(0,'/mnt/niva-array/work/aspen-determinacy-stage19-l3-20261008/aspen/determinacy')
import acd_guarded_publish as publisher

def sync(source,target):
    subprocess.run(['rsync','-a',source,str(target)],check=True)

def publish(step):
    if step=='panel':
        sys.path.insert(0,'/mnt/niva-array/work/aspen-deadline-20261008')
        import acd_stage22_panel_publish
        return acd_stage22_panel_publish.result('panel')
    if step=='inference':
        from acd_stage22_runtime import complete
        tasks=json.loads((ROOT/'receipts/acd_stage22_freeze_f.json').read_text())['tasks']
        assert not (OUT/'FAILED.json').exists()
        assert all(complete(r['name']) for r in tasks)
        files=['runs/stage22/inference_verified.json']
        for row in tasks:
            prefix='runs/stage22/inference/'+row['name']+'/'
            files.extend(prefix+p for p in ['complete.json','hashes.json'])
        files.extend(str(p.relative_to(ROOT)) for p in (OUT/'inference_logs').glob('*') if p.suffix in ['.json','.log'])
        return publisher.publish(ROOT,'stage22-inference',files,marker=OUT/'inference_pushed.json',
            status_message='All Stage22 required GPU tasks completed, exact assigned-case coverage and hashes verified; frozen scoring next.')
    if step=='results':
        remote='sulaco:/home/todd/work/aspen-stage22-panel-20261010/'
        sync(remote+'receipts/acd_stage22.json',ROOT/'receipts/acd_stage22.json')
        sync(remote+'ACD_STAGE22_READING.md',ROOT/'ACD_STAGE22_READING.md')
        sync(remote+'runs/stage22/scoring_complete.json',OUT/'scoring_complete.json')
        sync(remote+'runs/stage22/scoring/access.jsonl',OUT/'scoring_access.jsonl')
        assert not (OUT/'FAILED.json').exists()
        from acd_stage22_runtime import digest
        done=json.loads((OUT/'scoring_complete.json').read_text())
        assert done['receipt_sha256']==digest(ROOT/'receipts/acd_stage22.json')
        # Split the new registry group, leaving the earlier registry values unchanged.
        inherited=publisher.configure_registry
        def configure(root,receipts):
            inherited(root,receipts)
            path=root/'acd_numbers.py';text=path.read_text()
            text=text.replace("groups={'posthoc_menu':", "groups={'stage22': ('ACD_STAGE22',), 'posthoc_menu':")
            path.write_text(text)
        publisher.configure_registry=configure
        return publisher.publish(ROOT,'stage22-results',['receipts/acd_stage22.json','ACD_STAGE22_READING.md',
             'runs/stage22/scoring_complete.json','runs/stage22/scoring_access.jsonl'],
             receipts=[('acd_stage22.json','ACD_STAGE22')],marker=OUT/'results_pushed.json',
             status_message='Stage22 fixed-panel readings published; registry PASS with all prior values unchanged; Stage23 prerequisites now satisfied.')
    if step=='failure':
        incident=json.loads((OUT/'FAILED.json').read_text())
        key=hashlib.sha256(json.dumps(incident,sort_keys=True).encode()).hexdigest()[:12]
        files=['runs/stage22/FAILED.json','runs/stage22/watchdog_events.jsonl']
        files.extend(str(p.relative_to(ROOT)) for p in (OUT/'inference_logs').glob('*') if p.suffix in ['.json','.log'])
        return publisher.publish(ROOT,'stage22-failure-'+key,files,marker=OUT/('failure_'+key+'_pushed.json'),
           status_message='FAILED: '+incident['reason']+'; dependent scoring/publication blocked, criteria unchanged.')
    raise ValueError(step)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('step',choices=['panel','inference','results','failure']);a=p.parse_args();publish(a.step)
