"""Stage 13 verification and receipt-derived completion record."""
import json,hashlib,subprocess,sys
from pathlib import Path
import numpy as np
from acd_stage13_analysis import ROOT,RAW,forecast_dt,finalize_dt
def run():
 finalize_dt()
 # Independent original-step restart verification, before interpreting changed answers.
 with np.load(RAW/'conf/case_000.npz') as d:
  original=d['J'][:4].copy();got=forecast_dt(d['theta'][:4],.01)
 restart_error=float(np.max(np.abs(got-original)));assert np.array_equal(got,original)
 old=json.load(open(ROOT/'runs/stage13/registry_before.json'))['numbers']
 subprocess.run([sys.executable,'acd_numbers.py'],cwd=ROOT,check=True)
 new=json.load(open(ROOT/'numbers_acd.json'))['numbers']
 changed=[k for k,v in old.items() if k not in new or v['value']!=new[k]['value']]
 assert not changed,changed
 check=subprocess.run([sys.executable,'check_acd.py'],cwd=ROOT,capture_output=True,text=True)
 assert check.returncode==0,check.stdout+check.stderr
 a=json.load(open(ROOT/'receipts/acd_stage13_decisions.json'))
 b=json.load(open(ROOT/'receipts/acd_stage13_dt.json'))
 c=json.load(open(ROOT/'receipts/acd_stage13_instance.json'))
 g=json.load(open(ROOT/'receipts/acd_stage13_evaluator_check.json'))
 assert g['pass_exact']
 from collections import Counter
 records=json.load(open(ROOT/'runs/stage9/receipt_analyses.json'))['A']['A2']['records']
 count=Counter((r[2],r[3]) for r in records if r[2]<r[3]);ties=sum(v==max(count.values()) for v in count.values())
 resolutions=[]
 if ties>1:resolutions.append('R-other: equally frequent illustrative endpoint combinations use lexicographic ordering, then lowest case/action; no outcome-based selection.')
 if b['paired_first_loss']['pairs']!=b['baseline_paired_first_loss']['pairs']:
  resolutions.append('R-other: step halving changes the eligible cohort under the same rule; report recomputed eligibility and the original fixed-cohort sensitivity, without a frozen-route claim.')
 d=dict(stage='Stage 13',post_hoc=True,CPU_only=True,registry_before=len(old),registry_after=len(new),prior_value_changes=changed,registry_check=check.stdout.strip(),restart_original_dt_max_absolute_cost_difference=restart_error,posterior_Stage9_decision_reproduction_rows=a['posterior_stage9_reproduction_rows'],evaluator_CNN_F_exact=g['pass_exact'],illustrative_combination_ties=ties,resolutions=resolutions)
 (ROOT/'receipts/acd_stage13_verification.json').write_text(json.dumps(d,indent=2)+'\n')
 (ROOT/'ACD_STAGE13_STATUS.md').write_text('# Stage 13 complete\n\nPost hoc confirmation; licenses no frozen route. CPU only on sulaco. Spark and Stage 10/10b untouched.\n\n'+json.dumps(d,indent=2)+'\n')
 print(json.dumps(d,indent=2))
if __name__=='__main__':run()
