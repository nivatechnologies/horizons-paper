# Stage21 R34 execution amendment

Todd authorized splitting the remaining matched-seed GPU queue across the three local Sparks. No frozen rollout or scoring source, checkpoint, estimator, population, threshold or pass criterion changes; criteria unchanged.

The host assignments and launcher hashes are in receipts/acd_stage21_multispark_execution.json. Both E1 fixed and E1 rolling for each seed use the same host and frozen GB10 CUDA worker. Already complete outputs are reused. CPU work is not dispatched to a Spark.

The third Spark uses its existing host-specific Todd SSH key explicitly. Todd authorized stopping tensorfold-single.service there; it is restored after that host queue completes. No other serving process is stopped on a Spark. All training image jobs remain offline with network disabled.

Each task preserves its log next to its return-code record. A nonzero return code or incomplete hashed output blocks scoring and result publication. The previous paused one-Spark dispatcher is retired between tasks without interrupting a worker.

## Execution follow-up

Future R34 and descriptive CPU scoring runs on sulaco using the unchanged frozen scorer and original instance order. R12 was already in flight. Copies are verified by the existing frozen guards; the realized cache is opened only by the frozen scoring code. Updated launcher hashes are recorded in receipts/acd_stage21_execution_host_followup.json.

Previously completed Spark outputs require their actual recorded process exit status. The stopped dispatcher’s second completed task had not yet written its return-code record; the Docker zombie exit status was recovered directly from /proc before retiring that dispatcher. No success code is inferred from output presence.
