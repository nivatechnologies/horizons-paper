"""Stage22 health probe: metadata/processes only; never opens hidden arrays."""
import json
import os
from pathlib import Path
import subprocess
import time

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'runs/stage22'

def probe():
    workers=[]
    for p in Path('/proc').glob('[0-9]*'):
        try:
            command=(p/'cmdline').read_bytes().replace(b'\0',b' ').decode(errors='replace')
            if str(ROOT) not in command or not any(x in command for x in ['acd_stage22_panel.py','acd_stage22_runtime.py']):continue
            stat=(p/'stat').read_text().rsplit(')',1)[1].split()
            workers.append(dict(pid=int(p.name),command=command,cpu_ticks=int(stat[11])+int(stat[12])))
        except (OSError,ValueError):pass
    receipt=None
    try:receipt=json.loads((ROOT/'receipts/acd_stage22_part1.json').read_text())
    except (OSError,ValueError):pass
    paths=[p for p in OUT.glob('*') if p.is_file() and p.suffix in ['.npz','.json','.log']]
    recent=max((p.stat().st_mtime for p in paths),default=0)
    units={}
    for name in ['aspen-stage22-blind','aspen-stage22-resume','aspen-stage22-prepare','aspen-stage22-score']:
        s=subprocess.run(['systemctl','--user','show',name+'.service','--property=ActiveState','--property=Result'],capture_output=True,text=True)
        units[name]=dict(x.split('=',1) for x in s.stdout.splitlines() if '=' in x)
    tails={p.name:p.read_text(errors='replace')[-1600:] for p in sorted(OUT.glob('worker_*.log'),key=lambda p:p.stat().st_mtime)[-3:]}
    return dict(utc=time.time(),host=os.uname().nodename,cases_done=len(list(OUT.glob('case_*.json'))),
        observed=len(list(OUT.glob('observed_*.npz'))),last_output_mtime=recent,workers=workers,units=units,
        status=receipt.get('status') if receipt else None,timing=receipt.get('timing_projection') if receipt else None,
        inputs_complete=(OUT/'inputs_complete.json').exists(),scoring_complete=(OUT/'scoring_complete.json').exists(),
        failed_logs=tails)

if __name__=='__main__':print(json.dumps(probe()))
