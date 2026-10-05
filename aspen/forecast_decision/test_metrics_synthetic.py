"""Constructed hypothesis inputs, not campaign measurements. No disk data reads."""
import copy
import numpy as np
from metrics import aggregate,read_gates,bounds,paired_gap,state_statistics,license_ids
from check_campaign import reject_nonfinite,equivalent


def entries():
    rows=[]
    for c in range(200):
        arms={}
        for name,correct,skill,rmse in [('N-last',True,.95,.30),('CNN-20k',c<148,.97,.25)]:
            chosen=0 if correct else 1
            arms[name]=dict(J=list(range(8)),J0=8.,chosen=chosen,correct=correct,failed=False,dropped=0,
                regret_raw=float(chosen),cost=list(range(8)) if correct else [1.,0.,2.,3.,4.,5.,6.,7.],
                wACC=skill,wRMSE=rmse,MSRE_num=1.,MSRE_den=4.,VRE_num=9.,VRE_den=16.)
        rows.append(dict(b=0,eligible=True,myopic_correct=c<160,fixed_correct=c<80,arms=arms))
    return rows


def run():
    rows=entries();samples=np.random.default_rng(421).integers(200,size=(2000,200))
    a=aggregate(rows,'CNN-20k');assert a['eligible']['P']==.74 and a['eligible']['MSRE']==.5 and a['eligible']['VRE']==.75
    assert a['all']['regret']==.26/7 and a['all']['B']==(1600-52)/1600
    g=read_gates(rows,['CNN-20k'],[],samples);assert g['H1a']=='PASS';assert license_ids(g,'1')==[]
    # Finite availability cannot turn an empty eligibility panel into a PASS.
    empty=copy.deepcopy(rows)
    for r in empty:r['eligible']=False
    h=read_gates(empty,['CNN-20k'],[],samples);assert not h['sufficiency'] and h['H1a'] is None
    assert paired_gap(empty,'N-last','CNN-20k',samples) is None
    assert bounds(None)['lower'] is None
    # Failure uses worst regret and ACC zero, while RMSE/response exclude.
    fail=copy.deepcopy(rows)
    r=fail[0]['arms']['CNN-20k'];r.update(failed=True,correct=False,chosen=-1,regret_raw=7.,wACC=0.,wRMSE=None,MSRE_num=None,MSRE_den=None,VRE_num=None,VRE_den=None,dropped=33)
    x=aggregate(fail,'CNN-20k');assert x['all']['excluded_cases']==1 and x['all']['regret_raw']==(52+7)/200
    for v in [float('nan'),float('inf'),-float('inf')]:
        try:reject_nonfinite({'P':v})
        except ValueError:pass
        else:raise AssertionError('nonfinite tamper accepted')
    try:equivalent({'P':.75},{'P':.74})
    except ValueError:pass
    else:raise AssertionError('finite tamper accepted')
    # Verify energy mean/spread identity on a nonzero spread ensemble.
    rgen=np.random.default_rng(21);states=rgen.normal(size=(8,64,4,40));mean=states.mean(1);var=states.var(1).sum(-1)
    st=state_statistics(mean,var,mean,var,mean,np.zeros((8,40)),np.arange(4),0,1.,0)
    parts=st['cost_difference_split'];cost=.5*(states**2).mean(axis=(1,2,3))
    assert np.allclose(np.array(parts['arm_mean_difference'])+parts['arm_spread_difference'],cost-cost[0])
    assert st['MSRE_num']==0 and st['VRE_num']==0
    print('PASS: constructed PASS, insufficiency, failure, covariance identity, finite/NaN tamper cases')
if __name__=='__main__':run()
