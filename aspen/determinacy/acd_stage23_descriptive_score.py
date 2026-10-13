"""Saved-output descriptive scoring through unchanged frozen statistics."""
from acd_stage23_common import *
import argparse,inspect,time,numpy as np
NAME='CNN-noF-response-corrected-selected'
def menus(costs,valid,actual,keep):
 import acd_posthoc_restricted_menu as existing
 return existing.rows(costs,valid,keep,actual,np.arange(9),'full')+existing.rows(costs,valid,keep,actual,np.arange(1,9),'seven_zero_mean_plus_no_action')
def audit_load(cache):
 original=np.load
 def logged(path,*a,**kw):
  if isinstance(path,(str,Path)) and Path(path).resolve()==cache.resolve():
   frame=inspect.stack()[1]
   assert frame.function=='score_actual' and Path(frame.filename).name in ('acd_stage19_score.py','acd_stage21_score.py')
   with (OUT/'descriptive_access.jsonl').open('a') as f:f.write(json.dumps(dict(path=str(path),caller=frame.filename,function=frame.function,sha256=digest(path),utc=time.time()))+'\n')
  return original(path,*a,**kw)
 np.load=logged
 return original
def fresh():
 ready();sys.path.insert(0,str(FROZEN18))
 import acd_stage19_learned as learned
 import acd_stage19_score as scoring
 import acd_stage19_part3b_score as groups
 from acd_protocol import LEADS
 view=OUT/'fresh19';assert (view/'scoring.npz').exists()
 learned.OUT=view;scoring.OUT=view;scoring.freeze_ready=ready
 original=audit_load(view/'scoring.npz')
 try:
  actual,factual=scoring.score_actual()
  d=json.loads((ROOT/'receipts/acd_stage2.json').read_text());jbar=d['null']['jbar'];null=np.asarray(d['null']['question_probabilities'])[np.r_[np.arange(8),37]]
  with np.load(view/'reused/runs/stage6/null_block.npz') as z:sd=(z['J'][:,:8]-z['J'][:,8,None]).std(0,ddof=1)
  with np.load(view/'reused/runs/stage4b_null/states.npz') as z:climate=z['states'].mean(0)
  p=learned.model_inputs('posterior',jbar,null)[3];fixed=p['observation'][:,:8,0]&p['confident'][:,8,0,None]
  inputs=learned.model_inputs(NAME,jbar,null);assert len(inputs[0])==len(actual)==200
  result=learned.metrics(NAME,*inputs,actual,factual,jbar,climate,sd,fixed)
  truth=np.concatenate([actual[:,:8]<actual[:,8,None],(actual[:,8]>jbar)[:,None]],1)
  result['pattern_group_readings']=groups.pattern_group_rows(inputs[0],inputs[4],inputs[3],truth,np.ones(len(actual),bool),LEADS)
  result['menu_decisions']=menus(inputs[0],inputs[2],actual,np.ones(len(actual),bool))
  write(ROOT/'receipts/acd_stage23_part3b.json',dict(descriptive_only=True,model=NAME,cases=len(actual),readings=result,realized_sha256=digest(view/'scoring.npz'),kernel_hashes={Path(x.__file__).name:digest(x.__file__) for x in [learned,scoring,groups]},adapter_sha256=digest(__file__)))
 finally:np.load=original
 print('PART3B DESCRIPTIVE SCORING COMPLETE',flush=True)
def shifted_menus():
 from acd_stage23_panel import configured
 _,view,name,gate=configured()
 import acd_stage21_score as scoring
 scoring.OUT=view;scoring.ready=gate
 assert (view/'scoring/actual.npz').exists()
 original=audit_load(view/'scoring/actual.npz')
 try:
  actual,_=scoring.score_actual();levels=scoring.assignments();costs=[];valid=[];keep=[]
  for c in range(len(levels)):
   with np.load(view/f'main_forecast_{c:03d}.npz') as z:keep.append(not bool(z['excluded']))
   with np.load(view/'inference'/name/f'{c:03d}.npz') as z:j=z['J'].copy();valid.append(bool(z['valid'].all()) and np.isfinite(j).all());costs.append(j)
  assert len(costs)==len(actual)==len(levels)
  keep=np.asarray(keep);valid=np.asarray(valid)
  result={group:menus(costs,valid,actual,keep & mask) for group,mask in [('pooled',np.ones(len(keep),bool)),('F7',np.asarray(levels)==7),('F9',np.asarray(levels)==9)]}
  write(ROOT/'receipts/acd_stage23_menus.json',dict(post_hoc=True,descriptive_only=True,model=name,panels=dict(stage22=result),adapter_sha256=digest(__file__)))
 finally:np.load=original
 print('STAGE22 MENU SCORING COMPLETE',flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--part',choices=['part3b','menus'],required=True);a=p.parse_args();fresh() if a.part=='part3b' else shifted_menus()
