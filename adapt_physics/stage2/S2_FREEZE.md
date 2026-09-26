# S2 freeze: Adapt the Physics, stage 2 (confirmation and robustness)

- **Order:** committed **before any fresh test panel**.
- **Scope:** arms and settings are identical to the pivot freeze (`pivot/PV_FREEZE.md`) unless stated here.
- **Machine-readable:** `s2_freeze.yaml`. **Gate:** `S2_GATE.md`.

## Part A: confirmation (outcome frozen)

- **Panels:** 300 fresh trajectories per test Re (36, 40, 44, 50, 56) in each world, from never-used streams: the
  pivot stream + 20.
- **Seeds:** H, L_range and L0 each have seeds 0, 1 and 2 per world. Seed 0 is the pivot model; seeds 1 and 2 are
  trained identically. L0-big is seed 0, World D only.
- **Windows:** w ∈ {3, 6, 11}. **Tolerance:** ε ∈ {0.1, 0.3}.
- **Estimator:**
  - Point value: the per-state mean over seeds, then the mean over states.
  - Bootstrap: resample trajectories, then resample seeds within each trajectory (2,000 reps, seed 777).
  - The same bootstrap gives the intervals for ratios and paired differences.
- **Criteria:** the pivot's KILL, PASS and MIDDLE, **unchanged**, in the order KILL → PASS → MIDDLE → otherwise, at
  w = 11 and ε = 0.1.
- **Reported:** the outcome, each criterion's value with its 95% interval, the per-seed values, and the screening
  values beside them.

## Part B: robustness (reported, not criteria)

1. **L_range-wide:** trained on Re from 30 to 60 in both worlds, one seed, with L_range's settings. Evaluated at
   every Re.
2. **Windows straddling the change:** 11-frame windows starting 3, 6 or 9 frames before t_c, at Re 44 and 50 in
   both worlds. Arms: H seed 0 and L_range seed 0.
3. **Two-parameter drift in World D:**
   - Cases: Re 44 with amplitude ×1.1, and Re 50 with amplitude ×0.9.
   - H identifies (Re, A) by a fixed Nelder–Mead: start (40, 1), steps (+5, +0.1), 60 evaluations.
   - H_Re_only is a diagnostic. O and L_range (not retrained) are the comparators.
4. **5% noise** at Re 44 and 50 in both worlds. Arms: O, H seed 0 and L_range seed 0.
5. **Recovery:** w = 3, 6 and 11 for every arm.
6. **Scoring convention:** from t = 0, and at ε = 0.3, for the part-A cell.
7. **Detector:** the identified-Re slope for H and P1. In World C, the per-state correlation of H's slope with its
   oracle shortfall.

## Cut order

Cut in this order: L0-big extra seeds, item 4, item 6, item 2 at 9 frames, then item 3's Re 50 case.

Never cut: part A, item 1, or item 3 at Re 44.
