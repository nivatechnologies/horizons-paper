# ACD execution-code freeze addendum — v2.3 confirmation

Connectivity is restored. The original scientific freeze at `1f38be3` has been
pushed. This addendum records the confirmation adapters before any confirmation
data is generated or accessed. Commit and push this addendum before execution.
The scientific thresholds, seeds, null, priors, likelihood, forecasting kernels
and Stage 1 reading are unchanged. `acd_stats.py`, `acd_posterior.py`,
`acd_fits.py` and `acd_mechanism.py` match their original frozen hashes exactly.

The sole changes to baseline scientific interfaces are observation-only
confirmation input paths, a separate truth path in permitted scoring/measurement
code, and the confirmation adapters/readings. The CPU JAX environment and the
original CPU package lock are retained; the GPU inference package additions are
recorded separately in `requirements-stage2.lock`.

## Pre-data resolutions

**R-other** — RML-conf cut removes prescribed fourth MAP and chain initializers: No RML fits on confirmation. Four MAP starts at (y0,Fhat),(y0,6.5),(y0,9.5),(y0,8.0); 8.0 is the prior midpoint. The four fitted states initialize the four chains. Lowest MAP likelihood cost is provisional; final minimum includes every full posterior draw. Same prior, likelihood, optimizer, diagnostics, seeds and thresholds.

**R-other** — Frozen R5-A cut removes all-site licensed-sentence clause: Report Q/F/V/R only; omit the all40 ceiling clause and RML sentence. No value is imputed for a cut arm.

## Execution and blind-order checks

`acd_confirmation.py` verifies every execution hash, inherited source hash,
checkpoint hash, raw-null hash and exact compute setting before generating any
case. A pushed-freeze receipt binds this addendum's committed receipt. Execution
requires sulaco. All inference uses the logged `load_observed` interface.
Truth-bearing histories are saved separately, without exposing them to inference.
Observed windows are generated from the inherited history stream, not from any
outcome. The posterior archive contains no truth/scoring arrays.

For each case, observations, posterior, crude and CNN are written and hashed,
in that order, before realized outcomes. A GPU omission has a hashed R-gpu
receipt before outcomes. CNN predictions use all nine actions, share the RML
perturbation seed, and pair-drop invalid members across all actions through the
2 LT scoring horizon (the last tick in its inherited window). The network and
normalization match the inherited code. CPU JAX cannot preallocate GPU memory.
No service is stopped; CNN tries smaller batches if memory is short.

R5 population is chosen only after the ordinary panel is complete, by case
index from pre-probe posteriors. Failed refits remain in the common denominator.
The refit and measurement kernels are unchanged except for the scoring truth
path. `acd_stage2_check.py` independently checks every blind-order event,
sampler archive/hash, settings, checkpoint, population and refit artifact.

The confirmation analysis preserves the Stage1 R0/R0-F/R1/R1m/R2a/R2b/R2c/R3/R5
calculations, replaces the development STRONG rule with §11 publish/kill/decide,
omits RML and cut P/B leads, and adds R6 at2LT. KILL takes precedence if coverage
is below .85. Every statistical route retains its frozen prerequisites and
count floors. Reports/ledger/vault outputs are generated from the final receipt.

Pre-data checks: Python syntax and whitespace checks; synthetic rendering of
publish/kill/decide and cut-arm suppression; four-MAP initializer smoke check
on development case0 only. No confirmation data was used for these checks.

## Code hashes (SHA-256)

| File | SHA-256 |
|---|---|
| `acd_analysis.py` | `81d92215e5daaa3da2ae9cad206aafa9cca52d288feb529b0b1bc426eabfe3eb` |
| `acd_campaign.py` | `b60295a66abf3504743a9d214b37bb794a38abb59221a2b20b5089e88bbb5556` |
| `acd_cnn_ensemble.py` | `8222efb35c72149ca60379b9043ffa2d24d097f71d6227cad93660f5684ea478` |
| `acd_confirmation.py` | `ce78f49bd01a550a83e366df74c07a9c440257cee2bbb8eb7f5919e5149e572b` |
| `acd_confirmation_analysis.py` | `4fc31d6936c04330da29838600752f6964df92f091a8d6f9d46da53a27e01b29` |
| `acd_fits.py` | `17e62ac36a1ff18bc93721dc828a77e079932f320423d3aa9e367432df9d13cd` |
| `acd_freeze.py` | `7218eebc432c0e1c09f0d3be5755089c09ee281630b7180c09fff73601980cfb` |
| `acd_freeze_code.py` | `bc5e3a660597164386dfa9a46d3843ef74f79e8758172c9d90fce66496e1f6fe` |
| `acd_ledger.py` | `bc20ad24420d08fe39b4840b506fa4faf065c69680e497df9cb8a6dca291d1f9` |
| `acd_measure.py` | `f9d8ff4bfd3ff3d4db6ff30379f8ba41edff509381d5b8f5eaeb2d949180d4d4` |
| `acd_mechanism.py` | `886fea5d67b217e72829c4e07b469473e391cfb17b84d18f6bc0307606e40e9f` |
| `acd_posterior.py` | `0b80c61b2e7530dabec4f9c3f0e7fee51f2cfc1ad15745b729d3ddc227c6a60a` |
| `acd_protocol.py` | `160eabe8ccee07d0de17576a441b6fef1a93e1d5dbb68f2df9eb118a1eaad000` |
| `acd_questions.py` | `5c932b427874ae9108824a528a4ae35b2b5d957c2376a9d71b02369fc5abb698` |
| `acd_render.py` | `c23373323b5acd3e6f6a22b524e5e16f3199c5bad1b728603363674ddd6bd920` |
| `acd_stage2_check.py` | `bd01b3aae26253a4d8c1402d80979c78f4dfee7c9941077d9d7da46f7639d44e` |
| `acd_stage2_render.py` | `c8fa27b57b5a888c4f1844127a44e0b491fc885cdd881e5a841091e6d25b61a1` |
| `acd_stats.py` | `1c97d51262a7546b70320c1207de554eff6f9b6a58b00428a2640f5ead6f685a` |
| `acd_stats_audit.py` | `92e4f1954c53f68fe2c794265aa22651b1e5d0edfddbf13b22183276be6c8f2f` |
| `acd_step0.py` | `2c5eb3a53e6b2f36f632b22d284d6a2ba49c9dc9ad3e4b95b36679cdb3efbb53` |
| `check_acd.py` | `e60140059c18f74e46a7170d4a4657f5ca82a70c6b633041b78d324fb36c3b31` |
| `spec_boundary_counterexample.py` | `975bc992a2ef1a45419a12762d8337184e0fe8662c26a9aa5d50ba303720efcc` |
| `ACD_FREEZE.md` | `ff04820b81450163db9d815c64f0c9fa5a8192e5b3db8925cc24711e6609a21a` |
| `receipts/acd_freeze.json` | `7b16346ed33ed69e7825d4ac0616afbcaec8f6e7197b1826ab8e965c55c2d60a` |
| `requirements-cpu.lock` | `795d5b658d49885467763be4a4eab2cf04f4c0a754c5acf8aaa3bf3d7daf9544` |
| `requirements-stage2.lock` | `01dbb9d525c1ad28c73a246ceeb4358857bb514b7078fbfb13a4db9a76be8514` |
| `sources/Ledger_pre_stage2.md` | `a0998e29431f0f2335a860d29cfc42b2b3c3fd349c99501c3daf3d24a963ee7e` |

Addendum receipt SHA-256: `4019410e46018904280ba12ee54e31c9e682ffbde5d37bdd0ab595179e479119`.
