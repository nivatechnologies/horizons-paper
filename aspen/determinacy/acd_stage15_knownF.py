"""Stage 15C fixed-forcing posterior; CPU only; all truth access confined to score()."""
import os
os.environ.update(JAX_PLATFORMS='cpu',JAX_ENABLE_X64='true',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMBA_NUM_THREADS='4',XLA_FLAGS='--xla_cpu_multi_thread_eigen=false')
import json,hashlib,time,sys,subprocess,concurrent.futures
from pathlib import Path
import numpy as np
from acd_protocol import ROOT,PATTERNS,LEADS,WINDOWS,SIGMA,physics
from acd_stage6_forward import RAW
import acd_stage15_knownF_source as known
from acd_posterior import functional_diagnostics
OUT=ROOT/'runs/stage15_knownF';OUT.mkdir(parents=True,exist_ok=True)
SOURCE_SHA='3436c492cc71fba647822d5e37e363ae135e75742227dc4ddaf38fb99f4882c3'
NAMESPACE='acd-stage15-knownF-sampler';ID=int.from_bytes(hashlib.sha256(NAMESPACE.encode()).digest()[:8],'little')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,d):
 tmp=p.with_suffix(p.suffix+'.tmp');tmp.write_text(json.dumps(d,indent=2,allow_nan=False)+'\n');tmp.replace(p)
def save_npz(p,**data):
 tmp=p.with_suffix('.tmp.npz');np.savez_compressed(tmp,**data);tmp.replace(p)
def rng(name,sub,case,member=0,action=0):return np.random.default_rng(np.random.SeedSequence([ID,0,sub,case,member,action]))
def verify():
 assert sha(known.__file__)==SOURCE_SHA,'Stage19 known-F implementation changed'
 import acd_protocol as p
 prior=set(p.ACD_IDS.values())|set(p.protocol.IDS.values())|p.protocol.AAH_IDS
 assert ID not in prior
 leaves=[(ID,0,s,c,m,0) for c in range(200) for s in range(3) for m in (range(128) if s==0 else range(4))]
 assert len(leaves)==len(set(leaves))
 return dict(namespace=NAMESPACE,id=ID,leaf_count=len(leaves),disjoint_prior_ids=sorted(prior),knownF_source_sha256=SOURCE_SHA)
def forecast(theta):
 x=physics.simulate(theta[:,:40],np.full((len(theta),40),8.),.01,11)[:,-1];cost=[];state_sum=None
 for b in range(0,len(x),64):
  xx=x[b:b+64];states=physics.simulate(np.repeat(xx,9,0),np.tile(8+.16*PATTERNS,(len(xx),1)),.01).reshape(len(xx),9,-1,40)
  cost.append(physics.costs(states));v=states[:,8].sum(0);state_sum=v if state_sum is None else state_sum+v
 return dict(x0=x,J=np.concatenate(cost),factual_mean=state_sum/len(x))
def case(c):
 verify();done=OUT/f'case_{c:03d}.json'
 if done.exists():
  d=json.loads(done.read_text())
  for file,h in d['files'].items():assert sha(ROOT/file)==h
  return d
 begin=time.monotonic();source=RAW/f'conf/input_{c:03d}.npz'
 with np.load(source) as z:y=z['observed'].copy()
 fitpath=OUT/f'fits_{c:03d}.npz';meta=fitpath.with_suffix('.json')
 if meta.exists():
  with np.load(fitpath) as z:fit={k:z[k].copy() for k in z.files}
  fit['report']=json.loads(meta.read_text())
 else:
  start=time.monotonic();fit=known.starts(y,c,.01,rng);fit['report']['seconds']=time.monotonic()-start;save_npz(fitpath,**{k:v for k,v in fit.items() if k!='report'});write(meta,fit['report'])
 attempts=[];excluded=True;files=[fitpath,meta]
 for attempt in range(2):
  samplepath=OUT/f'sample_{c:03d}_{attempt}.npz';samplemeta=samplepath.with_suffix('.json')
  if samplemeta.exists():
   with np.load(samplepath) as z:theta=z['theta'].copy()
   sample=json.loads(samplemeta.read_text())
  else:
   theta,sample=known.sample(y,fit['starts'],c,.01,attempt,rng);save_npz(samplepath,theta=theta);write(samplemeta,sample)
  files+=[samplepath,samplemeta];start=time.monotonic();diag=known.diagnostics(theta,y,.01,sample)
  ids=np.floor(np.arange(128)*500/128).astype(int);selected=theta[:,ids].reshape(-1,41);pred=forecast(selected);fun=functional_diagnostics(pred['J'].reshape(4,128,9,8));full=False
  if not fun['passed']:
   selected=theta.reshape(-1,41);pred=forecast(selected);fun=functional_diagnostics(pred['J'].reshape(4,500,9,8));full=True
  attempts.append(dict(attempt=attempt,sampler=sample,parameters=diag,functions=fun,rescored=full,diagnostic_forecast_seconds=time.monotonic()-start))
  if diag['passed'] and fun['passed']:excluded=False;break
 target=OUT/f'forecast_{c:03d}.npz';save_npz(target,theta=selected,excluded=excluded,**pred);files+=[target]
 result=dict(case=c,excluded=excluded,attempts=attempts,draws=len(selected),confidence_vote_threshold=int(np.ceil(.95*len(selected))),seconds=time.monotonic()-begin,fit_seconds=fit['report']['seconds'],observations_sha256=sha(source),files={str(p.relative_to(ROOT)):sha(p) for p in files},realized_outcome_accesses=[])
 write(done,result);print(c,result['seconds'],excluded,flush=True);return result

