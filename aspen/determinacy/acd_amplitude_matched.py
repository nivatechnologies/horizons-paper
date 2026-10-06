"""Stage4b: authorized climatological integrations and saved development readings."""
import os
os.environ['JAX_PLATFORMS']='cpu'
os.environ['CUDA_VISIBLE_DEVICES']=''
os.environ['NUMBA_NUM_THREADS']='16'
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
os.environ['MPLBACKEND']='Agg'
import json,hashlib,math,time
from pathlib import Path
import numpy as np
from acd_protocol import PATTERNS,physics,rng,LT,LEADS,WINDOWS,TICKS,ACD_IDS,SUB_ROLES
from acd_questions import distribution
from acd_stats import difference_interval
ROOT=Path(__file__).resolve().parent
RAW=Path('/home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs')
OUT=ROOT/'runs/stage4b_null'
FORECAST=ROOT/'runs/stage4_amplitude'
AMPS=[.04,.08,.16,.32,.64]
DT=.01
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
def integrate(states,amp):
 costs=[]
 for first in range(0,len(states),64):
  x=states[first:first+64]
  f=(np.full((len(x),1,1),8.)+amp*PATTERNS[None]).reshape(-1,40)
  trajectory=physics.simulate(np.repeat(x,9,axis=0),f,DT).reshape(len(x),9,len(TICKS),40)
  costs.append(physics.costs(trajectory))
 return np.concatenate(costs)
def null_only():
 """No development, posterior, calibration, observations or truth inputs enter here."""
 OUT.mkdir(parents=True,exist_ok=True)
 start=time.perf_counter()
 initial=np.array([8+rng('acd-climatology',SUB_ROLES['null'],c).standard_normal(40) for c in range(4096)])
 steps=int(round(50*LT/DT))
 states=physics.flow(initial,np.full_like(initial,8.),steps,DT)
 np.savez(OUT/'states.npz',initial=initial,states=states)
 j=integrate(states,.16)
 regenerated_mean=float(j[:,8,:].mean())
 preliminary_prob=distribution(j,regenerated_mean)
 original=RAW/'null/null.npz'
 with np.load(original,allow_pickle=False) as a:
  old_prob=a['prob'].copy();old_mean=float(a['jbar']);old_j=a['J'].copy()
 tol=8*np.finfo(np.float64).eps
 prob_diff=float(np.max(np.abs(preliminary_prob-old_prob)))
 mean_diff=abs(regenerated_mean-old_mean)
 reproduced=bool(prob_diff<=tol and mean_diff<=tol*max(1.,abs(old_mean)))
 # Preserve the frozen anomaly origin when matched; otherwise use the regenerated origin.
 jbar=old_mean if reproduced else regenerated_mean
 resolutions=[]
 if not reproduced:resolutions.append(dict(rule='R-other',trigger='Regenerated baseline null does not reproduce saved probabilities/mean to float64 round-off',resolution='Use regenerated null probabilities and regenerated no-action mean for every amplitude, including 0.16. Old calibration is not assumed to transfer.',probability_max_abs=prob_diff,jbar_abs=mean_diff))
 files={};outputs={}
 for amp in [.16,.04,.08,.32,.64]:
  z=j if amp==.16 else integrate(states,amp)
  prob=distribution(z,jbar)
  target=OUT/f'null_{amp}.npz';np.savez(target,J=z,prob=prob,jbar=jbar)
  files[str(amp)]=dict(path=str(target.relative_to(ROOT)),sha256=sha(target),amplitude=amp,question_probabilities=prob.tolist(),Fc_above_shares=prob[37,:,1].tolist(),jbar=jbar,no_action_bitwise_equal=np.array_equal(z[:,8],j[:,8]))
  outputs[str(target.relative_to(ROOT))]=sha(target)
  print('null amplitude',amp,'written and hashed',flush=True)
 receipt=dict(panel='climatological',purpose='development exploratory amplitude matching',states=4096,F=8,dt=DT,dtype='float64',threads=16,spinup_LT=50,spinup_steps=steps,seed=dict(name='acd-climatology',id=ACD_IDS['acd-climatology'],sub=SUB_ROLES['null'],case_indices=[0,4095],tuple_template=[ACD_IDS['acd-climatology'],0,SUB_ROLES['null'],'case',0,0],generator='PCG64 / SeedSequence'),patterns=PATTERNS.tolist(),leads=LEADS.tolist(),windows=[w.tolist() for w in WINDOWS],states_path=str((OUT/'states.npz').relative_to(ROOT)),states_sha256=sha(OUT/'states.npz'),source_hashes={str(original):sha(original),'acd_protocol.py':sha(ROOT/'acd_protocol.py'),'acd_mechanism.py':sha(ROOT/'acd_mechanism.py'),'inherited/protocol.py':sha(Path(physics.__file__).with_name('protocol.py')),'inherited/physics.py':sha(Path(physics.__file__))},baseline_comparison=dict(reproduces_to_float64_roundoff=reproduced,probabilities_bitwise_equal=np.array_equal(preliminary_prob,old_prob),probability_max_abs=prob_diff,probability_abs_tolerance=tol,jbar_saved=old_mean,jbar_regenerated=regenerated_mean,jbar_abs=mean_diff,J_max_abs=float(np.max(np.abs(j-old_j))),J_bitwise_equal=np.array_equal(j,old_j),selected_jbar=jbar,use_regenerated_at_every_amplitude=True),amplitudes=files,resolutions=resolutions,seconds=time.perf_counter()-start)
 save(ROOT/'receipts/acd_stage4b_null.json',receipt)
 return receipt
