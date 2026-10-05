"""WO v2.3 predictable plug-in betting; outward discrete inversion."""
import os
os.environ['JAX_PLATFORMS']='cpu'
os.environ['JAX_ENABLE_X64']='true'
import math
import numpy as np
from numba import njit, prange
from scipy.stats import beta, binomtest

@njit(cache=True)
def log_capital_max(x, m, direction, alpha=.05):
    total, residual, count = .5, .25, 0
    capital, peak = 0., 0.
    for value in x:
        if np.isnan(value): continue
        t=count+1
        variance=residual/t
        bet=min(.9, math.sqrt(2*math.log(1/alpha)/(variance*t*math.log(t+1))))
        capital+=math.log1p(direction*bet*(value-m))
        peak=max(peak,capital)
        total+=value
        count+=1
        mu=total/(count+1)
        residual+=(value-mu)**2
    return peak

@njit(cache=True)
def one_sided(x,alpha,direction):
    threshold=math.log(1/alpha)
    low,high=0,1000
    if direction==1:
        if log_capital_max(x,0.,1,alpha)<threshold: return 0.
        while low<high:
            mid=(low+high+1)//2
            if log_capital_max(x,mid/1000.,1,alpha)>=threshold:low=mid
            else:high=mid-1
        return low/1000.
    if log_capital_max(x,1.,-1,alpha)<threshold:return 1.
    while low<high:
        mid=(low+high)//2
        if log_capital_max(x,mid/1000.,-1,alpha)>=threshold:high=mid
        else:low=mid+1
    return low/1000.

@njit(cache=True)
def interval(x,alpha=.01):
    return one_sided(x,alpha/2,1),one_sided(x,alpha/2,-1)

@njit(cache=True,parallel=True)
def r0_pass_batch(sizes,correct):
    result=np.zeros(sizes.shape[0],dtype=np.bool_)
    for i in prange(sizes.shape[0]):
        n,c=sizes[i],correct[i]
        if n.sum()<100 or (n>0).sum()<30 or c.sum()/n.sum()<.9:continue
        x=np.empty(n.size)
        for j in range(n.size):x[j]=c[j]/n[j] if n[j] else np.nan
        lo,hi=one_sided(x,.05,1),one_sided(x,.05,-1)
        result[i]=lo>=.9 and hi>=.9
    return result

@njit(cache=True,parallel=True)
def interval_noncoverage_batch(x,true_mean=.5,alpha=.01):
    result=np.zeros(x.shape[0],dtype=np.bool_)
    for i in prange(x.shape[0]):
        lo,hi=interval(x[i],alpha)
        result[i]=not lo<=true_mean<=hi
    return result

@njit(cache=True,parallel=True)
def positive_r2_route_batch(x,minimum=.15,alpha=.01):
    result=np.zeros(x.shape[0],dtype=np.bool_)
    for i in prange(x.shape[0]):
        lo,hi=interval(x[i],alpha)
        result[i]=lo<=hi and lo>.5 and 2*x[i].mean()-1>=minimum
    return result

@njit(cache=True,parallel=True)
def monotonicity_audit(sequences):
    counts=np.zeros(len(sequences),dtype=np.int64)
    for i in prange(len(sequences)):
        pp=log_capital_max(sequences[i],0.,1,.005)
        pm=log_capital_max(sequences[i],0.,-1,.005)
        for k in range(1,10001):
            p=log_capital_max(sequences[i],k/10000.,1,.005)
            m=log_capital_max(sequences[i],k/10000.,-1,.005)
            if p>pp+1e-10 or m<pm-1e-10:counts[i]+=1
            pp,pm=p,m
    return counts

def cp_bounds(correct, total, alpha=.05):
    if not 0 <= correct <= total or total < 1:
        raise ValueError('Require 0 <= correct <= total, total >= 1')
    lower = float(beta.ppf(alpha, correct, total - correct + 1)) if correct else 0.
    upper = float(beta.ppf(1 - alpha, correct + 1, total - correct)) if correct < total else 1.
    return lower, upper


def mcnemar(q_only, alternative_only):
    if min(q_only, alternative_only) < 0:
        raise ValueError('Discordant counts must be nonnegative')
    total = q_only + alternative_only
    return float(binomtest(q_only, total, .5, alternative='greater').pvalue) if total else 1.


def r0(sizes,correct,fallback=False):
    n,c=np.asarray(sizes),np.asarray(correct)
    nonempty=n>0
    a=c[nonempty]/n[nonempty]
    lo,hi=float(one_sided(a,.05,1)),float(one_sided(a,.05,-1))
    if fallback and len(a):
        lo=min(lo,cp_bounds(int((c[nonempty]==n[nonempty]).sum()),len(a))[0])
        hi=max(hi,cp_bounds(int((c[nonempty]>0).sum()),len(a))[1])
    ap=float(c.sum()/n.sum()) if n.sum() else None
    status=('NOT EVALUABLE' if n.sum()<100 or nonempty.sum()<30 else
            'INSUFFICIENT' if lo>=.9 and hi<.9 else
            'PASS' if lo>=.9 and ap>=.9 else 'FAIL' if hi<.9 else 'INSUFFICIENT')
    return dict(status=status,cases=int(nonempty.sum()),answers=int(n.sum()),
                case_accuracy=float(a.mean()) if len(a) else None,
                case_lower=lo,case_upper=hi,answer_accuracy=ap,fallback=fallback)

def difference_interval(d,alpha=.01,fallback=False):
    d=np.asarray(d);lo,hi=interval((d+1)/2,alpha)
    lo,hi=2*lo-1,2*hi-1
    if fallback and len(d):
        radius=math.sqrt(2*math.log(2/alpha)/len(d))
        lo=min(lo,float(d.mean())-radius);hi=max(hi,float(d.mean())+radius)
    return dict(lower=float(lo),upper=float(hi),empty=lo>hi,
                point=float(d.mean()) if len(d) else None,
                offset=bool(len(d) and not lo<=d.mean()<=hi),fallback=fallback)

def r0_f(correct,total):
    lo,hi=cp_bounds(correct,total) if total else (0.,1.)
    status=('NOT EVALUABLE' if total<30 else 'PASS' if lo>=.9 else 'FAIL' if hi<.9 else 'INSUFFICIENT')
    return dict(status=status,lower=lo,upper=hi)

def descriptive_ratio_bootstrap(numerator, denominator, rng, replicates=10000):
    numerator, denominator = np.asarray(numerator), np.asarray(denominator)
    if numerator.shape != denominator.shape or numerator.ndim != 1:
        raise ValueError('Require matching one-dimensional case arrays')
    if denominator.sum() == 0:
        return dict(interval=None, redraws=0, status='NOT EVALUABLE', approximate=True)
    values, redraws = [], 0
    while len(values) < replicates:
        indices = rng.integers(0, numerator.size, size=(replicates - len(values), numerator.size))
        den = denominator[indices].sum(axis=1)
        valid = den > 0
        redraws += int((~valid).sum())
        values.extend((numerator[indices].sum(axis=1)[valid] / den[valid]).tolist())
    return dict(interval=np.quantile(values, [.025, .975]).tolist(),
                redraws=redraws, status='DESCRIPTIVE', approximate=True)
