import sys,json,argparse,time,hashlib
from pathlib import Path
sys.path.insert(0,'/mnt/niva-array/work/aspen-determinacy-stage19-l3-20261008/aspen/determinacy')
from acd_guarded_publish import publish
r=Path('/mnt/niva-array/work/aspen-determinacy-stage19-20261007/aspen/determinacy');out=r/'runs/stage18'
p=argparse.ArgumentParser();p.add_argument('part',choices=['D','data','C']);a=p.parse_args()
if a.part=='D':
 files=['receipts/acd_stage18_D.json','ACD_STAGE18_READING.md','acd_stage18_derivative_report.py']
 files += [str(p.relative_to(r)) for p in (r/'receipts').glob('acd_stage18_derivatives_*.json')]
 publish(r,'stage18-D',files,[('receipts/acd_stage18_D.json','ACD_POSTHOC_18D')],marker=out/'D_pushed.json')
elif a.part=='data':
 manifest=out/'response_data/manifest.json'
 d=json.loads(manifest.read_text())
 for name,h in d['data_sha256'].items():assert hashlib.sha256((out/'response_data'/name).read_bytes()).hexdigest()==h
 assert hashlib.sha256((out/'response_data/validation_reference.npz').read_bytes()).hexdigest()==d['validation_reference_sha256']
 result=publish(r,'stage18-C-data',['receipts/acd_stage18_response_data.json','runs/stage18/response_data/manifest.json'],[('receipts/acd_stage18_response_data.json','ACD_POSTHOC_18Cdata')],marker=out/'C_data_publication.json')
 (out/'response_data/generation_pushed.json').write_text(json.dumps(dict(commit=result['commit'],manifest_sha256=hashlib.sha256(manifest.read_bytes()).hexdigest()))+'\n')
else:
 sys.path.insert(0,str(r));from acd_stage18_report import run
 status=json.loads((out/'C_reading_ready.json').read_text());names=status['completed_models'];run('C',names)
 models={n:json.loads((r/'receipts'/f'acd_stage18_{n}.json').read_text()) for n in names}
 training={p.parent.name:json.loads(p.read_text()) for p in (out/'training').glob('CNN-noF-response-*/complete.json')}
 result=dict(post_hoc=True,licenses_frozen_route=False,models=models,training=training,execution=status,selection=json.loads((out/'C_selection.json').read_text()) if (out/'C_selection.json').exists() else None)
 from acd_stage18_C_execution_reading import run as execution_reading
 result['execution_reading']=execution_reading()
 (r/'receipts/acd_stage18_C.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
 # Presentation uses existing scored receipts only.
 import numpy as np
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 first=json.loads((r/'receipts/acd_stage9.json').read_text())['C'];arms=dict(first)
 decision_reference=json.loads((r/'receipts/acd_stage13_decisions.json').read_text())['models']
 for n,m in arms.items():
  if n in decision_reference:m['decisions']=decision_reference[n]['readings']
 for filename in ['acd_stage10b.json','acd_stage18_A.json','acd_stage18_B.json']:
  d=json.loads((r/'receipts'/filename).read_text());arms.update(d.get('models',{}))
 arms.update(models)
 wanted={k:v for k,v in arms.items() if k in ['CNN-F','CNN-noF'] or k.startswith(('CNN-F-E0-fixed','CNN-F-E1-fixed','CNN-F-E1-rolling','CNN-noF-response'))}
 groups={}
 for n,m in wanted.items():groups.setdefault(n.rsplit('-seed',1)[0],[]).append((n,m))
 fig,axes=plt.subplots(1,2,figsize=(10,4));markers=['o','s','^','D','x','+','v','p']
 for x,(arm,members) in enumerate(groups.items()):
  for n,m in members:
   conf=next(v for v in m['confidence_readings'] if v['lead']==2.)
   regret=next(v['mean_regret'] for v in m['decisions'] if v['lead']==3. and v['policy']=='E')
   for ax,y in zip(axes,[1-conf['all_confident_accuracy']['answer_accuracy'],regret]):ax.plot(x,y,marker=markers[x%len(markers)],color=str((x%4)/5),linestyle='none',markersize=5)
 posterior=first['posterior'];reference=[1-next(v for v in posterior['confidence_readings'] if v['lead']==2.)['all_confident_accuracy']['answer_accuracy'],next(v['mean_regret'] for v in posterior['decisions'] if v['lead']==3. and v['policy']=='E')]
 for ax,y,label in zip(axes,reference,['confident S error, 2 LT','E regret, 3 LT']):
  ax.axhline(y,color='black',linestyle=':',linewidth=.8,label='posterior');ax.set_ylabel(label);ax.set_xticks(range(len(groups)),list(groups),rotation=60,ha='right',fontsize=6);ax.legend(fontsize=7)
 fig.tight_layout();(r/'figures').mkdir(exist_ok=True)
 for ext in ['pdf','png']:fig.savefig(r/'figures'/('F21_repair_paper.'+ext),dpi=150)
 plt.close(fig)
 files=['receipts/acd_stage18_C.json','receipts/acd_stage18_C_execution_reading.json','acd_stage18_C_execution_reading.py','ACD_STAGE18_READING.md','figures/F21_repair_paper.pdf','figures/F21_repair_paper.png'];files += [f'receipts/acd_stage18_{n}.json' for n in names]
 publish(r,'stage18-C',files,[('receipts/acd_stage18_C.json','ACD_POSTHOC_18C')],marker=out/'C_pushed.json')
