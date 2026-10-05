"""Script-generated development readings; truth scoring is authorized here."""
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
def calibration(s,truth,keep):
    results=[]
    for t in range(8):
        obs=s['observation'][:,:,t][:,:8];right=s['modal'][:,:,t][:,:8]==truth[:,:,t][:,:8]
        n=obs.sum(1);correct=(obs&right).sum(1);primary=r0(n[keep],correct[keep]);sensitivity=r0(n,correct)
        order={'PASS':0,'INSUFFICIENT':1,'FAIL':2}
        status=primary['status']
        if status!='NOT EVALUABLE' and sensitivity['status']!='NOT EVALUABLE':status=max([status,sensitivity['status']],key=lambda v:order[v])
        primary.update(status=status,included_excluded=sensitivity,answer_descriptive=boot(correct[keep],n[keep],0))
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
    pop=json.loads((ROOT/'runs/dev/measure_population.json').read_text())['population'];n=len(pop);out={};binary={}
    for arm,name in enumerate(ARMS):
        rows=[];correct=[];settled=[];covered=[]
        for entry in pop:
            c,k,l=entry['case'],entry['k'],entry['l'];p=ROOT/f'runs/dev/measure/refit_{c:03d}_3_{arm}.json'
            if not p.exists():continue
            row=json.loads(p.read_text());rows.append(row)
            with np.load(ROOT/f'runs/dev/score_{c:03d}.npz') as data:j=data['actual_cost']
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

