"""WO v5.2 case-level metrics and frozen paired-case inference.

Pure functions only: importing this module never opens campaign outputs.
"""
import numpy as np


def finite(value):
    return value is not None and bool(np.isfinite(value))


def average(values):
    values=[v for v in values if finite(v)]
    return float(np.mean(values)) if values else None


def ratio(num, den):
    return float(num/den) if finite(num) and finite(den) and den != 0 else None


def response_ratio(rows, prefix):
    usable=[r for r in rows if finite(r.get(prefix+'_num')) and finite(r.get(prefix+'_den'))]
    den=sum(r[prefix+'_den'] for r in usable)
    return float(np.sqrt(sum(r[prefix+'_num'] for r in usable)/den)) if den>0 else None


def quantile(values, q):
    values=np.asarray(values,dtype=float)
    return float(np.quantile(values,q,method='linear')) if values.size and np.isfinite(values).all() else None


def paired_gap(entries, first, second, samples, eligible=True):
    mask=np.array([e['eligible'] if eligible else True for e in entries])
    differences=np.array([int(e['arms'][first]['correct'])-int(e['arms'][second]['correct']) for e in entries])
    counts=mask[samples].sum(1)
    if not mask.any() or not np.all(counts):return None
    return (differences[samples]*mask[samples]).sum(1)/counts


def bounds(values, level=.95):
    if values is None:return dict(lower=None,upper=None,level=level)
    return dict(lower=quantile(values,1-level),upper=quantile(values,level),level=level)


def spearman(x,y):
    # Average ranks preserve ties, without scipy as a runtime dependency.
    def ranks(a):
        a=np.asarray(a);order=np.argsort(a,kind='stable');out=np.empty(len(a),float)
        start=0
        while start<len(a):
            end=start+1
            while end<len(a) and a[order[end]]==a[order[start]]:end+=1
            out[order[start:end]]=(start+end-1)/2
            start=end
        return out
    a=ranks(x);b=ranks(y);a-=a.mean();b-=b.mean()
    return ratio(float(a@b),float(np.sqrt((a@a)*(b@b))))


def state_statistics(mean,var,truth_mean,truth_var,actual,climate,window,b,sigma,point_tick,failed=False):
    """Capture additive response statistics before converting states into cost."""
    mean=np.asarray(mean);var=np.asarray(var);truth_mean=np.asarray(truth_mean);truth_var=np.asarray(truth_var)
    other=np.arange(8)!=b
    response=mean[other][:,window]-mean[b,window]
    target=truth_mean[other][:,window]-truth_mean[b,window]
    vresponse=var[other][:,window]-var[b,window]
    vtarget=truth_var[other][:,window]-truth_var[b,window]
    def acc(ticks):
        f=mean[:,ticks]-climate[:,None,:];o=actual[:,ticks]-climate[:,None,:]
        f2=np.sum(f*f,axis=-1);o2=np.sum(o*o,axis=-1)
        result=np.zeros(f2.shape)
        result[o2<=0]=np.nan
        keep=(o2>0)&(f2>0)&(f2>=1e-24*o2)
        result[keep]=np.sum(f*o,axis=-1)[keep]/np.sqrt(f2[keep]*o2[keep])
        return float(result.mean()) if np.isfinite(result).all() else None
    parts={}
    for label,m,v in [('arm',mean,var),('truth',truth_mean,truth_var)]:
        mean_energy=np.sum(m[:,window]**2,axis=-1).mean(-1)/(2*m.shape[-1])
        spread_energy=v[:,window].mean(-1)/(2*m.shape[-1])
        parts[label+'_mean_difference']=(mean_energy-mean_energy[b]).tolist()
        parts[label+'_spread_difference']=(spread_energy-spread_energy[b]).tolist()
    return dict(wACC=0. if failed else acc(window),pointACC=0. if failed else acc([point_tick]),
        wRMSE=None if failed else float(np.sqrt(np.mean((mean[:,window]-actual[:,window])**2,axis=-1)).mean()/sigma),
        MSRE_num=None if failed else float(np.sum((response-target)**2)),MSRE_den=None if failed else float(np.sum(target**2)),
        VRE_num=None if failed else float(np.sum((vresponse-vtarget)**2)),VRE_den=None if failed else float(np.sum(vtarget**2)),
        cost_difference_split=None if failed else parts)


