"""CPU validation-only L* worker; no imports or paths for test panels."""
import argparse,datetime,json
from pathlib import Path
import numpy as np

def main(inputs,out):
    configuration=json.loads((inputs/'configuration.json').read_text())
    for pair in configuration.get('initializer_proofs',[]):
        import torch
        base=torch.load(inputs/pair['base'],map_location='cpu',weights_only=True)
        initial=torch.load(inputs/pair['initial'],map_location='cpu',weights_only=True)
        if base['sigma']!=initial['sigma'] or base['state_dict'].keys()!=initial['state_dict'].keys():
            raise RuntimeError('initialization metadata mismatch')
        if not all(torch.equal(base['state_dict'][k],initial['state_dict'][k]) for k in base['state_dict']):
            raise RuntimeError('initialization state differs from baseline')
    d=np.load(inputs/'validation_inputs.npz')
    skill=np.load(inputs/'skill_inputs.npz')
    truth=d['truth'];sj=float(np.median(np.ptp(truth,axis=1)))
    if not np.isfinite(sj) or sj<=0:raise RuntimeError('validation S_J unavailable')
    eligible=skill['eligible'];actual=skill['actual'];climate=skill['climate'];sigma=float(skill['sigma'])
    records={}
    for name in configuration['S']:
        prediction=np.load(inputs/(name+'.npz'))
        keep=prediction['survivors'];failed=keep.sum(1)<32
        costs=prediction['cost'];choice=costs.argmin(1)
        regrets=(truth[np.arange(len(truth)),choice]-truth.min(1))/sj
        regrets[failed]=np.ptp(truth[failed],axis=1)/sj
        means=prediction['mean_window']
        a=means-climate[None,:,None,:];b=actual-climate[None,:,None,:]
        fa=np.sum(a*a,axis=-1);ob=np.sum(b*b,axis=-1)
        acc=np.zeros_like(fa);acc[ob<=0]=np.nan
        valid=(ob>0)&(fa>0)&(fa>=1e-24*ob)
        acc[valid]=np.sum(a*b,axis=-1)[valid]/np.sqrt(fa[valid]*ob[valid])
        wacc=acc.mean(axis=(1,2));wacc[failed]=0.
        rmse=np.sqrt(np.mean((means-actual)**2,axis=-1)).mean(axis=(1,2))/sigma
        eligible_wacc=float(wacc[eligible].mean()) if eligible.any() else None
        rmse_mask=eligible&~failed
        eligible_rmse=float(rmse[rmse_mask].mean()) if rmse_mask.any() else None
        if eligible_wacc is not None and not np.isfinite(eligible_wacc):eligible_wacc=None
        if eligible_rmse is not None and not np.isfinite(eligible_rmse):eligible_rmse=None
        records[name]=dict(mean_normalized_regret=float(regrets.mean()),wACC=eligible_wacc,wRMSE=eligible_rmse,
                           eligible_cases=int(eligible.sum()),failed_cases=int(failed.sum()),dropped_members=int((~keep).sum()),
                           all_case_wACC=float(wacc.mean()),
                           all_case_wRMSE=float(rmse[~failed].mean()) if (~failed).any() else None)
    best=min(r['mean_normalized_regret'] for r in records.values())
    tied=[n for n,r in records.items() if r['mean_normalized_regret']==best]
    if len(tied)>1:
        if any(records[n]['wACC'] is None for n in tied):raise RuntimeError('unavailable validation ACC needed for exact tie')
        best_acc=max(records[n]['wACC'] for n in tied);tied=[n for n in tied if records[n]['wACC']==best_acc]
    if len(tied)>1:
        if any(records[n]['wRMSE'] is None for n in tied):raise RuntimeError('unavailable validation RMSE needed for exact tie')
        best_rmse=min(records[n]['wRMSE'] for n in tied);tied=[n for n in tied if records[n]['wRMSE']==best_rmse]
    selected=min(tied,key=configuration['order'].index)
    completed=datetime.datetime.now(datetime.timezone.utc).isoformat()
    result=dict(status='FINAL',system=configuration['system'],selected_L=selected,selection_completed_at=completed,
                S=configuration['S'],models=configuration['models'],cuts=configuration['cuts'],not_run=configuration['not_run'],
                compute_manifest=configuration.get('compute_manifest'),
                rule='all-case mean normalized regret; higher eligible-case wACC; lower eligible-case wRMSE; frozen order',
                isolation='bubblewrap: only validation inputs, validation predictions and selected source exposed')
    out.mkdir(parents=True,exist_ok=True)
    evidence=dict(system=configuration['system'],selection_completed_at=completed,selected_L=selected,
                  validation_S_J=sj,records=records,input_hashes=configuration['input_hashes'])
    for filename,payload in [('final_selection.json',result),('selection_evidence.json',evidence)]:
        tmp=out/(filename+'.tmp');tmp.write_text(json.dumps(payload,indent=2,allow_nan=False)+'\n');tmp.replace(out/filename)
    print(json.dumps(dict(status='FINAL',selected_L=selected,completed_at=completed)),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--inputs',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();main(a.inputs,a.out)
