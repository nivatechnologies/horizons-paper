"""Uniform branch forcing traces and direct saved-cost errors; no realized files."""
import argparse,hashlib,json,socket,sys
from pathlib import Path
import numpy as np

def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def traces(outputs,inputs):
 results={};executions={}
 for folder in sorted((outputs/'inference').iterdir()):
  execution=json.loads((folder/'complete.json').read_text());executions[folder.name]=execution
  stats=[];invalid=[]
  for c in range(200):
   p=folder/f'{c:03d}.npz';assert digest(p)==execution['output_hashes'][p.name]
   with np.load(p) as z:estimate=z['estimated_F'].copy();valid=z['valid'].copy();options=z['options'].copy();steps=z['steps'].copy()
   with np.load(inputs/f'{c:03d}.npz') as z:F=z['F'].copy()
   if not valid.all() or not np.isfinite(estimate).all():invalid.append(c)
   target=F[:,None,None]-(.16 if execution['kind']=='E0' else 0.)
   error=estimate.mean(0)-target
   stats.append(dict(n=len(F),MSE=(error*error).mean(0),bias=error.mean(0),estimate=estimate.mean(axis=(0,1)),forcing=float(F.mean())))
  if invalid:
   results[folder.name]=dict(evaluable=False,invalid_cases=invalid,rows=[],no_survivor_conditioning=True);continue
  mse=np.asarray([x['MSE'] for x in stats]);bias=np.asarray([x['bias'] for x in stats]);n=np.asarray([x['n'] for x in stats]);est=np.asarray([x['estimate'] for x in stats]);rows=[]
  for b,option in enumerate(options):
   for t,step in enumerate(steps):
    rows.append(dict(option=int(option),step=int(step),reference='draw F minus action amplitude' if execution['kind']=='E0' else 'draw F',equal_case_estimate=float(est[:,b,t].mean()),pooled_estimate=float(np.average(est[:,b,t],weights=n)),equal_case_estimate_minus_reference=float(bias[:,b,t].mean()),pooled_estimate_minus_reference=float(np.average(bias[:,b,t],weights=n)),equal_case_RMSE=float(np.sqrt(mse[:,b,t]).mean()),pooled_RMSE=float(np.sqrt(np.average(mse[:,b,t],weights=n))),case_RMSE_median=float(np.median(np.sqrt(mse[:,b,t])))))
  results[folder.name]=dict(evaluable=True,rows=rows,invalid_cases=[],cases=len(stats),draws=int(n.sum()))
 return dict(rows=results,executions=executions)

def direct_costs(a):
 if socket.gethostname()!='sulaco':raise RuntimeError('Saved-cost analysis requires sulaco CPU')
 sys.path.insert(0,str(a.science_root))
 from acd_stage6_analysis import RAW,LEADS
 specs=[('posterior',None)]+[(n,a.science_root/'runs/stage9/inference'/n) for n in ['CNN-20k','CNN-F','CNN-noF']]
 specs += [(f'{m}-seed{i}',a.science_root/'runs/stage9/inference'/f'{m}-seed{i}') for i in range(1,5) for m in ['CNN-F','CNN-noF']]
 specs += [(f'CNN-F-{e}-{mode}-seed{i}',a.stage18/'runs/stage18/inference'/f'CNN-F-{e}-{mode}-seed{i}') for e,mode in [('E0','fixed'),('E1','fixed'),('E1','rolling')] for i in range(1,6)]
 specs += [(f'CNN-F-E0-{mode}-seed{i}-Spark',a.stage20_c/'inference'/f'CNN-F-E0-{mode}-seed{i}') for mode in ['fixed','rolling'] for i in range(1,6)]
 results={}
 for name,directory in specs:
  cases=[];sources={};invalid=[]
  for c in range(200):
   p=RAW/f'conf/case_{c:03d}.npz'
   with np.load(p) as z:physical=z['J'].copy();exclude=bool(z['excluded'])
   if directory is None:j=physical
   else:
    source=directory/f'{c:03d}.npz';sources[str(source)]=digest(source)
    with np.load(source) as z:j=z['J'].copy();valid=bool(z['valid'].all()) and np.isfinite(j).all()
    if not valid:invalid.append(c)
   assert j.shape==physical.shape
   if exclude:continue
   error=(j[:,0]-j[:,8])-(physical[:,0]-physical[:,8]);cases.append(dict(n=len(error),bias=error.mean(0),MSE=(error*error).mean(0)))
  finite=all(np.isfinite(x['bias']).all() and np.isfinite(x['MSE']).all() for x in cases)
  n=np.asarray([x['n'] for x in cases]);b=np.asarray([x['bias'] for x in cases]);m=np.asarray([x['MSE'] for x in cases])
  rows=[dict(lead=float(lead),population='uniform_decrease_only',equal_case_Dk_bias=float(b[:,t].mean()) if finite else None,pooled_Dk_bias=float(np.average(b[:,t],weights=n)) if finite else None,equal_case_Dk_RMSE=float(np.sqrt(m[:,t]).mean()) if finite else None,pooled_Dk_RMSE=float(np.sqrt(np.average(m[:,t],weights=n))) if finite else None) for t,lead in enumerate(LEADS)]
  results[name]=dict(rows=rows,cases=len(cases),invalid_cases=invalid,source_hashes=sources,no_survivor_conditioning=True)
 a.receipt.write_text(json.dumps(dict(models=results,adapter_sha256=digest(__file__),no_realized_outcomes_opened=True),indent=2,allow_nan=False)+'\n')

