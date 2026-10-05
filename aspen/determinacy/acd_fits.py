"""Joint RK4 reverse mode, MAP and RML; observed data only."""
import os
os.environ['JAX_PLATFORMS']='cpu'
os.environ['JAX_ENABLE_X64']='true'
import numpy as np,time
from numba import njit
from scipy.optimize import minimize
from concurrent.futures import ThreadPoolExecutor
from acd_protocol import NOISE,SIGMA,rng,physics,dt,resolution

@njit(cache=True)
def vjp(x,g):
    out=-g.copy()
    for i in range(40):
        out[(i+1)%40]+=g[i]*x[(i-1)%40]
        out[(i-2)%40]-=g[i]*x[(i-1)%40]
        out[(i-1)%40]+=g[i]*(x[(i+1)%40]-x[(i-2)%40])
    return out
@njit(cache=True)
def rkback(x,F,h,g):
    k1=physics.rhs(x,F);b=x+h*.5*k1;k2=physics.rhs(b,F);c=x+h*.5*k2;k3=physics.rhs(c,F);d=x+h*k3
    adj=g.copy();a1=h/6*g;a2=h/3*g;a3=h/3*g;a4=h/6*g
    gf=a4.sum();gd=vjp(d,a4);adj+=gd;a3+=h*gd
    gf+=a3.sum();gc=vjp(c,a3);adj+=gc;a2+=h*.5*gc
    gf+=a2.sum();gb=vjp(b,a2);adj+=gb;a1+=h*.5*gb
    gf+=a1.sum();adj+=vjp(x,a1)
    return adj,gf
@njit(cache=True,nogil=True)
def objective(theta,window,h,mask,z):
    nper=int(round(.05/h));n=10*nper;F=np.full(40,theta[40])
    states=np.empty((n+1,40));states[0]=theta[:40]
    for s in range(n):states[s+1]=physics.step(states[s],F,h)
    val=0.;adj=np.zeros(40);gf=0.
    for s in range(n,-1,-1):
        if s==n:
            diff=(states[s]-z)*mask
            val+=100*np.sum(diff*diff)/440;adj+=200*diff/440
        if s%nper==0:
            diff=states[s]-window[s//nper];val+=np.sum(diff*diff)/440;adj+=2*diff/440
        if s>0:
            adj,force=rkback(states[s-1],F,h,adj);gf+=force
    result=np.empty(41);result[:40]=adj;result[40]=gf
    return val,result

def fit(y,start,h,mask=None,z=None,use_jax=False):
    mask=np.zeros(40) if mask is None else mask;z=np.zeros(40) if z is None else z
    if use_jax:
        from acd_posterior import objective_jax
        fn=lambda theta:tuple(np.asarray(v) for v in objective_jax(theta,y,h,mask,z))
    else:fn=lambda theta:objective(theta,y,h,mask,z)
    opt=minimize(fn,start,jac=True,method='L-BFGS-B',bounds=[(None,None)]*40+[(6.,10.)],options={'maxiter':500,'ftol':1e-12,'gtol':1e-8})
    return opt.x,dict(success=bool(opt.success),iterations=int(opt.nit),value=float(opt.fun),chi2=float(440*opt.fun/NOISE**2),message=str(opt.message))
def sequence(theta,h):return physics.simulate(theta[None,:40],np.full((1,40),theta[40]),h,11)[0]
def chi(theta,y,h,mask=None,z=None):
    mask=np.zeros(40) if mask is None else mask;z=np.zeros(40) if z is None else z
    return float(objective(theta,y,h,mask,z)[0]*440/NOISE**2)
def case_fits(y,panel,c,h,use_jax=False,workers=8):
    start=time.perf_counter();fhat=physics.identify(y,h)
    name='acd-dtcheck' if panel=='dtcheck' else 'acd-sampler-'+panel
    sub=2 if panel=='dtcheck' else 0
    def member(m):
        eps=NOISE*rng(name,sub,c,m).standard_normal(y.shape)
        return fit(y+eps,np.r_[y[0]+eps[0],fhat],h,use_jax=use_jax)
    with ThreadPoolExecutor(max_workers=workers) as pool:members=list(pool.map(member,range(128)))
    theta=np.asarray([r[0] for r in members]);member_chi=np.array([chi(t,y,h) for t in theta])
    best=theta[np.nanargmin(member_chi)]
    starts=[np.r_[y[0],f] for f in [fhat,6.5,9.5]]+[best]
    maps=[fit(y,s,h,use_jax=use_jax) for s in starts]
    minimum=min([r[1]['chi2'] for r in maps]+member_chi.tolist())
    valid=[]
    for t,ch in zip(theta,member_chi):
        seq=sequence(t,h)
        valid.append(bool(np.isfinite(seq).all() and (np.sqrt(np.mean(seq**2,axis=1))<=10*SIGMA).all() and ch-minimum<=74.75))
    valid=np.array(valid);lowest=np.flatnonzero(valid)[:4]
    if valid.sum()<112:resolution('R-rml',f'{panel} {c}: {valid.sum()} valid','Use available valid members as cross-check')
    if len(lowest)<4:
        resolution('R-other',f'{panel} {c}: fewer than four valid starts','Use lowest-chi finite members for chain starts; flag')
        lowest=np.argsort(member_chi)[:4]
    map_index=int(np.argmin([r[1]['chi2'] for r in maps]))
    return dict(rml=theta,rml_valid=valid,rml_chi=member_chi,map=maps[map_index][0],
                starts=theta[lowest],minimum=minimum,fhat=fhat,
                report=dict(seconds=time.perf_counter()-start,valid=int(valid.sum()),members=[r[1] for r in members],maps=[r[1] for r in maps],
                            boundary_contacts=int(((theta[:,40]<=6+1e-8)|(theta[:,40]>=10-1e-8)).sum())))
