"""Gate-summary Markdown from checked NUMBERS records, never invented values."""

def value(x):return 'unavailable' if x is None else f'{x:.6g}'

def stage1_note(reading,checker):
    if checker.get('status')!='PASS':raise ValueError('checker PASS required')
    r=reading['primary'];a=r['arms'];n=a['N-last'];c=a['CNN-20k']
    return '\n'.join([
        '# Aspen forecast-versus-decision: Stage 1 reading','',
        f"Stage and gate: Stage 1, sufficiency then H1a, T*=2 LT. {r['sufficiency_status']}; H1a {r['H1a']}.",'',
        f"Sufficiency: {r['eligible']}/{r['total']} eligible ({value(r['eligible_fraction'])}); P_N − max(P_myopic,P_fixed)={value(r['null_gap'])}; myopic={value(r['myopic_P'])}; fixed={value(r['fixed_P'])}.",'',
        f"H1a: P_N={value(n['P'])}; P_CNN-20k={value(c['P'])}; gap={value(r['gap'])}; one-sided 95% lower={value(r['lower95'])}, upper={value(r['upper95'])}.",'',
        f"wACC: N-last={value(n['wACC'])}, CNN-20k={value(c['wACC'])}. wRMSE: N-last={value(n['wRMSE'])}, CNN-20k={value(c['wRMSE'])}.",'',
        f"Failed cases: N-last={n['failed_cases']}, CNN-20k={c['failed_cases']}; dropped members: N-last={n['dropped_members']}/{n['attempted_members']}, CNN-20k={c['dropped_members']}/{c['attempted_members']}.",'',
        'Stage 1 licenses no sentence. Source: NUMBERS Stage-1 reading and checker PASS.',''])


def licensed_text(result):
    """Frozen prose only after completed Stage-2 gate, with numeric provenance."""
    from protocol import ORDER
    p=result['primary'];g=p['gate'];ids=g['licensed_sentences'];m=g['metrics'];physics='N2' if result['stage']=='2b' else 'N-last';base='CNN2-20k' if result['stage']=='2b' else 'CNN-20k';cost='CNN2-cost' if result['stage']=='2b' else 'CNN-cost';selected=result.get('selected')
    f=lambda x:'unavailable' if x is None else f'{x:.6g}'
    P=lambda a:f(m[a]['eligible']['P']);R=lambda a:f(m[a]['all']['regret']);B=lambda a:f(m[a]['all']['B'])
    witness=min(g['witnesses'],key=lambda a:(-m[a]['eligible']['wACC'],ORDER.index(a) if a in ORDER else len(ORDER))) if g.get('witnesses') else None
    texts={}
    if witness:
        texts['S1']=f"A deterministic learned emulator ({witness}) with window ACC at least as high and window RMSE no higher than the physics arm's identifies the best intervention less often: {P(witness)} against {P(physics)}."
        texts['S1+']=f"…and incurs higher energy regret: {R(witness)} against {R(physics)}, capturing {B(witness)} against {B(physics)} of the attainable energy reduction."
        texts['S8']=f"With unresolved fast scales, where the physics arm knows only the resolved dynamics and fits its closure from the X data the base emulator trains on, a deterministic learned emulator ({witness}) with window ACC at least as high and window RMSE no higher also identifies the best intervention less often: {P(witness)} against {P(physics)}."
    if selected and g.get('H1b_bounds') is not None:
        gap=g['H1b_bounds']['point']
        texts['S2']=f"The validation-selected emulator ({selected}) retains a {f(100*gap)}-point gap."
        texts['S2+']=f"…with higher energy regret, capturing {B(selected)} against {B(physics)} of the attainable energy reduction."
        texts['S8+']=f"…and the validation-selected emulator retains a {f(100*gap)}-point gap"+(' with higher energy regret.' if g['REG'][selected]['95']['holds'] else '.')
    repairs=g.get('repairs',{})
    texts['S3']='None of the tested repaired models ('+', '.join(a for a,r in repairs.items() if r['reading']=='RETAINS')+') closes the gap; each retains one.'
    repair_text=[]
    for a,r in repairs.items():
        if r['reading']=='RETAINS':s=f'Repair {a} retains a gap'
        elif r['reading']=='CLOSES':s=f'Repair {a} is no more than five points worse than the physics arm'
        elif r['reading']=='unstable':s=f'Repair {a} is unstable and is not counted'
        else:s=f"Repair {a}'s gap is unresolved (interval {f(r['bounds']['lower'])} to {f(r['bounds']['upper'])})"
        if r['NARROWS']:s+=' and narrows the base model\'s gap'
        repair_text.append(s+'.')
    texts['S7']=texts['S7₂']=' '.join(repair_text)
    if 'CNN-resp' in m and 'CNN-roll' in m:
        delta=m['CNN-resp']['eligible']['P']-m['CNN-roll']['eligible']['P']
        texts['S4']=f'The model trained with an added loss on solver-generated counterfactual pairs closes the gap, gaining {f(100*delta)} points over its otherwise identical rollout-trained twin.'
        texts['S4b']='The counterfactual-supervised emulator is no more than five percentage points worse than the physics arm.'
        texts['S5']='This counterfactual-pair repair retains a gap.'
    texts['S6']='Physics with run-time identification makes better intervention decisions than every tested learned model, in this matched-law setting.'
    if cost in m and g.get('H1e_bounds') is not None:
        texts['S10']=f'A model trained directly on intervention cost, with solver-generated labels for every action, also identifies the best intervention less often: {P(cost)} against {P(physics)}.'
        texts['S10+']='…with higher energy regret.'
        texts['S10b']=f'A model trained directly on intervention cost, with solver-generated labels for every action, is no more than five points worse than the physics arm: {P(cost)} against {P(physics)}.'
        cb=g['H1e_bounds'];texts['S10c']=f"Whether a model trained directly on intervention cost retains a gap is unresolved ({P(cost)} against {P(physics)}, interval {f(cb['lower'])} to {f(cb['upper'])})."
        texts['S11']=texts['S10' if g['H1e']=='RETAINS' else 'S10b' if g['H1e']=='CLOSES' else 'S10c']
    if result['stage']=='2b':
        outcome='the two-scale panel could not test the claim' if not g['sufficiency'] else 'the comparably skilled emulators are no more than five points worse than the physics arm' if g['H1a']=='KILL' else 'the physics arm is no better than a trivial rule' if not g['physics_floor'] else 'the comparison is unresolved'
        texts['S9']='With unresolved fast scales, '+outcome+'.'
        if g.get('S12'):texts['S12']=f"The online forcing adjustment adds {f(100*g['S12_bounds']['point'])} points over a forcing fixed offline."
    if 'S1s' in ids:texts['S1s']=f"Of three independently trained base models, {g['base_seed_witness_count']} meet the same criteria."
    return [{'id':i,'text':texts[i]} for i in ids]


