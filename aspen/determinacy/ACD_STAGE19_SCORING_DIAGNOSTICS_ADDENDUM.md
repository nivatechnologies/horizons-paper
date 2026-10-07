# Stage 19 scoring diagnostics addendum

The frozen learned scoring implementation now records exact zero-effect ties among acted cases and the per-case answer counts, wrong counts and differences used by the primary learned comparison. These are additive audit fields. The estimands, eligibility, probabilities, intervals and pass criteria remain those in Freeze B. The original strict harm convention is unchanged. This addendum is committed before learned scoring begins.

Original scorer SHA-256: `63492818dd11bb5a4e294c515aaa462d9b1559fd32ee436fb69783f19e7dec26`.

Scorer with additive diagnostics SHA-256: `9319e768f5d211472d6c52fe0b7c4cef975d878be242b14807a43178e7e85930`.

The inference and reference scoring implementations are unchanged. No new model selection or statistical reading is introduced.
