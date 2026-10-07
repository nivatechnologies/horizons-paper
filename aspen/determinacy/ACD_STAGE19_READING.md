# Stage 19 fresh-panel readings

Reference side: Freeze A and Freeze B. The original confirmation-panel mechanism and seven-pattern comparisons were post hoc; these fresh-panel readings were frozen before outcomes were computed.

| Reading | Original confirmation | Fresh panel | Fresh bound | Result |
|---|---:|---:|---|---|
| C1 (2.0 LT) | 0.995250 | 0.996717 | [0.979000, 1.000000] | PASS |
| C2 (paired LT) | -0.308787 | -0.321013 | [-0.488000, -0.144000] | PASS |
| C3 (2.0 LT) | -0.243125 | -0.225625 | [-0.338000, -0.120000] | PASS |
| C3 (3.0 LT) | -0.266250 | -0.218750 | [-0.360000, -0.098000] | PASS |
| C4 (2.0 LT) | -0.156429 | -0.140714 | [-0.258000, -0.032000] | PASS |
| C4 (3.0 LT) | -0.297857 | -0.257143 | [-0.396000, -0.136000] | PASS |
| M1 (2.0 LT) | 0.995089 | 0.995875 | — | PASS |
| M2 (2.0 LT) | 0.856875 | 0.856250 | [0.820000, 1.000000] | PASS |

C1 retains the original R0 one-sided 95% case bounds and original answer/case prerequisites. C2–C4 use two-sided 99% case betting intervals. M1 has the frozen median threshold without an interval. M2 has a one-sided 99% case betting lower bound. The C2 direction is reported separately in the receipt.

| R0 lead (LT) | Observation-confident answers | Contributing cases | Equal-case accuracy | Lower / upper | Status |
|---:|---:|---:|---:|---|---|
| 0.0 | 1376 | 200 | 1.000000 | [0.983000, 1.000000] | PASS |
| 1.0 | 1283 | 200 | 0.999286 | [0.982000, 1.000000] | PASS |
| 1.5 | 1139 | 199 | 0.996722 | [0.979000, 1.000000] | PASS |
| 2.0 | 951 | 198 | 0.996717 | [0.979000, 1.000000] | PASS |
| 2.5 | 904 | 193 | 0.996669 | [0.978000, 1.000000] | PASS |
| 3.0 | 650 | 178 | 0.992175 | [0.972000, 1.000000] | PASS |
| 4.0 | 217 | 92 | 0.992754 | [0.955000, 1.000000] | PASS |
| 6.0 | 8 | 5 | 1.000000 | [0.088000, 1.000000] | NOT EVALUABLE |

| Descriptive lead (LT) | Mean-flow variance share median, seven patterns | Three-class agreement | Kappa | Per-draw sign agreement | Original z ratio | Fresh z ratio |
|---:|---:|---:|---:|---:|---:|---:|
| 0.0 | 0.262751 | 0.976250 | 0.953198 | 0.985511 | 3.576923 | 4.083958 |
| 1.0 | 0.946819 | 0.955000 | 0.919520 | 0.976186 | 1.271961 | 1.282136 |
| 1.5 | 0.983652 | 0.913125 | 0.859908 | 0.955655 | 0.851964 | 0.839049 |
| 2.0 | 0.995875 | 0.856250 | 0.782072 | 0.910129 | 0.607695 | 0.662505 |
| 2.5 | 0.998201 | 0.820000 | 0.720663 | 0.868971 | 0.547837 | 0.507464 |
| 3.0 | 0.998520 | 0.810000 | 0.649728 | 0.794519 | 0.528972 | 0.543811 |
| 4.0 | 0.999015 | 0.898750 | 0.502539 | 0.646357 | 0.475866 | 0.564897 |
| 6.0 | 0.999742 | 0.994375 | 0.180188 | 0.519953 | 0.743197 | 0.621134 |

Fresh eligibility yields 1299 pairs in 189 cases. The descriptive M3 crossover expectation holds: the median z ratio is above one at lead zero and below one at the frozen mechanism lead.

Known-forcing readings remain deferred to Part 3. Its exclusion is recorded in the Part 1 receipt and Freeze B. No emulator was needed for these reference readings.

No statistical R-other condition fired. The first scoring process completed the realized-cost cache, then encountered a Numba thread-environment mismatch while compiling betting intervals. The same frozen code completed with NUMBA_NUM_THREADS set consistently before imports; calculations and criteria were unchanged.

Source receipts: receipts/acd_stage19_reference.json, receipts/acd_stage19_part1.json; original values and precise keys are retained in the reference receipt. The realized cache and scoring-only access log remain under runs/stage19/.
