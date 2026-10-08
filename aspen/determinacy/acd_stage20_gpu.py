"""Stage20 original-panel Spark diagnostics; no outcome files or fresh inputs."""
import argparse, hashlib, json, time
from pathlib import Path
import numpy as np
import torch
ROOT=Path(__file__).resolve().parent

def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,d):
    p=Path(p); t=p.with_suffix('.tmp.json');t.write_text(json.dumps(d,indent=2,allow_nan=False)+'\n');t.replace(p)
def setup():
    torch.set_num_threads(4);torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
    torch.backends.cudnn.deterministic=True;torch.backends.cudnn.benchmark=False

def manifest(out):
    p=out/'hashes.json'; hashes=json.loads(p.read_text()) if p.exists() else {}
    for name,h in hashes.items():
        if digest(out/name)!=h:raise RuntimeError('Output hash mismatch '+name)
    return hashes

def commit_npz(target,arrays,hashes):
    tmp=target.with_suffix('.tmp.npz');np.savez_compressed(tmp,**arrays);tmp.replace(target)
    hashes[target.name]=digest(target);write(target.parent/'hashes.json',hashes)

def readability(args):
    from acd_stage18_estimators import Estimator
    from acd_stage9_cnn import ForcingModel, Emulator
    setup();settings=json.loads((args.data/'settings.json').read_text());sigma=settings['sigma'];out=args.out;out.mkdir(parents=True,exist_ok=True)
    estimators=[]
    for p in sorted(args.estimators.glob('E0-seed*/selected.pt')):
        m=Estimator(False).cuda().eval();m.load_state_dict(torch.load(p,map_location='cpu',weights_only=True)['state_dict']);estimators.append(m)
    if len(estimators)!=5:raise RuntimeError('Requires all five frozen E0 estimators')
    model=None
    if args.name!='physics':
        model=(ForcingModel() if args.name.startswith('CNN-F') else Emulator()).cuda().eval()
        model.load_state_dict(torch.load(args.checkpoint,map_location='cpu',weights_only=True)['state_dict'])
    hashes=manifest(out)
    def rhs(x,f):return (torch.roll(x,-1,-1)-torch.roll(x,2,-1))*torch.roll(x,1,-1)-x+f[:,None]
    for case in range(200):
        target=out/f'{case:03d}.npz'
        if target.name in hashes:continue
        started=time.monotonic()
        with np.load(args.data/f'{case:03d}.npz') as d:H=d['H'].copy();F=d['F'].copy()
        estimates=np.empty((len(estimators),len(H),49));good=np.ones(len(H),bool)
        with torch.no_grad():
            for b in range(0,len(H),args.micro):
                ctx=torch.tensor(H[b:b+args.micro]/sigma,device='cuda',dtype=torch.float32)
                f=torch.tensor((F[b:b+args.micro]-8)/2,device='cuda',dtype=torch.float32);action=torch.zeros((len(ctx),40),device='cuda')
                x=torch.tensor(H[b:b+args.micro,-1],device='cuda',dtype=torch.float64)
                physical_context=torch.tensor(H[b:b+args.micro],device='cuda',dtype=torch.float64)
                physical_f=torch.tensor(F[b:b+args.micro],device='cuda',dtype=torch.float64)
                for s in range(49):
                    for j,e in enumerate(estimators): estimates[j,b:b+len(ctx),s]=e(ctx).cpu().numpy().astype(float)*2+8
                    state=(physical_context[:,-1] if model is None else ctx[:,-1].double()*sigma)
                    good[b:b+len(ctx)] &= (torch.isfinite(state).all(-1)&(state.square().mean(-1).sqrt()<=10*sigma)).cpu().numpy()
                    if s==48:continue
                    if model is None:
                        for _ in range(5):
                            k1=rhs(x,physical_f);k2=rhs(x+.005*k1,physical_f);k3=rhs(x+.005*k2,physical_f);k4=rhs(x+.01*k3,physical_f)
                            x=x+.01/6*(k1+2*k2+2*k3+k4)
                        physical_context=torch.cat([physical_context[:,1:],x[:,None]],1);ctx=(physical_context/sigma).float()
                    else:
                        pred=model(ctx,action,f) if args.name.startswith('CNN-F') else model(ctx,action)
                        ctx=torch.cat([ctx[:,1:],pred[:,None]],1)
        commit_npz(target,dict(estimated_F=estimates,valid=good),hashes)
        print(args.name,case,len(H),time.monotonic()-started,flush=True)
    write(out/'complete.json',dict(model=args.name,host=__import__('socket').gethostname(),GPU=torch.cuda.get_device_name(),
          output_hashes=hashes,code_sha256=digest(__file__),checkpoint_sha256=digest(args.checkpoint) if model is not None else None,
          estimator_hashes={str(p.relative_to(args.estimators)):digest(p) for p in sorted(args.estimators.glob('E0-seed*/selected.pt'))},
          physics='float64 RK4 with frozen dt and output spacing, own forcing, no action; estimator network FP32'))

