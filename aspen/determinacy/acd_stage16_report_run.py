"""Publish one completed Stage16 run from saved scoring and training records only."""
import json,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def run(name):
 metrics_path=ROOT/f'runs/stage16/metrics_{name}.json';metrics=json.loads(metrics_path.read_text())
 train_path=ROOT/f'runs/stage9_training/{name}/complete.json'
 if train_path.exists():training=json.loads(train_path.read_text());training_source=str(train_path.relative_to(ROOT))
 elif name=='CNN-F':training=json.loads((ROOT/'receipts/acd_stage9.json').read_text())['F'][name];training_source='receipts/acd_stage9.json $.F.CNN-F'
 else:raise RuntimeError('Training metadata missing for '+name)
 freeze=json.loads((ROOT/'receipts/acd_stage16_freeze.json').read_text());entry=next((x for x in freeze['runs'] if x['name']==name),None)
 model=entry['model'] if entry else name
 receipt=dict(post_hoc=True,licenses_frozen_route=False,model=model,run=name,baseline=entry is None,seed_index=entry['seed_index'] if entry else 0,host=entry['host'] if entry else 'retained baseline',training=training,metrics=metrics,training_source=training_source,metrics_source=str(metrics_path.relative_to(ROOT)),metrics_sha256=hashlib.sha256(metrics_path.read_bytes()).hexdigest())
 (ROOT/f'receipts/acd_stage16_run_{name}.json').write_text(json.dumps(receipt,indent=2,allow_nan=False)+'\n')
 lines=['# Stage 16 run: '+name,'','Post hoc on confirmation; licenses no frozen route. Every run is reported, without selection among seeds. Case-level uncertainty and training-run variation are separate.','', '| Lead | State RMSE/sigma | State ACC | S confidence | Pooled S error | Case S error | Case error lower | Case error upper |','|---|---:|---:|---:|---:|---:|---:|---:|']
 for r in metrics['confidence_readings']:
  skill=next(x for x in metrics['state_skill'] if x['lead']==r['lead']);a=r['all_confident_accuracy'];values=[r['lead'],skill['window_mean_RMSE_over_sigma'],skill['window_mean_anomaly_correlation'],r['confident_S_share'],1-a['answer_accuracy'],1-a['case_accuracy'],1-a['case_upper'],1-a['case_lower']]
  lines.append('| '+' | '.join(map(str,values))+' |')
 lines+=['','| Lead | Policy | Regret | Capture | Harms | Acting share | Chosen-action histogram |','|---|---|---:|---:|---:|---:|---|']
 for r in metrics['decisions']:lines.append('| '+' | '.join(map(str,[r['lead'],r['policy'],r['mean_regret'],r['capture_fraction'],r['harms'],r['acting_share'],r['chosen_actions']]))+' |')
 lines+=['','| Lead | Patterns | Coverage | Answers | Pooled error | Case error |','|---|---|---:|---:|---:|---:|']
 for r in metrics['matched_coverage']['rows']:lines.append('| '+' | '.join(map(str,[r['lead'],r['patterns'],r['target_coverage'],r['answers'],r['pooled_error'],r['case_error']]))+' |')
 lines+=['','Uniform-decrease collapse for E: '+json.dumps(metrics['uniform_decrease_collapse'])+'.','', 'All training times, selected steps, guard outcomes, per-draw cost errors, confidence bounds, calibration tests, paired endpoints and histograms remain in the full receipt.','']
 (ROOT/f'ACD_STAGE16_RUN_{name}.md').write_text('\n'.join(lines))
 print(json.dumps(dict(run=name,receipt=f'receipts/acd_stage16_run_{name}.json',reading=f'ACD_STAGE16_RUN_{name}.md')))
if __name__=='__main__':run(sys.argv[1])
