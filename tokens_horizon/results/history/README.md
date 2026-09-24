# Task 2.6: history reference (context sweep, timing jitter, observation noise)

System lorenz28, k-means tokenizers at 4 and 6 bits (cached codebooks), 300 states (the first 300 of the dt = 0.005
confirmation panel, panel sha `22f6ea508a54c49f`). Integration dt = 0.005 everywhere (truth, particle propagation,
jitter substep, forecast), per `freeze.yaml: pins.delta_035` and `pins.history_sweep`.

## Files
- `history.json`: `meta`, `rows` (one per method x bits x Delta x tau x variant x particles), `paired_vs_clean`.
- `history.csv`: the same rows (without `obs_info`).
- `../../runs/history/*.npz`: per-state arrays (posterior mean and spread, tokens, t = 0 error, horizons for all six
  scores, crossing flags, seeds). `refs_b*_D*.npz`: output-support bound and decode-and-integrate on the same states.
- `../../figures/F6_history.{svg,png,csv}`: Figure F6.
- Scripts: `scripts/t2_history.py` (re-runnable, skip-if-done per setting), `scripts/fig_F6.py`.

## Labels
- `reference`: particle-filter history reference; decode-and-integrate.
- `reference (unreliable)`: particle-filter reference whose fallback rate exceeded 5% at 1,500 and again at 3,000
  particles (frozen stop rule, FREEZE 2.5).
- `bound`: output-support bound.
- `estimate`: paired differences (perturbed minus clean) with bootstrap intervals.

## Columns
Every score `eps{0.3,0.1,0.5}_{future,from_t0}` has `_mean` (restricted mean of lambda*VPT, W = 27), `_lo95`/`_hi95`
(bootstrap over states, 2,000 reps, seed 777) and `_no_cross`. Primary is `eps0.3_future`.
`err0_rms_rel` = RMS over states of ||posterior mean - x(0)|| / sigma_A, with bootstrap 95% interval; `err0_median_rel`
and `frac_err0_gt_0p3` are given beside it. `fallback_rate` = fallback events / (states x filter steps).
`canonical` marks the row used for a setting (the 3,000-particle row when a rerun exists). `sha` = `config.git_sha()`.

## Protocol details fixed by this script
- Context: L = round(tau / Delta) frames before t = 0. tau = 0: particles are 1,500 calibration members of the current
  cell, no propagation; estimate = their mean.
- Filter: `th.pf.particle_filter` unchanged, `dt = 0.005`, `sub = Delta / 0.005`, 48 workers, `chunk = 7`
  (300 states -> 43 jobs). The process was pinned to 48 cores (`taskset -c 80-127`).
- Seeds: pf seed = first 8 bytes of sha256(`t2_history|pf|lorenz28|Delta|tau|bits|variant|M`) mod 2^63; the
  jitter/noise draw seed = sha256(`t2_history|draw|lorenz28|Delta|tau|variant`), shared by both rates so 4 and 6 bits see
  the same physical perturbation. Both are stored per row and per npz.
- Jitter: u_k ~ U(-Delta/4, Delta/4) i.i.d. per frame and state, including t = 0; grid state at or before t_k + u_k
  plus one RK4 substep of the remainder (`th.systems.rk4` with array dt). The filter assumes t_k.
- Noise: N(0, (0.02 sigma_A)^2) per coordinate on every observed state, including t = 0, before tokenization.
- Scoring for all variants is against the true, unperturbed trajectory (x(0) true at t = 0).
- Bound and decode-and-integrate are computed once per (bits, Delta) on clean tokens.

## Stop condition
Clean sweep: fallback rate at most 1.8% in every setting (60 settings); no rerun. Jitter: every setting exceeded 5% at
1,500 and at 3,000 particles (rates 5.9% to 40%) and is labelled unreliable. Noise: 4 bits Delta = 0.1 stayed below 5%
at 1,500 (4.0%); 4 bits Delta = 0.07 went 5.4% -> 3.9% at 3,000; the other eight noise settings stayed above 5% at
3,000 (6.3% to 27%) and are labelled unreliable.

## Note on the t = 0 error
The RMS posterior-mean error at t = 0 is not monotone in tau for clean tokens (e.g. 4 bits, Delta = 0.02: 0.017 at
tau = 1.6, 0.055 at 3.2, 0.155 at 6.4), while the median keeps falling (0.0079, 0.0061, 0.0058). The RMS is driven by a
few states whose filter estimate is far from the truth (err0 > 0.3 sigma_A in 0%, 0.7%, 1.7% of states). This is an
approximation property of the finite-particle filter at long contexts, reported as measured; no library change was made.