def aggregate(entries,name):
    """Eligible and all-case versions with explicit exclusion counts; recompute S_J."""
    truth=np.asarray([e['arms'][name]['J'] for e in entries]);scale=float(np.median(np.ptp(truth,axis=1)))
    result={'S_J':scale,'failed_cases':sum(e['arms'][name]['failed'] for e in entries),
            'dropped_members':sum(e['arms'][name]['dropped'] for e in entries),
            'attempted_members':len(entries)*64}
    result['reliable']=result['failed_cases']<=.01*len(entries) and result['dropped_members']<=.01*len(entries)*64
    for subset,selected in [('eligible',[e for e in entries if e['eligible']]),('all',entries)]:
        rows=[e['arms'][name] for e in selected];valid=[r for r in rows if not r['failed']]
        values=dict(cases=len(rows),P=average([int(r['correct']) for r in rows]),
                    wACC=average([r.get('wACC') for r in rows]),pointACC=average([r.get('pointACC') for r in rows]),
                    wRMSE=average([r.get('wRMSE') for r in valid]),
                    MSRE=response_ratio(valid,'MSRE'),VRE=response_ratio(valid,'VRE'),
                    excluded_cases=len(rows)-len(valid))
        raw=[r['regret_raw'] for r in rows]
        values.update(regret_raw=average(raw),regret=ratio(average(raw),scale))
        values['realized_regret_raw']=average([r.get('realized_regret_raw') for r in rows])
        values['realized_regret']=average([r.get('realized_regret') for r in rows])
        values['cost_forecast_error']=ratio(average([float(np.mean(np.abs(np.asarray(r['cost'])-r['J']))) for r in valid]),scale)
        values['spearman']=average([spearman(r['cost'],r['J']) for r in valid])
        # Winner/runner-up uses selection-half b, with full-mean cheapest remaining action.
        margins=[];pair_num=pair_den=pair_dot=pred_norm=pair_target_sum=pair_pred_sum=0.;pair_count=0
        for e in selected:
            r=e['arms'][name]
            if r['failed']:continue
            j=np.asarray(r['J']);p=np.asarray(r['cost']);b=e['b'];others=np.flatnonzero(np.arange(8)!=b)
            runner=others[np.argmin(j[others])]
            margins.append(int(np.sign(p[runner]-p[b])==np.sign(j[runner]-j[b])))
            ix,iy=np.triu_indices(8,1);target=j[iy]-j[ix];pred=p[iy]-p[ix]
            pair_num+=np.sum((pred-target)**2);pair_den+=target@target;pair_dot+=pred@target;pred_norm+=pred@pred
            pair_target_sum+=target.sum();pair_pred_sum+=pred.sum();pair_count+=len(target)
        values.update(margin_sign_accuracy=average(margins),cost_difference_RE=float(np.sqrt(pair_num/pair_den)) if pair_den>0 else None,
                      cost_difference_correlation=ratio(pair_dot-pair_target_sum*pair_pred_sum/pair_count,float(np.sqrt(max(0.,pair_den-pair_target_sum**2/pair_count)*max(0.,pred_norm-pair_pred_sum**2/pair_count)))) if pair_count else None)
        choices=[];savings=[];fractions=[];optimum=[]
        for r in rows:
            j=np.asarray(r['J']);chosen=float(j.max()) if r['failed'] else float(j[r['chosen']]);j0=r['J0']
            savings.append(j0-chosen);fractions.append(ratio(100*(j0-chosen),j0));optimum.append(j0-j.min())
            choices.append(r['chosen'])
        den=sum(optimum)
        values.update(B=float(sum(savings)/den) if den>0 else None,energy_saved=average(savings),energy_saved_percent=average(fractions),
                      action_frequency=[choices.count(k)/len(rows) if rows else None for k in range(8)],failed_choice_frequency=choices.count(-1)/len(rows) if rows else None)
        splits=[r.get('cost_difference_split') for r in valid if r.get('cost_difference_split') is not None]
        if splits:
            mean_error=np.array([np.asarray(v['arm_mean_difference'])-v['truth_mean_difference'] for v in splits])
            spread_error=np.array([np.asarray(v['arm_spread_difference'])-v['truth_spread_difference'] for v in splits])
            values['cost_difference_split']=dict(mean_part_mean_error=float(mean_error.mean()),spread_part_mean_error=float(spread_error.mean()),mean_part_MSE=float(np.mean(mean_error**2)),spread_part_MSE=float(np.mean(spread_error**2)),cross_MSE=float(2*np.mean(mean_error*spread_error)),total_MSE=float(np.mean((mean_error+spread_error)**2)),cases=len(splits))
        else:values['cost_difference_split']=None
        result[subset]=values
    return result


