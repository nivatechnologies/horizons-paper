"""Aggregate Stage16 runs without selection; separate run variation from case uncertainty."""
import hashlib,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
def get_metrics(d):
 out={}
 for row in d['confidence_readings']:
  lead=str(row['lead']);a=row['all_confident_accuracy'];fc=row['Fc_accuracy']
  vals=dict(S_confident_share=row['confident_S_share'],Fc_confident_share=row['confident_Fc_share'],Fc_case_accuracy=fc['case_accuracy'],Fc_pooled_accuracy=fc['answer_accuracy'],S_case_error=1-a['case_accuracy'],S_pooled_error=1-a['answer_accuracy'])
  for r in d['state_skill']:
   if r['lead']==row['lead']:vals.update(state_RMSE_over_sigma=r['window_mean_RMSE_over_sigma'],anomaly_correlation=r['window_mean_anomaly_correlation'])
  for r in d['pooled_per_draw_errors']:
   if r['lead']==row['lead'] and r['quantity'] in ['J8','Dk']:
    vals.update({r['quantity']+'_'+k:r[k] for k in ['RMSE','bias']})
  for r in d['comparisons']:
   if r['lead']==row['lead']:vals['seven_minus_Fc']=r['seven_minus_Fc']['point']
  for matched in d['matched_readings']:
   if matched['lead']==row['lead']:
    for test in matched['calibration_test']:
     vals['mean_calibration_error_threshold_'+str(test['threshold'])]=test['overconfidence_interval']['point']
  for r in d['matched_coverage'].get('rows',[]):
   if r['lead']==row['lead']:
    prefix=r['patterns']+'_coverage_'+str(r['target_coverage'])
    vals[prefix+'_pooled_error']=r['pooled_error']
    vals[prefix+'_case_error']=r['case_error']
  for r in d['decisions']:
   if r['lead']==row['lead']:vals.update({r['policy']+'_'+k:r[k] for k in ['mean_regret','capture_fraction','harms','acting_share']})
  out[lead]=vals
 out['paired_endpoint']=d['paired_endpoint_fixed_posterior_cohort']['interval']['point']
 return out

def main():
 freeze=json.loads((ROOT/'receipts/acd_stage16_freeze.json').read_text())
 runs=[]
 for model,name in [('CNN-F','CNN-F'),('CNN-noF','CNN-noF')]+[(r['model'],r['name']) for r in freeze['runs']]:
  tr=ROOT/f'runs/stage9_training/{name}/complete.json'
  mp=ROOT/f'runs/stage16/metrics_{name}.json'
  d=dict(model=model,name=name,baseline=name==model)
  if tr.exists():d['training']=json.loads(tr.read_text())
  elif name=='CNN-F':d['training']=json.loads((ROOT/'receipts/acd_stage9.json').read_text())['F']['CNN-F']
  else:
   exit_path=tr.parent/'queue_exit.json'
   if exit_path.exists():d['failure']=json.loads(exit_path.read_text())
  if mp.exists():d['metrics']=json.loads(mp.read_text());d['summary_metrics']=get_metrics(d['metrics']);d['status']='scored'
  else:d['status']='unavailable; no invented reading'
  runs.append(d)
 summaries={}
 for model in ['CNN-F','CNN-noF']:
  complete=[r['summary_metrics'] for r in runs if r['model']==model and 'summary_metrics' in r]
  result=dict(scored_runs=len(complete),planned_runs=sum(r['model']==model for r in runs),scope='descriptive training-run mean and range; separate from case-level bounds')
  if complete:
   for lead in ['2.0','3.0']:
    result[lead]={k:dict(mean=float(np.mean([r[lead][k] for r in complete])),min=float(min(r[lead][k] for r in complete)),max=float(max(r[lead][k] for r in complete))) for k in complete[0][lead]}
   values=[r['paired_endpoint'] for r in complete];result['paired_endpoint']=dict(mean=float(np.mean(values)),min=float(min(values)),max=float(max(values)))
  summaries[model]=result
 d=dict(post_hoc=True,licenses_frozen_route=False,selection_among_seeds=False,freeze_sha256=hashlib.sha256((ROOT/'receipts/acd_stage16_freeze.json').read_bytes()).hexdigest(),runs=runs,model_summaries=summaries)
 (ROOT/'receipts/acd_stage16.json').write_text(json.dumps(d,indent=2,allow_nan=False)+'\n')
 L=['# Stage16 training-seed replication','','Post hoc on confirmation; licenses no frozen route. Every run is reported. Means and ranges describe training-run variation; case-level betting bounds remain in the full receipt.','','| Run | Status | GPU seconds | Completed | Skipped | Selected step |','|---|---|---:|---:|---:|---:|']
 for r in runs:
  t=r.get('training',{});L.append('| '+' | '.join(map(str,[r['name'],r['status'],t.get('charged_gpu_seconds'),t.get('completed_updates',t.get('step')),t.get('skipped_updates','unguarded'),t.get('selected_step')]))+' |')
 L+=['','| Model | Lead | Quantity | Mean over scored runs | Minimum | Maximum |','|---|---:|---|---:|---:|---:|']
 for model,s in summaries.items():
  for lead in ['2.0','3.0']:
   for key,row in s.get(lead,{}).items():L.append(f"| {model} | {lead} | {key} | {row['mean']} | {row['min']} | {row['max']} |")
 L+=['','Per-run readings, bounds, calibration and action histograms: receipts/acd_stage16.json.','']
 (ROOT/'ACD_STAGE16_READING.md').write_text('\n'.join(L)+'\n')
 posterior=json.loads((ROOT/'runs/stage9/metrics_posterior.json').read_text())
 fig,axes=plt.subplots(1,2,figsize=(10,4))
 for group,model in enumerate(['CNN-F','CNN-noF']):
  for i,r in enumerate([r for r in runs if r['model']==model and 'metrics' in r]):
   val=r['summary_metrics']['3.0'];x=group+(i-2)*.06
   for ax,y in zip(axes,[val['S_case_error'],val['E_mean_regret']]):ax.plot(x,y,marker='o' if model=='CNN-F' else 's',color='black',linestyle='none',markerfacecolor='white' if r['baseline'] else 'black')
 for ax in axes:ax.set_xticks([0,1],['CNN-F','CNN-noF']);ax.set_xlim(-.3,1.3)
 p=next(r for r in posterior['confidence_readings'] if r['lead']==3)
 axes[0].axhline(1-p['all_confident_accuracy']['case_accuracy'],color='black',linestyle='--',label='posterior')
 pr=json.loads((ROOT/'receipts/acd_stage13_decisions.json').read_text())['models']['posterior']['readings']
 axes[1].axhline(next(r['mean_regret'] for r in pr if r['lead']==3 and r['policy']=='E'),color='black',linestyle='--',label='posterior')
 axes[0].set_ylabel('share of confident intervention answers wrong (all eight patterns)');axes[1].set_ylabel('E mean regret, 3 LT')
 for ax in axes:ax.legend();ax.grid(axis='y',color='.85')
 fig.tight_layout()
 for ext in ['pdf','png']:fig.savefig(ROOT/f'figures/F19_seeds_paper.{ext}',dpi=180)
 plt.close(fig)
if __name__=='__main__':main()
