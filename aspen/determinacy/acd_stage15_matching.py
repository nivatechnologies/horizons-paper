"""Stage 15A: CPU scoring from saved outputs; outcome access confined to score()."""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMBA_NUM_THREADS='4',JAX_PLATFORMS='cpu',JAX_ENABLE_X64='true')
import json,hashlib
from pathlib import Path
import numpy as np
import numba
import acd_stage13_analysis as prior
import acd_protocol,protocol
from acd_stage6_analysis import ROOT,RAW,OUT,SIGMA,LEADS,WINDOWS,binary,stack
from acd_stats import r0,cp_bounds,difference_interval
from acd_stage17_events import error_bounds
numba.set_num_threads(min(4,numba.config.NUMBA_NUM_THREADS))
MODELS=['posterior','CNN-20k','CNN-F','CNN-noF','CNN-F-resp','CNN-F-resp-0.01']
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def score():
 # Saved realized costs/states are opened only inside scoring.
 actual=np.array([np.load(RAW/f'conf/score_{c:03d}.npz')['actual_cost'] for c in range(200)])
 with np.load(OUT/'scoring.npz') as z:states=z['factual'].copy()
 with np.load(ROOT/'runs/stage4b_null/states.npz') as z:climate=z['states'].mean(0)
 jbar,null=prior.frozen();costs_by={m:prior.loadcosts(m) for m in MODELS}
 namespace='acd-stage15-ties';seed=int.from_bytes(hashlib.sha256(namespace.encode()).digest()[:8],'little')
 generator=np.random.default_rng(np.random.SeedSequence(seed));tieorder=generator.permutation(actual.shape[0]*actual.shape[1] - actual.shape[0]);tierank=np.argsort(tieorder)
 # One fixed randomized order of case/action identifiers, reused for every model and lead.
 assertions={'unique_namespace':namespace not in (set(acd_protocol.ACD_IDS) | set(protocol.IDS)),'unique_question_order':len(np.unique(tieorder))==len(tieorder)}
 assert all(assertions.values())
 physics=costs_by['posterior'][0];answer=actual[:,:8]<actual[:,8,None];factual=actual[:,8]>jbar
 results={}
 for model,(costs,valid,keep) in costs_by.items():
  if not valid[keep].all():raise RuntimeError('R-other: nonfinite saved draw; probability reading requires explicit invalid-draw resolution, no survivor conditioning')
  summaries=stack([binary(j,jbar,null[np.r_[np.arange(8),37]]) for j in costs]);means=[]
  for c in range(len(costs)):
   path=OUT/f'conf_{c:03d}_0.16.npz' if model=='posterior' else ROOT/f'runs/stage9/inference/{model}/{c:03d}.npz'
   with np.load(path) as z:means.append(z['factual_mean'].copy())
  means=np.asarray(means);assert means.shape[0]==states.shape[0] and means.shape[2:]==states.shape[2:];common=max(max(w) for w in WINDOWS)+1;assert means.shape[1]>=common and states.shape[1]>=common,"Every scored tick must exist in model and truth";err=np.sqrt(np.mean((means[:,:common]-states[:,:common])**2,-1))/SIGMA
  x=means[:,:common]-climate;y=states[:,:common]-climate;acc=np.sum(x*y,-1)/np.sqrt(np.sum(x*x,-1)*np.sum(y*y,-1))
  rows=[]
  for t in [3,5]:
   cases=np.flatnonzero(keep);pF=np.array([(j[:,8,t]>jbar).mean() for j in costs]);modalF=np.maximum(pF,1-pF);rightF=(pF>.5)==factual[:,t];confF=modalF>=.95
   fcaccuracy=r0(confF[keep].astype(int),(confF&rightF)[keep].astype(int));nf=int(confF[keep].sum());cf=int((confF&rightF)[keep].sum())
   j8err=[j[:,8,t]-p[:,8,t] for j,p,k in zip(costs,physics,keep) if k];pooled=np.concatenate(j8err);realerr=np.array([costs[c][:,8,t].mean()-actual[c,8,t] for c in cases])
   p=summaries['p'][:,:8,t];wrong=summaries['modal'][:,:8,t]!=answer[:,:,t];mask=summaries['confident'][:,:8,t]
   row=dict(lead=float(LEADS[t]),state_skill=dict(window_mean_state_RMSE_over_sigma=float(err[keep][:,WINDOWS[t]].mean()),window_mean_anomaly_correlation=float(acc[keep][:,WINDOWS[t]].mean()),averaging='Compute site-RMS/normalizer and site anomaly correlation at each tick, then equal tick/window and case means.'),factual_energy=dict(per_draw_J8_RMSE=float(np.sqrt(np.mean(pooled**2))),per_draw_J8_bias=float(pooled.mean()),equal_case_J8_RMSE=float(np.mean([np.sqrt(np.mean(e**2)) for e in j8err])),equal_case_J8_bias=float(np.mean([e.mean() for e in j8err])),ensemble_mean_J8_RMSE_against_realized=float(np.sqrt(np.mean(realerr**2))),ensemble_mean_J8_bias_against_realized=float(realerr.mean())),forecast=dict(event='J8 > Jbar',confident_share=float(confF[keep].mean()),accuracy=fcaccuracy,pooled_accuracy_CP_one_sided95=list(cp_bounds(cf,nf)) if nf else None,case_accuracy_CP_one_sided95=list(cp_bounds(cf,nf)) if nf else None,calibration_test=difference_interval((modalF-rightF)[keep]),calibration_scope='all forecast answers; instance-level modal probability minus correctness; two-sided99% mean-calibration betting test'),confident_S=dict(share=float(mask[keep].mean()),answers=int(mask[keep].sum()),pooled_error=float(wrong[keep][mask[keep]].mean()) if mask[keep].any() else None,**error_bounds(mask[keep],wrong[keep])),matched_coverage=[])
   for group,ks in [('all_eight',np.arange(8)),('seven_zero_mean',np.arange(1,8))]:
    allowed=np.zeros_like(p,bool);allowed[np.ix_(cases,ks)]=True;ids=np.flatnonzero(allowed.ravel());order=ids[np.lexsort((tierank[ids],-p.ravel()[ids]))]
    for coverage in [.5,.7]:
     take=int(round(coverage*len(order)));selected=np.zeros(p.size,bool);selected[order[:take]]=True;selected=selected.reshape(p.shape)
     row['matched_coverage'].append(dict(patterns=group,target_coverage=coverage,questions=len(order),answers=take,selected_case_action_ids=order[:take].tolist(),pooled_error=float(wrong[selected].mean()),**error_bounds(selected[keep],wrong[keep])))
   rows.append(row)
  results[model]=dict(main_text=model in MODELS[:4],rows=rows)
 decisions={}
 for filename in ['acd_stage13_decisions.json','acd_stage10b_decisions.json','acd_stage10b_resp001_decisions.json']:
  path=ROOT/'receipts'/filename
  if path.exists():
   receipt=json.loads(path.read_text())
   for model,record in receipt['models'].items():decisions[model]=[r for r in record['readings'] if r['policy'] in ['E','C_delta_0']]
 receipt=dict(post_hoc=True,licenses_frozen_route=False,A=results,decision_references=decisions,ranking=dict(namespace=namespace,seed=seed,tie_order_case_action_ids=tieorder.tolist(),ordering='descending modal probability; ties by the single fixed namespace-seeded permutation, independent of outcomes; reused across models, leads and pattern subsets',assertions=assertions),source_hashes={str(p):sha(p) for p in [Path(__file__),ROOT/'acd_stage13_analysis.py',ROOT/'acd_stats.py',ROOT/'acd_stage17_events.py']})
 (ROOT/'receipts/acd_stage15_matching.json').write_text(json.dumps(receipt,indent=2,allow_nan=False)+'\n')
 render(receipt)
