"""Sequential gradient verification on a fixed training batch; no optimizer execution."""
import importlib.util,copy,ast,hashlib,json,math,os,sys,time,traceback
from pathlib import Path
spec=importlib.util.spec_from_file_location('closeout','/tmp/acd_stage23_closeout_check.py');c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
import numpy as np
import torch
c.RECORD=json.loads((c.OUT/'progress.json').read_text())
META=c.verify();ids,amplitudes,BATCH,REFERENCE,INDEPENDENT=c.rebuild_batch(META)
assert c.array_hash(dict(BATCH,start_indices=ids))==c.RECORD['batch']['canonical_tensor_sha256']
original_optimizer_init=torch.optim.AdamW.__init__
def prohibited_optimizer_init(*a,**k):raise RuntimeError('Optimizer execution is forbidden in closeout')
torch.optim.AdamW.__init__=prohibited_optimizer_init
N=len(BATCH['H']);MICRO=32
CODE=ast.parse((c.ROOT/'acd_stage23_train.py').read_text());RUN=next(n for n in CODE.body if isinstance(n,ast.FunctionDef) and n.name=='run')
PAIRED=next(n for n in RUN.body if isinstance(n,ast.FunctionDef) and n.name=='paired');BASE=next(n for n in RUN.body if isinstance(n,ast.FunctionDef) and n.name=='base')
def loss_functions(model,truncated=True):
 paired=copy.deepcopy(PAIRED)
 if not truncated:
  removed=0
  for node in ast.walk(paired):
   if isinstance(node,ast.For):
    old=len(node.body);node.body=[x for x in node.body if not (isinstance(x,ast.If) and any(isinstance(y,ast.Call) and isinstance(y.func,ast.Attribute) and y.func.attr=='detach' for y in ast.walk(x)))];removed+=old-len(node.body)
  assert removed==1
 env=dict(model=model,torch=torch,math=math)
 module=ast.fix_missing_locations(ast.Module(body=[copy.deepcopy(BASE),paired],type_ignores=[]))
 exec(compile(module,'unchanged_frozen_loss_ast','exec'),env)
 return env['base'],env['paired']
def tensors(model,b,end):
 return [torch.as_tensor(BATCH[k][b:end],device=next(model.parameters()).device,dtype=next(model.parameters()).dtype) for k in ['H','A','F','T']]
def norms(grads):return [float(torch.linalg.vector_norm(g)) for g in grads]
def gradient(model,truncated,kind='paired',predictions=False,energy=False):
 base,paired=loss_functions(model,truncated);params=list(model.parameters());sums=[torch.zeros_like(p) for p in params];branch_square=[0.,0.];effects=[];value=0.
 window=c.protocol.WINDOWS[list(c.protocol.LEADS).index(2.)]
 for b in range(0,N,MICRO):
  end=min(b+MICRO,N);H,A,F,T=tensors(model,b,end);outputs=[]
  hook=model.register_forward_hook(lambda m,i,o:outputs.append(o)) if predictions or energy else None
  try:
   loss=base(H,A,F,T) if kind=='base' else paired(H,A,F,T)[0];w=(end-b)/N;value+=float(loss.detach())*w
   if energy:
    states=torch.stack([H[:,-1].repeat_interleave(2,0),*outputs],1).to(torch.float64)*c.protocol.SIGMA
    en=.5*states.square().mean(-1);cost=en[:,window].mean(1).reshape(-1,2);effects.append((cost[:,0]-cost[:,1]).detach().cpu().numpy())
   extra=outputs if predictions else []
   gg=torch.autograd.grad(w*loss,params+extra)
   with torch.no_grad():
    for dst,g in zip(sums,gg[:len(params)]):dst.add_(g)
   if predictions:
    for g in gg[len(params):]:
     g=g.reshape(end-b,2,-1).to(torch.float64)
     for j in range(2):branch_square[j]+=float(g[:,j].square().sum())
  finally:
   if hook:hook.remove()
 return dict(grads=sums,loss=value,branch_norms=[math.sqrt(v) for v in branch_square],effects=np.concatenate(effects).reshape(len(ids),-1) if effects else None)
def loss_value(model):
 _,paired=loss_functions(model,False);value=0.
 with torch.no_grad():
  for b in range(0,N,MICRO):
   end=min(b+MICRO,N);value+=float(paired(*tensors(model,b,end))[0])*(end-b)/N
 return value
def vector(grads):return torch.cat([g.reshape(-1) for g in grads])
def set_parameters(model,flat):
 with torch.no_grad():
  b=0
  for p in model.parameters():p.copy_(flat[b:b+p.numel()].reshape_as(p));b+=p.numel()
 assert b==len(flat)
