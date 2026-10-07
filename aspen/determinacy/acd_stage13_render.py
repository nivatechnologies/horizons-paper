"""Stage 13 presentation: receipts only, no outcome files opened."""
import os
os.environ['MPLBACKEND']='Agg'
import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
def read(n):return json.load(open(ROOT/'receipts'/n))
def savefig(fig,name):
 fig.tight_layout()
 for ext in ['pdf','png']:fig.savefig(ROOT/f'figures/{name}.{ext}',dpi=180)
 plt.close(fig)
def figures():
 plt.rcParams.update({'font.size':9,'axes.prop_cycle':plt.cycler(color=['black','0.35','0.60','0.15'])})
 sizes={}
 d=read('acd_stage6.json');rows=d['A']['A1']['comparisons']
 fig,axs=plt.subplots(1,2,figsize=(10,4))
 for field,label,style,marker in [('Fc_share','forecast sign F_c','-','o'),('all_S_share','all-eight S','--','s'),('seven_S_share','seven-pattern S','-.','^'),('observation_S_share','observation-confident S',':','d')]:
  if field=='seven_S_share':y=[r['seven_minus_Fc']['point']+r['Fc_share'] for r in rows]
  else:y=[r[field] for r in rows]
  axs[0].plot([r['lead'] for r in rows],y,linestyle=style,marker=marker,label=label)
 axs[0].set(xlabel='Lead (LT)',ylabel='Confident share');axs[0].legend(fontsize=8)
 ep=read('acd_stage9.json')['A']['A2']['case_averaged'];labels=['earlier','later','same']
 bars=axs[1].bar(labels,[ep[k] for k in labels],color=['0.8','0.6','0.95'],edgecolor='black')
 for b,h in zip(bars,['/','x','..']):b.set_hatch(h)
 axs[1].set_ylabel('Case-averaged first-loss share')
 savefig(fig,'F15_overview_paper');sizes['F15_overview_paper']=[720,288]
 d=read('acd_stage13_instance.json');fig,axs=plt.subplots(1,2,figsize=(10,4))
 for name,label,color,style,marker,hatch in [('Fc','J8 − Jbar','0.25','-','o','/'),('S','D_k','black','--','s','x')]:
  r=d['series'][name];x=d['leads']
  axs[0].fill_between(x,r['q05'],r['q95'],facecolor='0.95',edgecolor=color,hatch=hatch,linewidth=.3,alpha=.7,label=f'{label}: 5–95%')
  axs[0].fill_between(x,r['q25'],r['q75'],facecolor='0.85',edgecolor=color,hatch=hatch+hatch,linewidth=.3,alpha=.6,label=f'{label}: 25–75%')
  axs[0].plot(x,r['median'],linestyle=style,marker=marker,color=color,label=f'{label}: posterior median')
  axs[0].plot(x,r['realized'],linestyle=':',marker='x' if name=='Fc' else '^',color=color,label=f'{label}: realized')
  axs[1].plot(x,r['modal_probability'],linestyle=style,marker=marker,color=color,label=name)
 axs[0].axhline(0,linestyle='-.',color='0.6');axs[0].set(xlabel='Lead (LT)',ylabel='Window cost / effect')
 axs[0].legend(fontsize=7)
 axs[1].axhline(.95,linestyle='--',color='0.6',label='Confidence threshold');axs[1].set(xlabel='Lead (LT)',ylabel='Posterior modal-answer probability',ylim=(.5,1.01));axs[1].legend()
 # Figure explicitly illustrative; no suptitle.
 axs[0].set_title('Illustrative instance')
 savefig(fig,'F16_instance_paper');sizes['F16_instance_paper']=[720,288]
 stage9=read('acd_stage9.json');fig,axs=plt.subplots(1,2,figsize=(10,4))
 for name,style,marker in [('posterior','-','o'),('CNN-20k','--','s'),('CNN-F','-.','^')]:
  model=stage9['C'][name];r=[r for r in model['reliability'] if r['questions']]
  axs[0].errorbar([v['mean_probability'] for v in r],[v['accuracy'] for v in r],yerr=np.array([[v['accuracy']-v['CP95'][0] for v in r],[v['CP95'][1]-v['accuracy'] for v in r]]),linestyle=style,marker=marker,label=name)
  r=[v for v in model['error_coverage'] if v['answers']]
  axs[1].plot([v['coverage'] for v in r],[v['pooled_error'] for v in r],linestyle=style,marker=marker,label=name)
 axs[0].plot([.5,1],[.5,1],linestyle=':',marker='+',color='0.6');axs[0].set(xlabel='Mean modal probability',ylabel='Observed accuracy')
 axs[1].set(xlabel='Coverage',ylabel='Pooled error')
 for ax in axs:ax.legend(fontsize=8)
 savefig(fig,'F13_main_paper');sizes['F13_main_paper']=[720,288]
 d=read('acd_stage13_decisions.json');fig,axs=plt.subplots(1,2,figsize=(10,4))
 names=['posterior','CNN-20k','CNN-F'];x=np.arange(len(names));width=.35
 for ax,lead in zip(axs,[2,3]):
  for i,(policy,label,hatch) in enumerate([('E','E','/'),('C_delta_0','C (δ = 0)','x')]):
   rows=[next(r for r in d['models'][name]['readings'] if r['lead']==lead and r['policy']==policy) for name in names]
   bars=ax.bar(x+(i-.5)*width,[r['mean_regret'] for r in rows],width,label=label,color='0.85' if i else '0.6',edgecolor='black',hatch=hatch)
   for b,r in zip(bars,rows):ax.annotate(str(r['harms']),xy=(b.get_x()+b.get_width()/2,b.get_height()),xytext=(0,3),textcoords='offset points',ha='center',fontsize=8)
  ax.set_xticks(x,names);ax.set(ylabel='Mean realized regret',title=f'{lead} LT');ax.legend(fontsize=8)
 savefig(fig,'F17_decisions_paper');sizes['F17_decisions_paper']=[720,288]
 # Read actual PDF MediaBox, rather than rely on requested canvas sizes.
 import re
 for name in sizes:
  raw=(ROOT/f'figures/{name}.pdf').read_bytes();box=re.search(rb'/MediaBox\s*\[\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*\]',raw)
  coords=list(map(float,box.groups()));sizes[name]=[coords[2]-coords[0],coords[3]-coords[1]]
 (ROOT/'receipts/acd_stage13_figures.json').write_text(json.dumps(dict(page_sizes_points=sizes,scope='presentation only, receipts only; greyscale and secondary cues'),indent=2)+'\n')
 print(sizes)
