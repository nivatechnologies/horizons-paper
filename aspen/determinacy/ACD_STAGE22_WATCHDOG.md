# Stage22 persistent watchdog and execution handoffs

Criteria unchanged. This execution record adds no scientific reading and amends no earlier freeze. The frozen panel adapter, statistical functions, inference rollout and scoring functions remain unchanged.

The watchdog is an enabled user systemd service, independent of the harness, with restart on process failure. Its metadata probe never opens hidden arrays or realized outcomes. It checks controller/worker activity, CPU time, written-output progress, phase markers, GPU processes, task exit records and completion hashes. Connection failures are retried. Resumable restarts preserve the fixed panel and original seeds and never replace excluded instances. Repeated execution failures stop dependent phases; an integrity or scientific failure is recorded and published rather than bypassed.

Only Stage22 services may be restarted. Existing authorized GPU leases record serving processes, refuse unrelated compute jobs and restore the Baccus serving unit after use or interruption. The Sparks and other stage queues are untouched.

After blind completion is pushed, inputs are built with the frozen preparation path on sulaco, transferred and hash-checked. Three independent GPU slots take the frozen task list on Baccus. Scoring waits for every required completion and pushed inference manifests. It invokes the count-parameterized frozen scorer and the already frozen thin R5/R6 wrapper. No realized outcome is opened during monitoring, sampling, preparation or inference.

Health: runs/stage22/watchdog_health.json. State: runs/stage22/watchdog_state.json. Events: runs/stage22/watchdog_events.jsonl. Service log: runs/stage22/watchdog.log. Failures: runs/stage22/FAILED.json.

```json
{
  "code_hashes": {
    "acd_stage22_runtime.py": "ebb2b10d73e5c7f100ec05c6a2a62f1fc37abc09220ad89de810c3a2111c6028",
    "acd_stage22_probe.py": "72302ac846abf543f9ca2f98d12b66f83e45da7ce666330ee42d2f61a0f36666",
    "acd_stage22_watchdog.py": "8f6b683c4d5ee510fe090a05cc27058f94868da5dc66d62071fd7555fa64a961",
    "acd_stage22_watchdog_publish.py": "4857f03af353d059cbf1b26b820846eb4282af680e0e8a79f6ddd9303f416573",
    "acd_stage22_watchdog_test.py": "ca2b0ad464e1ab06fe881231ab16fee9460f807ba44871a4dd77ede784417628",
    "aspen-stage22-watchdog.service": "997b3df70102b47d891a50c0a1e766b9f4a0bc2e45aa99da17488526f8bee499"
  },
  "criteria_changes": [],
  "realized_outcome_accesses": [],
  "service": "aspen-stage22-watchdog.service",
  "host": "baccus",
  "scope": "Stage22 operational recovery and frozen execution handoffs only",
  "recovery": "Retry network failures; resume interrupted/stalled Stage22 jobs using identical tasks, seeds, affinity, gates and checkpoints; preserve/hash-check completed outputs. Never alter scientific code, thresholds, populations or outcomes.",
  "fail_loud": "Nonzero scientific task exit, missing completion, hash/integrity mismatch, failed frozen gate or exhausted execution retries blocks dependent scoring/publication and publishes the incident.",
  "tests": "Active computation is never restarted for elapsed time alone; integrity failure blocks all launches; dead CPU controller resumes only after passed timing gate.",
  "handoffs": "Entire blind panel must be committed before inputs and inference; all compared pipelines use Baccus170HX; required complete files and exact N coverage/hash verification before scoring; realized access only through unchanged frozen scorer; no interim scores.",
  "sampling_layout": {
    "seconds": 16385.83486450481,
    "hours": 4.55162079569578,
    "limit_hours": 24,
    "workers": 8,
    "cores_per_worker": 4,
    "reserved_cpus": [
      124,
      125,
      126,
      127
    ],
    "pilot_wall_seconds": 87.46472783200443,
    "pilot_mean_seconds": 80.42127540861256,
    "prior_retry_rate": 0.055,
    "prior_rescore_rate": 0.575,
    "component_seconds": {
      "main": {
        "fit_seconds": 5.305151733430103,
        "forecast_seconds": 30.650124673196114
      }
    },
    "passed": true
  },
  "gpu_environment_execution_fix": "Explicit inherited source root on Baccus GPU worker subprocesses; no rollout, statistic, criterion or checkpoint change. No Stage22 inference preceded this correction.",
  "operational_recovery_hardening": "Event timestamps remain serializable; interrupted GPU leases wait for unrelated compute before restoring serving. Criteria unchanged."
}
```
