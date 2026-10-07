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

## Freeze B learned readings

The original-panel values are post hoc; fresh-panel L1 and L2 use the pushed Freeze B criteria. No frozen route is licensed. Invalid instances are withheld without conditioning on survivors.

| Reading | Original confirmation | Fresh panel | Fresh outcome |
|---|---:|---:|---|
| L1 | 0.062828 [-0.002, 0.128]; 196 instances | 0.068747 [0.004, 0.132]; 198 instances | PASS |
| L2 | 29/199 harms/acted; lower 0.106255 | 27/200 harms/acted; lower 0.0970282 | PASS |

L1 uses a two-sided 99% instance betting interval on CNN-noF minus CNN-F seven-pattern confident wrong share. L2 uses an exact one-sided 95% Clopper–Pearson lower bound for CNN-noF C(delta=0) harm conditional on acting at three LT. L3 awaits all frozen Stage16 checkpoints and remains descriptive.

| Model | Lead (LT) | Original / fresh S confident share | Original / fresh pooled S error | Original / fresh case S error | Fresh case error interval | Original / fresh F_c confident share | Fresh F_c case accuracy |
|---|---:|---:|---:|---:|---:|---:|---:|
| posterior | 2 | 0.72375 / 0.7175 | 0.00431779 / 0.00261324 | 0.00409452 / 0.00266667 | [0, 0.02] | 0.85 / 0.82 | 1 |
| posterior | 3 | 0.40375 / 0.40625 | 0.00928793 / 0.0107692 | 0.0169508 / 0.00782504 | [0, 0.028] | 0.67 / 0.625 | 0.992 |
| CNN-F | 2 | 0.72125 / 0.71875 | 0.00866551 / 0.00173913 | 0.00757358 / 0.00166667 | [0, 0.019] | 0.845 / 0.82 | 1 |
| CNN-F | 3 | 0.4075 / 0.396875 | 0.00766871 / 0.00787402 | 0.011134 / 0.00677966 | [0, 0.026] | 0.65 / 0.625 | 0.992 |
| CNN-noF | 2 | 0.740625 / 0.75125 | 0.0658228 / 0.0607321 | 0.0623869 / 0.0627857 | [0.041, 0.086] | 0.845 / 0.825 | 0.993939 |
| CNN-noF | 3 | 0.4625 / 0.470625 | 0.0756757 / 0.0783533 | 0.108752 / 0.102214 | [0.07, 0.149] | 0.655 / 0.65 | 0.992308 |
| CNN-20k | 2 | 0.7325 / 0.72625 | 0.0546075 / 0.0447504 | 0.053744 / 0.0391131 | [0.02, 0.059] | 0.875 / 0.83 | 0.993976 |
| CNN-20k | 3 | 0.419375 / 0.393125 | 0.0581222 / 0.0413355 | 0.0494081 / 0.0395731 | [0.014, 0.076] | 0.655 / 0.645 | 0.992248 |

Case accuracy/error bounds use v2.3 one-sided 95% bounds; the two directions are reported together. Pooled answer error is descriptive.

| Model | Lead | Original / fresh RMSE/sigma | Original / fresh anomaly correlation |
|---|---:|---:|---:|
| posterior | 2 | 0.120196 / 0.112221 | 0.982929 / 0.986104 |
| posterior | 3 | 0.267713 / 0.260149 | 0.927682 / 0.935558 |
| CNN-F | 2 | 0.122231 / 0.113359 | 0.982641 / 0.986041 |
| CNN-F | 3 | 0.269676 / 0.261697 | 0.927257 / 0.934958 |
| CNN-noF | 2 | 0.122844 / 0.115636 | 0.982278 / 0.985549 |
| CNN-noF | 3 | 0.271781 / 0.26615 | 0.925921 / 0.933085 |
| CNN-20k | 2 | 0.12302 / 0.114162 | 0.982156 / 0.985745 |
| CNN-20k | 3 | 0.277103 / 0.264053 | 0.923981 / 0.934474 |

Factual state skill is averaged over each scored window and over instances.

