"""Freeze D CPU scoring; only score() opens the existing realized cache."""
import os
os.environ.update(JAX_PLATFORMS='cpu', JAX_ENABLE_X64='true', OPENBLAS_NUM_THREADS='1',
                  OMP_NUM_THREADS='1', NUMBA_NUM_THREADS='4')
import json
from pathlib import Path
import numpy as np
from acd_stage19_part3b_contract import ROOT, OUT, ready, digest
from acd_stage19_l3_statistic import pair_statistic
from acd_stats import difference_interval, one_sided, cp_bounds


def seed_average(pairs, alpha=.01, lower_only=False, expected=5):
    if len(pairs) != expected:
        return dict(evaluable=False, available_seeds=len(pairs), expected_seeds=expected,
                    interval=None, confirmed=None)
    matrix = np.asarray([[np.nan if x is None else x for x in p['case_differences']]
                         for p in pairs], dtype=float)
    n = np.isfinite(matrix).sum(0)
    means = np.divide(np.nansum(matrix, axis=0), n, out=np.zeros(matrix.shape[1]), where=n>0)
    values = means[n>0]
    if not len(values):
        return dict(evaluable=False, interval=None, confirmed=None)
    if lower_only:
        lower = float(2*one_sided((values+1)/2, alpha, 1)-1)
        interval = dict(point=float(values.mean()), lower=lower, alpha=alpha,
                        bound_type='one-sided95% v2.3 instance betting', fallback=False)
        confirmed = lower > 0
    else:
        interval = difference_interval(values, alpha)
        interval['bound_type'] = 'two-sided99% v2.3 instance betting'
        confirmed = not interval['empty'] and not interval['offset'] and interval['lower'] > 0
    return dict(evaluable=True, contributing_instances=int((n>0).sum()),
                defined_seeds_per_instance=n.tolist(),
                case_mean_differences=[float(v) if k else None for v,k in zip(means,n)],
                per_seed=pairs, interval=interval, confirmed=bool(confirmed))


def forcing_error(name):
    values = []
    for case in range(N):
        with np.load(OUT/'inference'/name/f'{case:03d}.npz') as data:
            if 'estimated_F_at_cutoff' not in data:
                return None
            estimate = data['estimated_F_at_cutoff'].copy()
        with np.load(OUT/'inference_inputs'/f'{case:03d}.npz') as data:
            forcing = np.repeat(data['F'], 9)
        if len(estimate) != len(forcing):
            raise RuntimeError('Estimator/draw/action alignment differs')
        values.append(np.column_stack([estimate,forcing]))
    joined = np.concatenate(values)
    error = joined[:,0]-joined[:,1]
    return dict(RMSE=float(np.sqrt(np.mean(error**2))), bias=float(error.mean()),
                correlation=float(np.corrcoef(joined.T)[0,1]),
                population='each retained draw/action at cutoff equally')


def all_pattern_pair(fixed, rolling, truth, tick):
    masks=[s['confident'][:,:8,tick] for s in (fixed,rolling)]
    wrong=[s['modal'][:,:8,tick]!=truth[:,:8,tick] for s in (fixed,rolling)]
    counts=[m.sum(1) for m in masks]
    defined=(counts[0]>0)&(counts[1]>0)
    rates=[np.divide((m&w).sum(1),n,out=np.zeros(len(n)),where=n>0) for m,w,n in zip(masks,wrong,counts)]
    values=rates[1]-rates[0]
    return dict(case_differences=[float(v) if ok else None for v,ok in zip(values,defined)],contributing_cases=int(defined.sum()),interval=difference_interval(values[defined]) if defined.any() else None)

def pattern_group_rows(costs, physical, summary, truth, keep, leads):
    from acd_stats import r0
    rows=[]
    for t,lead in enumerate(leads):
        for group,sl in [('uniform_decrease',slice(0,1)),('seven_zero_mean',slice(1,8))]:
            conf=summary['confident'][:,sl,t];right=summary['modal'][:,sl,t]==truth[:,sl,t]
            accuracy=r0(conf[keep].sum(1),(conf&right)[keep].sum(1))
            errors=[((j[:,:8]-j[:,8,None])-(p[:,:8]-p[:,8,None]))[:,sl,t].ravel() for j,p,k in zip(costs,physical,keep) if k]
            finite=all(np.isfinite(x).all() for x in errors)
            pooled=np.concatenate(errors) if errors and finite else None
            rows.append(dict(lead=float(lead),population=group,confident_share=float(conf[keep].mean()),share_wrong=None if accuracy['answer_accuracy'] is None else 1-accuracy['answer_accuracy'],accuracy=accuracy,equal_case_Dk_bias=float(np.mean([x.mean() for x in errors])) if pooled is not None else None,pooled_Dk_bias=float(pooled.mean()) if pooled is not None else None,equal_case_Dk_RMSE=float(np.mean([np.sqrt(np.mean(x*x)) for x in errors])) if pooled is not None else None,pooled_Dk_RMSE=float(np.sqrt(np.mean(pooled*pooled))) if pooled is not None else None,invalid_errors=not finite))
    return rows

