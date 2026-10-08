# Stage 21 R12 execution recovery

Cause: every original R12 task failed at import with `ModuleNotFoundError: No module named 'numba'`. The GPU interpreter lacked the inherited physics dependency.

Fix: Numba and llvmlite were installed into the existing GPU virtual environment from the offline local cache, without sudo. Frozen rollout, scoring, checkpoint, estimator and criterion hashes are unchanged. All task-list checkpoint/estimator paths match their frozen hashes. Original Stage 18 training paths are absent in this worktree; the task-list copies are present and verified.

criteria unchanged

The execution wrappers now require a zero task return code and valid complete.json before scoring or result publication. Logs accompany task JSON records. FAILED phases publish diagnostics only. R34 waits for successful R12 recovery, descriptive arms follow R34, and Stage 18 is released after descriptive publication.

Timing: a recovery launched before this instruction had already produced outputs. Its controller was paused while this note was prepared; workers already in progress were left intact. This note precedes resumed dispatch and scoring.

## First error from every original task

runs/stage21/priority_logs/R12_CNN-F-E0-fixed-seed1.log

> ModuleNotFoundError: No module named 'numba'

runs/stage21/priority_logs/R12_CNN-F-E0-fixed-seed2.log

> ModuleNotFoundError: No module named 'numba'

runs/stage21/priority_logs/R12_CNN-F-E0-fixed-seed3.log

> ModuleNotFoundError: No module named 'numba'

runs/stage21/priority_logs/R12_CNN-F-E0-fixed-seed4.log

> ModuleNotFoundError: No module named 'numba'

runs/stage21/priority_logs/R12_CNN-F-E0-fixed-seed5.log

> ModuleNotFoundError: No module named 'numba'

runs/stage21/priority_logs/R12_CNN-F-constantF.log

> ModuleNotFoundError: No module named 'numba'

runs/stage21/priority_logs/R12_CNN-noF.log

> ModuleNotFoundError: No module named 'numba'

## Execution wrapper hashes

{
  "acd_stage21_ops_.py": "cce779a1414640d66b6ea72406004c709de94eeeb754ab51f16855962565529b",
  "acd_stage21_ops__R12_recovery.py": "fb900486f757c06a3f045843aaae12e5689fe2e21ea3efc25bb56af04bb4e166",
  "acd_stage21_ops__strict.py": "f82ac6ca5fbeed03eb7e97a70a604a36230931a92597deced2f072d49e3fe620"
}
