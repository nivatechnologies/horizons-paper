"""Observation-only targeting, designed probes, and posterior refits.
Only probe_values opens true, solely to construct the authorized measurement z.
"""
import os
os.environ['JAX_PLATFORMS']='cpu'
os.environ['JAX_ENABLE_X64']='true'
import time,json,argparse
import numpy as np
from acd_protocol import *
from acd_fits import fit,chi
from acd_posterior import sample,diagnostics,functional_diagnostics,loglike_batch
from acd_mechanism import forecast
from acd_questions import coverage
ARMS=['Q','F','V','R','A']
def greedy(x,value):
    joint=np.cov(np.column_stack([x,value]),rowvar=False);chosen=[]
    for _ in range(4):
        gain=joint[:40,40]**2/(np.diag(joint)[:40]+(.1*NOISE)**2)
        gain[chosen]=-np.inf;i=int(gain.argmax());chosen.append(i)
        joint-=np.outer(joint[:,i],joint[i,:])/(joint[i,i]+(.1*NOISE)**2)
    return chosen

def sites_for(panel,c,t,x,j,k,l):
    return [greedy(x,j[:,k,t]-j[:,l,t]),greedy(x,j[:,8,t]),
            np.argsort(-x.var(0,ddof=1),kind='stable')[:4].tolist(),
            rng('acd-measure-'+panel,1,c,0,t).choice(40,4,replace=False).tolist(),list(range(40))]
def probe_values(panel,c,t):
    with np.load(input_path(panel,c),allow_pickle=False) as data:decision=data['true'][-1].copy()
    return decision+.1*NOISE*rng('acd-measure-'+panel,0,c,0,t).standard_normal(40)

def refit(panel,c,t,arm,sites,k,l,base,z,prefix='refit'):
    directory=ROOT/f'runs/{panel}/measure';directory.mkdir(parents=True,exist_ok=True)
    target=directory/f'{prefix}_{c:03d}_{t}_{arm}.npz';receipt=target.with_suffix('.json')
    if receipt.exists():return json.loads(receipt.read_text())
    tick=time.perf_counter();y=load_observed(panel,c);h=dt();config=settings();D=config['draws'];mask=np.zeros(40);mask[sites]=1
    mode,optimization=fit(y,base['map'],h,mask,z,use_jax=config.get('use_jax_gradient',False))
    excluded=False
    for attempt in range(2):
        theta,sreport=sample(y,base['chain_last'],panel,c,h,sub=(20 if attempt else 10)+arm,action=t,warmup=2000 if attempt else config['warmup'],draws=D,mask=mask,z=z)
        diag=diagnostics(theta,y,h,sreport,mask,z)
        keep=np.floor(np.arange(128)*D/128).astype(int);selected=theta[:,keep].reshape(-1,41)
        predicted=forecast(selected,h,actions=[k,l]);full=False
        fun=functional_diagnostics(predicted['J'].reshape(4,128,2,8),indices=(0,1,t))
        if not fun['passed']:
            selected=theta.reshape(-1,41);predicted=forecast(selected,h,actions=[k,l]);full=True
            fun=functional_diagnostics(predicted['J'].reshape(4,D,2,8),indices=(0,1,t))
        if diag['passed'] and fun['passed']:break
        if attempt:
            excluded=True;resolution('R-diag',f'{panel} {c} R5 {ARMS[arm]} refit fails after retry',dict(parameters=diag,function=fun))
    minimum=min(chi(mode,y,h,mask,z),float(np.min(-2*np.asarray(loglike_batch(theta.reshape(-1,41),y,h,mask,z)))))
    cov=coverage(panel,c,y,minimum,h,mask,z)
    event=predicted['J'][:,0,t]<predicted['J'][:,1,t];p=float(event.mean());modal=bool(p>.5);confident=bool(max(p,1-p)>=.95 and p!=.5 and not excluded)
    np.savez(target,J=predicted['J'],theta=selected,sites=sites,z=z,minimum=minimum)
    result=dict(case=c,lead=t,arm=ARMS[arm],sites=sites,k=k,l=l,p=p,modal=modal,confident=confident,excluded=excluded,coverage=cov,optimization=optimization,parameters=diag,functional=fun,full_forecast=full,seconds=time.perf_counter()-tick,sha256=digest(target))
    save_json(receipt,result);print('refit',c,ARMS[arm],round(result['seconds'],2),flush=True);return result

def benchmark_refit(panel,c,sites):
    # Benchmarks use development seed roles; dtcheck has no refit seed roles.
    if panel!='dev':raise ValueError('Refit benchmark must use a development case')
    with np.load(ROOT/f'runs/{panel}/case_{c:03d}.npz') as d:base={key:d[key] for key in d.files}
    k,l=sorted(np.argsort(base['J'][:,:8,3].mean(0),kind='stable')[:2].tolist())
    designed=sites_for(panel,c,3,base['x0'],base['J'],k,l)
    arm=4 if len(sites)==40 else 0
    return refit(panel,c,3,arm,designed[arm],k,l,base,probe_values(panel,c,3),prefix='benchmark')

def population(require_complete=True):
    result=[];config=settings()
    for c in range(200):
        if c==199 and not (ROOT/'runs/ordinary_complete').exists() and not require_complete:break
        path=ROOT/f'runs/dev/case_{c:03d}.npz'
        # Receipts are written last, so a forecast file alone is not completion.
        if not path.with_suffix('.json').exists():
            if require_complete:raise RuntimeError(f'Ordinary development case {c} missing')
            break
        with np.load(path) as d:
            if bool(d['excluded']):continue
            j=d['J'];k,l=sorted(np.argsort(j[:,:8,3].mean(0),kind='stable')[:2].tolist());p=float((j[:,k,3]<j[:,l,3]).mean())
        if max(p,1-p)<.95:result.append(dict(case=c,k=k,l=l))
    return result[:config['r5_population']]

def process_population(rows,worker=0,workers=1):
    config=settings();arms=4 if 'R5-A' in config['cuts'] else 5
    for row in rows:
        c,k,l=row['case'],row['k'],row['l']
        owned=[arm for arm in range(arms) if (c*arms+arm)%workers==worker]
        if not owned:continue
        with np.load(ROOT/f'runs/dev/case_{c:03d}.npz') as d:base={key:d[key] for key in d.files}
        sites=sites_for('dev',c,3,base['x0'],base['J'],k,l);z=probe_values('dev',c,3)
        for arm in owned:refit('dev',c,3,arm,sites[arm],k,l,base,z)

def campaign():
    rows=population();save_json(ROOT/'runs/dev/measure_population.json',dict(lead=3,population=rows,not_evaluable=len(rows)<40));process_population(rows)

def worker(index,workers):
    # Prefix selection is stable as remaining ordinary cases arrive. All earlier
    # case receipts must exist; this cannot skip an unresolved lower index.
    while True:
        done=(ROOT/'runs/ordinary_complete').exists();process_population(population(require_complete=done),index,workers)
        if done:return
        time.sleep(5)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--worker',type=int);p.add_argument('--workers',type=int,default=1);a=p.parse_args()
    if a.worker is None:campaign()
    else:worker(a.worker,a.workers)

