"""Compute v6 paper derivations from retained receipts and generating code."""
import json,hashlib,ast,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def build():
 d=json.loads((ROOT/'receipts/acd_stage9.json').read_text());s=json.loads((ROOT/'receipts/acd_stage2.json').read_text())
 rows={}
 def add(k,v,source,path,derivation):rows[k]=dict(value=v,source=source,source_path=path,derivation=derivation)
 for name in d['F']:
  add(name+'_GPU_HOURS',d['F'][name]['charged_gpu_seconds']/3600,'receipts/acd_stage9.json','$.F.'+name+'.charged_gpu_seconds','charged seconds / seconds per hour; discarded duration already included')
 provenance=d['CNN_provenance']['CNN20k']
 n=int(re.search(r'(\d+) training',provenance['training_distribution'])[1])
 add('CNN20K_TRAIN_TRAJECTORIES',n,'receipts/acd_stage9.json','$.CNN_provenance.CNN20k.training_distribution','parse retained training trajectory count; generating source recorded in provenance.source')
 tree=ast.parse((ROOT/'acd_stage9_training_data.py').read_text())
 loop=next(n for n in ast.walk(tree) if isinstance(n,ast.For) and isinstance(n.iter,ast.List) and all(isinstance(x,ast.Tuple) for x in n.iter.elts))
 for role,name,count in ast.literal_eval(loop.iter):
  add('CNNF_'+name.upper()+'_TRAJECTORIES',count,'acd_stage9_training_data.py',f'line {loop.lineno}, run trajectory loop','literal_eval trajectory counts in generating code; training and validation use distinct roles')
 i=next(i for i,r in enumerate(d['D']) if r['lead']==2 and r['policy']=='E');r=d['D'][i]
 add('E_LARGEST_HARM_OVER_MEAN_IMPROVEMENT_2LT',r['max_harm']/r['mean_improvement'],'receipts/acd_stage9.json',f'$.D[{i}].max_harm / $.D[{i}].mean_improvement','largest realized harm / mean realized improvement, E at 2 LT')
 c=[r for r in s['all_confident_calibration'] if r['type']=='S' and 0<=r['lead']<=3]
 total=sum(r['answers'] for r in c);wrong=sum(r['answers']-r['correct'] for r in c)
 add('POSTERIOR_S_WRONG_SHARE_0_TO_3LT',wrong/total,'receipts/acd_stage2.json','$.all_confident_calibration, S rows at leads 0 through 3','sum wrong / sum confident answers; pooled descriptive')
 add('POSTERIOR_S_ANSWERS_PER_ERROR_0_TO_3LT',total/wrong,'receipts/acd_stage2.json','$.all_confident_calibration, S rows at leads 0 through 3','sum confident answers / sum wrong')
 return dict(scope='Paper v6 receipt-only derivations; post hoc; no frozen route license',source_hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ['receipts/acd_stage9.json','receipts/acd_stage2.json','acd_stage9_training_data.py']},quantities=rows)
if __name__=='__main__':
 (ROOT/'receipts/acd_paper_v6_derived.json').write_text(json.dumps(build(),indent=2,allow_nan=False)+'\n')