def initial_model():
 torch.manual_seed(META['torch_initialization_seed']);model=c.trainer.Emulator(False)
 assert c.checkpoint_state_hash(model.state_dict())==c.RECORD['models']['rebuilt_initial_tensor_hash']
 return model
def selected_model():
 model=c.trainer.Emulator(False);path=c.META/'selected.pt';ck=torch.load(path,map_location='cpu',weights_only=True)
 assert ck['step']==META['selected_step'] and 'optimizer' not in ck;model.load_state_dict(ck['state_dict'])
 c.RECORD['models']['selected_tensor_hash']=c.checkpoint_state_hash(model.state_dict());return model

def run_checks(card):
 assert not torch.cuda.is_initialized();os.environ['CUDA_VISIBLE_DEVICES']=card['uuid']
 torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False;torch.backends.cudnn.deterministic=True;torch.backends.cudnn.benchmark=False
 models={'initial':initial_model().cuda(),'selected':selected_model().cuda()};saved={}
 physics_energy=.5*np.mean(INDEPENDENT**2,axis=-1);window=c.protocol.WINDOWS[list(c.protocol.LEADS).index(2.)];cost=physics_energy[:,:,:,window].mean(-1);physics_effect=cost[:,:,0]-cost[:,:,1]
 c.RECORD['A1b']=dict(descriptive_only=True,lead_LT=float(c.protocol.LEADS[list(c.protocol.LEADS).index(2.)]),window_ticks=window.tolist(),physics_action_minus_twin=physics_effect.tolist(),models={})
 a2={}
 for name,model in models.items():
  start=time.monotonic();result=gradient(model,True,predictions=True,energy=True);saved[name]=result
  effect=result['effects'];error=effect-physics_effect
  c.RECORD['A1b']['models'][name]=dict(predicted_action_minus_twin=effect.tolist(),predicted_mean=float(effect.mean()),physics_mean=float(physics_effect.mean()),predicted_quartiles=np.quantile(effect,[.25,.5,.75]).tolist(),physics_quartiles=np.quantile(physics_effect,[.25,.5,.75]).tolist(),effect_RMSE=float(np.sqrt(np.mean(error**2))),effect_bias=float(error.mean()))
  a2[name]=dict(action_prediction_gradient_norm=result['branch_norms'][0],twin_prediction_gradient_norm=result['branch_norms'][1],predicted_subtraction='action branch minus no-action twin',target_subtraction='action branch minus no-action twin',seconds=time.monotonic()-start)
  c.RECORD['current_phase']='A2 '+name;c.save();print(c.RECORD['current_phase'],a2[name],flush=True)
 c.gate('A2',dict(models=a2,pass_rule='both branch prediction gradient norms nonzero, with matching subtraction order',passed=all(v['action_prediction_gradient_norm']>0 and v['twin_prediction_gradient_norm']>0 for v in a2.values())))
 a3={}
 for name,model in models.items():
  rows=[dict(parameter=label,shape=list(p.shape),gradient_norm=float(torch.linalg.vector_norm(g)),trainable=p.requires_grad) for (label,p),g in zip(model.named_parameters(),saved[name]['grads'])]
  a3[name]=rows
 c.gate('A3',dict(models=a3,pass_rule='every trainable parameter tensor has nonzero truncated paired-loss gradient norm',passed=all(v['gradient_norm']>0 for rows in a3.values() for v in rows if v['trainable'])))
 a4={};seed=int.from_bytes(hashlib.sha256(b'acd-stage23-closeout-directions').digest()[:8],'little')
 for name,model in models.items():
  model64=copy.deepcopy(model).to(dtype=torch.float64);theta=vector([p.detach() for p in model64.parameters()]).clone();untruncated=gradient(model64,False);truncated=gradient(model64,True)
  ug,tg=vector(untruncated['grads']),vector(truncated['grads']);cosine=float(torch.dot(ug,tg)/(torch.linalg.vector_norm(ug)*torch.linalg.vector_norm(tg)))
  r=np.random.default_rng(seed);directions=[]
  for i in range(5):
   v=r.standard_normal(len(theta));v/=np.linalg.norm(v);direction=torch.as_tensor(v,device=theta.device,dtype=torch.float64);autodiff=float(torch.dot(ug,direction));rows=[]
   for h in [1e-3,1e-4,1e-5]:
    set_parameters(model64,theta+h*direction);plus=loss_value(model64);set_parameters(model64,theta-h*direction);minus=loss_value(model64);set_parameters(model64,theta)
    difference=(plus-minus)/(2*h);den=max(abs(difference),abs(autodiff));error=abs(difference-autodiff)/den if den else 0.
    rows.append(dict(step_size=h,loss_plus=plus,loss_minus=minus,central_difference=difference,relative_error=error))
    c.RECORD['current_phase']=f'A4 {name} direction {i+1} step {h}';c.save();print(c.RECORD['current_phase'],error,flush=True)
   item=dict(index=i+1,unit_direction_seed=seed,unit_direction_sha256=hashlib.sha256(v.tobytes()).hexdigest(),direction_norm=float(np.linalg.norm(v)),autodiff=autodiff,step_sizes=rows,best_relative_error=min(x['relative_error'] for x in rows));directions.append(item)
   if item['best_relative_error']>1e-4:
    a4[name]=dict(directions=directions,truncated_untruncated_cosine=cosine)
    c.gate('A4',dict(models=a4,pass_rule='best relative error <= 1e-4 for every one of five fixed random unit directions at the three requested step sizes',passed=False))
  a4[name]=dict(directions=directions,truncated_untruncated_cosine=cosine,loss=untruncated['loss']);del model64,ug,tg,untruncated,truncated,theta
  torch.cuda.empty_cache()
 c.gate('A4',dict(models=a4,direction_seed=seed,relative_definition='|central difference - autodiff| / max(|central difference|,|autodiff|)',pass_rule='best relative error <= 1e-4 for every direction for both model states',passed=True))
 a5={}
 for name,model in models.items():
  gb=gradient(model,True,kind='base')['grads'];gp=saved[name]['grads'];w=META['response_multiplier']
  combined,row=c.trainer.balanced_gradients(gb,gp,w);assert combined is not None
  bn=torch.linalg.vector_norm(torch.stack([torch.linalg.vector_norm(g) for g in gb]));pn=torch.linalg.vector_norm(torch.stack([torch.linalg.vector_norm(g) for g in gp]));scale=w*bn/pn;reference=[b+scale*p for b,p in zip(gb,gp)]
  norm=torch.linalg.vector_norm(torch.stack([torch.linalg.vector_norm(g) for g in reference]));factor=torch.clamp(1./(norm+1e-6),max=1.);reference=[g*factor for g in reference]
  for p,g in zip(model.parameters(),combined):p.grad=g
  torch.nn.utils.clip_grad_norm_(model.parameters(),1.)
  difference=max(float(torch.max(torch.abs(p.grad-g))) for p,g in zip(model.parameters(),reference));paired_share=float(torch.linalg.vector_norm(torch.stack([torch.linalg.vector_norm(scale*g) for g in gp]))/bn)
  a5[name]=dict(response_weight=w,applied_paired_gradient_norm_share=paired_share,applied_scale=float(scale),base_gradient_norm=float(bn),paired_gradient_norm=float(pn),combined_preclip_norm=float(norm),clip_coefficient=float(factor),maximum_absolute_direction_difference=difference,clip_epsilon=1e-6,interpretation='Clipped gradient delivered to the optimizer, not an AdamW parameter change; no optimizer is instantiated or run.')
 c.gate('A5',dict(models=a5,pass_rule='independent and actual-source clipped FP32 gradient directions agree exactly',passed=all(x['maximum_absolute_direction_difference']==0 for x in a5.values())))
 for name,model in models.items():assert c.checkpoint_state_hash(model.state_dict())==c.RECORD['models'][('rebuilt_initial_tensor_hash' if name=='initial' else 'selected_tensor_hash')]
 c.verify();c.RECORD['status']='IMPLEMENTATION_CHECKS_COMPLETE';c.RECORD['current_phase']='B exclusion accounting next';c.save();print('IMPLEMENTATION_CHECKS_COMPLETE',flush=True)

def main():
 # Isolated execution log; frozen source modules and existing scientific records are untouched.
 sys.path.insert(0,str(c.FROZEN))
 import acd_stage18_gpu_lease as lease
 lease.OUT=c.OUT;lease.freeze_ready=c.verify
 with lease.lease(2) as card:
  c.RECORD['verification_gpu']=card;c.save();run_checks(card)
if __name__=='__main__':
 try:main()
 except SystemExit:raise
 except BaseException as e:
  c.RECORD['status']='FAILED_EXECUTION';c.RECORD['exception']=repr(e);c.save();traceback.print_exc();raise
 finally:torch.optim.AdamW.__init__=original_optimizer_init
