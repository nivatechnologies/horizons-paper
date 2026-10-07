"""Stage19 fixed-F posterior: observation-only implementation of Todd's contract."""
import numpy as np
import jax,jax.numpy as jnp
import numpyro,numpyro.distributions as dist
from numpyro.infer import MCMC
from scipy.optimize import minimize
from acd_protocol import NOISE,SIGMA
from acd_fits import objective,chi,sequence
from acd_posterior import ReusableNUTS,scaled_objective

def model(y,h):
 u=numpyro.sample('u',dist.Normal(-y[0]/NOISE,10*SIGMA/NOISE).to_event(1))
 theta=jnp.concatenate([y[0]+NOISE*u,jnp.array([8.])])
 numpyro.factor('likelihood',-.5*440*scaled_objective(theta,y,h,jnp.zeros(40),jnp.zeros(40))/NOISE**2)

def fit_known(y,start,h):
 def fn(x):
  v,g=objective(np.r_[x,8.],y,h,np.zeros(40),np.zeros(40));return v,g[:40]
 o=minimize(fn,start,jac=True,method='L-BFGS-B',options={'maxiter':500,'ftol':1e-12,'gtol':1e-8})
 return np.r_[o.x,8.],dict(success=bool(o.success),iterations=int(o.nit),value=float(o.fun),chi2=float(440*o.fun/NOISE**2),message=str(o.message))

def starts(y,c,h,rng):
 # The same original-observation misfit and trajectory checks as case_fits.
 results=[]
 for m in range(128):
  eps=NOISE*rng('acd-r3-knownF-sampler',0,c,m).standard_normal(y.shape)
  results.append(fit_known(y+eps,y[0]+eps[0],h))
 theta=np.array([v[0] for v in results]);ch=np.array([chi(t,y,h) for t in theta])
 direct=fit_known(y,y[0],h);minimum=float(min(direct[1]['chi2'],np.min(ch)))
 valid=np.array([bool(np.isfinite(sequence(t,h)).all() and (np.sqrt(np.mean(sequence(t,h)**2,axis=1))<=10*SIGMA).all() and v-minimum<=74.75) for t,v in zip(theta,ch)])
 ids=np.flatnonzero(valid)[:4]
 if len(ids)<4:raise RuntimeError('R-other: fewer than four valid fixed-F noise-perturbed initializers; case needs recorded resolution')
 return dict(starts=theta[ids],rml=theta,rml_valid=valid,rml_chi=ch,minimum=minimum,report=dict(members=[v[1] for v in results],valid=int(valid.sum()),initializer_indices=ids.tolist(),direct=direct[1]))

def sample(y,starts,c,h,attempt,rng):
 warmup=1000 if attempt==0 else 2000
 keys=jnp.stack([jax.random.PRNGKey(int(rng('acd-r3-knownF-sampler',1+attempt,c,i).integers(0,2**32,dtype=np.uint32))) for i in range(4)])
 m=MCMC(ReusableNUTS(lambda y:model(y,h),dense_mass=True,target_accept_prob=.9),num_warmup=warmup,num_samples=500,num_chains=4,chain_method='vectorized',progress_bar=False,jit_model_args=True)
 import time
 t=time.monotonic();m.run(keys,jnp.asarray(y),init_params={'u':jnp.asarray((starts[:,:40]-y[0])/NOISE)},extra_fields=('diverging','num_steps'))
 x=np.asarray(m.get_samples(group_by_chain=True)['u'])*NOISE+y[0];theta=np.concatenate([x,np.full((*x.shape[:2],1),8.)],axis=-1)
 e=m.get_extra_fields(group_by_chain=True)
 return theta,dict(seconds=time.monotonic()-t,warmup=warmup,draws=500,divergences=int(np.asarray(e['diverging']).sum()),divergent_fraction=float(np.asarray(e['diverging']).mean()),mean_steps=float(np.asarray(e['num_steps']).mean()))

def diagnostics(theta,y,h,report):
 import arviz as az
 from acd_posterior import loglike_batch
 ll=np.asarray(loglike_batch(theta.reshape(-1,41),y,h,np.zeros(40),np.zeros(40))).reshape(theta.shape[:2])
 data={'parameters':theta[...,:40],'log_likelihood':ll};rh=az.rhat(data,method='rank');ess=az.ess(data,method='bulk')
 r=np.concatenate([np.asarray(v).ravel() for v in rh.data_vars.values()]);e=np.concatenate([np.asarray(v).ravel() for v in ess.data_vars.values()])
 return dict(max_rhat=float(r.max()),min_ess=float(e.min()),rhat=r.tolist(),ess=e.tolist(),passed=bool(np.isfinite(r).all() and np.isfinite(e).all() and r.max()<=1.01 and e.min()>=400 and report['divergent_fraction']<=.01))
