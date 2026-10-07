"""Stage10b guarded control and response-weight sweep; training-only inputs."""
import os,time,json,math,argparse,hashlib
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
def run(name,data,out,micro,prior_charge=0.,resp_weight=1.):
 torch.set_num_threads(4);torch.manual_seed(61006);torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
 torch.backends.cudnn.deterministic=True;torch.backends.cudnn.benchmark=False
 out.mkdir(parents=True,exist_ok=True);begin=time.monotonic();cap=36000-prior_charge;model=Emulator(name!='CNN-noF').cuda();opt=torch.optim.AdamW(model.parameters(),lr=.001,weight_decay=.0001)
 d=np.load(data/'train.npz');v=np.load(data/'val.npz');R=np.random.default_rng(6100601)
 def tensors(indices):
  return [torch.tensor(d[k][indices],device='cuda') for k in ['H','A','F','T']]
 def base(H,A,F,T):
  loss=H.sum()*0;ctx=H
  for t in range(4):
   pred=model(ctx,A[:,0],F);e=(pred-T[:,0,t]).square().mean();loss=loss+e/4+(e if t==0 else 0);ctx=torch.cat([ctx[:,1:],pred[:,None]],1)
  return loss
 def paired(H,A,F,T):
  ctx=H.repeat_interleave(2,0);action=A.reshape(-1,40);forcing=F.repeat_interleave(2)
  loss=ctx.sum()*0;maximum=0.
  for t in range(36):
   pred=model(ctx,action,forcing);delta=(pred.reshape(-1,2,40)[:,0]-pred.reshape(-1,2,40)[:,1])-(T[:,0,t]-T[:,1,t])
   maximum=max(maximum,float(pred.detach().abs().max()));loss=loss+delta.square().mean()/36;ctx=torch.cat([ctx[:,1:],pred[:,None]],1)
  return loss,maximum
 # Same initial model and fixed normalization samples for both; no panel/validation read here.
 nr=np.random.default_rng(6100602);normalbase=normaldiff=0.
 with torch.no_grad():
  for _ in range(64 if name!='CNN-noF' else 0):
   ids=nr.integers(len(d['H']),size=128)
   for b in range(0,128,micro):
    H,A,F,T=tensors(ids[b:b+micro]);w=len(H)/128;normalbase+=base(H,A,F,T).item()*w/64;normaldiff+=paired(H,A,F,T)[0].item()*w/64
 if name!='CNN-noF':assert normalbase>0 and normaldiff>0
 if name!='CNN-noF':assert normalbase==0.35864407243207097 and normaldiff==0.05537332111271098, 'Stage9 normalizers changed'
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
 for iteration in range(1,20001):
  torch.cuda.synchronize()
  if time.monotonic()-begin+(max(recent) if recent else 0)+120>=cap:break
  start=time.monotonic();ids=R.integers(len(d['H']),size=128);opt.zero_grad();value=0.;components=[];bad=None;gradient_norm=None;max_prediction=None
  for b in range(0,128,micro):
   H,A,F,T=tensors(ids[b:b+micro]);base_loss=base(H,A,F,T);paired_loss=base_loss.new_zeros(());maximum=None
   if name.startswith('CNN-F-resp'):paired_loss,maximum=paired(H,A,F,T)
   loss=base_loss+(resp_weight*(normalbase/normaldiff)*paired_loss if name.startswith('CNN-F-resp') else 0)
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
  torch.cuda.synchronize();recent.append(time.monotonic()-start);recent=recent[-32:]
  if iteration%100==0:
   row=dict(step=iteration,loss=value,microbatches=components,gradient_norm=gradient_norm,completed_updates=completed,skipped_updates=skipped,charged_gpu_seconds=time.monotonic()-begin);log.append(row);(out/'progress.json').write_text(dumps(log));print(dumps(row),flush=True)
  if iteration%1000==0:
   score=validate();path=out/f'checkpoint_{iteration:06d}.pt'
   ck=dict(state_dict=model.state_dict(),step=iteration,validation_MSE=score,forcing_conditioned=name!='CNN-noF');torch.save(ck,path)
   if score<best:best=score;chosen=iteration;torch.save(ck,out/'selected.pt')
  if abort:break
 # If cap before first scheduled checkpoint, preserve current checkpoint and validation; label R-other.
 if chosen is None:
  score=validate();chosen=step;best=score;torch.save(dict(state_dict=model.state_dict(),step=step,validation_MSE=score,forcing_conditioned=True),out/'selected.pt')
 from acd_stage10_loss_balance import measure
 balance=measure(model,data,micro,normalbase,normaldiff,resp_weight) if name.startswith('CNN-F-resp') else dict(scope='not applicable: base-only CNN-noF')
 terminal=out/'terminal.pt';torch.save(dict(state_dict=model.state_dict(),step=step,forcing_conditioned=name!='CNN-noF'),terminal)
 balance.update(model=name,terminal_step=step,terminal_sha256=hashlib.sha256(terminal.read_bytes()).hexdigest(),selected_sha256=hashlib.sha256((out/'selected.pt').read_bytes()).hexdigest())
 (out/'terminal_loss_balance.json').write_text(dumps(balance))
 torch.cuda.synchronize()
 result=dict(model=name,step=step,scheduled_updates=step,completed_updates=completed,skipped_updates=skipped,abort=abort,guarded=True,guard_recipe_equivalence=('no update was skipped; guard changed no optimizer update' if skipped==0 else 'guard skipped updates'),selected_step=chosen,validation_MSE=best,parameter_count=sum(p.numel() for p in model.parameters()),charged_gpu_seconds=time.monotonic()-begin+prior_charge,current_run_gpu_seconds=time.monotonic()-begin,discarded_gpu_seconds=prior_charge,cap_seconds=36000,capped=step<20000,gpu=torch.cuda.get_device_name(),torch=torch.__version__,normal_base=normalbase,normal_difference=normaldiff,response_multiplier=resp_weight,terminal_loss_balance=balance,microbatch=micro,data_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in data.glob('*.npz')},selected_sha256=hashlib.sha256((out/'selected.pt').read_bytes()).hexdigest())
 (out/'complete.json').write_text(dumps(result));print(dumps(result),flush=True)
def clean(v):
 if isinstance(v,float) and not math.isfinite(v):return str(v)
 if isinstance(v,dict):return {k:clean(x) for k,x in v.items()}
 if isinstance(v,list):return [clean(x) for x in v]
 return v
def dumps(v):return json.dumps(clean(v),indent=2,allow_nan=False)+'\n'
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--name',required=True);p.add_argument('--data',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--micro',type=int,default=128);p.add_argument('--prior-charge',type=float,default=0.);p.add_argument('--resp-weight',type=float,required=True);a=p.parse_args();assert (a.name,a.resp_weight) in [('CNN-F-resp-0.1',.1),('CNN-F-resp-0.01',.01),('CNN-noF',0.)];run(a.name,a.data,a.out,a.micro,a.prior_charge,a.resp_weight)
