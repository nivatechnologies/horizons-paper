"""Stage16 scoring using frozen saved costs; truth access only in scoring functions."""
import importlib.util,json,hashlib
from pathlib import Path
import numpy as np
import acd_stage10b_metrics as metrics
import acd_stage13_analysis as decisions
from acd_stats import r0
ROOT=Path(__file__).resolve().parent

def score_coverage(costs,valid,keep,jbar,null):
 # Truth opened only in this sulaco scoring function.
 actual=np.array([np.load(decisions.RAW/f'conf/score_{c:03d}.npz')['actual_cost'] for c in range(200)])
 summary=decisions.summaries(costs,valid,jbar,null)
 contract=json.loads((ROOT/'receipts/acd_stage16_coverage_contract.json').read_text())
 assert contract['status']=='fixed'
 assert hashlib.sha256((ROOT/contract['code_path']).read_bytes()).hexdigest()==contract['code_sha256']
 spec=importlib.util.spec_from_file_location('coverage_rule',ROOT/contract['code_path'])
 mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 return getattr(mod,contract['function'])(summary,actual,keep)

def score_decisions_and_coverage(name):
 actual=np.array([np.load(decisions.RAW/f'conf/score_{c:03d}.npz')['actual_cost'] for c in range(200)])
 costs,valid,keep=decisions.loadcosts(name)
 rows,_=decisions.decision_rows(actual,costs,valid,keep,decisions.nullsd())
 jbar,null=decisions.frozen()
 d=json.loads((metrics.DEST/f'metrics_{name}.json').read_text())
 d['decisions']=[r for r in rows if r['policy'] in ['E','C_delta_0']]
 contract=ROOT/'receipts/acd_stage16_coverage_contract.json'
 d['matched_coverage']=score_coverage(costs,valid,keep,jbar,null[np.r_[np.arange(8),37]]) if contract.exists() else {'status':'pending committed Stage15A ranking definition'}
 d['uniform_decrease_collapse']={str(r['lead']): bool(r['chosen_actions'][0]==r['cases']) for r in d['decisions'] if r['policy']=='E'}
 (ROOT/f'runs/stage16/metrics_{name}.json').write_text(json.dumps(d,indent=2,allow_nan=False)+'\n')

if __name__=='__main__':
 import sys
 (ROOT/'runs/stage16').mkdir(parents=True,exist_ok=True)
 metrics.run(sys.argv[1])
 score_decisions_and_coverage(sys.argv[1])