def stage2_note(result,checker):
    if checker.get('status')!='PASS':raise ValueError('checker PASS required')
    g=result['primary']['gate'];m=g['metrics'];physics='N2' if result['stage']=='2b' else 'N-last';selected=result.get('selected')
    value=lambda x:'unavailable' if x is None else f'{x:.6g}'
    headline='H1a '+str(g['H1a'])+'; H1b '+str(g['H1b'])+'. '
    if selected and g.get('H1b_bounds') is not None:
        b=g['H1b_bounds'];headline+=f"Validation-selected {selected}: gap {value(b['point'])}, lower {value(b['lower'])}, upper {value(b['upper'])}; PASS requires gap≥0.10 and lower≥0.05; KILL requires upper≤0.05."
    choice='stop' if g['H1a']=='KILL' and result['stage']=='2' else 'go' if g['H1a']=='PASS' and g['H1b']=='PASS' else 'pivot'
    reason='H1a KILL ends the campaign under WO §9' if choice=='stop' else 'the full headline thresholds are met, with all mandatory companion readings below' if choice=='go' else 'the full headline is not licensed; Todd decides whether the measured scope warrants an Aspen headline'
    lines=[f"Stage and gate: Stage {result['stage']}, sufficiency then frozen hypotheses at T*=2 {'LT_ref' if result['stage']=='2b' else 'LT'}.",
           f"Headline value now, against the threshold: {headline}",
           'What changed since the last gate: frozen training, validation selection and complete test inference now supply the budgeted repairs and decision-trained comparison.',
           'Largest remaining risk to the so-what test: the matched-law operating point and the measured outcome of the strongest incumbent; the two-scale reading determines the broader scope.',
           f'Coordinator would: {choice}, because {reason}.','',
           f"Sufficiency: {g['eligible']}/{g['total']} eligible; physics-minus-strongest-null {value(g['null_gap'])}; sufficiency {'PASS' if g['sufficiency'] else 'otherwise'}.",'',
           '| Arm | P | wACC | wRMSE | Failed cases | Dropped members | Reliable |','|---|---|---|---|---|---|---|']
    for name,a in m.items():lines.append('| '+ ' | '.join([name,value(a['eligible']['P']),value(a['eligible']['wACC']),value(a['eligible']['wRMSE']),str(a['failed_cases']),str(a['dropped_members']),str(a['reliable'])])+' |')
    lines+=['','H1a witness and KILL bounds: '+str(g.get('H1a_bounds'))+'; '+str(g.get('H1a_kill_bounds')),
            'Repair readings: '+str(g.get('repairs')),
            'H1e: '+str(g['H1e'])+'; '+str(g.get('H1e_bounds')),
            'H1c: '+str(g['H1c'])+'; H2: '+str(g['H2'])+'; H3: '+str(g['H3']),
            '', 'One-scale conditional sentences; final abstract set remains open until combined Stage2b scope check:' if result['stage']=='2' else 'Licensed two-scale sentences (WO §7.7):','']
    lines.extend(x['id']+': '+x['text'] for x in licensed_text(result));lines+=['','Every displayed number comes from the checked NUMBERS full-metrics record.','']
    return '\n'.join(lines)