| Model | Lead | Quantity | Original / fresh equal-case RMSE | Original / fresh equal-case bias | Fresh pooled RMSE | Fresh pooled bias |
|---|---:|---|---:|---:|---:|---:|
| posterior | 2 | J8 | — / 0 | — / 0 | 0 | 0 |
| posterior | 2 | Jk | — / 0 | — / 0 | 0 | 0 |
| posterior | 2 | Dk | — / 0 | — / 0 | 0 | 0 |
| posterior | 3 | J8 | — / 0 | — / 0 | 0 | 0 |
| posterior | 3 | Jk | — / 0 | — / 0 | 0 | 0 |
| posterior | 3 | Dk | — / 0 | — / 0 | 0 | 0 |
| CNN-F | 2 | J8 | 0.0160508 / 0.0155438 | -0.00231998 / -0.000824491 | 0.0223841 | -0.00108746 |
| CNN-F | 2 | Jk | 0.0219491 / 0.0205798 | -0.00425284 / -0.00286609 | 0.0247333 | -0.00314408 |
| CNN-F | 2 | Dk | 0.0177908 / 0.0166639 | -0.00193286 / -0.0020416 | 0.0220855 | -0.00205662 |
| CNN-F | 3 | J8 | 0.0594487 / 0.0554506 | -0.00163844 / 0.00131218 | 0.0758813 | 0.00209482 |
| CNN-F | 3 | Jk | 0.0733581 / 0.0695904 | -0.00457246 / -0.000888325 | 0.0843945 | -7.69716e-05 |
| CNN-F | 3 | Dk | 0.0816559 / 0.0765571 | -0.00293402 / -0.0022005 | 0.0997217 | -0.00217179 |
| CNN-noF | 2 | J8 | 0.0336946 / 0.0321942 | 0.0181195 / 0.0185781 | 0.0423685 | 0.0202169 |
| CNN-noF | 2 | Jk | 0.33798 / 0.340301 | -0.0932143 / -0.0970432 | 0.340705 | -0.0944559 |
| CNN-noF | 2 | Dk | 0.342716 / 0.344679 | -0.111334 / -0.115621 | 0.345104 | -0.114673 |
| CNN-noF | 3 | J8 | 0.0880493 / 0.0832734 | 0.0268131 / 0.0305081 | 0.110084 | 0.0345654 |
| CNN-noF | 3 | Jk | 0.573718 / 0.57235 | -0.14527 / -0.152485 | 0.576675 | -0.152745 |
| CNN-noF | 3 | Dk | 0.586389 / 0.586486 | -0.172083 / -0.182993 | 0.591721 | -0.187311 |
| CNN-20k | 2 | J8 | 0.0768105 / 0.0768501 | -0.00243529 / 0.00291214 | 0.0844986 | 0.00210029 |
| CNN-20k | 2 | Jk | 0.10553 / 0.10541 | -0.00527216 / 0.00464827 | 0.116142 | 0.00438302 |
| CNN-20k | 2 | Dk | 0.0728086 / 0.0715164 | -0.00283687 / 0.00173613 | 0.0876733 | 0.00228273 |
| CNN-20k | 3 | J8 | 0.153723 / 0.150448 | 0.00299537 / 0.00761523 | 0.180391 | 0.00936918 |
| CNN-20k | 3 | Jk | 0.244195 / 0.243939 | -0.00169585 / 0.0149132 | 0.275431 | 0.0155628 |
| CNN-20k | 3 | Dk | 0.242489 / 0.243316 | -0.00469122 / 0.00729795 | 0.287382 | 0.00619361 |

Draw-cost errors compare each model with the same draw’s physics forecast.

| Model | Lead | Original / fresh seven-pattern S share minus F_c | Fresh betting 99% interval |
|---|---:|---:|---:|
| posterior | 2 | -0.156429 / -0.140714 | [-0.258, -0.032] |
| posterior | 3 | -0.297857 / -0.257143 | [-0.396, -0.136] |
| CNN-F | 2 | -0.155 / -0.139286 | [-0.258, -0.038] |
| CNN-F | 3 | -0.278571 / -0.268571 | [-0.404, -0.142] |
| CNN-noF | 2 | -0.140714 / -0.109286 | [-0.218, -0.002] |
| CNN-noF | 3 | -0.268571 / -0.255 | [-0.398, -0.134] |
| CNN-20k | 2 | -0.173571 / -0.141429 | [-0.248, -0.038] |
| CNN-20k | 3 | -0.263571 / -0.285 | [-0.41, -0.16] |

