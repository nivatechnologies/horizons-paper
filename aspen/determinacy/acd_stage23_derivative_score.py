"""Redirect the unchanged saved-JVP scorer to Stage23 outputs; no truth access."""
from acd_stage23_common import *
import shutil
sys.path.insert(0,str(FROZEN18))
def run():
 ready()
 import acd_stage18_derivative_readings as source
 original=Path(os.environ.get('ACD_STAGE23_ORIGINAL_ROOT',str(FROZEN18)))
 workspace=OUT/'derivative_workspace';(workspace/'receipts').mkdir(parents=True,exist_ok=True);(workspace/'runs').mkdir(exist_ok=True)
 shutil.copyfile(ROOT/'receipts/acd_stage11_clim_tangent.json',workspace/'receipts/acd_stage11_clim_tangent.json')
 path=workspace/'runs/stage9'
 if not path.exists():path.symlink_to(original/'runs/stage9',target_is_directory=True)
 source.ROOT=workspace;source.OUT=OUT/'original';source.guarded=ready
 source.run('CNN-noF-response-corrected-selected')
 shutil.copyfile(workspace/'receipts/acd_stage18_derivatives_CNN-noF-response-corrected-selected.json',ROOT/'receipts/acd_stage23_derivatives.json')
if __name__=='__main__':run()
