"""CPU coordinator case rows for reported secondary and approved two-scale panels."""
import datetime
import numpy as np
from protocol import write_json,digest,IDS,AAH_IDS
from score_stage1 import normal_eligible,bootstrap_eligible


def derive(root,panel,fixed_action,two_scale=False):
    if fixed_action not in range(8):raise ValueError('already-selected validation fixed action required')
    count=200 if two_scale else 100;physics='N2' if two_scale else 'N-last';leads=[0.,1.,1.5,2.] if two_scale else [0.,1.,1.5,2.,2.5,3.,4.,6.]
    if two_scale:
        approval=root/'runs/twoscale/sampler_go.json'
        go=__import__('json').loads(approval.read_text());assert go.get('approved') is True and go.get('approved_by')=='Todd'
        assert go['sampler_check_sha256']==digest(root/'runs/twoscale/sampler_check.json')
    case_offset=0 if two_scale else 200
    if not two_scale:
        def key(case,member):return (IDS['afd-bootstrap'],0,3,case,member,0)
        primary={key(c,h) for c in range(200) for h in range(8)}|{key(0,j+100) for j in range(7)}
        secondary={key(c+200,h) for c in range(100) for h in range(8)}|{key(200,j+100) for j in range(7)}
        assert not primary&secondary and all(k[0] not in AAH_IDS for k in primary|secondary)
        mapping=dict(recorded_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),namespace='afd-bootstrap',system_tag=0,substream=3,member_confirmation_case='c+200',case_interval_case=200,primary_draws_unchanged=True,instantiation='Recorded now before secondary bootstrap, from frozen panel counts and unique-root rule; the pre-data protocol reserved case keys 0..299 but did not explicitly assign panels',leaf_sets_disjoint=True,AAH_prefixes_disjoint=True)
        path=root/'runs/secondary_bootstrap_map.json';write_json(path,mapping)
        with (root/'AFD_ARTIFACTS.md').open('a') as f:f.write('\n- Secondary bootstrap mapping, before its execution: '+str(path.relative_to(root))+' SHA256 '+digest(path)+'; '+mapping['recorded_at']+'; deterministic c+200 / case-CI200 instantiation, no historical freeze edit.\n')
    rows=[]
    for c in range(count):
        with np.load(root/f'runs/{panel}/cpu_{c:03d}.npz') as d:
            myopic=int(d[physics+'_cost'][:,:,0].mean(1).argmin());entries=[]
            for h,T in enumerate(leads):
                if h==0:continue
                truth=d['truth_cost'][:8,:,h];b,eligible,low=normal_eligible(truth)
                boot,bootlow=bootstrap_eligible(truth,b,'afd2-bootstrap' if two_scale else 'afd-bootstrap',c+case_offset,h)
                full=truth.mean(1);cost=d[physics+'_cost'][:,:,h].mean(1);chosen=int(cost.argmin())
                entries.append(dict(T=T,h=h,b=b,eligible=eligible,confirmation_bounds=low.tolist(),bootstrap_eligible=boot,bootstrap_bounds=bootlow.tolist(),full_best=int(full.argmin()),myopic_correct=myopic==b,fixed_correct=fixed_action==b,
                    arms={physics:dict(chosen=chosen,correct=chosen==b,failed=False,dropped=0,cost=cost.tolist(),J=full.tolist(),J0=float(d['truth_cost'][8,:,h].mean()),regret_raw=float(full[chosen]-full.min()))}))
        rows.append(dict(case=c,leads=entries));print('derived',panel,c+1,flush=True)
    return dict(cases=rows,role='statistics coordinator only',panel=panel,already_selected_fixed_action=fixed_action,derived_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
