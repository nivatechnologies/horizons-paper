## Adapt the Physics, stage 1: session review (2026-09-26)

Branch `paper/adapt-physics-2026-09`, created from `paper/tokens-horizon-2026-09`. All work is under
`adapt_physics/` and reuses the Kolmogorov solver in `tokens_horizon/th/`.

### Spec errors found in the WO

The full list is in the gate report, `adapt_physics/AP_GATE.md`.

1. **The Lorenz-63 mechanism part is unspecified** (gate check 3): no arms, no adaptation procedure, no score. It was
   not executed; it is also first in the cut order.
2. **"Unannounced" change against a window counted from t_c.** Pinned: t_c falls uniformly inside the interval after
   frame 0. The identification arms and L_ft use frames 1..w. The context arms use their last n_in observations.
3. **The kill rule's panel is unpinned.** L_ft runs on 100 states and the other arms on 300. Pinned: the kill rule
   uses the first 100 states. The 300-state ratios are reported beside it.
4. **L_ft "one-step pairs inside the window".** With a 4-frame input this gives no pairs at w = 3. Pinned: the pairs
   whose target lies in the window.
5. **Window lengths in Lyapunov times are wrong for the drag world.** The WO's "0.125, 0.25, 0.5 and 1 Lyapunov
   time" assumes the no-drag λ of 0.127. With the calibrated drag, λ(Re 40) = 0.168, so w = 3, 6, 11 and 23 frames
   are 0.18, 0.35, 0.65 and 1.35 Lyapunov times. At Re 44 (λ 0.220), w = 11 is 0.85 Lyapunov times. The frame counts
   were kept as the WO fixed them.
6. **Details the WO left open, all pinned in the freeze before any test data:**
   - the definitions of the drag share and the noise scale;
   - L_param's number of input frames;
   - the FNO data sizes, budgets, optimizer and input-noise augmentation;
   - the identification objective and its estimate;
   - the "time to 90% of oracle" grid;
   - the referent of the flag.
7. **The kill rule has no uncertainty term.** It was applied as written, and paired intervals are reported beside it.
8. **Selector separation (check 9) is not satisfied.** The arms, drift sizes, windows and architectures were
   authored by the WO author and revised by an external review; there is no competing selector. Results are
   labelled selector-dependent.

### Process

- **Order:**
  1. drag calibration and the chaos gate (calibration and Lyapunov blocks only);
  2. a 300-step timing pilot, written to scratch;
  3. the freeze, `7ae83af`;
  4. then the test panels, training and evaluation.
- **Executor fixes before any affected result:**
  - The JSON updates of the data jobs and the eval jobs were made locked read-modify-write. Without that, concurrent
    processes on the same file would drop each other's entries. No written entry was lost; the chaos-gate file was
    checked and holds all five Re.
  - The analysis's reading function reads the frozen margins from the freeze.
- **GPUs:** the Qwen vLLM services were stopped for the GPU work (approved in the WO) and restarted at the end.
