"""Verify frozen execution, blind order, archives and confirmation readings."""
import os
os.environ['JAX_PLATFORMS']='cpu'
os.environ['JAX_ENABLE_X64']='true'
import json,ast
import numpy as np
from acd_protocol import *
from acd_confirmation import verify_freeze

def run():
    verify_freeze();errors=[];manifest=[]
    expected=['observations_written_and_hashed','posterior_written_and_hashed',
              'crude_written_and_hashed','cnn_written_and_hashed','realized_outcomes_after_all_sampler_hashes']
    for c in range(200):
        p=ROOT/f'runs/conf/order_{c:03d}.jsonl';rows=[json.loads(l) for l in p.read_text().splitlines()]
        if [r['kind'] for r in rows]!=expected:errors.append(f'{c}: blind order')
        if any(rows[i]['time']>rows[i+1]['time'] for i in range(4)):errors.append(f'{c}: order timestamps')
        for row in rows:
            for f in row['files']:
                if digest(ROOT/f['path'])!=f['sha256']:errors.append(f"{c}: altered {f['path']}")
        with np.load(input_path('conf',c)) as d:
            if d.files!=['observed']:errors.append(f'{c}: truth-bearing observation archive')
        with np.load(ROOT/f'runs/conf/case_{c:03d}.npz') as d:
            if any(k in d for k in ['true','actual','actual_cost']):errors.append(f'{c}: inference truth')
            if d['J'].shape[1:]!=(9,8) or not np.isfinite(d['J']).all():errors.append(f'{c}: costs')
            if d['theta'].shape[1:]!=(41,):errors.append(f'{c}: parameter shape')
        row=json.loads((ROOT/f'runs/conf/case_{c:03d}.json').read_text())
        if row['diagnostics']['sampler']['draws']!=500 or row['diagnostics']['sampler']['warmup'] not in [1000,2000]:errors.append(f'{c}: changed production settings')
        cnn=json.loads((ROOT/f'runs/conf/cnn_{c:03d}.json').read_text())
        if cnn['status']=='COMPLETE':
            if cnn['checkpoint_sha256']!=json.loads((ROOT/'receipts/acd_freeze.json').read_text())['checkpoint']:errors.append(f'{c}: checkpoint')
            with np.load(ROOT/f'runs/conf/cnn_{c:03d}.npz') as d:
                if d['J_2LT'].shape!=(cnn['members'],9) or d['valid'].shape!=(128,):errors.append(f'{c}: CNN shape')
    for line in (ROOT/'runs/acd_access.jsonl').read_text().splitlines():
        row=json.loads(line)
        if row['array']!='observed':errors.append('H1: access log truth read')
    pop=json.loads((ROOT/'runs/conf/measure_population.json').read_text())['population']
    from acd_confirmation import population
    if pop!=population():errors.append('R5 population changed')
    for row in pop:
        for arm in range(4):
            p=ROOT/f"runs/conf/measure/refit_{row['case']:03d}_3_{arm}.npz"
            receipt=json.loads(p.with_suffix('.json').read_text())
            if digest(p)!=receipt['sha256']:errors.append('Changed R5 refit')
    if digest(ROOT/'CODEX_SELECTOR.md')!='4bbd87f7a578d1222e6af82079db3b44d2cf3567eddc0872b28d3c08d3c05070':errors.append('Step0b changed')
    import jax
    if any(d.platform!='cpu' for d in jax.devices()) or not jax.config.jax_enable_x64:errors.append('JAX device/precision')
    for p in sorted((ROOT/'runs').rglob('*')):
        if p.is_file() and p.suffix in ['.npz','.json','.jsonl']:
            manifest.append(dict(path=str(p.relative_to(ROOT)),bytes=p.stat().st_size,sha256=digest(p)))
    result=dict(passed=not errors,errors=errors,host=os.uname().nodename,blind_order_cases=200,
                settings=settings(),seed_leaves=assert_leaves(),manifest=manifest)
    save_json(ROOT/'ACD_STAGE2_ARTIFACTS.json',result)
    print('Stage2 check', 'PASS' if not errors else errors,flush=True)
    if errors:raise RuntimeError('Stage2 verification failed')

if __name__=='__main__':run()
