"""Distinguish a real worker completion from an externally observed resource stop."""
import datetime, hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def terminal_record(name):
    directory=ROOT/'runs/training'/name
    completed=directory/'training_complete.json'
    if completed.exists():return json.loads(completed.read_text()),completed
    # Exact-count recipes cannot be completed by an external stop.
    if name not in ['CNN-cost','CNN-R2','CNN2-cost','CNN2-R2']:return None,None
    guard=ROOT/'GUARD_STATUS'/(name+'.json')
    if not guard.exists():return None,None
    observed=json.loads(guard.read_text())
    if not observed.get('stop_requested') or observed.get('alive',True):return None,None
    target=directory/'resource_stop.json'
    if not target.exists():
        progress=directory/'progress.json'
        if not progress.exists():return None,None
        log=json.loads(progress.read_text())['log']
        if not log:return None,None
        last=log[-1]
        record=dict(name=name,kind='cost' if name.endswith('cost') else 'r2',
            status='EXTERNALLY_STOPPED',recorded_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            completed_updates_exact=None,completed_updates_lower_bound=last['step'],
            exact_last_step=None,last_recorded_step=last['step'],
            recorded_phase_gpu_seconds_lower_bound=last['charged_gpu_seconds'],
            exact_total_gpu_seconds=None,cap_seconds=observed['cap_seconds'],
            guard_receipt=str(guard.relative_to(ROOT)),
            guard_receipt_sha256=hashlib.sha256(guard.read_bytes()).hexdigest(),
            guard_snapshot=observed,
            scientific_selection_status='pending complete scheduled-checkpoint validation; no candidate omitted',
            completion_receipt_fabricated=False)
        temporary=target.with_suffix('.tmp')
        temporary.write_text(json.dumps(record,indent=2,allow_nan=False)+'\n');temporary.replace(target)
    return json.loads(target.read_text()),target
