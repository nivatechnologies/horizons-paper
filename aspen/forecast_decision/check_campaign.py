"""Independent Stage-1 reading checker. Run only by authorized coordinator."""
import argparse,json
from pathlib import Path
import numpy as np
from protocol import rng
from metrics import aggregate,read_gates


def reject_nonfinite(value,path='$'):
    if isinstance(value,dict):
        for k,v in value.items():reject_nonfinite(v,path+'.'+k)
    elif isinstance(value,list):
        for i,v in enumerate(value):reject_nonfinite(v,path+'['+str(i)+']')
    elif isinstance(value,float) and not np.isfinite(value):raise ValueError('nonfinite number at '+path)


def equivalent(actual,expected,path='$'):
    if isinstance(expected,dict):
        for k,v in expected.items():
            if k not in actual:raise ValueError('missing '+path+'.'+k)
            equivalent(actual[k],v,path+'.'+k)
    elif isinstance(expected,(int,float)) and not isinstance(expected,bool):
        if actual is None or not np.isfinite(actual) or not np.isclose(actual,expected,rtol=1e-10,atol=1e-12):raise ValueError('mismatch '+path)
    elif actual!=expected:raise ValueError('mismatch '+path+': '+repr(actual)+' != '+repr(expected))


def verify(cases,reading,raw_root=None):
    reject_nonfinite(cases);reject_nonfinite(reading)
    rows=cases['cases'];assert len(rows)==200
    assert [r['case'] for r in rows]==list(range(200))
    assert reading['stage']=='1' and reading['S']==['CNN-20k'] and reading['licensed_sentences']==[]
    for j,r in enumerate(reading['leads']):
        entries=[v['leads'][j] for v in rows];assert all(e['T']==r['T'] for e in entries)
        for e in entries:
            for name,a in e['arms'].items():
                assert len(a['J'])==8 and len(a['cost'])==8 and 0<=a['dropped']<=64
                equivalent(a['failed'],a['dropped']>32)
                equivalent(a['correct'],not a['failed'] and a['chosen']==e['b'])
                if a['failed']:
                    equivalent(a['chosen'],-1);equivalent(a['wACC'],0.)
                    equivalent(a['regret_raw'],float(np.ptp(a['J'])))
                else:
                    equivalent(a['chosen'],int(np.argmin(a['cost'])))
                    equivalent(a['regret_raw'],float(a['J'][a['chosen']]-min(a['J'])))
        if raw_root is not None:
            for row,e in zip(rows,entries):
                with np.load(Path(raw_root)/('cpu_%03d.npz'%row['case'])) as raw:truth=raw['truth_cost'][:8,:,e['h']]
                assert truth.shape==(8,2048) and np.isfinite(truth).all()
                b=int(truth[:,:1024].mean(1).argmin());d=truth[:,1024:]-truth[b,1024:]
                low=d.mean(1)-2.983*d.std(1,ddof=1)/np.sqrt(1024)
                equivalent(e['b'],b);equivalent(e['eligible'],bool(np.all(np.delete(low,b)>0)))
                assert np.allclose(low,e['confirmation_bounds'],rtol=1e-10,atol=1e-12)
                for a in e['arms'].values():
                    assert np.allclose(a['J'],truth.mean(1),rtol=1e-10,atol=1e-12)
        samples=rng('afd-bootstrap',3,member=j+100).integers(200,size=(2000,200))
        gate=read_gates(entries,['CNN-20k'],[],samples)
        eq=dict(eligible=gate['eligible'],total=200,eligible_fraction=gate['eligible']/200,sufficiency=gate['sufficiency'],null_gap=gate['null_gap'],
                H1a=gate['H1a'] or 'otherwise',
                eligibility_bootstrap_agreement=sum(e['eligible']==e['bootstrap_eligible'] for e in entries),
                eligible_full_argmin_disagreements=sum(e['eligible'] and e['b']!=e['full_best'] for e in entries),
                myopic_P=float(np.mean([e['myopic_correct'] for e in entries if e['eligible']])) if gate['eligible'] else None,
                fixed_P=float(np.mean([e['fixed_correct'] for e in entries if e['eligible']])) if gate['eligible'] else None)
        bounds=gate.get('H1a_bounds',{}).get('CNN-20k')
        # The original coordinator stores bounds even when sufficiency fails.
        if bounds is None:
            from metrics import paired_gap,bounds as bound
            bounds=bound(paired_gap(entries,'N-last','CNN-20k',samples))
        eq.update(lower95=bounds['lower'],upper95=bounds['upper'])
        equivalent(r,eq)
        expected_gap=gate['metrics']['N-last']['eligible']['P']-gate['metrics']['CNN-20k']['eligible']['P'] if gate['eligible'] else None
        equivalent(r.get('gap'),expected_gap)
        nacc=gate['metrics']['N-last']['eligible']['wACC'];cacc=gate['metrics']['CNN-20k']['eligible']['wACC']
        equivalent(r.get('comparable'),nacc is not None and cacc is not None and cacc>=nacc-.01)
        for name in ['N-last','N-oracle','CNN-20k']:
            m=gate['metrics'][name]
            equivalent(r['arms'][name],dict(P=m['eligible']['P'],wACC=m['eligible']['wACC'],wRMSE=m['eligible']['wRMSE'],
                failed_cases=m['failed_cases'],dropped_members=m['dropped_members'],attempted_members=m['attempted_members'],reliable=m['reliable']))
    primary=next(r for r in reading['leads'] if r['T']==2)
    equivalent(reading['primary'],primary)
    return dict(status='PASS',case_count=len(rows),leads=len(reading['leads']),raw_truth_checked=raw_root is not None)


def main():
    p=argparse.ArgumentParser();p.add_argument('--cases',type=Path,required=True);p.add_argument('--reading',type=Path,required=True);p.add_argument('--raw-root',type=Path);p.add_argument('--output',type=Path);a=p.parse_args()
    result=verify(json.loads(a.cases.read_text()),json.loads(a.reading.read_text()),a.raw_root)
    if a.output:a.output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(result))
if __name__=='__main__':main()
