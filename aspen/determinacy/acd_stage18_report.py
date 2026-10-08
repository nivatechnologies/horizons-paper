"""Render Stage18 lettered results from saved scoring receipts only."""
import argparse,json
import numpy as np
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def fmt(x):return '—' if x is None else format(x,'.6g')

def run(letter,names):
    entries={n:json.loads((ROOT/'receipts'/f'acd_stage18_{n}.json').read_text()) for n in names}
    summaries=[]
    if letter=='B':
        for arm in ['CNN-F-E0-fixed','CNN-F-E1-fixed','CNN-F-E1-rolling']:
            members=[m for n,m in entries.items() if n.rsplit('-seed',1)[0]==arm]
            for lead in sorted({r['lead'] for m in members for r in m['confidence_readings']}):
                rows=[next(r for r in m['confidence_readings'] if r['lead']==lead) for m in members]
                values={
                    'confident_S_share':[r['confident_S_share'] for r in rows],
                    'pooled_confident_S_error':[1-r['all_confident_accuracy']['answer_accuracy'] for r in rows],
                    'case_confident_S_error':[1-r['all_confident_accuracy']['case_accuracy'] for r in rows],
                    'E_regret':[next(r['mean_regret'] for r in m['decisions'] if r['lead']==lead and r['policy']=='E') for m in members],
                    'C_regret':[next(r['mean_regret'] for r in m['decisions'] if r['lead']==lead and r['policy']=='C_delta_0') for m in members]}
                for key in ['window_mean_RMSE_over_sigma','window_mean_anomaly_correlation']:
                    values[key]=[next(r[key] for r in m['state_skill'] if r['lead']==lead) for m in members]
                for quantity in ['J8','Dk']:
                    for key in ['RMSE','bias']:
                        values[quantity+'_'+key]=[next(r[key]['mean'] for r in m['per_draw_cost_errors'] if r['lead']==lead and r['quantity']==quantity) for m in members]
                values['seven_pattern_same_lead_difference']=[next(r['seven_minus_Fc']['point'] for r in m['comparisons'] if r['lead']==lead) for m in members]
                values['fixed_cohort_paired_endpoint']=[m['paired_endpoint_fixed_posterior_cohort']['interval']['point'] for m in members]
                for policy in ['E','C_delta_0']:
                    for key in ['capture_fraction','harms','actions_taken']:
                        values[policy+'_'+key]=[next(r[key] for r in m['decisions'] if r['lead']==lead and r['policy']==policy) for m in members]
                for key in ['RMSE','bias','correlation']:
                    values['forcing_estimate_'+key]=[m['forcing_estimate_error'][key] for m in members]
                summaries.append(dict(arm=arm,lead=lead,runs=len(members),metrics={k:dict(mean=float(np.mean(v)),minimum=float(np.min(v)),maximum=float(np.max(v))) for k,v in values.items()}))
    training={p.parent.name:json.loads(p.read_text()) for p in (ROOT/'runs/stage18/training').glob('*/complete.json')} if letter=='B' else {}
    aggregate=dict(part=letter,post_hoc=True,licenses_frozen_route=False,models=entries,training_runs=training,seed_summaries=summaries)
    (ROOT/'receipts'/f'acd_stage18_{letter}.json').write_text(json.dumps(aggregate,indent=2,allow_nan=False)+'\n')
    body=f'\n## Part {letter}\n\nEvery arm uses the original confirmation instances and retained draws. These readings are post hoc and license no frozen route. Outcome arrays are opened only by the Sulaco scorer. Training-run variation remains distinct from case-level uncertainty.\n\n'
    if letter=='A':
        body+='Own forcing, posterior-mean forcing and fixed climatological forcing are information diagnostics. The seeded within-case forcing permutation deliberately breaks the joint posterior; it is reported as an intervention on model input, without a posterior interpretation.\n\n'
    body+='| Arm | LT | State RMSE/sigma | State ACC | Confident S share | Pooled confident S error | Case confident S error | Case error bounds |\n|---|---:|---:|---:|---:|---:|---:|---:|\n'
    for name,m in entries.items():
        for row in m['confidence_readings']:
            skill=next(r for r in m['state_skill'] if r['lead']==row['lead'])
            a=row['all_confident_accuracy']
            body+=f"| {name} | {fmt(row['lead'])} | {fmt(skill['window_mean_RMSE_over_sigma'])} | {fmt(skill['window_mean_anomaly_correlation'])} | {fmt(row['confident_S_share'])} | {fmt(1-a['answer_accuracy'])} | {fmt(1-a['case_accuracy'])} | [{fmt(1-a['case_upper'])}, {fmt(1-a['case_lower'])}] |\n"
    body+='\nEach direction of the case-error bounds uses the v2.3 one-sided 95% instance betting construction; pooled error is descriptive.\n\n| Arm | LT | Quantity | Equal-case RMSE | Equal-case bias |\n|---|---:|---|---:|---:|\n'
    for name,m in entries.items():
        for r in m['per_draw_cost_errors']:
            body+=f"| {name} | {fmt(r['lead'])} | {r['quantity']} | {fmt(r['RMSE']['mean'])} | {fmt(r['bias']['mean'])} |\n"
    body+='\nErrors compare each emulator draw with the same draw’s physics forecast.\n\n| Arm | LT | Policy | Regret | Capture | Actions taken | Harms | Conditional harm CP95 | Uniform decrease in every instance |\n|---|---:|---|---:|---:|---:|---:|---:|---|\n'
    for name,m in entries.items():
        for r in m['decisions']:
            if r['policy'] not in ['E','C_delta_0']:continue
            c=r['conditional_harm_CP95']
            body+=f"| {name} | {fmt(r['lead'])} | {r['policy']} | {fmt(r['mean_regret'])} | {fmt(r['capture_fraction'])} | {r['actions_taken']} | {r['harms']} | [{fmt(c[0])}, {fmt(c[1])}] | {r['uniform_decrease_every_instance']} |\n"
    body+='\nConditional harm bounds are exact one-sided 95% Clopper–Pearson bounds. Action histograms and the full calibration, coverage, paired-endpoint and confidence readings are in the receipt.\n\n'
    for name,m in entries.items():
        if 'GB10_reproduction' in m:
            r=m['GB10_reproduction'];body+=f"{name} reproduction: maximum absolute predicted-cost difference {fmt(r['max_absolute_cost_difference'])}; changed confidence classifications {r['confidence_classification_changes']}.\n\n"
        if 'forcing_estimate_error' in m:
            r=m['forcing_estimate_error'];body+=f"{name} forcing estimate: RMSE {fmt(r['RMSE'])}, bias {fmt(r['bias'])}, correlation {fmt(r['correlation'])}. Population: {r['population']}.\n\n"
    if letter=='B':
        body+='Training-run variation (means and ranges only; separate from case-level bounds):\n\n| Arm | LT | Metric | Mean | Range | Runs |\n|---|---:|---|---:|---:|---:|\n'
        for row in summaries:
            for metric,v in row['metrics'].items():
                body+=f"| {row['arm']} | {fmt(row['lead'])} | {metric} | {fmt(v['mean'])} | [{fmt(v['minimum'])}, {fmt(v['maximum'])}] | {row['runs']} |\n"
        body+='\n| Estimator run | Completed updates | Skipped updates | Selected step | Charged GPU seconds | GPU |\n|---|---:|---:|---:|---:|---|\n'
        for name,v in training.items():
            body+=f"| {name} | {v['completed_updates']} | {v.get('skipped_updates', 0)} | {v['selected_step']} | {fmt(v['charged_gpu_seconds'])} | {v.get('gpu', 'unavailable')} |\n"
        body+='\n'
        alignment=json.loads((ROOT/'receipts/acd_stage18_alignment.json').read_text())
        body+='Alignment record: '+alignment['training_context']+' '+alignment['training_rollout']+' '+alignment['evaluation']+' '+alignment['E1']+'\n\n'
        body+=f"All factual-context frames have been replaced after {alignment['all_original_context_replaced_after_ticks']} output ticks ({fmt(alignment['all_original_context_replaced_after_time'])} model-time units; {fmt(alignment['all_original_context_replaced_after_LT'])} LT). Source code hashes and line evidence are in receipts/acd_stage18_alignment.json.\n\n"
    path=ROOT/'ACD_STAGE18_READING.md'
    existing=path.read_text() if path.exists() else '# Stage 18 learned controls and response derivatives\n'
    marker=f'\n## Part {letter}\n'
    if marker in existing:
        start=existing.index(marker);end=existing.find('\n## Part ',start+len(marker));existing=existing[:start]+(existing[end:] if end!=-1 else '')
    path.write_text(existing.rstrip()+'\n'+body)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('letter');p.add_argument('names',nargs='+');a=p.parse_args();run(a.letter,a.names)
