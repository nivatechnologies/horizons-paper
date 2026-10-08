"""Original-panel uniform readability and E1 rolling traces, without outcomes."""
import argparse,json,time
from pathlib import Path
import numpy as np
import torch
from acd_stage20_gpu import setup,manifest,commit_npz,write,digest

def run(a):
 from acd_stage18_estimators import Estimator
 from acd_stage9_cnn import ForcingModel,Emulator
 setup();settings=json.loads((a.data/'settings.json').read_text());sigma=settings['sigma']
 pattern=np.asarray(settings['patterns'])[0];assert np.all(pattern==-1), 'Uniform-decrease action must be negative one at every site'
 if a.kind=='E0':
  paths=sorted(a.models.glob('E0-seed*/selected.pt'));assert len(paths)==5
 else:paths=[a.models/f'E1-seed{a.seed}/selected.pt']
 estimators=[]
 for p in paths:
  e=Estimator(a.kind=='E1').cuda().eval();e.load_state_dict(torch.load(p,map_location='cpu',weights_only=True)['state_dict']);estimators.append(e)
 model=None
 if a.name!='physics':
  model=(ForcingModel() if a.name.startswith('CNN-F') else Emulator()).cuda().eval();model.load_state_dict(torch.load(a.models/(('CNN-F' if a.kind=='E1' else a.name)+'.pt'),map_location='cpu',weights_only=True)['state_dict'])
 a.out.mkdir(parents=True,exist_ok=True);hashes=manifest(a.out);branches=[0] if a.kind=='E0' else [8,0]
 def rhs(x,f):return (torch.roll(x,-1,-1)-torch.roll(x,2,-1))*torch.roll(x,1,-1)-x+f[:,None]
 for case in range(200):
  target=a.out/f'{case:03d}.npz'
  if target.name in hashes:continue
  start=time.monotonic()
  with np.load(a.data/f'{case:03d}.npz') as z:H=z['H'].copy();F=z['F'].copy()
  ests=np.empty((len(estimators),len(H),len(branches),49));valid=np.ones((len(H),len(branches)),bool)
  with torch.no_grad():
   for b in range(0,len(H),a.micro):
    for branch_index,option in enumerate(branches):
     amount=.16*pattern if option==0 else np.zeros_like(pattern)
     ctx=torch.tensor(H[b:b+a.micro]/sigma,device='cuda',dtype=torch.float32)
     action=torch.tensor(np.broadcast_to(amount/sigma,(len(ctx),40)).copy(),device='cuda',dtype=torch.float32)
     f=torch.tensor((F[b:b+a.micro]-8)/2,device='cuda',dtype=torch.float32)
     phys=torch.tensor(H[b:b+a.micro],device='cuda',dtype=torch.float64);x=phys[:,-1].clone()
     forcing=torch.tensor(F[b:b+a.micro]-(.16 if option==0 else 0),device='cuda',dtype=torch.float64)
     for s in range(49):
      estimated=[]
      for j,e in enumerate(estimators):
       value=e(ctx,action) if a.kind=='E1' else e(ctx)
       estimated.append(value);ests[j,b:b+len(ctx),branch_index,s]=value.cpu().numpy().astype(float)*2+8
      state=phys[:,-1] if model is None else ctx[:,-1].double()*sigma
      valid[b:b+len(ctx),branch_index] &= (torch.isfinite(state).all(-1)&(state.square().mean(-1).sqrt()<=10*sigma)).cpu().numpy()
      if s==48:continue
      if model is None:
       for _ in range(5):
        k1=rhs(x,forcing);k2=rhs(x+.005*k1,forcing);k3=rhs(x+.005*k2,forcing);k4=rhs(x+.01*k3,forcing);x=x+.01/6*(k1+2*k2+2*k3+k4)
       phys=torch.cat([phys[:,1:],x[:,None]],1);ctx=(phys/sigma).float()
      else:
       context=estimated[0] if a.kind=='E1' else f
       pred=model(ctx,action,context) if a.name.startswith('CNN-F') else model(ctx,action)
       ctx=torch.cat([ctx[:,1:],pred[:,None]],1)
  commit_npz(target,dict(estimated_F=ests,valid=valid,options=np.asarray(branches),steps=np.arange(49)),hashes)
  print(a.name,case,len(H),time.monotonic()-start,flush=True)
 write(a.out/'complete.json',dict(name=a.name,kind=a.kind,seed=a.seed,host=__import__('socket').gethostname(),GPU=torch.cuda.get_device_name(),output_hashes=hashes,adapter_sha256=digest(__file__),estimator_hashes={str(p.relative_to(a.models)):digest(p) for p in paths},checkpoint_sha256=digest(a.models/(('CNN-F' if a.kind=='E1' else a.name)+'.pt')) if model is not None else None,options=branches,no_outcome_access=True))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--kind',choices=['E0','E1'],required=True);p.add_argument('--name',required=True);p.add_argument('--seed',type=int);p.add_argument('--models',type=Path,required=True);p.add_argument('--data',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--micro',type=int,default=1024);run(p.parse_args())
