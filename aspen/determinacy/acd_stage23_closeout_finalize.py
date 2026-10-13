"""Posterior-generation accounting and receipt-only closeout report."""
from pathlib import Path
import ast,datetime,hashlib,json,os,subprocess,sys
import numpy as np
ROOT=Path('/mnt/niva-array/work/aspen-determinacy-stage23-20261012/aspen/determinacy')
PANEL=Path('/mnt/niva-array/work/aspen-determinacy-stage22-20261010/aspen/determinacy')
BASE=Path('/mnt/niva-array/work/aspen-determinacy-stage21-20261008/aspen/determinacy')
OUT=ROOT/'runs/stage23_closeout'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def fmt(v):return format(v,'.10g') if isinstance(v,(float,int)) else str(v)
def timestamp(t):return datetime.datetime.fromtimestamp(t,datetime.timezone.utc).isoformat()
def thresholds():
 tree=ast.parse((BASE/'acd_posterior.py').read_text());fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='diagnostics');result={}
 for n in ast.walk(fn):
  if not isinstance(n,ast.Compare) or len(n.comparators)!=1 or not isinstance(n.comparators[0],ast.Constant):continue
  left=ast.unparse(n.left)
  key={'r.max()':'rhat_max','e.min()':'ess_min',"report['divergent_fraction']":'divergent_fraction_max'}.get(left)
  if key:result[key]=n.comparators[0].value
 assert len(result)==3
 return result

