# Stage21 forcing-shift panel readings

## Frozen reference readings

No emulator is needed for G1/G2. The original R0 criterion and the original own-eligibility/censoring construction are unchanged. The instance is the inference unit; excluded instances are withheld. Realized outcomes are created or read only inside scoring code.

| Reading | Estimate | Bound / interval | Result |
|---|---:|---|---|
| G1 | 0.9958206686930091 | [0.977, 1.0] — original R0 one-sided 95% bounds; pooled accuracy 0.9959100204498977 | PASS |
| G2 | -0.2309265010351967 | [-0.404, -0.04400000000000004] — two-sided 99% v2.3 betting | PASS |

Population: 198 retained of 200; exclusions [69, 160]. Paired eligibility gives 1266 pairs across 184 instances.
