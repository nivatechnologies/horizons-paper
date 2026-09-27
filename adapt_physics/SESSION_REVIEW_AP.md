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
  - The analysis's reading function hard-codes the frozen margins (0.25 and 0.10), the same values as `ap_freeze.yaml`.
- **GPUs:** the Qwen vLLM services were stopped for the GPU work (approved in the WO) and restarted at the end.

## Pivot kill test (physics plus learned correction): session review (2026-09-26)

### Order

1. Step 0, blinded Codex: answer committed in `5b6bdd1`.
   - The first invocation hung waiting on stdin and was killed.
   - The rerun was killed by the executor's own `pkill -f`, which matched its own shell.
   - The third run completed. The single clarifying question and its answer are in `6f30a74`.
   - Codex had no repository access; the event logs show web search only.
2. β calibration and the chaos gates.
3. Freeze, `49d060f`, before any pivot test data. H_D training began shortly before the freeze, on training data
   only, with the settings committed unchanged. This is recorded in the freeze.
4. Test panels, training and evaluation.

### Spec errors found in the WO

The full list is in `pivot/PV_GATE.md`.

1. **The outcome categories overlap.** A KILL input can also meet MIDDLE, and the WO gives no precedence. Pinned:
   KILL → PASS → MIDDLE → otherwise.
2. **The World D thresholds are not independent (check 2).** They were written after the stage-1 values of O,
   L_range, L0 and L0-big on the same panels were known. Only H was new information in World D. World C and Re 56
   were fresh.
3. **Codex's clarified starting magnitude overshoots.** β_T = 3.35 changes η̄ by +39.8%. It was tuned with the same
   sign to Codex's own target, reaching β_T = 1.469 and +12.2%. η̄(β) is not monotone: β = 1.05 gives −6.5%.
4. **"Training conditions" is unpinned.** Pinned as distinct Re values plus training states.
5. **The search range differs between arms.** It is [25, 80] for H and [25, 70] for P1 and P1x, kept for continuity
   with stage 1.
6. **The hybrid budget was the executor's choice.** It was set by a timing pilot on training data (launch-bound:
   2.2 s per step at batch 64), not by the WO.

### Executor slips

- The `pkill -f` self-kill during step 0. It cost one Codex rerun and affected no result. The memory note has been
  updated.
- An unquoted heredoc in the generator that wrote `CODEX_MISMATCH.md` let bash substitute backticks in the
  Invocation lines. It was fixed in `6a2d298`. The prompt and answer were verified verbatim.
- A placeholder wait on a file that would never exist was launched by mistake and killed within a minute.
- The World D Re 56 chaos job wrote its entry into the committed stage-1 `results/chaos_gate.json`. The entry was
  moved to `pivot/results/chaos_gate_D.json`, and the stage-1 file was restored unchanged.

### Scope

- One seed per model, on a 300-trajectory screening panel.
- The mismatch terms are drag (from stage 1) and one Codex term.
- Check 9 is satisfied only for the mismatch selector. The thresholds and arms are selector-dependent.

## Stage 2 (confirmation and robustness): session review (2026-09-27)

### Order

1. Freeze `89c9bc9`, before any fresh panel.
2. Part A final at `d79a5f6` / `150a5e1`: **PASS confirmed** on fresh panels with 3 seeds.
3. Part B final at `2b566a9` / `2f539db`.
4. The paper-facts note and the NUMBERS export were generated from the repository after Part A and again after Part B.

### Spec errors found in the WO

The full list is in `stage2/S2_GATE.md`.

1. **Estimator and intervals unpinned.**
   - The seed-pooled estimator, "seeds resampled within each trajectory" and "every criterion's value with its
     interval" had no pinned estimator.
   - Pinned: a per-state mean over seeds, then a bootstrap over trajectories with seeds resampled within each; ratio
     intervals under the same resampling.
2. **The PASS Re-40 criterion mixes seed counts.** It compares seed-pooled L0 with single-seed L0-big. Applied as
   written.
3. **Part B left most settings unpinned.** Seeds, Re values, arms and the Nelder–Mead details were pinned before any
   result.
4. **w = 23 is not named for the fresh panels.** It was not repeated there because of cost, so the detector slope
   uses 3 points.
5. **Check 9 is not satisfied for part B's selectors.** Part B is labelled selector-dependent.

### Executor slips (none changed a result)

- **Wrong model path.** A model-path bug made three World D hybrid jobs fail to load. It was fixed and the jobs
  re-queued.
- **Dependency race.** A two-parameter panel started before its chaos entry existed, and was re-queued.
- **Worker lifetime.** The queue workers had a hard 8 h lifetime, which stalled the queue for about 1.5 h before it
  was noticed. They were relaunched with a 20 h lifetime.
- **Job priority.** Training jobs outranked evaluations in the queue file. It was re-prioritized under the queue
  lock.

### Result the paper must carry

- **Item 2: windows straddling the change.** H has no change detector. When its 11-frame window starts 3–9 frames
  before the change, H falls below L_range at Re 44 and Re 50 in both worlds.
  - World D, Re 50: H 0.51–1.27 against L_range 1.00–1.69.
  - This is a real limitation of the method as tested.

## Objections and edge timing: session review (2026-09-27)

### Order

1. Started after stage-2 part B was complete and exported.
2. Freeze `1871700`, before any World V data and any Part 2 evaluation.
3. The Orin NX timing was run by a subagent. The datacenter comparison used the same harness at batch 1 on a Baccus
   GPU.

### Spec errors found in the WO

The full list is in `stage2/objections/OBJ_GATE.md`.

1. **The detector reading has no effect-size floor.** It is nearly degenerate: with 900 seed-state estimates, a
   negligible slope excludes zero. Applied as written, with the magnitude reported. In World V the slope (+0.059 per
   frame, a +2.5 bias in Re) is large regardless.
2. **The Part 3 datacenter comparison was unpinned.** Pinned: the same harness at batch 1.
3. **"Same code, FP32" conflicts with the datacenter settings,** where the oracle runs in float64. The datacenter
   settings were kept.
4. **The Orin torch build.** No torch wheel is built for compute capability 8.7 on JetPack 7. NVIDIA's torch 2.11.0
   SBSA wheel runs sm_80 kernels by binary compatibility; numerics were checked to machine precision. The datacenter
   runs torch 2.13.0.
5. **jetson_clocks** could not be enabled without sudo (power mode MAXN).
6. **The FNO-Re identification procedure** was pinned in the freeze (inputs, scored frames, the short-window rule),
   as the WO requires.

### Executor slips (none changed a result)

- The objections results directory did not exist yet for the first Part 2 evaluations. Three crashed on writing
  their metadata; they were re-run and the crashed outputs set aside.
- The Orin subagent ran `tegrastats` for about 3 s during the H arm to confirm the job was alive. There were 60,782
  power samples in that arm.

### Qwen services

Kept stopped from stage 2 through this WO, as it requires, and restarted at its end.
