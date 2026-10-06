"""End-of-training loss balance on the frozen training-only probe."""
import json,hashlib,argparse
from pathlib import Path
import numpy as np,torch
def measure(model,data,micro,normal_base,normal_difference,multiplier):
 d=np.load(data/'train.npz');rng=np.random.default_rng(6100602)
 base_total=difference_total=0.;model.eval()
 with torch.no_grad():
  for _ in range(64):
   ids=rng.integers(len(d['H']),size=128)
   for b in range(0,128,micro):
    H,A,F,T=[torch.tensor(d[k][ids[b:b+micro]],device='cuda') for k in ['H','A','F','T']]
    weight=len(H)/(128*64);ctx=H;base=H.sum()*0
    for t in range(4):
     pred=model(ctx,A[:,0],F);e=(pred-T[:,0,t]).square().mean()
     base=base+e/4+(e if t==0 else 0);ctx=torch.cat([ctx[:,1:],pred[:,None]],1)
    ctx=H.repeat_interleave(2,0);action=A.reshape(-1,40);forcing=F.repeat_interleave(2);difference=H.sum()*0
    for t in range(36):
     pred=model(ctx,action,forcing)
     delta=(pred.reshape(-1,2,40)[:,0]-pred.reshape(-1,2,40)[:,1])-(T[:,0,t]-T[:,1,t])
     difference=difference+delta.square().mean()/36;ctx=torch.cat([ctx[:,1:],pred[:,None]],1)
    base_total+=base.item()*weight;difference_total+=difference.item()*weight
 coefficient=multiplier*(normal_base/normal_difference)
 return dict(multiplier=multiplier,normal_base=normal_base,normal_difference=normal_difference,
  difference_coefficient=coefficient,base_loss=base_total,difference_loss=difference_total,
  weighted_difference_loss=coefficient*difference_total,
  difference_to_base_ratio=coefficient*difference_total/base_total,
  weighted_difference_fraction=coefficient*difference_total/(base_total+coefficient*difference_total),
  probe_seed=6100602,probe_batches=64,probe_batch_size=128,
  scope='training-only fixed probe; terminal model, not a checkpoint selection criterion')
def main():
 from acd_stage10_train import Emulator
 p=argparse.ArgumentParser();p.add_argument('--checkpoint',type=Path,required=True);p.add_argument('--receipt',type=Path,required=True);p.add_argument('--data',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
 a=p.parse_args();torch.set_num_threads(4);torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False;torch.backends.cudnn.deterministic=True;torch.backends.cudnn.benchmark=False
 ck=torch.load(a.checkpoint,map_location='cpu',weights_only=True);model=Emulator().cuda();model.load_state_dict(ck['state_dict'])
 receipt=json.load(open(a.receipt));d=measure(model,a.data,128,receipt['normal_base'],receipt['normal_difference'],1.)
 d.update(model=receipt['model'],terminal_step=ck['step'],checkpoint_sha256=hashlib.sha256(a.checkpoint.read_bytes()).hexdigest())
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(d,indent=2)+'\n');print(d,flush=True)
if __name__=='__main__':main()
