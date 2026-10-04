"""Compute explicit frozen statistics from raw per-case solver evidence."""
import argparse
import concurrent.futures
import json
import multiprocessing
import time
import numpy as np
from common import ROOT,GRID,BUDGETS,eligible,rng,m95,member_reading,write_json,sha

def acc(pred,target,mean):
    a=pred-mean;b=target-mean
    fa=np.sum(a*a,axis=-1);ob=np.sum(b*b,axis=-1)
    cross=np.sum(a*b,axis=-1)
    ans=np.zeros_like(fa)
    ans[ob<=0]=np.nan
    # The frozen threshold is on norms; these quantities are squared norms.
    use=(ob>0)&(fa>0)&(fa>=1e-24*ob)
    ans[use]=cross[use]/np.sqrt(fa[use]*ob[use])
    return ans

def one_case(c):
    begin=time.time();root=ROOT/'runs/l96/test'
    data=np.load(root/f'case_{c:03d}.npz')
    climate=np.load(root/'climatology.npy')[:,None]
    truth=data['truth_cost']
    result=dict(case=c,eligible=[],best=[],arms={},commitment=[])
    arms=['paired','unpaired','jitter','misidentified']
    for arm in arms:
        result['arms'][arm]=dict(correct=[],regret=[],realized_regret=[],acc=[],response_differences=[])
    for h,T in enumerate(GRID):
        e=eligible(truth[:,:,h],'truth',0,c)
        result['eligible'].append(e['eligible']);result['best'].append(e['best'])
        expected=truth[:,:,h].mean(1)
        actual=data['actual_cost'][:,h]
        gap=expected.max()-expected.min();actualgap=actual.max()-actual.min()
        for arm in arms:
            costs=data[arm+'_cost'][:,:,h]
            selections=[int(costs[:,:m].mean(1).argmin()) for m in BUDGETS]
            result['arms'][arm]['correct'].append([k==e['best'] for k in selections])
            k=selections[3]
            result['arms'][arm]['regret'].append(float((expected[k]-expected.min())/gap) if gap>0 else None)
            result['arms'][arm]['realized_regret'].append(float((actual[k]-actual.min())/actualgap) if actualgap>0 else None)
            score=acc(data[arm+'_mean_snap'][:,h],data['actual_snap'][:,h],climate[:,0])
            result['arms'][arm]['acc'].append(score.tolist())
            means=costs.mean(1)
            result['arms'][arm]['response_differences'].append([float(means[j]-means[k]) for j in range(8) for k in range(j)])
        result.setdefault('truth_differences',[]).append([float(expected[j]-expected[k]) for j in range(8) for k in range(j)])
        result.setdefault('myopic_correct',[]).append(None)
        # The myopic costs are added by the separate frozen [0,1 LT] null runner.
        myopic_path=root/f'myopic_{c:03d}.json'
        if myopic_path.exists():
            k=json.loads(myopic_path.read_text())['chosen']
            result['myopic_correct'][-1]=k==e['best']
        else:
            result['myopic_correct'][-1]=None
        committed=None
        paired=data['paired_cost'][:,:,h]
        commitment_seconds=0.
        for look,m in enumerate(BUDGETS):
            tick=time.time()
            leader=int(paired[:,:m].mean(1).argmin())
            ind=rng('arm',0,3,c,member=m).integers(m,size=(1000,m))
            lower=[]
            for j in range(8):
                if j!=leader:
                    samples=(paired[j,:m]-paired[leader,:m])[ind].mean(1)
                    lower.append(float(np.quantile(samples,.05/(6*7))))
            commitment_seconds+=time.time()-tick
            if all(v>0 for v in lower):
                committed=dict(members=m,chosen=leader,error=leader!=e['best'],
                               interval_analysis_seconds=commitment_seconds)
                break
        result['commitment'].append(committed)
    result['seconds']=time.time()-begin
    profile=root/f'profile_{c:03d}.json'
    if profile.exists():
        timing=json.loads(profile.read_text())['cumulative_solver_seconds']
        result['solver_seconds_by_budget']=timing
        for committed in result['commitment']:
            if committed is not None:
                committed['wall_seconds']=timing[str(committed['members'])]+committed['interval_analysis_seconds']
    return result

