# AP freeze: Adapt the Physics, stage-1 kill test

This freeze covers WO "Adapt the Physics kill test (stage 1)", issued 2026-09-26, under the contract
P_Paper-Adapt-The-Physics-2026-09.

It was committed **before any test-panel data or result**, and before any learned-arm training beyond a 300-step
timing pilot. The machine-readable version is `ap_freeze.yaml`; the gate report is `AP_GATE.md`.

## Question

After an unannounced change in Re, does identifying Re from a short observation window restore a chaotic-flow
forecast far better than adapting a learned model's weights or context? The comparison includes a larger model, and
it runs in a world with **model mismatch**: the truth has linear drag, and the physics family omits it.

## System

- **Kolmogorov flow:** n = 4, 64², IFRK4, dt 0.01, float64.
- **Truth drag:** α = **0.07733**. At Re 40 it carries 14.9% of enstrophy dissipation (target 15% ± 0.2%).
- **Chaos gate** (λ with drag, 95% interval over 64 starts; σ_A per test Re): the values are listed in
  `ap_freeze.yaml` → `chaos_gate.values`. **Re 36 is chaotic, so it is kept.**
- **Windows in Lyapunov times:** with drag, λ(Re 40) = 0.168, so w = 3, 6, 11 and 23 frames are 0.18, 0.35, 0.65
  and 1.35 Lyapunov times. The WO's "0.125, 0.25, 0.5 and 1" assumed the no-drag λ. The frame counts stay as the WO
  fixed them; the mapping is reported.

## Drift and observations

- **Drift:** burn-in at Re 40, then the switch to the test Re (36, 40, 44 or 50) at t_c, which falls uniformly
  inside the interval after frame 0.
- **Observations:** full-field vorticity every 0.35, with white noise of 2% σ_A(test) RMS.
- **Windows:** w ∈ {3, 6, 11, 23} frames after the change. The forecast starts from the last noisy frame.
- **Panel:** 300 independent trajectories per test Re.

## Arms

| Arm | Role | Definition |
|---|---|---|
| O | oracle | truth family (drag) and true Re |
| P0 | null | no-drag family at Re 40 |
| persistence | null | hold the last observation |
| **P1** | identification | no-drag family, Re from a 30-evaluation golden-section search on [25, 70] against the window misfit |
| P1x | diagnostic | as P1, with drag known |
| **L_param + P1** | identification (hybrid) | Re-conditioned FNO (Re ~ U[34, 46]) given P1's Re |
| L_param + true Re | diagnostic | the same FNO given the true Re |
| **L_range** | opponent | 8-frame history FNO trained on Re ~ U[34, 46]; adapts in context |
| **L_ft** | opponent | L0 fine-tuned on the w window pairs: 200 AdamW steps at learning rate 1e-4; first 100 states |
| **L0-big** | opponent | nominal FNO at width 156: 99.8 M parameters, 5.94× L0; 2× the steps |
| L0 | diagnostic | frozen nominal FNO, 4 frames, Re 40 |

**FNO:** 16 modes, width 64, 4 layers, residual output and coordinate channels. The loss is one-step MSE plus a
4-step unrolled rollout. Training: AdamW at learning rate 1e-3, cosine schedule, batch 32, input noise equal to the
observation noise, seed 0. Budgets: 30k steps, and 60k for L0-big. The checkpoint with the lowest validation loss is
kept. All learned arms train on the truth, drag included.

**Lorenz-63:** not executed. Gate check 3 failed (its arms and score are unspecified), and it is first in the cut
order.

## Scoring and readings

- **Tolerance:** ε ∈ {0.1 (primary), 0.3} × σ_A(test).
- **Window:** W = 10 Lyapunov times of the test system.
- **Horizon:** the restricted mean, in Lyapunov times and in physical time.
- **Reported alongside:** S(1), S(3), paired bootstrap differences over trajectories, and the online and training
  costs.
- **Frozen margins:**
  - well below: a difference of at least 0.25 with the 95% interval excluding 0;
  - approximately equal: the 90% interval within ±0.10.

## Kill rule

The cell is Re 44, ε 0.1 and w = 11, on the first 100 states (where every arm is present).

- I\* = max(P1, L_param + P1)
- A\* = max(L_range, L_ft, L0-big)

| Outcome | Condition |
|---|---|
| **Pass** | I\* ≥ 2 A\* at Re 44 **and** at Re 50 |
| **Kill** | A\* ≥ 0.75 I\* at Re 44 |
| In between | anything else; Todd decides |

**Flag:** raised if I\*/A\* at Re 40 is at least I\*/A\* at Re 44. It is reported prominently.

The 300-state ratios (A\* without L_ft) are reported beside the 100-state ones.

## Cut order

Lorenz-63 (already cut), then Re 36, then w = 3, then L0-big.
