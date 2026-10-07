"""Render Freeze C tables from receipts only; no array or outcome access."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def f(x):return '—' if x is None else f'{x:.6g}'
def interval(r):return f"{f(r['point'])} [{f(r['lower'])}, {f(r['upper'])}]"
def run():
 r=json.loads((ROOT/'receipts/acd_stage19_part3a.json').read_text());old=r['first_panel'];timing=json.loads((ROOT/'receipts/acd_stage19_part3a_timing.json').read_text());k=r['known_forcing'];main=r['main_on_knownF_cohort'];at=lambda rows,l:next(x for x in rows if x['lead']==l)
 lines=['','## Part 3a — Freeze C','',
'K and V readings are confirmatory on the fresh panel under the pushed Freeze C. The unchanged Stage15/Stage6 interval helpers retain their original POST HOC scope string in the receipt; that string describes their first-panel origin, not the frozen fresh-panel reading. Descriptive replications use realized counts already reported in Part 2; they have no confirmatory criteria. No frozen route is licensed. Known-forcing and matched main readings use the retained known-forcing cohort; K4 uses all main-posterior instances. First-panel values retain their original populations.','',
'| Reading | First panel | Fresh panel | Fresh population / bound | Result |','|---|---:|---:|---|---|']
 def row(key,o,n,p,b,status):lines.append(f'| {key} | {o} | {n} | {p}; {b} | {"PASS" if status else "FAIL"} |')
 row('K1',interval(old['known_forcing']['paired_first_loss']['interval']),interval(r['K1']),k['population'],'two-sided 99% case betting',r['K1']['confirmed'])
 for x in r['K2']['rows']:
  o=at(old['known_forcing']['comparisons'],x['lead'])['seven_minus_Fc'];row('K2 '+f(x['lead'])+' LT',interval(o),interval(x),k['population'],'two-sided 99% case betting',x['upper']<0 and not(x['offset'] or x['empty']))
 o=at(old['known_forcing']['accuracy'],2)['S'];n=r['K3'];row('K3',f(o['case_accuracy'])+' lower '+f(o['case_lower']),f(n['case_accuracy'])+' lower '+f(n['case_lower']),str(k['population'])+' retained; '+str(n['cases'])+' contributing','original R0 one-sided 95%',n['confirmed'])
 o=at(old['known_forcing']['main_posterior_forcing_correlation'],2);n=r['K4'];row('K4 D / J8',f(o['D']['median'])+' / '+f(o['J8']['median']),f(n['D_median'])+' / '+f(n['J8_median']),n['population'],'median thresholds; no interval',n['confirmed'])
 for key in ['V1','V2']:row(key,'descriptive Stage15D; see ratio table','both ratios in range' if r[key] else 'criterion fails',r['variance']['population'],'median thresholds; no interval',r[key])
 lines+=['',f"K1 eligibility: {k['paired_first_loss']['actions']} pairs in {k['paired_first_loss']['cases']} contributing instances, from {k['population']} retained known-forcing instances. First panel: {old['known_forcing']['paired_first_loss']['actions']} pairs in {old['known_forcing']['paired_first_loss']['cases']} contributing instances."]
 lines+=['','| Lead | Fresh J8 ratio q25 / median / q75 | First J8 q25 / median / q75 | Fresh G ratio q25 / median / q75 | First G q25 / median / q75 |','|---|---:|---:|---:|---:|']
 for x in r['variance']['summary']:
  o=at(old['variance']['summary'],x['lead']);trip=lambda v:' / '.join(f(v[q]) for q in ['q25','median','q75']);lines.append(f"| {f(x['lead'])} | {trip(x['J8_ratio'])} | {trip(o['J8_ratio'])} | {trip(x['G_ratio'])} | {trip(o['G_ratio'])} |")
 lines+=['','First tested breakdown leads: '+json.dumps(r['variance']['first_lead_median_outside_half_to_two'])+'.',f"Pilot projection {f(timing['projected_hours'])} hours on {len(timing['cores'])} cores; case set {timing['case_set']}. First-panel variance population: {len(old['variance']['cases'])}.",'',
'| Lead | Known-F S8 / S7 / obs-S / Fc | Matched main S8 / S7 / obs-S / Fc | First known-F S8 / S7 / obs-S / Fc |','|---|---:|---:|---:|']
 for x in k['shares']:
  l=x['lead'];fields=['S8_confident_share','S7_confident_share','observation_S_share','Fc_confident_share'];values=lambda v:' / '.join(f(v[q]) for q in fields);lines.append(f"| {f(l)} | {values(x)} | {values(at(main['shares'],l))} | {values(at(old['known_forcing']['shares'],l))} |")
 lines+=['','| Lead | Known-F obs-S case accuracy / lower95 | Matched main | First known-F |','|---|---:|---:|---:|']
 for x in k['accuracy']:
  fmt=lambda v:f(v['S']['case_accuracy'])+' / '+f(v['S']['case_lower']);lines.append(f"| {f(x['lead'])} | {fmt(x)} | {fmt(at(main['accuracy'],x['lead']))} | {fmt(at(old['known_forcing']['accuracy'],x['lead']))} |")
 lines+=['','| Lead | Known-F pooled obs-S accuracy / Fc pooled accuracy / Fc CP95 | Matched main | First known-F |','|---|---:|---:|---:|']
 for x in k['accuracy']:
  fmt=lambda v:f(v['S']['answer_accuracy'])+' / '+f(v['Fc_CP_one_sided95']['accuracy'])+' / '+str(v['Fc_CP_one_sided95']['bounds']);lines.append(f"| {f(x['lead'])} | {fmt(x)} | {fmt(at(main['accuracy'],x['lead']))} | {fmt(at(old['known_forcing']['accuracy'],x['lead']))} |")
 lines+=['','| Lead | Known-F rho / c / zD / zF medians | Matched main medians | First known-F medians |','|---|---:|---:|---:|']
 for x in k['shares']:
  fmt=lambda v:' / '.join(f(v[q]['median']) for q in ['rho','c','z_D','z_F']);lines.append(f"| {f(x['lead'])} | {fmt(x)} | {fmt(at(main['shares'],x['lead']))} | {fmt(at(old['known_forcing']['shares'],x['lead']))} |")
 lines+=['','First-panel matched-main accuracy, confidence-share and mechanism-summary rows were not recorded on the exact retained known-forcing cohort; those exact first-panel counterparts are unavailable.','', 'Known-F minus matched main confidence-share differences (two-sided99% case betting; first-panel paired-share intervals were not reported and are unavailable):']
 for x in r['paired_share_differences']:lines.append(f"- {x['quantity']}, {f(x['lead'])} LT: {interval(x['interval'])}.")
 lines+=['','Main forcing SD, matched cohort: '+json.dumps(r['main_forcing_sd'])+'. First panel: '+json.dumps(old['known_forcing']['main_posterior_forcing_sd'])+'.','Main forcing correlations, all cases: '+json.dumps(r['main_all_forcing_correlations'])+'. Matched-cohort correlations: '+json.dumps(r['main_matched_forcing_correlations'])+'.','',
'First-panel forcing SD and correlations use the original main panel; fresh descriptive forcing summaries use the matched known-forcing cohort.']
 lines+=['','Main forcing correlation medians, first panel / fresh matched cohort (different panel populations):']
 for x in r['main_matched_forcing_correlations']:
  o=at(old['known_forcing']['main_posterior_forcing_correlation'],x['lead']);lines.append(f"- {f(x['lead'])} LT: F with J8 {f(o['J8']['median'])} / {f(x['J8']['median'])}; F with D {f(o['D']['median'])} / {f(x['D']['median'])}.")
 lines+=['','| Model | Lead | Patterns | Coverage | Fresh pooled error / case error / upper95 | First-panel pooled / case / upper95 |','|---|---:|---|---:|---:|---:|']
 for m,rows in r['descriptive']['matching'].items():
  for x in rows:
   o=next(v for v in at(old['matching']['A'][m]['rows'],x['lead'])['matched_coverage'] if v['patterns']==x['patterns'] and v['target_coverage']==x['coverage']);fmt=lambda v:' / '.join(f(v[q]) for q in ['pooled_error','case_error','case_error_upper95']);lines.append(f"| {m} | {f(x['lead'])} | {x['patterns']} | {f(x['coverage'])} | {fmt(x)} | {fmt(o)} |")
 lines+=['','Matched-coverage case error bounds are one-sided95% v2.3 bounds; population is the full panel and case bounds omit cases with no contributing selected answers.','',
'| Model | Lead | Policy | Fresh expected / realized harms | First expected / realized harms | Fresh actions |','|---|---:|---|---:|---:|---:|']
 for m,rows in r['descriptive']['selected_action'].items():
  for x in rows:
   o=next(v for v in old['selected_action']['models'][m]['selected'] if v['lead']==x['lead'] and v['policy']==x['policy']);lines.append(f"| {m} | {f(x['lead'])} | {x['policy']} | {f(x['expected_harms'])} / {x['realized_harms']} | {f(o['expected_harms'])} / {o['harms']} | {x['actions']} |")
 lines+=['','Stage17C counts non-lowering effects as harm; Part2 strict-positive harm counts and zero-effect ties are recorded separately.','',
'| Model, 2 LT | Fresh median bound / share below0.05 / vacuous share | First-panel values |','|---|---:|---:|']
 for x in r['descriptive']['transfer']:
  o=next(v for v in old['transfer']['rows'] if v['model']==x['model'] and v['lead']==x['lead']);fmt=lambda v:' / '.join(f(v[q]) for q in ['median_minimized_bound','share_bound_below_0_05','share_bound_at_least_one']);lines.append(f"| {x['model']} | {fmt(x)} | {fmt(o)} |")
 lines+=['','R-other resolutions: '+json.dumps(r['resolutions'])+'.','']
 p=ROOT/'ACD_STAGE19_READING.md';oldtext=p.read_text().split('\n## Part 3a — Freeze C')[0];p.write_text(oldtext+'\n'.join(lines))
if __name__=='__main__':run()
