"""Stage10 receipts-only report; no cross-weight model selection."""
from pathlib import Path
import json,hashlib,subprocess
ROOT=Path(__file__).resolve().parent
NEW=['CNN-F-resp-0.1','CNN-F-resp-0.01']
MODELS=['CNN-F','CNN-F-resp']+NEW
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def compact_endpoint(e):
 return {k:v for k,v in e.items() if k!='records'} if e is not None else None
def run():
 old=json.load(open(ROOT/'receipts/acd_stage9.json'));models={};resolutions=[
 'R-other: every Stage10 result is post hoc and licenses no frozen route; the full sweep is reported without selecting a weight.',
 'R-other inherited: nominal one-LT validation is the same twelve-tick approximation; response loss and normalizers are the frozen Stage9 recipe.',
 'R-other inherited: pooled Clopper-Pearson reliability bars are descriptive because questions cluster within cases; the calibration test uses independent cases.',
 'R-other inherited: model-specific lead-zero eligibility and the original posterior fixed cohort are reported separately.']
 sources={'baseline_receipt':sha(ROOT/'receipts/acd_stage9.json'),'terminal_baseline':sha(ROOT/'receipts/acd_stage10_terminal_baseline.json'),'freeze':sha(ROOT/'ACD_STAGE10_TRAINING_FREEZE.md')}
 for name in MODELS:
  if name in NEW:
   training=json.load(open(ROOT/f'runs/stage9_training/{name}/complete.json'))
   metric=json.load(open(ROOT/f'runs/stage9/metrics_{name}.json'))
   balance=training['terminal_loss_balance']
   sources[name+'_metrics']=sha(ROOT/f'runs/stage9/metrics_{name}.json')
   sources[name+'_training']=sha(ROOT/f'runs/stage9_training/{name}/complete.json')
  else:
   training=old['F'][name];metric=old['C'][name]
   balance=json.load(open(ROOT/'receipts/acd_stage10_terminal_baseline.json')) if name=='CNN-F-resp' else None
  alpha=training.get('response_multiplier',1. if name=='CNN-F-resp' else 0.)
  assert training['parameter_count']==1000961
  assert training['data_sha256']==old['F']['CNN-F-resp']['data_sha256']
  assert training['normal_base']==old['F']['CNN-F-resp']['normal_base']
  assert training['normal_difference']==old['F']['CNN-F-resp']['normal_difference']
  assert training['charged_gpu_seconds']<=36000
  assert metric['matched_cases']==200 and metric['matched_questions']==1400
  assert metric['model']==name and metric['execution']['checkpoint_sha256']==training['selected_sha256']
  if balance:
   assert balance['multiplier']==alpha and balance['terminal_step']==training['step']
   assert abs(balance['difference_to_base_ratio']-balance['weighted_difference_loss']/balance['base_loss'])<1e-12
  models[name]=dict(alpha=alpha,difference_coefficient=balance['difference_coefficient'] if balance else 0.,training=training,terminal_loss_balance=balance,evaluation=metric)
  if training['capped']:resolutions.append(f"R-other: {name} capped at {training['step']} updates; selected within-model checkpoint {training['selected_step']} by the prescribed validation rule.")
  if metric['invalid_cases']:resolutions.append(f"R-other: {name} has invalid cases {metric['invalid_cases']}; do not condition confidence on surviving draws.")
 if len({v['training']['step'] for v in models.values()})>1:resolutions.append('R-other: unequal updates under separate GPU-time caps prevent an isolated comparison of loss weights.')
 subprocess.run(['git','diff','--exit-code','eeed4b0','--','aspen/determinacy/paper','aspen/determinacy/ACD_ABSTRACT_DRAFT.md','aspen/determinacy/receipts/acd_stage9.json'],cwd=ROOT,check=True)
 baseline=json.loads(subprocess.check_output(['git','show','eeed4b0:aspen/determinacy/numbers_acd.json'],cwd=ROOT))
 current=json.load(open(ROOT/'numbers_acd.json'))
 assert all(current['numbers'][k]==v for k,v in baseline['numbers'].items())
 d=dict(stage=10,post_hoc=True,no_frozen_route_license=True,no_selection_among_weights=True,
  models=models,posterior_reference=old['C']['posterior'],resolutions=resolutions,
  verification=dict(status='PASS',prior_numbers_unchanged=len(baseline['numbers']),paper_abstract_and_stage9_receipt_unchanged=True,
   training_normalizers_data_and_architecture_matched=True,budget_caps_checked=True,matched_confirmation_questions_checked=True),
  source_hashes=sources,code_hashes={p.name:sha(p) for p in ROOT.glob('acd_stage10*.py')})
 (ROOT/'receipts/acd_stage10.json').write_text(json.dumps(d,indent=2,allow_nan=False)+'\n')
 lines=['# Stage 10 — effect-loss weight sweep','',
 'Post hoc confirmation; licenses no frozen route. No selection among the reported weights. Spark NVIDIA GB10 training/inference, sulaco CPU scoring. Paper, abstract and Stage9 receipt untouched.','',
 'Machine-readable source: receipts/acd_stage10.json. Freeze: ACD_STAGE10_TRAINING_FREEZE.md. Baselines retained from Stage9; new weights evaluated by exactly the same posterior-history/own-forcing procedure, a=0.16.','',
 'Terminal loss balance uses the frozen training-only 64x128 probe on the final trained model, which may differ from the validation-selected checkpoint. The reported ratio is alpha*(normal_base/normal_difference)*terminal_difference_loss/terminal_base_loss. It is measured, not used for selection. CNN-F has no difference term.','',
 '| Model | Alpha | Completed / selected updates | GPU hours | Difference coefficient | Terminal base loss | Terminal difference loss | Weighted difference / base |','|---|---|---|---|---|---|---|---|']
 for name,m in models.items():
  t=m['training'];b=m['terminal_loss_balance']
  coef=m['difference_coefficient']
  lines.append(f"| {name} | {m['alpha']} | {t['step']} / {t['selected_step']} | {t['charged_gpu_seconds']/3600} | {coef} | {b['base_loss'] if b else 'not measured'} | {b['difference_loss'] if b else 'not applicable'} | {b['difference_to_base_ratio'] if b else 0} |")
 lines+=['','## Confidence and factual skill','',
 '| Model | LT | RMSE/sigma | Anomaly correlation | Confident S share | Observation-confident S share | S case accuracy [lower95, upper95] | Confident Fc share | Fc case accuracy [lower95, upper95] |',
 '|---|---|---|---|---|---|---|---|---|']
 for name,m in models.items():
  e=m['evaluation']
  for row in e['confidence_readings']:
   skill=next(s for s in e['state_skill'] if s['lead']==row['lead']);a=row['all_confident_accuracy'];f=row['Fc_accuracy']
   lines.append(f"| {name} | {row['lead']} | {skill['window_mean_RMSE_over_sigma']} | {skill['window_mean_anomaly_correlation']} | {row['confident_S_share']} | {row['observation_S_share']} | {a['case_accuracy']} [{a['case_lower']}, {a['case_upper']}] | {row['confident_Fc_share']} | {f['case_accuracy']} [{f['case_lower']}, {f['case_upper']}] |")
 lines+=['','Observation-dependent S accuracy and its case-level bounds are retained separately in each model evaluation.confidence_readings.observation_confident_accuracy. Calibration below uses matched seven-pattern S questions at2LT, same200 cases/1400 questions across every model; lower accuracy when confident and mean miscalibration are separate readings.','',
 '## Per-draw costs','',
 '| Model | LT | Quantity | Pooled bias | Pooled RMSE | Pooled MAE |','|---|---|---|---|---|---|']
 for name,m in models.items():
  for r in m['evaluation']['pooled_per_draw_errors']:
   lines.append('| '+' | '.join(str(x) for x in [name,r['lead'],r['quantity'],r['bias'],r['RMSE'],r['MAE']])+' |')
 lines+=['','Equal-case distributions of bias/RMSE/MAE, signed per-draw quartiles, counts and weights are also retained in the receipt.','',
 '## Seven-pattern same-lead differences','',
 '| Model | LT | S minus Fc point | Betting99 interval |','|---|---|---|---|']
 for name,m in models.items():
  for r in m['evaluation']['comparisons']:
   i=r['seven_minus_Fc'];lines.append(f"| {name} | {r['lead']} | {i['point']} | [{i['lower']}, {i['upper']}] |")
 lines+=['','## Paired first-loss endpoint','',
 '| Model | Cohort | Eligible pairs | Later minus earlier | Betting99 interval |','|---|---|---|---|---|']
 for name,m in models.items():
  for field in ['paired_endpoint','paired_endpoint_fixed_posterior_cohort']:
   p=m['evaluation'][field];i=p['interval'];lines.append(f"| {name} | {field} | {p['pairs']} | {i['point']} | [{i['lower']}, {i['upper']}] |")
 lines+=['','## Calibration test','',
 'The unchanged Stage9 test is a two-sided99% v2.3 case-level betting interval for case-mean modal probability minus correctness. Excluding zero rejects perfect mean calibration; including zero does not establish full conditional calibration. Pooled Clopper-Pearson reliability bins remain descriptive because questions cluster within instances. Reliability bins and error-coverage curves for every model are in the receipt.','',
 '| Model | Threshold | Cases | Overconfidence point | Betting99 interval | Reject mean calibration? |','|---|---|---|---|---|---|']
 for name,m in models.items():
  for r in m['evaluation']['calibration_test']:
   i=r['overconfidence_interval'];lines.append(f"| {name} | {r['threshold']} | {r['cases']} | {i['point']} | [{i['lower']}, {i['upper']}] | {r['reject_mean_calibration']} |")
 lines+=['','## Resolution rules','']+['- '+v for v in resolutions]+['',
 'Verification: prior NUMBERS values, paper/abstract and original Stage9 receipt unchanged; datasets, normalizers, parameter counts, time caps and matched-question counts checked. No cross-weight selection.','']
 (ROOT/'ACD_STAGE10_READING.md').write_text('\n'.join(lines))
 url='https://github.com/nivatechnologies/horizons-paper/blob/paper/aspen-2026-10-determinacy/aspen/determinacy/'
 note='\n'.join(['---','title: Aspen Stage10 effect-loss weight sweep','type: research-result','status: complete','created: 2026-10-06','tags: [aspen, determinacy, post-hoc]','---','# Stage 10 — effect-loss weight sweep','',
 'Post hoc confirmation. The full sweep is reported; no weight selected.','',
 '- [Report]('+url+'ACD_STAGE10_READING.md)',
 '- [Receipt]('+url+'receipts/acd_stage10.json)',
 '- [Freeze]('+url+'ACD_STAGE10_TRAINING_FREEZE.md)',
 '- [NUMBERS]('+url+'NUMBERS_ACD.md)','',
 'Resolution rules:','']+['- '+v for v in resolutions])+'\n'
 (ROOT/'receipts/acd_stage10_vault.md').write_text(note)
 (Path('/home/todd/obsidian-vault/04-Results')/'R_Aspen-Counterfactual-Determinacy-Stage10-2026-10.md').write_text(note)
 print('Stage10 report, receipt and vault note written; verification PASS',flush=True)
if __name__=='__main__':run()
