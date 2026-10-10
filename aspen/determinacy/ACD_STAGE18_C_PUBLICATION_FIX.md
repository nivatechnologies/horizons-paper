# Stage 18 C publication execution fix

All response-control training, inference and scoring finished. Figure publication failed with `KeyError: decisions`: retained CNN-noF and CNN-F metric receipts were merged after their decision records had been attached, replacing those records. The presentation adapter now attaches the existing committed receipts/acd_stage10b_decisions.json readings after all metric-receipt merges. This changes only the figure lookup; no training, selection, inference, scoring, statistic or criterion changes, and no outcome is opened. Criteria unchanged.

The first traceback is preserved in runs/stage18/C_publication_failure.log. The supervisor retries publication, then dispatches the existing selected-model derivative controller.

Previous publisher SHA-256: f3f147032d0370e042dc76583664e5eef0b24680a837dfd88b60f3a17e65becb

Corrected publisher SHA-256: c0f0003941d1b594435eda5816897f332055667a8bfd53bb5c5746f1be494dde
