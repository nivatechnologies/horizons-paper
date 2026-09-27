# OBJ freeze: objections and edge timing

- **Order:** committed after stage-2 part B was complete and exported, and **before any World V data and any Part 2
  evaluation**.
- **Scope:** arms and settings are identical to stage-2 part A unless stated here.
- **Machine-readable:** `obj_freeze.yaml`. **Gate:** `OBJ_GATE.md`.

## Part 1: drag that drifts with viscosity (World V)

- **World V:** α(Re) = α₀·40/Re (α₀ = 0.0773; 0.0619 at Re 50).
  - Physical basis: bottom-friction drag is proportional to ν, so it drifts when the viscosity drifts (the WO's
    hypothesis).
  - World V equals World D at Re 40, so the nominal data, H (3 seeds), L0 and L0-big are reused.
- **Chaos gate:** Re 50 in World V.
- **Panel:** 300 fresh trajectories at Re 50 (stream 40).
- **Arms:**
  - H, the World D correction with seeds 0–2, not retrained.
  - H + true Re.
  - O_V.
  - L_range_V: the L_range recipe on World V data; seed 0, plus 1 and 2 if time allows.
  - L0, reused.
  - P1x_V.
- **Readings** (reported, not criteria):
  - **holds:** H/O ≥ 0.85 and H/L_range_V ≥ 1.5.
  - **degrades, still leads:** holds fails, but H/L_range_V ≥ 1.2.
  - **loses its lead:** H/L_range_V < 1.2.
  - **Detector flags** if the 95% interval of H's slope excludes 0. This reading has no effect-size floor (see the
    gate).

## Part 2: the network given the parameter (FNO-Re)

- **Arm:** L_param (stage 1), not retrained. Seeds 1 and 2 are trained with the stage-1 recipe. L_param_C is seed 0
  and is cut first.
- **FNO-Re + true Re** runs at w = 11.
- **FNO-Re + identified Re:**
  - Search: the same golden-section as H, Re ∈ [25, 80], 30 evaluations.
  - Misfit: the network's autoregressive rollout against the window frames.
  - For w ≥ 5: the inputs are frames 1..4, and frames 5..w are scored.
  - For w = 3: the inputs are frames −2..1, and frames 2..3 are scored.
  - Windows: w ∈ {3, 6, 11, 23}.
- **Reading (decides the claim):** the claim "A network given the parameter does not extrapolate" is stated if, at
  Re 50 **and** 56 in World D, H − (FNO-Re + true Re) ≥ 0.25 with the 95% interval above 0. Otherwise the claim is
  removed.
- **L_ft (stage-1 procedure):** fresh World D panels at Re 44, 50 and 56, all 300 states, w = 11. Reported only.

## Part 3: edge timing (reported only)

- **Hardware:** Orin NX (JetPack 7.2.1, CUDA 13.2, torch 2.11.0, MAXN, jetson_clocks off).
- **Settings:** the same code, weights and settings as the datacenter; batch 1, no TensorRT.
- **States:** 20 timed states (states 3–22) of the World D Re 50 fresh panel.
- **Arms:** H (identification and forecast), H + true Re, O, L0, L_range, L0-big, FNO-Re + identified Re, and L_ft.
- **Measurements:** wall time median and p90, frames per second, memory, and VDD_IN power and energy.
- **Comparison:** the same harness at batch 1 on a Baccus GPU, plus the horizon agreement.

## Cut order

Cut in this order:
1. Part 2 World C.
2. L_range_V seeds 1 and 2.
3. L_param seeds 1 and 2.
4. ε = 0.3.
5. P1x_V.
6. L_ft at Re 56.
7. The w = 3 and 23 identification runs.

Within Part 3, cut L0-big first, then L_ft, then FNO-Re.