def main(workers):
    begin=time.time();context=multiprocessing.get_context('spawn')
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers,mp_context=context) as pool:
        rows=list(pool.map(one_case,range(200)))
    eligible_array=np.array([r['eligible'] for r in rows])
    horizon_rows=[]
    for h,T in enumerate(GRID):
        mask=eligible_array[:,h];n=int(mask.sum())
        record=dict(T=float(T),eligible=n,total=200,sufficient=n>=100,near_ties=200-n,arms={})
        for arm in rows[0]['arms']:
            correct=np.array([r['arms'][arm]['correct'][h] for r in rows])
            accuracy=correct[mask].mean(0).tolist() if n else [None]*6
            df=np.array([r['arms'][arm]['response_differences'][h] for r in rows]).reshape(-1)
            dt=np.array([r['truth_differences'][h] for r in rows]).reshape(-1)
            correlation=float(np.corrcoef(df,dt)[0,1]) if np.std(df)>0 and np.std(dt)>0 else None
            rel=float(np.linalg.norm(df-dt)/np.linalg.norm(dt)) if np.linalg.norm(dt)>0 else None
            record['arms'][arm]=dict(accuracy=accuracy,M95=m95(accuracy) if n else None,
                 ACC=float(np.mean([r['arms'][arm]['acc'][h] for r in rows])),
                 normalized_regret=float(np.mean([r['arms'][arm]['regret'][h] for r in rows if r['eligible'][h]])) if n else None,
                 realized_regret=float(np.mean([r['arms'][arm]['realized_regret'][h] for r in rows if r['eligible'][h]])) if n else None,
                 response_correlation=correlation,response_relative_error=rel)
        record['member_criterion']=member_reading(record['arms']['paired']['M95'],record['arms']['unpaired']['M95'])
        committed=[r['commitment'][h] for r in rows if r['commitment'][h] is not None]
        eligible_committed=[r['commitment'][h] for r in rows if r['eligible'][h] and r['commitment'][h] is not None]
        record['commitment']=dict(committed=len(committed),uncommitted=200-len(committed),
                  mean_members=float(np.mean([v['members'] for v in committed])) if committed else None,
                  eligible_committed=len(eligible_committed),error_rate=float(np.mean([v['error'] for v in eligible_committed])) if eligible_committed else None,
                  mean_wall_seconds=float(np.mean([v['wall_seconds'] for v in committed])) if committed and all('wall_seconds' in v for v in committed) else None,
                  wall_time_basis='measured nested-cohort solver costs through commitment, sharing all horizons, plus measured interval-analysis time')
        vals=[r['myopic_correct'][h] for r in rows if r['eligible'][h] and r['myopic_correct'][h] is not None]
        record['myopic_accuracy']=float(np.mean(vals)) if len(vals)==n and n else None
        record['random_accuracy_expected']=1/8
        horizon_rows.append(record)
    tf=next((r['T'] for r in horizon_rows if r['arms']['paired']['ACC']<.2),None)
    td=None
    if tf is not None:
        for row in horizon_rows:
            if row['T']<tf:continue
            if not row['sufficient'] or row['arms']['paired']['accuracy'][3]<.8:break
            td=row['T']
    out=ROOT/'results';out.mkdir(exist_ok=True)
    write_json(out/'l96_solver_statistics.json',dict(system='Lorenz-96',Tf=tf,Td=td,horizons=horizon_rows,
               seconds=time.time()-begin,git_sha=sha(),learned_arm_pending=True))
    write_json(ROOT/'runs/l96/test/case_statistics.json',dict(cases=rows,git_sha=sha()))
    print('L96 solver statistics Tf=',tf,'Td=',td,flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--workers',type=int,default=16)
    main(p.parse_args().workers)
