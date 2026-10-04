"""Add learned and null diagnostics without recomputing truth eligibility."""
import json
import numpy as np
from common import ROOT,GRID,BUDGETS,m95,write_json,sha
from analyze_l96 import acc

def mean_available(values):
    values=[float(v) for v in values if v is not None and np.isfinite(v)]
    return float(np.mean(values)) if values else None

def main():
    root=ROOT/'runs/l96/test'
    report=json.loads((ROOT/'results/l96_solver_statistics.json').read_text())
    cases=json.loads((root/'case_statistics.json').read_text())['cases']
    learned=all((root/f'neural_{c:03d}.npz').exists() for c in range(200))
    climate=np.load(root/'climatology.npy')
    arrays=[dict(correct=[],acc=[],regret=[],realized=[],diff=[],drop=[]) for _ in GRID]
    nulls=[dict(random=[],random_actual=[],myopic=[],myopic_actual=[]) for _ in GRID]
    truthdiff=[[] for _ in GRID]
    drops=[]
    for c,row in enumerate(cases):
        data=np.load(root/f'case_{c:03d}.npz')
        chosen=json.loads((root/f'myopic_{c:03d}.json').read_text())['chosen']
        if learned:
            net=np.load(root/f'neural_{c:03d}.npz')
            valid=net['valid'];drops.append(int((~valid).sum()))
            target=np.load(root/f'neural_target_{c:03d}.npy')
        for h,T in enumerate(GRID):
            expected=data['truth_cost'][:,:,h].mean(1);actual=data['actual_cost'][:,h]
            gap=np.ptp(expected);rgap=np.ptp(actual)
            if row['eligible'][h]:
                nulls[h]['random'].append(float((expected.mean()-expected.min())/gap) if gap>0 else None)
                nulls[h]['random_actual'].append(float((actual.mean()-actual.min())/rgap) if rgap>0 else None)
                nulls[h]['myopic'].append(float((expected[chosen]-expected.min())/gap) if gap>0 else None)
                nulls[h]['myopic_actual'].append(float((actual[chosen]-actual.min())/rgap) if rgap>0 else None)
            if not learned:continue
            costs=net['cost'][:,:,h]
            selections=[];correct=[]
            for m in BUDGETS:
                keep=valid[:m];n=int(keep.sum())
                k=int(costs[:,:m][:,keep].mean(1).argmin()) if n else None
                selections.append(k)
                correct.append(n>=m/2 and k==row['best'][h])
            if row['eligible'][h]:arrays[h]['correct'].append(correct)
            keep=valid[:64];k=selections[3]
            if row['eligible'][h]:
                arrays[h]['regret'].append(float((expected[k]-expected.min())/gap) if k is not None and gap>0 else None)
                arrays[h]['realized'].append(float((actual[k]-actual.min())/rgap) if k is not None and rgap>0 else None)
            if keep.any():arrays[h]['acc'].extend(acc(net['mean_snap'][:,h],target[:,h],climate).tolist())
            if valid.any():
                means=costs[:,valid].mean(1)
                arrays[h]['diff'].extend([float(means[j]-means[k]) for j in range(8) for k in range(j)])
                truthdiff[h].extend([float(expected[j]-expected[k]) for j in range(8) for k in range(j)])
            arrays[h]['drop'].append(int((~keep).sum()))
    for h,record in enumerate(report['horizons']):
        record['null_regrets']={k:mean_available(v) for k,v in nulls[h].items()}
        if not learned:continue
        a=arrays[h];accuracy=np.mean(a['correct'],axis=0).tolist() if a['correct'] else [None]*6
        df=np.asarray(a['diff']);dt=np.asarray(truthdiff[h])
        record['arms']['learned']=dict(accuracy=accuracy,M95=m95(accuracy) if a['correct'] else None,
            ACC=mean_available(a['acc']) if len(a['acc'])==200*8 and np.isfinite(a['acc']).all() else None,normalized_regret=mean_available(a['regret']),
            realized_regret=mean_available(a['realized']),
            response_correlation=float(np.corrcoef(df,dt)[0,1]) if len(df)>1 and np.std(df)>0 and np.std(dt)>0 else None,
            response_relative_error=float(np.linalg.norm(df-dt)/np.linalg.norm(dt)) if np.linalg.norm(dt)>0 else None,
            mean_dropped_first64=float(np.mean(a['drop'])),unavailable_forecast_cases=200-len(a['acc'])//8)
    report['learned_arm_pending']=not learned
    if learned:report['learned_stability']=dict(attempted_members=200*256,dropped=sum(drops),per_case=drops)
    report['diagnostics_source_sha']=sha()
    write_json(ROOT/'results/l96_solver_statistics.json',report)
    print('L96 diagnostics enriched; learned complete:',learned,flush=True)

if __name__=='__main__':main()
