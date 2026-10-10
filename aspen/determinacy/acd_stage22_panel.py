"""Panel-path/namespace launcher for the count-parameterized frozen blind sampler."""
import argparse,hashlib,json,os,sys,types
from pathlib import Path
import acd_stage22_adapter as adapter
HERE=Path(__file__).resolve().parent
OUT=HERE/'runs/stage22'
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def configure():
    record=json.loads((HERE/'receipts/acd_stage22_freeze_f.json').read_text())
    adapter.install(record['N'])
    import acd_protocol
    acd_protocol.ROOT=HERE  # Panel-path adapter; source bytes remain frozen.
    import acd_stage21_contract as contract
    contract.OUT=OUT
    contract.NAMES=['acd-stage22-'+s for s in ['assign','instances','observation','sampler']]
    contract.IDS=record['namespaces']
    import acd_stage21_part1 as blind
    blind.OUT=OUT;blind.RECEIPT=HERE/'receipts/acd_stage22_part1.json'
    blind.NAMES=[contract.NAMES[2],contract.NAMES[3]]
    blind.IDS=contract.IDS
    def rng(name,sub=0,case=0,member=0,action=0):
        name={'acd-sampler-r3':contract.NAMES[3], 'acd-posterior-r3':contract.NAMES[3],
              'acd-stage21-sampler':contract.NAMES[3],
              'acd-stage21-observation':contract.NAMES[2]}.get(name,name)
        return contract.rng(name,sub,case,member,action)
    blind.rng=rng
    blind.__file__=str(Path(__file__).resolve())  # Only subprocess launcher path changes.
    def verify():
        marker=json.loads((OUT/'panel_contract_pushed.json').read_text())
        d=json.loads((HERE/'receipts/acd_stage22_panel_contract.json').read_text())
        assert marker['commit']
        assert digest(HERE/'ACD_STAGE22_PANEL_CONTRACT.md')==d['document_sha256']
        assert digest(HERE/'ACD_STAGE22_FREEZE_F.md')==d['freeze_f_sha256']
        for name,h in d['adapter_code_hashes'].items():assert digest(HERE/name)==h,name
        for name,h in d['frozen_code_hashes'].items():assert digest(adapter.BASE/name)==h,name
        import jax,numpyro
        assert jax.__version__=='0.11.2' and numpyro.__version__=='0.22.0'
        assert jax.config.x64_enabled and all(x.platform=='cpu' for x in jax.devices())
    contract.verify_contract=verify
    # Existing run() calls publication at its original timing and completion points.
    publication=types.ModuleType('acd_stage21_publish')
    def publish(step):
        import subprocess,time
        command=['ssh','-o','BatchMode=yes','-o','ConnectTimeout=10','baccus',
                 '/mnt/niva-array/work/aspen-stage19-env-20261007/bin/python',
                 '/mnt/niva-array/work/aspen-deadline-20261008/acd_stage22_panel_publish.py',step]
        while True:
            result=subprocess.run(command)
            if result.returncode==0:return
            if result.returncode==42:raise RuntimeError('Stage22 publication assertion FAILED')
            time.sleep(60)
    publication.publish=publish
    sys.modules['acd_stage21_publish']=publication
    return record,contract,blind

def contract_document():
    record,contract,blind=configure()
    import jax,numpyro,platform,numpy as np
    assert jax.__version__=='0.11.2' and numpyro.__version__=='0.22.0'
    assert jax.config.x64_enabled
    assert len(contract.assignments())==record['N']
    assert np.sum(contract.assignments()==7)==record['N']//2
    assert np.sum(contract.assignments()==9)==record['N']//2
    assert json.loads((OUT/'freeze_f_pushed.json').read_text())['commit']
    hashes={name:digest(HERE/name) for name in ['acd_stage22_adapter.py','acd_stage22_panel.py']}
    hashes.update({x['path']:digest(HERE/x['path']) for x in record['parameterization']['modules']})
    data=dict(N=record['N'],namespaces=record['namespaces'],root_disjoint=record['root_disjoint'],
              leaves_unique=record['leaves_unique'],leaf_count=record['leaf_count'],
              forcing_by_case=contract.assignments().tolist(),
              environment=dict(host=platform.node(),jax=jax.__version__,numpyro=numpyro.__version__,float64=jax.config.x64_enabled,platforms=[x.platform for x in jax.devices()]),
              frozen_code_hashes=record['freeze_e_hashes'],adapter_code_hashes=hashes,
              freeze_f_sha256=digest(HERE/'ACD_STAGE22_FREEZE_F.md'),
              gate='first five cases; original Stage21 worker layout and wall-time cap',
              realized_outcome_accesses=[],criteria_changes=[])
    doc='''# Stage22 blind panel contract

Freeze F and its passed full-receipt reproduction gate precede generation. No realized outcome is computed or opened in blind sampling. Excluded instances are withheld and not replaced. No interim confirmatory scoring is permitted.

The unchanged Stage21 sampler is called through the count-parameterized copy. The launcher changes panel paths and dispatches the new Stage22 seed namespaces; all priors, NUTS settings, initialization, diagnostic gates, thinning, full-draw functional rescoring and single warm-up retry remain frozen. The new assignment is the same balanced permutation with its assigned count supplied by Freeze F. Spin-up, observation frames, absolute noise, reference LT, nine-option amplitude and frozen windows remain unchanged.

Run on sulaco CPU in float64 with the exact frozen JAX and NumPyro versions. The first-five timing gate uses the same worker layout and wall-time cap as Stage21. Every case writes observations, draws, forecasts, gate outcomes and hashes before downstream reading, and completed cases are skipped after hash verification. Frozen generation writes hidden history separately; the blind path never opens it. Sampling must stop if the timing projection fails. Scoring and inference wait for the entire fixed assigned panel and complete hashes.

Machine-readable execution values follow.

'''
    (HERE/'ACD_STAGE22_PANEL_CONTRACT.md').write_text(doc+'```json\n'+json.dumps(data,indent=2)+'\n```\n')
    data['document_sha256']=digest(HERE/'ACD_STAGE22_PANEL_CONTRACT.md')
    (HERE/'receipts/acd_stage22_panel_contract.json').write_text(json.dumps(data,indent=2)+'\n')
    print('Panel contract ready; generation has not started',flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['contract','case','run']);p.add_argument('index',type=int,nargs='?');args=p.parse_args()
    if args.mode=='contract':contract_document()
    else:
        record,contract,blind=configure()
        if args.mode=='case':print(json.dumps(blind.case(args.index)),flush=True)
        else:blind.run()
