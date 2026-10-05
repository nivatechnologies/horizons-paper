# AFD Step 0 — HALT before data

Governing work order: vault `02-Projects/WO_Aspen-Forecast-Decision-Kill-Test-2026-10-04.md`, v5.1, status go-v5.1; read in full through niva-obsidian MCP. Todd's execution go is present in §1. Local body snapshot: WO_v5.1.md. Read-only scientific source: `paper/aspen-2026-10-horizon` at `1cd0ab701b5e663eb7e0304b1d705ddeabe80617`. All source references below index that commit.

## Stop required by §3

Existing solver cost accumulation (`aspen/horizon/l96.py:45`) and CNN cost accumulation (`aspen/horizon/evaluate_l96_neural.py:51`) include only output ticks inside the **unrounded** interval. WO §4 instead rounds both endpoints to the nearest output time and includes both endpoints. This changes the scientific cost, action rankings, eligibility and regret.

At primary lead, existing code uses output indices **24–35**, while the WO uses **24–36**. The myopic window differs too: **0–11** versus **0–12**. Full lead comparison is in NUMBERS §AFD_WINDOWS; these are computed from the measured AAH LT, not estimated. No trajectories were generated to discover this mismatch.

WO §3: “Where code and this WO differ on anything that defines a scientific quantity (sampler, truth, eligibility, metrics, arm inputs, scoring), stop. Report it, and wait for a WO amendment before data.”

Required amendment: explicitly authorize replacing the inherited unrounded cost-window predicate with the §4 rounded, closed-endpoint rule in every AFD solver, learned rollout and myopic-null calculation. The AAH artifacts and results should remain historical. Differential prediction: leads whose output index sets already match stay unchanged in sample membership; mismatched windows gain or lose exactly the ticks recorded in AFD_WINDOWS. No claim is made that any scientific verdict will revive.

No freeze, timestep check, benchmark using newly generated states, panels, training, or Stage 2b sampler check has run. No AFD test output exists; the coordinator is the only actor and no training/selection worker has been launched.

## Verification items

### 1. CNN interface and base recipe — verified

Sources: `train_l96.py:9–20,23–68`, `learned_l96_data.py:12–46`, `evaluate_l96_neural.py:17–62`.

- Eleven historical state frames at output spacing 0.05; history covers 0.5 time units.
- States and the **physical forcing perturbation field** are divided by the measured spatial RMS sigma. Action is not an integer class embedding: it is a site-wise field, supplied as a twelfth convolutional input channel.
- Residual next-state forecast: last normalized frame plus convolutional output. Five circular Conv1d layers with channel sizes 12→256→256→256→256→1, kernels 5/5/5/5/1, GELU after the first four. Output advances one 0.05 tick.
- Checkpoint tensor count verifies **999,681** parameters; selected checkpoint is update **20,000**. Measurements and hashes: NUMBERS §AFD_STEP0 and §AFD_HASHES.
- AdamW, learning rate 1e-3, weight decay 1e-4, cosine annealing over the update count, gradient norm clip 1, effective batch 128, torch seed 0.
- Exact loss is four rollout-step MSEs weighted 1/4 each **plus an additional first-step MSE**. Do not silently replace this with an equally weighted four-step loss when reproducing the base recipe.
- Checkpoint selection every 1,000 updates by smallest independent validation one-LT rollout MSE; code rounds the one-LT step count. Base training inputs receive one iid noise layer, distinct from operational member windows' two noise layers.
- Retained training wall duration is **6943.836976528168 seconds**. Code trains CPU tensors/model and records thread count; it contains no CUDA transfer. There is no verified AAH training GPU-time or GPU-type record. The WO's missing-record budget fallback applies; the wall duration must not be relabelled GPU-hours.

### 2. AAH formulas and populations — verified; historical formulas retained

Sources: `analyze_l96.py:12–23,34–47,86–102`; `enrich_l96.py:29–70`.

ACC: anomalies a=forecast−action climatology, b=realized target−action climatology; dot(a,b)/sqrt(sum(a²)sum(b²)). Zero observed anomaly norm is unavailable; forecast squared norm below 1e-24 times observed squared norm scores zero. AAH reports point ACC, averaged across all cases/actions, not eligible-only.

AAH “response” here is **cost difference**, not MSRE or VRE. For each lead, flatten d(c,j,k)=mean(C_j)−mean(C_k) over all cases and pairs j>k. Correlation is Pearson corrcoef(d_arm,d_truth); relative error is norm(d_arm−d_truth)/norm(d_truth), unavailable for zero truth norm. This uses all cases, not only eligible cases. Historical solver differences use all stored arm members; learned differences use every surviving stored member. Operational accuracy uses the first member cohort specified for the reported budget. These historical statistics must not be substituted for the new WO's eligible-case state-response statistics.

