"""Stage10b receipt report; no model execution or outcome opening."""
import json,hashlib,math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
MODELS=['posterior','CNN-20k','CNN-F','CNN-F-resp','CNN-noF','CNN-F-resp-0.01','CNN-F-resp-0.1']
NEW=MODELS[4:]
def read(path):return json.loads(path.read_text())
def fmt(v):return 'not available' if v is None else repr(v)
def interval(r):return f"{fmt(r['point'])} [{fmt(r['lower'])}, {fmt(r['upper'])}]"
def main():
 stage9=read(ROOT/'receipts/acd_stage9.json')
 result=dict(post_hoc=True,panel='confirmation',licenses_frozen_route=False,selection_among_models=False,models={},training={},failure=read(ROOT/'receipts/acd_stage10_failure.json'),resolutions=[],source_hashes={},code_hashes={})
 for name in MODELS:
  path=ROOT/'runs/stage9'/f'metrics_{name}.json'
  if not path.exists():
   result['models'][name]=dict(status='unavailable; no imputed metrics')
   result['resolutions'].append(f'R-other: {name} has no completed inference/scoring receipt; report unavailable, retain every other model.')
   continue
  d=read(path)
  if name in NEW:
   tr=read(ROOT/'runs/stage9_training'/name/'complete.json')
   assert tr['charged_gpu_seconds']<=tr['cap_seconds']
   assert tr['data_sha256']==stage9['F']['CNN-F']['data_sha256']
   assert tr['selected_sha256']==d['execution']['checkpoint_sha256']
   skips=ROOT/'runs/stage9_training'/name/'skips.json'
   tr['skip_records']=read(skips) if skips.exists() else []
   assert len(tr['skip_records'])==tr['skipped_updates'], 'missing skip diagnostics'
   result['training'][name]=tr
  elif name in stage9['F']:result['training'][name]=stage9['F'][name]
  for row in d['confidence_readings']:
   for typ,field in [('S','all_confident_accuracy'),('observation_S','observation_confident_accuracy'),('Fc','Fc_accuracy')]:
    a=row[field]
    row[typ+'_error_summary']=dict(case_error=1-a['case_accuracy'] if a['case_accuracy'] is not None else None,case_error_lower=1-a['case_upper'],case_error_upper=1-a['case_lower'],pooled_error=1-a['answer_accuracy'] if a['answer_accuracy'] is not None else None,answers=a['answers'],cases=a['cases'],bound='v2.3 one-sided 95% case-level betting bounds (each side separately); pooled point is descriptive')
   if row['all_confident_accuracy'].get('fallback'):result['resolutions'].append(f"R-other: {name} lead {row['lead']} uses declared statistical fallback.")
  result['models'][name]=d;result['source_hashes'][str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
 result['baseline_terminal_loss_balance']=read(ROOT/'receipts/acd_stage10_terminal_baseline.json')
 result['resolutions'].append(result['failure']['accounting_rule'])
 result['resolutions'].append('R-other: preserve estimands: pooled question errors are descriptive; v2.3 case-level bounds apply to equal-case errors only. Reliability-bin Clopper–Pearson intervals remain descriptive under within-case dependence.')
 for path in ROOT.glob('acd_stage10b*.py'):result['code_hashes'][path.name]=hashlib.sha256(path.read_bytes()).hexdigest()
 (ROOT/'receipts/acd_stage10b.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
 L=['# Stage 10b guarded control and response-weight sweep','','POST HOC ON CONFIRMATION. Licenses no frozen route. Every model is reported; there is no selection among models or weights.','','## Training','','| Model | Scheduled | Completed | Skipped | Selected step | Charged GPU seconds | Abort |','|---|---|---|---|---|---|---|']
 for name,tr in result['training'].items():
  L.append(f"| {name} | {tr.get('scheduled_updates',tr['step'])} | {tr.get('completed_updates',tr['step'])} | {tr.get('skipped_updates','unguarded; not monitored')} | {tr['selected_step']} | {fmt(tr['charged_gpu_seconds'])} | {tr.get('abort') or 'none'} |")
  if name in NEW:L.append('')
 for name,tr in result['training'].items():
  if tr.get('guarded'):L += ['',f"{name}: {tr['guard_recipe_equivalence']}."]
 L+=['','## Terminal training-only loss balance','','Final model, independently of validation selection. Alpha-one receipt is retained from Stage 10; selected and terminal serializations may have different file hashes.','','| Model | Multiplier | Base | Paired raw | Weighted paired/base | Weighted paired fraction | Terminal step |','|---|---|---|---|---|---|---|']
 balances=[result['baseline_terminal_loss_balance']]+[result['training'][n]['terminal_loss_balance'] for n in NEW if n in result['training'] and n.startswith('CNN-F-resp')]
 for b in balances:L.append(f"| {b['model']} | {fmt(b['multiplier'])} | {fmt(b['base_loss'])} | {fmt(b['difference_loss'])} | {fmt(b['difference_to_base_ratio'])} | {fmt(b['weighted_difference_fraction'])} | {b['terminal_step']} |")
 L+=['','## Skill and confidence','','All-S shares use all eight action questions; Fc is the sign of the unforced window-energy anomaly. Error bounds are case-level; pooled error is descriptive.','','| Model | Lead LT | RMSE/sigma | Anomaly correlation | Confident S | Observation-confident S | Confident Fc | Case S error [bounds] | Pooled S error | Case observation S error [bounds] | Pooled observation S error |','|---|---|---|---|---|---|---|---|---|---|---|']
 for name,d in result['models'].items():
  if 'confidence_readings' not in d:L+=['',name+': '+d['status']];continue
  for row in d['confidence_readings']:
   skill=next(x for x in d['state_skill'] if x['lead']==row['lead']);a=row['S_error_summary'];o=row['observation_S_error_summary']
   L.append(f"| {name} | {row['lead']} | {fmt(skill['window_mean_RMSE_over_sigma'])} | {fmt(skill['window_mean_anomaly_correlation'])} | {fmt(row['confident_S_share'])} | {fmt(row['observation_S_share'])} | {fmt(row['confident_Fc_share'])} | {fmt(a['case_error'])} [{fmt(a['case_error_lower'])}, {fmt(a['case_error_upper'])}] | {fmt(a['pooled_error'])} | {fmt(o['case_error'])} [{fmt(o['case_error_lower'])}, {fmt(o['case_error_upper'])}] | {fmt(o['pooled_error'])} |")
 L+=['','| Model | Lead LT | S answers | Observation S answers | Fc answers | Case Fc error [bounds] | Pooled Fc error |','|---|---|---|---|---|---|---|']
 for name,d in result['models'].items():
  for row in d.get('confidence_readings',[]):
   a=row['S_error_summary'];o=row['observation_S_error_summary'];f=row['Fc_error_summary']
   L.append(f"| {name} | {row['lead']} | {a['answers']} | {o['answers']} | {f['answers']} | {fmt(f['case_error'])} [{fmt(f['case_error_lower'])}, {fmt(f['case_error_upper'])}] | {fmt(f['pooled_error'])} |")
 L+=['','## Per-draw cost errors','','Pooled weights every saved draw/action equally. Equal-case columns average the per-case metric, giving each case equal weight. The posterior is its own physics reference, so its per-draw model error is identically zero by definition.','','| Model | Lead | Quantity | Pooled bias | Pooled RMSE | Pooled MAE | Equal-case bias | Equal-case RMSE | Equal-case MAE |','|---|---|---|---|---|---|---|---|---|']
 for name,d in result['models'].items():
  for row in d.get('pooled_per_draw_errors',[]):
   e=next(x for x in d['per_draw_cost_errors'] if x['lead']==row['lead'] and x['quantity']==row['quantity'])
   L.append(f"| {name} | {row['lead']} | {row['quantity']} | {fmt(row['bias'])} | {fmt(row['RMSE'])} | {fmt(row['MAE'])} | {fmt(e['bias']['mean'])} | {fmt(e['RMSE']['mean'])} | {fmt(e['MAE']['mean'])} |")
 L+=['','## Seven-pattern same-lead differences','','Case-level betting two-sided 99% intervals; difference is seven-pattern confident S share minus confident Fc share.','','| Model | Lead | Difference [interval] |','|---|---|---|']
 for name,d in result['models'].items():
  for row in d.get('comparisons',[]):L.append(f"| {name} | {row['lead']} | {interval(row['seven_minus_Fc'])} |")
 L+=['','## Paired first-loss endpoints','','Difference is later minus earlier, averaged over eligible instances. Fixed cohort comes from the saved posterior endpoint; model-specific eligibility comes from each model’s lead-zero confidence.','','| Model | Cohort | Pairs | Cases | Earlier | Later | Same | Later minus earlier [99% interval] |','|---|---|---|---|---|---|---|---|']
 for name,d in result['models'].items():
  for field in ['paired_endpoint','paired_endpoint_fixed_posterior_cohort']:
   r=d.get(field)
   if r:L.append(f"| {name} | {field} | {r['pairs']} | {r['cases']} | {fmt(r['case_averaged']['earlier'])} | {fmt(r['case_averaged']['later'])} | {fmt(r['case_averaged']['same'])} | {interval(r['interval'])} |")
 L+=['','## Matched seven-pattern reliability and error coverage','','All model bins use the same cases and seven-pattern questions at the stated lead. Binomial intervals are descriptive, not independent-case confidence claims. The case-level betting calibration test checks mean modal probability minus correctness; it is not a test of full conditional calibration. Separate its verdict from confident-answer error.','','| Model | Lead | Threshold | Coverage | Pooled error | Case accuracy |','|---|---|---|---|---|---|']
 for name,d in result['models'].items():
  for r in d.get('matched_readings',[]):
   for c in r['error_coverage']:L.append(f"| {name} | {r['lead']} | {c['threshold']} | {fmt(c['coverage'])} | {fmt(c['pooled_error'])} | {fmt(c['case_accuracy']['case_accuracy'])} |")
 L+=['','| Model | Lead | Threshold | Modal probability minus correctness [99% interval] | Reject mean calibration? |','|---|---|---|---|---|']
 for name,d in result['models'].items():
  for r in d.get('matched_readings',[]):
   for t in r['calibration_test']:L.append(f"| {name} | {r['lead']} | {t['threshold']} | {interval(t['overconfidence_interval'])} | {t['reject_mean_calibration']} |")
 L+=['','| Model | Lead | Probability bin | Questions | Correct | Mean probability | Accuracy | Descriptive CP interval |','|---|---|---|---|---|---|---|---|']
 for name,d in result['models'].items():
  for r in d.get('matched_readings',[]):
   for b in r['reliability']:L.append(f"| {name} | {r['lead']} | [{b['lower_edge']}, {b['upper_edge']}] | {b['questions']} | {b['correct']} | {fmt(b['mean_probability'])} | {fmt(b['accuracy'])} | {b['CP95']} |")
 L+=['','## Resolutions','']+['- '+x for x in result['resolutions']]
 L+=['','Full precision, Fc error summaries, distributions, execution hashes and all matched-question readings: receipts/acd_stage10b.json.']
 (ROOT/'ACD_STAGE10B_READING.md').write_text('\n'.join(L)+'\n')
 print('STAGE10B RECEIPT AND READING COMPLETE')
if __name__=='__main__':main()
