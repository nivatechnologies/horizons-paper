"""Receipt-only Freeze D reading; every displayed value comes from a receipt."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent


def f(value):
    return 'pending' if value is None else f'{value:.6g}'


def interval(row):
    if row is None:
        return 'not evaluable'
    return f"{f(row['point'])} [{f(row['lower'])}, {f(row.get('upper'))}]"


def render():
    data = json.loads((ROOT/'receipts/acd_stage19_part3b.json').read_text())
    body = '\n## Part 3b — inferred-context repair\n\n'
    body += 'Fresh readings use pushed Freeze D; first-panel readings are post hoc. No frozen route is licensed. Every instance uses all its draws; an invalid draw invalidates that pipeline instance. Seed variation is separate from instance-level uncertainty. Realized counts were already computed in Part2; this scoring uses only its existing cache.\n\n'
    body += '| Reading | Fresh result | Outcome | Bound type |\n|---|---|---|---|\n'
    for key in ['B1','B3','B4']:
        row = data[key]
        body += f"| {key} | {interval(row['interval'])} | {'not evaluable' if not row['evaluable'] else 'PASS' if row['confirmed'] else 'FAIL'} | {row['interval']['bound_type'] if row['interval'] else 'none'} |\n"
    b2 = data['B2']
    body += f"| B2 | all E0 seeds | {'not evaluable' if not b2['evaluable'] else 'PASS' if b2['confirmed'] else 'FAIL'} | {b2['bound_type']} |\n"
    body += '\n| E0 seed | Actions at 3 LT | Strict-positive harms | Exact zero-effect ties | Harm upper | Outcome |\n|---|---:|---:|---:|---:|---|\n'
    for row in b2['per_seed']:
        body += f"| {row['seed']} | {row['actions_taken']} | {row['harms']} | {row['zero_effect_ties']} | {f(row['CP95'][1])} | {'PASS' if row['confirmed'] else 'FAIL'} |\n"
    body += '\nP0 minus retained CNN-F is descriptive only: '+interval(data['P0_minus_CNN_F_descriptive']['interval'])+'. No equivalence claim is made.\n\n'
    body += '| Pipeline | Lead | First / fresh S confident share | First / fresh pooled S error | First / fresh case S error | Fresh case error bounds | First / fresh state RMSE/sigma | First / fresh state ACC |\n|---|---:|---:|---:|---:|---:|---:|---:|\n'
    for name, model in data['models'].items():
        old = data['first_panel'].get(name)
        for row in model['confidence_readings']:
            previous = next((r for r in old['confidence_readings'] if r['lead']==row['lead']),None) if old else None
            skill = next(r for r in model['state_skill'] if r['lead']==row['lead'])
            prior_skill = next((r for r in old['state_skill'] if r['lead']==row['lead']),None) if old else None
            def value(key):
                return f(previous.get(key)) if previous else 'pending'
            a = previous['all_confident_accuracy'] if previous else None
            prior_error = f(1-a['answer_accuracy']) if a and a['answer_accuracy'] is not None else 'pending'
            prior_case = f(1-a['case_accuracy']) if a and a['case_accuracy'] is not None else 'pending'
            body += f"| {name} | {f(row['lead'])} | {value('confident_S_share')} / {f(row['confident_S_share'])} | {prior_error} / {f(row['pooled_confident_error'])} | {prior_case} / {f(row['case_confident_error'])} | [{f(row['case_error_lower'])}, {f(row['case_error_upper'])}] | {f(prior_skill['window_mean_RMSE_over_sigma']) if prior_skill else 'pending'} / {f(skill['window_mean_RMSE_over_sigma'])} | {f(prior_skill['window_mean_anomaly_correlation']) if prior_skill else 'pending'} / {f(skill['window_mean_anomaly_correlation'])} |\n"
    body += '\nConfidence/error population: all eight intervention patterns at each lead; case bounds are v2.3 one-sided95%, each direction reported. Primary contrasts use seven zero-mean patterns and pair-specific contributing instances. Pooled error is descriptive. State metrics average sites within ticks, ticks within the window, then instances, as implemented by the unchanged scorer.\n\n'
    body += '| Pipeline | First / fresh cutoff F RMSE | First / fresh bias | First / fresh correlation |\n|---|---:|---:|---:|\n'
    for name, model in data['models'].items():
        row = model.get('forcing_estimate_error')
        if row is None:
            continue
        old = (data['first_panel'].get(name) or {}).get('forcing_estimate_error')
        body += '| '+name+' | '+' | '.join(f"{f(old[k]) if old else 'pending'} / {f(row[k])}" for k in ['RMSE','bias','correlation'])+' |\n'
    body += '\nForcing errors pool draw/action values at the cutoff, including for rolling pipelines; they do not describe subsequent predicted-window estimation errors.\n\n'
    body += '| Pipeline | Lead | Quantity | First / fresh equal-case RMSE | First / fresh equal-case bias | Fresh pooled RMSE | Fresh pooled bias |\n|---|---:|---|---:|---:|---:|---:|\n'
    for name, model in data['models'].items():
        old = data['first_panel'].get(name)
        for row in model['per_draw_cost_errors']:
            prior = next((r for r in old['per_draw_cost_errors'] if r['lead']==row['lead'] and r['quantity']==row['quantity']),None) if old else None
            body += f"| {name} | {f(row['lead'])} | {row['quantity']} | {f(prior.get('RMSE',prior.get('equal_case_RMSE'))) if prior else 'pending'} / {f(row['equal_case_RMSE'])} | {f(prior.get('bias',prior.get('equal_case_bias'))) if prior else 'pending'} / {f(row['equal_case_bias'])} | {f(row['pooled_RMSE'])} | {f(row['pooled_bias'])} |\n"
    body += '\n| Pipeline | Lead | Policy | First / fresh regret | First / fresh capture | Fresh actions | Fresh harms | Conditional harm bounds | Uniform every instance | Histogram |\n|---|---:|---|---:|---:|---:|---:|---|---|---|\n'
    for name, model in data['models'].items():
        old = data['first_panel'].get(name)
        for row in model['decisions']:
            if row['policy'] not in ['E','C_delta_0']:
                continue
            prior = next((r for r in old['decisions'] if r['lead']==row['lead'] and r['policy']==row['policy']),None) if old else None
            body += f"| {name} | {f(row['lead'])} | {row['policy']} | {f(prior.get('mean_regret')) if prior else 'pending'} / {f(row.get('mean_regret'))} | {f(prior.get('capture_fraction')) if prior else 'pending'} / {f(row.get('capture_fraction'))} | {row['actions_taken']} | {row['strict_positive_harms']} | {row['conditional_harm_CP95']} | {row['uniform_decrease_every_case']} | {row['chosen_actions']} |\n"
    body += '\nConditional harm limits are exact one-sided95% Clopper–Pearson bounds, with strictly positive harms and zero ties separately in the receipt. Histograms retain all nine options.\n\n'
    body += '| Pipeline | First / fresh own-cohort paired interval | Fresh calibration intervals by lead/threshold |\n|---|---|---|\n'
    for name, model in data['models'].items():
        old = data['first_panel'].get(name)
        body += f"| {name} | {json.dumps(old['paired_endpoint']) if old else 'pending'} / {json.dumps(model['paired_endpoint'])} | {json.dumps(model['calibration_test'])} |\n"
    body += '\nOwn-cohort paired and mean-calibration intervals are two-sided99% v2.3 instance betting intervals. Full reliability, coverage, counts, seed-level contrasts, unavailable-pipeline records and first-panel fields are in receipts/acd_stage19_part3b.json. First-panel matched Stage16/E0 pipelines not yet scored remain pending; no replacement value is supplied.\n'
    body += '\n| Pipeline | Lead | Group | Confident share | Share wrong | Equal-case D bias | Pooled D bias |\n|---|---:|---|---:|---:|---:|---:|\n'
    for name,model in data['models'].items():
        for row in model.get('pattern_group_readings',[]):
            body += '| '+name+' | '+' | '.join(f(row[k]) if isinstance(row[k],(int,float)) or row[k] is None else str(row[k]) for k in ['lead','population','confident_share','share_wrong','equal_case_Dk_bias','pooled_Dk_bias'])+' |\n'
    path = ROOT/'ACD_STAGE19_READING.md'
    previous = path.read_text()
    marker = '\n## Part 3b — inferred-context repair\n'
    if marker in previous:
        a,b = previous.split(marker,1)
        next_section = b.find('\n## ')
        previous = a+(b[next_section:] if next_section>=0 else '')
    path.write_text(previous.rstrip()+'\n'+body)


if __name__ == '__main__':
    render()