def fmt(v):
 if v is None:return '—'
 if isinstance(v,float):return format(v,'.6g')
 return str(v)
def table(rows,fields):
 return ['| '+' | '.join(fields)+' |','| '+' | '.join(['---']*len(fields))+' |']+['| '+' | '.join(fmt(r.get(k)) for k in fields)+' |' for r in rows]
def report():
 a=read('acd_stage13_decisions.json');b=read('acd_stage13_dt.json');c=read('acd_stage13_instance.json');d=read('acd_stage13_withheld.json');g=read('acd_stage13_evaluator_check.json');fig=read('acd_stage13_figures.json')
 lines=['# Stage 13 — review-3 analyses','','Post hoc on confirmation; licenses no frozen route. CPU forward integration and scoring on sulaco. Paper and abstract unchanged. No Spark, GPU, Stage 10/10b, Qwen or AFD close-out work. All reported values below are rendered from the receipts by acd_stage13_render.py.','','## A — cross-model decisions','','Improvement and regret use realized costs. Capture = mean improvement / mean no-action regret. Any invalid draw/option forces no action for E/C, with no survivor conditioning. Histograms list options in index order, no action last. Zero-harm upper bounds are one-sided exact Clopper–Pearson.','']
 for model,r in a['models'].items():
  lines+=['### '+model,'','Invalid case indices: '+str(r['invalid_case_indices']), '']
  lines+=table(r['readings'],['lead','policy','mean_improvement','mean_regret','capture_fraction','acting_share','harms','median_harm','max_harm','zero_harm_CP_upper','chosen_actions'])+['']
 lines+=['### Paired comparisons against posterior','','Sign tests are exact two-sided on nonzero case regret differences. Bootstrap intervals are descriptive paired case intervals. McNemar is exact on case harm indicators. No multiplicity-adjusted or frozen-route claim.','']
 lines+=table(a['paired_comparisons'],['model','lead','policy','chosen_option_different_share','mean_regret_difference','exact_two_sided_sign_p','descriptive_paired_bootstrap_95_interval','posterior_only_harm','model_only_harm','exact_McNemar_p'])+['']
 lines+=['## B — full-grid step halving','','First-frame restart includes the observation window. Every saved posterior draw, every option, every lead window, truth and the saved null are reintegrated with float64 RK4. The climatological anomaly reference Jbar is frozen; null probabilities are recomputed.','',f"Draws: {b['all_saved_draws']}; null states: {b['null_states']}; dt: {b['baseline_dt']} → {b['dt']}.", '']
 lines+=table(b['changes'],['lead','type','draw_answer_changed_share','confidence_changed_count','confidence_changed_share','realized_answer_changed_count','realized_answer_changed_share'])+['']
 for label,key in [('Recomputed eligibility','paired_first_loss'),('Original eligible cohort sensitivity','paired_fixed_original_cohort'),('Original baseline','baseline_paired_first_loss')]:
  r=b[key];lines += [label+': '+json.dumps({k:r[k] for k in ['pairs','cases','case_averaged','interval']}),'']
 lines+=["Paired point change: "+fmt(b['paired_point_change']), '', 'Table 2, observation-confident S accuracy and confident Fc accuracy:','',*table(b['Table2'],['lead','S_case_accuracy','S_one_sided95_lower','S_answers','S_cases','Fc_accuracy','Fc_one_sided95_lower','Fc_answers']),'', 'Other question accuracy and seven-pattern comparisons: full-precision receipt tables in receipts/acd_stage13_dt.json.', '',json.dumps(b['seven_pattern_comparisons'],indent=2),'']
 lines+=['## C — worked instance (illustrative)','',c['selection_rule'],'',*table([c],['case','action','eligible_pairs','earlier_pairs','combination_count','S_first_loss_lead','Fc_first_loss_lead']),'']
 rows=[]
 for r in d['readings']:
  for status,v in r['groups'].items():
   rows.append(dict(lead=r['lead'],patterns=r['patterns'],status=status,**v,withheld_exceeds_confident_median=r['not_confident_exceeds_confident_median_share'] if status=='not_confident' else None,withheld_beneficial=r['not_confident_beneficial_share'] if status=='not_confident' else None))
 lines+=['## D — withheld effect sizes (descriptive)','',*table(rows,['lead','patterns','status','questions','realized_absolute_effect','posterior_mean_absolute_effect','realized_absolute_effect_over_climate_sd','withheld_exceeds_confident_median','withheld_beneficial']),'']
 lines+=['## E–G — figures, registry and release preparation','',*table([dict(figure=k,page_size_points=v) for k,v in fig['page_sizes_points'].items()],['figure','page_size_points']),'', 'Evaluator exact reproduction: '+str(g['pass_exact'])+'; differences: '+str(g['differences'])+'. See README_EVALUATE.md and RELEASE_MANIFEST.md. No public archive is published.','', '## Resolution rules','']
 verification=read('acd_stage13_verification.json')
 lines += verification['resolutions'] or ['None fired.']
 lines += ['', 'Registry before: '+str(verification['registry_before'])+'; after: '+str(verification['registry_after'])+'. Prior values unchanged. Registry check: '+verification['registry_check']+'.']
 release=read('acd_stage13_release.json')
 lines += ['', 'Release inventory summary:', '']
 lines += table([dict(role=k,**v) for k,v in release['groups'].items()],['role','files','size_bytes'])
 lines += ['', 'Flagged items and checkpoint hashes: RELEASE_MANIFEST.md and receipts/acd_stage13_release.json.']

 (ROOT/'ACD_STAGE13_READING.md').write_text('\n'.join(lines)+'\n')
if __name__=='__main__':
 import sys
 (figures if sys.argv[1]=='figures' else report)()
