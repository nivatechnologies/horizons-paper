"""Synthetic-only v2.3 audit, reproducible on sulaco CPU."""
import argparse
import hashlib
import json
import math
import platform
import time
from pathlib import Path
import numpy as np
import scipy
from scipy.stats import binom, binomtest
from acd_stats import (cp_bounds, mcnemar, r0, r0_f, r0_pass_batch,
                        interval_noncoverage_batch, positive_r2_route_batch,
                        one_sided, interval, descriptive_ratio_bootstrap)


def estimate(values, nominal=None):
    rate = float(np.mean(values))
    se = math.sqrt((nominal * (1 - nominal) if nominal is not None else rate * (1 - rate)) / len(values))
    result = dict(rate=rate, mc_se=se, panels=len(values), events=int(np.sum(values)))
    if nominal is not None:
        result.update(nominal=nominal, limit=nominal + 2 * se,
                      passed=rate <= nominal + 2 * se)
    return result


def sizes_for(rng, theme, panels, n=200):
    if theme == 'executor':
        return rng.choice([0, 1, 8], size=(panels, n), p=[.85, .1, .05])
    if theme == 'uniform':
        return rng.integers(0, 9, size=(panels, n))
    # Half empty, other half uniform 1..8. Explicitly pinned implementation choice.
    return rng.integers(1, 9, size=(panels, n)) * rng.binomial(1, .5, size=(panels, n))


def correct_for(rng, sizes, mechanism, accuracy=.9, eight_fraction=None):
    if mechanism == 'independent':
        return rng.binomial(sizes, accuracy)
    if mechanism == 'whole-case':
        return sizes * rng.binomial(1, accuracy, size=sizes.shape)
    fail_probability = (1 - accuracy) / eight_fraction
    if fail_probability > 1 + 1e-12:
        raise ValueError('Impossible case-averaged target for eight-only errors')
    return sizes * (1 - ((sizes == 8) & (rng.random(sizes.shape) < fail_probability)))


def exact_audit():
    cp_error = 0.
    for n in [1, 5, 20, 30, 34, 40, 100, 200]:
        for k in range(n + 1):
            expected = binomtest(k, n).proportion_ci(confidence_level=.90, method='exact')
            actual = cp_bounds(k, n)
            cp_error = max(cp_error, abs(actual[0] - expected.low), abs(actual[1] - expected.high))
    mc_error = 0.
    for n in range(1, 101):
        for q in range(n + 1):
            actual = mcnemar(q, n - q)
            expected = binomtest(q, n, .5, alternative='greater').pvalue
            # Independent exact-tail computation checks scipy agreement too.
            tail = sum(math.comb(n, j) for j in range(q, n + 1)) / 2 ** n
            mc_error = max(mc_error, abs(actual - expected), abs(actual - tail))
    # Redraw behavior and non-evaluable all-empty case are checked without gate use.
    redraw = descriptive_ratio_bootstrap([1, 0], [1, 0], np.random.default_rng(17))
    empty = descriptive_ratio_bootstrap([0, 0], [0, 0], np.random.default_rng(17))
    return dict(cp_max_absolute_error=cp_error, cp_tolerance=1e-10,
                mcnemar_max_absolute_error=mc_error, mcnemar_tolerance=1e-12,
                mcnemar_no_discordance=mcnemar(0, 0),
                mcnemar_five_all_Q=mcnemar(5, 0),
                thirty_perfect_Fc=r0_f(30, 30),
                descriptive_redraw_test=redraw, descriptive_all_empty_test=empty,
                passed=(cp_error < 1e-10 and mc_error < 1e-12
                        and redraw['redraws'] > 0 and redraw['interval'] == [1., 1.]
                        and empty['status'] == 'NOT EVALUABLE'))