The new WO explicitly requires both its eligible-case descriptive cost-pair metrics and the differing AAH all-case versions. New split-sample eligibility, panel-median regret normalization, decision-window skill and MSRE/VRE are new AFD quantities; historical AAH outputs are not fresh evidence.

### 3. Initial states — verified

Sources: `evaluate_l96.py:55–76`; `evaluate_l96_neural.py:34–62`. Physics receives the last frame of each perturbed member window. CNN receives the full member window and advances autoregressively. Realized true state is only a scoring target. The WO preserves this asymmetry.

### 4. LT — verified

`AAH_FREEZE_CALIBRATION_L96.md` and `results/l96_calibration.json`: LT **0.5928295944308761** time units, reciprocal of the retained mean exponent. Measured sigma **4.312600593723798**. Both are reproduced in NUMBERS; these are retained calibration measurements, not new AFD estimates.

### 5. Reuse — verified

- One `runs/l96/test/climatology.npy` contains all action climatology rows. SHA256 **4513b34ab1ab674bb7c5bf295906e38334ce938ebcb729b6bfa9d97467c7499e**. Metadata and source hashes are in NUMBERS §AFD_HASHES.
- `climatology_l96.py:28–35` runs each action after a 50-LT spin-up and averages for 500 LT, sampling every output tick; action amplitude is the retained calibration amplitude.
- F identifier: `evaluate_l96.py:10–30`; starts from the first observed frame, propagates through the observed history, minimizes summed spatial MSE over subsequent frames, golden-section [6,10], two initial and 28 subsequent objective evaluations, returns final interval midpoint.
- AAH myopic null: `profile_l96.py:17–33`; identified-F paired solver, first 64 operational member windows, cost on [0,1 LT]. Thus it is the predecessor of N-last, not the CNN or oracle. Its unrounded cost window is affected by the halt.

### 6. Seeds — verified

`common.py:13–23` uses hierarchical SeedSequence [namespace,system,substream,case,member,action] and default_rng (PCG64).

Namespace IDs are reproduced in NUMBERS §AFD_SEEDS: calibration, truth, arm, train, val, climatology, jitter, lyapunov and observation. Substreams in AAH_FREEZE: initial 0, observational 1, member 2, bootstrap 3, action 4, tangent 5; training minibatch/order substream 6 is also used by train_l96.py. Future AFD namespace IDs/leaf uniqueness have not been frozen or exercised.

### 7. Checkpoint, actions and observation sampler — verified

- CNN checkpoint SHA256 **3c67fc2cfc3a858613160cc81151c09ef45829f08bda67df00b9e78f35f5fe74**. Same digest measured on Baccus retained copy and sulaco retained copy. Climatology digest also matches across those machines.
- sulaco's task directory is a source/artifact copy without a .git directory; do not report a remote Git HEAD. The local pinned source and file hashes establish the inspected code provenance.
- `common.py:25–40`: action order is uniform −1; sqrt(2)cos(k theta) for k=1,2,4,8,10; alternating sites; compensated single-site reduction (1−40·indicator(i=0))/sqrt(39). theta=2pi i/40. Code renormalizes each to unit RMS. Measured RMS values are in NUMBERS §AFD_ACTIONS and equal unity to floating-point precision.
- `evaluate_l96.py:44–69`: true window plus iid site/frame Gaussian noise with SD 0.02 sigma, then fresh iid noise of the same SD for each member; paired actions share each member window. Truth and operational member streams are disjoint. Spatial **state RMS** is the noise reference, not anomaly SD or Euclidean anomaly norm.
- AAH independently spins up each initial random state for 500 time units; the new WO explicitly specifies 50 LT instead. Do not reuse old cases or trajectories. This is a specified new-panel recipe, not evidence from AAH.

## Provenance and status

NUMBERS sections AFD_STEP0, AFD_WINDOWS, AFD_HASHES, AFD_ACTIONS and AFD_SEEDS derive from step0_evidence.json. Run `/mnt/niva-array/horizons-paper/.venv/bin/python aspen/forecast_decision/preflight.py` from the AFD worktree. It rereads the source artifacts, recomputes tensor count, hashes, action RMS and window predicates, checks the rendered NUMBERS text and rejects a tampered parameter count. This checker covers preflight only; no campaign verdict checker is claimed.

Branch pushes are recorded in EXECUTION_STATUS.md.