def run():
    start=time.perf_counter()
    with np.load(ROOT/'runs/null/null.npz') as n:jbar=float(n['jbar']);null=n['prob']
    post=[];crude=[];rml=[];truth=[];reports=[];mechanisms=[];divergences=[];extras=[];ranks=[];precision=[];agreement=[]
    for c in range(200):
        reports.append(json.loads((ROOT/f'runs/dev/case_{c:03d}.json').read_text()))
        with np.load(ROOT/f'runs/dev/case_{c:03d}.npz') as d:
            j=d['J'];post.append(summary(j,jbar,null));crude.append(basic(d['crude_J'],jbar,null));rml.append(basic(d['rml_J'],jbar,null));mechanisms.append(mechanism(j))
            spread=np.sqrt(np.mean(np.maximum(0,d['factual_square_sum']/len(j)-(d['state_sum'][8]/len(j))**2),axis=-1))
            divergences.append(d['divergence_sum'][:8]/len(j)/np.maximum(spread,1e-30))
            pp,ps=signed_se(j,jbar);rr,rs=signed_se(d['rml_J'],jbar,chains=0)
            agreement.append(dict(mean_probability_difference=np.abs(pp-rr).mean(0).tolist(),substantive=(np.abs(pp-rr)>3*np.sqrt(ps*ps+rs*rs)).mean(0).tolist(),threshold_crossing=((pp>=.95)!=(rr>=.95)).mean(0).tolist(),threshold_crossing_mc_expected=(norm.cdf(-np.abs(pp-.95)/rs)).mean(0).tolist()))
            with np.load(ROOT/f'runs/dev/score_{c:03d}.npz') as scoring:actual=scoring['actual_cost']
            truth.append(labels(actual,jbar)[0]);D=j[:,:8]-j[:,8,None];real=actual[:8]-actual[8]
            ranks.append((D<real[None]).mean(0))
            meanj=j.mean(0);chosen=int(meanj[:,3].argmin());draw_regret=j[:,:,3]-j[:,:,3].min(1)[:,None]
            extras.append(dict(case=c,unforced_quantiles=np.quantile(j[:,8],[.05,.5,.95],axis=0).tolist(),effect_mean=D.mean(0).tolist(),effect_quantiles=np.quantile(D,[.05,.5,.95],axis=0).tolist(),backfire_probability=(D>0).mean(0).tolist(),positive_expected_loss=np.maximum(D,0).mean(0).tolist(),nine_action_best=np.stack([(j.argmin(1)==a).mean(0) for a in range(9)]).tolist(),posterior_regret_2LT=draw_regret.mean(0).tolist(),chosen_nine_action=chosen,realized_regret_2LT=float(actual[chosen,3]-actual[:,3].min())))
    def stack(rows):return {key:np.stack([r[key] for r in rows]) for key in rows[0]}
    s=stack(post);sc=stack(crude);sr=stack(rml);truth=np.asarray(truth);keep=np.array([not r['excluded'] for r in reports]);cal=calibration(s,truth,keep);cal_c=calibration(sc,truth,keep);cal_r=calibration(sr,truth,keep)
    covered=sum(r['coverage']['covered'] for r in reports)
    if covered/200<.85:resolution('R-cov','Development coverage below0.85',dict(covered=covered,cases=200))
    if (~keep).mean()>.05:resolution('R-diag','Development diagnostic exclusions above5%',dict(excluded=int((~keep).sum())))
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
        values=[];counts={'earlier':0,'later':0,'same_lead':0,'both_beyond':0};eligible_actions=0
        for c in np.flatnonzero(keep):
            eligible=np.flatnonzero(s['observation'][c,:8,0]&s['confident'][c,37,0]);pairs=[]
            for k in eligible:
                def loss(v):
                    z=np.flatnonzero(~v);return int(z[0]) if len(z) else 8
                a=loss(s['observation' if use_observation else 'confident'][c,k]);b=loss(s['confident'][c,37]);pairs.append(int(a>b)-int(a<b));eligible_actions+=1
                counts['later' if a>b else 'earlier' if a<b else 'both_beyond' if a==8 else 'same_lead']+=1
            if pairs:values.append(float(np.mean(pairs)))
        return values,counts,eligible_actions
    loss,counts,actions=ordered_loss();b=difference_interval(loss);prereq=all(v['R0']['status'] in ['PASS','NOT EVALUABLE'] and v['R0_F']['status'] in ['PASS','NOT EVALUABLE'] for v in cal)
    R2b=dict(cases=len(loss),actions=actions,pair_counts=counts,pair_shares={k:v/actions if actions else None for k,v in counts.items()},prerequisite=prereq,**b)
    R2b['status']='NOT EVALUABLE' if len(loss)<30 else 'PREREQUISITE NOT MET' if not prereq else 'NO ORDER DETECTED' if b['empty'] else 'OUTLIVES' if b['point']>=.2 and b['lower']>0 else 'PRECEDES' if b['point']<=-.2 and b['upper']<0 else 'NO DIRECTIONAL PREFERENCE' if b['lower']>=-.1 and b['upper']<=.1 else 'NO ORDER DETECTED'
    variant,vc,va=ordered_loss(True);R2b['observation_loss_variant']=dict(interval=difference_interval(variant),pair_counts=vc,actions=va)
    if b['empty'] or b['offset']:resolution('R-other','R2b interval conflict',b)
    fcshare=s['confident'][keep,37].mean(0);good=np.flatnonzero(fcshare>=.5);horizon=int(good[-1]) if len(good) else -1;R2c=[]
    for t in range(8):
        conf=s['confident'][keep,:8,t];right=(s['modal'][keep,:8,t]==truth[keep,:8,t]);answer=t<=horizon;selected=~conf if answer else conf
        num=selected.sum(1);correct=(right&selected).sum(1)
        R2c.append(dict(lead=float(LEADS[t]),answers=answer,exception_share=float(selected.mean()),exception_accuracy=float(correct.sum()/num.sum()) if num.sum() else None,accuracy_descriptive=boot(correct,num,3)))
    mechan={}
    for key in mechanisms[0]:
        values=np.stack([r[key] for r in mechanisms])[keep]
        mechan[key]=dict(median=np.median(values,axis=(0,1) if values.ndim==3 else 0).tolist(),quartiles=np.quantile(values,[.25,.75],axis=(1,2) if False else (0,1) if values.ndim==3 else 0).tolist())
    rho_med=np.array(mechan['rho']['median']);cross=np.flatnonzero(rho_med<.5);mechan['first_median_rho_below_half']=float(LEADS[cross[0]]) if len(cross) else None
    div=np.asarray(divergences)[keep];mechan['divergence_ratio']=dict(median=np.median(div,axis=(0,1)).tolist(),quartiles=np.quantile(div,[.25,.75],axis=(0,1)).tolist(),ticks=TICKS.tolist())
    zvals=np.stack([r['z_D'] for r in mechanisms])[keep];cvals=np.stack([r['cancellation'] for r in mechanisms])[keep];conf=s['confident'][keep,:8];mechan['bins']={}
    for name,values,edges in [('z_D',zvals,[0,1,1.645,2,3,np.inf]),('cancellation',cvals,[0,.1,.25,.5,1,np.inf]),('Phi_zD',norm.cdf(zvals),[.5,.6,.7,.8,.9,.95,1.000001])]:
        rows=[]
        for lo,hi in zip(edges[:-1],edges[1:]):
            m=(values>=lo)&(values<hi);rows.append(dict(lower=lo,upper=None if np.isinf(hi) else hi,count=int(m.sum()),confident_share=float(conf[m].mean()) if m.any() else None,mean_Phi_zD=float(norm.cdf(zvals)[m].mean()) if m.any() else None))
        mechan['bins'][name]=rows
    mechan['z_F']=np.median(np.stack([np.abs(np.asarray(e['unforced_quantiles'])[1]-jbar) for e in extras]),axis=0).tolist() # replaced below with exact mean/std
    zf=[]
    for c in range(200):
        with np.load(ROOT/f'runs/dev/case_{c:03d}.npz') as d:j=d['J'][:,8];zf.append(np.abs(j.mean(0)-jbar)/j.std(0,ddof=1))
    mechan['z_F']=dict(median=np.median(np.asarray(zf)[keep],axis=0).tolist(),quartiles=np.quantile(np.asarray(zf)[keep],[.25,.75],axis=0).tolist())
    measure=r5();strong=False
    if cal[3]['R0']['status']=='PASS':
        strong=any(v['status']=='DIFFERS' and abs(v['point'])>=.25 for v in R2a) or (R2b['status'] in ['OUTLIVES','PRECEDES'] and abs(R2b['point'])>=.30) or (measure['status']=='Q-BEATS' and measure['margin']>=.15)
    decision='STRONG' if strong else 'STOP AND REPORT' if cal[3]['R0']['status']=='FAIL' and cal[5]['R0']['status']=='FAIL' else 'TODD DECIDES'
    resolutions=[]
    if (ROOT/'runs/resolutions.jsonl').exists():resolutions=[json.loads(l) for l in (ROOT/'runs/resolutions.jsonl').read_text().splitlines()]
    # Spec findings are recorded even when no numerical resolution fired.
    if not any(r['rule']=='R-other' and r['trigger']=='Spec gate scope findings' for r in resolutions):
        resolution('R-other','Spec gate scope findings','True-F climate advantage is literal rather than proven monotone; untested selector targeting arms cannot support L6; Wilks coverage remains approximate.')
        resolutions=[json.loads(l) for l in (ROOT/'runs/resolutions.jsonl').read_text().splitlines()]
    output=dict(version='2.3',panel='development',cases=200,gate=decision,dt=dt(),settings=settings(),R0=cal,R1=shares,R1m=mechan,R2a=R2a,R2b=R2b,R2c=dict(horizon=float(LEADS[horizon]) if horizon>=0 else None,readings=R2c),R3=dict(calibration=cal_c,reliability=reliability(sc,truth,keep)),R3b=dict(calibration=cal_r,reliability=reliability(sr,truth,keep),posterior_agreement=agreement),R5=measure,coverage=dict(covered=covered,total=200,share=covered/200,descriptive=boot(np.array([r['coverage']['covered'] for r in reports]),sub=7)),excluded=int((~keep).sum()),fit_flags=sum(r['minimum']>467.6 for r in reports),reliability=reliability(s,truth,keep),threshold_uncertain=s['uncertain'][keep].mean((0,1)).tolist(),split_instability=s['split_unstable'][keep].mean((0,1)).tolist(),rank_histogram=np.histogram(np.asarray(ranks)[keep],bins=np.linspace(0,1,11))[0].tolist(),extra_selector_readings=extras,resolutions=resolutions,seconds=time.perf_counter()-start)
    for name,arm in [('crude',sc),('RML',sr)]:
        # Cohen kappa for modal classifications plus abstention, per lead.
        kappas=[]
        for t in range(8):
            a=np.where(s['confident'][keep,:8,t],s['modal'][keep,:8,t],-1).ravel();b=np.where(arm['confident'][keep,:8,t],arm['modal'][keep,:8,t],-1).ravel();pe=sum(np.mean(a==v)*np.mean(b==v) for v in [-1,0,1]);po=np.mean(a==b);kappas.append(float((po-pe)/(1-pe)) if pe<1 else None)
        output['R3' if name=='crude' else 'R3b']['kappa']=kappas
    save_json(ROOT/'runs/audit/acd_stage1.json',output)
    lines=['# Aspen counterfactual determinacy — Stage 1 (v2.3)','',f'**Stage 1 gate: {decision}.** Development only; Todd decides whether to authorize a freeze and confirmation.','',f'Completed 200 cases on sulaco CPU at dt={dt()}; truth coverage {covered}/200; diagnostic exclusions {int((~keep).sum())}/200.','', '| Lead (LT) | R0 | Case accuracy [L,U] | Answers / cases | R0-F |','|---|---|---|---|---|']
    for row in cal:
        r=row['R0'];point='NA' if r['case_accuracy'] is None else f"{r['case_accuracy']:.3f}";lines.append(f"| {row['lead']:g} | {r['status']} | {point} [{r['case_lower']:.3f}, {r['case_upper']:.3f}] | {r['answers']} / {r['cases']} | {row['R0_F']['status']} |")
    lines+=['','R0 includes the required sensitivity with excluded cases included; the worse status governs. Bounds are v2.3 betting bounds; R0-F uses exact Clopper–Pearson.','']
    for row in R2a:lines.append(f"R2a at {row['lead']:g} LT: {row['status']}; Δ={row['point']:.3f}, 99% interval [{row['lower']:.3f}, {row['upper']:.3f}].")
    point='NA' if R2b['point'] is None else f"{R2b['point']:.3f}";lines+=['',f"R2b: {R2b['status']}; Δ_loss={point}, 99% interval [{R2b['lower']:.3f}, {R2b['upper']:.3f}], {R2b['cases']} eligible cases.",'',f"R5 at 2 LT: {measure['status']}; common population {measure['population']}; margin {measure['margin']}. Only Q, F, V and R support the tested comparison.",'','| Arm | Confident correct / population | Confident wrong | Accuracy lower bound | Truth coverage |','|---|---|---|---|---|']
    for name,r in measure['arms'].items():lines.append(f"| {name} | {r['correct']} / {r['population']} | {r['wrong']} | {r['accuracy_lower']:.3f} | {r['coverage']:.3f} |")
    lines+=['','Resolution rules fired: '+', '.join(sorted(set(r['rule'] for r in resolutions)))+'.','']
    for rule in sorted(set(r['rule'] for r in resolutions)):
        triggered=[r['trigger'] for r in resolutions if r['rule']==rule];lines.append(f"- **{rule}**: "+'; '.join(dict.fromkeys(triggered))+'.')
    lines+=['','All share/mechanism/comparator bootstrap intervals are approximate and descriptive. Extra selector readings (unforced distribution, effect magnitudes/backfire, nine-action best and regret) are reported only. The full receipt includes R1/R1m maps, reliability, rank histogram, threshold uncertainty, split stability, RML cross-checks and R5 site/refit records: `runs/audit/acd_stage1.json`.','','This is development analysis; it licenses no confirmation claim. Work stops here. No freeze, confirmation reading or CNN inference was performed.']
    rendered='\n'.join(lines)+'\n';(ROOT/'ACD_STAGE1_READING.md').write_text(rendered)
    note=ROOT/'vault/04-Results/R_Aspen-Counterfactual-Determinacy-Stage1-2026-10.md';note.parent.mkdir(parents=True,exist_ok=True);note.write_text(rendered+'\nRelated: [[WO_Aspen-Counterfactual-Determinacy-2026-10-04]], [[L_Aspen-Counterfactual-Determinacy-Claim-Ledger-2026-10]].\n')
    print('Stage1 gate',decision,flush=True)
if __name__=='__main__':run()
