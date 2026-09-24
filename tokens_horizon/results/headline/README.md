# Headline bound and references (Task 2.2), lorenz28

Produced by `scripts/t2_headline.py all` (per-state arrays in `runs/headline/<setting>.npz`,
setting = `lorenz28_b<bits>_D<Delta>_dt<dt>_M<particles>`). One row per (bits, Delta, dt, particles).
`headline.json` holds the same rows plus metadata; in `headline.csv` intervals are JSON lists `[lo, hi]`.

## Labels
- `bound_*`: **bound** (output-support bound, d_C(x_j)/sigma_A on the true future).
- `DI_*` (decode-and-integrate), `PF_*` (particle-filter history reference): **reference**.
  `history_ref_label` is `reference` or `unreliable` (fallback rate > 5% at 1,500 and at 3,000 particles).
- `persistence_*`, `climatology_*`: **reference (null)**.
- every `_ci95`, `_ci90`, `diff_*`, `outlast_*`, `ties_*`, `p0_*`, `sens_*`, `halving_*`: **estimate**.

## Columns
- `bits, delta, dt, particles, n_states` (1,000), `n_hist` (300, first 300 states of the panel).
- `pf_seed` (deterministic from bits, Delta, M, dt), `pf_context_frames` (round(3.2/Delta)),
  `pf_fallback_events`, `pf_steps` (n_hist x context frames), `pf_fallback_rate`, `stop_condition`.
- `labels_vs_encode_mismatch`: share of calibration states whose stored k-means label differs from the
  exact nearest prototype (the particle-filter init pool uses the stored labels).
- `p0_eps<e>`: share of states with d_C(x_0)/sigma_A > e (1,000 states); `_hist` on the first 300.
- `<q>_eps<e>_<score>{,_hist}_mean | _ci95 | _nocross`: restricted mean E[min(lambda T, W)], W = 27, its
  bootstrap 95% interval (2,000 reps, seed 777, states resampled), non-crossing fraction.
  `q` in {bound, DI, persistence, climatology, PF}; `score` = `future` (primary, frames j >= 1) or
  `from_t0` (secondary); eps in {0.3 primary, 0.1, 0.5}. No suffix = 1,000 states (PF: 300);
  `_hist` = first 300 states.
- `outlast_PF_vs_bound_*`, `ties_PF_vs_bound_*`: per-state share with PF lambda T > bound lambda T
  strictly, and share tied (300 states). `outlast_DI_vs_bound_*` on 1,000 (and `_hist` on 300).
- `diff_<a>_minus_<b>_*` with `_ci90`, `_ci95`: paired bootstrap of the restricted-mean difference
  (PF_minus_bound and PF_minus_DI on 300 states; DI_minus_bound on 1,000).
- `sens_PF_M3000_minus_M1500_*` (+ `_ci95`): 3,000-particle rows only; paired difference vs the
  1,500-particle history reference at the same setting.
- `halving_<q>_minus_dt0.01_*` (+ `_ci95`): dt = 0.005 rows only; paired difference vs dt = 0.01 on the
  same burned-in starts. Per-state truths diverge between the two integrations, so per-state
  differences are not meaningful; the restricted means and their intervals are the comparison.
- `panel_sha`, `git_sha`.
