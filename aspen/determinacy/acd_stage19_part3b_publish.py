"""Publish completed Freeze D scoring with receipt registry verification."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from acd_stage19_part3b_contract import ROOT, REPO, OUT, ready


def command(args, network=False):
    while True:
        result = subprocess.run(args, cwd=REPO)
        if result.returncode == 0:
            return
        if not network:
            raise RuntimeError('Command failed: '+str(args))
        time.sleep(60)


def publish():
    work = OUT/'part3b'
    marker = work/'scoring_ready_for_publication.json'
    while not marker.exists():
        time.sleep(60)
    ready()
    tracked = ['ACD_STAGE19_READING.md','receipts/acd_stage19_part3b.json',
               'acd_numbers.py','numbers_acd.json','NUMBERS_ACD.md']
    before = json.loads((ROOT/'numbers_acd.json').read_text())['numbers']
    path = ROOT/'acd_numbers.py'
    text = path.read_text()
    entry = "    stage13_receipts.append(('receipts/acd_stage19_part3b.json', 'ACD_FRESH_19_3B'))\n"
    if entry not in text:
        text = text.replace('    for filename,prefix in stage13_receipts:',
                            entry+'    for filename,prefix in stage13_receipts:')
        text = text.replace("omit=('source_hashes','code_hashes','records','case_records','selected_case_action_ids') if",
            "omit=('source_hashes','code_hashes','first_panel','records','case_records','selected_case_action_ids','case_differences','case_mean_differences','defined_seeds_per_instance','defined_seeds_per_instance','case_indices') if filename.endswith('acd_stage19_part3b.json') else ('source_hashes','code_hashes','records','case_records','selected_case_action_ids') if")
        path.write_text(text)
    command([sys.executable,str(ROOT/'acd_numbers.py')])
    after = json.loads((ROOT/'numbers_acd.json').read_text())['numbers']
    if any(k not in after or after[k]['value'] != v['value'] for k,v in before.items()):
        raise RuntimeError('A prior registry value changed')
    command([sys.executable,str(ROOT/'check_acd.py')])
    if (ROOT/'numbers_acd.json').stat().st_size >= 100*1024*1024:
        raise RuntimeError('Registry exceeds remote file-size limit; preserve receipt and request registry packaging review')
    command(['git','add',*[str((ROOT/p).relative_to(REPO)) for p in tracked]])
    command(['git','commit','-m','Report Stage 19 inferred-context fresh-panel confirmation'])
    sha = subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()
    p = ROOT/'ACD_PIPELINE_STATUS.md'
    p.write_text(p.read_text()+f'\nLane 2 | Stage19 Part3b scoring | {sha} | {datetime.now(timezone.utc).isoformat()} | B1/B2/B3 and all available descriptive pipelines reported; registry PASS with prior values unchanged; Stage18 D/C remain outside this freeze.\n')
    command(['git','add',str(p.relative_to(REPO))])
    command(['git','commit','-m','Record Stage 19 Part3b publication status'])
    command(['git','fetch','origin','paper/aspen-2026-10-determinacy'],network=True)
    command(['git','rebase','FETCH_HEAD'])
    command([sys.executable,str(ROOT/'check_acd.py')])
    command(['git','push','origin','HEAD:paper/aspen-2026-10-determinacy'],network=True)
    report = dict(commit=sha, head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),
                  registry_before=len(before), registry_after=len(after),
                  utc=datetime.now(timezone.utc).isoformat())
    (work/'published.json').write_text(json.dumps(report,indent=2)+'\n')


if __name__ == '__main__':
    try:
        publish()
    except Exception as exc:
        work=OUT/'part3b'; work.mkdir(exist_ok=True)
        (work/'publication_error.json').write_text(json.dumps(dict(error=repr(exc),
            utc=datetime.now(timezone.utc).isoformat()))+'\n')
        raise
