# Stage22 publication connection recovery

The pilot passed its frozen timing gate, but its publication callback could not resolve baccus from sulaco. An SSH host alias now supplies the verified address and the existing passwordless identity files. The callback connected successfully and publication resumed. No scientific code, seed, case count, criterion or frozen hash changed. Criteria unchanged.

Pilot timing receipt:

```json
{
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
}
```
