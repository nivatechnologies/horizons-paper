"""Blind Stage19 sampling and reference forecasts; no scoring/truth-reading path."""
import os
os.environ.update(JAX_PLATFORMS='cpu',JAX_ENABLE_X64='true',NUMBA_NUM_THREADS='8',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
from pathlib import Path
import json,time,hashlib,argparse,subprocess,sys,concurrent.futures
import numpy as np
from acd_protocol import ROOT,physics,protocol,PATTERNS,WINDOWS,LEADS
OUT=ROOT/'runs/stage19'; RECEIPT=ROOT/'receipts/acd_stage19_part1.json'
NAMES=['acd-r3-observation','acd-r3-sampler','acd-r3-knownF-sampler']
IDS={n:int.from_bytes(hashlib.sha256(n.encode()).digest()[:8],'little') for n in NAMES}
protocol.IDS.update(IDS)
def rng(n,sub=0,case=0,member=0,action=0):
 n={'acd-sampler-r3':'acd-r3-sampler','acd-posterior-r3':'acd-r3-sampler'}.get(n,n)
 return np.random.default_rng(np.random.SeedSequence([IDS[n],0,sub,case,member,action]))
def sha(p):return protocol.digest(p)
def write(p,data):protocol.write_json(p,data)
def event(c,kind,paths=()):
 row=dict(case=c,kind=kind,time=time.time(),files=[dict(path=str(p.relative_to(ROOT)),sha256=sha(p)) for p in paths])
 p=OUT/f'access_{c:03d}.jsonl'
 with p.open('a') as f:f.write(json.dumps(row)+'\n')
def save_npz(p,**data):
 tmp=p.with_name(p.name+'.tmp')
 with tmp.open('wb') as f:np.savez_compressed(f,**data)
 os.replace(tmp,p)
def verify():
 if not (OUT/'freeze_pushed.json').exists():raise RuntimeError('Freeze A must be pushed before observation generation')
 receipt=json.loads((OUT/'freeze_pushed.json').read_text());freeze=json.loads((ROOT/'receipts/acd_stage19_freeze_a.json').read_text())
 if sha(ROOT/'ACD_STAGE19_FREEZE_A.md')!=receipt['freeze_sha256']:raise RuntimeError('Freeze A changed')
 for p,h in freeze['code_hashes'].items():
  if sha(Path(p))!=h:raise RuntimeError('Frozen code changed '+p)
 for p,h in freeze['null_hashes'].items():
  if sha(ROOT/p)!=h:raise RuntimeError('Frozen null changed '+p)
 import jax,numpyro
 if jax.__version__!='0.11.2' or numpyro.__version__!='0.22.0' or not jax.config.x64_enabled:raise RuntimeError('Exact software/float64 contract failed')
 if os.uname().nodename!='baccus':raise RuntimeError('Stage19 requires Baccus CPU')
 if any(d.platform!='cpu' for d in jax.devices()):raise RuntimeError('Non-CPU JAX device')
def functional(J):
 import arviz as az
 values=np.concatenate([(J[:,:,:8,[3,5]]-J[:,:,8:9,[3,5]]).reshape(4,J.shape[1],16),J[:,:,8,[3,5]]],-1)
 r=np.asarray(az.rhat({'functions':values},method='rank')['functions']);e=np.asarray(az.ess({'functions':values},method='bulk')['functions'])
 return dict(rhat=r.tolist(),ess=e.tolist(),max_rhat=float(r.max()),min_ess=float(e.min()),passed=bool(np.isfinite(r).all() and np.isfinite(e).all() and r.max()<=1.01 and e.min()>=400))
def case(c):
 verify();OUT.mkdir(parents=True,exist_ok=True)
 complete=OUT/f'case_{c:03d}.json'
 if complete.exists():
  cached=json.loads(complete.read_text())
  assert sha(ROOT/cached['observations']['path'])==cached['observations']['sha256']
  for report in cached['arms'].values():
   for p,h in report['files'].items():assert sha(ROOT/p)==h,p
  return cached
 import numba
 numba.set_num_threads(1)
 import acd_fits as fits,acd_posterior as posterior,acd_stage19_knownF as known
 from acd_mechanism import forecast
 from acd_stage6_forward import forward,WEIGHTS
 from acd_stage9_forward import tangent_forward,W
 numba.set_num_threads(1)
 fits.rng=rng
 fits.resolution=lambda rule,trigger,detail:event(c,rule+": "+trigger+": "+str(detail))
 # Separate initializer and primary/retry sample leaves inside the new namespace.
 posterior.rng=lambda name,sub=0,case=0,member=0,action=0:rng(name,sub+1,case,member,action)
 times={};begin=time.monotonic();obs=OUT/f'observed_{c:03d}.npz'
 if not obs.exists():
  t=time.monotonic();true,y=physics.history('acd-r3-observation',c,.01)
  hidden=OUT/'hidden'/f'input_{c:03d}.npz';hidden.parent.mkdir(exist_ok=True)
  # Generation writes the hidden history; no Part1 function ever opens it.
  save_npz(hidden,true=true);save_npz(obs,observed=y);del true
  times['generation']=time.monotonic()-t;event(c,'observations_written_and_hashed',[obs])
 with np.load(obs,allow_pickle=False) as d:y=d['observed'].copy()
 event(c,'observations_read',[obs]);arms={}
 for arm in ['main','knownF']:
  done=OUT/f'{arm}_{c:03d}.json'
  if done.exists():
   cached=json.loads(done.read_text())
   for p,h in cached['files'].items():assert sha(ROOT/p)==h,p
   arms[arm]=cached;continue
  fitfile=OUT/f'{arm}_fits_{c:03d}.npz';fitmeta=fitfile.with_suffix('.json')
  if fitmeta.exists():
   with np.load(fitfile) as d:fit={k:d[k].copy() for k in d.files}
   fit['report']=json.loads(fitmeta.read_text());fit_seconds=fit['report']['seconds']
  else:
   t=time.monotonic();fit=fits.case_fits(y,'r3',c,.01,workers=1) if arm=='main' else known.starts(y,c,.01,rng)
   fit_seconds=time.monotonic()-t;fit['report']['seconds']=fit_seconds
   if int(np.sum(fit['rml_valid']))<4:raise RuntimeError('R-other: fewer than four valid initializers; no sampling')
   save_npz(fitfile,**{k:v for k,v in fit.items() if k!='report'});write(fitmeta,fit['report']);event(c,arm+'_initializers_written_and_hashed',[fitfile,fitmeta])
  attempts=[];excluded=True
  for attempt in range(2):
   samplefile=OUT/f'{arm}_sample_{c:03d}_{attempt}.npz';samplemeta=samplefile.with_suffix('.json')
   if samplemeta.exists():
    with np.load(samplefile) as d:theta=d['theta'].copy()
    sreport=json.loads(samplemeta.read_text())
   else:
    if arm=='main':theta,sreport=posterior.sample(y,fit['starts'],'r3',c,.01,sub=attempt,warmup=1000 if attempt==0 else 2000,draws=500)
    else:theta,sreport=known.sample(y,fit['starts'],c,.01,attempt,rng)
    save_npz(samplefile,theta=theta);write(samplemeta,sreport);event(c,arm+'_sampler_written_and_hashed',[samplefile,samplemeta])
   t=time.monotonic();diag=(posterior.diagnostics if arm=='main' else known.diagnostics)(theta,y,.01,sreport)
   keep=np.floor(np.arange(128)*500/128).astype(int);selected=theta[:,keep].reshape(-1,41)
   pred=forecast(selected,.01);fun=functional(pred['J'].reshape(4,128,9,8));full=False
   if not fun['passed']:
    selected=theta.reshape(-1,41);pred=forecast(selected,.01);full=True;fun=functional(pred['J'].reshape(4,500,9,8))
   attempts.append(dict(attempt=attempt,parameters=diag,functions=fun,sampler=sreport,rescored=full,diagnostic_forecast_seconds=time.monotonic()-t))
   if diag['passed'] and fun['passed']:excluded=False;break
  t=time.monotonic();x=pred['x0'];components={}
  if arm=='main':
   J,block,terms,state=forward(x,selected[:,40],.16,PATTERNS,WEIGHTS);components['global_block_budget_joint_seconds']=time.monotonic()-t
   gt=time.monotonic();G=tangent_forward(x,selected[:,40],PATTERNS[:8],W);components['tangent_seconds']=time.monotonic()-gt
   closure=float(np.max(abs(J-pred['J'])));assert closure<1e-12
   values=dict(theta=selected,x0=x,J=J,block=block,G=G,terms=terms,factual_mean=state.mean(0),excluded=excluded)
  else:
   bt=time.monotonic();blocks=[]
   for b in range(0,len(x),64):
    xx=x[b:b+64];tr=physics.simulate(np.repeat(xx,9,0),(8+.16*PATTERNS)[None].repeat(len(xx),0).reshape(-1,40),.01).reshape(len(xx),9,-1,40)
    blocks.append(np.stack([(.5*np.mean(tr[...,w,:10]**2,-1)).mean(-1) for w in WINDOWS],-1))
   components['block_seconds']=time.monotonic()-bt
   values=dict(theta=selected,x0=x,J=pred['J'],block=np.concatenate(blocks),factual_mean=pred['state_sum'][8]/len(x),excluded=excluded)
  target=OUT/f'{arm}_forecast_{c:03d}.npz';save_npz(target,**values);event(c,arm+'_forecasts_written_and_hashed',[target])
  report=dict(case=c,arm=arm,components=components,excluded=excluded,attempts=attempts,fit_seconds=fit_seconds,forecast_seconds=time.monotonic()-t,forecast_draws=len(x),confidence_vote_threshold=int(np.ceil(.95*len(x))),files={str(p.relative_to(ROOT)):sha(p) for p in [fitfile,fitmeta,target]+[OUT/f'{arm}_sample_{c:03d}_{a}{ext}' for a in range(len(attempts)) for ext in ['.npz','.json']]})
  write(done,report);event(c,arm+'_diagnostics_written_and_hashed',[done]);arms[arm]=report
 result=dict(case=c,arms=arms,seconds=time.monotonic()-begin,times=times,observations=dict(path=str(obs.relative_to(ROOT)),sha256=sha(obs)),realized_outcome_accesses=[])
 write(complete,result);event(c,'case_complete',[complete]);return result

def topology():
 lines=subprocess.check_output(['lscpu','-p=CPU,CORE,SOCKET'],text=True).splitlines();core={}
 for line in lines:
  if line.startswith('#'):continue
  cpu,c,s=map(int,line.split(','));core.setdefault((s,c),cpu)
 available=[v for v in core.values() if v in os.sched_getaffinity(0)];usable=available[:-4]
 return [usable[i:i+4] for i in range(0,len(usable)-3,4)],available[-4:]
def summarize(state,projection=None):
 import fcntl
 with (OUT/"receipt.lock").open("w") as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  return _summarize_locked(state,projection)
def _summarize_locked(state,projection=None):
 rows=[json.loads(p.read_text()) for p in sorted(OUT.glob('case_*.json'))];env=json.loads((ROOT/'receipts/acd_stage19_step0.json').read_text())['environment']
 summary={}
 for arm in ['main','knownF']:
  rr=[r['arms'][arm] for r in rows];summary[arm]=dict(completed=len(rr),excluded=[r['case'] for r in rr if r['excluded']],rerun=[r['case'] for r in rr if len(r['attempts'])>1],rescored=[r['case'] for r in rr if any(a['rescored'] for a in r['attempts'])])
 access=ROOT/'ACD_STAGE19_ACCESS.jsonl'
 access.write_text(''.join(p.read_text() for p in sorted(OUT.glob('access_*.jsonl'))))
 d=dict(stage='19 Part1',status=state,environment=env,timing_projection=projection,cases=rows,gates=summary,realized_outcome_accesses=[],emulator_runs=[],generated_at=time.time())
 write(RECEIPT,d);return d

def run():
 verify();groups,reserved=topology();started=time.monotonic()
 def job(c,cpus):
  log=OUT/f'worker_{c:03d}.log'
  with log.open('a') as f:
   result=subprocess.run(['taskset','-c',','.join(map(str,cpus)),sys.executable,__file__,'case',str(c)],stdout=f,stderr=subprocess.STDOUT)
  if result.returncode:raise RuntimeError(f'Case {c} failed; see {log}')
 with concurrent.futures.ThreadPoolExecutor(max_workers=len(groups)) as pool:
  list(pool.map(lambda c:job(c,groups[c%len(groups)]),range(5)))
 rows=[json.loads((OUT/f'case_{c:03d}.json').read_text()) for c in range(5)]
 # Include original rates as additional allowances rather than treating pilot rates as zero.
 prior=[json.loads(p.read_text()) for p in (OUT/'reused/runs/conf').glob('case_*.json')]
 retry=sum(r['diagnostics'].get('attempt',0)>0 for r in prior)/len(prior)
 full=sum(r['diagnostics'].get('full_forecast',False) for r in prior)/len(prior)
 mean=float(np.mean([r['seconds'] for r in rows]));projected=200*mean/len(groups)*(1+retry+full)
 projection=dict(seconds=projected,hours=projected/3600,limit_hours=24,workers=len(groups),cores_per_worker=len(groups[0]),reserved_cpus=reserved,pilot_wall_seconds=time.monotonic()-started,pilot_mean_seconds=mean,prior_retry_rate=retry,prior_rescore_rate=full,component_seconds={a:{k:float(np.mean([r['arms'][a][k] for r in rows])) for k in ['fit_seconds','forecast_seconds']} for a in ['main','knownF']},passed=bool(projected<=24*3600))
 summarize('timing_passed' if projection['passed'] else 'timing_gate_stopped',projection)
 if not projection['passed']:return
 # One persistent worker per affinity group avoids overlap as case durations vary.
 def queue(index):
  for c in range(5+index,200,len(groups)):job(c,groups[index]);summarize('blind_sampling_running',projection)
 with concurrent.futures.ThreadPoolExecutor(max_workers=len(groups)) as pool:list(pool.map(queue,range(len(groups))))
 result=summarize('blind_sampling_complete',projection);result['wall_seconds']=time.monotonic()-started;write(RECEIPT,result)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('mode',choices=['case','run']);p.add_argument('index',type=int,nargs='?');args=p.parse_args()
 if args.mode=='case':print(json.dumps(case(args.index)),flush=True)
 else:run()
