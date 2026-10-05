"""CPU-only float64 NumPyro NUTS and RK4 AD; observation-only interface."""
import os
os.environ['JAX_PLATFORMS']='cpu'
os.environ['JAX_ENABLE_X64']='true'
import jax
jax.config.update('jax_enable_x64',True)
import jax.numpy as jnp
from functools import partial,lru_cache
import numpy as np,time
import numpyro,numpyro.distributions as dist
from numpyro.infer import MCMC,NUTS
from acd_protocol import SIGMA,NOISE,rng,settings

def rhs(x,f):return (jnp.roll(x,-1)-jnp.roll(x,2))*jnp.roll(x,1)-x+f
def step(x,f,h):
    a=rhs(x,f);b=rhs(x+h/2*a,f);c=rhs(x+h/2*b,f);d=rhs(x+h*c,f)
    return x+h/6*(a+2*b+2*c+d)
@partial(jax.jit,static_argnums=(1,))
def history(theta,h):
    nper=int(round(.05/h))
    def tick(x,_):
        x=jax.lax.fori_loop(0,nper,lambda _,v:step(v,theta[40],h),x)
        return x,x
    _,tail=jax.lax.scan(tick,theta[:40],None,length=10)
    return jnp.concatenate([theta[None,:40],tail])
def scaled_objective(theta,y,h,mask,z):
    seq=history(theta,h)
    return (jnp.sum((seq-y)**2)+100*jnp.sum(mask*(seq[-1]-z)**2))/440
objective_jax=jax.jit(jax.value_and_grad(scaled_objective),static_argnums=(2,))
@partial(jax.jit,static_argnums=(2,))
def loglike_batch(theta,y,h,mask,z):
    return jax.vmap(lambda t:-.5*440*scaled_objective(t,y,h,mask,z)/NOISE**2)(theta)

def model(y,mask,z,h):
    # Centering and scaling change coordinates, not the declared x prior.
    u=numpyro.sample('u',dist.Normal(-y[0]/NOISE,10*SIGMA/NOISE).to_event(1))
    f=numpyro.sample('F',dist.Uniform(6.,10.))
    theta=jnp.concatenate([y[0]+NOISE*u,jnp.atleast_1d(f)])
    numpyro.factor('likelihood',-.5*440*scaled_objective(theta,y,h,mask,z)/NOISE**2)

class ReusableNUTS(NUTS):
    """Restore scalar kernel before each vectorized initialization.

    NumPyro's init wraps _sample_fn in vmap on each call. Preserve the scalar
    function so independent warmups do not accumulate wrappers on reuse.
    """
    def _init_state(self,*args,**kwargs):
        state=super()._init_state(*args,**kwargs)
        if not hasattr(self,'_scalar_sample'):self._scalar_sample=self._sample_fn
        self._sample_fn=self._scalar_sample
        return state

@lru_cache(maxsize=16)
def sampler(h,warmup,draws):
    return MCMC(ReusableNUTS(partial(model,h=h),dense_mass=True,target_accept_prob=.9),num_warmup=warmup,num_samples=draws,num_chains=4,chain_method='vectorized',progress_bar=False,jit_model_args=True)

def sample(y,starts,panel,c,h,sub=None,action=0,warmup=None,draws=None,mask=None,z=None):
    config=settings();warmup=config['warmup'] if warmup is None else warmup;draws=config['draws'] if draws is None else draws
    mask=np.zeros(40) if mask is None else mask;z=np.zeros(40) if z is None else z
    name='acd-dtcheck' if panel=='dtcheck' else 'acd-posterior-'+panel
    sub=(4 if panel=='dtcheck' else 0) if sub is None else sub
    keys=jnp.stack([jax.random.PRNGKey(int(rng(name,sub,c,chain,action).integers(0,2**32,dtype=np.uint32))) for chain in range(4)])
    fraction=np.clip((starts[:,40]-6)/4,1e-6,1-1e-6)
    initial={'u':jnp.asarray((starts[:,:40]-y[0])/NOISE),'F':jnp.asarray(np.log(fraction/(1-fraction)))}
    mcmc=sampler(h,warmup,draws)
    mcmc.post_warmup_state=None
    tick=time.perf_counter();mcmc.run(keys,jnp.asarray(y),jnp.asarray(mask),jnp.asarray(z),init_params=initial,extra_fields=('diverging','num_steps'))
    samples=mcmc.get_samples(group_by_chain=True);extra=mcmc.get_extra_fields(group_by_chain=True)
    theta=np.concatenate([np.asarray(samples['u'])*NOISE+y[0],np.asarray(samples['F'])[...,None]],axis=-1)
    return theta,dict(seconds=time.perf_counter()-tick,warmup=warmup,draws=draws,divergences=int(np.asarray(extra['diverging']).sum()),
                      divergent_fraction=float(np.asarray(extra['diverging']).mean()),mean_steps=float(np.asarray(extra['num_steps']).mean()),boundary_contacts=int(((theta[...,40]<6.001)|(theta[...,40]>9.999)).sum()))

