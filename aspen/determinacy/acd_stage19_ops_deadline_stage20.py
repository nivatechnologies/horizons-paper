import sys,time,json
from pathlib import Path
r=Path('/mnt/niva-array/work/aspen-determinacy-stage20-20261008/aspen/determinacy')
sys.path.insert(0,'/mnt/niva-array/work/aspen-determinacy-stage19-l3-20261008/aspen/determinacy');sys.path.insert(0,str(r))
from acd_guarded_publish import publish
import acd_stage20_finish as f
f.PYTHON='/mnt/niva-array/niva-platform/.venv-cu130/bin/python'
def guarded(part):
 files=[f'receipts/acd_stage20_{part}.json','ACD_STAGE20_READING.md']
 if part=='B':files+=['figures/F22_readability_paper.pdf','figures/F22_readability_paper.png']
 return publish(r,'stage20-'+part,files,[(f'receipts/acd_stage20_{part}.json','ACD_POSTHOC_20'+part)],marker=f.CACHE/(part+'_published.json'))
f.publish=guarded
f.main()
