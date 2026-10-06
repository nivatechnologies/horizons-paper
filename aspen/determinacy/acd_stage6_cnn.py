"""Stage6C: frozen CNN-20k, saved-draw noise-free windows, GPU inference only."""
import os
os.environ['JAX_PLATFORMS']='cpu'
os.environ['JAX_ENABLE_X64']='true'
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
os.environ['NUMBA_NUM_THREADS']='2'
import json,time,numpy as np
import torch
from torch import nn
from acd_protocol import ROOT,INHERITED,PATTERNS,physics,SIGMA,WINDOWS
from acd_stage6_forward import RAW,OUT
from acd_stage6_analysis import sha,save,binary,stack,comparisons,calibration
class Emulator(nn.Module):
 def __init__(self):
  super().__init__();sizes=[12,256,256,256,256,1];layers=[]
  for i in range(5):
   k=5 if i<4 else 1
   layers.append(nn.Conv1d(sizes[i],sizes[i+1],k,padding=k//2,padding_mode='circular'))
   if i<4:layers.append(nn.GELU())
  self.net=nn.Sequential(*layers)
 def forward(self,frames,action):
  return frames[:,-1]+self.net(torch.cat([frames,action[:,None]],1))[:,0]
def histories(c):
 p=OUT/f'H_{c:03d}.npz'
 if p.exists():
  with np.load(p) as d:return d['H']
 with np.load(RAW/f'conf/case_{c:03d}.npz') as d:theta=d['theta'].copy();x0=d['x0'].copy()
 H=physics.simulate(theta[:,:40],np.repeat(theta[:,40,None],40,1),.01,11)
 error=float(np.max(np.abs(H[:,-1]-x0)))
 if error>1e-12:raise RuntimeError('Noise-free history endpoint mismatch')
 np.savez_compressed(p,H=H)
 return H
def predict(model,H,micro):
 n=len(H);last=int(WINDOWS[3][-1]);J=np.empty((n,9));valid=np.empty((n,9),bool)
 window=set(int(x) for x in WINDOWS[3])
 with torch.inference_mode():
  for first in range(0,n*9,micro):
   ids=np.arange(first,min(n*9,first+micro))
   context=torch.tensor(H[ids//9]/SIGMA,dtype=torch.float32,device='cuda')
   action=torch.tensor(.16*PATTERNS[ids%9]/SIGMA,dtype=torch.float32,device='cuda')
   alive=torch.ones(len(ids),dtype=torch.bool,device='cuda');total=torch.zeros(len(ids),dtype=torch.float64,device='cuda')
   for t in range(last+1):
    state=context[:,-1].double()*SIGMA
    alive &= torch.isfinite(state).all(-1)&(torch.sqrt((state*state).mean(-1))<=10*SIGMA)
    if t in window:total+=.5*(state*state).mean(-1)/len(window)
    if t<last:
     context[~alive]=0
     pred=model(context,action);context=torch.cat([context[:,1:],pred[:,None]],1)
   J[ids//9,ids%9]=total.cpu().numpy();valid[ids//9,ids%9]=alive.cpu().numpy()
 return J,valid
def score_C(post,keep,jbar):
 # Only the scoring function opens saved truth costs; CNN windows/model never do.
 from acd_questions import labels
 truth=[]
 for c in range(200):
  with np.load(RAW/f'conf/score_{c:03d}.npz') as d:truth.append(labels(d['actual_cost'],jbar)[0,np.r_[np.arange(8),37]])
 truth=np.array(truth)
 return calibration(post,truth,keep)[3]
def run():
 start=time.perf_counter();torch.set_num_threads(1)
 torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
 torch.backends.cudnn.deterministic=True;torch.backends.cudnn.benchmark=False
 checkpoint=INHERITED/'inputs/CNN-20k.pt';h=sha(checkpoint)
 ckpt=torch.load(checkpoint,map_location='cpu',weights_only=True)
 assert ckpt['step']==20000 and ckpt['sigma']==SIGMA
 model=Emulator();model.load_state_dict(ckpt['state_dict']);model.eval()
 receipt=OUT/'C.json';rules=[];micro=256
 try:model.to('cuda')
 except (torch.cuda.OutOfMemoryError,RuntimeError) as e:
  save(receipt,dict(status='SKIPPED',reason=str(e),rules=[dict(rule='R-gpu',resolution='Model does not fit with Qwen running; skip C, no service changes')],checkpoint_sha256=h));return
 stage2=json.load(open(ROOT/'receipts/acd_stage2.json'));jbar=stage2['null']['jbar'];null=np.array(stage2['null']['question_probabilities'])[np.r_[np.arange(8),37]]
 post=[];keep=[];members=[]
 for c in range(200):
  path=OUT/f'CNN_{c:03d}.npz'
  with np.load(RAW/f'conf/case_{c:03d}.npz') as d:keep.append(not bool(d['excluded']))
  if path.exists():
   with np.load(path) as d:J=d['J'];valid=d['valid'];used_micro=int(d['microbatch']) if 'microbatch' in d else 64
  else:
   H=histories(c)
   while True:
    try:J,valid=predict(model,H,micro);break
    except torch.cuda.OutOfMemoryError:
     torch.cuda.empty_cache()
     if micro==1:
      save(receipt,dict(status='SKIPPED',reason='GPU OOM at microbatch1',rules=rules+[dict(rule='R-gpu',resolution='Skip incomplete C; Qwen unchanged')],checkpoint_sha256=h));return
     micro=max(1,micro//2);rules.append(dict(rule='R-gpu',case=c,microbatch=micro,resolution='Reduce inference microbatch only; Qwen unchanged'))
   np.savez_compressed(path,J=J,valid=valid,microbatch=micro)
   used_micro=micro
  # Any divergent draw prevents declaring confidence for this case; never condition on surviving draws.
  if valid.all():
   full=np.zeros((len(J),9,8));full[:,:,3]=J;s=binary(full,jbar,null)
  else:
   full=np.zeros((1,9,8));s=binary(full,jbar,null);s['confident'][:]=False;s['observation'][:]=False
   rules.append(dict(rule='R-other',case=c,resolution='CNN has divergent draw; case contributes no confident answer, do not discard draws selectively'))
  post.append(s);members.append(dict(case=c,draws=len(J),valid_draws=int(valid.all(1).sum()),microbatch=used_micro))
  print('CNN-own-window',c,'draws',len(J),'micro',micro,'elapsed',round(time.perf_counter()-start,1),flush=True)
 s=stack(post);keep=np.array(keep)
 reading=comparisons(s,keep)[3]
 save(receipt,dict(status='COMPLETE',post_hoc=True,licenses_frozen_route=False,panel='confirmation',checkpoint_sha256=h,
  normalization=SIGMA,action_amplitude=.16,device='cuda',tf32=False,training=False,noise_free_H=True,microbatch=micro,
  members=members,comparisons_2LT=reading,calibration_2LT=score_C(s,keep,jbar),rules=rules,seconds=time.perf_counter()-start,
  limitation='Frozen surrogate uses noise-free draw history and action; inferred F is encoded only indirectly in history, not supplied as a separate channel.'))
if __name__=='__main__':run()
