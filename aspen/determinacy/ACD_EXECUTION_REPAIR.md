# Confirmation receipt serialization repair

The initial workers saved posterior and crude outputs for cases0–15, then failed writing their case receipts because the MAP boundary-contact diagnostic was a NumPy integer. No confirmation realized outcomes or readings were computed. CNN was waiting for those receipts and was stopped; no Qwen service was stopped.

Convert the diagnostic to a Python int. This changes serialization only: no inference, statistics, seeds, thresholds, fit order or compute settings change. Preserve the initial arm outputs and order logs under runs/audit/serialization_retry_preoutcome; rerun the same case indices with the frozen seeds/settings.

The original scientific and code freezes are preserved. The additive repair receipt records the sole changed source hash, and runtime verification requires its committed/pushed receipt before resuming.

SHA-256 of acd_confirmation.py: `8d3b481a87945bd23d6b971c1b521d6471a981cb25709a56d2d76ec84f232d2c`.
