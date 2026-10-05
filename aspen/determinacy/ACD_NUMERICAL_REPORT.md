# ACD numerical report — v2.3

Stage 0 completed on sulaco CPU, float64. Only hard stops H1–H3 govern continuation.

| Check | Result |
|---|---|
| Joint adjoint, all 41 components, centered eps=1e-6 | max absolute error 1.68569741499e-10 <1e-6 |
| JAX RK4 over 11 frames | relative discrepancy 5.42612451922e-16 <1e-12 |
| Gaussian sampler | PASS=True; mean 1.906 MC SE, variance 3.165 MC SE; extreme-direction variance ratios [1.0347592897856717, 0.9817957244623462] |
| dt versus dt/2 | PASS=True; ≤3 LT max draw-answer change 0.0000160; max classification change 0.0000000 |
| Climatology | 4096 independently seeded F=8 states; Jbar=9.361002091; 2.21s |

| Benchmark, including compilation/forecast/diagnostics | Seconds |
|---|---|
| Ordinary case | 42.301 |
| Four-site Q refit | 41.373 |
| All-site A refit | 69.713 |

Initial serial 8-core projection: 1.2 × (400 ordinary +1200 four-site +300 all-site) = **29.161 hours**. This includes a 20% rerun allowance and counts first-compilation cost conservatively for every run. Benchmarks used development case199/dtcheck case0; no confirmation input.

**R-time fired.** Apply cuts in order: R7, R5-A, R6-3LT, RML-conf, P/B-other-leads, R5-3LT. R5 population cap=60; warmup=1000; draws=500 per chain. The serial projection after the population cut is 15.570h, before the final draw reduction. The final settings continue as §14 directs, even if a serial projection remains over budget. Stage1 runs independent cases in parallel on reserved CPU affinities; no GPU use.

dt remains .01. No R-grad, R-impl or R-dt fallback fired. The Stage0 benchmark development case is resampled at the production draw count before Stage1 scoring.

IDs and sub roles are fixed in acd_protocol.py. The complete planned leaf uniqueness assertion covers 147464 leaves; no overlap with inherited IDs. Full records: `receipts/acd_numerical.json`, `runs/null/null.npz`, `runs/acd_access.jsonl`, and `runs/resolutions.jsonl`.

```json
{
  "count": 147464,
  "ids": {
    "acd-observation-conf": 1200000,
    "acd-posterior-dev": 1200001,
    "acd-posterior-conf": 1200002,
    "acd-sampler-dev": 1200003,
    "acd-sampler-conf": 1200004,
    "acd-crude-dev": 1200005,
    "acd-crude-conf": 1200006,
    "acd-climatology": 1200007,
    "acd-measure-dev": 1200008,
    "acd-measure-conf": 1200009,
    "acd-dtcheck": 1200010,
    "acd-bootstrap": 1200011,
    "acd-twoscale": 1200012
  },
  "sub_roles": {
    "history": {
      "initial": 0,
      "noise": 1
    },
    "rml": 0,
    "crude": 0,
    "posterior": {
      "primary": 0,
      "diag": 1,
      "stage1a": 2,
      "refit": [
        10,
        11,
        12,
        13,
        14
      ],
      "refit_rerun": [
        20,
        21,
        22,
        23,
        24
      ]
    },
    "measure": {
      "noise": 0,
      "random_sites": 1
    },
    "dtcheck": {
      "rml": 2,
      "crude": 3,
      "posterior": 4,
      "implementation": 5,
      "diag": 6
    },
    "null": 0,
    "bootstrap": {
      "R0_answer": 0,
      "R1": 1,
      "R1m": 2,
      "R2c": 3,
      "R3": 4,
      "R3b": 5,
      "R6": 6,
      "coverage": 7
    }
  }
}
```
