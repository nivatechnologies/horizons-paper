"""Synthetic audit of the WO's literal grid inversion, not of Aspen data."""
import hashlib
import json
import math
import platform
from pathlib import Path
import numpy as np
from statistics import interval, log_capital_max


def run():
    alpha = .01
    rows = []
    for value in [1., 0.]:
        x = np.full(200, value)
        lo, hi = interval(x, alpha)
        candidate = lo - .0001 if value == 1 else hi + .0001
        plus = math.exp(log_capital_max(x, candidate, 1))
        minus = math.exp(log_capital_max(x, candidate, -1))
        outside = not lo <= candidate <= hi
        rejected = max(.5 * plus, .5 * minus) >= 1 / alpha
        rows.append(dict(cases=200,constant=value,interval=[lo,hi],candidate=candidate,
                         plus_prefix_peak=plus,minus_prefix_peak=minus,
                         hedged_peak=max(.5*plus,.5*minus),threshold=1/alpha,
                         candidate_outside_interval=outside,
                         candidate_rejected_by_declared_capital_rule=rejected,
                         inversion_consistent=not outside or rejected))
    result = dict(host=platform.node(),source_class='synthetic hypotheses under test',
                  scope='literal grid inversion consistency; not an observed coverage-rate failure',
                  statistics_sha256=hashlib.sha256(Path('statistics.py').read_bytes()).hexdigest(),
                  rows=rows,passed=all(r['inversion_consistent'] for r in rows))
    Path('STATS_GRID_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    return result['passed']


if __name__ == '__main__':
    raise SystemExit(0 if run() else 2)
