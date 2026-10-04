"""Await full prescribed CNN evaluation, then collect and finish diagnostics."""
import os
import subprocess
import time
from common import ROOT,write_json

REPO=ROOT.parents[1]
REMOTE='/home/todd/work/aspen-horizon-20261004/aspen/horizon'

def run(args,env=None):return subprocess.run(args,cwd=REPO,env=env,check=True)

def main():
    while subprocess.run(['ssh','sulaco',f'test -f {REMOTE}/runs/l96/learned/evaluation_complete.json'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode:
        time.sleep(30)
    # Enrichment may still be running on the older frozen diagnostic source.
    # Collect complete raw evidence and derive current diagnostics independently.
    run(['rsync','-a',f'sulaco:{REMOTE}/runs/l96/',str(ROOT/'runs/l96')+'/'])
    source=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()
    env=dict(os.environ,AAH_SOURCE_SHA=source)
    run([str(REPO/'.venv/bin/python'),str(ROOT/'enrich_l96.py')],env)
    run([str(REPO/'.venv/bin/python'),str(ROOT/'posthoc_l96.py')],env)
    run([str(REPO/'.venv/bin/python'),str(ROOT/'manifest.py'),'l96'],env)
    write_json(ROOT/'results/l96_execution_status.json',dict(status='COMPLETE',source_sha=source))

if __name__=='__main__':
    try:main()
    except Exception as exc:
        write_json(ROOT/'results/l96_execution_error.json',dict(error=repr(exc)))
        raise
