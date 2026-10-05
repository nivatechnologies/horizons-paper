"""Independent ACD definitions and the sole observation loader."""
import os
os.environ['JAX_PLATFORMS']='cpu'
os.environ['JAX_ENABLE_X64']='true'
import sys,json,time,hashlib,inspect
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent
INHERITED=Path(os.environ.get('ACD_INHERITED_ROOT', '/home/todd/work/aspen-forecast-decision-20261005/aspen/forecast_decision'))
sys.path.insert(0,str(INHERITED))
import protocol,physics
LT,SIGMA,LEADS,OUT,TICKS,WINDOWS=protocol.LT,protocol.SIGMA,protocol.LEADS,protocol.OUT,protocol.TICKS,protocol.WINDOWS
NAMES=['acd-observation-conf','acd-posterior-dev','acd-posterior-conf',
       'acd-sampler-dev','acd-sampler-conf','acd-crude-dev','acd-crude-conf',
       'acd-climatology','acd-measure-dev','acd-measure-conf','acd-dtcheck',
       'acd-bootstrap','acd-twoscale']
ACD_IDS={name:1200000+i for i,name in enumerate(NAMES)}
assert not set(ACD_IDS.values()) & (set(protocol.IDS.values()) | protocol.AAH_IDS)
protocol.IDS.update(ACD_IDS)
PATTERNS=np.vstack([protocol.patterns(),np.zeros(40)])
NOISE=.02*SIGMA
SUB_ROLES=dict(history={'initial':0,'noise':1},rml=0,crude=0,
               posterior={'primary':0,'diag':1,'stage1a':2,'refit':[10,11,12,13,14],'refit_rerun':[20,21,22,23,24]},
               measure={'noise':0,'random_sites':1},dtcheck={'rml':2,'crude':3,'posterior':4,'implementation':5,'diag':6},
               null=0,bootstrap={'R0_answer':0,'R1':1,'R1m':2,'R2c':3,'R3':4,'R3b':5,'R6':6,'coverage':7})
def digest(path):return protocol.digest(path)
def save_json(path,data):return protocol.write_json(path,data)
def settings():
    p=ROOT/'runs/numerics/acd_dt.json'
    return json.loads(p.read_text()) if p.exists() else dict(dt=.01,warmup=1000,draws=1000,r5_population=100,cuts=[])
def dt():return settings()['dt']
def resolution(rule,trigger,detail):
    p=ROOT/'runs/resolutions.jsonl';p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('a') as f:f.write(json.dumps(dict(rule=rule,trigger=trigger,detail=detail,time=time.time()))+'\n')
def rng(name,sub=0,case=0,member=0,action=0):return protocol.rng(name,sub,case,member,action)
def input_path(panel,c):
    if panel=='dev':return INHERITED/f'runs/test/input_{c:03d}.npz'
    if panel=='dtcheck':return ROOT/f'runs/dtcheck/input_{c:03d}.npz'
    raise RuntimeError('H2: confirmation unavailable in this authorization')
def load_observed(panel,c):
    path=input_path(panel,c)
    # The inherited archive has truth arrays; only this array is extracted.
    with np.load(path,allow_pickle=False) as archive:observed=archive['observed'].copy()
    log=ROOT/'runs/acd_access.jsonl';log.parent.mkdir(parents=True,exist_ok=True)
    record=dict(panel=panel,case=c,path=str(path),array='observed',caller=inspect.stack()[1].filename,time=time.time(),sha256=digest(path))
    with log.open('a') as f:f.write(json.dumps(record)+'\n')
    return observed
def assert_leaves():
    leaves=[]
    def add(name,sub,c,m=0,a=0):leaves.append((ACD_IDS[name],0,sub,c,m,a))
    for panel in ['dev','conf']:
        for c in range(200):
            if panel=='conf':
                for sub in [0,1]:add('acd-observation-conf',sub,c)
            for m in range(128):
                add('acd-sampler-'+panel,0,c,m);add('acd-crude-'+panel,0,c,m)
            for chain in range(4):
                for sub in [0,1,2]:add('acd-posterior-'+panel,sub,c,chain)
                for a in [3,5]:
                    for arm in range(5):
                        for sub in [10+arm,20+arm]:add('acd-posterior-'+panel,sub,c,chain,a)
            for a in [3,5]:
                for sub in [0,1]:add('acd-measure-'+panel,sub,c,0,a)
    for c in range(8):
        for sub in [0,1]:add('acd-dtcheck',sub,c)
        for m in range(128):
            for sub in [2,3]:add('acd-dtcheck',sub,c,m)
        for chain in range(4):
            for sub in [4,5,6]:add('acd-dtcheck',sub,c,chain)
    for c in range(4096):add('acd-climatology',0,c)
    for sub in range(8):add('acd-bootstrap',sub,0)
    assert len(leaves)==len(set(leaves))
    return dict(count=len(leaves),ids=ACD_IDS,sub_roles=SUB_ROLES)