def diagnostics(theta,y,h,report,mask=None,z=None):
    import arviz as az
    mask=np.zeros(40) if mask is None else mask;z=np.zeros(40) if z is None else z
    ll=np.asarray(loglike_batch(theta.reshape(-1,41),y,h,mask,z)).reshape(theta.shape[:2])
    data={'parameters':theta,'log_likelihood':ll}
    rhat=az.rhat(data,method='rank');ess=az.ess(data,method='bulk')
    r=np.concatenate([np.asarray(v).ravel() for v in rhat.data_vars.values()]);e=np.concatenate([np.asarray(v).ravel() for v in ess.data_vars.values()])
    return dict(max_rhat=float(r.max()),min_ess=float(e.min()),rhat=r.tolist(),ess=e.tolist(),passed=bool(np.isfinite(r).all() and np.isfinite(e).all() and r.max()<=1.01 and e.min()>=400 and report['divergent_fraction']<=.01))

def functional_diagnostics(cost,indices=None):
    import arviz as az
    if indices is None:
        values=np.concatenate([(cost[:,:,0:8,[3,5]]-cost[:,:,8:9,[3,5]]).reshape(cost.shape[0],cost.shape[1],16),cost[:,:,8,[3,5]]],axis=-1)
    else:
        k,l,t=indices;values=(cost[:,:,k,t]-cost[:,:,l,t])[...,None]
    rh=np.asarray(az.rhat({'functions':values},method='rank')['functions']);es=np.asarray(az.ess({'functions':values},method='bulk')['functions'])
    return dict(max_rhat=float(rh.max()),min_ess=float(es.min()),passed=bool(np.isfinite(rh).all() and np.isfinite(es).all() and rh.max()<=1.01 and es.min()>=400))

def implementation_check(map_theta,y,h,c=0,warmup=1000,draws=1000):
    jac=np.asarray(jax.jacfwd(lambda t:history(t,h).reshape(-1))(jnp.asarray(map_theta)))
    precision=jac.T@jac/NOISE**2
    covariance=np.linalg.inv(precision)
    def gaussian():numpyro.sample('theta',dist.MultivariateNormal(jnp.asarray(map_theta),precision_matrix=jnp.asarray(precision)))
    keys=jnp.stack([jax.random.PRNGKey(int(rng('acd-dtcheck',5,c,chain).integers(0,2**32,dtype=np.uint32))) for chain in range(4)])
    m=MCMC(NUTS(gaussian,dense_mass=True,target_accept_prob=.9),num_warmup=warmup,num_samples=draws,num_chains=4,chain_method='vectorized',progress_bar=False)
    tick=time.perf_counter();m.run(keys);samples=np.asarray(m.get_samples(group_by_chain=True)['theta'])
    import arviz as az
    ess=np.asarray(az.ess({'theta':samples},method='bulk')['theta'])
    sq=(samples-map_theta)**2;vess=np.asarray(az.ess({'variance':sq},method='bulk')['variance'])
    flat=samples.reshape(-1,41);mean=flat.mean(0);variance=flat.var(0,ddof=1)
    means_se=np.sqrt(np.diag(covariance)/ess);var_se=np.diag(covariance)*np.sqrt(2/vess)
    mean_errors=np.abs(mean-map_theta)/means_se;var_errors=np.abs(variance-np.diag(covariance))/var_se
    eig,vec=np.linalg.eigh(precision);ratios=[]
    for index in [0,40]:ratios.append(float(np.var(flat@vec[:,index],ddof=1)*eig[index]))
    passed=bool((mean_errors<=4).all() and (var_errors<=4).all() and all(abs(v-1)<=.1 for v in ratios))
    return dict(passed=passed,seconds=time.perf_counter()-tick,warmup=warmup,draws=draws,max_mean_mcse=float(mean_errors.max()),max_variance_mcse=float(var_errors.max()),extreme_variance_ratios=ratios,precision=precision.tolist())
