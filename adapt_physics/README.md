# Adapt the Physics, Not the Weights (stage 1)

Affiliation: Niva Platforms, Inc.

Stage-1 kill test: after an unannounced change in the Reynolds number of 2D Kolmogorov flow (with unmodeled linear
drag in the truth), compare identifying Re from a short observation window (then integrating) against adapting a
learned neural operator's weights or context. Protocol: `AP_FREEZE.md` / `ap_freeze.yaml`; gate report `AP_GATE.md`.
Numbers: `NUMBERS.md` (sections AP*). Reuses the Kolmogorov solver from `../tokens_horizon/th/`.

Order: `scripts/ap_drag_calibrate.py` → `scripts/ap_data.py chaos <Re>` → `ap_data.py train <set>` →
`scripts/ap_train.py <arm>` → `ap_data.py test <Re>` → `scripts/ap_eval.py <Re>` → `scripts/ap_analysis.py` →
figures → `scripts/make_numbers_ap.py`. Caches and weights (runs/cache, *.pt) are not committed.

License: Apache-2.0 (tokens_horizon/LICENSE).
