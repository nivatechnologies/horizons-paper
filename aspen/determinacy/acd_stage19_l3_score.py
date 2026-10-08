"""Execute frozen L3 statistics after all committed runs and hashed inference finish."""
import os
os.environ.update(JAX_PLATFORMS='cpu',JAX_ENABLE_X64='true',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',NUMBA_NUM_THREADS='4')
import json,subprocess,time
from pathlib import Path
import numpy as np
from acd_stage19_learned import ROOT,OUT,digest,freeze_ready,model_inputs,metrics
from acd_stage19_l3_statistic import pair_statistic,aggregate_new_pairs
REPO=ROOT.parents[1]
def score():
 freeze_ready();start=time.monotonic();statuses={};sources={};names=[f'{m}-seed{i}' for i in range(1,5) for m in ['CNN-F','CNN-noF']]
 for name in names:
  p=ROOT/'receipts'/f'acd_stage16_run_{name}.json';rel=p.relative_to(REPO)
  assert subprocess.check_output(['git','show','HEAD:'+str(rel)],cwd=REPO)==p.read_bytes()
  d=json.loads(p.read_text())['training'];statuses[name]=d;sources[str(p.relative_to(ROOT))]=digest(p)
  path=OUT/'inference'/name;complete=json.loads((path/'complete.json').read_text());hashes=json.loads((path/'hashes.json').read_text())
  assert complete['cases']==len(hashes)==200
  assert all(digest(path/p)==h for p,h in hashes.items())
  assert digest(OUT/'L3_checkpoints'/name/'selected.pt')==d['selected_sha256']
  sources[str((path/'hashes.json').relative_to(ROOT))]=digest(path/'hashes.json')
 # Realized arrays are opened only here, after every training and inference gate.
 from acd_stage19_score import score_actual
 actual,factual=score_actual();stage2=json.loads((ROOT/'receipts/acd_stage2.json').read_text());jbar=stage2['null']['jbar'];null=np.asarray(stage2['null']['question_probabilities'])[np.r_[np.arange(8),37]]
 with np.load(OUT/'reused/runs/stage6/null_block.npz') as z:sd=(z['J'][:,:8]-z['J'][:,8,None]).std(0,ddof=1)
 with np.load(OUT/'reused/runs/stage4b_null/states.npz') as z:climate=z['states'].mean(0)
 posterior=model_inputs('posterior',jbar,null)[3];fixed=posterior['observation'][:,:8,0]&posterior['confident'][:,8,0,None]
 truth=actual[:,:8]<actual[:,8,None];pairs={};results={}
 for i in range(5):
  models=['CNN-F','CNN-noF'] if i==0 else [f'CNN-F-seed{i}',f'CNN-noF-seed{i}']
  inputs={m:model_inputs(m,jbar,null) for m in models}
  pairs[i]=pair_statistic(inputs[models[0]][3],inputs[models[1]][3],truth,3)
  for name in models:
   results[name]=metrics(name,*inputs[name],actual,factual,jbar,climate,sd,fixed)
   readings=[];s=inputs[name][3]
   from acd_stats import r0
   for t in [3,5]:
    mask=s['confident'][:,1:8,t];right=s['modal'][:,1:8,t]==truth[:,1:8,t];a=r0(mask.sum(1),(mask&right).sum(1))
    readings.append(dict(lead=float([2,3][[3,5].index(t)]),accuracy=a,pooled_error=None if a['answer_accuracy'] is None else 1-a['answer_accuracy'],case_error=None if a['case_accuracy'] is None else 1-a['case_accuracy'],case_error_lower=1-a['case_upper'],case_error_upper=1-a['case_lower']))
   results[name]['seven_pattern_confident_error']=readings
  print('Scored seed pair',i,pairs[i]['interval'],flush=True)
  del inputs
 aggregated=aggregate_new_pairs(pairs,statuses)
 pooled_count=sum(results[('CNN-noF' if i==0 else f'CNN-noF-seed{i}')]['confidence_readings'][0]['pooled_confident_error']>results[('CNN-F' if i==0 else f'CNN-F-seed{i}')]['confidence_readings'][0]['pooled_confident_error'] for i in range(5))
 output=dict(stage=19,reading='L3',fresh_panel=True,L3=aggregated,original_descriptive_pooled_error_count=pooled_count,pairs=pairs,models=results,training_run_status=statuses,source_hashes=sources,code_hashes={n:digest(ROOT/n) for n in ['acd_stage19_l3_score.py','acd_stage19_l3_statistic.py','acd_stage19_learned.py','acd_stats.py']},wall_seconds=time.monotonic()-start)
 (ROOT/'receipts/acd_stage19_L3.json').write_text(json.dumps(output,indent=2,allow_nan=False)+'\n')
 lines=['\n## L3 training-seed replication','', 'All eight new selected checkpoints are committed and all fresh inference manifests were verified before scoring. L3a and L3b use the unchanged frozen aggregation, case contribution rule and failed-run rule. Training-run variation is separate from case-level bounds.','',f"L3a: {aggregated['L3a']}. L3b positive new pair count: {aggregated['positive_new_pair_count']}. Confirmed: {aggregated['confirmed']}.",'','| Seed | L1 estimate | 99% interval | CNN-F pooled S error | CNN-noF pooled S error |','|---|---:|---|---:|---:|']
 for i,p in pairs.items():
  f='CNN-F' if i==0 else f'CNN-F-seed{i}';n='CNN-noF' if i==0 else f'CNN-noF-seed{i}';v=p['interval'];lines.append(f"| {i} | {v['point']} | [{v['lower']}, {v['upper']}] | {results[f]['confidence_readings'][0]['pooled_confident_error']} | {results[n]['confidence_readings'][0]['pooled_confident_error']} |")
 lines+=['','Full per-seed state skill, confident errors and bounds, gate harm bounds, uniform-decrease choices and other descriptive metrics are in receipts/acd_stage19_L3.json.']
 p=ROOT/'ACD_STAGE19_READING.md';p.write_text(p.read_text()+'\n'.join(lines)+'\n')
 (OUT/'L3_scored.json').write_text(json.dumps(dict(utc=time.time(),receipt_sha256=digest(ROOT/'receipts/acd_stage19_L3.json')))+'\n')
 print(json.dumps(aggregated),flush=True)
if __name__=='__main__':score()
