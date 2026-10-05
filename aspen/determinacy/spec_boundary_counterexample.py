"""Synthetic spec audit only. No Aspen data, samplers, or scientific kernels."""
import json
import math


def audit():
    # IID case summaries: (observation-confident S, correct S).
    rows = [(0, 0, 0.85), (1, 1, 0.10), (8, 8, 0.043), (8, 0, 0.007)]
    accuracy = sum(n * p for _, n, p in rows) / sum(d * p for d, _, p in rows)
    # Exact multinomial probability of no error and both R0 count floors.
    # Every percentile case-bootstrap replicate of such a panel equals one.
    terms = []
    for eight in range(201):
        for one in range(201 - eight):
            zero = 200 - eight - one
            if eight + one < 30 or 8 * eight + one < 100:
                continue
            lp = (math.lgamma(201) - math.lgamma(eight + 1)
                  - math.lgamma(one + 1) - math.lgamma(zero + 1)
                  + eight * math.log(0.043) + one * math.log(0.10)
                  + zero * math.log(0.85))
            terms.append(math.exp(lp))
    # On the event there are at most 170 zero-denominator cases. Even if
    # any empty replicate invalidates the entire bound, subtract this union
    # bound for 10,000 replicates; the false-PASS probability still exceeds .05.
    empty_replicate_bound = 10000 * (170 / 200) ** 200
    false_pass_lower = math.fsum(terms) - empty_replicate_bound
    return {
        "source_class": "synthetic hypothesis under test; exact mathematical counterexample",
        "case_rows_denominator_numerator_probability": rows,
        "n_cases": 200,
        "population_ratio_of_expectations": accuracy,
        "true_accuracy_below_R0_threshold": accuracy < 0.90,
        "no_error_evaluable_false_PASS_probability": math.fsum(terms),
        "one_sided_nominal_error": 0.05,
        "bootstrap_lower_bound_on_this_event": 1.0,
        "bootstrap_replicates": 10000,
        "bootstrap_argument": "Every nonempty resample has numerator=denominator, so all defined quantiles are 1.",
        "empty_replicate_union_bound": empty_replicate_bound,
        "false_PASS_probability_lower_even_if_any_empty_replicate_blocks_PASS": false_pass_lower,
        "max_one_sided_coverage": 1 - false_pass_lower,
        "simple_boundary_probability_at_r095_n30": 0.95 ** 30,
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2))
