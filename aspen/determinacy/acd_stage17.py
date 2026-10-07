"""Stage 17 saved-output extensions; CPU only, at most four threads."""
import os
os.environ.update(OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', NUMBA_NUM_THREADS='4', JAX_PLATFORMS='cpu', JAX_ENABLE_X64='true')
import json, hashlib, inspect
from pathlib import Path
import numpy as np
from scipy.stats import beta
import acd_stage13_analysis as prior
from acd_stage6_analysis import ROOT, RAW, LEADS, stack
from acd_stage9_receipts import dist
from acd_stats import cp_bounds
import acd_protocol as protocol
import acd_stats
import numba
numba.set_num_threads(min(4,numba.config.NUMBA_NUM_THREADS))
FORWARD=Path('/home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/runs/stage9')
MODELS=list(json.loads((ROOT/'receipts/acd_stage10b_decisions.json').read_text())['models'])
THRESHOLDS=[.5,.55,.6,.65,.7,.75,.8,.85,.9,.95,.99]
AMPS=[.04,.16,.64]
GAMMAS=[.05,.1,.2,.5]
RECEIPT=ROOT/'receipts/acd_stage17.json'
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def save(d):RECEIPT.write_text(json.dumps(d,indent=2,allow_nan=False)+'\n')
def tangent():
 # Copy B2's calculations verbatim; only the amplitude loop and J source differ.
 original=(ROOT/'acd_stage9_forward_readings.py').read_text()
 body=original[original.index(' results=[];amps=[]'):original.index('  real=score_actual(amp)')]
 body=body.replace('results=[];amps=[]','results=[];amps=[];near=[]')
 body=body.replace('for ai,amp in enumerate([.04,.64]):','for ai,amp in enumerate(AMPS):')
 body=body.replace("with np.load(DEST/f'forward_{c:03d}.npz') as d:G=d['G'].copy();J=d['J'][:,ai].copy()", "with np.load(DEST/f'forward_{c:03d}.npz') as d:G=d['G'].copy();J=d['J'][:,0 if amp==.04 else 1].copy()\n   if amp==.16:\n    with np.load(RAW/f'conf/case_{c:03d}.npz') as d:J=d['J'].copy()")
 body=body.replace('  keep=np.array(keep);', '  near.append((amp,allD,keep));keep=np.array(keep);')
 # Existing summaries need the matching saved null; no integration or scoring.
 from acd_stage6_analysis import binary
 scope=dict(np=np,ROOT=ROOT,RAW=RAW,DEST=FORWARD,LEADS=LEADS,AMPS=AMPS,binary=binary,stack=stack,dist=dist,jbar=prior.frozen()[0])
 exec('def copied_b2():\n'+body+' return results,near\n',scope)
 results,near=scope['copied_b2']()
 old=json.loads((ROOT/'receipts/acd_stage9.json').read_text())['B']['B2']
 reproduced=[r for r in results if r['amplitude']!=.16]
 assert reproduced==old,'Stage 9 B2 differs'
 clim=json.loads((ROOT/'receipts/acd_stage11_clim_tangent.json').read_text())
 sd=np.array([[next(r['standard_deviation'] for r in clim['rows'] if r['pattern']==k and r['lead']==float(lead)) for lead in LEADS] for k in range(8)])
 near_rows=[]
 for amp,ds,keep in near:
  for gamma in GAMMAS:
   fractions=np.array([(np.abs(d/amp)<=gamma*sd).mean(0) for d,k in zip(ds,keep) if k])
   for t,lead in enumerate(LEADS):
    for label,indices in [('all_eight',slice(None)),('seven_zero_mean',slice(1,None))]:
     near_rows.append(dict(amplitude=amp,gamma=gamma,lead=float(lead),patterns=label,mass=dist(fractions[:,indices,t].ravel())))
 return dict(B2=results,near_zero_mass=near_rows,stage9_reproduction=dict(exact=True,rows=len(old)),climatological_scale='per-action, per-lead standard_deviation of G from Stage 11; retained confirmation cases, equal case/action summaries')
def summarize(x):return dist(np.asarray(x)) if len(x) else None
def score_selected_risk():
 # Sole outcome access: saved realized costs are opened inside scoring.
 actual=[]
 n=len(json.loads((ROOT/'receipts/acd_stage13_decisions.json').read_text())['models']['posterior']['invalid_case_indices'])
 costs_by={m:prior.loadcosts(m) for m in MODELS}
 count=len(costs_by['posterior'][0])
 for c in range(count):
  with np.load(RAW/f'conf/score_{c:03d}.npz') as f:actual.append(f['actual_cost'])
 actual=np.array(actual);sd=prior.nullsd()
 old=json.loads((ROOT/'receipts/acd_stage10b_decisions.json').read_text())
 output={};reproduction={}
 for model,(costs,valid,keep) in costs_by.items():
  rows,_=prior.decision_rows(actual,costs,valid,keep,sd)
  assert rows==old['models'][model]['readings'],model+' decision reproduction'
  reproduction[model]=dict(exact=True,rows=len(rows))
  selected=[];margins=[];curves=[]
  for t in [3,5]:
   cases=np.flatnonzero(keep);base=actual[cases,8,t];best=actual[cases,:,t].min(1)
   e=prior.choices(costs,valid,t,sd)['E']
   def result(ch):
    value=actual[cases,ch[cases],t];effect=value-base;acted=ch[cases]!=8
    harmed=acted&(effect>=0)
    return value,effect,acted,harmed
   for policy,ch in prior.choices(costs,valid,t,sd).items():
    if policy not in ['E','C_delta_0','C_delta_0.1']:continue
    value,effect,acted,harmed=result(ch);na=int(acted.sum());nh=int(harmed.sum())
    probs=np.array([np.mean(costs[c][:,ch[c],t]-costs[c][:,8,t]<0) for c in cases[acted]])
    bins=[]
    for lo,hi in zip([0,.5,.95,.97,.99],[.5,.95,.97,.99,1.]):
     mask=(probs>=lo)&((probs<=hi) if hi==1 else probs<hi);nn=int(mask.sum());correct=int((effect[acted][mask]<0).sum())
     bins.append(dict(lower_edge=lo,upper_edge=hi,acted_cases=nn,beneficial=correct,mean_probability=float(probs[mask].mean()) if nn else None,observed_benefit=correct/nn if nn else None,CP_one_sided95=list(cp_bounds(correct,nn)) if nn else None))
    selected.append(dict(lead=float(LEADS[t]),policy=policy,cases=len(cases),actions=na,harms=nh,harm_conditional=nh/na if na else None,harm_conditional_CP_one_sided95=list(cp_bounds(nh,na)) if na else None,unconditional_harm=nh/len(cases),unconditional_harm_CP_upper95=cp_bounds(nh,len(cases))[1],expected_harms=float((1-probs).sum()),reliability=bins,harm_magnitude=summarize(effect[harmed]),regret=summarize(value-best),invalid_cases=int((~valid&keep).sum())))
   for delta in [0,.1,.25]:
    ch=np.full(count,8,int)
    for c in cases:
     k=e[c]
     if valid[c] and k<8 and np.mean(costs[c][:,k,t]-costs[c][:,8,t]<-delta*sd[k,t])>=.95:ch[c]=k
    value,effect,acted,harmed=result(ch);scale=delta*sd[ch[cases].clip(max=7),t]
    margins.append(dict(lead=float(LEADS[t]),delta=delta,actions=int(acted.sum()),acting_share=float(acted.mean()),harms=int(harmed.sum()),insufficient_benefit=int((acted&(effect<0)&(effect>=-scale)).sum()),mean_regret=float((value-best).mean())))
   for threshold in THRESHOLDS:
    ch=np.full(count,8,int)
    for c in cases:
     k=e[c]
     if valid[c] and k<8 and np.mean(costs[c][:,k,t]-costs[c][:,8,t]<0)>=threshold:ch[c]=k
    value,effect,acted,harmed=result(ch);na=int(acted.sum())
    curves.append(dict(lead=float(LEADS[t]),threshold=threshold,actions=na,acting_share=float(acted.mean()),harms=int(harmed.sum()),harm_conditional=float(harmed.sum()/na) if na else None,mean_regret=float((value-best).mean())))
  output[model]=dict(selected=selected,margins=margins,risk_coverage_regret=curves)
 return dict(models=output,reproduction=reproduction,harm_definition='among acted cases, realized D >= 0; source rows retain their original strict D > 0 convention',margin_definition='delta times saved climatological standard deviation of D_k for the chosen action k and lead; gate P(D_k < -delta*sd_clim(D_k)) >= threshold',reliability_scope='case-level selected-action diagnostic; E includes below-half probabilities explicitly; selection is post hoc')
def methods():
 windows=[dict(lead=float(lead),indices=w.tolist(),times=(protocol.TICKS[w]*protocol.OUT).tolist(),LT_values=(protocol.TICKS[w]*protocol.OUT/protocol.LT).tolist(),samples=len(w)) for lead,w in zip(LEADS,protocol.WINDOWS)]
 hashes={p:sha(ROOT/p) for p in ['acd_stats.py','acd_protocol.py','acd_stage9_forward_readings.py','acd_stage13_analysis.py','acd_stage17.py']}
 hashes[str(Path(protocol.protocol.__file__))]=sha(protocol.protocol.__file__)
 lines=['# Windows and betting methods','', 'Post hoc methods record; licenses no frozen route.', '', 'LT constant: '+repr(protocol.LT)+'. Output spacing: '+repr(protocol.OUT)+'. Inclusion: tick time >= lead*LT - 1e-12 and <= (lead+1)*LT + 1e-12, exactly as protocol.WINDOWS.', '', '| Lead LT | Tick indices | Times | LT values |','|---:|---|---|---|']
 for row in windows:lines.append('| '+str(row['lead'])+' | '+str(row['indices'])+' | '+str(row['times'])+' | '+str(row['LT_values'])+' |')
 lines+=['','Case fractions are processed in ascending retained case index; cases with no contributing answers are omitted. Paired differences d use x=(d+1)/2 and return 2*bound-1. Brier differences use the same bounded mapping.','', 'The predictable bet uses prior residual sum initialized at 0.25, pseudo-total 0.5, and t=count+1. variance=residual/t; bet=min(0.9, sqrt(2*log(1/alpha)/(variance*t*log(t+1)))). After the capital increment, total and count update, mu=total/(count+1), then residual+=(value-mu)^2. This is the implemented pseudo-observation residual convention.','', 'Rejection uses the running maximum log capital >= log(1/alpha). Inversion uses an integer grid from 0 to 1000 divided by 1000; bounds retain the rejection boundary grid cell, giving outward rounding. One-sided bounds allocate alpha=0.05 to each requested tail. Two-sided 99% bounds allocate alpha=0.005 per tail. Empty answer cases are omitted before inversion. The fallback branch is opt-in: r0 widens with all-correct/any-correct case CP bounds, and difference_interval widens with its Hoeffding radius. Stage 17 calls the default fallback=False; no newly computed Stage 17 interval uses fallback.','', 'Code SHA-256s:']
 lines += ['- `'+p+'`: `'+h+'`' for p,h in hashes.items()]
 (ROOT/'ACD_METHODS_WINDOWS_BETTING.md').write_text('\n'.join(lines)+'\n')
 return dict(LT=protocol.LT,output_spacing=protocol.OUT,windows=windows,code_hashes=hashes,fallback_used=False)
def main():
 d=dict(post_hoc=True,licenses_frozen_route=False,threads_limit=4,resolutions=['R-other: Stage 15A receipt and ranking definitions are not committed in the available branch; B and D remain pending until they land.','Stage 15D is required after Stage 15 A–C by Todd; this task does not modify protected Stage 15 paths.'])
 d['A']=tangent();save(d);print('A complete; exact Stage 9 reproduction',flush=True)
 d['C']=score_selected_risk();save(d);print('C complete; exact decision reproduction',flush=True)
 d['E']=methods();save(d);print('E complete',flush=True)
if __name__=='__main__':main()
