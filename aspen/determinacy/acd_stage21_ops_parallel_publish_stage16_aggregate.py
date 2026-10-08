"""Publish the unchanged saved-output aggregation independently of GPU inference."""
import sys,time,json
from pathlib import Path
H=Path(__file__).resolve().parent;O=Path('/mnt/niva-array/work/aspen-determinacy-stage21-20261008/aspen/determinacy/runs/stage21')
while not (O/'parallel_descriptive_execution_pushed.json').exists():time.sleep(60)
sys.path.insert(0,'/mnt/niva-array/work/aspen-determinacy-stage19-l3-20261008/aspen/determinacy')
import acd_guarded_publish as f
# Keep the new aggregation in a supplemental registry; all run values already have committed keys.
original=f.configure_registry
def configure(root,receipts):
 original(root,receipts)
 p=root/'acd_numbers.py';s=p.read_text().replace("'stage21': ('ACD_21',)","'stage16_aggregate': ('ACD_POSTHOC_STAGE16_AGGREGATE',), 'stage21': ('ACD_21',)")
 s=s.replace("'executions') if filename=='receipts/acd_stage16.json'","'executions','runs','committed_source_hashes') if filename=='receipts/acd_stage16.json'")
 p.write_text(s)
f.configure_registry=configure
r=Path('/mnt/niva-array/work/aspen-stage16-aggregate-20261008/aspen/determinacy')
f.publish(r,'stage16-combined',['acd_stage16_aggregate_committed.py','receipts/acd_stage16.json','ACD_STAGE16_READING.md','figures/F19_seeds_paper.pdf','figures/F19_seeds_paper.png'],[('receipts/acd_stage16.json','ACD_POSTHOC_STAGE16_AGGREGATE')],marker=H/'stage16_aggregate_pushed.json')
