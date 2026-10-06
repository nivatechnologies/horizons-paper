"""Stage9 checkpoint inference only. No truth files opened."""
import os,json,time,hashlib,argparse
import torch,numpy as np
from pathlib import Path
from acd_stage9_train import Emulator as ForcingModel
from torch import nn
class Emulator(nn.Module):
 def __init__(self):
  super().__init__();sizes=[12,256,256,256,256,1];layers=[]
  for i in range(5):
   k=5 if i<4 else 1;layers.append(nn.Conv1d(sizes[i],sizes[i+1],k,padding=k//2,padding_mode='circular'))
   if i<4:layers.append(nn.GELU())
  self.net=nn.Sequential(*layers)
 def forward(self,H,A):return H[:,-1]+self.net(torch.cat([H,A[:,None]],1))[:,0]
class CostModel(nn.Module):
 def __init__(self):
  super().__init__();sizes=[12,256,256,256,256];layers=[]
  for i in range(4):layers.extend([nn.Conv1d(sizes[i],sizes[i+1],5,padding=2,padding_mode='circular'),nn.GELU()])
  self.trunk=nn.Sequential(*layers);self.head=nn.Sequential(nn.Linear(256,64),nn.GELU(),nn.Linear(64,1))
 def forward(self,H,A):return self.head(self.trunk(torch.cat([H,A[:,None]],1)).mean(-1))[:,0]
def run(name,checkpoint,data,out,micro):
 torch.set_num_threads(1);torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
 torch.backends.cudnn.deterministic=True;torch.backends.cudnn.benchmark=False
 settings=json.load(open(data/'settings.json'));sigma=settings['sigma'];P=np.array(settings['patterns']);W=[np.array(w,dtype=int) for w in settings['windows']]
 ck=torch.load(checkpoint,map_location='cpu',weights_only=True);conditioned=name.startswith('CNN-F');cost=name=='CNN-cost'
 model=ForcingModel() if conditioned else CostModel() if cost else Emulator()
 model.load_state_dict(ck['state_dict']);model.cuda().eval();out.mkdir(parents=True,exist_ok=True)
 for c in range(200):
  target=out/f'{c:03d}.npz'
  if target.exists():continue
  start=time.monotonic()
  with np.load(data/f'{c:03d}.npz') as d:H=d['H'].copy();F=d['F'].copy()
  n=len(H);J=np.zeros((n,9,8));valid=np.ones((n,9),bool);mean=np.zeros((max(w[-1] for w in W)+1,40))
  while True:
   try:
    for b in range(0,n*9,micro):
     ids=np.arange(b,min(n*9,b+micro));draw=ids//9;action=ids%9
     ctx=torch.tensor(H[draw]/sigma,device='cuda',dtype=torch.float32);a=torch.tensor(.16*P[action]/sigma,device='cuda',dtype=torch.float32);f=torch.tensor((F[draw]-8)/2,device='cuda',dtype=torch.float32)
     with torch.no_grad():
      if cost:
       pred=model(ctx,a).cpu().numpy().astype(float);J[draw,action,3]=pred;valid[draw,action]=np.isfinite(pred)
      else:
       alive=np.ones(len(ids),bool)
       for t in range(len(mean)):
        state=ctx[:,-1].cpu().numpy().astype(float)*sigma
        alive&=np.isfinite(state).all(-1)&(np.sqrt(np.mean(state*state,-1))<=10*sigma)
        for j,w in enumerate(W):
         if t in w:J[draw,action,j]+=.5*np.mean(state*state,-1)/len(w)
        factual=action==8
        if factual.any():mean[t]+=state[factual].sum(0)/n
        if t+1<len(mean):
         pred=model(ctx,a,f) if conditioned else model(ctx,a);ctx=torch.cat([ctx[:,1:],pred[:,None]],1)
       valid[draw,action]=alive
    break
   except torch.cuda.OutOfMemoryError:
    torch.cuda.empty_cache();micro//=2
    if micro<1:raise
    J.fill(0);mean.fill(0);valid.fill(True)
  np.savez_compressed(target,J=J,valid=valid,factual_mean=mean)
  print(name,c,n,micro,round(time.monotonic()-start,2),flush=True)
 (out/'complete.json').write_text(json.dumps(dict(model=name,checkpoint_sha256=hashlib.sha256(checkpoint.read_bytes()).hexdigest(),gpu=torch.cuda.get_device_name(),microbatch=micro,torch=torch.__version__,construction='each posterior draw own noise-free eleven-frame history; own forcing channel for CNN-F models'),indent=2)+'\n')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--name',required=True);p.add_argument('--checkpoint',type=Path,required=True);p.add_argument('--data',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--micro',type=int,default=256);a=p.parse_args();run(a.name,a.checkpoint,a.data,a.out,a.micro)