def score():
 from acd_stage6_analysis import binary,stack,comparisons,loss,calibration
 from acd_stage13_analysis import frozen
 from acd_stage9_receipts import dist
 rows=[json.loads(p.read_text()) for p in sorted(OUT.glob('case_*.json'))]
 assert len(rows)==200,'All case outputs must be written and hashed before scoring'
 for r in rows:
  for file,h in r['files'].items():assert sha(ROOT/file)==h
 # Saved realized outcomes opened only inside this scoring function.
 actual=np.array([np.load(RAW/f'conf/score_{c:03d}.npz')['actual_cost'] for c in range(200)])
 jbar,null=frozen();summaries=[];keep=[];Js=[];Fstd=[];Fcorr=[];rho=[];climate=[];zD=[];zF=[]
 for c,row in enumerate(rows):
  with np.load(OUT/f'forecast_{c:03d}.npz') as z:J=z['J'].copy();excluded=bool(z['excluded'])
  s=binary(J,jbar,null[np.r_[np.arange(8),37]]);summaries.append(s);keep.append(not excluded);Js.append(J)
  D=J[:,:8]-J[:,8,None];va=J[:,:8].var(0,ddof=1);vf=J[:,8].var(0,ddof=1);cov=np.mean((J[:,:8]-J[:,:8].mean(0))*(J[:,8,None]-J[:,8,None].mean(0)),axis=0)*len(J)/(len(J)-1);rho.append(cov/np.sqrt(va*vf));climate.append(D.var(0,ddof=1)/(va+vf));zD.append(np.abs(D.mean(0))/D.std(0,ddof=1));v=J[:,8]-jbar;zF.append(np.abs(v.mean(0))/v.std(0,ddof=1))
  with np.load(RAW/f'conf/case_{c:03d}.npz') as z:theta=z['theta'].copy();PJ=z['J'].copy()
  Fstd.append(float(theta[:,40].std(ddof=1)));corr=[]
  for t in [3,5]:
   values=np.concatenate([PJ[:,8:9,t],PJ[:,:8,t]-PJ[:,8,None,t]],axis=1);corr.append(dict(lead=float(LEADS[t]),J8=float(np.corrcoef(theta[:,40],values[:,0])[0,1]),D=[float(np.corrcoef(theta[:,40],values[:,k])[0,1]) for k in range(1,values.shape[1])]))
  Fcorr.append(corr)
 s=stack(summaries);keep=np.array(keep)
 truth=np.concatenate([actual[:,:8]<actual[:,8,None],(actual[:,8]>jbar)[:,None]],axis=1);accuracy=calibration(s,truth,keep)
 from acd_stats import cp_bounds
 for t,row in enumerate(accuracy):
  mask=s['confident'][keep,8,t];right=s['modal'][keep,8,t]==truth[keep,8,t];n=int(mask.sum());correct=int((mask&right).sum());row['Fc_CP_one_sided95']=dict(answers=n,correct=correct,accuracy=correct/n if n else None,bounds=list(cp_bounds(correct,n)) if n else None)
 gate_summary=dict(cases=len(rows),retained=int(keep.sum()),excluded=int((~keep).sum()),rescored=sum(r['draws']>512 for r in rows),rerun=sum(len(r['attempts'])>1 for r in rows),summed_case_seconds=sum(r['seconds'] for r in rows))
 summaries_by_lead=[]
 for t,lead in enumerate(LEADS):
  summaries_by_lead.append(dict(lead=float(lead),S8_confident_share=float(s['confident'][keep,:8,t].mean()),S7_confident_share=float(s['confident'][keep,1:8,t].mean()),observation_S_share=float(s['observation'][keep,:8,t].mean()),Fc_confident_share=float(s['confident'][keep,8,t].mean()),rho=dist(np.asarray(rho)[keep,:,t].ravel()),c=dist(np.asarray(climate)[keep,:,t].ravel()),z_D=dist(np.asarray(zD)[keep,:,t].ravel()),z_F=dist(np.asarray(zF)[keep,t])))
 receipt=dict(post_hoc=True,licenses_frozen_route=False,contract=verify(),gate_summary=gate_summary,cases=rows,excluded=np.flatnonzero(~keep).tolist(),accuracy=accuracy,shares=summaries_by_lead,comparisons=[r for r in comparisons(s,keep) if r['lead'] in [2,3]],paired_first_loss=loss(s,keep),main_posterior_forcing_sd=dist(np.asarray(Fstd)),main_posterior_forcing_correlation=[dict(lead=float(LEADS[t]),J8=dist(np.array([r[i]['J8'] for r in Fcorr])),D=dist(np.array([r[i]['D'] for r in Fcorr]).ravel())) for i,t in enumerate([3,5])],source_code_hashes={str(p):sha(p) for p in [Path(__file__),Path(known.__file__)]})
 write(ROOT/'receipts/acd_stage15_knownF.json',receipt);(ROOT/'ACD_STAGE15_KNOWNF.md').write_text('# Stage 15C known forcing\n\nPost hoc; licenses no frozen route. Gates, hashes, shares, accuracy, correlations and paired endpoint are recorded in receipts/acd_stage15_knownF.json.\n\n'+json.dumps({k:v for k,v in receipt.items() if k not in ['cases','source_code_hashes']},indent=2)+'\n')

