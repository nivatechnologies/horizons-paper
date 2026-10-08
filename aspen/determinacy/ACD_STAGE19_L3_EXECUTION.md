# Stage 19 L3 inference execution record

The per-run checkpoint gate amendment is pushed. All new Stage16 run receipts and selected checkpoint hashes are committed. This adapter extends only the in-memory checkpoint/name allowlist and calls the unchanged Part2 run function. Frozen files and criteria are unchanged. Separate seed directories retain checkpoint provenance, atomic per-case outputs and their hashes. No realized outcome is opened and no scoring is launched. Outcome access and L3 readings remain gated on all new runs committed and all inference complete.

GPU lanes use Baccus cards with no non-serving compute holder. The authorized serving units may be stopped and are restored after each run; any other job makes the lane wait. Card zero remains outside this controller. Checkpoints are copied read-only from completed outputs on Sulaco; the Sparks and Stage16/Stage18 queues are untouched. Failures are logged and do not suppress later runs.

Adapter SHA-256: 11b7c75b772d5c1ceeafa1ea3de29681d550896d2fa93f60a00d03e16011dfee

Part2 inference SHA-256: 591f6ce4989b19be4bbda36e6ffa39ecf34940bc513a1770e361b00ee1a7ef6d

Startup amendment: seed receipt ancestry uses the stable remote branch reference. The inherited access-gate fetch is serialized across seed workers to avoid concurrent FETCH_HEAD replacement. This changes only repository metadata synchronization; the scientific inference path is unchanged. Initial transport/gate failures are recorded separately and may be retried without scoring or replacing a training run.
