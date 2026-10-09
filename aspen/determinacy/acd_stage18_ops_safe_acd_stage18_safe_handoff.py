"""Execution-only D-to-C handoff; no scientific code or frozen rule changes."""
import hashlib,json,os,signal,time
from pathlib import Path
R=Path('/mnt/niva-array/work/aspen-determinacy-stage19-20261007/aspen/determinacy')
O=R/'runs/stage18'
H=Path(__file__).resolve().parent
required=['CNN-20k','CNN-F','CNN-noF','CNN-F-E0-fixed-seed1']
while not (H/'stage18_safe_handoff_pushed.json').exists():time.sleep(5)
while not (O/'D_reading_ready.json').exists():time.sleep(5)
for name in required:
    assert (O/'derivatives'/name/'complete.json').exists(),name
    assert (R/'receipts'/f'acd_stage18_derivatives_{name}.json').exists(),name
manifest=O/'response_data/manifest.json'
marker=json.loads((O/'response_data/generation_pushed.json').read_text())
assert hashlib.sha256(manifest.read_bytes()).hexdigest()==marker['manifest_sha256']
# The legacy coordinator has finished all D workers and scorers at this marker.
# Its next instruction would regenerate already committed C data; only stop that coordinator.
stopped=[]
for p in Path('/proc').iterdir():
    if not p.name.isdigit():continue
    try:args=(p/'cmdline').read_bytes().decode().split('\0')
    except (OSError,UnicodeError):continue
    if '/tmp/acd_stage18_after_B.py' in args:
        os.kill(int(p.name),signal.SIGTERM);stopped.append(int(p.name))
record=dict(utc=time.time(),stage='D_to_C_execution_handoff',all_initial_D_outputs_complete=True,
            stopped_legacy_coordinator_pids=stopped,committed_C_manifest_sha256=marker['manifest_sha256'],
            instruction='Supervisor publishes D, then launches unchanged C controller; committed data reused; criteria unchanged.')
(O/'safe_handoff.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record),flush=True)
while not (O/'D_pushed.json').exists():time.sleep(5)
print('D pushed; existing persistent supervisor may launch unchanged C controller.',flush=True)
