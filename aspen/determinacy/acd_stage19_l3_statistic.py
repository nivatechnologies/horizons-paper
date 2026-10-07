"""Freeze B L3 matched-seed aggregation; arrays enter only from scoring code."""
import numpy as np
from acd_stats import difference_interval


def pair_statistic(forcing_summary, history_summary, realized_signs, lead_index):
    """Exactly L1: within each case, each model uses its own confident answers."""
    masks = [s['confident'][:, 1:8, lead_index] for s in
             (forcing_summary, history_summary)]
    wrong = [s['modal'][:, 1:8, lead_index] != realized_signs[:, 1:8, lead_index]
             for s in (forcing_summary, history_summary)]
    sizes = [m.sum(1) for m in masks]
    defined = (sizes[0] > 0) & (sizes[1] > 0)
    errors = [np.divide((m & w).sum(1), n, out=np.zeros(len(n), dtype=float),
                        where=n > 0) for m, w, n in zip(masks, wrong, sizes)]
    differences = errors[1] - errors[0]
    values = differences[defined]
    return dict(case_differences=[float(v) if ok else None
                                 for v, ok in zip(differences, defined)],
                contributing_cases=int(defined.sum()),
                interval=difference_interval(values) if len(values) else None)


def aggregate_new_pairs(pairs, run_status):
    """Stored indices one through four only; any failed run blocks confirmation."""
    indices = tuple(range(1, 5))
    expected = {f'{model}-seed{i}' for i in indices
                for model in ('CNN-F', 'CNN-noF')}
    missing = sorted(expected - set(run_status))
    failed = sorted(name for name in expected & set(run_status)
                    if run_status[name].get('capped') or run_status[name].get('abort')
                    or not run_status[name].get('selected_sha256')
                    or run_status[name].get('failed', False))
    pair_intervals = {i: pairs[i]['interval'] for i in indices if i in pairs}
    positive = sum(row is not None and row['point'] > 0
                   for row in pair_intervals.values())
    evaluable = not missing and not failed and all(i in pairs for i in indices)
    result = dict(evaluable=evaluable, missing_runs=missing, failed_runs=failed,
                  positive_new_pair_count=int(positive), required_positive_pairs=3,
                  L3a=None, L3b=None, confirmed=None)
    if not evaluable:
        return result
    matrix = np.array([[np.nan if v is None else v
                        for v in pairs[i]['case_differences']] for i in indices])
    counts = np.isfinite(matrix).sum(0)
    contributing = counts > 0
    means = np.divide(np.nansum(matrix, axis=0), counts,
                      out=np.zeros(matrix.shape[1]), where=contributing)
    values = means[contributing]
    interval = difference_interval(values) if len(values) else None
    valid = interval is not None and not interval['empty'] and not interval['offset']
    result.update(contributing_cases=int(contributing.sum()),
                  defined_pairs_per_case=counts.tolist(),
                  case_mean_differences=[float(v) if ok else None
                                         for v, ok in zip(means, contributing)],
                  L3a=interval, L3b=positive >= 3,
                  confirmed=bool(valid and interval['lower'] > 0 and positive >= 3))
    return result
