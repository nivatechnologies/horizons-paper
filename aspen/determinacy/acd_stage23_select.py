"""Thin adapter to unchanged Stage18 validation selector; no panel outcomes."""
from acd_stage23_common import *
import argparse
sys.path.insert(0,str(FROZEN18))
def select():
 cfg=ready()
 amendment=OUT/'cap_amendment_pushed.json'
 if amendment.exists():
  import time
  while not (OUT/'cap12_completed.json').exists():
   if (OUT/'cap12_FAILED.json').exists():raise RuntimeError('Authorized cap continuation failed; selection blocked')
   time.sleep(60)
 import acd_stage18_select as frozen
 frozen.OUT=OUT
 training=OUT/'training';training.mkdir(parents=True,exist_ok=True)
 baseline=FROZEN18/cfg['weight_zero']['checkpoint_path'];assert digest(baseline)==cfg['weight_zero']['checkpoint_sha256']
 link=training/'CNN-noF-response-0-seed1'
 if not link.exists():link.symlink_to(baseline.parent,target_is_directory=True)
 for w in cfg['weights']:
  p=training/f'CNN-noF-response-{w:g}-seed1';meta=json.loads((p/'complete.json').read_text())
  if meta.get('selected_step') is None:raise RuntimeError('No eligible checkpoint: '+p.name)
  if digest(p/'selected.pt')!=meta['selected_sha256']:raise RuntimeError('Selected checkpoint hash mismatch')
 frozen.select(FROZEN18/'runs/stage18/response_data',training,FROZEN18/'runs/stage18/confirmation_inputs/settings.json',128)
 record=json.loads((OUT/'C_selection.json').read_text());write(OUT/'selection.json',record)
if __name__=='__main__':select()
