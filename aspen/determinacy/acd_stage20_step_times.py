"""Convert saved readability departure steps using the frozen time constants."""
import ast,hashlib,json,os
from pathlib import Path
ROOT=Path(__file__).resolve().parent
source=Path(os.environ['ACD_INHERITED_ROOT'])/'protocol.py'
constants={}
for node in ast.parse(source.read_text()).body:
 if isinstance(node,ast.Assign):
  for target in node.targets:
   if isinstance(target,ast.Name) and target.id in ('LT','OUT'):constants[target.id]=ast.literal_eval(node.value)
b=ROOT/'receipts/acd_stage20_B.json';d=json.loads(b.read_text());rows={}
for name,v in d['departures'].items():
 if name.startswith('CNN-noF'):
  step=v['first_step_above_twice_physics'];rows[name]=dict(step=step,model_time=step*constants['OUT'],LT=step*constants['OUT']/constants['LT'])
values=[r['LT'] for r in rows.values()];receipt=dict(post_hoc=True,definition='first step above twice physics equal-case RMSE; conversion only, no inference or scoring',step_model_time=constants['OUT'],step_LT=constants['OUT']/constants['LT'],LT_model_time=constants['LT'],departures=rows,range_LT=dict(min=min(values),max=max(values)),source_hashes={str(source):hashlib.sha256(source.read_bytes()).hexdigest(),str(b):hashlib.sha256(b.read_bytes()).hexdigest()})
(ROOT/'receipts/acd_stage20_B_step_times.json').write_text(json.dumps(receipt,indent=2)+'\n')
p=ROOT/'ACD_STAGE20_READING.md';s=p.read_text();heading='## B — forcing readability along each own rollout';assert heading in s
extra=f"\n\nEach learned rollout step is {receipt['step_model_time']} model-time units, or {receipt['step_LT']:.6f} reference LT. CNN-noF's first departures above twice physics range from {min(r['step'] for r in rows.values())} to {max(r['step'] for r in rows.values())} steps across the retained run and training seeds: {receipt['range_LT']['min']:.6f} to {receipt['range_LT']['max']:.6f} reference LT. These are descriptive conversions of the saved departure steps.\n"
s=s.replace(heading,heading+extra);p.write_text(s)
print(json.dumps(receipt,indent=2))
