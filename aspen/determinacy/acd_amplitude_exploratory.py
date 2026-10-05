"""Authorized development amplitude exploration; reuses draws, never samples."""
import os
os.environ['JAX_PLATFORMS']='cpu'
os.environ['CUDA_VISIBLE_DEVICES']=''
os.environ['NUMBA_NUM_THREADS']='2'
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
import json,hashlib,time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import numpy as np
ROOT=Path(__file__).resolve().parent
RAW=Path('/home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs')
OUT=ROOT/'runs/stage4_amplitude'
AMPS=[.04,.08,.16,.32,.64]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def task(item):
 c,amp=item
 from acd_protocol import PATTERNS,physics
 p=RAW/f'dev/case_{c:03d}.npz'
 out=OUT/f'J_{amp}_{c:03d}.npz'
 if out.exists():return c,amp
 with np.load(p,allow_pickle=False) as d:
  x0=d['x0'].copy();theta=d['theta'].copy()
  if amp==.16:j=d['J'].copy()
 if amp!=.16:
  blocks=[]
  for first in range(0,len(theta),64):
   t=theta[first:first+64];x=x0[first:first+64]
   state=physics.simulate(np.repeat(x,9,axis=0),(t[:,40,None,None]+amp*PATTERNS[None]).reshape(-1,40),.01).reshape(len(t),9,84,40)
   blocks.append(physics.costs(state))
  j=np.concatenate(blocks)
 np.savez_compressed(out,J=j)
 return c,amp
def analyze():
 from acd_stats import difference_interval
 dev=json.loads((ROOT/'receipts/acd_stage1.json').read_text())
 null=np.array(dev['null']['question_probabilities']);keep=[];post=[];source={}
 for c in range(200):
  p=RAW/f'dev/case_{c:03d}.npz';source[str(p)]=sha(p)
  with np.load(p,allow_pickle=False) as a:keep.append(not bool(a['excluded']))
 keep=np.array(keep);rows=[]
 for amp in AMPS:
  confs=[];obss=[];hashes={}
  for c in range(200):
   p=OUT/f'J_{amp}_{c:03d}.npz';hashes[str(p.relative_to(ROOT))]=sha(p)
   with np.load(p,allow_pickle=False) as a:j=a['J']
   signs=j[:,:8]<j[:,8,None];f=j[:,8]>dev['null']['jbar']
   probabilities=np.concatenate([signs.mean(0),f.mean(0)[None]])
   modal=probabilities>=.5;conf=np.maximum(probabilities,1-probabilities)>=.95
   climate=np.take_along_axis(null[np.r_[np.arange(8),37]],modal[...,None].astype(int),-1)[...,0]>=.95
   confs.append(conf);obss.append(conf&~climate)
  conf=np.array(confs);obs=np.array(obss);loss=[]
  for c in np.flatnonzero(keep):
   eligible=np.flatnonzero(obs[c,:8,0]&conf[c,8,0]);values=[]
   for k in eligible:
    def first_loss(a):
     x=np.flatnonzero(~a);return int(x[0]) if len(x) else 8
    a,b=first_loss(conf[c,k]),first_loss(conf[c,8]);values.append(int(a>b)-int(a<b))
   if values:loss.append(float(np.mean(values)))
  interval=difference_interval(loss)
  shares=[dict(lead=lead,confident_S=float(conf[keep,:8,t].mean()),observation_confident_S_frozen_null_proxy=float(obs[keep,:8,t].mean()),confident_Fc=float(conf[keep,8,t].mean())) for t,lead in [(3,2),(5,3)]]
  row=dict(amplitude=amp,panel='development',exploratory=True,cases=int(keep.sum()),shares=shares,baseline_null_R2b_proxy=dict(cases=len(loss),**interval),amplitude_matched_observation_confident=amp==.16,matched_null_R2b=interval if amp==.16 else None,forecast_hashes=hashes)
  rows.append(row)
 data=dict(panel='development',exploratory=True,licenses_abstract=False,source_hashes=source,rows=rows,resolutions=[dict(rule='R-other',trigger='No saved initial states for amplitude-matched climatological nulls',resolution='For changed amplitudes report frozen 0.16-null-relative proxy explicitly; amplitude-matched observation confidence and R2b are unavailable. Do not create climatology runs or treat proxies as licensed R2b readings.')])
 (ROOT/'receipts/acd_stage4_amplitude.json').write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
 lines=['# Aspen amplitude exploration — DEVELOPMENT / EXPLORATORY','',
 'This licenses nothing in the abstract. Saved development posterior draws and terminal states are re-forecast under the same patterns, leads, windows and questions; no new posterior, MAP, RML or training. Amplitude 0.16 reuses saved J exactly. Other amplitudes use the inherited float64 RK4 integrator at frozen dt 0.01. Existing factual predictions are unchanged.',
 '',
 '**R-other:** the saved climatological receipt contains costs and probabilities, not initial states. A matched climatological null at other amplitudes cannot be obtained solely by re-forecasting saved states. No new climatology run is authorized here. The table explicitly reports observation-confidence relative to the frozen 0.16 null as an exploratory proxy. Amplitude-matched observation-confidence and R2b are unavailable outside 0.16. The displayed loss point and 99% betting interval likewise use that frozen-null eligibility proxy; they carry no R2b route status, calibration claim or abstract license. The 0.16 row is the matched development reading.',
 '',
 '| Amplitude | Lead (LT) | Confident S | Observation-confident S (0.16-null proxy) | Confident Fc | Proxy loss difference | Proxy 99% interval | Matched null? |',
 '|---|---|---|---|---|---|---|---|']
 for r in rows:
  b=r['baseline_null_R2b_proxy']
  for s in r['shares']:lines.append('| '+' | '.join(map(str,[r['amplitude'],s['lead'],s['confident_S'],s['observation_confident_S_frozen_null_proxy'],s['confident_Fc'],b['point'],[b['lower'],b['upper']],r['amplitude_matched_observation_confident']]))+' |')
 lines+=['','Fc denotes the sign of the unforced window-energy anomaly. Loss is first nonconfident tested lead, or beyond-grid; differences are averaged within eligible cases then over cases, using the v2.3 continuous betting inversion. No realized trajectory is opened by the exploration. Posterior diagnostic exclusions follow existing receipts. Details and source/output hashes: receipts/acd_stage4_amplitude.json.','']
 (ROOT/'ACD_AMPLITUDE_EXPLORATORY.md').write_text('\n'.join(lines))
 print('Exploration finished',flush=True)
def run():
 if not all((RAW/f'dev/case_{c:03d}.npz').exists() for c in range(200)):
  (ROOT/'ACD_AMPLITUDE_EXPLORATORY.md').write_text('# Development exploratory amplitude analysis\n\nSKIPPED: complete saved development posterior draws unavailable. No new posterior is run.\n');return
 OUT.mkdir(parents=True,exist_ok=True)
 with ProcessPoolExecutor(max_workers=8) as pool:
  for i,item in enumerate(pool.map(task,[(c,a) for a in AMPS for c in range(200)])):
   if (i+1)%50==0:print('Forecast receipts',i+1,'/1000',flush=True)
 analyze()
if __name__=='__main__':run()