def basic(j,jbar,null):
 n=len(j);signs=j[:,:8]<j[:,8,None];f=j[:,8]>jbar
 count=np.concatenate([signs.sum(0),f.sum(0)[None]])
 modal=count>n/2
 conf=(np.maximum(count,n-count)>=math.ceil(.95*n))&(2*count!=n)
 indices=np.r_[np.arange(8),37]
 climate=np.take_along_axis(null[indices],modal[...,None].astype(int),-1)[...,0]>=.95
 return dict(modal=modal,confident=conf,climate=climate,observation=conf&~climate)
def bootstrap(case_values):
 # Same frozen case seed/sub and B; pool only within-case action means.
 g=rng('acd-bootstrap',SUB_ROLES['bootstrap']['R1']);values=[]
 for first in range(0,10000,250):
  indices=g.integers(0,len(case_values),size=(min(250,10000-first),len(case_values)))
  values.append(case_values[indices].mean(1))
 quantiles=np.quantile(np.concatenate(values),[.025,.975],axis=0)
 return quantiles
def r2a_pattern(b):
 return 'INCONCLUSIVE' if b['empty'] else 'DIFFERS' if (b['point']>=.15 and b['lower']>0) or (b['point']<=-.15 and b['upper']<0) else 'EQUIVALENT' if b['lower']>=-.1 and b['upper']<=.1 else 'INCONCLUSIVE'
def loss_reading(s,keep,prerequisite,observation_loss=False):
 values=[];counts=dict(earlier=0,later=0,same_lead=0,both_beyond=0);case_records=[]
 for c in np.flatnonzero(keep):
  eligible=np.flatnonzero(s['observation'][c,:8,0]&s['confident'][c,8,0])
  pairs=[];local={k:0 for k in counts}
  for k in eligible:
   def lost(a):
    z=np.flatnonzero(~a);return int(z[0]) if len(z) else len(LEADS)
   a=lost(s['observation' if observation_loss else 'confident'][c,k]);b=lost(s['confident'][c,8])
   pairs.append(int(a>b)-int(a<b))
   category='later' if a>b else 'earlier' if a<b else 'both_beyond' if a==len(LEADS) else 'same_lead'
   counts[category]+=1;local[category]+=1
  if pairs:
   values.append(float(np.mean(pairs)))
   case_records.append(dict(case=int(c),eligible_actions=eligible.tolist(),d_loss=values[-1],shares={k:v/len(pairs) for k,v in local.items()}))
 interval=difference_interval(values)
 if interval['point'] is None:pattern='NOT EVALUABLE'
 else:pattern='NO ORDER DETECTED' if interval['empty'] else 'OUTLIVES' if interval['point']>=.2 and interval['lower']>0 else 'PRECEDES' if interval['point']<=-.2 and interval['upper']<0 else 'NO DIRECTIONAL PREFERENCE' if interval['lower']>=-.1 and interval['upper']<=.1 else 'NO ORDER DETECTED'
 status='NOT EVALUABLE' if len(values)<30 else 'PREREQUISITE NOT MET' if not prerequisite else pattern
 return dict(cases=len(values),actions=sum(counts.values()),pair_counts=counts,pair_shares={k:float(np.mean([r['shares'][k] for r in case_records])) if case_records else None for k in counts},case_values=case_records,prerequisite=prerequisite,status=status,numeric_pattern_status=pattern,**interval)
