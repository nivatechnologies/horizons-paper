# Check 9: blinded competing selector (second model)

Author: OpenAI Codex (via the codex-rescue agent), 2026-09-24. Blinded: it received only the research
question (no systems, rates, intervals, arms or margins from the WO) and was told not to read any file.
Prompt and verbatim answer below.

## Prompt (research question only)

When a continuous chaotic dynamical system is observed only through a discrete tokenizer (a finite
codebook / vector quantizer applied to the state at a fixed frame interval), how much forecast horizon
does each bit of token rate buy? Separate three costs of tokenization: (a) information the token discards
about the current state, (b) the limited resolution of a forecaster whose outputs must themselves be
codebook entries, and (c) what a trained sequence model fails to use from the token history. Test whether
a token history can support forecasts that its own output vocabulary cannot express. Test whether a simple
exchange law predicts horizon at held-out rates. [Then asked for systems, rates, intervals, horizon
definition, arms and controls incl. null, bounds, margins, held-out exchange-law test, one surprise.]

## Answer (verbatim)

1. Systems and parameters

Use Lorenz–63 (σ=10, ρ=28, β=8/3), Rössler (a=b=0.2, c=5.7), and 1-D Kuramoto–Sivashinsky (domain length 22, ν=1, 64-point dealiased spectral grid). They span a low-dimensional strange attractor, a second standard flow, and spatiotemporal chaos. Estimate each system's largest Lyapunov exponent λ and information dimension D₁ from training trajectories. Integrate at high precision, then sample at Δ/Tλ = 0.02, 0.05, 0.1, where Tλ=1/λ.

2. Token rates and intervals

Fit standardized Euclidean vector quantizers with K=2ʳ codewords at r=2, 4, 6, 8, 10 bits/frame. Train/evaluate at each of the three intervals. Hold out odd rates r=3, 5, 7, 9 from all model and exchange-law fitting. Report both bits/frame and bits/Tλ (rTλ/Δ); these are different rate comparisons.

3. Forecast horizon

For each forecast, calculate normalized full-state RMSE: sqrt(mean ||x̂−x||² / mean ||x−mean(x)||²), with means and scales fixed from training data. Horizon is the first crossing sustained for three sampled frames, in Lyapunov times. Report thresholds 0.2 and 0.4; censor at 5 Tλ and estimate median horizon with a survival estimator. Use 100 independent test trajectories per system, each at least 100 Tλ long.

4. Forecasters and controls

Compare: (i) exact-model integration from the true initial state, a forecastability ceiling; (ii) exact-model integration from the current token centroid, measuring sensitivity to discarded state detail; (iii) a large-data token-history analogue conditional-mean predictor, a non-learned recoverability reference; (iv) the same six-layer, 256-wide Transformer with either a continuous state-vector head or a categorical codeword head; and (v) persistence and climatological-mean nulls. Give each learned model a 2 Tλ token context and direct multi-step outputs to 5 Tλ. The paired Transformer heads isolate output-vocabulary cost; its gap to the analogue reference estimates model-use failure. Compare exact-state integration with the token-history reference, and z₀-only with history, to quantify lost information and history recovery.

5. Bounds and recoverability

For any codeword-valued point forecast, E[minⱼ||x−cⱼ||²] is a hard per-time-step distortion floor. Estimate it on test states. Shannon's rate-distortion converse gives a finite-rate lower bound on state distortion; the data-processing inequality bounds state information in a finite token history by its token entropy. These support distortion limits, but neither gives a universal horizon bound: future targets can be less state-sensitive than the full state. Test recoverability empirically against the token-history conditional-mean analogue. Takens' embedding theorem does not guarantee reconstruction from a finite-alphabet vector quantizer; finite symbolic partitions can require special generating-partition properties.

6. Statistical margins

Use paired trajectory-cluster bootstrap intervals (10,000 resamples), never individual frames as independent samples. Call horizons approximately equal if the 90% CI for the paired difference lies inside ±0.10 Tλ (TOST). Call an arm clearly below a reference if the 95% CI lies wholly below −0.25 Tλ; call it near if the 90% CI lies wholly inside ±0.25 Tλ. Apply the same margins to both thresholds.

7. Held-out exchange law

The rate-distortion/high-rate hypothesis is H(r)=α+(ln 2/D₁)r: squared error scales roughly as 2^(−2r/D₁), and chaotic error grows as e^(λt), giving about 0.336 Tλ/bit for Lorenz (D₁≈2.06). For each system and interval, fix that slope and fit only α on even rates; predict odd-rate horizons without refitting. Pass if held-out MAE is ≤0.15 Tλ, no held-out residual exceeds 0.25 Tλ, and the bootstrap interval for the observed even-rate slope overlaps the predicted slope within ±20%. Treat this as a high-rate hypothesis, not a theorem.

8. Surprising result

I would be surprised if low-rate token histories substantially beat their z₀-only information limit: a long symbolic itinerary might locate the current state within its codeword cell well enough that a continuous head beats the codeword distortion floor and recovers much of the exact-state horizon. That would expose a real history-reconstruction benefit even though Takens does not guarantee it.
