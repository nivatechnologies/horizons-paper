"""Resumable CPU campaign; samplers receive observed windows only."""
import os
os.environ['JAX_PLATFORMS']='cpu'
os.environ['JAX_ENABLE_X64']='true'
import argparse,json,time
from pathlib import Path
import numpy as np,numba
from acd_protocol import *
from acd_fits import case_fits,chi,objective
from acd_posterior import sample,diagnostics,functional_diagnostics,history,implementation_check
from acd_mechanism import forecast
from acd_questions import prepare_dtcheck,coverage,actual,distribution,summary,labels,signed_se

def case(panel,c,forced_draws=None,rerun_stage1a=False):
    directory=ROOT/f'runs/{panel}';directory.mkdir(parents=True,exist_ok=True)
    target=directory/f'case_{c:03d}.npz';report_path=target.with_suffix('.json')
    if target.exists() and not rerun_stage1a:
        previous=json.loads(report_path.read_text())
        if panel!='dev' or previous.get('stage1a_rerun',False) or previous['diagnostics']['sampler']['draws']==settings()['draws']:return previous
        target.unlink();report_path.unlink()
    tick=time.perf_counter();h=dt();y=load_observed(panel,c);config=settings()
    fit_path=directory/f'fits_{c:03d}.npz'
    if fit_path.exists():
        with np.load(fit_path) as d:fit={k:d[k] for k in d.files}
        fit['minimum']=float(fit['minimum']);fit['fhat']=float(fit['fhat'])
        fit_report=json.loads(fit_path.with_suffix('.json').read_text())
    else:
        fit=case_fits(y,panel,c,h,use_jax=config.get('use_jax_gradient',False))
        fit_report=fit.pop('report');np.savez(fit_path,**fit);save_json(fit_path.with_suffix('.json'),fit_report)
    rml=forecast(fit['rml'][fit['rml_valid']],h)
    crude_name='acd-dtcheck' if panel=='dtcheck' else 'acd-crude-'+panel
    crude_sub=3 if panel=='dtcheck' else 0
    crude_theta=np.array([np.r_[y[-1]+NOISE*rng(crude_name,crude_sub,c,m).standard_normal(40),fit['fhat']] for m in range(128)])
    crude=forecast(crude_theta,h,initial_is_last=True)
    D=config['draws'] if forced_draws is None else forced_draws
    kept_per_chain=512 if rerun_stage1a else 128
    sub=2 if rerun_stage1a else None
    excluded=False;last=None
    for attempt in range(2):
        if attempt:sub=6 if panel=='dtcheck' else 1
        theta,sampler_report=sample(y,fit['starts'],panel,c,h,sub=sub,warmup=config['warmup'] if not attempt else 2000,draws=D)
        diag=diagnostics(theta,y,h,sampler_report)
        keep=np.floor(np.arange(kept_per_chain)*D/kept_per_chain).astype(int)
        selected=theta[:,keep].reshape(-1,41);prediction=forecast(selected,h)
        fdiag=functional_diagnostics(prediction['J'].reshape(4,kept_per_chain,9,8))
        full=False
        if not fdiag['passed']:
            selected=theta.reshape(-1,41);prediction=forecast(selected,h);full=True
            fdiag=functional_diagnostics(prediction['J'].reshape(4,D,9,8))
        last=dict(parameters=diag,functions=fdiag,sampler=sampler_report,attempt=attempt,full_forecast=full)
        if diag['passed'] and fdiag['passed']:break
        if attempt:
            excluded=True;resolution('R-diag',f'{panel} case {c} diagnostics after rerun',last)
    from acd_posterior import loglike_batch
    minimum=min(float(fit['minimum']),float(np.min(-2*np.asarray(loglike_batch(theta.reshape(-1,41),y,h,np.zeros(40),np.zeros(40))))))
    np.savez(target,theta=selected,x0=prediction['x0'],J=prediction['J'],
             state_sum=prediction['state_sum'],factual_square_sum=prediction['factual_square_sum'],divergence_sum=prediction['divergence_sum'],
             chain_last=theta[:,-1],map=fit['map'],minimum=minimum,rml_J=rml['J'],crude_J=crude['J'],rml_valid=fit['rml_valid'],excluded=excluded)
    # Truth reads occur only inside the permitted scoring/coverage module.
    cov=coverage(panel,c,y,minimum,h);actual_cost,_=actual(panel,c,h)
    np.savez(directory/f'score_{c:03d}.npz',actual_cost=actual_cost)
    final=dict(case=c,panel=panel,seconds=time.perf_counter()-tick,excluded=excluded,coverage=cov,
               diagnostics=last,fits=fit_report,forecast_draws=len(selected),dt=h,minimum=minimum,
               sha256=digest(target),stage1a_rerun=rerun_stage1a)
    save_json(report_path,final);print('case',panel,c,'seconds',round(final['seconds'],2),'excluded',excluded,flush=True)
    return final

