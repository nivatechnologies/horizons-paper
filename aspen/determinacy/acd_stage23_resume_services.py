"""Restore the recorded serving state after an interrupted Stage23 lease."""
from acd_stage23_common import *
import time
sys.path.insert(0,str(FROZEN18))
import acd_stage18_gpu_lease as lease
from acd_stage19_part2_gate import gpu_inventory
lease.OUT=OUT;lease.freeze_ready=ready
ready()
for path in OUT.glob('gpu_service_recovery_*.json'):
 record=json.loads(path.read_text());index=record['gpu']['index']
 if record['was_active']:
  while any('VLLM' not in p['process'].upper() for p in next(c for c in gpu_inventory() if c['index']==index)['processes']):time.sleep(60)
  lease.service('start',record['unit']);assert lease.active(record['unit']);lease.log('gpu_service_restored_before_resume',unit=record['unit'])
 path.unlink()
