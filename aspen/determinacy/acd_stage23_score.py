"""Thin Q1/Q2 wrapper around frozen inference/scoring statistics."""
from acd_stage23_common import *
from acd_stage23_panel import configured
import numpy as np,inspect,time

def score():
 frozen,view,name,gate=configured()
 assert (OUT/'inference_complete.json').exists() and frozen.complete(name)
 import acd_stage21_score as source
 workspace=OUT/'scoring_workspace';(workspace/'receipts').mkdir(parents=True,exist_ok=True)
 (workspace/'ACD_STAGE21_FREEZE_E.md').write_bytes((PANEL22/'ACD_STAGE21_FREEZE_E.md').read_bytes())
 source.ROOT=workspace;source.OUT=view;source.ready=gate
 original=np.load
 def logged(path,*a,**kw):
  if Path(path).resolve()==(view/'scoring/actual.npz').resolve():
   frame=inspect.stack()[1];assert frame.function=='score_actual' and Path(frame.filename).name=='acd_stage21_score.py'
   with (view/'scoring/access.jsonl').open('a') as f:f.write(json.dumps(dict(path=str(path),caller=frame.filename,function=frame.function,sha256=digest(path),utc=time.time()))+'\n')
  return original(path,*a,**kw)
 np.load=logged
 try:
  source.score();data=json.loads((workspace/'receipts/acd_stage21.json').read_text());actual,_=source.score_actual()
  levels=source.assignments();climate={}
  for f in [7,9]:
   with np.load(view/'climatology'/f'F{f}.npz') as z:climate[f]=(float(z['jbar']),z['prob'].copy())
  summaries={}
  for pipeline in [name,'CNN-noF']+[f'CNN-F-E0-fixed-seed{j}' for j in range(1,6)]:
   rows=[]
   for c,f in enumerate(levels):
    with np.load(view/f'main_forecast_{c:03d}.npz') as z:excluded=bool(z['excluded'])
    with np.load(view/'inference'/pipeline/f'{c:03d}.npz') as z:j=z['J'].copy();valid=bool(z['valid'].all()) and np.isfinite(j).all()
    s=source.binary(j,*climate[f])
    if excluded or not valid:s['confident'].fill(False);s['observation'].fill(False)
    rows.append(s)
   summaries[pipeline]=source.stack(rows)
  truth=np.concatenate([actual[:,:8]<actual[:,8,None],(actual[:,8]>np.array([climate[f][0] for f in levels])[:,None])[:,None]],1)
  pair=source.pair_statistic(summaries[name],summaries['CNN-noF'],truth,3);q1=dict(pair,confirmed=pair['interval'] is not None and pair['interval']['lower']>0)
  chosen=next(r for r in data['models'][name]['pooled']['decisions'] if r['lead']==3. and r['policy']=='C_delta_0')
  q2=dict(chosen,confirmed=chosen['actions_taken']>0 and chosen['conditional_harm_CP95'][1]<.05,bound_type='exact one-sided95% Clopper-Pearson upper, strict-positive harms')
  comparisons=[source.pair_statistic(summaries[f'CNN-F-E0-fixed-seed{j}'],summaries[name],truth,3) for j in range(1,6)]
  record=dict(stage=23,Q1=q1,Q2=q2,selected_minus_E0_fixed=source.seed_average(comparisons),descriptive_models={name:data['models'][name]},comparator_receipt_sha256=digest(PANEL22/'receipts/acd_stage22.json'),missing_models=data['missing_models'],excluded_cases=data['excluded_cases'],selection=json.loads((OUT/'selection.json').read_text()))
  write(ROOT/'receipts/acd_stage23.json',record);write(OUT/'scoring_complete.json',dict(receipt_sha256=digest(ROOT/'receipts/acd_stage23.json')))
 finally:np.load=original
if __name__=='__main__':score()