def render(d):
 lines=['# Stage 15 matched comparisons','','Post hoc on the confirmation panel; licenses no frozen route. CNN-F and CNN-noF have no development-panel runs; no independent equivalence margin is available. These readings form a frontier, not an equivalence test.','','Ranking: '+d['ranking']['ordering']+'.','','| Model | Lead | State RMSE/sigma | State ACC | Per-draw J8 RMSE | Per-draw J8 bias | Ensemble J8 RMSE vs truth | Fc confidence | Fc pooled accuracy | Confident S error |','|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
 for model,record in d['A'].items():
  if not record['main_text']:continue
  for r in record['rows']:
   s,e,f=r['state_skill'],r['factual_energy'],r['forecast'];v=[model,r['lead'],s['window_mean_state_RMSE_over_sigma'],s['window_mean_anomaly_correlation'],e['per_draw_J8_RMSE'],e['per_draw_J8_bias'],e['ensemble_mean_J8_RMSE_against_realized'],f['confident_share'],f['accuracy']['answer_accuracy'],r['confident_S']['case_error']];lines.append('| '+' | '.join(map(str,v))+' |')
 lines+=['','| Model | Lead | Patterns | Coverage | Answers | Pooled error | Case error | Case error one-sided95 lower | Case error one-sided95 upper |','|---|---:|---|---:|---:|---:|---:|---:|---:|']
 for model,record in d['A'].items():
  if not record['main_text']:continue
  for r in record['rows']:
   for m in r['matched_coverage']:lines.append('| '+' | '.join(map(str,[model,r['lead'],m['patterns'],m['target_coverage'],m['answers'],m['pooled_error'],m['case_error'],m['case_error_lower95'],m['case_error_upper95']]))+' |')
 lines+=['','R-other: physics saves an extra terminal tick beyond the emulator grid; every scored tick is present in both, explicitly asserted. State errors are computed across sites at each output tick, then averaged equally over the scored window and instances. Factual energy errors include pooled draws and equal-instance readings in the receipt.','', '| Model | Lead | Fc pooled/equal-case accuracy | One-sided95 lower | One-sided95 upper | Calibration mean | Calibration99 lower | Calibration99 upper |','|---|---:|---:|---:|---:|---:|---:|---:|---:|']
 for model,record in d['A'].items():
  if not record['main_text']:continue
  for r in record['rows']:
   f=r['forecast'];q=f['calibration_test'];cp=f['pooled_accuracy_CP_one_sided95'];lines.append('| '+' | '.join(map(str,[model,r['lead'],f['accuracy']['answer_accuracy'],cp[0],cp[1],q['point'],q['lower'],q['upper']]))+' |')
 lines+=['','| Model | Lead | Policy | Regret | Capture | Harms | Acting share | Chosen actions |','|---|---:|---|---:|---:|---:|---:|---|']
 for model,rows in d['decision_references'].items():
  if model not in MODELS[:4]:continue
  for r in rows:lines.append('| '+' | '.join(map(str,[model,r['lead'],r['policy'],r['mean_regret'],r['capture_fraction'],r['harms'],r['acting_share'],r['chosen_actions']]))+' |')
 lines+=['','R-other: the initial seven-pattern coverage count used a floating-point product followed by truncation. The corrected count rounds the prescribed fraction before selecting questions. The earlier receipt is superseded for these readings and retained separately for registry history.','']
 lines+=['','Bounds and all forecast calibration tests are recorded at full precision in receipts/acd_stage15_matching.json. Instance means omit instances without selected answers. Fc has one answer per contributing instance, so pooled and equal-case accuracy and their exact one-sided Clopper–Pearson intervals coincide. E/C decisions are referenced without recomputation; receipt-only response models are retained.','']
 (ROOT/'ACD_STAGE15_READING.md').write_text('\n'.join(lines))
if __name__=='__main__':score()
