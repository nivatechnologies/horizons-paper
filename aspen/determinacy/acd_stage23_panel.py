"""Route a selected checkpoint through unchanged N-parameterized Stage21 paths."""
from acd_stage23_common import *
import argparse

def configured():
 cfg=ready();sys.path.insert(0,str(PANEL22));os.environ['ACD_STAGE22_BASE']=os.environ.get('ACD_STAGE23_PANEL21BASE','/mnt/niva-array/work/aspen-determinacy-stage21-20261008/aspen/determinacy')
 os.environ['ACD_INHERITED_ROOT']=os.environ.get('ACD_STAGE23_INHERITED','/mnt/niva-array/work/aspen-forecast-decision-20261005/aspen/forecast_decision')
 import acd_stage22_runtime as runtime
 old_ready,contract,_=runtime.configured();record=old_ready()
 selected=json.loads((OUT/'selection.json').read_text())['selected'];checkpoint=OUT/'training'/selected['model']/'selected.pt';assert digest(checkpoint)==selected['checkpoint_sha256']
 name='CNN-noF-response-corrected-selected';task=dict(name=name,checkpoint=str(checkpoint),estimator=None,kind=None,rolling=False,arm=None)
 view=OUT/'fresh22';view.mkdir(parents=True,exist_ok=True)
 source=PANEL22/'runs/stage22'
 for p in source.glob('main_forecast_*.npz'):
  q=view/p.name
  if not q.exists():q.symlink_to(p)
 for name0 in ['climatology','inference_inputs','A_inputs']:
  q=view/name0
  if not q.exists():q.symlink_to(source/name0,target_is_directory=True)
 inference=view/'inference';inference.mkdir(exist_ok=True)
 for row in record['tasks']:
  q=inference/row['name']
  if not q.exists():q.symlink_to(source/'inference'/row['name'],target_is_directory=True)
 scoring=view/'scoring';scoring.mkdir(exist_ok=True);cache=scoring/'actual.npz'
 if not cache.exists():cache.symlink_to(source/'scoring/actual.npz')
 def selected_ready():
  old_ready();ready();return dict(record,tasks=record['tasks']+[task])
 import acd_stage21_freeze_e as e;e.ready=selected_ready
 import acd_stage21_inference as frozen
 frozen.ROOT=ROOT;frozen.OUT=view;frozen.ready=selected_ready
 return frozen,view,name,selected_ready

def infer():
 frozen,view,name,_=configured();frozen.worker(name)
 assert frozen.complete(name)
 write(OUT/'inference_complete.json',dict(model=name,cases=json.loads((view/'inference'/name/'complete.json').read_text())['cases'],checkpoint_sha256=digest(OUT/'training'/json.loads((OUT/'selection.json').read_text())['selected']['model']/'selected.pt')))
if __name__=='__main__':infer()
