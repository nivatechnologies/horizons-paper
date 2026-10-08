"""Aggregate original-panel forcing readability; no outcome access."""
import argparse, hashlib, json
from pathlib import Path
import numpy as np

def run(args):
    rows={};executions={};case_values={};source_hashes={}
    for folder in sorted((args.outputs/'inference').iterdir()):
        complete=folder/'complete.json'
        if not complete.exists():raise RuntimeError('Missing complete output '+str(folder))
        execution=json.loads(complete.read_text());executions[folder.name]=execution
        models=[];per_seed=[];invalid=[]
        for case in range(200):
            p=folder/f'{case:03d}.npz'
            if hashlib.sha256(p.read_bytes()).hexdigest()!=execution['output_hashes'][p.name]:raise RuntimeError('Output hash mismatch')
            with np.load(p) as d:est=d['estimated_F'].copy();valid=d['valid'].copy()
            with np.load(args.inputs/f'{case:03d}.npz') as d:forcing=d['F'].copy()
            if not valid.all() or not np.isfinite(est).all():invalid.append(case)
            error=est.mean(0)-forcing[:,None];e=est-forcing[None,:,None]
            models.append(dict(n=len(forcing),MSE=(error**2).mean(0),bias=error.mean(0)))
            per_seed.append(dict(MSE=(e**2).mean(1),bias=e.mean(1)))
        if invalid:raise RuntimeError('Invalid original-panel readability instances; no survivor conditioning: '+str(invalid))
        mse=np.array([r['MSE'] for r in models]);bias=np.array([r['bias'] for r in models]);n=np.array([r['n'] for r in models]);root=np.sqrt(mse)
        eq=root.mean(0);po=np.sqrt(np.average(mse,axis=0,weights=n));b=bias.mean(0);pb=np.average(bias,axis=0,weights=n)
        seeds=np.sqrt(np.array([r['MSE'] for r in per_seed])).mean(0)
        rows[folder.name]=[dict(step=s,equal_case_RMSE=float(eq[s]),pooled_RMSE=float(po[s]),equal_case_bias=float(b[s]),pooled_bias=float(pb[s]),case_RMSE_median=float(np.median(root[:,s])),case_RMSE_q25=float(np.quantile(root[:,s],.25)),case_RMSE_q75=float(np.quantile(root[:,s],.75))) for s in range(len(eq))]
        case_values[folder.name]=dict(E0_seed_equal_case_RMSE=seeds.tolist())
    physics=np.array([r['equal_case_RMSE'] for r in rows['physics']]);control=np.array([r['equal_case_RMSE'] for r in rows['CNN-F']]);departures={}
    def first(a,b,multiple):
        x=np.flatnonzero(a>multiple*b);return int(x[0]) if len(x) else None
    for name,readings in rows.items():
        rmse=np.array([r['equal_case_RMSE'] for r in readings])
        departures[name]=dict(first_step_above_twice_physics=first(rmse,physics,2),first_step_above_CNN_F=first(rmse,control,1),first_step_above_twice_CNN_F=first(rmse,control,2))
    result=dict(post_hoc=True,panel='original confirmation',licenses_frozen_route=False,rows=rows,departures=departures,
        E0_seed_readings=case_values,executions=executions,
        weighting='Five E0 estimates are averaged per draw before errors. Equal-case RMSE is the mean of per-instance RMSE; pooled RMSE pools squared errors across draws. Case median summarizes per-instance RMSE. Training-run ranges are separate from estimator variation.',
        interpretation='Physics is the floor and own-forcing CNN-F is the control. Twice-baseline departures are descriptive thresholds, not tests of a causal mechanism; complete step series are reported.',
        adapter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    args.receipt.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(figsize=(10,4));styles={'physics':('-',None,'0.3'),'CNN-F':('-.','^','0.15'),'CNN-noF':((0,(8,2,1,2)),'D','0.0')}
    for name,(line,marker,color) in styles.items():
        y=np.array([r['equal_case_RMSE'] for r in rows[name]]);ax.plot(np.arange(len(y)),y,linestyle=line,marker=marker,markevery=6,color=color,label=name,linewidth=1 if name=='physics' else 1.5)
        seeds=[name]+[f'{name}-seed{i}' for i in range(1,5)] if name!='physics' else []
        if seeds:
            v=np.array([[r['equal_case_RMSE'] for r in rows[n]] for n in seeds]);ax.fill_between(np.arange(v.shape[1]),v.min(0),v.max(0),facecolor='none',edgecolor=color,hatch='///' if name=='CNN-F' else '\\\\',linewidth=.4,alpha=.5)
    ax.axvline(11,color='0.5',linestyle=':',linewidth=1);ax.set(xlabel='Rollout step',ylabel='E0 forcing-estimate RMSE');ax.legend(frameon=False);fig.tight_layout()
    args.figures.mkdir(parents=True,exist_ok=True)
    for ext in ['pdf','png']:fig.savefig(args.figures/f'F22_readability_paper.{ext}',dpi=180)
    plt.close(fig)
    lines=['','## B — forcing readability along each own rollout','','Physics is the floor and CNN-F with its own forcing is the control. All E0 estimators are unchanged. No realized outcomes are read. Hatched bands show training-run ranges, including the retained model.','','Equal-case RMSE averages instance RMSEs; pooled RMSE pools all squared draw errors. The receipt reports every step, biases and case medians. Departure below uses twice the comparator RMSE and is descriptive.','','| Model | First step above twice physics | First step above twice retained CNN-F |','|---|---:|---:|']
    for name,r in departures.items():lines.append(f"| {name} | {r['first_step_above_twice_physics']} | {r['first_step_above_twice_CNN_F']} |")
    args.reading.write_text(args.reading.read_text()+'\n'.join(lines)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--outputs',type=Path,required=True);p.add_argument('--inputs',type=Path,required=True);p.add_argument('--receipt',type=Path,required=True);p.add_argument('--reading',type=Path,required=True);p.add_argument('--figures',type=Path,required=True);run(p.parse_args())
