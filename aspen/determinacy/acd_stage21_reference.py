"""Frozen G1/G2 alone; realized cache is opened only by this scoring function."""
import os
os.environ.update(JAX_PLATFORMS='cpu',JAX_ENABLE_X64='true',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',NUMBA_NUM_THREADS='4')
import json,time
import numpy as np
from acd_stage21_score import score_actual,clean
from acd_stage21_freeze_e import ready
from acd_stage21_contract import OUT,digest,assignments
from acd_protocol import ROOT
from acd_stage6_analysis import binary,stack,calibration,loss

def score():
 ready();started=time.monotonic();actual,_=score_actual();levels=assignments();climates={}
 for f in np.unique(levels):
  with np.load(OUT/'climatology'/f'F{int(f)}.npz') as z:climates[int(f)]=(float(z['jbar']),z['prob'].copy())
 rows=[];keep=[];hashes={}
 for c,f in enumerate(levels):
  p=OUT/f'main_forecast_{c:03d}.npz'
  with np.load(p) as z:j=z['J'].copy();k=not bool(z['excluded'])
  assert np.isfinite(j).all(), 'Invalid posterior forecast'
  rows.append(binary(j,*climates[int(f)]));keep.append(k);hashes[str(p.relative_to(ROOT))]=digest(p)
 summary=stack(rows);keep=np.array(keep);jbar=np.array([climates[int(f)][0] for f in levels])
 truth=np.concatenate([actual[:,:8]<actual[:,8,None],(actual[:,8]>jbar[:,None])[:,None]],axis=1)
 accuracy=calibration(summary,truth,keep);paired=loss(summary,keep)
 g1=next(r['S'] for r in accuracy if r['lead']==2.)
 interval=paired['interval'];g2=dict(**interval,confirmed=not(interval['empty'] or interval['offset']) and interval['upper']<0,pairs=paired['actions'],cases=paired['cases'],bound_type='two-sided99% v2.3 instance betting')
 result=clean(dict(stage=21,part='reference',frozen=True,licenses_frozen_route=False,population=dict(generated=len(keep),retained=int(keep.sum()),excluded=np.flatnonzero(~keep).tolist()),G1=dict(**g1,confirmed=g1['status']=='PASS',bound_type='original R0 one-sided95% instance betting'),G2=g2,accuracy_by_lead=accuracy,paired=paired,source_hashes=hashes,realized_sha256=digest(OUT/'scoring/actual.npz'),code_hashes={n:digest(ROOT/n) for n in ['acd_stage21_reference.py','acd_stage21_score.py','acd_stage6_analysis.py','acd_stats.py']},wall_seconds=time.monotonic()-started))
 (ROOT/'receipts/acd_stage21_reference.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
 text=['# Stage21 forcing-shift panel readings','','## Frozen reference readings','','No emulator is needed for G1/G2. The original R0 criterion and the original own-eligibility/censoring construction are unchanged. The instance is the inference unit; excluded instances are withheld. Realized outcomes are created or read only inside scoring code.','','| Reading | Estimate | Bound / interval | Result |','|---|---:|---|---|',f"| G1 | {g1['case_accuracy']} | [{g1['case_lower']}, {g1['case_upper']}] — original R0 one-sided 95% bounds; pooled accuracy {g1['answer_accuracy']} | {g1['status']} |",f"| G2 | {interval['point']} | [{interval['lower']}, {interval['upper']}] — two-sided 99% v2.3 betting | {'PASS' if g2['confirmed'] else 'FAIL'} |",'',f"Population: {int(keep.sum())} retained of {len(keep)}; exclusions {np.flatnonzero(~keep).tolist()}. Paired eligibility gives {paired['actions']} pairs across {paired['cases']} instances.",'']
 (ROOT/'ACD_STAGE21_READING.md').write_text('\n'.join(text))
 print(json.dumps({k:result[k] for k in ['G1','G2','population','wall_seconds']}),flush=True)
if __name__=='__main__':score()