def analyze(null_receipt):
 """Nulls are sealed before development or realized-calibration receipts are read."""
 start=time.perf_counter();dev=json.loads((ROOT/'receipts/acd_stage1.json').read_text())
 keep=[];raw_hashes={}
 for c in range(200):
  p=RAW/f'dev/case_{c:03d}.npz'
  with np.load(p,allow_pickle=False) as a:keep.append(not bool(a['excluded']))
  raw_hashes[str(p)]=sha(p)
 keep=np.array(keep);oldnull=np.array(dev['null']['question_probabilities'])
 old=[]
 for c in range(200):
  with np.load(FORECAST/f'J_0.16_{c:03d}.npz',allow_pickle=False) as a:old.append(basic(a['J'],dev['null']['jbar'],oldnull))
 old={k:np.array([r[k] for r in old]) for k in old[0]}
 rows=[];resolutions=list(null_receipt['resolutions'])
 resolutions.append(dict(rule='R-other',trigger='Changed-amplitude R0 calibration is unavailable and only null forward integrations are newly authorized',resolution='Compute case-ordered R2a/R2b estimates and betting intervals, but formal route status is PREREQUISITE NOT MET for changed amplitudes. Report numerical margin/interval classification separately without a route license. Reuse baseline calibration only if the baseline question origin and classifications match. No realized-action forecast or posterior fit is run.'))
 for amp in AMPS:
  nr=null_receipt['amplitudes'][str(amp)]
  with np.load(ROOT/nr['path'],allow_pickle=False) as a:null=a['prob'].copy();jbar=float(a['jbar'])
  summaries=[];forecast_hashes={}
  for c in range(200):
   p=FORECAST/f'J_{amp}_{c:03d}.npz'
   with np.load(p,allow_pickle=False) as a:summaries.append(basic(a['J'],jbar,null))
   forecast_hashes[str(p.relative_to(ROOT))]=sha(p)
  s={k:np.array([r[k] for r in summaries]) for k in summaries[0]}
  calibration_reusable=bool(amp==.16 and jbar==dev['null']['jbar'] and all(np.array_equal(s[k],old[k]) for k in ['modal','confident','observation']))
  percase=np.stack([s['confident'][keep,:8].mean(1),s['climate'][keep,:8].mean(1),s['observation'][keep,:8].mean(1),s['confident'][keep,8]],axis=1)
  intervals=bootstrap(percase);shares=[]
  names=['confident_S','climate_confident_S','observation_confident_S','confident_Fc']
  for t,lead in enumerate(LEADS):
   row=dict(lead=float(lead))
   for k,name in enumerate(names):
    row[name]=float(percase[:,k,t].mean())
    row[name+'_descriptive']=dict(lower=float(intervals[0,k,t]),upper=float(intervals[1,k,t]),replicates=10000,seed_sub=SUB_ROLES['bootstrap']['R1'],approximate=True)
   row['confident_and_climate_confident_S']=float((s['confident'][keep,:8,t]&s['climate'][keep,:8,t]).mean())
   shares.append(row)
  R2a=[]
  for t in [3,5]:
   b=difference_interval(s['observation'][keep,:8,t].mean(1)-s['confident'][keep,8,t])
   prereq=bool(calibration_reusable and dev['R0'][t]['R0']['status']=='PASS' and dev['R0'][t]['R0_F']['status']=='PASS')
   pattern=r2a_pattern(b)
   R2a.append(dict(lead=float(LEADS[t]),prerequisite=prereq,status=pattern if prereq else 'PREREQUISITE NOT MET',numeric_pattern_status=pattern,**b))
  prereq=bool(calibration_reusable and all(r['R0']['status'] in ['PASS','NOT EVALUABLE'] and r['R0_F']['status'] in ['PASS','NOT EVALUABLE'] for r in dev['R0']))
  R2b=loss_reading(s,keep,prereq);R2b['observation_loss_variant']=loss_reading(s,keep,prereq,True)
  for label,b in [('R2a '+str(r['lead']),r) for r in R2a]+[('R2b',R2b)]:
   if b['empty'] or b['offset']:resolutions.append(dict(rule='R-other',trigger=f'Amplitude {amp} {label} crossed or offset bounds',resolution='Report bounds and point, withhold directional route where bounds are crossed; no threshold changes.',reading=label,amplitude=amp,interval=b))
  baseline_checks=None
  if amp==.16:
   baseline_checks=dict(calibration_inputs_unchanged=calibration_reusable,shares_match=all(shares[t]['confident_S']==dev['R1m']['lead_relationship'][t]['confident_S_share'] and shares[t]['observation_confident_S']==dev['R1m']['lead_relationship'][t]['observation_S_share'] and shares[t]['confident_Fc']==dev['R1m']['lead_relationship'][t]['confident_Fc_share'] for t in range(8)),R2a_match=all(all(row[k]==oldrow[k] for k in ['point','lower','upper','status']) for row,oldrow in zip(R2a,dev['R2a'])),R2b_match=all(R2b[k]==dev['R2b'][k] for k in ['point','lower','upper','cases','actions','status']))
   if not all(baseline_checks.values()):resolutions.append(dict(rule='R-other',trigger='Matched baseline differs from existing development reading',resolution='Keep new matched reading labelled exploratory; do not replace frozen development/confirmation reading or transfer unsupported calibration.',checks=baseline_checks))
  rows.append(dict(amplitude=amp,fraction_true_forcing=amp/8,panel='development',exploratory=True,licenses_abstract=False,cases=int(keep.sum()),calibration_reusable=calibration_reusable,shares=shares,R2a=R2a,R2b=R2b,baseline_checks=baseline_checks,forecast_hashes=forecast_hashes))
 receipt=dict(base='bf614b6510960ccc706ea3e8ecae13797898f759',panel='development',exploratory=True,licenses_abstract=False,states=4096,F=8,dt=DT,cases=200,excluded=int((~keep).sum()),bootstrap_replicates=10000,betting_interval_level=.99,null_reproduction=null_receipt['baseline_comparison'],rows=rows,resolutions=resolutions,raw_posterior_metadata_hashes=raw_hashes,source_hashes={p:sha(ROOT/p) for p in ['receipts/acd_stage4b_null.json','receipts/acd_stage1.json','receipts/acd_stage4_amplitude.json','acd_amplitude_matched.py','acd_stats.py','acd_protocol.py']},seconds=time.perf_counter()-start)
 save(ROOT/'receipts/acd_stage4b_amplitude_matched.json',receipt)
 return receipt
