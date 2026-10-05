"""Confirmation observations, observed-only inference, then permitted scoring.

No data is generated unless both scientific and execution-code freezes verify.
"""
import os
os.environ['JAX_PLATFORMS']='cpu'
os.environ['JAX_ENABLE_X64']='true'
import argparse,json,time,subprocess
import numpy as np
from acd_protocol import *
from acd_fits import fit,chi
from acd_posterior import sample,diagnostics,functional_diagnostics,loglike_batch
from acd_mechanism import forecast
from acd_questions import actual,coverage

def verify_freeze():
    d=json.loads((ROOT/'receipts/acd_freeze_code.json').read_text())
    hashes=dict(d['hashes']);repair=ROOT/'receipts/acd_execution_repair.json'
    if repair.exists():hashes.update(json.loads(repair.read_text())['hashes'])
    for name,sha in hashes.items():
        if digest(ROOT/name)!=sha:raise RuntimeError(f'Execution freeze changed: {name}')
    if settings()!=d['settings']:raise RuntimeError('Frozen compute settings changed')
    for name,sha in d['inherited'].items():
        if digest(INHERITED/name)!=sha:raise RuntimeError(f'Inherited source changed: {name}')
    if digest(INHERITED/'inputs/CNN-20k.pt')!=d['checkpoint']:raise RuntimeError('Checkpoint changed')
    for row in d['null_raw_manifest']:
        if digest(ROOT/row['path'])!=row['sha256']:raise RuntimeError('Frozen null changed')
    # An explicit receipt is transferred only after both freeze commits were pushed.
    pushed=ROOT/'receipts/acd_freeze_pushed.json'
    if not pushed.exists():raise RuntimeError('H2: pushed-freeze receipt missing')
    receipt=json.loads(pushed.read_text())
    if receipt['execution_receipt_sha256']!=digest(ROOT/'receipts/acd_freeze_code.json'):
        raise RuntimeError('H2: pushed execution freeze differs')
    if repair.exists() and receipt.get('repair_receipt_sha256')!=digest(repair):
        raise RuntimeError('H2: execution repair must be committed and pushed')
    if os.uname().nodename!='sulaco':raise RuntimeError('H3: compute requires sulaco')

def event(c,kind,paths=()):
    p=ROOT/f'runs/conf/order_{c:03d}.jsonl';p.parent.mkdir(parents=True,exist_ok=True)
    row=dict(case=c,kind=kind,time=time.time(),files=[dict(path=str(v.relative_to(ROOT)),sha256=digest(v)) for v in paths])
    with p.open('a') as f:f.write(json.dumps(row)+'\n')

def prepare(c):
    """Generate the authorized history; isolate truth from observation consumers."""
    verify_freeze();p=input_path('conf',c);hidden=truth_path('conf',c)
    if p.exists():
        if not hidden.exists():raise RuntimeError('Partial history requires repair before inference')
        return
    hidden.parent.mkdir(parents=True,exist_ok=True)
    true,observed=physics.history('acd-observation-conf',c,dt())
    np.savez(hidden,true=true);np.savez(p,observed=observed)
    event(c,'observations_written_and_hashed',[p])

def confirmation_fits(y,h):
    """R-other: omitted RML replaced by four observation-only MAP starts."""
    fhat=physics.identify(y,h)
    starts=[np.r_[y[0],f] for f in [fhat,6.5,9.5,8.0]]
    results=[fit(y,start,h) for start in starts]
    index=int(np.argmin([r[1]['chi2'] for r in results]))
    return dict(map=results[index][0],starts=np.asarray([r[0] for r in results]),
                minimum=float(results[index][1]['chi2']),fhat=fhat,
                report=dict(maps=[r[1] for r in results],rml='cut',
                            start_forcings=[float(v[40]) for v in starts],
                            boundary_contacts=int(sum(abs(r[0][40]-6)<1e-8 or abs(r[0][40]-10)<1e-8 for r in results))))

