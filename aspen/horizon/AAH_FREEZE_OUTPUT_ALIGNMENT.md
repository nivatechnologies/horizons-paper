# Learned-output alignment and scoring detail — 2026-10-04

Recorded before any learned-arm test evaluation. No criterion, Niva T_f convention, training architecture, checkpoint selection or panel changes.

Learned models advance by the system's output interval (0.05 Lorenz;0.35 Kolmogorov). Their reported single-time forecasts use the nearest output tick to each nominal T. Generate an independent true scoring trajectory at exactly that tick, so a forecast is never compared against a different time. Record actual times and offsets. Criterion Niva snapshots continue at the nearest0.01 integrator tick as in the initial freeze. No interpolation of states or horizon readings.

Both learned and solver objective means use identical uniform output ticks inside closed[T,T+1 LT]. Neural predictions are scored as their full fields (no post-hoc denoising or projection). Kolmogorov objective coefficients are the benchmark's fixedRe40 and dragalpha for every arm; model dynamics still use its specified identified/misidentified parameters. This separates the specified objective from dynamics error. RFFT gradient-budget weights follow the existing solver. Lorenz objective remains half the spatial mean square.

Stability is checked through the first output tick reaching21LT. If a member is unstable under any action, remove it for all actions and every reported horizon. Decisions at budgetM use retained members among the firstM; >50% drops forces an incorrect decision, even if the surviving argmin matches truth. No surviving members gives no cost/forecast/response estimate; report unavailable. Attempted and retained counts are distinct and reported.

Wall-time profiling and batches may use available CPU cores; actual thread counts reported. CNN inference uses64CPU threads. Random null regret is averaged analytically over allKchoices; myopic uses the same64-member paired arm inputs and the prescribed[0,1 LT] window.

The Kolmogorov FNO retains the original L_range input scale64/sigma_A(Re40) from the prior chaos artifact. Observation noise uses the newly specified total-state RMSsigma, so its normalized augmentation is0.02*sigma/(sigma_A/64). This feature normalization does not change any physical observation or action field.
