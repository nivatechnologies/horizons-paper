"""Stage18 history-only response training; guarded paired recipe, training-only inputs."""
import os,time,json,math,argparse,hashlib,subprocess
import numpy as np,torch
from torch import nn
from pathlib import Path
class Emulator(nn.Module):
 def __init__(self,conditioned=True):
  super().__init__();self.conditioned=conditioned;sizes=[13 if conditioned else 12,256,256,256,256,1];layers=[]
  for i in range(5):
   k=5 if i<4 else 1;layers.append(nn.Conv1d(sizes[i],sizes[i+1],k,padding=k//2,padding_mode='circular'))
   if i<4:layers.append(nn.GELU())
  self.net=nn.Sequential(*layers)
 def forward(self,H,A,F):
  channels=[H,A[:,None]]
  if self.conditioned:channels.append(F[:,None,None].expand(-1,1,40))
  return H[:,-1]+self.net(torch.cat(channels,1))[:,0]
def run(name,data,out,micro,torch_seed,batch_seed,resp_weight):
 from acd_stage18_inference import guarded,digest
 guarded()
 if (out/'complete.json').exists():return
 marker=json.loads((data/'generation_pushed.json').read_text())
 if digest(data/'manifest.json')!=marker['manifest_sha256']:raise RuntimeError('Response data manifest differs from pushed generation')
 committed=json.loads(subprocess.check_output(['git','show',marker['commit']+':aspen/determinacy/receipts/acd_stage18_response_data.json'],text=True))
 generation=json.loads((data/'manifest.json').read_text())
 if committed!=generation:raise RuntimeError('Response data generation receipt is not the committed receipt')
 for filename,expected in generation['data_sha256'].items():
  if digest(data/filename)!=expected:raise RuntimeError('Response training data differs from generation receipt')
 from acd_stage18_charge import Charge
 budget=Charge(out)
 resume=out/'resume.pt';saved=torch.load(resume,map_location='cpu',weights_only=False) if resume.exists() else None
 prior_charge=budget.prior;conditioned=False
 torch.set_num_threads(4);torch.manual_seed(torch_seed);torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
 torch.backends.cudnn.deterministic=True;torch.backends.cudnn.benchmark=False
 out.mkdir(parents=True,exist_ok=True);begin=budget.started;cap=36000-prior_charge;model=Emulator(conditioned).cuda();opt=torch.optim.AdamW(model.parameters(),lr=.001,weight_decay=.0001)
 d=np.load(data/'train.npz');v=np.load(data/'val.npz');R=np.random.default_rng(batch_seed)
 def tensors(indices):
  return [torch.tensor(d[k][indices],device='cuda') for k in ['H','A','F','T']]
 def base(H,A,F,T):
  ctx=H.repeat_interleave(2,0);action=A.reshape(-1,40);forcing=F.repeat_interleave(2);targets=T.reshape(-1,36,40)
  loss=ctx.sum()*0
  for tick in range(4):
   pred=model(ctx,action,forcing);e=(pred-targets[:,tick]).square().mean();loss+=e/4+(e if tick==0 else 0);ctx=torch.cat([ctx[:,1:],pred[:,None]],1)
  return loss
 def paired(H,A,F,T):
  ctx=H.repeat_interleave(2,0);action=A.reshape(-1,40);forcing=F.repeat_interleave(2);loss=ctx.sum()*0;maximum=0.
  for tick in range(36):
   pred=model(ctx,action,forcing);difference=(pred.reshape(-1,2,40)[:,0]-pred.reshape(-1,2,40)[:,1])-(T[:,0,tick]-T[:,1,tick]);loss+=difference.square().mean()/36
   current=float(pred.detach().abs().max());maximum=max(maximum,current) if math.isfinite(current) else current;ctx=torch.cat([ctx[:,1:],pred[:,None]],1)
  return loss,maximum
 normalbase=normaldiff=0.
 nr=np.random.default_rng(np.random.SeedSequence([batch_seed,3]))
 if saved is not None:
  normalbase,normaldiff=saved['normal_base'],saved['normal_difference']
 else:
  with torch.no_grad():
   for _ in range(64):
    ids=nr.integers(len(d['H']),size=128)
    for b in range(0,128,micro):
     H,A,F,T=tensors(ids[b:b+micro]);w=len(H)/128;normalbase+=float(base(H,A,F,T))*w/64;pl,_=paired(H,A,F,T);normaldiff+=float(pl)*w/64;budget.snapshot()
 if not (math.isfinite(normalbase) and math.isfinite(normaldiff) and normalbase>0 and normaldiff>0):raise RuntimeError('Invalid initial response normalization')
 def validate():
  total=0.
  with torch.no_grad():
   for b in range(0,len(v['H']),micro):
    H,A,F,T=[torch.tensor(v[k][b:b+micro],device='cuda') for k in ['H','A','F','T']]
    ctx=H
    for t in range(12):
     pred=model(ctx,A[:,0],F);total+=(pred-T[:,0,t]).square().mean().item()*len(H)/(len(v['H'])*12);ctx=torch.cat([ctx[:,1:],pred[:,None]],1)
  return total
 best=float('inf');chosen=None;recent=[];log=[];step=0;completed=skipped=consecutive=0;abort=None;skip_log=[]
 if saved is not None:
  ck=saved
  model.load_state_dict(ck['state_dict']);opt.load_state_dict(ck['optimizer'])
  R.bit_generator.state=ck['batch_rng'];torch.set_rng_state(ck['torch_rng']);torch.cuda.set_rng_state_all(ck['cuda_rng'])
  step=ck['step'];best=ck['best'];chosen=ck['chosen'];completed=ck['completed'];skipped=ck['skipped'];consecutive=ck['consecutive'];log=ck['log'];skip_log=ck['skip_log']
  if chosen is not None:
   selected_checkpoint=out/f'checkpoint_{chosen:06d}.pt'
   eligible=torch.load(selected_checkpoint,map_location='cpu',weights_only=True)
   if eligible['step']!=chosen or eligible['validation_MSE']!=best:raise RuntimeError('Selected scheduled checkpoint identity mismatch')
   (out/'selected.tmp.pt').write_bytes(selected_checkpoint.read_bytes());(out/'selected.tmp.pt').replace(out/'selected.pt')
  # Startup, checkpoint loading and all GPU work remain charged from begin.
 for iteration in range(step+1,20001):
  torch.cuda.synchronize()
  if time.monotonic()-begin+(max(recent) if recent else 0)+120>=cap:break
  start=time.monotonic();ids=R.integers(len(d['H']),size=128);opt.zero_grad();value=0.;components=[];bad=None;gradient_norm=None;max_prediction=None
  for b in range(0,128,micro):
   H,A,F,T=tensors(ids[b:b+micro]);base_loss=base(H,A,F,T);paired_loss,maximum=paired(H,A,F,T)
   loss=base_loss if resp_weight==0 else base_loss+resp_weight*(normalbase/normaldiff)*paired_loss
   components.append(dict(microbatch_start=b,base_loss=float(base_loss.detach()),paired_loss=float(paired_loss.detach()),loss=float(loss.detach()),max_abs_paired_prediction=maximum))
   if maximum is not None:max_prediction=maximum if max_prediction is None else max(max_prediction,maximum)
   if not torch.isfinite(loss):bad='nonfinite microbatch loss';break
   w=len(H)/128;(w*loss).backward();value+=w*loss.item()
  if bad is None:
   norms=[torch.linalg.vector_norm(p.grad.detach()) for p in model.parameters() if p.grad is not None]
   norm=torch.linalg.vector_norm(torch.stack(norms));gradient_norm=float(norm)
   if not torch.isfinite(norm):bad='nonfinite gradient norm'
  opt.param_groups[0]['lr']=.001*.5*(1+math.cos(math.pi*(iteration-1)/20000))
  if bad is None:
   nn.utils.clip_grad_norm_(model.parameters(),1.);opt.step();completed+=1;consecutive=0
  else:
   opt.zero_grad();skipped+=1;consecutive+=1
   skip=dict(step=iteration,reason=bad,microbatches=components,gradient_norm=gradient_norm,max_abs_paired_prediction=max_prediction,skipped_updates=skipped,consecutive_skips=consecutive)
   skip_log.append(skip);(out/'skips.json').write_text(dumps(skip_log));print(dumps(skip),flush=True)
   if skipped>20 or consecutive>=3:abort='skip limit exceeded'
  step=iteration
  budget.snapshot()
  torch.cuda.synchronize();recent.append(time.monotonic()-start);recent=recent[-32:]
  if iteration%100==0:
   row=dict(step=iteration,loss=value,microbatches=components,gradient_norm=gradient_norm,completed_updates=completed,skipped_updates=skipped,charged_gpu_seconds=prior_charge+time.monotonic()-begin);log.append(row);(out/'progress.json').write_text(dumps(log));print(dumps(row),flush=True)
  if iteration%1000==0:
   score=validate();path=out/f'checkpoint_{iteration:06d}.pt'
   ck=dict(state_dict=model.state_dict(),step=iteration,validation_MSE=score,forcing_conditioned=conditioned);torch.save(ck,path.with_suffix('.tmp.pt'));path.with_suffix('.tmp.pt').replace(path)
   if score<best:
    best=score;chosen=iteration;torch.save(ck,out/'selected.tmp.pt');(out/'selected.tmp.pt').replace(out/'selected.pt')
   recovery=dict(state_dict=model.state_dict(),optimizer=opt.state_dict(),batch_rng=R.bit_generator.state,torch_rng=torch.get_rng_state(),cuda_rng=torch.cuda.get_rng_state_all(),step=step,best=best,chosen=chosen,completed=completed,skipped=skipped,consecutive=consecutive,log=log,skip_log=skip_log,normal_base=normalbase,normal_difference=normaldiff,charged_gpu_seconds=prior_charge+time.monotonic()-begin)
   torch.save(recovery,out/'resume.tmp.pt');(out/'resume.tmp.pt').replace(resume)
  if abort:break
 if chosen is None:
  result=dict(model=name,status='failed_no_eligible_checkpoint',abort=abort or 'cap before a finite scheduled validation checkpoint',step=step,completed_updates=completed,skipped_updates=skipped,selected_step=None,charged_gpu_seconds=prior_charge+time.monotonic()-begin)
  budget.snapshot()
  (out/'complete.json').write_text(dumps(result));print(dumps(result),flush=True);return
 balance=dict(scope='response loss normalization',normal_base=normalbase,normal_difference=normaldiff,response_weight=resp_weight)
 terminal=out/'terminal.pt';torch.save(dict(state_dict=model.state_dict(),step=step,forcing_conditioned=conditioned),terminal)
 balance.update(model=name,terminal_step=step,terminal_sha256=hashlib.sha256(terminal.read_bytes()).hexdigest(),selected_sha256=hashlib.sha256((out/'selected.pt').read_bytes()).hexdigest())
 (out/'terminal_loss_balance.json').write_text(dumps(balance))
 torch.cuda.synchronize()
 result=dict(model=name,torch_initialization_seed=torch_seed,batch_order_seed=batch_seed,forcing_conditioned=conditioned,step=step,scheduled_updates=step,completed_updates=completed,skipped_updates=skipped,abort=abort,guarded=True,guard_recipe_equivalence=('no update was skipped; guard changed no optimizer update' if skipped==0 else 'guard skipped updates'),selected_step=chosen,validation_MSE=best,parameter_count=sum(p.numel() for p in model.parameters()),charged_gpu_seconds=time.monotonic()-begin+prior_charge,current_run_gpu_seconds=time.monotonic()-begin,resumed_gpu_seconds=prior_charge,discarded_gpu_seconds=0.,cap_seconds=36000,capped=step<20000,gpu=torch.cuda.get_device_name(),torch=torch.__version__,normal_base=normalbase,normal_difference=normaldiff,response_multiplier=resp_weight,terminal_loss_balance=balance,microbatch=micro,data_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in data.glob('*.npz')},selected_sha256=hashlib.sha256((out/'selected.pt').read_bytes()).hexdigest())
 budget.snapshot()
 (out/'complete.json').write_text(dumps(result));print(dumps(result),flush=True)
def clean(v):
 if isinstance(v,float) and not math.isfinite(v):return str(v)
 if isinstance(v,dict):return {k:clean(x) for k,x in v.items()}
 if isinstance(v,list):return [clean(x) for x in v]
 return v
def dumps(v):return json.dumps(clean(v),indent=2,allow_nan=False)+'\n'
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--name',required=True);p.add_argument('--data',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--micro',type=int,default=128);p.add_argument('--torch-seed',type=int,required=True);p.add_argument('--batch-seed',type=int,required=True);p.add_argument('--response-weight',type=float,required=True);a=p.parse_args();run(a.name,a.data,a.out,a.micro,a.torch_seed,a.batch_seed,a.response_weight)