def null():
    target=ROOT/'runs/null/null.npz';target.parent.mkdir(parents=True,exist_ok=True)
    if target.exists():return
    start=time.perf_counter();h=dt()
    initial=np.array([8+rng('acd-climatology',0,c).standard_normal(40) for c in range(4096)])
    states=physics.flow(initial,np.full_like(initial,8.),int(round(50*LT/h)),h)
    result=forecast(np.c_[states,np.full(4096,8.)],h,initial_is_last=True)
    jbar=float(result['J'][:,8,:].mean());probs=distribution(result['J'],jbar)
    np.savez(target,J=result['J'],jbar=jbar,prob=probs)
    save_json(target.with_suffix('.json'),dict(seconds=time.perf_counter()-start,dt=h,jbar=jbar,sha256=digest(target),stage1a_rerun=rerun_stage1a))
    print('null complete',flush=True)

def stage0():
    begin=time.perf_counter();config=settings();save_json(ROOT/'runs/numerics/acd_dt.json',config)
    prepare_dtcheck(dt());y=load_observed('dtcheck',0)
    point=np.r_[y[0]+.1,7.3];value,grad=objective(point,y,dt(),np.zeros(40),np.zeros(40));fd=np.zeros(41)
    for i in range(41):
        delta=np.zeros(41);delta[i]=1e-6
        fd[i]=(objective(point+delta,y,dt(),np.zeros(40),np.zeros(40))[0]-objective(point-delta,y,dt(),np.zeros(40),np.zeros(40))[0])/(2e-6)
    error=float(np.max(np.abs(fd-grad)))
    if error>=1e-6:
        config['use_jax_gradient']=True;resolution('R-grad','Joint adjoint FD error',error);save_json(ROOT/'runs/numerics/acd_dt.json',config)
    reference=physics.simulate(point[None,:40],np.full((1,40),point[40]),dt(),11)[0]
    copied=np.asarray(history(point,dt()));relative=float(np.max(np.abs(reference-copied))/max(1,np.max(np.abs(reference))))
    if relative>1e-12:
        resolution('R-other','JAX copy parity failed','Unmatched JAX kernel must be repaired before sampling')
        raise RuntimeError('Implementation repair required: RK4 parity')
    fits=case_fits(y,'dtcheck',0,dt(),use_jax=config.get('use_jax_gradient',False));fit_report=fits.pop('report')
    root=ROOT/'runs/dtcheck';np.savez(root/'fits_000.npz',**fits);save_json(root/'fits_000.json',fit_report)
    impl=implementation_check(fits['map'],y,dt(),warmup=config['warmup'],draws=config['draws'])
    if not impl['passed']:
        resolution('R-impl','Gaussian check failed at default settings',impl)
        config['warmup']*=2;config['draws']*=2;save_json(ROOT/'runs/numerics/acd_dt.json',config)
        repeated=implementation_check(fits['map'],y,dt(),warmup=config['warmup'],draws=config['draws'])
        impl['repeat']=repeated
        if not repeated['passed']:resolution('R-impl','Gaussian doubled check failed','Retain doubled NumPyro settings and flag')
    save_json(ROOT/'runs/audit/acd_implementation.json',impl)
    ordinary=case('dtcheck',0);ordinary_extra_fit_seconds=fit_report['seconds']
    for c in range(1,8):case('dtcheck',c)
    # Pooled dt comparison. Jbar is computed from the coarse null and held fixed.
    null()
    with np.load(ROOT/'runs/null/null.npz') as n:jbar=float(n['jbar'])
    def dt_comparison(coarse,fine):
        draw_changes=np.zeros(8);class_changes=np.zeros(8);draw_total=np.zeros(8);class_total=np.zeros(8)
        for c in range(8):
            with np.load(root/f'case_{c:03d}.npz') as d:t=d['theta'].copy()
            # Shared decision-time states are computed once at the coarse dt.
            x0=physics.simulate(t[:,:40],np.repeat(t[:,40,None],40,axis=1),coarse,11)[:,-1]
            tt=np.c_[x0,t[:,40]]
            a=labels(forecast(tt,coarse,initial_is_last=True)['J'],jbar)
            b=labels(forecast(tt,fine,initial_is_last=True)['J'],jbar)
            draw_changes+=(a!=b).sum((0,1));draw_total+=a.shape[0]*38
            def classifications(lab):
                probs=np.stack([(lab==ans).mean(0) for ans in range(8)],-1)
                mod=probs.argmax(-1);conf=probs.max(-1)>=.95
                return np.where(conf,mod,-1)
            class_changes+=(classifications(a)!=classifications(b)).sum(0);class_total+=38
        rates=draw_changes/draw_total;classes=class_changes/class_total
        return dict(dt=coarse,fine=fine,answer_change=rates.tolist(),classification_change=classes.tolist(),passed=bool((rates[:6]<=.005).all() and (classes[:6]<=.01).all()))
    checked=dt_comparison(dt(),dt()/2)
    if not checked['passed']:
        resolution('R-dt','Pooled timestep check failed',checked)
        old=dt();config['dt']=old/2;save_json(ROOT/'runs/numerics/acd_dt.json',config)
        # New fit/forecast definition: drop only owned coarse Stage0 artifacts.
        for p in root.glob('case_*'):p.unlink()
        for p in root.glob('fits_*'):p.unlink()
        for p in root.glob('score_*'):p.unlink()
        (ROOT/'runs/null/null.npz').unlink();null()
        with np.load(ROOT/'runs/null/null.npz') as n:jbar=float(n['jbar'])
        finer_reports=[case('dtcheck',c) for c in range(8)]
        ordinary=finer_reports[0];ordinary_extra_fit_seconds=0.
        checked['repeat']=dt_comparison(old/2,old/4)
    from acd_measure import benchmark_refit
    benchmark_case=case('dev',199)
    four=benchmark_refit('dev',199,[0,1,2,3]);allsite=benchmark_refit('dev',199,list(range(40)))
    # Conservative initial projection includes first ordinary compilation/fit cost.
    ordinary_seconds=ordinary['seconds']+ordinary_extra_fit_seconds
    projection=400*ordinary_seconds+1200*four['seconds']+300*allsite['seconds']
    projection*=1.2
    if projection>43200:
        config['cuts']=['R7','R5-A','R6-3LT','RML-conf','P/B-other-leads','R5-3LT']
        reduced=1.2*(400*ordinary_seconds+1200*four['seconds'])
        if reduced>43200:
            config['r5_population']=60;reduced=1.2*(400*ordinary_seconds+720*four['seconds'])
        if reduced>43200:config['draws']=500
        resolution('R-time','Stages1–3 full projection exceeds12h',dict(initial_seconds=projection,after_population_seconds=reduced,settings=config))
        save_json(ROOT/'runs/numerics/acd_dt.json',config)
    report=dict(joint_adjoint_error=error,jax_relative_match=relative,implementation=impl,dtcheck=checked,
                ordinary_seconds=ordinary_seconds,four_site=four,all_site=allsite,projection_seconds=projection,
                settings=settings(),seconds=time.perf_counter()-begin,seeds=assert_leaves())
    save_json(ROOT/'runs/audit/acd_numerical.json',report)
    (ROOT/'ACD_NUMERICAL_REPORT.md').write_text('# ACD numerical report\n\nStage 0 completed on sulaco CPU. Full numerical receipt: runs/audit/acd_numerical.json.\n\n```json\n'+json.dumps(report,indent=2)+'\n```\n')
    print('Stage0 complete',flush=True)