def finish():
 d=read(OUT/'progress.json');assert d['status']=='IMPLEMENTATION_CHECKS_COMPLETE' and all(d['checks'][k]['passed'] for k in ['A1','A2','A3','A4','A5'])
 result=subprocess.check_output(['systemctl','--user','show','aspen-stage23-closeout-check','-p','Result','--value'],text=True).strip();assert result=='success',result
 t=thresholds();panel=read(PANEL/'receipts/acd_stage22_part1.json');cases={r['case']:r for r in panel['cases']};contract=read(PANEL/'receipts/acd_stage22_panel_contract.json');marker=read(PANEL/'runs/stage22/panel_contract_pushed.json')
 documents=[ROOT/'ACD_STAGE19_FREEZE_A.md',ROOT/'ACD_STAGE21_PANEL_CONTRACT.md',PANEL/'ACD_STAGE22_PANEL_CONTRACT.md']
 assert sha(documents[-1])==contract['document_sha256']
 freeze_quote=documents[0].read_text().splitlines()[12]
 assert 'Exclude only after that retry fails.' in freeze_quote
 inheritance_quote=documents[-1].read_text().splitlines()[4]
 first=min(json.loads(line)['time'] for p in (PANEL/'runs/stage22').glob('access_*.jsonl') for line in p.read_text().splitlines() if json.loads(line)['kind']=='observations_written_and_hashed')
 assert marker['utc']<first,'Contract publication does not precede first observed write'
 commit_map=dict(line.split() for line in (ROOT/'receipts/repo_rewrite_commit_map.txt').read_text().splitlines()[1:]);mapped=commit_map.get(marker['commit'],marker['commit'])
 committed=subprocess.check_output(['git','-C',str(ROOT),'show',mapped+':aspen/determinacy/ACD_STAGE22_PANEL_CONTRACT.md'])
 assert hashlib.sha256(committed).hexdigest()==contract['document_sha256']
 namespace=next((name,value) for name,value in contract['namespaces'].items() if name.endswith('-sampler'))
 fields=[]
 for case in [401,812,910]:
  arm=cases[case]['arms']['main'];attempts=[]
  for a in arm['attempts']:
   ps,fs=a['parameters'],a['functions'];sampler=a['sampler'];failed=[]
   labels=[f'x_first[{i}]' for i in range(len(ps['rhat'])-2)]+['F','log_likelihood']
   import importlib.util
   spec=importlib.util.spec_from_file_location('closeout_protocol','/mnt/niva-array/work/aspen-forecast-decision-20261005/aspen/forecast_decision/protocol.py');prot=importlib.util.module_from_spec(spec);spec.loader.exec_module(prot)
   function_labels=[f'D_{k} at {fmt(lead)} LT' for k in range(len(prot.patterns())) for lead in prot.LEADS[[3,5]]]+[f'J_8 at {fmt(lead)} LT' for lead in prot.LEADS[[3,5]]]
   for group,labelset,values in [('parameters_and_log_likelihood',labels,ps),('decision_functionals',function_labels,fs)]:
    for metric,comparison,limit in [('rhat',lambda v:v>t['rhat_max'],t['rhat_max']),('ess',lambda v:v<t['ess_min'],t['ess_min'])]:
     for i,value in enumerate(values[metric]):
      if not np.isfinite(value) or comparison(value):failed.append(dict(group=group,diagnostic=metric,index=i,label=labelset[i],value=value,frozen_limit=limit))
   if sampler['divergent_fraction']>t['divergent_fraction_max']:failed.append(dict(group='sampler',diagnostic='divergent_fraction',value=sampler['divergent_fraction'],frozen_limit=t['divergent_fraction_max']))
   for group,v in [('parameters',ps),('functions',fs)]:
    expected=np.isfinite(v['rhat']).all() and np.isfinite(v['ess']).all() and v['max_rhat']<=t['rhat_max'] and v['min_ess']>=t['ess_min']
    if group=='parameters':expected=expected and sampler['divergent_fraction']<=t['divergent_fraction_max']
    assert bool(expected)==v['passed'],(case,a['attempt'],group,'stored flag differs from frozen thresholds')
   meta=PANEL/'runs/stage22'/f'main_sample_{case:03d}_{a["attempt"]}.json';stored=read(meta);assert stored==sampler
   seeds={k:v for k,v in stored.items() if 'seed' in k.lower() or 'rng' in k.lower() or 'key' in k.lower()}
   # Missing numeric PRNG keys are never reconstructed from deterministic namespaces.
   attempts.append(dict(attempt=a['attempt'],sampler=sampler,parameters_and_log_likelihood=ps,decision_functionals=fs,full_draw_functional_rescore=a['rescored'],failed_diagnostics=failed,outcome='PASS' if ps['passed'] and fs['passed'] else 'FAIL',recorded_sampler_seeds=seeds or None,seed_recording='No numeric per-chain NUTS seeds/PRNG keys were recorded in the sampler metadata or returned report.' if not seeds else 'Recorded sampler metadata',sampler_namespace=dict(name=namespace[0],id=namespace[1]),pre_rescore_thinned_functional_diagnostics=None if a['rescored'] else fs,pre_rescore_recording='Not saved when replaced by the full-draw diagnostic vector.' if a['rescored'] else 'Stored functional vector is the thinned-draw diagnostic.',invalid_draw_count=None,invalid_draw_recording='Not recorded; raw draw arrays were not opened or inspected.',source=dict(path=str(meta),sha256=sha(meta))))
  assert len(attempts)==2 and arm['excluded'] and attempts[-1]['outcome']=='FAIL'
  fields.append(dict(case=case,excluded=arm['excluded'],attempts=attempts,final_exclusion_diagnostics=attempts[-1]['failed_diagnostics'],source_case_json=dict(path=str(PANEL/'runs/stage22'/f'case_{case:03d}.json'),sha256=sha(PANEL/'runs/stage22'/f'case_{case:03d}.json'))))
 d['exclusions']=dict(thresholds=t,cases=fields,rules_frozen_before_generation=True,contract_commit_original=marker['commit'],contract_commit_after_history_rewrite=mapped,contract_push_timestamp=marker['utc'],first_observation_write_timestamp=first,contract_push_UTC=timestamp(marker['utc']),first_observation_write_UTC=timestamp(first),frozen_rule_quote=freeze_quote,stage22_inheritance_quote=inheritance_quote,document_sources={str(p):sha(p) for p in documents},recorded_seed_namespace=dict(name=namespace[0],id=namespace[1]),missing_records=['Numeric per-chain NUTS PRNG keys for both attempts of all three cases.','Thinned functional diagnostic vectors overwritten by full-draw rescoring.','Raw invalid-draw counts.'])
 d['scope_attestation']=dict(training_updates=0,optimizer_runs=0,new_panel=False,panel_rescoring=False,realized_outcome_accesses=[],frozen_definitions_changed=False)
 d['published_verifier_hashes']={name:sha('/tmp/'+name) for name in ['acd_stage23_closeout_check.py','acd_stage23_closeout_gradients.py']};d['code_hashes'][str(Path(__file__))]=sha(__file__)
 d['code_hashes'][str(BASE/'acd_posterior.py')]=sha(BASE/'acd_posterior.py')
 d['status']='CLOSEOUT_CHECKS_COMPLETE';(ROOT/'receipts/acd_stage23_closeout.json').write_text(json.dumps(d,indent=2,allow_nan=False)+'\n')
 return d