def aggregate(a):
 e0=traces(a.outputs/'E0',a.inputs);e1=traces(a.outputs/'E1',a.inputs);costs=json.loads(a.costs.read_text());original=json.loads(a.base_receipt.read_text())
 result=dict(post_hoc=True,panel='original confirmation',licenses_frozen_route=False,E0_uniform=e0,E1_rolling_branches=e1,direct_uniform_cost_errors=costs,amendment_sha256=digest(Path(__file__).parent/'ACD_STAGE20_B_UNIFORM_AMENDMENT.md'),weighting='Five E0 estimators averaged per draw before errors; equal-case averages case biases and case RMSEs. Pooled metrics weight every retained draw equally. E1 is reported per seed on both branches against draw F. Any invalid instance is reported; no survivors are used.',interpretation='Physics is the floor for a correct uniform-decrease trajectory; CNN-F is the control. Differences against F minus action amplitude measure what the estimator reads, rather than asserting a known effective forcing.')
 a.receipt.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 fig,axes=plt.subplots(1,2,figsize=(10,4));styles={'physics':('-',None,'0.3'),'CNN-F':('-.','^','0.15'),'CNN-noF':((0,(8,2,1,2)),'D','0')}
 for ax in axes:ax.axvline(11,color='.5',linestyle=':',linewidth=1);ax.set_xlabel('Rollout step')
 for name,(style,marker,color) in styles.items():
  left=np.asarray([r['equal_case_RMSE'] for r in original['rows'][name]])
  right=np.asarray([r['equal_case_estimate_minus_reference'] for r in e0['rows'][name]['rows']])
  for ax,y in zip(axes,[left,right]):ax.plot(np.arange(len(y)),y,linestyle=style,marker=marker,markevery=6,color=color,label=name,linewidth=1 if name=='physics' else 1.5)
  if name!='physics':
   names=[name]+[f'{name}-seed{i}' for i in range(1,5)]
   for ax,values in [(axes[0],np.asarray([[r['equal_case_RMSE'] for r in original['rows'][n]] for n in names])),(axes[1],np.asarray([[r['equal_case_estimate_minus_reference'] for r in e0['rows'][n]['rows']] for n in names]))]:ax.fill_between(np.arange(values.shape[1]),values.min(0),values.max(0),facecolor='none',edgecolor=color,hatch='///' if name=='CNN-F' else '\\\\',linewidth=.4,alpha=.5)
 axes[0].set_ylabel('E0 forcing-estimate RMSE');axes[0].set_title('No action');axes[1].set_ylabel('E0 estimate minus (F − a)');axes[1].set_title('Uniform decrease');axes[1].axhline(0,color='.5',linestyle=':',linewidth=.7);axes[0].legend(frameon=False);fig.tight_layout()
 for ext in ['pdf','png']:fig.savefig(a.figures/f'F22_readability_paper.{ext}',dpi=180)
 plt.close(fig)
 lines=['','## B extension — uniform-decrease readability','','Post hoc; original panel only. Physics is the floor and CNN-F is the control. No realized outcomes are read. Equal-case biases average the per-instance draw means; pooled biases weight every draw equally. Five E0 estimates are averaged before their errors. E1 is traced against draw F on both uniform and no-action branches at every step. Direct uniform Dk errors use saved cost arrays, without subtraction of group statistics.','','| Model | Lead | Uniform D bias (equal case) | Uniform D RMSE (equal case) | Pooled bias | Pooled RMSE |','|---|---:|---:|---:|---:|---:|']
 for name,m in costs['models'].items():
  for r in m['rows']:lines.append('| '+name+' | '+' | '.join(str(r[k]) for k in ['lead','equal_case_Dk_bias','equal_case_Dk_RMSE','pooled_Dk_bias','pooled_Dk_RMSE'])+' |')
 lines+=['','Every forcing step and branch is reported in receipts/acd_stage20_B_uniform.json. Hatched bands show the five training runs; markers and line styles distinguish models.']
 a.reading.write_text(a.reading.read_text()+'\n'.join(lines)+'\n')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('mode',choices=['costs','aggregate']);p.add_argument('--science-root',type=Path);p.add_argument('--stage18',type=Path);p.add_argument('--stage20-c',type=Path);p.add_argument('--outputs',type=Path);p.add_argument('--inputs',type=Path);p.add_argument('--costs',type=Path);p.add_argument('--base-receipt',type=Path);p.add_argument('--receipt',type=Path,required=True);p.add_argument('--figures',type=Path);p.add_argument('--reading',type=Path);a=p.parse_args();direct_costs(a) if a.mode=='costs' else aggregate(a)
