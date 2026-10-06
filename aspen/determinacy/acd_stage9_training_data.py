"""Panel-disjoint new acd-train-F data. Sulaco CPU only; no panel files read."""
import os
os.environ.update(NUMBA_NUM_THREADS='24',OPENBLAS_NUM_THREADS='1',JAX_PLATFORMS='cpu')
import hashlib,json,numpy as np
from acd_protocol import ROOT,LT,SIGMA,PATTERNS,physics
OUT=ROOT/'runs/stage9_training/data'
def seed(role):return np.random.default_rng(np.random.SeedSequence([int.from_bytes(hashlib.sha256(b'acd-train-F').digest()[:8],'little'),role]))
def run():
 OUT.mkdir(parents=True,exist_ok=True)
 for role,name,n in [(0,'train',4096),(1,'val',512)]:
  p=OUT/f'{name}.npz'
  if p.exists():continue
  r=seed(role);F=r.uniform(6,10,n);x=F[:,None]+r.standard_normal((n,40))
  x=physics.flow(x,np.repeat(F[:,None],40,1),round(50*LT/.01),.01)
  H=physics.simulate(x,np.repeat(F[:,None],40,1),.01,11)
  pairs=np.array([(k,l) for k in range(8) for l in range(k+1,8)])
  ix=pairs[r.integers(28,size=n)];flip=r.integers(2,size=n).astype(bool);ix[flip]=ix[flip,::-1];amp=r.uniform(-.32,.32,size=n)
  A=amp[:,None,None]*PATTERNS[ix]
  T=np.empty((n,2,36,40),np.float32)
  for b in range(0,n,128):
   e=min(n,b+128);tr=physics.simulate(np.repeat(H[b:e,-1],2,0),(F[b:e,None,None]+A[b:e]).reshape(-1,40),.01,37)
   T[b:e]=tr[:,1:].reshape(e-b,2,36,40)/SIGMA
  np.savez_compressed(p,H=(H/SIGMA).astype(np.float32),F=((F-8)/2).astype(np.float32),A=(A/SIGMA).astype(np.float32),T=T)
  print(name,n,flush=True)
 (OUT/'manifest.json').write_text(json.dumps(dict(namespace='acd-train-F',namespace_id=int.from_bytes(hashlib.sha256(b'acd-train-F').digest()[:8],'little'),train=4096,val=512,trajectory_disjoint=True,noise_free=True,spinup_LT=50,dt=.01,sigma=SIGMA),indent=2)+'\n')
if __name__=='__main__':run()