def stage1a():
    reports=[case('dev',c) for c in range(20)]
    with np.load(ROOT/'runs/null/null.npz') as n:jbar=float(n['jbar'])
    disagreement=[];questions=0;repeat_report=[];agreement=[]
    for c in range(20):
        with np.load(ROOT/f'runs/dev/case_{c:03d}.npz') as d:a=d['J'];b=d['rml_J']
        pp,sp=signed_se(a,jbar);pr,sr=signed_se(b,jbar,chains=0)
        z=(pp-pr)/np.sqrt(sp*sp+sr*sr);flag=np.abs(z[:8,3])>3
        disagreement.append(flag);questions+=int(flag.sum())
        agreement.append(dict(case=c,mean_signed_probability_difference_2_3=np.abs(pp-pr)[:,[3,5]].mean(0).tolist(),substantive_S_2_3=(np.abs(z[:8,[3,5]])>3).sum(0).tolist(),threshold_crossing_2_3=((np.maximum(pp[:,[3,5]],1-pp[:,[3,5]])>=.95)!=(np.maximum(pr[:,[3,5]],1-pr[:,[3,5]])>=.95)).sum(0).tolist()))
    if questions/160>.05:
        resolution('R-rml','Stage1a substantive disagreement >5%',dict(questions=questions,total=160))
        for c,flags in enumerate(disagreement):
            if not flags.any():continue
            with np.load(ROOT/f'runs/dev/case_{c:03d}.npz') as d:old=d['J'].copy()
            case('dev',c,forced_draws=4*settings()['draws'],rerun_stage1a=True)
            with np.load(ROOT/f'runs/dev/case_{c:03d}.npz') as d:new=d['J'].copy()
            p,s=signed_se(old,jbar);q,t=signed_se(new,jbar)
            substantive=np.abs((p-q)/np.sqrt(s*s+t*t))[:8,3]>3
            repeat_report.append(dict(case=c,initial_disagreements=int(flags.sum()),posterior_self_disagreements=int((substantive&flags).sum())))
    reports=[json.loads((ROOT/f'runs/dev/case_{c:03d}.json').read_text()) for c in range(20)]
    compared=sum(v['initial_disagreements'] for v in repeat_report)
    self_changed=sum(v['posterior_self_disagreements'] for v in repeat_report)
    if compared and self_changed/compared>.01:resolution('R-rml','Stage1a posterior rerun still substantively differs >1%',dict(changed=self_changed,questions=compared))
    flag_cov=sum(v['coverage']['covered'] for v in reports)<15
    excluded=sum(v['excluded'] for v in reports)
    if flag_cov:resolution('R-cov','Stage1a coverage below15/20','Report and continue')
    if excluded>1:resolution('R-diag','Stage1a exclusion rate>1/20','Flag and continue')
    result=dict(cases=20,covered=sum(v['coverage']['covered'] for v in reports),excluded=excluded,substantive_S_questions_2LT=questions,total_questions=160,reruns=repeat_report,agreement=agreement)
    save_json(ROOT/'runs/audit/acd_stage1a.json',result)
    (ROOT/'ACD_STAGE1A_VALIDATION.md').write_text('# ACD Stage1a validation\n\n```json\n'+json.dumps(result,indent=2)+'\n```\n\nAll flags use §14 resolution rules; development continues to200 cases.\n')
    print('Stage1a complete',flush=True)
def main():
    p=argparse.ArgumentParser();p.add_argument('task',choices=['stage0','stage1a','stage1b','case','batch']);p.add_argument('--case',type=int,default=0);p.add_argument('--panel',default='dtcheck');p.add_argument('--cases',default='');a=p.parse_args()
    numba.set_num_threads(8)
    if a.task=='stage0':stage0()
    elif a.task=='stage1a':stage1a()
    elif a.task=='case':case(a.panel,a.case)
    elif a.task=='batch':
        for c in map(int,a.cases.split(',')):case(a.panel,c)
    else:
        for c in range(200):case('dev',c)
        from acd_measure import campaign
        campaign()
        from acd_analysis import run
        run()
if __name__=='__main__':main()
