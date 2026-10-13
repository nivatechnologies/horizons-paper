"""POST HOC descriptive training/validation effects; forward passes only, no outcomes."""
import os,sys,json,hashlib,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import acd_stage23_closeout_check as c
import numpy as np
import torch
sys.path.insert(0,str(c.FROZEN))
from acd_stage9_cnn import Emulator,ForcingModel
OUT=ROOT/'runs/stage23_pattern_breakdown';OUT.mkdir(parents=True,exist_ok=True)
def sha(p):return c.digest(p)
def write(p,v):p.write_text(json.dumps(v,indent=2,allow_nan=False)+'\n')
def metrics(pred,truth):
 p=pred.ravel();t=truth.ravel();e=p-t
 return dict(label='POST HOC, descriptive',count=len(p),effect_RMSE=float(np.sqrt(np.mean(e**2))),mean_bias=float(np.mean(e)),sign_agreement=float(np.mean(np.sign(p)==np.sign(t))),correlation=float(np.corrcoef(p,t)[0,1]) if np.std(p)>0 and np.std(t)>0 else None,predict_zero_RMSE=float(np.sqrt(np.mean(t**2))))
def main():
 meta=c.verify();close=json.loads((ROOT/'receipts/acd_stage23_closeout.json').read_text());selection=json.loads((ROOT/'receipts/acd_stage23.json').read_text())['selection']
 ids,amp,batch,ref,_=c.rebuild_batch(meta)
 assert c.array_hash(dict(batch,start_indices=ids))==close['batch']['canonical_tensor_sha256']
 assert ids.tolist()==close['batch']['start_indices'] and amp.tolist()==close['batch']['per_start_amplitudes']
 truth1=np.asarray(close['A1b']['physics_action_minus_twin']);window=close['A1b']['window_ticks']
 en=.5*np.mean(ref**2,-1);retruth=en[:,:,0,window].mean(-1)-en[:,:,1,window].mean(-1)
 assert np.array_equal(retruth,truth1),'D1 physics reproduction mismatch'
 data=c.FROZEN/'runs/stage18/response_data';manifest=json.loads((data/'manifest.json').read_text())
 for name,h in manifest['data_sha256'].items():assert sha(data/name)==h
 assert sha(data/'validation_reference.npz')==manifest['validation_reference_sha256']
 with np.load(data/'val.npz') as z:val={k:z[k].copy() for k in ['H','F']}
 with np.load(data/'validation_reference.npz') as z:j=z['J'][:,:,3].copy()
 truth2=j[:,:8]-j[:,8,None];cfg=json.loads((c.FROZEN/'runs/stage18/confirmation_inputs/settings.json').read_text());sigma=cfg['sigma'];patterns=np.asarray(cfg['patterns']);assert cfg['windows'][3]==window
 models=[dict(name='initial',initial=True,conditioned=False)]
 for row in selection['rows']:
  p=ROOT/'runs/stage23/training'/row['model']/'selected.pt';assert sha(p)==row['checkpoint_sha256']
  models.append(dict(name=row['model'],path=str(p),sha256=row['checkpoint_sha256'],conditioned=False,validation_effect_RMSE=row['validation_effect_RMSE']))
 base=Path('/mnt/niva-array/work/aspen-determinacy-stage21-20261008/aspen/determinacy')
 freeze=(base/'ACD_STAGE21_FREEZE_E.md').read_text()
 for name in ['CNN-noF','CNN-F']:
  p=base/'runs/stage21/checkpoints'/f'{name}.pt';h=sha(p);assert h in freeze,'Retained hash absent from Freeze E'
  models.append(dict(name=name+(' (true forcing supplied)' if name=='CNN-F' else ''),path=str(p),sha256=h,conditioned=name=='CNN-F'))
 result=dict(label='POST HOC, descriptive; no pass rules or confirmations',realized_outcome_accesses=[],models=models,data_hashes={str(data/n):sha(data/n) for n in ['train.npz','val.npz','validation_reference.npz']},fixed_batch=close['batch'],code_hashes={str(p):sha(p) for p in [Path(__file__),ROOT/'acd_stage23_train.py',c.FROZEN/'acd_stage18_select.py',c.FROZEN/'acd_stage9_cnn.py',c.INHERITED/'physics.py',c.INHERITED/'protocol.py']},datasets={},reproduction=[])
 torch.set_num_threads(4);torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False;torch.backends.cudnn.deterministic=True;torch.backends.cudnn.benchmark=False
 import acd_stage18_gpu_lease as lease
 lease.OUT=OUT;lease.freeze_ready=lambda:None
 with lease.lease(2) as card:
  os.environ['CUDA_VISIBLE_DEVICES']=card['uuid'];result['gpu']=card
  for item in models:
   if item.get('initial'):
    torch.manual_seed(meta['torch_initialization_seed']);model=c.trainer.Emulator(False)
    assert c.checkpoint_state_hash(model.state_dict())==close['models']['rebuilt_initial_tensor_hash'];item['tensor_sha256']=c.checkpoint_state_hash(model.state_dict())
   else:
    model=ForcingModel() if item['conditioned'] else Emulator();model.load_state_dict(torch.load(item['path'],map_location='cpu',weights_only=True)['state_dict'])
   model.cuda().eval()
   def call(h,a,f):return model(h,a,f) if item.get('initial') or item['conditioned'] else model(h,a)
   for ds,truth in [('D1',truth1),('D2',truth2)]:
    with torch.no_grad():
     if ds=='D1':
      effects=[]
      for b in range(0,len(batch['H']),32):
       h=torch.tensor(batch['H'][b:b+32],device='cuda');a=torch.tensor(batch['A'][b:b+32].reshape(-1,40),device='cuda');f=torch.tensor(batch['F'][b:b+32],device='cuda').repeat_interleave(2);ctx=h.repeat_interleave(2,0);states=[ctx[:,-1]]
       for tick in range(batch['T'].shape[2]):
        pred=call(ctx,a,f);states.append(pred);ctx=torch.cat([ctx[:,1:],pred[:,None]],1)
        if (tick+1)%4==0:ctx=ctx.detach()
       states=torch.stack(states,1).to(torch.float64)*sigma;energy=.5*states.square().mean(-1);cost=energy[:,window].mean(1).reshape(-1,2);effects.append((cost[:,0]-cost[:,1]).cpu().numpy())
      predicted=np.concatenate(effects).reshape(truth.shape)
      saved_key='initial' if item.get('initial') else 'selected' if item.get('sha256')==close['models']['selected_checkpoint_sha256'] else None
      if saved_key:
       saved=np.asarray(close['A1b']['models'][saved_key]['predicted_action_minus_twin']);delta=float(np.max(np.abs(predicted-saved)));assert np.array_equal(predicted,saved),f'D1 {saved_key} reproduction mismatch: {delta}'
       result['reproduction'].append(dict(dataset=ds,model=item['name'],maximum_absolute_difference=delta,exact=True));predicted=saved
     else:
      costs=np.zeros((len(val['H']),len(patterns)))
      for b in range(0,len(val['H'])*len(patterns),128):
       flat=np.arange(b,min(b+128,len(val['H'])*len(patterns)));draw,action=flat//len(patterns),flat%len(patterns)
       ctx=torch.tensor(val['H'][draw],device='cuda',dtype=torch.float32);a=torch.tensor(selection['validation_amplitude']*patterns[action]/sigma,device='cuda',dtype=torch.float32);f=torch.tensor(val['F'][draw],device='cuda',dtype=torch.float32)
       for tick in range(max(window)+1):
        state=ctx[:,-1].to(torch.float64)*sigma
        if tick in window:costs[draw,action]+=(.5*state.square().mean(-1)/len(window)).cpu().numpy()
        if tick<max(window):ctx=torch.cat([ctx[:,1:],call(ctx,a,f)[:,None]],1)
      predicted=costs[:,:8]-costs[:,8,None]
    assert np.isfinite(predicted).all()
    all8=metrics(predicted,truth)
    if ds=='D2' and 'validation_effect_RMSE' in item:
     expected=item['validation_effect_RMSE'];actual=all8['effect_RMSE'];assert actual==expected,f'D2 reproduction mismatch {item["name"]}: {actual} versus {expected}'
     result['reproduction'].append(dict(dataset=ds,model=item['name'],stored_RMSE=expected,recomputed_RMSE=actual,maximum_absolute_difference=abs(actual-expected),exact=True))
    entry=dict(label='POST HOC, descriptive',in_sample=ds=='D1' and item['name'] not in ['initial','CNN-noF','CNN-F (true forcing supplied)'],data_usage='training batch' if ds=='D1' else 'validation set used for checkpoint/weight selection by response models',per_pattern={str(k):metrics(predicted[:,k],truth[:,k]) for k in range(truth.shape[1])},pooled={'pattern_0':metrics(predicted[:,0],truth[:,0]),'seven_zero_mean':metrics(predicted[:,1:],truth[:,1:]),'all_eight':all8})
    result['datasets'].setdefault(ds,{})[item['name']]=entry
    write(OUT/'progress.json',result);print(ds,item['name'],all8['effect_RMSE'],flush=True)
   del model;torch.cuda.empty_cache()
 result['provenance_hashes']={str(p):sha(p) for p in [ROOT/'receipts/acd_stage23_closeout.json',ROOT/'receipts/acd_stage23.json',ROOT/'ACD_STAGE23_FREEZE_G.md',c.FROZEN/'acd_stage9_train.py']}
 write(ROOT/'receipts/acd_stage23_pattern_breakdown.json',result);write(OUT/'complete.json',dict(receipt_sha256=sha(ROOT/'receipts/acd_stage23_pattern_breakdown.json')))
if __name__=='__main__':
 try:main()
 except BaseException:
  (OUT/'FAILED.log').write_text(traceback.format_exc());raise
