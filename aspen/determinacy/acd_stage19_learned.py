"""Freeze B learned readings; fresh realized arrays are opened only by score()."""
import os
os.environ.update(JAX_PLATFORMS='cpu', JAX_ENABLE_X64='true', OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
import json
from pathlib import Path
import numpy as np
from scipy.stats import beta
from acd_stage19_part2_gate import ROOT, OUT, digest, freeze_ready
from acd_protocol import LEADS, WINDOWS, SIGMA
from acd_stage6_analysis import binary, stack, comparisons
from acd_stage9_receipts import endpoint_fixed, dist
from acd_stage13_analysis import decision_rows, choices
from acd_stats import r0, difference_interval, cp_bounds

MODELS = ['posterior', 'CNN-F', 'CNN-noF', 'CNN-20k']


def model_inputs(name, jbar, null):
    costs, means, valid, rows, physics_costs = [], [], [], [], []
    directory = OUT / 'inference' / name
    if name != 'posterior':
        execution = json.loads((directory / 'complete.json').read_text())
        if execution['cases'] != 200:
            raise RuntimeError('Model inference incomplete')
    for case in range(200):
        with np.load(OUT / f'main_forecast_{case:03d}.npz') as data:
            physical = data['J'].copy()
            mean = data['factual_mean'].copy()
        if name == 'posterior':
            predicted = physical
            ok = np.isfinite(predicted).all()
        else:
            path = directory / f'{case:03d}.npz'
            if digest(path) != execution['output_hashes'][path.name]:
                raise RuntimeError('Inference output hash mismatch')
            with np.load(path) as data:
                predicted = data['J'].copy()
                mean = data['factual_mean'].copy()
                ok = bool(data['valid'].all()) and np.isfinite(predicted).all()
            if predicted.shape != physical.shape:
                raise RuntimeError('Draw/option/lead alignment differs')
        summary = binary(predicted, jbar, null)
        if not ok:
            summary['confident'].fill(False)
            summary['observation'].fill(False)
        costs.append(predicted)
        physics_costs.append(physical)
        means.append(mean)
        valid.append(bool(ok))
        rows.append(summary)
    return costs, np.asarray(means), np.asarray(valid), stack(rows), physics_costs


def metrics(name, costs, means, valid, summary, physical, actual, factual, jbar, climate, sd, fixed):
    keep = np.ones(len(costs), dtype=bool)
    truth = np.concatenate([actual[:, :8] < actual[:, 8, None], (actual[:, 8] > jbar)[:, None]], 1)
    readings, skills, errors = [], [], []
    for t in [3, 5]:
        right = summary['modal'][:, :8, t] == truth[:, :8, t]
        conf = summary['confident'][:, :8, t]
        obs = summary['observation'][:, :8, t]
        fc = summary['confident'][:, 8, t]
        fc_right = summary['modal'][:, 8, t] == truth[:, 8, t]
        acc = r0(conf.sum(1), (conf & right).sum(1))
        readings.append(dict(lead=float(LEADS[t]), confident_S_share=float(conf.mean()),
                             observation_S_share=float(obs.mean()), confident_Fc_share=float(fc.mean()),
                             all_confident_accuracy=acc,
                             observation_confident_accuracy=r0(obs.sum(1), (obs & right).sum(1)),
                             Fc_accuracy=r0(fc.astype(int), (fc & fc_right).astype(int)),
                             pooled_confident_error=None if acc['answer_accuracy'] is None else 1-acc['answer_accuracy'],
                             case_confident_error=None if acc['case_accuracy'] is None else 1-acc['case_accuracy'],
                             case_error_lower=1-acc['case_upper'], case_error_upper=1-acc['case_lower']))
        common = min(means.shape[1], factual.shape[1])
        prediction, realized = means[:, :common], factual[:, :common]
        rmse = np.sqrt(np.mean((prediction-realized)**2, -1))/SIGMA
        x, y = prediction-climate, realized-climate
        acc_state = np.sum(x*y, -1)/np.sqrt(np.sum(x*x, -1)*np.sum(y*y, -1))
        skills.append(dict(lead=float(LEADS[t]), window_mean_RMSE_over_sigma=float(rmse[:, WINDOWS[t]].mean()),
                           window_mean_anomaly_correlation=float(acc_state[:, WINDOWS[t]].mean())))
        for kind in ['J8', 'Jk', 'Dk']:
            local = []
            for predicted, target in zip(costs, physical):
                error = (predicted[:, 8, t]-target[:, 8, t] if kind == 'J8' else
                         predicted[:, :8, t]-target[:, :8, t] if kind == 'Jk' else
                         (predicted[:, :8, t]-predicted[:, 8, None, t])-(target[:, :8, t]-target[:, 8, None, t]))
                local.append(error.ravel())
            joined = np.concatenate(local)
            errors.append(dict(lead=float(LEADS[t]), quantity=kind, draw_action_values=len(joined),
                               pooled_bias=float(joined.mean()), pooled_RMSE=float(np.sqrt(np.mean(joined**2))),
                               equal_case_bias=float(np.mean([v.mean() for v in local])),
                               equal_case_RMSE=float(np.mean([np.sqrt(np.mean(v**2)) for v in local]))))
    reliability, coverage, tests = [], [], []
    for t in [3, 5]:
        p = summary['p'][:, 1:8, t]
        right = summary['modal'][:, 1:8, t] == truth[:, 1:8, t]
        edges = [.5, .6, .7, .8, .9, .95, .99, 1.]
        for lo, hi in zip(edges[:-1], edges[1:]):
            mask = (p >= lo) & ((p <= hi) if hi == 1 else p < hi)
            total, correct = int(mask.sum()), int(right[mask].sum())
            lower = float(beta.ppf(.025, correct, total-correct+1)) if correct else 0.
            upper = float(beta.ppf(.975, correct+1, total-correct)) if correct < total else 1.
            reliability.append(dict(lead=float(LEADS[t]), lower_edge=lo, upper_edge=hi,
                                    questions=total, correct=correct,
                                    mean_probability=float(p[mask].mean()) if total else None,
                                    accuracy=correct/total if total else None,
                                    CP95=[lower, upper] if total else None,
                                    scope='Pooled descriptive interval; within-case questions dependent.'))
        for threshold in [.5, .55, .6, .65, .7, .75, .8, .85, .9, .95, .99]:
            mask = p >= threshold
            accuracy = r0(mask.sum(1), (mask & right).sum(1))
            coverage.append(dict(lead=float(LEADS[t]), threshold=threshold, coverage=float(mask.mean()),
                                 pooled_error=None if accuracy['answer_accuracy'] is None else 1-accuracy['answer_accuracy'],
                                 accuracy=accuracy))
        for threshold in [.5, .95]:
            values = [(p[c, p[c] >= threshold]-right[c, p[c] >= threshold]).mean()
                      for c in range(len(p)) if np.any(p[c] >= threshold)]
            interval = difference_interval(values)
            tests.append(dict(lead=float(LEADS[t]), threshold=threshold, cases=len(values),
                              overconfidence_interval=interval,
                              reject_mean_calibration=bool(not interval['empty'] and not interval['offset'] and
                                                           (interval['lower'] > 0 or interval['upper'] < 0)),
                              test='v2.3 two-sided99% case-mean modal probability minus correctness'))
    eligible = summary['observation'][:, :8, 0] & summary['confident'][:, 8, 0, None]
    decisions, _ = decision_rows(actual, costs, valid, keep, sd)
    for row in decisions:
        t = int(np.flatnonzero(np.asarray(LEADS) == row['lead'])[0])
        selected = choices(costs, valid, t, sd)[row['policy']]
        acting = selected != 8
        harms = actual[np.arange(len(actual)), selected, t]-actual[:, 8, t]
        count = int(acting.sum())
        row['actions_taken'] = count
        row['conditional_harm_CP95'] = list(cp_bounds(int(np.sum((harms > 0) & acting)), count)) if count else [0., 1.]
        row['uniform_decrease_every_case'] = bool(np.all(selected == 0))
    return dict(model=name, fresh_panel=True, descriptive=True, invalid_cases=np.flatnonzero(~valid).tolist(),
                confidence_readings=readings, state_skill=skills, per_draw_cost_errors=errors,
                reliability=reliability, error_coverage=coverage, calibration_test=tests,
                comparisons=[v for v in comparisons(summary, keep) if v['lead'] in [2., 3.]],
                paired_endpoint=endpoint_fixed(summary, keep, eligible),
                paired_endpoint_fixed_posterior_cohort=endpoint_fixed(summary, keep, fixed), decisions=decisions)


def score():
    freeze = freeze_ready()
    # This is the only learned adapter function that opens realized arrays.
    from acd_stage19_score import score_actual
    actual, factual = score_actual()
    stage2 = json.loads((ROOT / 'receipts/acd_stage2.json').read_text())
    jbar = stage2['null']['jbar']
    null = np.asarray(stage2['null']['question_probabilities'])[np.r_[np.arange(8), 37]]
    with np.load(OUT / 'reused/runs/stage6/null_block.npz') as data:
        null_j = data['J'].copy()
    sd = (null_j[:, :8]-null_j[:, 8, None]).std(0, ddof=1)
    with np.load(OUT / 'reused/runs/stage4b_null/states.npz') as data:
        climate = data['states'].mean(0)
    inputs = {name: model_inputs(name, jbar, null) for name in MODELS}
    posterior = inputs['posterior'][3]
    fixed = posterior['observation'][:, :8, 0] & posterior['confident'][:, 8, 0, None]
    results = {name: metrics(name, *inputs[name], actual, factual, jbar, climate, sd, fixed) for name in MODELS}
    truth = actual[:, :8, 3] < actual[:, 8, None, 3]
    contrasts = []
    contributing = []
    for c in range(len(actual)):
        fractions = []
        for name in ['CNN-F', 'CNN-noF']:
            summary = inputs[name][3]
            conf = summary['confident'][c, 1:8, 3]
            wrong = summary['modal'][c, 1:8, 3] != truth[c, 1:8]
            fractions.append(float(wrong[conf].mean()) if conf.any() else None)
        if all(value is not None for value in fractions):
            contrasts.append(fractions[1]-fractions[0])
            contributing.append(c)
    interval = difference_interval(contrasts)
    L1 = dict(interval=interval, cases=len(contrasts), case_indices=contributing,
              confirmed=bool(not interval['empty'] and not interval['offset'] and interval['lower'] > 0))
    decision = next(r for r in results['CNN-noF']['decisions'] if r['lead'] == 3. and r['policy'] == 'C_delta_0')
    L2 = dict(actions_taken=decision['actions_taken'], harms=decision['harms'],
              conditional_harm_CP95=decision['conditional_harm_CP95'],
              confirmed=bool(decision['conditional_harm_CP95'][0] > .05))
    output = dict(freeze_b_commit=freeze['commit'], fresh_panel=True, models=results,
                  L1=L1, L2=L2, L3=dict(status='Pending Stage16 committed checkpoints'),
                  code_sha256=digest(Path(__file__)))
    (ROOT / 'receipts/acd_stage19_learned.json').write_text(json.dumps(output, indent=2, allow_nan=False)+'\n')
    print(json.dumps(dict(L1=L1, L2=L2), indent=2), flush=True)


if __name__ == '__main__':
    score()
