"""Immutable five-case timing receipt derived from blind pilot outputs."""
from pathlib import Path
import json,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'runs/stage19'
d=json.loads((ROOT/'receipts/acd_stage19_part1.json').read_text());rows=[json.loads((OUT/f'case_{c:03d}.json').read_text()) for c in range(5)]
components={}
for arm in ['main','knownF']:
 rr=[r['arms'][arm] for r in rows]
 components[arm]={'fit_seconds':float(np.mean([r['fit_seconds'] for r in rr])),'sampler_seconds':float(np.mean([sum(a['sampler']['seconds'] for a in r['attempts']) for r in rr])),'diagnostics_and_gate_forecasts_seconds':float(np.mean([sum(a['diagnostic_forecast_seconds'] for a in r['attempts']) for r in rr])),'final_forecast_and_save_seconds':float(np.mean([r['forecast_seconds'] for r in rr]))}
 for key in sorted(set(k for r in rr for k in r['components'])):components[arm][key]=float(np.mean([r['components'].get(key,0) for r in rr]))
summary={a:{'completed':len(rows),'excluded':sum(r['arms'][a]['excluded'] for r in rows),'rerun':sum(len(r['arms'][a]['attempts'])>1 for r in rows),'rescored':sum(any(x['rescored'] for x in r['arms'][a]['attempts']) for r in rows),'divergences':sum(sum(x['sampler']['divergences'] for x in r['arms'][a]['attempts']) for r in rows)} for a in ['main','knownF']}
result={'timing_projection':d['timing_projection'],'mean_component_seconds':components,'gates':summary,'pilot_case_receipts':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [OUT/f'case_{c:03d}.json' for c in range(5)]},'realized_outcome_accesses':[]}
(ROOT/'receipts/acd_stage19_timing.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