def figures(d):
 import matplotlib.pyplot as plt
 from matplotlib.ticker import NullLocator
 plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
 fig,axs=plt.subplots(1,3,figsize=(12,3.8));x=np.array(AMPS)
 for ax,t in zip(axs[:2],[3,5]):
  for name,label,style,marker in [('confident_S','confident S','--','s'),('observation_confident_S','observation-confident S','-','o')]:
   ax.plot(x,[r['shares'][t][name] for r in d['rows']],color='black',ls=style,marker=marker,label=label)
  # Reference plotted from each saved reading, not an imputed constant.
  ax.plot(x,[r['shares'][t]['confident_Fc'] for r in d['rows']],color='0.55',ls='-.',marker='^',label='sign of the unforced\nwindow-energy anomaly')
  ax.set(xlabel='Action amplitude',ylabel='Share',title=f'Development — {LEADS[t]:g} LT',xscale='log',ylim=(0,1));ax.set_xticks(x,[str(a) for a in AMPS]);ax.xaxis.set_minor_locator(NullLocator());ax.legend(fontsize=7)
 ax=axs[2];y=np.array([r['R2b']['point'] for r in d['rows']]);lo=np.array([r['R2b']['lower'] for r in d['rows']]);hi=np.array([r['R2b']['upper'] for r in d['rows']])
 ax.errorbar(x,y,yerr=[y-lo,hi-y],color='black',ls='-',marker='D',capsize=4,label='matched null, betting 99%')
 ax.axhline(0,color='0.6',ls='--');ax.set(xscale='log',xlabel='Action amplitude',ylabel='Later minus earlier loss share',title='Development — eligible-case mean');ax.set_xticks(x,[str(a) for a in AMPS]);ax.xaxis.set_minor_locator(NullLocator());ax.legend(fontsize=7)
 fig.tight_layout();out=ROOT/'figures';out.mkdir(exist_ok=True)
 for ext in ['pdf','png']:fig.savefig(out/('F6_amplitude.'+ext),dpi=220,metadata={'Creator':'Aspen analysis','CreationDate':None,'ModDate':None} if ext=='pdf' else None)
 plt.close(fig)
 caption='F6. DEVELOPMENT / EXPLORATORY, five tested amplitudes and 200 saved development posterior re-forecasts. Matched 4096-state climatological null at each amplitude. Confident S: dashed squares; observation-confident S: solid circles; the sign of the unforced window-energy anomaly: dash-dot triangles in grey. Loss difference: solid diamonds with v2.3 betting 99% intervals. These are case-ordered estimates, not confirmation evidence. Changed-amplitude R0 calibration has not been run, so their formal R2a/R2b routes are PREREQUISITE NOT MET; numerical margin/interval patterns do not license comparisons in the abstract. No interpolation claim across untested amplitudes.'
 (out/'F6_amplitude_CAPTION.md').write_text(caption+'\n')
 save(ROOT/'receipts/acd_stage4b_figures.json',dict(source_hashes={'receipts/acd_stage4b_amplitude_matched.json':sha(ROOT/'receipts/acd_stage4b_amplitude_matched.json')},outputs={f'figures/F6_amplitude.{ext}':sha(out/('F6_amplitude.'+ext)) for ext in ['pdf','png']},caption=caption))
