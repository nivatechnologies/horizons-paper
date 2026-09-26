# EXT2 freeze: learned-tokenizer kill test

This freeze covers the work order "Learned-tokenizer kill test", issued 2026-09-25. It is committed before any
training beyond a timing pilot of at most 1,000 steps. Every EXT2 results commit postdates it.

The machine-readable version is `ext2_freeze.yaml`. The spec integrity gate report is `EXT2_GATE.md`.

## Question

On 2D Kolmogorov flow (Re 40, 64²), the paper's k-means patch tokenizers show two things at 0.1σ_A: the
perfect-token ceiling lies below decode-and-integrate (DI) at the low-bit end of each layout, and it lies above DI at
higher bits (see the gate report, error 3).

This work order asks whether a learned FSQ autoencoder behaves the same way at the same layouts and rates. Its
decoder combines neighbouring latent positions.

## Tokenizer

The tokenizer is an FSQ autoencoder (`ext2/fsq_ae.py`):
- VQGAN-style residual encoder and decoder, 64 base channels;
- circular padding on every 3×3 convolution;
- no attention;
- MSE on vorticity scaled by σ_A/64, so the loss equals ‖x − x̂‖²/σ_A², the scored error. There is no other loss
  term.

The level sets come from the FSQ paper, Table 1.

| Config | Latent | Levels | Codes per token | Bits per frame |
|---|---|---|---|---|
| L8-b10 | 8×8 | [8,5,5,5] | 1,000 | 637.8 |
| L8-b12 | 8×8 | [7,5,5,5,5] | 4,375 | 774.1 |
| L8-b16 | 8×8 | [8,8,8,5,5,5] | 64,000 | 1,021.8 |
| L16-b10 | 16×16 | [8,5,5,5] | 1,000 | 2,551.1 |
| L16-b12 | 16×16 | [7,5,5,5,5] | 4,375 | 3,096.3 |

## Data

All seeds follow the freeze.yaml scheme with system index 8.

| Block | Use | Size |
|---|---|---|
| Calibration fit (seed 10800) + training (seed 20800, new) | training | 409,600 states from 512 independent trajectories |
| Validation (seed 30800, new) | checkpoint selection only | 6,400 states from 64 trajectories |
| Calibration held-out (seed 10801) | report only: reconstruction, utilization, level usage | 51,200 states from 64 trajectories |
| Confirmation (seed 40800) | measurement only | 1,000 states, the KKE3 panel |

## Training

- 30,000 steps at batch 64.
- AdamW at learning rate 3e-4, betas 0.9/0.999, weight decay 0.01.
- Cosine decay to 0, no warm-up, gradient-norm clip 1.0.
- float32, model seed 0.
- Validation every 1,000 steps; the checkpoint with minimum validation loss is kept.
- **Divergence** means a non-finite loss, or a best validation loss of at least 1.0 (the zero-prediction null).
- **Fallback:** one rerun at learning rate 1e-4. There is no other tuning.

## Measurements

All measurements use the 1,000 KKE3 confirmation states and W = 27.
- Frame intervals: Δ = 0.35 is primary; 0.14 and 0.70 are secondary.
- ε ∈ {0.1, 0.3, 0.5}.
- Scores: future frames (primary) and from t = 0 (secondary).

| ID | What | Label |
|---|---|---|
| M1 | reconstruction ‖x₀ − D(E(x₀))‖/σ_A: RMS, and the share within ε | learned |
| M2 | T_pt: the first scored frame with ‖x_t − D(E(x_t))‖ > εσ_A on true frames. **"Perfect next-token prediction (reference)". It is not a bound.** | reference |
| M3 | decode-and-integrate from D(E(x₀)) (E3 pipeline and projection) | reference |
| M4 | persistence of D(E(x₀)) | reference |
| M5 | paired M3 − M2 (paired bootstrap over trajectories, 2,000 reps, seed 777), with 90% and 95% intervals; the strict outlast share; S(1), S(3), S(10) for M2 and M3 | estimate |
| M6 | beside the KKE3 k-means rows at the same layout and nearest bits. Descriptive only; no reading. | bound / reference |

## Readings

All readings use the frozen margins, on d = M3 − M2.
- **R1 (the vocabulary binds):** d ≥ 0.25 and the lower 95% limit is above 0.
- **R2 (the vocabulary does not bind):** either the 90% interval lies within ±0.10, or the upper 95% limit of d is
  below 0 (T_pt above DI).
- **Otherwise,** no reading applies.

Readings are reported per configuration, Δ, ε and score. The primary is future frames at Δ = 0.35.

**Kill criterion.** The frozen WO text: "if R1 fails at ε = 0.1 for every configuration with at least 2^10 codes
per token, the tight-tolerance practical claim is dropped."

The gate found its eligible set unpinned, so the executor does not issue the verdict. R1 at ε = 0.1 is reported for
both candidate sets:
- **literal:** L8-b12, L8-b16, L16-b12;
- **nominal:** all five configurations.

The decision is Todd's.

## Cut order

Cuts, in order: Δ 0.14 and 0.70, then L16-b12, then L8-b16. Never cut L8-b12 or L16-b10.

## Deliverables

- NUMBERS section K3.
- Figure F9. F8 already exists; F9 has F7's axes, with panels at ε 0.1 and 0.3.
- A script-generated results-note section.
- A session-review section.
- No AI attribution lines in any commit.
