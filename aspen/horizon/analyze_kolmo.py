"""Frozen horizon statistics from retained World D per-case evidence."""
import argparse
import concurrent.futures
import json
import numpy as np
from common import ROOT,GRID,BUDGETS,eligible,rng,m95,member_reading,write_json,sha
from analyze_l96 import acc
from enrich_l96 import mean_available

def one_case(c):
    root=ROOT/'runs/kolmo/test'
    data=np.load(root/f'arms_{c:03d}.npz');target=np.load(root/f'targets_{c:03d}.npz')
    truth=np.load(root/f'truth_{c:03d}.npy');climate=np.load(root/'climatology.npy').reshape(6,-1)
    neural_path=root/f'neural_{c:03d}.npz'
    neural=np.load(neural_path) if neural_path.exists() else None
    row=dict(case=c,eligible=[],best=[],arms={},commitment=[],null_regrets=[],myopic_correct=[],truth_differences=[])
    arms=['paired','unpaired','jitter','misidentified']+(['learned'] if neural is not None else [])
    for arm in arms:row['arms'][arm]=dict(correct=[],regret=[],realized_regret=[],acc=[],response_differences=[])
    for h,T in enumerate(GRID):
        e=eligible(truth[:,:,h],'truth',1,c);row['eligible'].append(e['eligible']);row['best'].append(e['best'])
        expected=truth[:,:,h].mean(1);actual=target['actual_cost'][:,h];gap=np.ptp(expected);agap=np.ptp(actual)
        row['truth_differences'].append([float(expected[j]-expected[k]) for j in range(6) for k in range(j)])
        chosen=int(data['myopic_chosen']);row['myopic_correct'].append(chosen==e['best'])
        row['null_regrets'].append(dict(random=float((expected.mean()-expected.min())/gap) if gap>0 else None,
           random_actual=float((actual.mean()-actual.min())/agap) if agap>0 else None,
           myopic=float((expected[chosen]-expected.min())/gap) if gap>0 else None,
           myopic_actual=float((actual[chosen]-actual.min())/agap) if agap>0 else None))
        for arm in arms:
            a=row['arms'][arm];values=neural['cost'][:,:,h] if arm=='learned' else data[arm+'_cost'][:,:,h]
            valid=neural['valid'] if arm=='learned' else np.ones(256,dtype=bool)
            choices=[];correct=[]
            for m in BUDGETS:
                keep=valid[:m];n=int(keep.sum());k=int(values[:,:m][:,keep].mean(1).argmin()) if n else None
                choices.append(k);correct.append(n>=m/2 and k==e['best'])
            a['correct'].append(correct);k=choices[3]
            a['regret'].append(float((expected[k]-expected.min())/gap) if k is not None and gap>0 else None)
            a['realized_regret'].append(float((actual[k]-actual.min())/agap) if k is not None and agap>0 else None)
            snap=neural['mean_snap'][:,h] if arm=='learned' else data[arm+'_mean_snap'][:,h]
            true=target['neural_target'][:,h] if arm=='learned' else target['actual_snap'][:,h]
            score=acc(snap.reshape(6,-1),true.reshape(6,-1),climate) if valid[:64].any() else np.full(6,np.nan)
            a['acc'].append([float(x) if np.isfinite(x) else None for x in score])
            if valid.any():
                means=values[:,valid].mean(1)
                a['response_differences'].append([float(means[j]-means[k]) for j in range(6) for k in range(j)])
            else:a['response_differences'].append(None)
        paired=data['paired_cost'][:,:,h];commit=None
        import time
        begin=time.time()
        for look,m in enumerate(BUDGETS):
            leader=int(paired[:,:m].mean(1).argmin());ind=rng('arm',1,3,c,member=m).integers(m,size=(1000,m))
            lower=[np.quantile((paired[j,:m]-paired[leader,:m])[ind].mean(1),.05/(6*5)) for j in range(6) if j!=leader]
            if all(x>0 for x in lower):
                commit=dict(members=m,error=leader!=e['best'],chosen=leader,
                            wall_seconds=float(data['paired_solver_cumulative_seconds'][look])+time.time()-begin)
                break
        row['commitment'].append(commit)
    if neural is not None:row['dropped']=int((~neural['valid']).sum())
    return row