def infer(c):
    prepare(c);directory=ROOT/'runs/conf';p=directory/f'case_{c:03d}.npz'
    if p.with_suffix('.json').exists():return
    tick=time.perf_counter();h=dt();config=settings();y=load_observed('conf',c)
    fits=confirmation_fits(y,h);fit_report=fits.pop('report');D=config['draws'];excluded=False
    for attempt in range(2):
        theta,sreport=sample(y,fits['starts'],'conf',c,h,sub=attempt,
                            warmup=2000 if attempt else config['warmup'],draws=D)
        diag=diagnostics(theta,y,h,sreport)
        keep=np.floor(np.arange(128)*D/128).astype(int)
        selected=theta[:,keep].reshape(-1,41);prediction=forecast(selected,h)
        fun=functional_diagnostics(prediction['J'].reshape(4,128,9,8));full=False
        if not fun['passed']:
            selected=theta.reshape(-1,41);prediction=forecast(selected,h);full=True
            fun=functional_diagnostics(prediction['J'].reshape(4,D,9,8))
        if diag['passed'] and fun['passed']:break
        if attempt:
            excluded=True;resolution('R-diag',f'conf case {c} diagnostic retry fails',dict(parameters=diag,functions=fun))
    minimum=min(fits['minimum'],float(np.min(-2*np.asarray(loglike_batch(theta.reshape(-1,41),y,h,np.zeros(40),np.zeros(40))))))
    np.savez(p,theta=selected,x0=prediction['x0'],J=prediction['J'],
             state_sum=prediction['state_sum'],factual_square_sum=prediction['factual_square_sum'],
             divergence_sum=prediction['divergence_sum'],chain_last=theta[:,-1],map=fits['map'],minimum=minimum,excluded=excluded)
    event(c,'posterior_written_and_hashed',[p])
    crude_theta=np.array([np.r_[y[-1]+NOISE*rng('acd-crude-conf',0,c,m).standard_normal(40),fits['fhat']] for m in range(128)])
    crude=forecast(crude_theta,h,initial_is_last=True);crude_path=directory/f'crude_{c:03d}.npz'
    np.savez(crude_path,J=crude['J']);event(c,'crude_written_and_hashed',[crude_path])
    result=dict(case=c,panel='conf',dt=h,excluded=excluded,minimum=minimum,
                diagnostics=dict(parameters=diag,functions=fun,sampler=sreport,attempt=attempt,full_forecast=full),
                fits=fit_report,forecast_draws=len(selected),seconds=time.perf_counter()-tick,sha256=digest(p))
    save_json(p.with_suffix('.json'),result);print('conf CPU',c,result['seconds'],excluded,flush=True)

def score(c):
    verify_freeze();directory=ROOT/'runs/conf';p=directory/f'case_{c:03d}.npz';target=directory/f'score_{c:03d}.npz'
    if target.exists():return
    kinds=[json.loads(l)['kind'] for l in (directory/f'order_{c:03d}.jsonl').read_text().splitlines()]
    required=['observations_written_and_hashed','posterior_written_and_hashed','crude_written_and_hashed','cnn_written_and_hashed']
    if kinds[:4]!=required:raise RuntimeError(f'H1: blind order missing for case {c}: {kinds}')
    report=json.loads(p.with_suffix('.json').read_text());y=load_observed('conf',c)
    actual_cost,_=actual('conf',c,dt());cov=coverage('conf',c,y,report['minimum'],dt())
    np.savez(target,actual_cost=actual_cost)
    report['coverage']=cov;save_json(p.with_suffix('.json'),report)
    event(c,'realized_outcomes_after_all_sampler_hashes',[target]);print('conf scored',c,flush=True)

def population():
    rows=[]
    for c in range(200):
        p=ROOT/f'runs/conf/case_{c:03d}.npz'
        if not (ROOT/f'runs/conf/score_{c:03d}.npz').exists():raise RuntimeError(f'Incomplete confirmation case {c}')
        with np.load(p) as d:
            if bool(d['excluded']):continue
            j=d['J'];k,l=sorted(np.argsort(j[:,:8,3].mean(0),kind='stable')[:2].tolist());p=float((j[:,k,3]<j[:,l,3]).mean())
        if max(p,1-p)<.95:rows.append(dict(case=c,k=k,l=l))
    return rows[:settings()['r5_population']]

def measures(worker,workers):
    verify_freeze()
    from acd_measure import sites_for,probe_values,refit
    rows=population();save_json(ROOT/'runs/conf/measure_population.json',dict(lead=3,population=rows,not_evaluable=len(rows)<40))
    for row in rows:
        c,k,l=row['case'],row['k'],row['l']
        owned=[arm for arm in range(4) if (c*4+arm)%workers==worker]
        if not owned:continue
        with np.load(ROOT/f'runs/conf/case_{c:03d}.npz') as d:base={key:d[key] for key in d.files}
        sites=sites_for('conf',c,3,base['x0'],base['J'],k,l);z=probe_values('conf',c,3)
        for arm in owned:refit('conf',c,3,arm,sites[arm],k,l,base,z)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('task',choices=['cpu','score','measure']);p.add_argument('--worker',type=int,default=0);p.add_argument('--workers',type=int,default=1);a=p.parse_args()
    if a.task=='measure':measures(a.worker,a.workers)
    else:
        for c in range(a.worker,200,a.workers):(infer if a.task=='cpu' else score)(c)