def read_gates(entries,S,Rep,samples,selected=None,two_scale=False):
    """Frozen §§7.1–7.7 verdicts. Does not select L* from test outcomes."""
    physics='N2' if two_scale else 'N-last';base='CNN2-20k' if two_scale else 'CNN-20k';cost='CNN2-cost' if two_scale else 'CNN-cost'
    names=list(entries[0]['arms']);metrics={n:aggregate(entries,n) for n in names}
    n=len(entries);eligible=sum(e['eligible'] for e in entries);p={a:metrics[a]['eligible']['P'] for a in names}
    myopic=average([int(e['myopic_correct']) for e in entries if e['eligible']]);fixed=average([int(e['fixed_correct']) for e in entries if e['eligible']])
    null_gap=p[physics]-max(myopic,fixed) if all(finite(v) for v in [p[physics],myopic,fixed]) else None
    suff=eligible>=.8*n and (finite(fixed) and fixed<=.85 if two_scale else finite(null_gap) and null_gap>=.05)
    out=dict(metrics=metrics,eligible=eligible,total=n,sufficiency=suff,physics_floor=finite(null_gap) and null_gap>=.05,null_gap=null_gap,
             H1a=None,H1b=None,H1d=None,H1e=None,H1c=None,H2=None,H3=None,licensed_sentences=[])
    if not suff:return out
    def gap(a,b,level=.95):
        point=p[a]-p[b] if finite(p[a]) and finite(p[b]) else None
        return dict(point=point,**bounds(paired_gap(entries,a,b,samples),level))
    def ge(a,b):return finite(a) and finite(b) and a>=b
    def le(a,b):return finite(a) and finite(b) and a<=b
    comparable=[a for a in S if ge(metrics[a]['eligible']['wACC'],metrics[physics]['eligible']['wACC']-.01)] if finite(metrics[physics]['eligible']['wACC']) else []
    witnesses=[];kill_bounds={a:gap(physics,a,1-.05/len(comparable)) for a in comparable}
    witness_bounds={a:gap(physics,a,1-.05/len(S)) for a in S}
    for a in comparable:
        m=metrics[a];g=witness_bounds[a]
        if m['reliable'] and ge(m['eligible']['wACC'],metrics[physics]['eligible']['wACC']) and le(m['eligible']['wRMSE'],metrics[physics]['eligible']['wRMSE']) and ge(g['point'],.15) and ge(g['lower'],.10):witnesses.append(a)
    out.update(comparable=comparable,witnesses=witnesses,H1a_bounds=witness_bounds,H1a_kill_bounds=kill_bounds,
               H1a='KILL' if comparable and all(le(g['upper'],.05) for g in kill_bounds.values()) else 'PASS' if witnesses else 'otherwise')
    if selected is not None:
        g=gap(physics,selected);out['H1b_bounds']=g
        out['H1b']='KILL' if le(g['upper'],.05) else 'PASS' if ge(g['point'],.10) and ge(g['lower'],.05) and metrics[selected]['reliable'] else 'otherwise'
    repairs={}
    for a in Rep:
        g=gap(physics,a,1-.05/len(Rep));narrow=gap(a,base,1-.05/len(Rep))
        reading='unstable' if not metrics[a]['reliable'] else 'RETAINS' if finite(g['lower']) and g['lower']>.05 else 'CLOSES' if le(g['upper'],.05) else 'UNRESOLVED'
        repairs[a]=dict(reading=reading,bounds=g,NARROWS=metrics[a]['reliable'] and ge(narrow['point'],.05) and finite(narrow['lower']) and narrow['lower']>0,narrow_bounds=narrow)
    out['repairs']=repairs;out['H1d']='HOLDS' if any(r['reading']!='unstable' for r in repairs.values()) and all(r['reading'] in ['RETAINS','unstable'] for r in repairs.values()) else 'FAILS'
    if cost in names:
        g=gap(physics,cost);out['H1e_bounds']=g
        out['H1e']='UNRESOLVED' if not metrics[cost]['reliable'] else 'RETAINS' if finite(g['lower']) and g['lower']>.05 else 'CLOSES' if le(g['upper'],.05) else 'UNRESOLVED'
    # REG recomputes all-case normalization within each bootstrap panel.
    regs={}
    for a in names:
        raw=np.array([e['arms'][a]['regret_raw']-e['arms'][physics]['regret_raw'] for e in entries])
        ranges=np.array([np.ptp(e['arms'][a]['J']) for e in entries]);scales=np.median(ranges[samples],axis=1)
        dist=raw[samples].mean(1)/scales if np.all(scales>0) else None
        levels={'95':.95,'witness':1-.05/max(1,len(S)),'S6':1-.05/(len(S)+2)}
        regs[a]={k:dict(**bounds(dist,v),holds=finite(quantile(dist,1-v) if dist is not None else None) and quantile(dist,1-v)>0 and finite(metrics[a]['all']['regret']) and metrics[a]['all']['regret']>metrics[physics]['all']['regret']) for k,v in levels.items()}
    out['REG']=regs
    if not two_scale and 'CNN-resp' in names and 'CNN-roll' in names:
        resp='CNN-resp';roll='CNN-roll';g=gap(physics,resp);d=gap(resp,roll);reliable=metrics[resp]['reliable'] and metrics[roll]['reliable']
        out['H1c_bounds']=g;out['H1c']='CLOSES' if reliable and le(g['upper'],.05) else 'OPEN' if reliable and ge(g['point'],.10) and finite(g['lower']) and g['lower']>0 else 'Inconclusive'
        matched=all(finite(metrics[resp]['eligible'][k]) and finite(metrics[roll]['eligible'][k]) and abs(metrics[resp]['eligible'][k]-metrics[roll]['eligible'][k])<=.02 for k in ['wACC','wRMSE'])
        evaluable=ge(gap(physics,roll)['point'],.15)
        out['H2_bounds']=d;out['H2']='REPAIR WORKS' if evaluable and reliable and matched and ge(d['point'],.10) and finite(d['lower']) and d['lower']>0 else 'REPAIR FAILS' if evaluable and reliable and matched and le(d['upper'],.05) else 'Inconclusive'
        out['H2_both_response_improved']=all(le(metrics[resp]['eligible'][k],.7*metrics[roll]['eligible'][k]) if finite(metrics[roll]['eligible'][k]) else False for k in ['MSRE','VRE'])
    h3arms=['CNN-80k','CNN-roll',base]
    if not two_scale and all(a in metrics for a in h3arms):
        errors=[(metrics[a]['eligible'][k],metrics[base]['eligible'][k]) for a in h3arms[:2] for k in ['MSRE','VRE']]
        if any(finite(x) and finite(y) and x<.8*y for x,y in errors):out['H3']='Not supported'
        elif all(finite(x) and finite(y) and x>=.8*y for x,y in errors) and finite(metrics[base]['eligible']['wACC']) and all(ge(metrics[a]['eligible']['wACC'],metrics[base]['eligible']['wACC']-.005) for a in h3arms[:2]):out['H3']='Supported'
        else:out['H3']='Inconclusive'
    elif not two_scale:out['H3']='Unavailable'
    if two_scale and 'N2-offline' in names:
        g=gap(physics,'N2-offline');out['S12_bounds']=g;out['S12']=ge(g['point'],.05) and finite(g['lower']) and g['lower']>0
    return out