def main(workers):
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as pool:cases=list(pool.map(one_case,range(30)))
    horizons=[]
    for h,T in enumerate(GRID):
        selected=[r for r in cases if r['eligible'][h]];n=len(selected)
        record=dict(T=float(T),eligible=n,total=30,sufficient=n>=15,near_ties=30-n,arms={})
        common_arms=set.intersection(*(set(r['arms']) for r in cases))
        for arm in sorted(common_arms):
            accuracy=np.mean([r['arms'][arm]['correct'][h] for r in selected],axis=0).tolist() if n else [None]*6
            pairs=[r for r in cases if r['arms'][arm]['response_differences'][h] is not None]
            df=np.asarray([r['arms'][arm]['response_differences'][h] for r in pairs]).reshape(-1)
            dt=np.asarray([r['truth_differences'][h] for r in pairs]).reshape(-1)
            record['arms'][arm]=dict(accuracy=accuracy,M95=m95(accuracy) if n else None,
                ACC=mean_available([v for r in cases for v in r['arms'][arm]['acc'][h]]),
                normalized_regret=mean_available([r['arms'][arm]['regret'][h] for r in selected]),
                realized_regret=mean_available([r['arms'][arm]['realized_regret'][h] for r in selected]),
                response_correlation=float(np.corrcoef(df,dt)[0,1]) if len(df)>1 and np.std(df)>0 and np.std(dt)>0 else None,
                response_relative_error=float(np.linalg.norm(df-dt)/np.linalg.norm(dt)) if np.linalg.norm(dt)>0 else None)
        record['member_criterion']=member_reading(record['arms']['paired']['M95'],record['arms']['unpaired']['M95'])
        committed=[r['commitment'][h] for r in cases if r['commitment'][h] is not None]
        scored=[r['commitment'][h] for r in selected if r['commitment'][h] is not None]
        record['commitment']=dict(committed=len(committed),uncommitted=30-len(committed),eligible_committed=len(scored),
             mean_members=mean_available([v['members'] for v in committed]),error_rate=mean_available([v['error'] for v in scored]),
             mean_wall_seconds=mean_available([v['wall_seconds'] for v in committed]),
             wall_time_basis='measured cumulative paired cohorts, sharing all horizons, plus interval analysis')
        record['myopic_accuracy']=mean_available([r['myopic_correct'][h] for r in selected]);record['random_accuracy_expected']=1/6
        record['null_regrets']={k:mean_available([r['null_regrets'][h][k] for r in selected]) for k in cases[0]['null_regrets'][h]}
        horizons.append(record)
    tf=next((r['T'] for r in horizons if r['arms']['paired']['ACC'] is not None and r['arms']['paired']['ACC']<.2),None)
    td=None
    if tf is not None:
        for r in horizons:
            if r['T']<tf:continue
            if not r['sufficient'] or r['arms']['paired']['accuracy'][3]<.8:break
            td=r['T']
    out=dict(system='Kolmogorov',Tf=tf,Td=td,horizons=horizons,git_sha=sha(),learned_arm_pending='learned' not in horizons[0]['arms'])
    if not out['learned_arm_pending']:out['learned_stability']=dict(attempted_members=30*256,dropped=sum(r['dropped'] for r in cases),per_case=[r['dropped'] for r in cases])
    write_json(ROOT/'results/kolmo_solver_statistics.json',out)
    write_json(ROOT/'runs/kolmo/test/case_statistics.json',dict(cases=cases,git_sha=sha()))
    print('Kolmo statistics Tf=',tf,'Td=',td,flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--workers',type=int,default=16);main(p.parse_args().workers)
