"""Discrete frozen verdicts and descriptive correlations; no interpolation."""
import json
import numpy as np
from common import ROOT,GRID,write_json,sha

def G(x):
    return next((float(t) for t in GRID if t>=x),None)

def system_reading(data):
    tf=data['Tf'];td=data['Td'];byT={r['T']:r for r in data['horizons']}
    killT=G(1.5*tf) if tf is not None else None
    passT=G(3*tf) if tf is not None else None
    killrow=byT.get(killT);forecastrow=byT.get(tf)
    kill=bool(killrow and killrow['sufficient'] and killrow['arms']['paired']['accuracy'][3] is not None and killrow['arms']['paired']['accuracy'][3]<.5)
    passed=bool(tf is not None and td is not None and passT is not None and td>=passT and forecastrow['member_criterion']['pass_condition'])
    return dict(Tf=tf,Td=td,kill_grid_T=killT,pass_grid_T=passT,kill_condition=kill,pass_condition=passed,
                ratio_at_Tf=forecastrow['member_criterion']['ratio_lower_bound'] if forecastrow else None,
                accuracy_at_kill_T=killrow['arms']['paired']['accuracy'][3] if killrow else None)

def partial(x,y,z):
    x=np.asarray(x,dtype=float);y=np.asarray(y,dtype=float);z=np.asarray(z,dtype=float)
    if len(x)<3:return None
    design=np.column_stack([np.ones(len(z)),z])
    if np.linalg.matrix_rank(design)!=2:return None
    q,r=np.linalg.qr(design,mode='reduced')
    # Full-rank QR solve only: no pseudoinverse or denominator adjustment.
    rx=x-design@np.linalg.solve(r,q.T@x);ry=y-design@np.linalg.solve(r,q.T@y)
    if np.std(rx)==0 or np.std(ry)==0:return None
    return float(np.corrcoef(rx,ry)[0,1])

def diagnostics(data):
    rows=[]
    for h in data['horizons']:
        for arm in ['learned','misidentified','jitter']:
            if arm not in h['arms']:continue
            a=h['arms'][arm]
            rows.append(dict(arm=arm,T=h['T'],accuracy=a['accuracy'][3],ACC=a['ACC'],
                             response=a['response_correlation'],response_relative_error=a['response_relative_error']))
    eligible=[r for r in rows if all(r[k] is not None and np.isfinite(r[k]) for k in ['accuracy','ACC','response'])]
    y=[r['accuracy'] for r in eligible];f=[r['ACC'] for r in eligible];r=[r['response'] for r in eligible]
    learnedTf=next((h['T'] for h in data['horizons'] if 'learned' in h['arms'] and h['arms']['learned']['ACC'] is not None and h['arms']['learned']['ACC']<.2),None)
    return dict(unit='(arm,grid T), pooled learned/misidentified/jitter within system',inference=False,
                attempted_units=len(rows),available_units=len(eligible),learned_Tf=learnedTf,
                learned_Tf_status='pending' if data.get('learned_arm_pending',True) else ('defined' if learnedTf is not None else 'censored_or_unavailable'),
                partial_accuracy_response_controlling_ACC=partial(y,r,f),
                partial_accuracy_ACC_controlling_response=partial(y,f,r),units=rows)

def main():
    systems={};diag={};complete=True
    for key in ['l96','kolmo']:
        p=ROOT/f'results/{key}_solver_statistics.json'
        if not p.exists():complete=False;continue
        d=json.loads(p.read_text());systems[key]=system_reading(d);diag[key]=diagnostics(d)
        complete &= not d.get('learned_arm_pending',True)
    verdict='PENDING'
    if len(systems)==2:
        verdict='KILL' if all(s['kill_condition'] for s in systems.values()) else ('PASS' if all(s['pass_condition'] for s in systems.values()) else 'OTHERWISE')
    write_json(ROOT/'results/readings.json',dict(scientific_verdict=verdict,required_evidence_complete=complete,systems=systems,diagnostics=diag,git_sha=sha()))
    print(verdict,'required evidence complete:',complete)

if __name__=='__main__':main()
