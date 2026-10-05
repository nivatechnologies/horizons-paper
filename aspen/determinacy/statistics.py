"""Standalone WO v2.2 statistics. No physics or experimental data imports.

Earlier-case pseudo moments: count=1, sum=.5, sum of squares=.5.
This is one unit of prior weight with mean .5 and variance .25.
Grid inversion follows the WO literally; no outward rounding is added.
"""
import math
import numpy as np
from numba import njit, prange
from scipy.stats import beta, binomtest


@njit(cache=True)
def log_capital_max(x, m, direction):
    total, squares, count = .5, .5, 1
    capital, peak = 0., 0.
    for value in x:
        if np.isnan(value):
            continue
        mu = total / count
        variance = max(0., squares / count - mu * mu)
        advantage = direction * (mu - m)
        denominator = variance + advantage * advantage
        bet = max(0., advantage / denominator) if denominator > 0 else 0.
        cap_den = m if direction == 1 else 1 - m
        if cap_den > 0:
            bet = min(bet, .75 / cap_den)
        capital += math.log1p(direction * bet * (value - m))
        peak = max(peak, capital)
        total += value
        squares += value * value
        count += 1
    return peak


@njit(cache=True)
def one_sided(x, alpha, direction):
    threshold = -math.log(alpha)
    if direction == 1:
        bound = 0.  # No rejected grid point at .500 gives the trivial lower bound.
        for k in range(500, 1001):
            if log_capital_max(x, k / 1000., 1) < threshold:
                break
            bound = k / 1000.
    else:
        bound = 1.
        for k in range(1000, -1, -1):
            if log_capital_max(x, k / 1000., -1) < threshold:
                break
            bound = k / 1000.
    return bound


@njit(cache=True)
def interval(x, alpha=.01):
    threshold = math.log(2 / alpha)
    lower, upper = 2., -1.
    for k in range(1001):
        m = k / 1000.
        if max(log_capital_max(x, m, 1), log_capital_max(x, m, -1)) < threshold:
            lower = min(lower, m)
            upper = max(upper, m)
    return lower, upper  # Empty retained grid is deliberately exposed.


@njit(cache=True, parallel=True)
def r0_pass_batch(sizes, correct):
    result = np.zeros(sizes.shape[0], dtype=np.bool_)
    threshold = math.log(20.)
    for i in prange(sizes.shape[0]):
        n, c = sizes[i], correct[i]
        if n.sum() < 100 or (n > 0).sum() < 30:
            continue
        if c.sum() / n.sum() < .9:
            continue
        x = np.empty(n.size)
        for j in range(n.size):
            x[j] = c[j] / n[j] if n[j] else np.nan
        # Necessary condition first; then every preceding grid point is tested.
        if log_capital_max(x, .9, 1) < threshold:
            continue
        passed = True
        for k in range(500, 900):
            if log_capital_max(x, k / 1000., 1) < threshold:
                passed = False
                break
        result[i] = passed
    return result


@njit(cache=True, parallel=True)
def interval_noncoverage_batch(x, true_mean=.5, alpha=.01):
    result = np.zeros(x.shape[0], dtype=np.bool_)
    threshold = math.log(2 / alpha)
    for i in prange(x.shape[0]):
        # On-grid retained mean is certainly in the retained-grid hull.
        if max(log_capital_max(x[i], true_mean, 1),
               log_capital_max(x[i], true_mean, -1)) < threshold:
            continue
        lo, hi = interval(x[i], alpha)
        result[i] = not lo <= true_mean <= hi
    return result


@njit(cache=True, parallel=True)
def positive_r2_route_batch(x, minimum=.15, alpha=.01):
    result = np.zeros(x.shape[0], dtype=np.bool_)
    threshold = math.log(2 / alpha)
    for i in prange(x.shape[0]):
        if 2 * x[i].mean() - 1 < minimum:
            continue
        if max(log_capital_max(x[i], .5, 1), log_capital_max(x[i], .5, -1)) < threshold:
            continue
        # All points at/below zero difference must be excluded for lower>0.
        passed = True
        for k in range(501):
            m = k / 1000.
            if max(log_capital_max(x[i], m, 1), log_capital_max(x[i], m, -1)) < threshold:
                passed = False
                break
        result[i] = passed
    return result


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


def r0(sizes, correct):
    n, c = np.asarray(sizes), np.asarray(correct)
    if n.shape != c.shape or np.any(c < 0) or np.any(c > n) or np.any(n > 8):
        raise ValueError('Require matched case counts with 0 <= correct <= sizes <= 8')
    nonempty = n > 0
    a = c[nonempty] / n[nonempty]
    answer_point = float(c.sum() / n.sum()) if n.sum() else None
    lo, hi = one_sided(a, .05, 1), one_sided(a, .05, -1)
    status = ('NOT EVALUABLE' if n.sum() < 100 or nonempty.sum() < 30 else
              'PASS' if lo >= .9 and answer_point >= .9 else
              'FAIL' if hi < .9 else 'INSUFFICIENT')
    # Candidate-dependent bounded process, including empty cases as required.
    answer_lower = 0.
    for k in range(500, 1001):
        m = k / 1000.
        values = (c - m * n) / 8 + m
        if log_capital_max(values, m, 1) < math.log(20):
            break
        answer_lower = m
    return dict(status=status, cases=int(nonempty.sum()), answers=int(n.sum()),
                case_accuracy=float(a.mean()) if a.size else None,
                case_lower=float(lo), case_upper=float(hi),
                answer_accuracy=answer_point, answer_lower=float(answer_lower))


def r0_f(correct, total):
    lo, hi = cp_bounds(correct, total) if total else (0., 1.)
    status = ('NOT EVALUABLE' if total < 30 else 'PASS' if lo >= .9 else
              'FAIL' if hi < .9 else 'INSUFFICIENT')
    return dict(status=status, lower=lo, upper=hi)


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
