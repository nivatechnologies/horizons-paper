"""Append learned fresh/original tables using receipts only; preserve reference prose."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def f(value):
    return '—' if value is None else f'{value:.6g}'


def run():
    fresh = json.loads((ROOT/'receipts/acd_stage19_learned.json').read_text())
    original_test = json.loads((ROOT/'receipts/acd_stage19_original_learned.json').read_text())
    original = json.loads((ROOT/'receipts/acd_stage9.json').read_text())['C']
    original['CNN-noF'] = json.loads((ROOT/'receipts/acd_stage10b.json').read_text())['models']['CNN-noF']
    decisions = json.loads((ROOT/'receipts/acd_stage10b_decisions.json').read_text())['models']
    body = '\n## Freeze B learned readings\n\n'
    body += 'The original-panel values are post hoc; fresh-panel L1 and L2 use the pushed Freeze B criteria. No frozen route is licensed. Invalid instances are withheld without conditioning on survivors.\n\n'
    body += '| Reading | Original confirmation | Fresh panel | Fresh outcome |\n|---|---:|---:|---|\n'
    for label in ['L1', 'L2']:
        old, new = original_test[label], fresh[label]
        if label == 'L1':
            render = lambda r: f"{f(r['interval']['point'])} [{f(r['interval']['lower'])}, {f(r['interval']['upper'])}]; {r['cases']} instances"
        else:
            render = lambda r: f"{r['harms']}/{r['actions_taken']} harms/acted; lower {f(r['conditional_harm_CP95'][0])}"
        body += f"| {label} | {render(old)} | {render(new)} | {'PASS' if new['confirmed'] else 'FAIL'} |\n"
    body += '\nL1 uses a two-sided 99% instance betting interval on CNN-noF minus CNN-F seven-pattern confident wrong share. L2 uses an exact one-sided 95% Clopper–Pearson lower bound for CNN-noF C(delta=0) harm conditional on acting at three LT. L3 awaits all frozen Stage16 checkpoints and remains descriptive.\n\n'
    body += '| Model | Lead (LT) | Original / fresh S confident share | Original / fresh pooled S error | Original / fresh case S error | Fresh case error interval | Original / fresh F_c confident share | Fresh F_c case accuracy |\n|---|---:|---:|---:|---:|---:|---:|---:|\n'
    for name, model in fresh['models'].items():
        for row in model['confidence_readings']:
            old = next(r for r in original[name]['confidence_readings'] if r['lead'] == row['lead'])
            a, b = old['all_confident_accuracy'], row['all_confident_accuracy']
            body += f"| {name} | {f(row['lead'])} | {f(old['confident_S_share'])} / {f(row['confident_S_share'])} | {f(1-a['answer_accuracy'])} / {f(1-b['answer_accuracy'])} | {f(1-a['case_accuracy'])} / {f(1-b['case_accuracy'])} | [{f(row['case_error_lower'])}, {f(row['case_error_upper'])}] | {f(old['confident_Fc_share'])} / {f(row['confident_Fc_share'])} | {f(row['Fc_accuracy']['case_accuracy'])} |\n"
    body += '\nCase accuracy/error bounds use v2.3 one-sided 95% bounds; the two directions are reported together. Pooled answer error is descriptive.\n\n'
    body += '| Model | Lead | Original / fresh RMSE/sigma | Original / fresh anomaly correlation |\n|---|---:|---:|---:|\n'
    for name, model in fresh['models'].items():
        for row in model['state_skill']:
            old = next(r for r in original[name]['state_skill'] if r['lead'] == row['lead'])
            body += f"| {name} | {f(row['lead'])} | {f(old['window_mean_RMSE_over_sigma'])} / {f(row['window_mean_RMSE_over_sigma'])} | {f(old['window_mean_anomaly_correlation'])} / {f(row['window_mean_anomaly_correlation'])} |\n"
    body += '\nFactual state skill is averaged over each scored window and over instances.\n\n'
    body += '| Model | Lead | Quantity | Original / fresh equal-case RMSE | Original / fresh equal-case bias | Fresh pooled RMSE | Fresh pooled bias |\n|---|---:|---|---:|---:|---:|---:|\n'
    for name, model in fresh['models'].items():
        for row in model['per_draw_cost_errors']:
            old = next((r for r in original[name]['per_draw_cost_errors'] if r['lead'] == row['lead'] and r['quantity'] == row['quantity']), None)
            old_rmse = None if old is None else old['RMSE']['mean']
            old_bias = None if old is None else old['bias']['mean']
            body += f"| {name} | {f(row['lead'])} | {row['quantity']} | {f(old_rmse)} / {f(row['equal_case_RMSE'])} | {f(old_bias)} / {f(row['equal_case_bias'])} | {f(row['pooled_RMSE'])} | {f(row['pooled_bias'])} |\n"
    body += '\nDraw-cost errors compare each model with the same draw’s physics forecast.\n\n'
    body += '| Model | Lead | Original / fresh seven-pattern S share minus F_c | Fresh betting 99% interval |\n|---|---:|---:|---:|\n'
    for name, model in fresh['models'].items():
        for row in model['comparisons']:
            old = next(r for r in original[name]['comparisons'] if r['lead'] == row['lead'])
            interval = row['seven_minus_Fc']
            body += f"| {name} | {f(row['lead'])} | {f(old['seven_minus_Fc']['point'])} / {f(interval['point'])} | [{f(interval['lower'])}, {f(interval['upper'])}] |\n"
    body += '\n| Model | Original / fresh fixed-posterior-cohort paired difference | Fresh betting 99% interval | Original / fresh pairs |\n|---|---:|---:|---:|\n'
    for name, model in fresh['models'].items():
        old = original[name]['paired_endpoint_fixed_posterior_cohort']
        new = model['paired_endpoint_fixed_posterior_cohort']
        interval = new['interval']
        body += f"| {name} | {f(old['interval']['point'])} / {f(interval['point'])} | [{f(interval['lower'])}, {f(interval['upper'])}] | {old['pairs']} / {new['pairs']} |\n"
    body += '\nThe fixed cohort is determined by each panel’s posterior at lead zero; the original and fresh cohorts have their own sizes.\n\n'
    body += '| Model | Lead | Policy | Original / fresh regret | Fresh capture | Fresh acted | Fresh harms | Conditional harm CP95 |\n|---|---:|---|---:|---:|---:|---:|---:|\n'
    for name, model in fresh['models'].items():
        for row in model['decisions']:
            if row['policy'] not in ['E', 'C_delta_0']:
                continue
            old = next(r for r in decisions[name]['readings'] if r['lead'] == row['lead'] and r['policy'] == row['policy'])
            bounds = row['conditional_harm_CP95']
            body += f"| {name} | {f(row['lead'])} | {row['policy']} | {f(old['mean_regret'])} / {f(row['mean_regret'])} | {f(row['capture_fraction'])} | {row['actions_taken']} | {row['harms']} | [{f(bounds[0])}, {f(bounds[1])}] |\n"
    body += '\nBoth conditional harm bounds are exact one-sided 95% bounds. Strict positive realized cost differences count as harm; acted zero-effect ties are recorded separately in the receipt.\n\n'
    body += 'Additional state skill, draw-level errors, reliability bins, calibration tests, same-lead differences and paired endpoints are recorded without selection in receipts/acd_stage19_learned.json.\n'
    path = ROOT/'ACD_STAGE19_READING.md'
    existing = path.read_text()
    marker = '\n## Freeze B learned readings\n'
    existing = existing.split(marker)[0]
    path.write_text(existing.rstrip()+'\n'+body)


if __name__ == '__main__':
    run()
