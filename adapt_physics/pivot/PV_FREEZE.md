# PV freeze: Adapt the Physics pivot kill test

This freeze covers WO "Adapt the Physics, pivot kill test", issued 2026-09-26.

- **Order:** committed after step 0 (Codex: `5b6bdd1`, clarification `6f30a74`) and **before any pivot test data**.
- **Machine-readable:** `pv_freeze.yaml`. **Gate:** `PV_GATE.md`.
- **Conventions:** stage-1 conventions (`../AP_FREEZE.md`) apply unless overridden here.

## Thesis under test

Physics carries the extrapolation and the network carries the discrepancy. A no-drag physics model plus a learned
correction, trained only at nominal Re 40, should adapt to drift by identifying Re.

## Worlds

- **World D:** the stage-1 truth, with drag α = 0.0773.
- **World C:** World D plus the blinded Codex term, topographic β: −β_T·v on the right-hand side.
  - β_T = **1.469**, tuned from Codex's start of 3.35 to its clarified target, a 12.5% change in η̄ = ⟨ν|∇ω|²⟩.
    The achieved change is +12.2%.
  - World C is chaotic at Re 40: λ = 0.195 [0.193, 0.196].
- **Physics family:** in both worlds it omits drag and β.
- **Chaos gate:** every test Re (36, 40, 44, 50, 56) is chaotic in both worlds. Re 56 needed no replacement.

## Hybrid H

- **Form:** a continuous-time correction inside the right-hand side, since the solver is differentiable in torch:
  dω/dt = no-drag physics(ω; Re) + g_θ(ω).
- **g_θ:** a 2.37 M-parameter FNO (width 32, 12 modes, 4 layers). It has no Re input, and its output layer is
  zero-initialized.
- **Training data:** Re 40 truth only (102,400 states, the frozen FNO's data).
- **Training:**
  - Loss: 1-frame rollouts (35 IFRK4 steps) from noisy frames.
  - Optimizer: AdamW at learning rate 1e-3 with a cosine schedule, batch 64, 2,000 steps, float32.
  - Selection: the checkpoint with the lowest validation loss.
- **At test:** the stage-1 golden-section search on the hybrid, Re ∈ [25, 80], 30 evaluations. H then forecasts at
  the identified Re. H_true is a diagnostic.

## Arms

- **World D:** L_range, L0 and L0-big are the stage-1 models.
- **World C:** L_range and L0 are retrained with the stage-1 settings on World C data.
- **O, P1x:** the truth family (drag, plus β in C). O uses the true Re; P1x identifies Re on [25, 70].
- **P1:** the no-drag family, identified on [25, 70].
- **Persistence.**
- **L_ft:** dropped.

## Measurements

- **Settings:** stage-1 observation model, w ∈ {3, 6, 11, 23}, ε ∈ {0.1, 0.3}, W = 10 Lyapunov times of the test
  system, 300 states per Re.
- **Panels:** World D reuses the stage-1 panels at Re 36/40/44/50 and gets a new panel at Re 56. World C gets new
  panels for every Re.
- **Reported:** the restricted mean in Lyapunov and physical time, S(1), S(3), paired differences, retention
  (arm/O), the ratio to L_range, time to 90% of O, online cost and training cost (conditions and states).
- **Window-drift detector:** the slope of the identified Re against w, with a bootstrap interval. Reported only.

## Pre-committed outcomes

All at w = 11, ε = 0.1, 300 states. Precedence: **KILL → PASS → MIDDLE → otherwise.**

| Outcome | Conditions |
|---|---|
| **KILL** | H/L_range ≤ 1.0 at Re 50 or 56 in either world, **or** H/O < 0.70 at Re 50 in D |
| **PASS** | **World D:** H/O ≥ 0.85 at Re 36/44/50/56; H/L_range ≥ 1.5 at Re 36/50/56; H ≥ 0.95 max(L0, L0-big) at Re 40. **World C:** H/O ≥ 0.70 and H/L_range ≥ 1.2 at Re 50/56 |
| **MIDDLE** | H/L_range ≥ 1.3 at Re 50 and 56 in both worlds. Publishable, with no retest. |
| Otherwise | Todd decides |

## Cut order

Cut w = 3 and 23 first, then ε = 0.3, then L0-big, then Re 36.
