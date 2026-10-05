"""Confirmation readings at the frozen statistics, with authorized truth scoring."""
import os
os.environ['JAX_PLATFORMS']='cpu'
os.environ['JAX_ENABLE_X64']='true'
import json,time
import numpy as np
from scipy.stats import norm,kstest
from acd_protocol import *
from acd_stats import r0,r0_f,difference_interval,cp_bounds,mcnemar,one_sided,descriptive_ratio_bootstrap
from acd_questions import summary,labels,signed_se
from acd_mechanism import mechanism
from acd_measure import ARMS

def basic(j,jbar,null):
    lab=labels(j,jbar);probs=np.stack([(lab==a).mean(0) for a in range(8)],-1);modal=probs.argmax(-1);p=probs.max(-1)
    conf=(p>=.95)&((probs==p[...,None]).sum(-1)==1)
    climate=np.take_along_axis(null,modal[...,None],-1)[...,0]>=.95
    return dict(modal=modal,p=p,confident=conf,climate=climate,observation=conf&~climate)
def boot(a,b=None,sub=1):
    a=np.asarray(a,float);b=np.ones_like(a) if b is None else np.asarray(b,float)
    return descriptive_ratio_bootstrap(a,b,rng('acd-bootstrap',sub))
def median_boot(values):
    values=np.asarray(values);g=rng('acd-bootstrap',2);draws=[]
    for first in range(0,10000,50):
        idx=g.integers(0,len(values),size=(min(50,10000-first),len(values)))
        selected=values[idx];axes=(1,2) if values.ndim==3 else 1
        draws.extend(np.median(selected,axis=axes).tolist())
    return dict(interval=np.quantile(draws,[.025,.975],axis=0).tolist(),approximate=True,replicates=10000)

def calibration(s,truth,keep,bootstrap_sub=0,lead_indices=range(8)):
    results=[]
    for t in lead_indices:
        obs=s['observation'][:,:,t][:,:8];right=s['modal'][:,:,t][:,:8]==truth[:,:,t][:,:8]
        n=obs.sum(1);correct=(obs&right).sum(1);primary=r0(n[keep],correct[keep]);sensitivity=r0(n,correct)
        order={'PASS':0,'INSUFFICIENT':1,'FAIL':2}
        status=primary['status']
        if status!='NOT EVALUABLE' and sensitivity['status']!='NOT EVALUABLE':status=max([status,sensitivity['status']],key=lambda v:order[v])
        for name,result in [('primary',primary),('included',sensitivity)]:
            result['bounds_crossed']=result['case_lower']>result['case_upper'];result['point_outside_bounds']=result['case_accuracy'] is not None and not result['case_lower']<=result['case_accuracy']<=result['case_upper']
            if result['bounds_crossed'] or result['point_outside_bounds']:resolution('R-other',f'R0 {LEADS[t]} {name} bounds conflict/offset',result)
        primary.update(status=status,included_excluded=sensitivity,answer_descriptive=boot(correct[keep],n[keep],bootstrap_sub))
        fc=s['confident'][:,37,t]&keep;good=s['modal'][:,37,t]==truth[:,37,t]
        f=r0_f(int((good&fc).sum()),int(fc.sum()));f.update(correct=int((good&fc).sum()),answers=int(fc.sum()),accuracy=float(good[fc].mean()) if fc.any() else None)
        results.append(dict(lead=float(LEADS[t]),R0=primary,R0_F=f))
    return results

def reliability(s,truth,keep):
    bins=[.5,.6,.7,.8,.9,.95,1.00000001];out=[]
    for lo,hi in zip(bins[:-1],bins[1:]):
        selection=(s['p']>=lo)&(s['p']<hi)&keep[:,None,None];correct=s['modal']==truth
        out.append(dict(lower=lo,upper=min(1.,hi),answers=int(selection.sum()),accuracy=float(correct[selection].mean()) if selection.any() else None))
    return out