def license_ids(gate,stage='2',selected=None,twoscale_gate=None,repeats_ran=False):
    """Exact sentence identifiers; prose must interpolate only checked metrics.

    Stage-1 reading never licenses prose, even when the witness passes.
    """
    if str(stage)=='1':return []
    two=str(stage)=='2b';ids=[]
    if two:
        if gate['sufficiency'] and gate['physics_floor'] and gate['H1a']=='PASS':
            ids.append('S8')
            if gate['H1b']=='PASS':
                ids.append('S8+')
                if gate['H1d']!='HOLDS':ids.append('S7₂')
            if gate['H1e'] is not None:ids.append('S11')
        else:ids.append('S9')
        if gate.get('S12'):ids.append('S12')
        return ids
    if not gate['sufficiency'] or gate['H1a']=='KILL':return []
    if gate['H1a']=='PASS':
        ids.append('S1')
        if repeats_ran:ids.append('S1s')
        # Witness selection uses highest test wACC, then frozen order.
        from protocol import ORDER
        witnesses=gate.get('witnesses',[])
        if witnesses:
            witness=min(witnesses,key=lambda a:(-gate['metrics'][a]['eligible']['wACC'],ORDER.index(a) if a in ORDER else len(ORDER)))
            if gate['REG'][witness]['witness']['holds']:ids.append('S1+')
    if gate['H1b']=='PASS':
        ids.append('S2')
        if selected and gate['REG'][selected]['95']['holds']:ids.append('S2+')
        if gate['H1d']!='HOLDS':ids.append('S7')
    if repeats_ran and ('S1' in ids or 'S2' in ids) and 'S1s' not in ids:ids.append('S1s')
    if gate['H1d']=='HOLDS':ids.append('S3')
    if gate['H1c']=='CLOSES':ids.append('S4' if gate['H2']=='REPAIR WORKS' else 'S4b')
    elif gate['H1c']=='OPEN':ids.append('S5')
    if gate['H1e']=='RETAINS':
        ids.append('S10')
        if gate['REG']['CNN-cost']['95']['holds']:ids.append('S10+')
    elif gate['H1e']=='CLOSES':ids.append('S10b')
    elif gate['H1e']=='UNRESOLVED':ids.append('S10c')
    if all(s in ids for s in ['S2+','S3','S5','S10']):
        learned=[a for a in gate['REG'] if a.startswith('CNN') and a not in ['CNN-20k-s2','CNN-20k-s3'] and gate['metrics'][a]['reliable']]
        if learned and all(gate['REG'][a]['S6']['holds'] for a in learned):ids.append('S6')
    if twoscale_gate is not None:
        tids=license_ids(twoscale_gate,'2b')
        if ('S1' in ids or 'S2' in ids) and 'S8' not in tids:ids.append('S9')
    return ids


