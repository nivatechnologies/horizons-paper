"""Stage16 matched coverage using the committed Stage15A outcome-independent ranks."""
import json,hashlib
from pathlib import Path
import numpy as np
from acd_stats import r0,log_capital_max
from acd_stage6_analysis import LEADS
ROOT=Path(__file__).resolve().parent

def pooled_bounds(mask,wrong):
 n=mask.sum(1).astype(float);e=(mask&wrong).sum(1).astype(float);used=n>0
 if not used.any():return [0.,1.]
 n=n[used]/mask.shape[1];e=e[used]/mask.shape[1]
 def reject(q,direction):return log_capital_max((e-q*n+1)/2,.5,direction,.05)>=np.log(1/.05)
 def invert(direction):
  low,high=0,1000
  if direction==1:
   if not reject(0.,1):return 0.
   while low<high:
    mid=(low+high+1)//2
    if reject(mid/1000,1):low=mid
    else:high=mid-1
  else:
   if not reject(1.,-1):return 1.
   while low<high:
    mid=(low+high)//2
    if reject(mid/1000,-1):high=mid
    else:low=mid+1
  return low/1000
 return [invert(1),invert(-1)]

def readings(summary,actual,keep):
 path=ROOT/'receipts/acd_stage15_matching.json'
 contract=json.loads((ROOT/'receipts/acd_stage16_coverage_contract.json').read_text())
 assert hashlib.sha256(path.read_bytes()).hexdigest()==contract['source_receipt_sha256']
 source=json.loads(path.read_text());tieorder=np.asarray(source['ranking']['tie_order_case_action_ids']);tierank=np.argsort(tieorder)
 assert len(tieorder)==actual.shape[0]*8 and len(np.unique(tieorder))==len(tieorder)
 rows=[];answer=actual[:,:8]<actual[:,8,None]
 for t in [3,5]:
  p=summary['p'][:,:8,t];wrong=summary['modal'][:,:8,t]!=answer[:,:,t];cases=np.flatnonzero(keep)
  assert np.isfinite(p[keep]).all(),'R-other: nonfinite probabilities cannot be ranked by survivor conditioning'
  for group,ks in [('all_eight',np.arange(8)),('seven_zero_mean',np.arange(1,8))]:
   allowed=np.zeros_like(p,bool);allowed[np.ix_(cases,ks)]=True;ids=np.flatnonzero(allowed.ravel());order=ids[np.lexsort((tierank[ids],-p.ravel()[ids]))]
   for coverage in [.5,.7]:
    take=int(round(coverage*len(order)));selected=np.zeros(p.size,bool);selected[order[:take]]=True;selected=selected.reshape(p.shape)
    mask=selected[keep];bad=wrong[keep];a=r0(mask.sum(1),(mask&~bad).sum(1))
    rows.append(dict(lead=float(LEADS[t]),patterns=group,target_coverage=coverage,questions=len(order),answers=take,selected_case_action_ids=order[:take].tolist(),pooled_error=float(wrong[selected].mean()),case_error=1-a['case_accuracy'] if a['case_accuracy'] is not None else None,case_error_lower95=1-a['case_upper'],case_error_upper95=1-a['case_lower'],pooled_error_bounds_one_sided95=pooled_bounds(mask,bad),accuracy_receipt=a))
 return dict(stage15_ranking_source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),ranking_namespace=source['ranking']['namespace'],count_rule='int(round(target coverage times eligible question count))',rows=rows)
