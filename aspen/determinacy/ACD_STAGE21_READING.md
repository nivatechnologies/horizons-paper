# Stage21 forcing-shift panel readings

## Frozen reference readings

No emulator is needed for G1/G2. The original R0 criterion and the original own-eligibility/censoring construction are unchanged. The instance is the inference unit; excluded instances are withheld. Realized outcomes are created or read only inside scoring code.

| Reading | Estimate | Bound / interval | Result |
|---|---:|---|---|
| G1 | 0.9958206686930091 | [0.977, 1.0] — original R0 one-sided 95% bounds; pooled accuracy 0.9959100204498977 | PASS |
| G2 | -0.2309265010351967 | [-0.404, -0.04400000000000004] — two-sided 99% v2.3 betting | PASS |

Population: 198 retained of 200; exclusions [69, 160]. Paired eligibility gives 1266 pairs across 184 instances.

## R12 — frozen incremental scoring

|---|---:|---|---|
| R1 | None | None, None | not evaluable |
| R2 | None | None, None | not evaluable |

| Pipeline | Population | Lead | S share | Pooled S error | Case S error | E regret | C regret |
|---|---|---:|---:|---:|---:|---:|---:|
| posterior | pooled | 2.0 | 0.7367424242424242 | 0.003427592116538092 | 0.003313696612665673 | 0.014551651928965832 | 0.02925494857143605 |
| posterior | pooled | 3.0 | 0.42676767676767674 | 0.00591715976331364 | 0.005938375350140079 | 0.09784896652732877 | 0.2710562233685539 |
| posterior | F7 | 2.0 | 0.8143939393939394 | 0.0031007751937984773 | 0.0027056277056276556 | 0.0024879037284774716 | 0.0024879037284774716 |
| posterior | F7 | 3.0 | 0.6035353535353535 | 0.004184100418409997 | 0.003534609720176718 | 0.022184858557011224 | 0.0708917374141156 |
| posterior | F9 | 2.0 | 0.6590909090909091 | 0.003831417624521105 | 0.003947368421052588 | 0.02661540012945419 | 0.05602199341439463 |
| posterior | F9 | 3.0 | 0.25 | 0.010101010101010055 | 0.009132420091324311 | 0.17351307449764633 | 0.47122070932299226 |

State skill, forcing errors against both draw and true forcing, cost errors, bounds, calibration, same-lead differences, endpoints and decision action/harm records are retained in receipts/acd_stage21.json. Every invalid draw invalidates its pipeline instance. Excluded posterior cases are withheld.