def run():
 verify();cores={}
 for line in subprocess.check_output(['lscpu','-p=CPU,CORE,SOCKET'],text=True).splitlines():
  if line.startswith('#'):continue
  cpu,c,s=map(int,line.split(','));cores.setdefault((s,c),cpu)
 available=[v for v in cores.values() if v in os.sched_getaffinity(0)];usable=available[:-8];groups=[usable[i:i+4] for i in range(0,len(usable)-3,4)]
 def worker(c,g):
  with (OUT/f'worker_{c:03d}.log').open('a') as f:
   r=subprocess.run(['taskset','-c',','.join(map(str,g)),sys.executable,__file__,'case',str(c)],stdout=f,stderr=subprocess.STDOUT)
  if r.returncode:raise RuntimeError(f'KnownF case {c} failed; resumable worker log')
 begin=time.monotonic()
 with concurrent.futures.ThreadPoolExecutor(max_workers=min(5,len(groups))) as pool:list(pool.map(lambda c:worker(c,groups[c%len(groups)]),range(5)))
 pilot=[json.loads((OUT/f'case_{c:03d}.json').read_text()) for c in range(5)];prior=[json.loads(p.read_text()) for p in (RAW/'conf').glob('case_*.json')]
 retry=sum(r['diagnostics'].get('attempt',0)>0 for r in prior)/len(prior);rescore=sum(r['diagnostics'].get('full_forecast',False) for r in prior)/len(prior);mean=np.mean([r['seconds'] for r in pilot]);seconds=200*mean/len(groups)*(1+retry+rescore)
 timing=dict(pilot_wall_seconds=time.monotonic()-begin,pilot_mean_seconds=float(mean),workers=len(groups),cores_per_worker=len(groups[0]),reserved_cpus=available[-8:],projected_seconds=float(seconds),projected_hours=float(seconds/3600),limit_hours=24,passed=bool(seconds<=24*3600),original_retry_rate=retry,original_full_rescore_rate=rescore)
 write(ROOT/'receipts/acd_stage15_knownF_timing.json',timing)
 if not timing['passed']:return
 def queue(i):
  for c in range(5+i,200,len(groups)):worker(c,groups[i])
 with concurrent.futures.ThreadPoolExecutor(max_workers=len(groups)) as pool:list(pool.map(queue,range(len(groups))))
 score()
if __name__=='__main__':
 mode=sys.argv[1]
 if mode=='case':case(int(sys.argv[2]))
 elif mode=='run':run()
 elif mode=='score':score()
