"""Read-only verification of completed Stage 1 and observational boundaries."""
import os
os.environ['JAX_PLATFORMS']='cpu'
os.environ['JAX_ENABLE_X64']='true'
import ast,json
import numpy as np
from acd_protocol import *
def run():
    errors=[];manifest=[]
    if digest(ROOT/'CODEX_SELECTOR.md')!='4bbd87f7a578d1222e6af82079db3b44d2cf3567eddc0872b28d3c08d3c05070':errors.append('Step0b selector changed')
    for name in ['acd_posterior.py','acd_fits.py','acd_mechanism.py']:
        tree=ast.parse((ROOT/name).read_text())
        for node in ast.walk(tree):
            if isinstance(node,ast.Subscript) and isinstance(node.slice,ast.Constant) and isinstance(node.slice.value,str) and (node.slice.value in ['true','actual','actual_cost'] or node.slice.value.startswith('truth_')):errors.append(f'{name}: truth subscript')
    for panel in ['dev','dtcheck']:
        for c in range(200 if panel=='dev' else 8):
            p=ROOT/f'runs/{panel}/case_{c:03d}.npz'
            if panel=='dtcheck' and not p.exists():continue # permitted removal after R-dt
            if not p.exists():errors.append(f'missing {panel} {c}');continue
            report=json.loads(p.with_suffix('.json').read_text())
            with np.load(p) as d:
                if any(k in d for k in ['true','actual','actual_cost']):errors.append(f'{p}: scoring array in sampler archive')
                if not np.isfinite(d['theta']).all() or not np.isfinite(d['J']).all():errors.append(f'{p}: nonfinite draws/costs')
                if d['J'].shape[1:]!=(9,8):errors.append(f'{p}: cost shape')
            if report['dt']!=dt():errors.append(f'{p}: wrong dt')
            if report['sha256']!=digest(p):errors.append(f'{p}: changed after receipt')
    if (ROOT/'runs/conf').exists() or (ROOT/'ACD_FREEZE.md').exists():errors.append('H2: confirmation/freeze present')
    for line in (ROOT/'runs/acd_access.jsonl').read_text().splitlines():
        row=json.loads(line)
        if row['array']!='observed' or row['panel']=='conf':errors.append('access log violation')
    for p in sorted((ROOT/'runs').rglob('*')):
        if p.is_file() and p.suffix in ['.npz','.json','.jsonl']:manifest.append(dict(path=str(p.relative_to(ROOT)),bytes=p.stat().st_size,sha256=digest(p)))
    inherited={name:digest(INHERITED/name) for name in ['protocol.py','physics.py','extras.py','campaign.py']}
    expected={'protocol.py':'e6d002264a8000ac88d15db41b76cd69bf17c5472de04b29f51b56408841412d','physics.py':'13ef98834e47bd667f53cce50af3e7d573a1bc4eb9c38987f389a05b1f2fc5d7'}
    if any(inherited[k]!=v for k,v in expected.items()):errors.append('inherited source changed')
    import jax,numpyro
    if any(d.platform!='cpu' for d in jax.devices()) or not jax.config.jax_enable_x64:errors.append('JAX platform or precision')
    report=dict(jax_devices=[str(d) for d in jax.devices()],jax_x64=bool(jax.config.jax_enable_x64),jax_version=jax.__version__,numpyro_version=numpyro.__version__,passed=not errors,errors=errors,host=os.uname().nodename,jax_platform='cpu',seed_leaves=assert_leaves(),inherited=inherited,manifest=manifest)
    save_json(ROOT/'ACD_ARTIFACTS.json',report);print('check_acd', 'PASS' if not errors else errors,flush=True)
    if errors:raise RuntimeError('Artifact verification requires repair')
if __name__=='__main__':run()
