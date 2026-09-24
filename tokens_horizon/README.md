# How Much Horizon Does a Bit Buy?

Code, raw run outputs and figures for *How Much Horizon Does a Bit Buy? What token histories reveal, what
vocabularies can express, and what forecasters learn*.

Affiliation: Niva Platforms, Inc.

A chaotic flow (Lorenz-63, Lorenz-96) is observed through a k-means tokenizer at a fixed frame interval.
We measure forecast horizon (restricted mean of λ·T, capped at 27 Lyapunov times, where T is the first frame with
‖x̂ − x‖ > 0.3σ_A) for:
- **bounds**: the output-support bound, which caps any forecaster whose outputs are codebook entries;
- **references**: forecasters that use the true dynamics (decode-and-integrate, a particle filter on the token
  history, persistence, climatology, residual-VQ oracles);
- **learned** arms on one transformer backbone (token model A, continuous-output B, continuous-input C,
  state reconstruction D, projection E, probes on A).

The protocol was frozen before any confirmation result or training run. See `FREEZE.md` and `freeze.yaml`,
and `gate/GATE_REPORT.md` for the pre-registration checks. `NUMBERS.md` lists every reportable number with its
label (bound / reference / learned / estimate), source file and commit.

## Layout

| Path | Contents |
|---|---|
| `freeze.yaml`, `FREEZE.md` | Frozen protocol: systems, seeds, splits, tokenizers, scoring, margins, pins |
| `th/` | Library: systems and RK4 (`systems.py`), trajectory blocks (`data.py`), tokenizers (`tokenize.py`), scoring and bootstrap (`score.py`), particle filter (`pf.py`), exchange-law helpers (`exchange.py`), transformer arms (`models.py`), training and rollout (`learn.py`) |
| `scripts/prep_cache.py` | Builds calibration blocks, codebooks and panels (deterministic caches) |
| `scripts/t0_lyapunov.py` | Lyapunov spectra, D_KY, spectrum-sum check, step-halving → `results/lyapunov.json` |
| `scripts/t0_pilot.py` | Training-speed pilot that set the step budget → `runs/pilot/` |
| `scripts/t2_system_table.py` | System table with D_eff and intervals → `results/system_table.*` |
| `scripts/t2_headline.py` | Output-support bound, history reference, decode-and-integrate, persistence, climatology; p_0; outlast fractions; step-halving; particle sensitivity → `runs/headline/`, `results/headline/`, `results/headline_subsets/` |
| `scripts/t2_decomposition.py` | Single-frame decomposition (I, O, bias-corrected O, projected-DI excess), known-zero test, trajectory bootstrap → `runs/decomposition/`, `results/decomposition/` |
| `scripts/postfreeze_codebook_seeds.py` | Post-freeze robustness: decomposition and output-support bound for k-means random_state 0–4 (4, 6 bits) → `results/postfreeze/` |
| `scripts/t2_exchange_law.py` | Calibration map h, held-out-rate predictions and criterion, r by orientation, FSLE → `runs/exchange_law/`, `results/exchange_law/` |
| `scripts/t2_dimension.py` | Distortion curves, scalar quantization, residual-VQ oracle horizons → `results/dimension/` |
| `scripts/t2_history.py` | Context sweep, timing jitter, observation noise → `runs/history/`, `results/history/` |
| `scripts/t3_learned.py` | Stall check, then train, select and evaluate every learned arm → `runs/learned/` |
| `scripts/t3_analysis.py` | Learned arms against bounds and references (paired, frozen readings) → `results/learned/` |
| `scripts/fig_F1.py`, `fig_F2_F4_F5.py`, `fig_F3.py`, `fig_F6.py` | Figures (SVG, PNG and CSV, greyscale-safe) → `figures/` |
| `scripts/make_numbers.py` | `NUMBERS.md` |
| `reproduce.py` | Runs the table, figure and NUMBERS steps from raw runs. `--full` also recomputes missing raw runs |
| `prelim/` | Preliminary exploratory scripts, verbatim, with the reproduction check that preceded the freeze |

The single-frame decomposition (F3) runs under Amendment 1 to the freeze (`FREEZE.md`). The known-zero threshold
was amended from 1e-10 to 1e-6 after the original threshold proved unattainable at 4 bits with the frozen k-means
settings. Both outcomes are reported in `results/decomposition/`.

## Reproduce

```
uv venv --python 3.12 .venv
uv pip sync --python .venv/bin/python tokens_horizon/env/requirements.lock \
    --extra-index-url https://download.pytorch.org/whl/cu130 --index-strategy unsafe-best-match
cd tokens_horizon
../.venv/bin/python reproduce.py          # tables, figures and NUMBERS.md from runs/
../.venv/bin/python reproduce.py --full   # recompute missing raw runs as well
```

The default mode rebuilds the calibration and codebook caches (about 20 min on 128 cores) and then regenerates every
table and figure from the committed per-state arrays. Trained weights are not committed. `runs/learned/MANIFEST.csv`
lists their SHA-256 hashes, and `--full` retrains any model whose run directory is missing.

Verified on 2026-09-24: a fresh clone of commit `48cc7cc` with a new venv built from the lockfile ran `reproduce.py`
with no failed step in 35 min 48 s. Every regenerated number matches the committed value to within a relative
2.9e-12. The only differences are floating-point summation order, including in the decomposition, which is
recomputed from codebooks refit from scratch.

## Hardware and runtime (build host)

128-core x86 server, 503 GB RAM, 3 × NVIDIA CMP 170HX (sm_80), Python 3.12.3, torch 2.13.0+cu130.
- References (Task 2): about 30 min of CPU in total with 48 worker processes (particle filters at 1,500 or 3,000 particles).
- Learned grid: 190 models at 10,000 AdamW steps (0.025 s/step at Δ = 0.02 on one GPU), run as 9 concurrent processes on 3 GPUs, taking about 5 h.
- Determinism: all seeds are derived from `freeze.yaml`. The CPU pipeline is bit-reproducible on the same library versions. GPU training is seeded but not bitwise deterministic across hardware.

## License

Apache License 2.0 (`LICENSE`).