def r5():
    pop=json.loads((ROOT/'runs/conf/measure_population.json').read_text())['population'];n=len(pop);out={};binary={}
    for arm,name in enumerate(ARMS):
        rows=[];correct=[];settled=[];covered=[]
        for entry in pop:
            c,k,l=entry['case'],entry['k'],entry['l'];p=ROOT/f'runs/conf/measure/refit_{c:03d}_3_{arm}.json'
            if not p.exists():
                if arm<4 or 'R5-A' not in settings()['cuts']:raise RuntimeError(f'Incomplete R5 result: {p}')
                continue
            row=json.loads(p.read_text());rows.append(row)
            with np.load(ROOT/f'runs/conf/score_{c:03d}.npz') as data:j=data['actual_cost']
            actual=bool(j[k,3]<j[l,3]);settled.append(row['confident']);correct.append(row['confident'] and row['modal']==actual);covered.append(row['coverage']['covered'])
        if not rows:continue
        correct=np.asarray(correct,bool);settled=np.asarray(settled,bool);binary[name]=correct
        out[name]=dict(population=n,settled=int(settled.sum()),correct=int(correct.sum()),wrong=int((settled&~correct).sum()),C=float(correct.sum()/n) if n else None,settled_share=float(settled.sum()/n) if n else None,accuracy_lower=cp_bounds(int(correct.sum()),int(settled.sum()))[0] if settled.any() else 0.,coverage=float(np.mean(covered)),failed=sum(v['excluded'] for v in rows),site_records=rows)
    tests={};margin=None;status='NOT EVALUABLE' if n<40 else 'DOES NOT BEAT'
    if 'Q' in out and all(a in out for a in ['V','F','R']):
        margin=out['Q']['C']-max(out[a]['C'] for a in ['V','F','R'])
        for a in ['V','F','R']:
            q=binary['Q'];b=binary[a];qonly=int((q&~b).sum());bonly=int((b&~q).sum());tests[a]=dict(q_only=qonly,other_only=bonly,p=mcnemar(qonly,bonly))
        if n>=40 and margin>=.10 and all(v['p']<=.01 for v in tests.values()) and out['Q']['settled']>=20 and out['Q']['accuracy_lower']>=.80 and out['Q']['coverage']>=.85:status='Q-BEATS'
    return dict(status=status,population=n,arms=out,margin=margin,McNemar=tests)

def cnn_reading(post,truth,keep,jbar,null):
    arms=[];members=[];cuts=[]
    for c in range(200):
        path=ROOT/f'runs/conf/cnn_{c:03d}.npz'
        report=json.loads(path.with_suffix('.json').read_text())
        if report['status']!='COMPLETE':
            cuts.append(c);n=0
        else:
            with np.load(path) as d:j=d['J_2LT'].copy()
            n=len(j)
        members.append(n)
        if n:
            expanded=np.zeros((n,9,8));expanded[:,:,3]=j
            arm=basic(expanded,jbar,null)
        else:
            arm=basic(np.zeros((1,9,8)),jbar,null)
            arm['confident'][:]=False;arm['observation'][:]=False
        arms.append(arm)
    if cuts:return dict(status='CUT R-gpu',cut_cases=cuts,members=members)
    s={key:np.stack([a[key] for a in arms]) for key in arms[0]}
    cal=calibration(s,truth,keep,6,lead_indices=[3])[0]
    selected=(~post['confident'][:,:8,3])&s['confident'][:,:8,3]&keep[:,None]
    eligible=(~post['confident'][:,:8,3])&keep[:,None]
    right=s['modal'][:,:8,3]==truth[:,:8,3]
    a=np.where(post['confident'][keep,:8,3],post['modal'][keep,:8,3],-1).ravel()
    b=np.where(s['confident'][keep,:8,3],s['modal'][keep,:8,3],-1).ravel()
    pe=sum(np.mean(a==v)*np.mean(b==v) for v in [-1,0,1]);po=np.mean(a==b)
    shares=[]
    for name,q in [('S',slice(0,8)),('P',slice(8,36)),('B',slice(36,37)),('Fc',slice(37,38))]:
        shares.append(dict(type=name,lead=2.,all=float(s['confident'][keep,q,3].mean()),
                           observation=float(s['observation'][keep,q,3].mean()),
                           descriptive=boot(s['confident'][keep,q,3].mean(1),sub=6)))
    return dict(status='COMPLETE',lead=2,calibration=cal,members=members,
                zero_member_cases=sum(n==0 for n in members),confidence_shares=shares,
                kappa_S=float((po-pe)/(1-pe)) if pe<1 else None,
                reliability=reliability({k:v[:,:,3:4] for k,v in s.items()},truth[:,:,3:4],keep),
                posterior_not_confident=dict(questions=int(eligible.sum()),cnn_confident=int(selected.sum()),
                    correct=int((selected&right).sum()),X=float(selected.sum()/eligible.sum()) if eligible.any() else None,
                    Y=float(right[selected].mean()) if selected.any() else None,
                    share_descriptive=boot(selected[keep].sum(1),eligible[keep].sum(1),6),
                    accuracy_descriptive=boot((selected&right)[keep].sum(1),selected[keep].sum(1),6)))

