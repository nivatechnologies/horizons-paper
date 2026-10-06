"""Isolated Stage9 forcing-conditioned training: mounts new train/val data only."""
import os,time,json,math,argparse,hashlib
import numpy as np,torch
from torch import nn
from pathlib import Path
class Emulator(nn.Module):
 def __init__(self):
  super().__init__();sizes=[13,256,256,256,256,1];layers=[]
  for i in range(5):
   k=5 if i<4 else 1;layers.append(nn.Conv1d(sizes[i],sizes[i+1],k,padding=k//2,padding_mode='circular'))
   if i<4:layers.append(nn.GELU())
  self.net=nn.Sequential(*layers)
 def forward(self,H,A,F):return H[:,-1]+self.net(torch.cat([H,A[:,None],F[:,None,None].expand(-1,1,40)],1))[:,0]
def run(name,data,out,micro):
 torch.set_num_threads(4);torch.manual_seed(61006);torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
 torch.backends.cudnn.deterministic=True;torch.backends.cudnn.benchmark=False
 out.mkdir(parents=True,exist_ok=True);begin=time.monotonic();cap=36000;model=Emulator().cuda();opt=torch.optim.AdamW(model.parameters(),lr=.001,weight_decay=.0001)
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
  loss=ctx.sum()*0
  for t in range(36):
   pred=model(ctx,action,forcing);delta=(pred.reshape(-1,2,40)[:,0]-pred.reshape(-1,2,40)[:,1])-(T[:,0,t]-T[:,1,t])
   loss=loss+delta.square().mean()/36;ctx=torch.cat([ctx[:,1:],pred[:,None]],1)
  return loss
 # Same initial model and fixed normalization samples for both; no panel/validation read here.
 nr=np.random.default_rng(6100602);normalbase=normaldiff=0.
 with torch.no_grad():
  for _ in range(64):
   ids=nr.integers(len(d['H']),size=128)
   for b in range(0,128,micro):
    H,A,F,T=tensors(ids[b:b+micro]);w=len(H)/128;normalbase+=base(H,A,F,T).item()*w/64;normaldiff+=paired(H,A,F,T).item()*w/64
 assert normalbase>0 and normaldiff>0
 def validate():
  total=0.
  with torch.no_grad():
   for b in range(0,len(v['H']),micro):
    H,A,F,T=[torch.tensor(v[k][b:b+micro],device='cuda') for k in ['H','A','F','T']]
    ctx=H
    for t in range(12):
     pred=model(ctx,A[:,0],F);total+=(pred-T[:,0,t]).square().mean().item()*len(H)/(len(v['H'])*12);ctx=torch.cat([ctx[:,1:],pred[:,None]],1)
  return total
 best=float('inf');chosen=None;recent=[];log=[];step=0
 for iteration in range(1,20001):
  torch.cuda.synchronize()
  if time.monotonic()-begin+(max(recent) if recent else 0)+120>=cap:break
  start=time.monotonic();ids=R.integers(len(d['H']),size=128);opt.zero_grad();value=0.
  for b in range(0,128,micro):
   H,A,F,T=tensors(ids[b:b+micro]);loss=base(H,A,F,T)
   if name=='CNN-F-resp':loss=loss+(normalbase/normaldiff)*paired(H,A,F,T)
   if not torch.isfinite(loss):raise RuntimeError('nonfinite loss')
   w=len(H)/128;(w*loss).backward();value+=w*loss.item()
  nn.utils.clip_grad_norm_(model.parameters(),1.);opt.param_groups[0]['lr']=.001*.5*(1+math.cos(math.pi*(iteration-1)/20000));opt.step();step=iteration
  torch.cuda.synchronize();recent.append(time.monotonic()-start);recent=recent[-32:]
  if iteration%100==0:
   row=dict(step=iteration,loss=value,charged_gpu_seconds=time.monotonic()-begin);log.append(row);(out/'progress.json').write_text(json.dumps(log,indent=2));print(row,flush=True)
  if iteration%1000==0:
   score=validate();path=out/f'checkpoint_{iteration:06d}.pt'
   ck=dict(state_dict=model.state_dict(),step=iteration,validation_MSE=score,forcing_conditioned=True);torch.save(ck,path)
   if score<best:best=score;chosen=iteration;torch.save(ck,out/'selected.pt')
 # If cap before first scheduled checkpoint, preserve current checkpoint and validation; label R-other.
 if chosen is None:
  score=validate();chosen=step;best=score;torch.save(dict(state_dict=model.state_dict(),step=step,validation_MSE=score,forcing_conditioned=True),out/'selected.pt')
 torch.cuda.synchronize()
 result=dict(model=name,step=step,selected_step=chosen,validation_MSE=best,parameter_count=sum(p.numel() for p in model.parameters()),charged_gpu_seconds=time.monotonic()-begin,cap_seconds=cap,capped=step<20000,gpu=torch.cuda.get_device_name(),torch=torch.__version__,normal_base=normalbase,normal_difference=normaldiff,microbatch=micro,data_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in data.glob('*.npz')},selected_sha256=hashlib.sha256((out/'selected.pt').read_bytes()).hexdigest())
 (out/'complete.json').write_text(json.dumps(result,indent=2)+'\n');print(result,flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--name',required=True);p.add_argument('--data',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--micro',type=int,default=32);a=p.parse_args();run(a.name,a.data,a.out,a.micro)
