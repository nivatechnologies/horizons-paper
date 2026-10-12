# Stage23 first-run cost projection

Computed from the charged GPU seconds at the first 500 scheduled updates of the first run. Initial diagnostics and startup charge are included; checkpoint validation adds later work. This is a projection, not an extension of the frozen 36,000-second cap. Every weight remains reported, and checkpoint selection stays frozen.

```json
{
  "model": "CNN-noF-response-0.01-seed1",
  "pilot_updates": 500,
  "charged_gpu_seconds": 737.9191204649396,
  "projected_seconds": 29516.76481859758,
  "projection_rule": "charged seconds at first 500 scheduled updates times 20000/500; cap unchanged",
  "cap_seconds": 36000,
  "source": "/mnt/niva-array/work/aspen-determinacy-stage23-20261012/aspen/determinacy/runs/stage23/training/CNN-noF-response-0.01-seed1/progress.json",
  "utc": 1791779427.4519405,
  "projected_hours": 8.199101338499329,
  "criteria_unchanged": true
}
```
