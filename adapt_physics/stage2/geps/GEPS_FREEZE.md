# GEPS freeze

- **Frozen file:** `geps_freeze.yaml` in this directory. It is committed before any test-panel evaluation.
- **Gate:** `GEPS_GATE.md`, with the scope change by Todd's ruling (2026-09-28).
- **Scope:** the first **N = 50** states of the fresh World D panels at Re 50 and Re 56, GEPS-range, with 500 and
  5,000 adaptation steps; no-adaptation at Re 50; batch-1 timing on s2_test_Re50_D.
- **Reading:** H − GEPS-range (better budget per Re) ≥ 0.25 with the 95% interval excluding 0, at Re 50 **and** 56.
- **Deviations:** GEPS-wide is trained at lr 1e-3 (the published 1e-2 diverged), and its evaluation is cut. GEPS-range collapsed to persistence at the published lr 1e-2 (a finding; archived, never evaluated) and is retrained at lr 1e-3 for about an hour, validated every 2 epochs. Euler
  integration follows the released code (the paper says RK4). See the freeze for the rest.
- **Code:** `geps_run.py`, `geps_fast.py`.
