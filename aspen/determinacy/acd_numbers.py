"""Receipt-only numbers registry; no sampler/physics imports."""
import json,re,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
LEADS=[0,1,1.5,2,2.5,3,4,6]
def lead(v):return str(v).replace('.0','').replace('.','P')+'LT'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def build():
    registry={}
    def add(key,value,path,receipt='receipts/acd_stage2.json',**meta):
        if isinstance(value,bool) or value is None:return
        if not isinstance(value,(int,float)):return
        key=re.sub('[^A-Z0-9_]+','_',key.upper()).strip('_')
        row=dict(value=value,receipt=receipt,receipt_path=path,**meta)
        if key in registry and registry[key]!=row:raise ValueError('Duplicate key '+key)
        registry[key]=row
    def walk(v,key,path,receipt='receipts/acd_stage2.json',suffix='',omit=()):
        if isinstance(v,dict):
            for k,x in v.items():
                if k not in omit:walk(x,key+'_'+k,path+'.'+k,receipt,suffix,omit)
        elif isinstance(v,list):
            for i,x in enumerate(v):walk(x,key+'_'+str(i),path+f'[{i}]',receipt,suffix,omit)
        else:add(key+suffix,v,path,receipt)
    for dev,name in [(False,'acd_stage2.json'),(True,'acd_stage1.json')]:
        receipt='receipts/'+name;d=json.loads((ROOT/receipt).read_text());prefix='ACD_DEV_' if dev else 'ACD_'
        for i,row in enumerate(d['R0']):
            suffix='_'+lead(row['lead'])
            walk(row['R0'],prefix+'R0','$.R0['+str(i)+'].R0',receipt,suffix)
            walk(row['R0_F'],prefix+'R0F','$.R0['+str(i)+'].R0_F',receipt,suffix)
        for i,row in enumerate(d['R1']):
            walk(row,prefix+'R1_'+row['type'],f'$.R1[{i}]',receipt,'_'+lead(row['lead']))
        for key in ['R2a','R2b','R2c','R5','coverage','excluded','fit_flags','cases','settings','resolutions']:
            walk(d[key],prefix+key,'$.'+key,receipt,omit=('site_records',))
        for arm in ['R3','R3b','R6']:
            if arm in d:walk(d[arm],prefix+arm,'$.'+arm,receipt,omit=('site_records','posterior_agreement','kappa_by_type_lead','reliability_by_lead','reliability_by_type_lead'))
        m=d['R1m']
        for key,v in m.items():
            if isinstance(v,dict) and 'median' in v:
                axis=LEADS if len(v['median'])==8 else range(len(v['median']))
                for i,t in enumerate(axis):
                    suffix='_'+lead(t) if len(v['median'])==8 else '_TICK_'+str(t)
                    add(prefix+'R1M_'+key+'_MEDIAN'+suffix,v['median'][i],f'$.R1m.{key}.median[{i}]',receipt)
                    for q,label in enumerate(['Q25','Q75']):
                        add(prefix+'R1M_'+key+'_'+label+suffix,v['quartiles'][q][i],f'$.R1m.{key}.quartiles[{q}][{i}]',receipt)
                if 'descriptive' in v:walk(v['descriptive'],prefix+'R1M_'+key+'_BOOTSTRAP','$.R1m.'+key+'.descriptive',receipt)
            else:walk(v,prefix+'R1M_'+key,'$.R1m.'+key,receipt)
        for i,t in enumerate(LEADS):
            paths=[f'$.R1m.z_D.median[{i}]',f'$.R1m.z_F.median[{i}]']
            add(prefix+'R1M_ZD_OVER_ZF_RATIO_OF_MEDIANS_'+lead(t),m['z_D']['median'][i]/m['z_F']['median'][i],paths,receipt,derivation='ratio of saved medians; not median of per-question ratios')
            a=m['lead_relationship'][i];all_s=a['confident_S_share'];obs=a['observation_S_share']
            if all_s:add(prefix+'L5_CLIMATE_FRACTION_'+lead(t),(all_s-obs)/all_s,[f'$.R1m.lead_relationship[{i}].confident_S_share',f'$.R1m.lead_relationship[{i}].observation_S_share'],receipt,derivation='(all confident S - observation confident S) / all confident S')
        rows=d['R2c']['readings'];ans=[x for x in rows if x['answers']];ref=[x for x in rows if not x['answers']]
        denom=sum(x['answered_not_confident_share'] for x in ans)
        if ans:add(prefix+'L9_ANSWERED_NOT_CONFIDENT',sum(x['answered_not_confident_share'] for x in ans)/len(ans),'$.R2c.readings',receipt,derivation='mean over answered leads')
        if ref:add(prefix+'L9_REFUSED_CONFIDENT',sum(x['refused_confident_share'] for x in ref)/len(ref),'$.R2c.readings',receipt,derivation='mean over refused leads')
        if denom:add(prefix+'L9_EXCEPTION_ACCURACY',sum(x['answered_not_confident_share']*(x['exception_accuracy'] or 0) for x in ans)/denom,'$.R2c.readings',receipt,derivation='exception-share weighted accuracy in answered range')
    for dev,name in [(False,'acd_stage2.json'),(True,'acd_stage1.json')]:
        receipt='receipts/'+name;d=json.loads((ROOT/receipt).read_text());prefix='ACD_DEV_' if dev else 'ACD_'
        for i,r in enumerate(d['resolutions']):
            for j,m in enumerate(re.finditer(r'(?<![A-Za-z0-9])\d+',r['trigger'])):
                add(prefix+'RESOLUTION_TRIGGER_'+str(i)+'_'+str(j),int(m[0]),f'$.resolutions[{i}].trigger',receipt,derivation='integer literal parsed from trigger string')
    # Literal contract numbers have honest sources: never invent Stage2 receipt paths.
    step=json.loads((ROOT/'receipts/acd_step0.json').read_text())
    for key,path,value in [('LT','$.LT',step['LT']),('SIGMA','$.SIGMA',step['SIGMA']),('OUT','$.OUT',step['OUT']),('CNN_STEP','$.checkpoint_metadata.step',step['checkpoint_metadata']['step'])]:
        add('ACD_CONTRACT_'+key,value,path,'receipts/acd_step0.json')
    constants={'VERSION':2.3,'STATE_DIMENSION':40,'FRAMES':11,'WINDOW_LT':1,'OBSERVATION_LT':.84,'OBSERVATION_NOISE_FACTOR':.02,'PROBE_FACTOR':.1,'AMPLITUDE':.16,'CONFIDENCE':.95,'PARAMETERS':41,'FORCING_MIN':6,'FORCING_MAX':10,'FORCING_MIDPOINT':8,'MAP_START_LOW':6.5,'MAP_START_HIGH':9.5,'RHAT_LIMIT':1.01,'ESS_MIN':400,'DIAG_WARMUP':2000,'RML_1A_S_QUESTIONS':160,'PUBLICATION_YEAR':2026,'BOOTSTRAP_COUNT':10000,'CP_LOWER_FLOOR':.80,'R5_SETTLED_MIN':20,'R0_FLOOR':.90,'COVERAGE_FLOOR':.85,'R5_MARGIN':.10,'R2A_MARGIN':.15,'R2B_MARGIN':.20,'R5_ALPHA':.01,'R2_ALPHA':.01,'CHI2_COVERAGE':56.94,'FIT_THRESHOLD':467.6,'PRIOR_SCALE':10,'SECTIONS':20,'ZERO':0,'ONE':1,'TWO':2,'THREE':3,'FOUR':4,'FIVE':5,'SEVEN':7,'NINE':9,'TWELVE':12,'PERCENT_SCALE':100,'BOOTSTRAP_CI_PERCENT':95,'ROUTE_CI_PERCENT':99}
    for key,value in constants.items():add('ACD_CONTRACT_'+key,value,'literal §3–§14; contract, not an empirical result','sources/WO_v2.3.md',provenance='R-other: no corresponding numeric field in Stage2 receipt')
    d=json.loads((ROOT/'receipts/acd_stage2.json').read_text())
    add('ACD_PANEL_LAST_CASE',d['cases']-1,'$.cases',derivation='cases minus one: last zero-based confirmation index')
    for i,r in enumerate(d['resolutions']):
        detail=r['detail']
        if isinstance(detail,dict):
            for field in ['initial_seconds','after_population_seconds']:
                if field in detail:add('ACD_PROJECTION_'+field+'_HOURS',detail[field]/3600,f'$.resolutions[{i}].detail.{field}',derivation='saved seconds / 3600')
    for filename,prefix in [('receipts/acd_stage4_f1.json','ACD_F1'),('receipts/acd_stage4_amplitude.json','ACD_DEV_AMPLITUDE')]:
        if (ROOT/filename).exists():
            stage4=json.loads((ROOT/filename).read_text())
            walk(stage4,prefix,'$',filename,omit=('source_hashes','forecast_hashes'))
    add('ACD_CONTRACT_R0_CI_LEVEL',.95,'literal one-sided R0 confidence level, §10','sources/WO_v2.3.md')
    add('ACD_CONTRACT_OBSERVATION_SPAN_LT',(constants['FRAMES']-1)*step['OUT']/step['LT'],['$.OUT','$.LT'],'receipts/acd_step0.json',derivation='(11 snapshots - 1) * OUT / LT',additional_sources=[dict(receipt='sources/WO_v2.3.md',receipt_path='§3–§4, 11 snapshots')])
    add('ACD_CONTRACT_R2C_HALF_CASES',.5,'literal R2c at least half of cases, §10','sources/WO_v2.3.md')
    add('ACD_NULL_FORCING',d['null']['F'],'$.null.F',derivation='true forcing specified in WO §3 and used by the saved climatological null')
    add('ACD_CONTRACT_MODEL_IDENTIFIER',96,'literal Lorenz-96 model name, §3; identifier, not state dimension','sources/WO_v2.3.md')
    amplitude_receipt='receipts/acd_stage4_amplitude.json'
    if (ROOT/amplitude_receipt).exists():
        a=json.loads((ROOT/amplitude_receipt).read_text())['rows']
        lo=min(range(len(a)),key=lambda i:a[i]['amplitude']);hi=max(range(len(a)),key=lambda i:a[i]['amplitude'])
        add('ACD_DEV_AMPLITUDE_RANGE_FACTOR',a[hi]['amplitude']/a[lo]['amplitude'],[f'$.rows[{hi}].amplitude',f'$.rows[{lo}].amplitude'],amplitude_receipt,derivation='maximum tested amplitude / minimum tested amplitude')
        for name,i in [('MIN',lo),('MAX',hi)]:
            add('ACD_DEV_AMPLITUDE_'+name+'_FRACTION_TRUE_FORCING',a[i]['amplitude']/d['null']['F'],f'$.rows[{i}].amplitude',amplitude_receipt,derivation='tested amplitude / true forcing ACD_NULL_FORCING',additional_sources=[dict(receipt='receipts/acd_stage2.json',receipt_path='$.null.F')])
    matched_receipt='receipts/acd_stage4b_amplitude_matched.json'
    if (ROOT/matched_receipt).exists():
        matched=json.loads((ROOT/matched_receipt).read_text())
        add('ACD_DEV_AMP_TESTED_AMPLITUDES_COUNT',len(matched['rows']),'$.rows',matched_receipt,derivation='number of saved tested amplitude rows')
        for field in ['states','F','dt','cases','excluded','bootstrap_replicates','betting_interval_level','null_reproduction']:
            walk(matched[field],'ACD_DEV_AMP_'+field,'$.'+field,matched_receipt)
        for i,row in enumerate(matched['rows']):
            token='A'+str(row['amplitude']).replace('.','P')
            stem='ACD_DEV_AMP_'+token
            add(stem+'_AMPLITUDE',row['amplitude'],f'$.rows[{i}].amplitude',matched_receipt)
            add(stem+'_FRACTION_TRUE_FORCING',row['fraction_true_forcing'],f'$.rows[{i}].fraction_true_forcing',matched_receipt)
            add(stem+'_CASES',row['cases'],f'$.rows[{i}].cases',matched_receipt)
            for j,r in enumerate(row['shares']):
                walk(r,stem+'_R1',f'$.rows[{i}].shares[{j}]',matched_receipt,'_'+lead(r['lead']))
            for j,r in enumerate(row['R2a']):
                walk(r,stem+'_R2A',f'$.rows[{i}].R2a[{j}]',matched_receipt,'_'+lead(r['lead']))
            walk(row['R2b'],stem+'_R2B',f'$.rows[{i}].R2b',matched_receipt,omit=('case_values',))
    null_receipt='receipts/acd_stage4b_null.json'
    if (ROOT/null_receipt).exists():
        null=json.loads((ROOT/null_receipt).read_text())
        for field in ['states','F','dt','threads','spinup_LT','spinup_steps','seed','baseline_comparison']:
            walk(null[field],'ACD_DEV_AMP_NULL_'+field,'$.'+field,null_receipt)
        for amp,r in null['amplitudes'].items():
            token='A'+amp.replace('.','P')
            for i,share in enumerate(r['Fc_above_shares']):
                add('ACD_DEV_AMP_NULL_'+token+'_FC_ABOVE_SHARE_'+lead(LEADS[i]),share,'$.amplitudes.'+amp+f'.Fc_above_shares[{i}]',null_receipt)
    # Stage 5 paper quantities: existing receipts only; no scientific execution.
    calibration=d['all_confident_calibration']
    walk(calibration,'ACD_ALL_CONFIDENT_CALIBRATION','$.all_confident_calibration')
    all_answers=sum(r['answers'] for r in calibration);all_correct=sum(r['correct'] for r in calibration)
    add('ACD_ALL_CONFIDENT_ANSWERS',all_answers,'$.all_confident_calibration[*].answers',derivation='sum over S/Fc at all tested leads and P/B at 2 and 3 LT; repeated questions are not independent samples')
    add('ACD_ALL_CONFIDENT_CORRECT',all_correct,'$.all_confident_calibration[*].correct',derivation='sum over the declared type/lead rows')
    add('ACD_ALL_CONFIDENT_ACCURACY',all_correct/all_answers,['$.all_confident_calibration[*].correct','$.all_confident_calibration[*].answers'],derivation='pooled correct / pooled confident answers; descriptive, not R0 case accuracy')
    selected=[i for i,r in enumerate(calibration) if r['type']=='S' and 0<=r['lead']<=3]
    paths=[f'$.all_confident_calibration[{i}]' for i in selected]
    add('ACD_S_CONFIDENT_ANSWERS_0_TO_3LT',sum(calibration[i]['answers'] for i in selected),paths,derivation='sum S confident answers at tested leads 0 through 3 LT inclusive')
    add('ACD_S_CONFIDENT_WRONG_0_TO_3LT',sum(calibration[i]['answers']-calibration[i]['correct'] for i in selected),paths,derivation='sum S answers minus correct at tested leads 0 through 3 LT')
    walk(d['true_F_rank']['uniformity_KS'],'ACD_TRUE_F_RANK_KS','$.true_F_rank.uniformity_KS')
    close_receipt='receipts/acd_stage2_closeout.json'
    close=json.loads((ROOT/close_receipt).read_text())
    for field in ['ordinary_all_draw_forecasts','ordinary_warmup_retries','ordinary_exclusions','refits']:
        add('ACD_CLOSEOUT_'+field,close[field],'$.'+field,close_receipt)
    add('ACD_CONTRACT_FULL_DRAW_VOTE_THRESHOLD',__import__('math').ceil(.95*4*d['settings']['draws']),'$.settings.draws',derivation='ceil(confidence .95 * four chains * frozen draws per chain); only applies to full 2000-draw forecasts',additional_sources=[dict(receipt='sources/WO_v2.3.md',receipt_path='§5: four chains and §6: at least 0.95')])
    horizon_receipt='../horizon/results/l96_calibration.json'
    horizon=json.loads((ROOT/horizon_receipt).read_text())['system']
    for key,field in [('LAMBDA1','lambda_mean'),('SIGMA','sigma')]:
        add('ACD_HORIZON_'+key,horizon[field],'$.system.'+field,horizon_receipt,additional_sources=[dict(receipt='../horizon/NUMBERS.md',receipt_path='AAHLSYSTEM-1; rounded display')])
    numerical_receipt='receipts/acd_numerical.json'
    numerical=json.loads((ROOT/numerical_receipt).read_text())
    for field in ['joint_adjoint_error','jax_relative_match','dtcheck']:
        walk(numerical[field],'ACD_NUMERICAL_'+field,'$.'+field,numerical_receipt)
    walk(numerical['implementation'],'ACD_NUMERICAL_GAUSSIAN','$.implementation',numerical_receipt,omit=('precision','mean','covariance'))
    probabilities=d['null']['question_probabilities']
    candidates=[]
    for k in range(1,8):
        for i,t in enumerate(LEADS):
            answer=max(range(2),key=lambda j:probabilities[k][i][j])
            path=f'$.null.question_probabilities[{k}][{i}][{answer}]'
            value=probabilities[k][i][answer];candidates.append((value,path))
            add(f'ACD_NULL_S_PATTERN_{k}_MODAL_PROBABILITY_'+lead(t),value,path,derivation='larger of two sign probabilities; climate-only modal confidence, not posterior-modal agreement')
    for label,f in [('MIN',min),('MAX',max)]:
        value,path=f(candidates)
        add('ACD_NULL_S_PATTERNS_1_TO_7_MODAL_PROBABILITY_'+label,value,path,derivation='extremum over patterns 1–7 and all eight tested leads; both probabilities sum to one')

    sources=['receipts/acd_stage2_closeout.json','receipts/acd_numerical.json','../horizon/results/l96_calibration.json','../horizon/NUMBERS.md','receipts/acd_stage2.json','receipts/acd_stage1.json','receipts/acd_step0.json','sources/WO_v2.3.md','receipts/acd_stage4_f1.json','receipts/acd_stage4_amplitude.json','receipts/acd_stage4b_amplitude_matched.json','receipts/acd_stage4b_null.json']
    return dict(schema=1,source_hashes={p:digest(ROOT/p) for p in sources if (ROOT/p).exists()},numbers=dict(sorted(registry.items())))
def render(d):
    lines=['# Aspen determinacy numbers — receipt registry','', 'Confirmation keys use ACD_; every development quantity uses ACD_DEV_. Full precision is retained in JSON. Empirical paths refer to receipts/acd_stage2.json; development to receipts/acd_stage1.json. Derived quantities list actual input paths and the operation. Contract constants have separately identified sources under R-other; no nonexistent numeric receipt path is asserted.','', '| Key | Full precision | Source | Receipt path / derivation |','|---|---|---|---|']
    for k,v in d['numbers'].items():lines.append(f"| {k} | {repr(v['value'])} | {v['receipt']} | {v['receipt_path']}"+(' ; '+v['derivation'] if 'derivation' in v else '')+' |')
    return '\n'.join(lines)+'\n'
def write():
    d=build();(ROOT/'numbers_acd.json').write_text(json.dumps(d,indent=2,allow_nan=False)+'\n');(ROOT/'NUMBERS_ACD.md').write_text(render(d));print('NUMBERS',len(d['numbers']))
if __name__=='__main__':write()
