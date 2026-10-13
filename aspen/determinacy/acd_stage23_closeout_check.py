"""Read-only Stage23 implementation verification; never instantiate an optimizer."""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='4',NUMBA_NUM_THREADS='4',JAX_PLATFORMS='cpu',JAX_ENABLE_X64='true')
from pathlib import Path
import ast,copy,hashlib,inspect,json,math,sys,time,traceback
import numpy as np
import torch
ROOT=Path(os.environ.get('ACD_CLOSEOUT_ROOT','/mnt/niva-array/work/aspen-determinacy-stage23-20261012/aspen/determinacy'))
FROZEN=Path('/mnt/niva-array/work/aspen-determinacy-stage19-20261007/aspen/determinacy')
INHERITED=Path('/mnt/niva-array/work/aspen-forecast-decision-20261005/aspen/forecast_decision')
OUT=ROOT/'runs/stage23_closeout';OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(INHERITED));sys.path.insert(0,str(ROOT))
import protocol,physics
import acd_stage23_train as trainer
META=ROOT/'runs/stage23/training/CNN-noF-response-0.03-seed1'
RECORD={ 'scope':'Implementation verification and posterior-generation exclusion accounting only', 'realized_outcome_accesses':[], 'training_updates':0,'optimizer_runs':0,'checks':{},'accesses':[] }
def digest(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
def read_json(p):
 RECORD['accesses'].append(dict(path=str(p),kind='metadata_or_generation_record',sha256=digest(p)))
 return json.loads(Path(p).read_text())
def save():
 (OUT/'progress.json').write_text(json.dumps(RECORD,indent=2,allow_nan=False)+'\n')
def checkpoint_state_hash(state):
 h=hashlib.sha256()
 for name,value in sorted(state.items()):
  a=value.detach().cpu().contiguous().numpy();h.update(json.dumps([name,str(a.dtype),list(a.shape)],separators=(',',':')).encode()+b'\0');h.update(a.tobytes())
 return h.hexdigest()
def array_hash(arrays):
 h=hashlib.sha256()
 for name,value in sorted(arrays.items()):
  a=np.ascontiguousarray(value);h.update(json.dumps([name,str(a.dtype),list(a.shape)],separators=(',',':')).encode()+b'\0');h.update(a.tobytes())
 return h.hexdigest()
def gate(name,record):
 RECORD['checks'][name]=record;save();print(name,json.dumps(record,allow_nan=False)[:2000],flush=True)
 if not record['passed']:
  RECORD['status']='FAILED_GATE';RECORD['failed_gate']=name;save();raise SystemExit(2)
def verify():
 expected=read_json(ROOT/'receipts/acd_stage23_execution.json')
 for name,sha in expected['code_hashes'].items():assert digest(ROOT/name)==sha,name
 assert digest(ROOT/'ACD_STAGE23_FREEZE_G.md').startswith('ac7e7104')
 meta=read_json(META/'complete.json');assert digest(META/'selected.pt')==meta['selected_sha256'] and meta['selected_sha256'].startswith('5e308dad')
 assert torch.__version__==meta['torch'],(torch.__version__,meta['torch'])
 return meta

def independent_paths(x,f,dt,frames):
 def rhs(a):return (np.roll(a,-1,axis=-1)-np.roll(a,2,axis=-1))*np.roll(a,1,axis=-1)-a+f
 result=[x.copy()]
 for _ in range(frames-1):
  for _ in range(int(round(protocol.OUT/dt))):
   k1=rhs(x);k2=rhs(x+dt*k1/2);k3=rhs(x+dt*k2/2);k4=rhs(x+dt*k3)
   x=x+(dt/6)*(k1+2*k2+2*k3+k4)
  result.append(x.copy())
 return np.stack(result,axis=1)

def target_expression():
 tree=ast.parse((ROOT/'acd_stage23_train.py').read_text());run=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='run')
 fn=next(n for n in run.body if isinstance(n,ast.FunctionDef) and n.name=='paired')
 assignment=next(n for n in ast.walk(fn) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='difference' for t in n.targets))
 return compile(ast.fix_missing_locations(ast.Expression(copy.deepcopy(assignment.value.right))),'frozen_target_expression','eval'),ast.unparse(assignment.value.right)

