"""Render the reference reading solely from computed receipts; no truth access."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
r=json.loads((ROOT/'receipts/acd_stage19_reference.json').read_text())
p=json.loads((ROOT/'receipts/acd_stage19_part1.json').read_text())
f=lambda x: '—' if x is None else f'{x:.6f}'
bounds=lambda x: f"[{f(x.get('lower',x.get('case_lower')))}, {f(x.get('upper',x.get('case_upper')))}]"
lines=['# Stage 19 fresh-panel readings','','Reference side: Freeze A and Freeze B. The original confirmation-panel mechanism and seven-pattern comparisons were post hoc; these fresh-panel readings were frozen before outcomes were computed.','','| Reading | Original confirmation | Fresh panel | Fresh bound | Result |','|---|---:|---:|---|---|']
old=r['confirmation_panel'];fresh=r['confirmatory']
for key in ['C1','C2','C3','C4','M1','M2']:
 for v in fresh[key] if isinstance(fresh[key],list) else [fresh[key]]:
  o=next(x for x in old[key] if x['lead']==v['lead']) if isinstance(old[key],list) else old[key]
  oval=o if isinstance(o,(int,float)) else o.get('point',o.get('case_accuracy',o.get('three_class_agreement')))
  val=v.get('point',v.get('value',v.get('case_accuracy')))
  lines.append(f"| {key} ({v.get('lead','paired')} LT) | {f(oval)} | {f(val)} | {'—' if key=='M1' else bounds(v)} | {'PASS' if v['confirmed'] else 'FAIL'} |")
lines+=['','C1 retains the original R0 one-sided 95% case bounds and original answer/case prerequisites. C2–C4 use two-sided 99% case betting intervals. M1 has the frozen median threshold without an interval. M2 has a one-sided 99% case betting lower bound. The C2 direction is reported separately in the receipt.','','| R0 lead (LT) | Observation-confident answers | Contributing cases | Equal-case accuracy | Lower / upper | Status |','|---:|---:|---:|---:|---|---|']
for x in r['accuracy']:
 a=x['S'];lines.append(f"| {x['lead']} | {a['answers']} | {a['cases']} | {f(a['case_accuracy'])} | {bounds(a)} | {a['status']} |")
lines+=['','| Descriptive lead (LT) | Mean-flow variance share median, seven patterns | Three-class agreement | Kappa | Per-draw sign agreement | Original z ratio | Fresh z ratio |','|---:|---:|---:|---:|---:|---:|---:|']
for x,o in zip(r['mechanism'],old['M3']):lines.append(f"| {x['lead']} | {f(x['mean_flow_variance_share_median'])} | {f(x['three_class_agreement'])} | {f(x['three_class_kappa'])} | {f(x['per_draw_sign_agreement'])} | {f(o['ratio'])} | {f(x['median_z_D_over_median_z_Fc'])} |")
lines+=['',f"Fresh eligibility yields {fresh['C2']['pairs']} pairs in {fresh['C2']['cases']} cases. The descriptive M3 crossover expectation holds: the median z ratio is above one at lead zero and below one at the frozen mechanism lead.",'','Known-forcing readings remain deferred to Part 3. Its exclusion is recorded in the Part 1 receipt and Freeze B. No emulator was needed for these reference readings.','','No statistical R-other condition fired. The first scoring process completed the realized-cost cache, then encountered a Numba thread-environment mismatch while compiling betting intervals. The same frozen code completed with NUMBA_NUM_THREADS set consistently before imports; calculations and criteria were unchanged.','','Source receipts: receipts/acd_stage19_reference.json, receipts/acd_stage19_part1.json; original values and precise keys are retained in the reference receipt. The realized cache and scoring-only access log remain under runs/stage19/.']
(ROOT/'ACD_STAGE19_READING.md').write_text('\n'.join(lines)+'\n')
