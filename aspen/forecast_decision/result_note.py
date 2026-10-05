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