def rebuild_batch(meta):
 path=FROZEN/'runs/stage18/response_data/train.npz';assert digest(path)==meta['data_sha256']['train.npz'];RECORD['accesses'].append(dict(path=str(path),kind='training_data_only',sha256=digest(path)))
 with np.load(path,allow_pickle=False) as z:stored={k:z[k].copy() for k in ['H','A','F','T']}
 ids=np.random.default_rng(meta['batch_order_seed']).integers(len(stored['H']),size=meta['microbatch'])
 namespace=read_json(ROOT/'receipts/acd_stage18_response_data.json')['namespace_id'];r=np.random.default_rng(np.random.SeedSequence([namespace,0]));n=len(stored['H'])
 forcing=r.uniform(6,10,n);starts=forcing[:,None]+r.standard_normal((n,stored['H'].shape[-1]));patterns=np.vstack([protocol.patterns(),np.zeros(stored['H'].shape[-1])]);ix=r.integers(len(patterns)-1,size=n);amplitude=r.uniform(-.32,.32,size=n)
 raw=physics.flow(starts[ids],np.repeat(forcing[ids,None],stored['H'].shape[-1],axis=1),round(50*protocol.LT/.01),.01)
 history=physics.simulate(raw,np.repeat(forcing[ids,None],stored['H'].shape[-1],axis=1),.01,stored['H'].shape[1])
 assert np.array_equal((history/protocol.SIGMA).astype(np.float32),stored['H'][ids]),'Rebuilt training histories differ'
 assert np.array_equal(((forcing[ids]-8)/2).astype(np.float32),stored['F'][ids]),'Rebuilt training forcings differ'
 original_actions=np.zeros((len(ids),2,stored['H'].shape[-1]));original_actions[:,0]=amplitude[ids,None]*patterns[ix[ids]]
 assert np.array_equal((original_actions/protocol.SIGMA).astype(np.float32),stored['A'][ids]),'Rebuilt original actions differ'
 # Every recorded start, using its recorded amplitude under each of the eight patterns.
 count=len(patterns)-1;actions=np.zeros((len(ids),count,2,stored['H'].shape[-1]));actions[:,:,0]=amplitude[ids,None,None]*patterns[None,:count]
 x=np.repeat(history[:,-1],count*2,axis=0);f=np.repeat(forcing[ids],count*2)[:,None]+actions.reshape(-1,stored['H'].shape[-1]);frames=stored['T'].shape[2]+1
 reference=physics.simulate(x,f,.01,frames).reshape(len(ids),count,2,frames,-1)
 independent=independent_paths(x.copy(),f,.01,frames).reshape(reference.shape)
 represented=(reference[:,:, :,1:]/protocol.SIGMA).astype(np.float32)
 recovered_original=np.take_along_axis(represented,ix[ids,None,None,None,None],axis=1)[:,0]
 assert np.array_equal(recovered_original,stored['T'][ids]),'Stored original targets not reproduced'
 batch=dict(H=np.repeat(stored['H'][ids],count,axis=0),A=(actions.reshape(-1,2,stored['H'].shape[-1])/protocol.SIGMA).astype(np.float32),F=np.repeat(stored['F'][ids],count),T=represented.reshape(-1,2,frames-1,stored['H'].shape[-1]))
 return ids,amplitude[ids],batch,reference,independent

def A1(meta,batch,reference,independent):
 expression,notation=target_expression();t=torch.tensor(batch['T'],dtype=torch.float32)
 actual=np.stack([eval(expression,{'T':t,'tick':i}).numpy().astype(np.float64) for i in range(t.shape[2])],axis=1)
 # Preserve the exact serialized branch-state precision of the frozen data recipe.
 branch=(independent[:,:,:,1:]/protocol.SIGMA).astype(np.float32)
 expected=(branch[:,:,0]-branch[:,:,1]).astype(np.float64).reshape(actual.shape)
 delta=np.abs(actual-expected);den=np.maximum(np.abs(actual),np.abs(expected));relative=np.divide(delta,den,out=np.zeros_like(delta),where=den>0)
 raw=((independent[:,:,0,1:]-independent[:,:,1,1:])/protocol.SIGMA).reshape(actual.shape)
 raw_delta=np.abs(actual-raw)
 maxrel=float(relative.max());record=dict(maximum_absolute_difference=float(delta.max()),maximum_relative_difference=maxrel,relative_definition='maximum componentwise |a-b| / max(|a|,|b|), with jointly zero components assigned zero',comparison_dtype='float64 after exact float32 target arithmetic',training_arithmetic_dtype='float32',independent_branch_storage_dtype='float32, exactly as frozen training data',training_target_expression=notation,training_subtraction='action branch minus no-action twin',independent_subtraction='action branch minus no-action twin',unquantized_physics_maximum_absolute_difference=float(raw_delta.max()),unquantized_physics_relative_Linf=float(raw_delta.max()/np.max(np.abs(raw))),independent_RK4_raw_state_maximum_absolute_difference=float(np.max(np.abs(reference-independent))),pass_rule='maximum relative difference <= 1e-6 in float64 and identical subtraction order',both_model_states_share_target=True,passed=maxrel<=1e-6)
 gate('A1',record)


def main():
 meta=verify();torch.set_num_threads(4);torch.manual_seed(meta['torch_initialization_seed']);initial=trainer.Emulator(False)
 # No step-zero checkpoint or state hash is saved by this trainer before its first scheduled checkpoint.
 RECORD['models']=dict(selected_checkpoint_sha256=digest(META/'selected.pt'),selected_step=meta['selected_step'],initialization_seed=meta['torch_initialization_seed'],rebuilt_initial_tensor_hash=checkpoint_state_hash(initial.state_dict()),recorded_step_zero_hash=None,step_zero_hash_comparison='No recorded step-zero hash found in this run metadata, checkpoint directory, or freeze records.')
 RECORD['code_hashes']={str(p):digest(p) for p in [ROOT/'acd_stage23_train.py',ROOT/'ACD_STAGE23_FREEZE_G.md',FROZEN/'acd_stage18_data.py',INHERITED/'physics.py',INHERITED/'protocol.py',Path(__file__)]}
 ids,amplitude,batch,reference,independent=rebuild_batch(meta)
 RECORD['batch']=dict(batch_order_seed=meta['batch_order_seed'],start_indices=ids.tolist(),per_start_amplitudes=amplitude.tolist(),expanded_rows=len(batch['H']),patterns_per_start=len(protocol.patterns()),tensor_shapes={k:list(v.shape) for k,v in batch.items()},tensor_dtypes={k:str(v.dtype) for k,v in batch.items()},canonical_tensor_sha256=array_hash(dict(batch,start_indices=ids)),expansion='Each recorded first-batch start retains its original recorded amplitude, expanded in frozen pattern order with an action/no-action twin.')
 save();A1(meta,batch,reference,independent)
 RECORD['status']='A1_COMPLETE';save();print('A1_COMPLETE',flush=True)
if __name__=='__main__':
 try:main()
 except SystemExit:raise
 except BaseException as e:
  RECORD['status']='FAILED_EXECUTION';RECORD['exception']=repr(e);save();traceback.print_exc();raise