def report(d):
 c=d['null_reproduction'];lines=['# Aspen amplitude exploration with matched climatology — DEVELOPMENT / EXPLORATORY','',
 'This licenses nothing in the abstract and changes no frozen confirmation reading. New authorization is limited to forward integration of the climatological null. No posterior, MAP, RML, realized-action forecast, training, inference or cloud computation. Executed on sulaco CPU with 16 integration threads; Qwen services untouched.',
 '',
 f"Frozen null: 4096 states at F=8, acd-climatology ID {ACD_IDS['acd-climatology']}, sub 0, case index 0–4095, PCG64/SeedSequence, initial 8+N(0,1), spin-up 50 LT ({int(round(50*LT/DT))} RK4 steps at dt {DT}). Identical spun-up states for all five amplitudes, the frozen patterns, output ticks and one-LT windows. Regenerated states are saved for future receipt reuse.",
 '',
 f"**Baseline reproduction:** probabilities bitwise equal = {c['probabilities_bitwise_equal']}; maximum absolute probability difference {c['probability_max_abs']!r}; tolerance {c['probability_abs_tolerance']!r}. No-action mean saved/regenerated = {c['jbar_saved']!r}/{c['jbar_regenerated']!r}; J bitwise equal = {c['J_bitwise_equal']}. Regenerated matched nulls are used at every amplitude, including 0.16. Saved frozen mean is retained when matched; otherwise the regenerated mean governs all amplitudes.",
 '',
 '**Definitions:** confident S uses at least ceil(0.95·draws) votes for a unique modal answer. Climate-confident S means at least 95% of the matched null gives that posterior modal answer, whether or not the posterior is confident. Observation-confident S is confident and not climate-confident. Thus confident S = observation-confident S + the confident-and-climate overlap; the raw climate-confident share need not equal confident minus observation. Tied posterior modes use answer 0 under the frozen code and are not confident. Fc means the sign of the unforced window-energy anomaly.',
 '',
 '**R-other / route prerequisites:** changed-amplitude realized calibration is absent. No new realized-action integration is authorized. R2a/R2b points and v2.3 betting 99% intervals are computed, but formal routes are PREREQUISITE NOT MET at changed amplitudes. The separate numerical-pattern column applies only the frozen margin/bounds classification; it is not a route, abstract license or confirmation result. At 0.16, baseline calibration is reused only when the question origin and posterior/modal/confidence/observation classifications match exactly. No new threshold is selected.',
 '',
 '## All tested leads','',
 '| Amplitude | Lead LT | Confident S | Climate-confident S | Observation-confident S | Confident Fc | Confident + climate overlap |',
 '|---|---|---|---|---|---|---|']
 for r in d['rows']:
  for s in r['shares']:lines.append('| '+' | '.join(repr(v) for v in [r['amplitude'],s['lead'],s['confident_S'],s['climate_confident_S'],s['observation_confident_S'],s['confident_Fc'],s['confident_and_climate_confident_S']])+' |')
 lines+=['','All shares are proportions. Their approximate descriptive 95% case-bootstrap intervals (B=10000, frozen acd-bootstrap sub 1) are in the JSON receipt; they do not gate or license comparison words.','', '## R2a: observation-confident S minus confident Fc','', '| Amplitude | Lead LT | Point | Betting 99% interval | Formal route status | Numerical pattern only |','|---|---|---|---|---|---|']
 for r in d['rows']:
  for a in r['R2a']:lines.append('| '+' | '.join(map(str,[r['amplitude'],a['lead'],a['point'],[a['lower'],a['upper']],a['status'],a['numeric_pattern_status']]))+' |')
 lines+=['','## R2b: first confidence loss on the tested lead grid','',
 'Eligible actions are observation-confident S at lead 0 with confident Fc at lead 0. The point is the mean over eligible cases of their eligible-action mean [later minus earlier]. Cases with no eligible action are excluded. Beyond-grid losses follow the frozen tie rule. Case-index order is preserved for predictable betting. Detailed pair counts/shares, per-case values and observation-loss variant are saved in the receipt.',
 '', '| Amplitude | Eligible cases | Eligible actions | Delta_loss | Betting 99% interval | Formal route status | Numerical pattern only |','|---|---|---|---|---|---|']
 for r in d['rows']:
  a=r['R2b'];lines.append('| '+' | '.join(map(str,[r['amplitude'],a['cases'],a['actions'],a['point'],[a['lower'],a['upper']],a['status'],a['numeric_pattern_status']]))+' |')
 lines+=['','## Prior proxy table — retained for reference','',
 'The old frozen-0.16-null proxy report and receipt are unchanged: ACD_AMPLITUDE_EXPLORATORY.md and receipts/acd_stage4_amplitude.json. That table is reproduced below as historical proxy readings; do not confuse it with the matched results above.','']
 old=(ROOT/'ACD_AMPLITUDE_EXPLORATORY.md').read_text()
 start=old.index('| Amplitude');end=old.index('\n\n',start)
 lines.append(old[start:end])
 lines+=['','## Resolution rules','', '| Rule | Trigger | Resolution |','|---|---|---|']
 for r in d['resolutions']:lines.append('| '+r['rule']+' | '+r['trigger']+' | '+r['resolution']+' |')
 lines+=['','No H1–H3 stop. Numerical baseline checks, source/output hashes, null probabilities, all-lead shares and intervals: receipts/acd_stage4b_null.json and receipts/acd_stage4b_amplitude_matched.json. Figure: figures/F6_amplitude.pdf and figures/F6_amplitude.png; caption: figures/F6_amplitude_CAPTION.md. Original proxy forecasts, calibration receipts, confirmation readings, draft and abstract audit are unchanged.','']
 (ROOT/'ACD_AMPLITUDE_MATCHED.md').write_text('\n'.join(lines).rstrip()+'\n')
def run():
 start=time.perf_counter()
 n=null_only();d=analyze(n);figures(d);report(d)
 print('Matched exploration completed in',time.perf_counter()-start,'seconds',flush=True)
 print(json.dumps(dict(reproduction=n['baseline_comparison'],loss=[dict(amplitude=r['amplitude'],point=r['R2b']['point'],lower=r['R2b']['lower'],upper=r['R2b']['upper'],status=r['R2b']['status'],pattern=r['R2b']['numeric_pattern_status']) for r in d['rows']],rules=[r['rule'] for r in d['resolutions']]),indent=2),flush=True)
if __name__=='__main__':run()