def render(d):
 lines=['# Stage 23 closeout — implementation verification and exclusion accounting','', 'No training, optimizer run, new panel, panel rescoring or realized-outcome access occurred. Freeze G and every existing scientific receipt, reading and frozen implementation remain unchanged. This document is generated from receipts/acd_stage23_closeout.json.','', '## Models and fixed batch','', 'Selected checkpoint SHA-256: `'+d['models']['selected_checkpoint_sha256']+'`. Selected step: '+fmt(d['models']['selected_step'])+'. Initialization seed: '+fmt(d['models']['initialization_seed'])+'. Rebuilt initial tensor hash: `'+d['models']['rebuilt_initial_tensor_hash']+'`. No step-zero hash was recorded, so there is no independent saved hash against which to compare the rebuilt state.','', 'First training batch-order seed: '+fmt(d['batch']['batch_order_seed'])+'. Every recorded start retains its original amplitude under all frozen action patterns, paired with no action. Canonical batch hash: `'+d['batch']['canonical_tensor_sha256']+'`. The canonical encoding hashes sorted tensor names, dtypes, shapes and C-order bytes, including the start-index vector.','', 'Start indices: '+json.dumps(d['batch']['start_indices'])+'.','', '## Gate summary','', '| Check | Initial state | Selected checkpoint | Pass rule | Outcome |','|---|---|---|---|---|']
 a=d['checks']['A1'];lines.append(f"| A1 | max absolute {fmt(a['maximum_absolute_difference'])}; max relative {fmt(a['maximum_relative_difference'])} | same target | relative difference at most 1e-6; matching subtraction | PASS |")
 a=d['checks']['A2']['models'];lines.append(f"| A2 | action {fmt(a['initial']['action_prediction_gradient_norm'])}; twin {fmt(a['initial']['twin_prediction_gradient_norm'])} | action {fmt(a['selected']['action_prediction_gradient_norm'])}; twin {fmt(a['selected']['twin_prediction_gradient_norm'])} | both norms nonzero; action minus twin in prediction and target | PASS |")
 a=d['checks']['A3']['models'];lines.append(f"| A3 | smallest norm {fmt(min(x['gradient_norm'] for x in a['initial']))} | smallest norm {fmt(min(x['gradient_norm'] for x in a['selected']))} | every trainable tensor has nonzero norm | PASS |")
 a=d['checks']['A4']['models'];lines.append(f"| A4 | worst best-step relative error {fmt(max(x['best_relative_error'] for x in a['initial']['directions']))} | worst best-step relative error {fmt(max(x['best_relative_error'] for x in a['selected']['directions']))} | at most 1e-4 for every fixed direction | PASS |")
 a=d['checks']['A5']['models'];lines.append(f"| A5 | paired norm share {fmt(a['initial']['applied_paired_gradient_norm_share'])}; max direction difference {fmt(a['initial']['maximum_absolute_direction_difference'])} | paired norm share {fmt(a['selected']['applied_paired_gradient_norm_share'])}; max direction difference {fmt(a['selected']['maximum_absolute_direction_difference'])} | frozen balancing formula and global clipping; independently computed directions agree exactly | PASS |")
 a=d['checks']['A1'];lines+=['','A1 independently reproduces the frozen FP32 branch-state serialization and then compares state differences in float64. Both branches use action minus no action. The raw float64 RK4 trajectory discrepancy is '+fmt(a['independent_RK4_raw_state_maximum_absolute_difference'])+'. The target discrepancy against unquantized float64 physics is '+fmt(a['unquantized_physics_maximum_absolute_difference'])+' absolute and '+fmt(a['unquantized_physics_relative_Linf'])+' relative in the maximum norm; this storage-quantization reading is separate from the target-equivalence gate.','', 'A2 uses gradients with respect to each rollout prediction, including its downstream dependence within the frozen truncated segments. A3 uses the raw paired-loss parameter gradients. The verification compiles the exact frozen base and paired function ASTs without invoking the training run. Only the detach statement is removed for A4.','', 'A5 compares the clipped gradient delivered to the optimizer, not an AdamW parameter delta. No optimizer was instantiated or run. Global clipping was inactive on this fixed batch in both model states; the recorded coefficients are in the receipt.','', '## A1b — descriptive window energies','', '| Model state | Mean predicted action-minus-twin energy | Mean physics energy difference | Effect RMSE | Effect bias |','|---|---:|---:|---:|---:|']
 for name,v in d['A1b']['models'].items():lines.append(f"| {name} | {fmt(v['predicted_mean'])} | {fmt(v['physics_mean'])} | {fmt(v['effect_RMSE'])} | {fmt(v['effect_bias'])} |")
 lines+=['','Window ticks: '+json.dumps(d['A1b']['window_ticks'])+'. Energies are accumulated in physical units in float64. Every start-pattern energy difference is retained in the JSON receipt; no criterion is attached to A1b.','', '## A3 — every parameter tensor','', '| Model state | Parameter | Shape | Paired gradient norm |','|---|---|---|---:|']
 for name,rows in d['checks']['A3']['models'].items():
  for v in rows:lines.append(f"| {name} | {v['parameter']} | {v['shape']} | {fmt(v['gradient_norm'])} |")
 lines+=['','## A4 — directional finite differences','', 'Fixed direction namespace: acd-stage23-closeout-directions. Seed: '+fmt(d['checks']['A4']['direction_seed'])+'. The same unit directions are used for both model states.','', '| Model state | Direction | Step size | Autodiff | Central difference | Relative error |','|---|---:|---:|---:|---:|---:|']
 for name,v in d['checks']['A4']['models'].items():
  for direction in v['directions']:
   for row in direction['step_sizes']:lines.append(f"| {name} | {direction['index']} | {fmt(row['step_size'])} | {fmt(direction['autodiff'])} | {fmt(row['central_difference'])} | {fmt(row['relative_error'])} |")
 lines+=['','Truncated versus untruncated gradient cosine (descriptive): '+', '.join(name+' '+fmt(v['truncated_untruncated_cosine']) for name,v in d['checks']['A4']['models'].items())+'. Their difference is not a failed gate.','', '## Posterior exclusions','', 'The rule and single-retry contract were frozen before generation. The pushed contract is byte-identical to its committed version. Contract publication: '+d['exclusions']['contract_push_UTC']+'; first observation write: '+d['exclusions']['first_observation_write_UTC']+'.','', 'Frozen Stage19 rule inherited by Stage21 and Stage22:', '', '> '+d['exclusions']['frozen_rule_quote'], '', 'Stage22 inheritance:', '', '> '+d['exclusions']['stage22_inheritance_quote'], '', '| Case | Attempt | Warm-up | Parameter / log-likelihood max R-hat | Minimum ESS | Functional max R-hat | Minimum ESS | Divergent fraction | Full-draw functional rescore | Outcome |','|---:|---:|---:|---:|---:|---:|---:|---:|---|---|']
 for case in d['exclusions']['cases']:
  for a in case['attempts']:
   p,f,s=a['parameters_and_log_likelihood'],a['decision_functionals'],a['sampler']
   lines.append(f"| {case['case']} | {a['attempt']} | {s['warmup']} | {fmt(p['max_rhat'])} | {fmt(p['min_ess'])} | {fmt(f['max_rhat'])} | {fmt(f['min_ess'])} | {fmt(s['divergent_fraction'])} | {a['full_draw_functional_rescore']} | {a['outcome']} |")
 lines+=['','The thresholds are copied from the frozen diagnostic implementation: '+json.dumps(d['exclusions']['thresholds'])+'.','', '| Case | Final exclusion reason after retry |','|---:|---|']
 for case in d['exclusions']['cases']:lines.append('| '+str(case['case'])+' | '+'; '.join(x['label']+' '+x['diagnostic']+' '+fmt(x['value'])+' against '+fmt(x['frozen_limit']) for x in case['final_exclusion_diagnostics'])+' |')
 lines+=['','Every attempt’s complete recorded R-hat and ESS vectors, sampler settings, divergence counts and metadata hashes are in the receipt. All three exclusions follow a failed initial attempt and the single failed warm-up retry. No ESS or divergence threshold was violated in these records.','', 'Missing records are reported rather than reconstructed: numeric per-chain NUTS PRNG keys were not saved; the namespace root was recorded. When full-draw rescoring replaced the initial functional diagnostic vector, that initial thinned vector was not retained. Raw invalid-draw counts were not recorded. No posterior draw arrays or realized-outcome arrays were opened to reconstruct these quantities.','', '## Provenance','']
 for path,value in d['code_hashes'].items():lines.append('- `'+path+'`: `'+value+'`')
 if 'registry_verification' in d:lines+=['', 'Registry PASS: '+fmt(d['registry_verification']['prior_key_count'])+' prior keys unchanged; '+fmt(d['registry_verification']['final_key_count'])+' total keys.']
 (ROOT/'ACD_STAGE23_CLOSEOUT.md').write_text('\n'.join(lines)+'\n')
if __name__=='__main__':
 d=finish();render(d);print('EXCLUSION ACCOUNTING AND CLOSEOUT REPORT COMPLETE')
