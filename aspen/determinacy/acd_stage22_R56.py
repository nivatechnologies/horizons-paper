"""Thin R5/R6 wrapper; frozen probability, pair, seed and CP functions only."""
def score(existing, tasks):
    import numpy as np
    import acd_stage21_score as frozen
    import acd_stage22_adapter as adapter
    from acd_stage19_l3_statistic import pair_statistic
    from acd_stage19_part3b_score import seed_average
    actual,_=frozen.score_actual()  # Sole outcome opener remains the frozen scorer.
    assert actual.shape[0]==adapter.N
    levels=frozen.assignments()
    assert len(levels)==adapter.N
    climates={}
    for level in [7,9]:
        with np.load(frozen.OUT/'climatology'/f'F{level}.npz') as data:
            climates[level]=dict(jbar=float(data['jbar']),null=data['prob'].copy())
    truth=np.concatenate([actual[:,:8]<actual[:,8,None],
          (actual[:,8]>np.array([climates[f]['jbar'] for f in levels])[:,None])[:,None]],1)
    assert truth.shape[0]==adapter.N
    summaries={}
    for row in tasks:
        if row.get('kind')!='E0':continue
        rows=[]
        for case,level in enumerate(levels):
            with np.load(frozen.OUT/'inference'/row['name']/f'{case:03d}.npz') as data:
                costs=data['J'].copy();valid=bool(data['valid'].all()) and np.isfinite(costs).all()
            summary=frozen.binary(costs,climates[level]['jbar'],climates[level]['null'])
            if not valid or case in existing['excluded_cases']:
                summary['confident'].fill(False);summary['observation'].fill(False)
            rows.append(summary)
        summaries[row['name']]=frozen.stack(rows)
        assert all(array.shape[0]==adapter.N for array in summaries[row['name']].values())
    required=[f'CNN-F-E0-{arm}-seed{seed}' for arm in ['fixed','rolling'] for seed in range(1,6)]
    if any(name not in summaries for name in required):
        return dict(R5_S22=dict(evaluable=False),R6_S22=dict(evaluable=False))
    def paired(ids):
        pairs=[]
        for seed in range(1,6):
            fixed=summaries[f'CNN-F-E0-fixed-seed{seed}'];rolling=summaries[f'CNN-F-E0-rolling-seed{seed}']
            pairs.append(pair_statistic({k:v[ids] for k,v in fixed.items()},
                         {k:v[ids] for k,v in rolling.items()},truth[ids],3))
        return seed_average(pairs,alpha=.01,lower_only=False)
    result=dict(R5_S22=paired(np.arange(adapter.N)),R5_by_forcing={})
    for label,level in [('F7',7),('F9',9)]:result['R5_by_forcing'][label]=paired(np.flatnonzero(levels==level))
    risk={}
    for label in ['pooled','F7','F9']:
        rows=[]
        for seed in range(1,6):
            model=existing['models'][f'CNN-F-E0-rolling-seed{seed}'][label]
            row=next(r for r in model['decisions'] if r['lead']==3. and r['policy']=='C_delta_0')
            rows.append(dict(seed=seed,actions=row['actions_taken'],strict_positive_harms=row['harms'],
                 zero_effect_ties=row['acted_zero_effect_ties'],
                 point=row['harms']/row['actions_taken'] if row['actions_taken'] else None,
                 lower=row['conditional_harm_CP95'][0],upper=row['conditional_harm_CP95'][1],
                 bound_type='exact one-sided95% Clopper-Pearson lower',
                 confirmed=bool(row['actions_taken'] and row['conditional_harm_CP95'][0]>.05)))
        risk[label]=dict(per_seed=rows,confirmed=all(r['confirmed'] for r in rows))
    result.update(R6_S22=risk['pooled'],R6_by_forcing={k:v for k,v in risk.items() if k!='pooled'})
    return result
