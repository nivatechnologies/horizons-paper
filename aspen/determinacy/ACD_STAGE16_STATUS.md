# Stage 16 replication status

Both alternating queues are running from pushed freeze 160d02a. Spark 1 runs seeds 1–2; Spark 2 runs seeds 3–4. Checkpointed training and per-case inference continue independently. Scoring runs on sulaco as each inference completes. Matched-coverage readings await the committed Stage 15A definition; training and evaluation do not wait for it.

Host, process, code and fixed data verification: receipts/acd_stage16_startup.json.