def score():
    freeze = ready()
    from acd_stage19_part3b_inference import complete
    from acd_stage19_learned import model_inputs, metrics
    from acd_stage13_analysis import choices
    if not (OUT/'scoring.npz').exists():
        raise RuntimeError('Existing realized cache required; no new outcome generation')
    # Outcome arrays are opened here only, by the scoring executable.
    with np.load(OUT/'scoring.npz') as data:
        actual, factual = data['actual'].copy(), data['factual'].copy()
    with (OUT/'scoring_access.jsonl').open('a') as log:
        log.write(json.dumps(dict(caller=__file__, path='runs/stage19/scoring.npz',
                                  sha256=digest(OUT/'scoring.npz'), part='3b'))+'\n')
    stage2 = json.loads((ROOT/'receipts/acd_stage2.json').read_text())
    jbar = stage2['null']['jbar']
    null = np.asarray(stage2['null']['question_probabilities'])[np.r_[np.arange(8),37]]
    with np.load(OUT/'reused/runs/stage6/null_block.npz') as data:
        sd = (data['J'][:,:8]-data['J'][:,8,None]).std(0, ddof=1)
    with np.load(OUT/'reused/runs/stage4b_null/states.npz') as data:
        climate = data['states'].mean(0)
    p = model_inputs('posterior', jbar, null)[3]
    fixed = p['observation'][:,:8,0] & p['confident'][:,8,0,None]
    realized_signs = np.concatenate([actual[:,:8] < actual[:,8,None],
                                     (actual[:,8] > jbar)[:,None]], axis=1)
    summaries, models, failed = {}, {}, []
    names = ['CNN-F','CNN-noF']+[r['name'] for r in freeze['tasks']]
    for name in names:
        if not complete(name):
            failed.append(name)
            continue
        inputs = model_inputs(name, jbar, null)
        result = metrics(name, *inputs, actual, factual, jbar, climate, sd, fixed)
        result['forcing_estimate_error'] = forcing_error(name)
        summaries[name] = inputs[3]
        for row in result['decisions']:
            tick = 3 if row['lead'] == 2. else 5
            selected = choices(inputs[0], inputs[2], tick, sd)[row['policy']]
            acting = selected != 8
            effect = actual[np.arange(len(actual)),selected,tick]-actual[:,8,tick]
            harms = int(np.sum(acting & (effect>0)))
            acted = int(acting.sum())
            row.update(strict_positive_harms=harms, actions_taken=acted,
                       zero_effect_ties=int(np.sum(acting & (effect==0))),
                       conditional_harm_CP95=list(cp_bounds(harms,acted)) if acted else [0.,1.])
        from acd_protocol import LEADS
        result['pattern_group_readings']=pattern_group_rows(inputs[0],inputs[4],inputs[3],realized_signs,np.ones(len(actual),dtype=bool),LEADS)
        models[name] = result
        del inputs
    b1, b3, b4, descriptive, risks = [], [], [], [], []
    for j in range(1,6):
        p0 = f'CNN-F-E0-fixed-seed{j}'
        f1, r1 = f'CNN-F-E1-fixed-seed{j}', f'CNN-F-E1-rolling-seed{j}'
        if p0 in summaries and 'CNN-noF' in summaries:
            b1.append(pair_statistic(summaries[p0],summaries['CNN-noF'],realized_signs,3))
            row = next(r for r in models[p0]['decisions'] if r['lead']==3. and r['policy']=='C_delta_0')
            risks.append(dict(seed=j, actions_taken=row['actions_taken'],
                harms=row['strict_positive_harms'], zero_effect_ties=row['zero_effect_ties'],
                CP95=row['conditional_harm_CP95'],
                confirmed=bool(row['conditional_harm_CP95'][1] < .05)))
        if p0 in summaries and 'CNN-F' in summaries:
            descriptive.append(pair_statistic(summaries['CNN-F'],summaries[p0],realized_signs,3))
        if f1 in summaries and r1 in summaries:
            b3.append(pair_statistic(summaries[f1],summaries[r1],realized_signs,5))
            b4.append(all_pattern_pair(summaries[f1],summaries[r1],realized_signs,5))
    b2 = dict(evaluable=len(risks)==5, per_seed=risks,
              bound_type='exact one-sided95% Clopper-Pearson upper',
              confirmed=all(r['confirmed'] for r in risks) if len(risks)==5 else None)
    first = {}
    for part in ['A','B']:
        first.update(json.loads((ROOT/f'receipts/acd_stage18_{part}.json').read_text())['models'])
    original = {row['name']:first.get(row['first_panel_name']) for row in freeze['tasks']}
    original['CNN-F'] = first['CNN-F-ownF']
    original['CNN-noF'] = json.loads((ROOT/'receipts/acd_stage10b.json').read_text())['models']['CNN-noF']
    original['CNN-noF'] = dict(original['CNN-noF'], decisions=json.loads(
        (ROOT/'receipts/acd_stage10b_decisions.json').read_text())['models']['CNN-noF']['readings'])
    result = dict(part='3b', fresh_panel=True, licenses_frozen_route=False,
        freeze_d=json.loads((OUT/'freeze_d_pushed.json').read_text()),
        B1=seed_average(b1), B2=b2, B3=seed_average(b3,alpha=.05,lower_only=True),
        B4=seed_average(b4,alpha=.05,lower_only=True),
        P0_minus_CNN_F_descriptive=seed_average(descriptive), models=models,
        first_panel=original, failed_pipelines=failed,
        resolutions=['Matched Stage16 first-panel pipelines not yet scored are recorded as pending, without substitution.'],
        source_hashes={'realized_cache':digest(OUT/'scoring.npz')}, code_hashes=freeze['code_hashes'])
    (ROOT/'receipts/acd_stage19_part3b.json').write_text(json.dumps(result, indent=2,allow_nan=False)+'\n')
    from acd_stage19_part3b_report import render
    render()


if __name__ == '__main__':
    score()
