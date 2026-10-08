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

Spark execution logs are copied alongside each task JSON before the R34 failure gate. Updated strict-wrapper SHA-256: e5fede30f889992ad704edfcc23cd0df4e470bcc980f99b121ba2e3540605a56. criteria unchanged.

A Stage18 release marker enables the saved-output Stage16 aggregation only after the requested GPU queue handoff. Remaining-wrapper SHA-256: 18ccc86dbacae977c13c121539681ee30e932044576533390311b122b623a9ca. criteria unchanged.

Direct scoring entry points also check the phase gate. Final remaining-wrapper SHA-256: c064d50c8bca5e45e7658cc17a13dff7912a5def02b1fd7d88133af3aaacb2f1. criteria unchanged.

## Handoff and publication-support hashes

{
  "acd_stage21_ops_acd_deadline_supervisor.py": "d5124271125d1080b72ed1b3f83dbf3036aed110e55174b628892e454a0970a7",
  "acd_stage21_ops_resume_strict_R12.py": "6572918ec797e4de206ee93405e881fd2de58ed57319255b84968a4a5c1d6ff9",
  "acd_stage21_ops_acd_guarded_publish.py": "4dd31368934a3f32eb764e02767a4c0c55db440a08ed8355965cc4b9cba80236"
}

Before replacing paused controllers, the handoff captures actual worker exit statuses, lets every active worker finish, and restores any serving units the previous controller leased. Final support hashes: {"acd_stage21_ops_acd_deadline_supervisor.py": "d5124271125d1080b72ed1b3f83dbf3036aed110e55174b628892e454a0970a7", "acd_stage21_ops_resume_strict_R12.py": "bccbd43d09e332c1b71587ba9f017566ed6ce537fd45e18f366182f9506aa222", "acd_stage21_ops_acd_guarded_publish.py": "4dd31368934a3f32eb764e02767a4c0c55db440a08ed8355965cc4b9cba80236"}. criteria unchanged.