def run():
    start=time.perf_counter()
    with np.load(ROOT/'runs/null/null.npz') as n:jbar=float(n['jbar']);null=n['prob']
    post=[];crude=[];rml=[];truth=[];reports=[];mechanisms=[];divergences=[];extras=[];ranks=[];precision=[];agreement=[];forcing_ranks=[];all_calibration=[];zeros=[]
    for c in range(200):
        reports.append(json.loads((ROOT/f'runs/conf/case_{c:03d}.json').read_text()))
        with np.load(ROOT/f'runs/conf/case_{c:03d}.npz') as d:
            j=d['J'];forcing_ranks.append(float((d['theta'][:,40]<8).mean()));post.append(summary(j,jbar,null));
            with np.load(ROOT/f'runs/conf/crude_{c:03d}.npz') as cd:crude.append(basic(cd['J'],jbar,null))
            mechanisms.append(mechanism(j))
            spread=np.sqrt(np.mean(np.maximum(0,d['factual_square_sum']/len(j)-(d['state_sum'][8]/len(j))**2),axis=-1))
            divergences.append(d['divergence_sum'][:8]/len(j)/np.maximum(spread,1e-30))
            with np.load(ROOT/f'runs/conf/score_{c:03d}.npz') as scoring:actual=scoring['actual_cost']
            zeros.append(dict(case=c,action_zero=np.argwhere(actual[:8]==actual[8]).tolist(),pair_zero=[[k,l,t] for k in range(8) for l in range(k+1,8) for t in range(8) if actual[k,t]==actual[l,t]],factual_zero=np.flatnonzero(actual[8]==jbar).tolist()));truth.append(labels(actual,jbar)[0]);D=j[:,:8]-j[:,8,None];real=actual[:8]-actual[8]
            ranks.append((D<real[None]).mean(0))
            meanj=j.mean(0);chosen=int(meanj[:,3].argmin());draw_regret=j[:,:,3]-j[:,:,3].min(1)[:,None]
            extras.append(dict(case=c,unforced_quantiles=np.quantile(j[:,8],[.05,.5,.95],axis=0).tolist(),effect_mean=D.mean(0).tolist(),effect_quantiles=np.quantile(D,[.05,.5,.95],axis=0).tolist(),backfire_probability=(D>0).mean(0).tolist(),positive_expected_loss=np.maximum(D,0).mean(0).tolist(),nine_action_best=np.stack([(j.argmin(1)==a).mean(0) for a in range(9)]).tolist(),posterior_regret_2LT=draw_regret.mean(0).tolist(),chosen_nine_action=chosen,realized_regret_2LT=float(actual[chosen,3]-actual[:,3].min())))
    def stack(rows):return {key:np.stack([r[key] for r in rows]) for key in rows[0]}
    s=stack(post);sc=stack(crude);truth=np.asarray(truth);keep=np.array([not r['excluded'] for r in reports]);cal=calibration(s,truth,keep);cal_c=calibration(sc,truth,keep,4)
    covered=sum(r['coverage']['covered'] for r in reports)
    wilson_center=(covered/200+1.96**2/400)/(1+1.96**2/200);wilson_radius=1.96*np.sqrt((covered/200)*(1-covered/200)/200+1.96**2/(4*200**2))/(1+1.96**2/200)
    # Confirmation coverage below .85 is a KILL, not a development R-cov fallback.
    if (~keep).mean()>.05:resolution('R-diag','Confirmation diagnostic exclusions above5%',dict(excluded=int((~keep).sum())))
    shares=[]
    types={'S':slice(0,8),'P':slice(8,36),'B':slice(36,37),'Fc':slice(37,38)}
    for name,q in types.items():
        for t in range(8):
            row=dict(type=name,lead=float(LEADS[t]))
            for key in ['confident','observation','climate']:
                v=s[key][keep,q,t].mean(1);row[key]=dict(point=float(v.mean()) if len(v) else None,descriptive=boot(v,sub=1))
            row['per_question_confident']=s['confident'][keep,q,t].mean(0).tolist();shares.append(row)
    R2a=[]
    for t in [3,5]:
        d=s['observation'][keep,:8,t].mean(1)-s['confident'][keep,37,t];bounds=difference_interval(d)
        prerequisite=cal[t]['R0']['status']=='PASS' and cal[t]['R0_F']['status']=='PASS'
        status='PREREQUISITE NOT MET'
        if prerequisite:
            status=('INCONCLUSIVE' if bounds['empty'] else 'DIFFERS' if (bounds['point']>=.15 and bounds['lower']>0) or (bounds['point']<=-.15 and bounds['upper']<0) else 'EQUIVALENT' if bounds['lower']>=-.1 and bounds['upper']<=.1 else 'INCONCLUSIVE')
        if bounds['empty'] or bounds['offset']:resolution('R-other',f'R2a {LEADS[t]} interval conflict',bounds)
        R2a.append(dict(lead=float(LEADS[t]),status=status,prerequisite=prerequisite,**bounds))
    def ordered_loss(use_observation=False):
        values=[];counts={'earlier':0,'later':0,'same_lead':0,'both_beyond':0};eligible_actions=0;case_shares=[]
        for c in np.flatnonzero(keep):
            eligible=np.flatnonzero(s['observation'][c,:8,0]&s['confident'][c,37,0]);pairs=[];categories=[]
            for k in eligible:
                def loss(v):
                    z=np.flatnonzero(~v);return int(z[0]) if len(z) else 8
                a=loss(s['observation' if use_observation else 'confident'][c,k]);b=loss(s['confident'][c,37]);pairs.append(int(a>b)-int(a<b));eligible_actions+=1
                category='later' if a>b else 'earlier' if a<b else 'both_beyond' if a==8 else 'same_lead';counts[category]+=1;categories.append(category)
            if pairs:
                values.append(float(np.mean(pairs)));case_shares.append({k:categories.count(k)/len(categories) for k in counts})
        return values,counts,eligible_actions,{k:float(np.mean([v[k] for v in case_shares])) if case_shares else None for k in counts}
    loss,counts,actions,loss_shares=ordered_loss();b=difference_interval(loss);prereq=all(v['R0']['status'] in ['PASS','NOT EVALUABLE'] and v['R0_F']['status'] in ['PASS','NOT EVALUABLE'] for v in cal)
    R2b=dict(cases=len(loss),actions=actions,pair_counts=counts,pair_shares=loss_shares,answer_weighted_pair_shares={k:v/actions if actions else None for k,v in counts.items()},prerequisite=prereq,**b)
    R2b['status']='NOT EVALUABLE' if len(loss)<30 else 'PREREQUISITE NOT MET' if not prereq else 'NO ORDER DETECTED' if b['empty'] else 'OUTLIVES' if b['point']>=.2 and b['lower']>0 else 'PRECEDES' if b['point']<=-.2 and b['upper']<0 else 'NO DIRECTIONAL PREFERENCE' if b['lower']>=-.1 and b['upper']<=.1 else 'NO ORDER DETECTED'
    variant,vc,va,vs=ordered_loss(True);R2b['observation_loss_variant']=dict(interval=difference_interval(variant),pair_counts=vc,actions=va,case_pair_shares=vs)
    if b['empty'] or b['offset']:resolution('R-other','R2b interval conflict',b)
    fcshare=s['confident'][keep,37].mean(0);good=np.flatnonzero(fcshare>=.5);horizon=int(good[-1]) if len(good) else -1;R2c=[]
    for t in range(8):
        conf=s['confident'][keep,:8,t];right=(s['modal'][keep,:8,t]==truth[keep,:8,t]);answer=t<=horizon;selected=~conf if answer else conf
        num=selected.sum(1);correct=(right&selected).sum(1)
        R2c.append(dict(lead=float(LEADS[t]),answers=answer,exception_share=float(selected.mean()),exception_accuracy=float(correct.sum()/num.sum()) if num.sum() else None,exception_share_descriptive=boot(num,np.full(len(num),8),3),answered_not_confident_share=float(selected.mean()) if answer else 0.,refused_confident_share=float(selected.mean()) if not answer else 0.,accuracy_descriptive=boot(correct,num,3)))
    mechan={}
    for key in mechanisms[0]:
        values=np.stack([r[key] for r in mechanisms])[keep]
        mechan[key]=dict(median=np.median(values,axis=(0,1) if values.ndim==3 else 0).tolist(),quartiles=np.quantile(values,[.25,.75],axis=(0,1) if values.ndim==3 else 0).tolist())
    for key in ['rho','cancellation','z_D']:
        mechan[key]['descriptive']=median_boot(np.stack([r[key] for r in mechanisms])[keep])
    rho_med=np.array(mechan['rho']['median']);cross=np.flatnonzero(rho_med<.5);mechan['first_median_rho_below_half']=float(LEADS[cross[0]]) if len(cross) else None
    div=np.asarray(divergences)[keep];mechan['divergence_ratio']=dict(median=np.median(div,axis=(0,1)).tolist(),quartiles=np.quantile(div,[.25,.75],axis=(0,1)).tolist(),ticks=TICKS.tolist())
    zvals=np.stack([r['z_D'] for r in mechanisms])[keep];cvals=np.stack([r['cancellation'] for r in mechanisms])[keep];conf=s['confident'][keep,:8];mechan['bins']={}
    for name,values,edges in [('z_D',zvals,[0,1,1.645,2,3,np.inf]),('cancellation',cvals,[0,.1,.25,.5,1,np.inf]),('Phi_zD',norm.cdf(zvals),[.5,.6,.7,.8,.9,.95,1.000001])]:
        rows=[]
        for lo,hi in zip(edges[:-1],edges[1:]):
            m=(values>=lo)&(values<hi);rows.append(dict(lower=lo,upper=None if np.isinf(hi) else hi,count=int(m.sum()),confident_share=float(conf[m].mean()) if m.any() else None,mean_Phi_zD=float(norm.cdf(zvals)[m].mean()) if m.any() else None))
        mechan['bins'][name]=rows
    zf=[]
    for c in range(200):
        with np.load(ROOT/f'runs/conf/case_{c:03d}.npz') as d:j=d['J'][:,8];zf.append(np.abs(j.mean(0)-jbar)/j.std(0,ddof=1))
    mechan['lead_relationship']=[dict(lead=float(LEADS[t]),confident_S_share=float(s['confident'][keep,:8,t].mean()),observation_S_share=float(s['observation'][keep,:8,t].mean()),confident_Fc_share=float(s['confident'][keep,37,t].mean()),median_cancellation=mechan['cancellation']['median'][t],median_rho=mechan['rho']['median'][t],window_divergence_ratio=float(np.median(div[:,:,WINDOWS[t]].mean(-1)))) for t in range(8)]
    mechan['z_F']=dict(median=np.median(np.asarray(zf)[keep],axis=0).tolist(),quartiles=np.quantile(np.asarray(zf)[keep],[.25,.75],axis=0).tolist())
    measure=r5()
    publish=cal[3]['R0']['status']=='PASS' and (any(v['status']=='DIFFERS' for v in R2a) or R2b['status'] in ['OUTLIVES','PRECEDES'] or (measure['status']=='Q-BEATS' and cal[3]['R0']['status']=='PASS'))
    kill=covered/200<.85 or (cal[3]['R0']['status']=='FAIL' and cal[5]['R0']['status']=='FAIL')
    decision='KILL' if kill else 'PUBLISH' if publish else 'TODD DECIDES'
    resolutions=[]
    if (ROOT/'runs/resolutions.jsonl').exists():resolutions=[json.loads(l) for l in (ROOT/'runs/resolutions.jsonl').read_text().splitlines()]
    # Spec findings are recorded even when no numerical resolution fired.
    if not any(r['rule']=='R-other' and r['trigger']=='Spec gate scope findings' for r in resolutions):
        resolution('R-other','Spec gate scope findings','True-F climate advantage is literal rather than proven monotone; untested selector targeting arms cannot support L6; Wilks coverage remains approximate.')
        resolutions=[json.loads(l) for l in (ROOT/'runs/resolutions.jsonl').read_text().splitlines()]
    output=dict(null=dict(jbar=jbar,F=8.,states=4096,Fc_above_shares=null[37,:,1].tolist(),question_probabilities=null.tolist()),version='2.3',panel='confirmation',cases=200,gate=decision,dt=dt(),settings=settings(),R0=cal,R1=shares,R1m=mechan,R2a=R2a,R2b=R2b,R2c=dict(horizon=float(LEADS[horizon]) if horizon>=0 else None,readings=R2c),R3=dict(calibration=cal_c,reliability=reliability(sc,truth,keep)),R3b=dict(status='NOT RUN: RML-conf cut'),R5=measure,coverage=dict(covered=covered,total=200,share=covered/200,descriptive=boot(np.array([r['coverage']['covered'] for r in reports]),sub=7),wilson95=[wilson_center-wilson_radius,wilson_center+wilson_radius]),excluded=int((~keep).sum()),fit_flags=sum(r['minimum']>467.6 for r in reports),reliability=reliability(s,truth,keep),threshold_uncertain=s['uncertain'][keep].mean((0,1)).tolist(),split_instability=s['split_unstable'][keep].mean((0,1)).tolist(),true_F_rank=dict(histogram=np.histogram(forcing_ranks,bins=np.linspace(0,1,11))[0].tolist(),uniformity_KS=dict(statistic=float(kstest(np.asarray(forcing_ranks)[keep],'uniform').statistic),p=float(kstest(np.asarray(forcing_ranks)[keep],'uniform').pvalue)),case_values=forcing_ranks),exact_zero_answers=zeros,rank_histogram=np.histogram(np.asarray(ranks)[keep],bins=np.linspace(0,1,11))[0].tolist(),extra_selector_readings=extras,resolutions=resolutions,source_hashes={p.name:digest(p) for p in sorted(list(ROOT.glob('acd_*.py'))+[ROOT/'check_acd.py'])},seconds=time.perf_counter()-start)
    for type_name,q in types.items():
        for t in range(8):
            selection=s['confident'][keep,q,t];right=s['modal'][keep,q,t]==truth[keep,q,t]
            all_calibration.append(dict(type=type_name,lead=float(LEADS[t]),answers=int(selection.sum()),correct=int((selection&right).sum()),accuracy=float(right[selection].mean()) if selection.any() else None,descriptive=boot((selection&right).sum(1),selection.sum(1),0),threshold_uncertain=int(s['uncertain'][keep,q,t].sum()),split_unstable=int(s['split_unstable'][keep,q,t].sum())))
    output['all_confident_calibration']=all_calibration
    output['reliability_by_type_lead']=[dict(type=type_name,lead=float(LEADS[t]),bins=reliability({key:val[:,q,t:t+1] for key,val in s.items()},truth[:,q,t:t+1],keep)) for type_name,q in types.items() for t in range(8)]
    for name,arm in [('crude',sc)]:
        # Cohen kappa for modal classifications plus abstention, per lead.
        kappas=[]
        for t in range(8):
            a=np.where(s['confident'][keep,:8,t],s['modal'][keep,:8,t],-1).ravel();b=np.where(arm['confident'][keep,:8,t],arm['modal'][keep,:8,t],-1).ravel();pe=sum(np.mean(a==v)*np.mean(b==v) for v in [-1,0,1]);po=np.mean(a==b);kappas.append(float((po-pe)/(1-pe)) if pe<1 else None)
        target=output['R3' if name=='crude' else 'R3b'];target['kappa_S']=kappas;target['kappa_by_type_lead']=[]
        for type_name,q in types.items():
            for t in range(8):
                a=np.where(s['confident'][keep,q,t],s['modal'][keep,q,t],-1).ravel();b=np.where(arm['confident'][keep,q,t],arm['modal'][keep,q,t],-1).ravel();pe=sum(np.mean(a==v)*np.mean(b==v) for v in range(-1,8));po=np.mean(a==b)
                target['kappa_by_type_lead'].append(dict(type=type_name,lead=float(LEADS[t]),kappa=float((po-pe)/(1-pe)) if pe<1 else None,agreement=float(po)))
        target['reliability_by_lead']=[reliability({key:val[:,:,t:t+1] for key,val in arm.items()},truth[:,:,t:t+1],keep) for t in range(8)]
        target['confidence_shares']=[dict(type=type_name,lead=float(LEADS[t]),all=float(arm['confident'][keep,q,t].mean()),observation=float(arm['observation'][keep,q,t].mean()),descriptive=boot(arm['confident'][keep,q,t].mean(1),sub=4 if name=='crude' else 5)) for type_name,q in types.items() for t in range(8)]
    output['R6']=cnn_reading(s,truth,keep,jbar,null)
    # Retain only the licensed P/B leads under the pre-confirmation compute cut.
    allowed=lambda r:r['type'] not in ['P','B'] or r['lead'] in [2.,3.]
    for key in ['R1','all_confident_calibration','reliability_by_type_lead']:
        output[key]=[r for r in output[key] if allowed(r)]
    for key in ['confidence_shares','kappa_by_type_lead']:
        output['R3'][key]=[r for r in output['R3'][key] if allowed(r)]
    save_json(ROOT/'runs/audit/acd_stage2.json',output)
    from acd_stage2_render import render
    render(output)
    print('Stage2',decision,flush=True)
    return output

if __name__=='__main__':run()