def run(args):
    started = time.monotonic()
    rng = np.random.default_rng(2026100522)
    report = dict(work_order='v2.3', source_class='synthetic hypotheses under test',
                  host=platform.node(), numpy=np.__version__, scipy=scipy.__version__,
                  seed=2026100522, null_panels=args.panels, power_panels=args.power_panels,
                  variance_convention='mu=(.5+sum x)/(t+1); sigma2=(.25+sum (x_i-mu_i)^2)/(t+1)',
                  grid='monotone bisection .001, outward rounding, continuous parameter; alpha/2 each side',
                  exact=exact_audit(), null_R0=[], null_R2=[], power_R0=[], power_R2=[])
    from acd_stats import monotonicity_audit, log_capital_max
    sequences=rng.uniform(size=(1000,200))
    sequences[:250]=rng.binomial(1,.5,size=(250,200))
    sequences[250:500]=rng.beta(2,10,size=(250,200))
    violations=monotonicity_audit(sequences)
    report['monotonicity']=dict(sequences=1000,grid_step=.0001,violations=int(violations.sum()),passed=not violations.any())
    report['witnesses']=[]
    for value,m in [(1.,.9629),(0.,.0371)]:
        x=np.full(200,value);lo,hi=interval(x,.01)
        peak=max(log_capital_max(x,m,1,.005),log_capital_max(x,m,-1,.005))
        report['witnesses'].append(dict(value=value,candidate=m,interval=[lo,hi],candidate_rejected=bool(peak>=math.log(200)),candidate_included=bool(lo<=m<=hi),peak=float(math.exp(peak))))
    print('Exact and monotonicity procedures audited',flush=True)
    for theme, fraction in [('executor', 1/3), ('uniform', 1/8), ('half-empty', 1/8)]:
        for mechanism in ['independent', 'whole-case', 'eight-only']:
            n = sizes_for(rng, theme, args.panels)
            c = correct_for(rng, n, mechanism, eight_fraction=fraction)
            outcome = r0_pass_batch(n, c)
            row = dict(sizes=theme, mechanism=mechanism,
                       case_averaged_true_accuracy=.9, eight_error_probability=.1/fraction
                       if mechanism == 'eight-only' else None,
                       evaluable_panels=int(((n.sum(axis=1) >= 100) & ((n > 0).sum(axis=1) >= 30)).sum()),
                       **estimate(outcome, .05))
            report['null_R0'].append(row)
            print('Null R0', theme, mechanism, row['rate'], flush=True)
    for theme in ['symmetric', 'skewed', 'sparse']:
        if theme == 'symmetric':
            d = rng.choice([-1., 1.], size=(args.panels, 200))
        elif theme == 'skewed':
            d = rng.choice([-1., .25], size=(args.panels, 200), p=[.2, .8])
        else:
            d = rng.choice([-1., 0., 1.], size=(args.panels, 200), p=[.01, .98, .01])
        result = interval_noncoverage_batch((d + 1) / 2)
        report['null_R2'].append(dict(theme=theme, true_difference=0., **estimate(result, .01)))
        print('Null R2', theme, float(result.mean()), flush=True)
    # Preserve both estimands on the prior counterexample.
    n = sizes_for(rng, 'executor', args.panels)
    c = n * (1 - ((n == 8) & (rng.random(n.shape) < .14)))
    old_pass = ((n.sum(axis=1) >= 100) & ((n > 0).sum(axis=1) >= 30)
                & (c.sum(axis=1) == n.sum(axis=1)))
    new_pass = r0_pass_batch(n, c)
    fixture_n = np.array([8]*10 + [1]*20 + [0]*170)
    report['counterexample'] = dict(answer_accuracy=.888, case_accuracy=(.1+.043)/.15,
                                    interpretation='case accuracy=.953333, so this is an alternative, not a v2.3 null',
                                    old_no_error_PASS=estimate(old_pass), new_PASS=estimate(new_pass),
                                    thirty_perfect_fixture=r0(fixture_n, fixture_n))
    print('Counterexample reported', flush=True)
    for accuracy in [.95, .97, .985]:
        for nonempty in [50, 80, 120, 160]:
            for mechanism in ['independent', 'whole-case']:
                # Cases nonempty at first indices, sizes uniform 1..8.
                n = np.zeros((args.power_panels, 200), dtype=np.int64)
                n[:, :nonempty] = rng.integers(1, 9, size=(args.power_panels, nonempty))
                c = correct_for(rng, n, mechanism, accuracy)
                result = r0_pass_batch(n, c)
                report['power_R0'].append(dict(accuracy=accuracy, nonempty=nonempty,
                                                mechanism=mechanism, **estimate(result)))
                print('Power R0', accuracy, nonempty, mechanism, float(result.mean()), flush=True)
    for delta in [.15, .25]:
        for theme in ['high-variance', 'low-variance']:
            if theme == 'high-variance':
                d = 2 * rng.binomial(1, (delta + 1)/2, size=(args.power_panels, 200)) - 1.
            else:
                d = delta + rng.choice([-.25, .25], size=(args.power_panels, 200))
            x = (d + 1) / 2
            result = positive_r2_route_batch(x)
            strong = positive_r2_route_batch(x, .25)
            report['power_R2'].append(dict(delta=delta, theme=theme,
                                            inference='statistical route only; assumes calibration prerequisites',
                                            publish=estimate(result), strong=estimate(strong)))
            print('Power R2', delta, theme, float(result.mean()), flush=True)
    report['all_prescribed_checks_pass'] = report['exact']['passed'] and report['monotonicity']['passed'] and all(
        row['passed'] for row in report['null_R0'] + report['null_R2'])
    report['wall_seconds'] = time.monotonic() - started
    report['code_hashes'] = {name: hashlib.sha256(Path(name).read_bytes()).hexdigest()
                              for name in ['acd_stats.py', 'acd_stats_audit.py']}
    Path(args.output).parent.mkdir(parents=True,exist_ok=True)
    Path(args.output).write_text(json.dumps(report, indent=2) + '\n')
    print('Audit complete', report['all_prescribed_checks_pass'], flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--panels', type=int, default=20000)
    parser.add_argument('--power-panels', type=int, default=5000)
    parser.add_argument('--output', default='runs/audit/acd_stats_audit.json')
    arguments = parser.parse_args()
    if arguments.panels < 20000:
        parser.error('WO requires at least 20,000 null panels per configuration')
    run(arguments)
