"""Frozen definitions. Standalone Aspen code; no platform imports."""
from pathlib import Path
import hashlib, json, os
import numpy as np

ROOT=Path(__file__).resolve().parent
LT=0.5928295944308761
SIGMA=4.312600593723798
LEADS=np.array([0.,1.,1.5,2.,2.5,3.,4.,6.])
OUT=.05
TICKS=np.arange(int(np.ceil(7*LT/OUT))+1)
WINDOWS=[np.flatnonzero((TICKS*OUT>=T*LT-1e-12)&(TICKS*OUT<=(T+1)*LT+1e-12)) for T in LEADS]
PRIMARY=3
AAH_IDS=set(range(100000,1000000,100000))
NAMES=["afd-test-truth","afd-test-arm","afd-val-truth","afd-val-arm",
       "afd-test2-truth","afd-test2-arm","afd-train-pairs","afd-train-cost",
       "afd-cnn-seed2","afd-cnn-seed3","afd-dtcheck","afd-bootstrap",
       "afd-observation-test","afd-observation-val","afd-observation-test2",
       "afd2-test-truth","afd2-test-arm","afd2-test-oracle","afd2-val-truth",
       "afd2-val-arm","afd2-train","afd2-train-cost","afd2-fastlib","afd2-twin",
       "afd2-dtcheck","afd2-bootstrap","afd2-observation-test","afd2-observation-val",
       "afd2-statecheck","afd-train-recipe","afd2-train-pairs","afd2-train-val",
       "afd2-climatology"]
IDS={name:1100000+i for i,name in enumerate(NAMES)}
assert len(set(IDS.values()))==len(IDS) and not set(IDS.values())&AAH_IDS
ORDER=["CNN-R2","CNN-roll","CNN-80k","CNN-20k","CNN-5k"]
ORDER2=["CNN2-R2","CNN2-roll","CNN2-20k"]
RECIPE={
"CNN-5k":dict(kind="base",updates=5000,cap_hours=1),
"CNN-80k":dict(kind="base",updates=80000,cap_hours=5),
"CNN-20k-s2":dict(kind="base",updates=20000,cap_hours=2),
"CNN-20k-s3":dict(kind="base",updates=20000,cap_hours=2),
"CNN-roll":dict(kind="roll",updates=10000,cap_hours=5),
"CNN-resp":dict(kind="resp",updates=10000,cap_hours=5),
"CNN-R2":dict(kind="r2",updates=100000000,cap_hours=10),
"CNN-cost":dict(kind="cost",updates=100000000,cap_hours=10),
"CNN2-20k":dict(kind="base",updates=20000,cap_hours=3),
"CNN2-roll":dict(kind="roll",updates=10000,cap_hours=2),
"CNN2-R2":dict(kind="r2",updates=100000000,cap_hours=7),
"CNN2-cost":dict(kind="cost",updates=100000000,cap_hours=8),
}
# 40 and 20 GPU-hour aggregate ceilings, counting checkpoint validation GPU use.
def rng(name,sub=0,case=0,member=0,action=0):
    return np.random.Generator(np.random.PCG64(np.random.SeedSequence(
        [IDS[name],0,sub,case,member,action])))
def digest(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):h.update(b)
    return h.hexdigest()
def write_json(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix(path.suffix+".tmp")
    tmp.write_text(json.dumps(data,indent=2,allow_nan=False)+"\n")
    os.replace(tmp,path)
def patterns():
    i=np.arange(40);theta=2*np.pi*i/40
    p=np.stack([-np.ones(40)]+[np.sqrt(2)*np.cos(k*theta) for k in [1,2,4,8,10]]+
               [(-1.)**i,(1-40*(i==0))/np.sqrt(39)])
    return p/np.sqrt(np.mean(p*p,axis=1))[:,None]
def assert_leaves():
    # All planned one/two-scale per-case roots, train starts and per-stream roles.
    leaves=[]
    for name in NAMES:
        count=16384 if "cost" in name else 4096 if "fastlib" in name or "pairs" in name else 2048 if "train" in name else 300
        for sub in range(7):
            leaves.extend((IDS[name],0,sub,c,0,0) for c in range(count))
    assert len(set(leaves))==len(leaves)
    assert all(x[0] not in AAH_IDS for x in leaves)
    return len(leaves)

