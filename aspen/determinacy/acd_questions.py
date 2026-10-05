"""Question definitions and authorized truth scoring / input preparation."""
import os
os.environ['JAX_PLATFORMS']='cpu'
os.environ['JAX_ENABLE_X64']='true'
import numpy as np,math
from acd_protocol import ROOT,INHERITED,PATTERNS,physics,NOISE,input_path,truth_path,save_json
PAIRS=[(k,l) for k in range(8) for l in range(k+1,8)]
def prepare_dtcheck(h):
    directory=ROOT/'runs/dtcheck';directory.mkdir(parents=True,exist_ok=True)
    for c in range(8):
        p=directory/f'input_{c:03d}.npz'
        if not p.exists():
            true,observed=physics.history('acd-dtcheck',c,h)
            np.savez(p,true=true,observed=observed)
def actual(panel,c,h):
    with np.load(truth_path(panel,c),allow_pickle=False) as data:true=data['true'].copy()
    states=physics.simulate(np.repeat(true[-1,None],9,axis=0),8+.16*PATTERNS,h)
    return physics.costs(states),np.r_[true[0],8.]
def coverage(panel,c,y,minimum,h,mask=None,z=None):
    from acd_fits import chi
    with np.load(truth_path(panel,c),allow_pickle=False) as data:initial=data['true'][0].copy()
    val=chi(np.r_[initial,8.],y,h,mask,z)-minimum
    return dict(delta_chi2=val,covered=val<=56.94)
def labels(j,jbar):
    if j.ndim==2:j=j[None]
    result=[j[:,:8]<j[:,8,None]]
    result.append(np.stack([j[:,k]<j[:,l] for k,l in PAIRS],axis=1))
    result.append(j[:,:8].argmin(1)[:,None]);result.append((j[:,8]>jbar)[:,None])
    return np.concatenate(result,axis=1).astype(np.int8)
def distribution(j,jbar):
    lab=labels(j,jbar);probs=np.zeros((38,8,8))
    for answer in range(8):probs[:,:,answer]=(lab==answer).mean(0)
    return probs
def summary(j,jbar,null_prob,chains=4):
    lab=labels(j,jbar);prob=distribution(j,jbar);modal=prob.argmax(-1)
    count=(lab==modal[None]).sum(0);p=count/len(j)
    ties=(prob==prob.max(-1,keepdims=True)).sum(-1)>1
    confident=(count>=math.ceil(.95*len(j)))&~ties
    climate=np.take_along_axis(null_prob,modal[...,None],axis=-1)[...,0]>=.95
    indicator=lab==modal[None]
    import arviz as az
    shaped=indicator.reshape(chains,len(j)//chains,38,8).astype(float)
    ess=np.asarray(az.ess({'indicator':shaped},method='bulk')['indicator'])
    constant=indicator.max(0)==indicator.min(0);ess[constant]=len(j)
    pt=(count+.5)/(len(j)+1);se=np.sqrt(pt*(1-pt)/ess)
    # Each sampler's own modal event; the cross-check uses signed events below.
    uncertain=np.abs(p-.95)<2*se
    a=distribution(j[:len(j)//2],jbar);b=distribution(j[len(j)//2:],jbar)
    first=np.where(a.max(-1)>=.95,a.argmax(-1),-1)
    second=np.where(b.max(-1)>=.95,b.argmax(-1),-1)
    return dict(modal=modal,p=p,confident=confident,climate=climate,observation=confident&~climate,
                uncertain=uncertain,se=se,split_unstable=first!=second)
def signed_se(j,jbar,chains=4):
    lab=labels(j,jbar)[:,np.r_[np.arange(36),37]]
    p=lab.mean(0);count=lab.sum(0);pt=(count+.5)/(len(j)+1)
    if chains:
        import arviz as az
        shaped=lab.reshape(chains,len(j)//chains,37,8).astype(float)
        ess=np.asarray(az.ess({'event':shaped},method='bulk')['event'])
        ess[lab.max(0)==lab.min(0)]=len(j)
    else:ess=np.full(p.shape,len(j),float)
    return p,np.sqrt(pt*(1-pt)/ess)