def pipeline(args):
    import acd_stage9_cnn as original
    from acd_stage18_estimators import Estimator
    setup();settings=json.loads((args.data/'settings.json').read_text());horizon=max(max(w) for w in settings['windows'])
    est=Estimator(False).cuda().eval();est.load_state_dict(torch.load(args.estimator,map_location='cpu',weights_only=True)['state_dict'])
    base=original.ForcingModel;instances=[];cutoff=[];probes=[];probe_steps=[0,12,24,36,48]
    class Pipeline(base):
        def __init__(self):super().__init__();self.calls=0;self.fixed=None;self.probes=None;instances.append(self)
        def forward(self,H,A,F):
            step=self.calls%horizon
            if step==0:
                self.fixed=est(H,A);cutoff.append(self.fixed.detach().cpu().numpy());self.probes=np.empty((len(H),len(probe_steps)))
            value=est(H,A) if args.rolling else self.fixed
            if step in probe_steps:self.probes[:,probe_steps.index(step)]=value.detach().cpu().numpy().astype(float)*2+8
            if step==max(probe_steps):probes.append(self.probes.copy())
            self.calls+=1
            return super().forward(H,A,value)
    out=args.out;out.mkdir(parents=True,exist_ok=True);hashes=manifest(out);oldsave=original.np.savez_compressed;empty=torch.cuda.empty_cache
    # Stage9 skips only outputs verified by this Stage20 manifest.
    for p in out.glob('[0-9][0-9][0-9].npz'):
        if p.name not in hashes:raise RuntimeError('Unhashed prior output '+str(p))
    def saved(p,**arrays):
        arrays['estimated_F_at_cutoff']=np.concatenate(cutoff).astype(float)*2+8
        arrays['forcing_probes']=np.concatenate(probes);arrays['probe_steps']=np.asarray(probe_steps)
        cutoff.clear();probes.clear();p=Path(p);tmp=p.with_suffix('.tmp.npz');oldsave(tmp,**arrays);tmp.replace(p)
        hashes[p.name]=digest(p);write(out/'hashes.json',hashes)
    def reset():
        for instance in instances:instance.calls=0;instance.fixed=None;instance.probes=None
        cutoff.clear();probes.clear();empty()
    original.ForcingModel=Pipeline;original.np.savez_compressed=saved;torch.cuda.empty_cache=reset
    try:original.run(args.name,args.checkpoint,args.data,out,args.micro)
    finally:original.ForcingModel=base;original.np.savez_compressed=oldsave;torch.cuda.empty_cache=empty
    d=json.loads((out/'complete.json').read_text());d.update(host=__import__('socket').gethostname(),output_hashes=hashes,
        estimator_sha256=digest(args.estimator),adapter_sha256=digest(__file__),rolling=args.rolling)
    write(out/'complete.json',d)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('part',choices=['B','C']);p.add_argument('--name',required=True);p.add_argument('--data',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--checkpoint',type=Path);p.add_argument('--estimators',type=Path);p.add_argument('--estimator',type=Path);p.add_argument('--rolling',action='store_true');p.add_argument('--micro',type=int,default=1024);a=p.parse_args();readability(a) if a.part=='B' else pipeline(a)