| Model | Original / fresh fixed-posterior-cohort paired difference | Fresh betting 99% interval | Original / fresh pairs |
|---|---:|---:|---:|
| posterior | -0.308787 / -0.321013 | [-0.488, -0.144] | 1332 / 1299 |
| CNN-F | -0.292096 / -0.307836 | [-0.476, -0.124] | 1332 / 1299 |
| CNN-noF | -0.302504 / -0.256311 | [-0.414, -0.066] | 1332 / 1299 |
| CNN-20k | -0.366912 / -0.425044 | [-0.588, -0.282] | 1332 / 1299 |

The fixed cohort is determined by each panel’s posterior at lead zero; the original and fresh cohorts have their own sizes.

| Model | Lead | Policy | Original / fresh regret | Fresh capture | Fresh acted | Fresh harms | Conditional harm CP95 |
|---|---:|---|---:|---:|---:|---:|---:|
| posterior | 2 | E | 0.0169731 / 0.00480133 | 0.98505 | 200 | 0 | [0, 0.014867] |
| posterior | 2 | C_delta_0 | 0.0209553 / 0.0100704 | 0.968644 | 196 | 0 | [0, 0.0151681] |
| posterior | 3 | E | 0.07843 / 0.0551412 | 0.898245 | 200 | 11 | [0.0311469, 0.0893961] |
| posterior | 3 | C_delta_0 | 0.171445 / 0.17997 | 0.667893 | 143 | 0 | [0, 0.0207313] |
| CNN-F | 2 | E | 0.00894941 / 0.00592277 | 0.981559 | 200 | 0 | [0, 0.014867] |
| CNN-F | 2 | C_delta_0 | 0.0184245 / 0.0110186 | 0.965692 | 197 | 0 | [0, 0.0150917] |
| CNN-F | 3 | E | 0.0850397 / 0.0720539 | 0.867035 | 200 | 13 | [0.0388727, 0.101357] |
| CNN-F | 3 | C_delta_0 | 0.182672 / 0.179759 | 0.668281 | 144 | 0 | [0, 0.0205888] |
| CNN-noF | 2 | E | 0.0535915 / 0.0481995 | 0.849923 | 200 | 2 | [0.00177968, 0.0311426] |
| CNN-noF | 2 | C_delta_0 | 0.0495035 / 0.0481995 | 0.849923 | 200 | 2 | [0.00177968, 0.0311426] |
| CNN-noF | 3 | E | 0.265633 / 0.257246 | 0.52529 | 200 | 27 | [0.0970282, 0.181332] |
| CNN-noF | 3 | C_delta_0 | 0.258528 / 0.257246 | 0.52529 | 200 | 27 | [0.0970282, 0.181332] |
| CNN-20k | 2 | E | 0.0271355 / 0.0152405 | 0.952546 | 200 | 1 | [0.000256434, 0.0234985] |
| CNN-20k | 2 | C_delta_0 | 0.0273705 / 0.0187359 | 0.941663 | 196 | 0 | [0, 0.0151681] |
| CNN-20k | 3 | E | 0.126281 / 0.0861569 | 0.84101 | 200 | 12 | [0.0349821, 0.0954014] |
| CNN-20k | 3 | C_delta_0 | 0.226339 / 0.184642 | 0.659271 | 137 | 1 | [0.000374334, 0.0341572] |

Both conditional harm bounds are exact one-sided 95% bounds. Strict positive realized cost differences count as harm; acted zero-effect ties are recorded separately in the receipt.

Additional state skill, draw-level errors, reliability bins, calibration tests, same-lead differences and paired endpoints are recorded without selection in receipts/acd_stage19_learned.json.
