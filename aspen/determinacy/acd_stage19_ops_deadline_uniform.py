import sys
from pathlib import Path
r=Path('/mnt/niva-array/work/aspen-determinacy-stage20-20261008/aspen/determinacy')
sys.path.insert(0,'/mnt/niva-array/work/aspen-determinacy-stage19-l3-20261008/aspen/determinacy');sys.path.insert(0,str(r))
from acd_guarded_publish import publish
import acd_stage20_uniform_finish as f
f.PY='/mnt/niva-array/niva-platform/.venv-cu130/bin/python'
def guarded():
 return publish(r,'stage20-uniform',['receipts/acd_stage20_B_uniform.json','ACD_STAGE20_READING.md','figures/F22_readability_paper.pdf','figures/F22_readability_paper.png'],[('receipts/acd_stage20_B_uniform.json','ACD_POSTHOC_20B_uniform')],marker=f.CACHE/'published.json')
f.publish=guarded
f.main()
