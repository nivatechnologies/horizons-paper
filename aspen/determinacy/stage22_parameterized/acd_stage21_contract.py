"""Stage21 blind-generation contract and disjoint SeedSequence leaves."""
import os
os.environ.update(JAX_PLATFORMS='cpu',JAX_ENABLE_X64='true',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
import hashlib,json,re,platform
from pathlib import Path
import numpy as np
from acd_protocol import ROOT,physics,protocol,LT,WINDOWS,LEADS
NAMES=['acd-stage21-assign','acd-stage21-instances','acd-stage21-observation','acd-stage21-sampler','acd-stage21-climatology']
IDS={n:int.from_bytes(hashlib.sha256(n.encode()).digest()[:8],'little') for n in NAMES}
SIGMA=4.313
OUT=ROOT/'runs/stage21'
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rng(name,sub=0,case=0,member=0,action=0):
 return np.random.default_rng(np.random.SeedSequence([IDS[name],0,sub,case,member,action]))
def assignments():
 return rng(NAMES[0]).permutation(np.repeat([7.,9.],N//2))
def configure():
 # Adapter globals implement Todd's explicit Stage21 sigma without editing inherited files.
 import acd_fits,acd_posterior
 for m in [acd_fits,acd_posterior]:m.SIGMA=SIGMA;m.NOISE=.02*SIGMA
 protocol.IDS.update(IDS)
def generate_history(c):
 f=assignments()[c];x=f+rng(NAMES[1],case=c).standard_normal((1,40))
 x=physics.flow(x,np.full_like(x,f),int(round(50*LT/.01)),.01)
 true=physics.paths(x,np.full_like(x,f),.01,11)[0]
 observed=true+.02*SIGMA*rng(NAMES[2],sub=1,case=c).standard_normal(true.shape)
 return true,observed

def verify_contract():
 p=OUT/'contract_pushed.json'
 if not p.exists():raise RuntimeError('Stage21 contract must be pushed before generation')
 seal=json.loads(p.read_text());d=json.loads((ROOT/'receipts/acd_stage21_contract.json').read_text())
 if digest(ROOT/'ACD_STAGE21_PANEL_CONTRACT.md')!=seal['contract_sha256']:raise RuntimeError('Contract changed')
 for path,h in d['code_hashes'].items():
  if digest(path)!=h:raise RuntimeError('Contract source changed: '+path)
 import jax,numpyro
 assert jax.__version__=='0.11.2' and numpyro.__version__=='0.22.0'
 assert jax.config.x64_enabled and all(x.platform=='cpu' for x in jax.devices())

def write_contract():
 import jax,numpyro
 assert jax.__version__=='0.11.2' and numpyro.__version__=='0.22.0' and jax.config.x64_enabled
 prior=json.loads((ROOT/'receipts/acd_stage19_freeze_a.json').read_text())
 inherited={}
 for path,h in prior['code_hashes'].items():
  name=Path(path).name
  if name in ['protocol.py','physics.py']:p=Path(physics.__file__).with_name(name)
  elif name in ['acd_protocol.py','acd_fits.py','acd_posterior.py','acd_mechanism.py','acd_stage6_forward.py','acd_stage9_forward.py']:p=ROOT/name
  else:continue
  assert digest(p)==h,(name,'Inherited frozen hash mismatch')
  inherited[str(p)]=h
 oldnames=set()
 for p in ROOT.glob('acd*.py'):
  if not p.name.startswith('acd_stage21'):oldnames.update(re.findall(r'[\"\'](acd[-a-zA-Z0-9_/]+)[\"\']',p.read_text()))
 oldroots=set(protocol.AAH_IDS)|set(protocol.IDS.values())|{int.from_bytes(hashlib.sha256(n.encode()).digest()[:8],'little') for n in oldnames}
 assert not set(IDS.values())&oldroots and len(set(IDS.values()))==len(IDS)
 leaves=[(IDS[NAMES[0]],0,0,0,0,0)]
 for c in range(N):
  leaves.extend([(IDS[NAMES[1]],0,0,c,0,0),(IDS[NAMES[2]],0,1,c,0,0)])
  leaves.extend((IDS[NAMES[3]],0,0,c,m,0) for m in range(128))
  leaves.extend((IDS[NAMES[3]],0,s,c,m,0) for s in [1,2] for m in range(4))
 for level in [7,9]:leaves.extend((IDS[NAMES[4]],0,level,c,0,0) for c in range(4096))
 assert len(set(leaves))==len(leaves)
 code={str(ROOT/n):digest(ROOT/n) for n in ['acd_stage21_contract.py','acd_stage21_part1.py','acd_stage21_climatology.py','acd_stage21_publish.py']};code.update(inherited)
 d=dict(stage=21,environment=dict(host=platform.node(),jax=jax.__version__,numpyro=numpyro.__version__,float64=jax.config.x64_enabled,platforms=[x.platform for x in jax.devices()]),code_hashes=code,namespace_ids=IDS,seed_rule='SeedSequence [SHA256-first-eight-bytes-little-endian,0,sub,case,member,action]',leaf_count=len(leaves),earlier_names=sorted(oldnames),root_disjoint=True,leaves_unique=True,forcing_by_case=assignments().tolist(),sigma=SIGMA,noise_standard_deviation=.02*SIGMA,prior_state_sd=10*SIGMA,reference_LT=LT,windows=[w.tolist() for w in WINDOWS],leads=LEADS.tolist(),realized_outcome_accesses=[],resolutions=[dict(rule='R-other',detail='Use explicit Stage21 sigma for observation noise and prior; preserve inherited exact LT/windows rather than rounding the time axis.',inherited_sigma=protocol.SIGMA,stage21_sigma=SIGMA)])
 (ROOT/'receipts/acd_stage21_contract.json').write_text(json.dumps(d,indent=2)+'\n')
 text='''# Stage21 panel contract — blind sampling

No realized outcome is computed or opened. No emulator runs until Freeze E is pushed. This is a forcing-shift panel and licenses no frozen route.

The assignment permutation, initial-state and observation streams, sampler leaves and climatology leaves are distinct from every earlier source namespace. True forcing is used in generation only; inference receives observations alone. The initial state is F plus independent standard normal noise; spin-up lasts the inherited fifty reference LT in model time. The eleven frames and RK4 map are unchanged.

The joint posterior preserves the Stage19 main posterior implementation, initializer selection, priors on forcing, NUTS schedule, diagnostics, thinning, full-draw functional rescoring and single warm-up retry. The Stage21 adapter supplies its new RNG and the explicitly requested sigma. No valid-start fallback is allowed. Exclusion occurs only after the retry. Per-case files are resumable, hash-verified and skipped when complete.

The first five instances determine the cost projection, with original-panel retry and rescore allowances. At most eight workers each use four physical cores, leaving the remaining cores to existing work. Continue only within the prescribed wall-time cap. GPU work queues behind all named prior jobs. The reference LT and windows remain the frozen F=8 units; physical Lyapunov time varies with forcing, and no new Lyapunov estimate is inferred here.

Observation arrays, sample arrays, retained forecasts and gate outcomes will be committed as requested. Hidden histories are stored separately and are never opened by blind sampling or climatology. Every future realized-outcome access requires the pushed Freeze E and scoring code.

Machine-readable values and source hashes follow.

'''
 (ROOT/'ACD_STAGE21_PANEL_CONTRACT.md').write_text(text+'```json\n'+json.dumps(d,indent=2)+'\n```\n')
 OUT.mkdir(parents=True,exist_ok=True)
 print(json.dumps(dict(leaf_count=len(leaves),root_disjoint=True,environment=d['environment'])))
if __name__=='__main__':write_contract()
