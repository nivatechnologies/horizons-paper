# Stage 15 recovery status

Inspection UTC: 2026-10-07T20:09:43.972724+00:00.

Post hoc on confirmation; licenses no frozen route.

| Part | Complete | Running | Remaining |
|---|---|---|---|
| A | Matched-coverage receipt, fixed ranking, four-model tables; exact count correction recorded | None | Serialized registry/push handled by recovery coordinator |
| B | Three PDF/PNG figure pairs and computed hashes/page sizes | None | Serialized push handled by recovery coordinator |
| C | 200 cases; 199 retained; 1 excluded after retry; all output hashes checked before scoring | None | Serialized registry/push handled by recovery coordinator |
| D | Fixed-case full-covariance nested-JVP receipt and table | None | Serialized registry/push handled by recovery coordinator |

Timing gate: {
  "pilot_wall_seconds": 44.680538551998325,
  "pilot_mean_seconds": 40.94921441599727,
  "workers": 30,
  "cores_per_worker": 4,
  "reserved_cpus": [
    120,
    121,
    122,
    123,
    124,
    125,
    126,
    127
  ],
  "projected_seconds": 444.9814633205036,
  "projected_hours": 0.12360596203347322,
  "limit_hours": 24,
  "passed": true,
  "original_retry_rate": 0.055,
  "original_full_rescore_rate": 0.575
}.

R-other: the initial missing Stage 15 contract was subsequently supplied by Todd. The floating-product truncation in the first matched-coverage receipt was corrected; the old receipt remains for registry history. Model factual outputs omit a physics terminal tick beyond all scored windows; every scored tick is asserted present in both sources.
