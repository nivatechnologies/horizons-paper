"""Assemble Stage23 saved receipts/logs and render the final report and figures."""
from pathlib import Path
import json,hashlib,math
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'runs/stage23'
def load(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,d):Path(p).write_text(json.dumps(d,indent=2,allow_nan=False)+'\n')
def fmt(v):return format(v,'.6g') if isinstance(v,(int,float)) else str(v)
def assemble():
 p=ROOT/'receipts/acd_stage23.json';d=load(p);base=OUT/'primary_scoring_receipt.json'
 if not base.exists():base.write_bytes(p.read_bytes())
 previous=load(p);d=load(base);d.update({k:previous[k] for k in ['registry_verification','figure_page_sizes_points','freeze_g_sha256'] if k in previous});d['primary_scoring_receipt_sha256']=sha(base)
 selection=load(OUT/'selection.json');zero=selection['rows'][0]['validation_state_MSE']
 old=load(ROOT/'receipts/acd_stage18_C_execution_reading.json')['validation_rows']
 d['validation_original_recipe']=old;d['validation_corrected_recipe']=[];d['training_runs']=[];d['training_logs']={};manifest=[]
 for row in selection['rows']:
  new=dict(row,validation_state_MSE_ratio_to_weight_zero=row['validation_state_MSE']/zero)
  if row['weight']:
   folder=OUT/'training'/row['model'];m=load(folder/'complete.json');new.update(selected_step=m['selected_step'],guard_abort=m['abort'],capped=m['capped'])
   d['training_runs'].append(m)
   progress=load(folder/'progress.json');skips=load(folder/'skips.json') if (folder/'skips.json').exists() else []
   d['training_logs'][row['model']]=dict(weight=row['weight'],progress_every_100_updates=progress,skips=skips,skip_steps=[s['step'] for s in skips],initial_base_over_paired=m['normal_base']/m['normal_difference'])
   for name in ['complete.json','complete_initial_cap.json','progress.json','skips.json','terminal_loss_balance.json','selected.pt']:
    f=folder/name
    if f.exists():manifest.append(dict(path=str(f),bytes=f.stat().st_size,sha256=sha(f)))
  else:new.update(selected_step=old[0]['selected_step'],guard_abort=None,capped=False)
  d['validation_corrected_recipe'].append(new)
 d['part3b_descriptive']=load(ROOT/'receipts/acd_stage23_part3b.json')
 d['derivatives_original_panel']=load(ROOT/'receipts/acd_stage23_derivatives.json')
 d['menu_decisions']=load(ROOT/'receipts/acd_stage23_menus.json')
 d['extra_seeds_triggered']=bool(d['Q1']['confirmed']);assert not d['extra_seeds_triggered']
 d['failed_attempts']=[load(p) for p in sorted((OUT/'task_logs').glob('*initial.json'))]
 d['GPU_task_records']={p.stem:load(p) for p in sorted((OUT/'task_logs').glob('*.json'))};d['Q2']['point']=d['Q2']['harms']/d['Q2']['actions_taken'];d['criteria_unchanged']=True;d['code_hashes']={p.name:sha(p) for p in ROOT.glob('acd_stage23_*.py')}
 d['execution_records']={name:load(OUT/name) for name in ['cap12_resume_record.json','cap12_completed.json'] if (OUT/name).exists()}
 d['training_manifest']=manifest
 from acd_stats import difference_interval
 levels=load(ROOT/'receipts/acd_stage22_panel_contract.json')['forcing_by_case']
 d['by_forcing_descriptive_comparisons']={}
 for level in sorted(set(levels)):
  ids=[i for i,f in enumerate(levels) if f==level]
  q1=[d['Q1']['case_differences'][i] for i in ids if d['Q1']['case_differences'][i] is not None]
  e0=[d['selected_minus_E0_fixed']['case_mean_differences'][i] for i in ids if d['selected_minus_E0_fixed']['case_mean_differences'][i] is not None]
  group=d['descriptive_models'][next(iter(d['descriptive_models']))]['F'+str(int(level))]
  risk=next(v for v in group['decisions'] if v['lead']==3. and v['policy']=='C_delta_0')
  d['by_forcing_descriptive_comparisons']['F'+str(int(level))]=dict(descriptive_only=True,Q1=dict(contributing_instances=len(q1),interval=difference_interval(q1)),selected_minus_E0_fixed=dict(contributing_instances=len(e0),interval=difference_interval(e0)),Q2=risk)
 write(p,d);return d

