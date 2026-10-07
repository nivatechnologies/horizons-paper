"""Score supplied per-case J arrays on the fixed post hoc confirmation questions.
Realized outcomes are opened only by the imported scoring functions on sulaco.
No propagation, fitting, training or checkpoint selection is performed.
"""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',JAX_PLATFORMS='cpu',JAX_ENABLE_X64='true')
import argparse,json
from pathlib import Path
import numpy as np
from acd_stage13_analysis import loadcosts,summaries,frozen,nullsd,decision_rows,ROOT,RAW
from acd_stage9_cnn_metrics import score
def score_decisions_external(costs,valid,keep):
 # Hidden realized costs are opened exclusively inside scoring.
 actual=np.array([np.load(RAW/f'conf/score_{c:03d}.npz')['actual_cost'] for c in range(200)])
 return decision_rows(actual,costs,valid,keep,nullsd())[0]
def evaluate(directory,model):
 jbar,null=frozen();_,_,keep=loadcosts('posterior')
 costs=[];valid=[]
 for c in range(len(keep)):
  with np.load(directory/f'{c:03d}.npz') as d:
   j=d['J'].copy();v=bool(d['valid'].all()) if 'valid' in d else True
  assert j.ndim==3 and j.shape[1:]==(9,8),(c,j.shape)
  with np.load(RAW/f'conf/case_{c:03d}.npz') as d:assert len(j)==len(d['J']),(c,'draw count')
  costs.append(j);valid.append(v and bool(np.isfinite(j).all()))
 s=summaries(costs,valid,jbar,null)
 result=score(model,None,s,keep,None,[],jbar)
 result['decisions']=score_decisions_external(costs,np.array(valid),keep)
 result['full_grid_readings'],result['full_grid_comparisons']=score_grid(costs,s,keep,jbar)
 result['invalid_cases']=np.flatnonzero(~np.array(valid)&keep).tolist()
 result['scope']='Post hoc on confirmation; licenses no frozen route. All supplied draws retained; any invalid option or draw forces no action.'
 return result
def score_grid(costs,s,keep,jbar):
 # Outcomes are read exclusively here, within scoring.
 from acd_stats import r0,r0_f
 from acd_stage6_analysis import LEADS,comparisons
 actual=np.array([np.load(RAW/f'conf/score_{c:03d}.npz')['actual_cost'] for c in range(200)])
 truth=np.concatenate([actual[:,:8]<actual[:,8,None],(actual[:,8]>jbar)[:,None]],axis=1)
 rows=[]
 for t,l in enumerate(LEADS):
  conf=s['confident'][keep,:8,t];obs=s['observation'][keep,:8,t]
  right=s['modal'][keep,:8,t]==truth[keep,:8,t]
  fc=s['confident'][keep,8,t];fcr=s['modal'][keep,8,t]==truth[keep,8,t]
  rows.append(dict(lead=float(l),confident_S_share=float(conf.mean()),observation_confident_S_share=float(obs.mean()),confident_Fc_share=float(fc.mean()),all_confident_accuracy=r0(conf.sum(1),(conf&right).sum(1)),observation_confident_accuracy=r0(obs.sum(1),(obs&right).sum(1)),Fc_accuracy=r0_f(int((fc&fcr).sum()),int(fc.sum()))))
 return rows,comparisons(s,keep)
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--cost-directory',type=Path,required=True);p.add_argument('--model-name',default='external');p.add_argument('--output',type=Path,required=True);p.add_argument('--reproduce-stage9-CNN-F',action='store_true');a=p.parse_args()
 d=evaluate(a.cost_directory,a.model_name);a.output.write_text(json.dumps(d,indent=2,allow_nan=False)+'\n')
 if a.reproduce_stage9_CNN_F:
  old=json.load(open(ROOT/'receipts/acd_stage9.json'))['C']['CNN-F']
  keys=['matched_cases','matched_questions','confidence_readings','reliability','error_coverage','calibration_test','comparisons','paired_endpoint','paired_endpoint_fixed_posterior_cohort','invalid_cases']
  differences=[key for key in keys if d[key]!=old[key]]
  receipt=dict(model='CNN-F',exact_fields=keys,differences=differences,pass_exact=not differences,input_directory=str(a.cost_directory),input_format='case-indexed NPZ: J[draw,9,8], optional valid mask',scope='Exact equality, including floating-point values, counts and bounds; factual-state skill not inferred from costs.')
  (ROOT/'receipts/acd_stage13_evaluator_check.json').write_text(json.dumps(receipt,indent=2)+'\n')
  print(json.dumps(receipt,indent=2));assert not differences
if __name__=='__main__':main()