def enrich_state_entry(entry,name,cpu,network,window,point_tick,sigma):
    """Coordinator passes arrays; training workers never open test files here."""
    arm=entry['arms'][name];b=entry['b'];h=entry['h']
    if network is None:mean=cpu[name+'_mean'];var=cpu[name+'_var']
    else:mean=network['mean'][h];var=network['var'][h]
    # Action-specific climatology must be provided explicitly in coordinator arrays.
    arm.update(state_statistics(mean[:8],var[:8],cpu['truth_mean'][:8],cpu['truth_var'][:8],cpu['actual'][:8],cpu['climatology'],window,b,sigma,point_tick,arm['failed']))
    realized=np.asarray(cpu['actual_cost'])[:8,h]
    raw=float(np.ptp(realized)) if arm['failed'] else float(realized[arm['chosen']]-realized.min())
    arm['realized_regret_raw']=raw
    # Normalize realized regret using the panel median realized range downstream.
    arm['realized_cost_range']=float(np.ptp(realized))
    return arm


def bootstrap_metrics(entries,name,samples):
    """Vectorized paired case bootstrap; recompute eligible denominator and S_J."""
    rows=[e['arms'][name] for e in entries];eligible=np.array([e['eligible'] for e in entries]);failed=np.array([r['failed'] for r in rows])
    ranges=np.array([np.ptp(r['J']) for r in rows]);scale=np.median(ranges[samples],axis=1)
    J=np.array([r['J'] for r in rows]);C=np.array([r['cost'] for r in rows]);J0=np.array([r['J0'] for r in rows])
    chosen=np.array([r['chosen'] for r in rows]);chosen_cost=np.array([j.max() if fail else j[k] for j,k,fail in zip(J,chosen,failed)])
    ix,iy=np.triu_indices(8,1);target=J[:,iy]-J[:,ix];pred=C[:,iy]-C[:,ix]
    result={}
    def v(field):return np.array([r.get(field) if finite(r.get(field)) else np.nan for r in rows])
    def divide(a,b):
        out=np.full(a.shape,np.nan);np.divide(a,b,out=out,where=b!=0);return out
    for subset,selected in [('eligible',eligible),('all',np.ones(len(rows),bool))]:
        valid=selected&~failed;mask=selected[samples];vmask=valid[samples];count=mask.sum(1);vcount=vmask.sum(1)
        def total(values,good=selected):return np.where(good[samples],np.asarray(values)[samples],0.).sum(1)
        def mean(values,good=selected):return divide(total(values,good),good[samples].sum(1))
        raw=mean(v('regret_raw'));forecasterror=np.abs(C-J).mean(1)
        draws=dict(P=mean(v('correct')),wACC=mean(v('wACC')),pointACC=mean(v('pointACC')),wRMSE=mean(v('wRMSE'),valid),
            regret_raw=raw,regret=divide(raw,scale),cost_forecast_error=divide(mean(forecasterror,valid),scale),
            energy_saved=mean(J0-chosen_cost),energy_saved_percent=mean(divide(100*(J0-chosen_cost),J0)),
            B=divide(total(J0-chosen_cost),total(J0-J.min(1))),
            spearman=mean(np.array([spearman(c,j) if spearman(c,j) is not None else np.nan for c,j in zip(C,J)]),valid))
        draws['B'][total(J0-J.min(1))<=0]=np.nan
        for prefix in ['MSRE','VRE']:
            numerator=total(v(prefix+'_num'),valid);denominator=total(v(prefix+'_den'),valid)
            draws[prefix]=np.sqrt(divide(numerator,denominator))
        draws['cost_difference_RE']=np.sqrt(divide(total(np.sum((pred-target)**2,axis=1),valid),total(np.sum(target**2,axis=1),valid)))
        paircount=28*vcount;pt=total(pred.sum(1),valid);tt=total(target.sum(1),valid)
        cov=total(np.sum(pred*target,axis=1),valid)-divide(pt*tt,paircount)
        pp=total(np.sum(pred*pred,axis=1),valid)-divide(pt*pt,paircount);tp=total(np.sum(target*target,axis=1),valid)-divide(tt*tt,paircount)
        draws['cost_difference_correlation']=divide(cov,np.sqrt(np.maximum(pp,0)*np.maximum(tp,0)))
        result[subset]={f:bounds(values) for f,values in draws.items()}
    return result


def seed_witness_readings(entries,gate,S,samples):
    """Reported seed repeats use the witness-in-S simultaneous level."""
    physics='N-last';readings={};m=gate['metrics']
    if not gate['sufficiency']:return dict(base_seed_witness_count=0,base_seed_readings={})
    for name in ['CNN-20k','CNN-20k-s2','CNN-20k-s3']:
        if name not in m:continue
        point=m[physics]['eligible']['P']-m[name]['eligible']['P'];b=bounds(paired_gap(entries,physics,name,samples),1-.05/len(S))
        a=m[name]['eligible'];n=m[physics]['eligible']
        witness=m[name]['reliable'] and all(finite(v) for v in [a['wACC'],a['wRMSE'],n['wACC'],n['wRMSE'],point,b['lower']]) and a['wACC']>=n['wACC'] and a['wRMSE']<=n['wRMSE'] and point>=.15 and b['lower']>=.10
        readings[name]=dict(witness=bool(witness),gap=point,**b)
    return dict(base_seed_witness_count=sum(r['witness'] for r in readings.values()),base_seed_readings=readings)
