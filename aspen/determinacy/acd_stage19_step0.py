import os
os.environ.update(JAX_PLATFORMS='cpu',JAX_ENABLE_X64='true',NUMBA_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',ACD_INHERITED_ROOT='/mnt/niva-array/work/aspen-forecast-decision-20261005/aspen/forecast_decision')
import sys,json,hashlib,time,platform
from pathlib import Path
root=Path('/mnt/niva-array/work/aspen-determinacy-stage19-20261007/aspen/determinacy');sys.path.insert(0,str(root))
import numpy as np,jax,numpyro
from acd_protocol import physics
from acd_fits import objective
assert jax.__version__=='0.11.2' and numpyro.__version__=='0.22.0' and jax.config.x64_enabled
p=root/'runs/stage19/reference.npz'
with np.load(p) as z:
 t=z['theta'];y=z['y']; f=physics.simulate(t[None,:40],np.full((1,40),t[40]),.01,11)[0];v,g=objective(t,y,.01,np.zeros(40),np.zeros(40));j=physics.costs(physics.simulate(z['null_states'],np.full((16,40),8.),.01))
 err=lambda a,b:float(np.linalg.norm(a-b)/max(np.linalg.norm(b),np.finfo(float).tiny))
 checks={'forward_relative_difference':err(f,z['forward']),'gradient_relative_difference':err(g,z['gradient']),'misfit_absolute_difference':float(abs(v-z['value'])),'null_energy_max_absolute_difference':float(np.max(abs(j-z['null_energies'])))}
 meta=json.loads(str(z['metadata']))
freeze=json.loads((root/'receipts/acd_freeze_code.json').read_text());hashes={}
for base,names,key in [(root,['acd_protocol.py','acd_fits.py','acd_posterior.py','acd_mechanism.py'],'hashes'),(Path(os.environ['ACD_INHERITED_ROOT']),['protocol.py','physics.py'],'inherited')]:
 for n in names:
  h=hashlib.sha256((base/n).read_bytes()).hexdigest();hashes[n]={'sha256':h,'expected':freeze[key][n],'passed':h==freeze[key][n]}
passed=all(q['passed'] for q in hashes.values()) and checks['forward_relative_difference']<=1e-10 and checks['gradient_relative_difference']<=1e-10 and checks['null_energy_max_absolute_difference']<=1e-12
out={'passed':passed,'environment':{'host':platform.node(),'python':platform.python_version(),'jax':jax.__version__,'numpyro':numpyro.__version__,'numpy':np.__version__,'jax_x64':jax.config.x64_enabled,'devices':[str(d) for d in jax.devices()]},'checks':checks,'hashes':hashes,'reference_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'reference_sources':meta,'mcmc_cross_host_bitwise_identity_expected':False,'realized_outcome_accesses':[]}
(root/'receipts/acd_stage19_step0.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert passed