def figures(d):
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 fig,axes=plt.subplots(2,3,figsize=(10,8),sharex=True)
 for ax,(name,row) in zip(axes.flat,d['training_logs'].items()):
  points=row['progress_every_100_updates'];norm=ax.twinx()
  for key,label,style,marker,target in [('base_loss','base loss','-','o',ax),('raw_paired_loss','raw paired loss','--','s',ax),('base_gradient_norm','base gradient norm','-.','^',norm),('paired_gradient_norm','paired gradient norm',':','x',norm)]:
   values=[(p['step'],p[key]) for p in points if isinstance(p.get(key),(int,float)) and math.isfinite(p[key]) and p[key]>0]
   target.plot([p[0] for p in values],[p[1] for p in values],color='black',linestyle=style,marker=marker,markevery=max(1,len(values)//10),markersize=3,linewidth=.8,label=label)
  ax.set_yscale('log');norm.set_yscale('log');ax.set_title('weight '+fmt(row['weight']));ax.set_xlabel('scheduled update');ax.set_ylabel('logged loss');norm.set_ylabel('gradient norm')
  lines=ax.get_lines()+norm.get_lines()
  for step in row['skip_steps']:ax.axvline(step,color='.5',linestyle=':',linewidth=.5)
 axes.flat[-1].axis('off');axes.flat[-1].legend(lines,[x.get_label() for x in lines],loc='center',fontsize=9);fig.tight_layout()
 (ROOT/'figures').mkdir(exist_ok=True)
 for ext in ['pdf','png']:fig.savefig(ROOT/'figures'/('F_stage23_training_losses.'+ext),dpi=150)
 plt.close(fig)

def render(d):
 lines=['# Stage 23 — corrected response-training recipe','', 'Frozen Q1 and Q2 results on the Stage 22 panel. Other readings are descriptive; the original-panel derivative and restricted-menu readings are POST HOC and license no frozen route. All tables below are generated from receipts/acd_stage23.json by acd_stage23_report.py.','', 'Weight '+fmt(d['selection']['selected']['weight'])+' was selected by the frozen validation rule. Q1 did not confirm, so no further training seeds are triggered.','', '| Reading | Point | Interval / bound | Bound type | Contributing n | Outcome |','|---|---:|---|---|---:|---|']
 q=d['Q1'];v=q['interval'];lines.append(f"| Q1: retained CNN-noF minus selected model, seven patterns, 2 LT | {fmt(v['point'])} | [{fmt(v['lower'])}, {fmt(v['upper'])}] | two-sided 99% v2.3 instance betting | {q['contributing_cases']} | {'PASS' if q['confirmed'] else 'FAIL'} |")
 q=d['Q2'];lines.append(f"| Q2: strict-positive harm conditional on C(delta=0) acting, 3 LT | {fmt(q['harms']/q['actions_taken'])} | upper {fmt(q['conditional_harm_CP95'][1])} | exact one-sided 95% Clopper–Pearson upper | {q['actions_taken']} actions; {q['cases']} retained instances | {'PASS' if q['confirmed'] else 'FAIL'} |")
 lines+=['','Descriptive selected-minus-E0-fixed, seven patterns at 2 LT: '+json.dumps(d['selected_minus_E0_fixed']['interval'])+'.','', '## Validation, both recipes','', '| Weight | Original state MSE / weight zero | Original effect RMSE | Corrected state MSE / weight zero | Corrected effect RMSE | Corrected checkpoint step |','|---:|---:|---:|---:|---:|---:|']
 for row in d['validation_corrected_recipe']:
  old=next(x for x in d['validation_original_recipe'] if x['weight']==row['weight'])
  lines.append('| '+' | '.join([fmt(row['weight']),fmt(old['validation_state_MSE_ratio_to_weight_zero']),fmt(old['validation_effect_RMSE']),fmt(row['validation_state_MSE_ratio_to_weight_zero']),fmt(row['validation_effect_RMSE']),fmt(row['selected_step'])])+' |')
 lines+=['','Original-recipe guard-aborted weights are retained descriptively at their last validation-eligible checkpoint. The exact guard-abort details and checkpoint steps are listed below. The corrected weight 0.1 run reached its authorized time cap; the other corrected runs completed their schedules. The cap continuation replayed updates from the last optimizer checkpoint and charged that replay time. Full execution records remain in the receipt.','', '## Training execution','', '| Weight | Scheduled updates | Skips | Selected step | Charged GPU seconds | Cap seconds | Abort |','|---:|---:|---:|---:|---:|---:|---|']
 for m in d['training_runs']:lines.append(f"| {fmt(m['response_multiplier'])} | {m['scheduled_updates']} | {m['skipped_updates']} | {m['selected_step']} | {fmt(m['charged_gpu_seconds'])} | {m['cap_seconds']} | {m['abort'] or 'none'} |")
 lines+=['','No corrected-model update was skipped. Every saved hundred-update loss and gradient record, the initial loss-value diagnostic ratio, applied gradient scale and combined preclip norm are in the JSON receipt. The loss-value ratio was diagnostic only; the update used separate gradient norms. Figure: figures/F_stage23_training_losses.pdf. Base loss uses solid circles; raw paired loss dashed squares; base gradient norm dash-dot triangles; paired gradient norm dotted crosses. Both loss and norm axes are logarithmic.','', '## Descriptive model readings','', '| Panel / population | Lead | State RMSE / sigma | State ACC | Confident S share (all eight) | Pooled confident S error | Case confident S error | Case error interval, one-sided 95% bounds |','|---|---:|---:|---:|---:|---:|---:|---|']
 name=next(iter(d['descriptive_models']));groups=[('Stage22 / '+pop,v) for pop,v in d['descriptive_models'][name].items() if pop in ['pooled','F7','F9']]+[('Part3b / all retained',d['part3b_descriptive']['readings'])]
 for label,result in groups:
  for c in result['confidence_readings']:
   skill=next(x for x in result['state_skill'] if x['lead']==c['lead'])
   lines.append(f"| {label} | {fmt(c['lead'])} | {fmt(skill['window_mean_RMSE_over_sigma'])} | {fmt(skill['window_mean_anomaly_correlation'])} | {fmt(c['confident_S_share'])} | {fmt(c['pooled_confident_error'])} | {fmt(c['case_confident_error'])} | [{fmt(c['case_error_lower'])}, {fmt(c['case_error_upper'])}] |")
 lines+=['','The JSON also reports pooled and equal-case J8/Jk/Dk RMSE and bias, seven-pattern reliability and coverage, calibration tests, same-lead differences, own/fixed-cohort paired endpoints, and per-pattern-group effect errors. Stage22 populations are reported pooled and separately by forcing; Part3b retains its existing population.','', '## Descriptive cost errors','', '| Panel / population | Lead | Quantity | Pooled RMSE | Pooled bias | Equal-case RMSE | Equal-case bias |','|---|---:|---|---:|---:|---:|---:|']
 for label,result in groups:
  for v in result['per_draw_cost_errors']:lines.append(f"| {label} | {fmt(v['lead'])} | {v['quantity']} | {fmt(v['pooled_RMSE'])} | {fmt(v['pooled_bias'])} | {fmt(v['equal_case_RMSE'])} | {fmt(v['equal_case_bias'])} |")
 lines+=['','## Descriptive confidence, same-lead and paired readings','', '| Panel / population | Lead | Seven-pattern S share | Observation-confident S share | F_c share | Seven S minus F_c, two-sided 99% interval |','|---|---:|---:|---:|---:|---|']
 for label,result in groups:
  for v in result['comparisons']:
   interval=v['seven_minus_Fc']
   lines.append(f"| {label} | {fmt(v['lead'])} | {fmt(v['seven_S_share'])} | {fmt(v['observation_S_share'])} | {fmt(v['Fc_share'])} | {fmt(interval['point'])} [{fmt(interval['lower'])}, {fmt(interval['upper'])}] |")
 lines+=['', '| Panel / population | Eligibility | Pairs | Instances | Later minus earlier, two-sided 99% interval | Case earlier / later / same |','|---|---|---:|---:|---|---|']
 for label,result in groups:
  for field in ['paired_endpoint','paired_endpoint_fixed_posterior_cohort']:
   if field not in result:continue
   v=result[field];interval=v['interval']
   lines.append(f"| {label} | {field} | {v.get('pairs',v.get('actions'))} | {v['cases']} | {fmt(interval['point'])} [{fmt(interval['lower'])}, {fmt(interval['upper'])}] | {v['case_averaged']} |")
 lines+=['', '| Panel / population | Lead | Threshold | Cases | Calibration point | Two-sided 99% v2.3 interval | Reject mean calibration |','|---|---:|---:|---:|---:|---|---|']
 for label,result in groups:
  for v in result['calibration_test']:
   interval=v['overconfidence_interval']
   lines.append(f"| {label} | {fmt(v['lead'])} | {fmt(v['threshold'])} | {v['cases']} | {fmt(interval['point'])} | [{fmt(interval['lower'])}, {fmt(interval['upper'])}] | {v['reject_mean_calibration']} |")
 lines+=['','## POST HOC full and restricted menus','', 'Restricted menu: seven zero-mean patterns plus no action; E keeps the existing argmin tie order, and C gates only that E choice. Harms are strictly positive effects; zero-effect ties are recorded separately. Expected harms sum the chosen actions’ predicted probabilities of not lowering energy.','', '| Panel / population | Menu | Lead | Policy | Actions | Harms | Expected harms | Regret | Capture | Conditional harm one-sided 95% CP bounds | Action histogram |','|---|---|---:|---|---:|---:|---:|---:|---:|---|---|']
 menu_groups=[('Stage22 / '+pop,rows) for pop,rows in d['menu_decisions']['panels']['stage22'].items()]+[('Part3b / all retained',d['part3b_descriptive']['readings']['menu_decisions'])]
 for label,rows in menu_groups:
  for v in rows:lines.append(f"| {label} | {v['menu']} | {fmt(v['lead'])} | {v['policy']} | {v['actions_taken']} | {v['strict_positive_harms']} | {fmt(v['expected_harms'])} | {fmt(v['mean_regret'])} | {fmt(v['capture_fraction'])} | {v['conditional_harm_CP_one_sided95']} | {v['chosen_actions']} |")
 lines+=['','## POST HOC original-panel derivatives','', '| Lead | Per-draw sign agreement | Normalized RMS error | Three-class agreement | Kappa | Median z |','|---:|---:|---:|---:|---:|---:|']
 for v in d['derivatives_original_panel']['rows']:lines.append(f"| {fmt(v['lead'])} | {fmt(v['per_draw_sign_agreement'])} | {fmt(v['normalized_RMS_error'])} | {fmt(v['three_class_agreement'])} | {fmt(v['three_class_kappa'])} | {fmt(v['median_z'])} |")
 lines+=['','Normalized RMS error uses the pooled physics-tangent RMS at each lead. The receipt includes transfer-bound ingredients: pooled and case-action squared derivative error, probability error, and near-zero posterior mass at each frozen gamma.','', '## Execution and provenance','', 'All inference outputs were written and hashed before scoring. Outcomes were opened only inside the unchanged frozen score_actual functions, with access logged. A private CPU dependency copy was incomplete on the first Part3b scoring attempt; its log is retained beside its failure JSON. Copying the unchanged modules repaired that execution failure. No scientific code or criterion changed.','', 'Checkpoint and output arrays remain untracked on niva-array; the publication includes their manifests and task logs. Frozen kernels are identified by hashes in the receipt. Training and inference are complete.']
 (ROOT/'ACD_STAGE23_READING.md').write_text('\n'.join(lines)+'\n')
if __name__=='__main__':
 d=assemble();figures(d);render(d);print('STAGE23 REPORT AND FIGURES GENERATED')
