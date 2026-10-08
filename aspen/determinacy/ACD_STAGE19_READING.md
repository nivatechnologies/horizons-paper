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

## Part 3a — Freeze C

K and V readings are confirmatory on the fresh panel under the pushed Freeze C. The unchanged Stage15/Stage6 interval helpers retain their original POST HOC scope string in the receipt; that string describes their first-panel origin, not the frozen fresh-panel reading. Descriptive replications use realized counts already reported in Part 2; they have no confirmatory criteria. No frozen route is licensed. Known-forcing and matched main readings use the retained known-forcing cohort; K4 uses all main-posterior instances. First-panel values retain their original populations.

| Reading | First panel | Fresh panel | Fresh population / bound | Result |
|---|---:|---:|---|---|
| K1 | -0.363065 [-0.54, -0.204] | -0.405363 [-0.572, -0.268] | 199; two-sided 99% case betting | PASS |
| K2 2 LT | -0.175879 [-0.284, -0.058] | -0.139268 [-0.254, -0.028] | 199; two-sided 99% case betting | PASS |
| K2 3 LT | -0.309404 [-0.432, -0.182] | -0.296482 [-0.438, -0.204] | 199; two-sided 99% case betting | PASS |
| K3 | 0.99638 lower 0.978 | 0.995685 lower 0.977 | 199 retained; 197 contributing; original R0 one-sided 95% | PASS |
| K4 D / J8 | -0.00411491 / 0.543141 | -0.0151889 / 0.572414 | 200; median thresholds; no interval | PASS |
| V1 | descriptive Stage15D; see ratio table | both ratios in range | 200; median thresholds; no interval | PASS |
| V2 | descriptive Stage15D; see ratio table | both ratios in range | 200; median thresholds; no interval | PASS |

K1 eligibility: 1361 pairs in 198 contributing instances, from 199 retained known-forcing instances. First panel: 1356 pairs in 197 contributing instances.

| Lead | Fresh J8 ratio q25 / median / q75 | First J8 q25 / median / q75 | Fresh G ratio q25 / median / q75 | First G q25 / median / q75 |
|---|---:|---:|---:|---:|
| 0 | 0.99977 / 1.00002 / 1.00021 | 0.999779 / 1.00009 / 1.0003 | 0.999395 / 1.00046 / 1.00156 | 0.999214 / 1.00039 / 1.00185 |
| 1 | 0.998775 / 1.00039 / 1.00216 | 0.996034 / 0.99992 / 1.00098 | 0.979463 / 0.999652 / 1.0153 | 0.961098 / 0.999578 / 1.01587 |
| 1.5 | 0.991493 / 1.00068 / 1.01282 | 0.982442 / 1.00068 / 1.02703 | 0.932641 / 1.00339 / 1.06746 | 0.870486 / 0.992024 / 1.07987 |
| 2 | 0.969979 / 1.0038 / 1.06465 | 0.970848 / 1.03257 / 1.14049 | 0.843582 / 1.0094 / 1.23915 | 0.828052 / 1.03632 / 1.38046 |
| 2.5 | 0.938508 / 1.02758 / 1.25395 | 0.912358 / 1.09023 / 1.7451 | 0.650785 / 1.05229 / 1.51335 | 0.680746 / 1.09231 / 2.18837 |
| 3 | 0.789043 / 1.06835 / 1.66035 | 1.06453 / 1.52191 / 2.74931 | 0.665293 / 1.21197 / 2.85827 | 0.523467 / 1.12623 / 3.1944 |
| 4 | 0.910199 / 2.00331 / 5.34213 | 0.982831 / 2.25094 / 5.35471 | 0.867094 / 2.47615 / 9.8303 | 0.545131 / 2.18602 / 10.6705 |
| 6 | 5.42113 / 25.635 / 242.209 | 7.31776 / 25.8843 / 156.525 | 2.11612 / 23.2264 / 515.953 | 3.08682 / 23.2045 / 198.58 |

First tested breakdown leads: {"J8_ratio": 4.0, "G_ratio": 4.0}.
Pilot projection 0.0656932 hours on 4 cores; case set [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199]. First-panel variance population: 40.

| Lead | Known-F S8 / S7 / obs-S / Fc | Matched main S8 / S7 / obs-S / Fc | First known-F S8 / S7 / obs-S / Fc |
|---|---:|---:|---:|
| 0 | 0.984296 / 0.982053 / 0.859296 / 0.994975 | 0.984925 / 0.982771 / 0.859925 / 0.944724 | 0.985553 / 0.983489 / 0.860553 / 0.98995 |
| 1 | 0.927764 / 0.917444 / 0.802764 / 0.969849 | 0.926508 / 0.916009 / 0.801508 / 0.924623 | 0.916457 / 0.904523 / 0.791457 / 0.959799 |
| 1.5 | 0.842965 / 0.820531 / 0.717965 / 0.949749 | 0.836683 / 0.813352 / 0.711683 / 0.944724 | 0.84799 / 0.828428 / 0.724874 / 0.949749 |
| 2 | 0.722362 / 0.684853 / 0.599246 / 0.824121 | 0.71608 / 0.677674 / 0.592965 / 0.819095 | 0.724246 / 0.693467 / 0.606784 / 0.869347 |
| 2.5 | 0.566583 / 0.524767 / 0.566583 / 0.773869 | 0.562814 / 0.521895 / 0.562814 / 0.758794 | 0.580402 / 0.543431 / 0.580402 / 0.758794 |
| 3 | 0.398869 / 0.361809 / 0.398869 / 0.658291 | 0.405151 / 0.366834 / 0.405151 / 0.628141 | 0.41206 / 0.379038 / 0.41206 / 0.688442 |
| 4 | 0.143216 / 0.133525 / 0.143216 / 0.376884 | 0.135678 / 0.126346 / 0.135678 / 0.346734 | 0.148241 / 0.140704 / 0.148241 / 0.371859 |
| 6 | 0.00565327 / 0.00502513 / 0.00565327 / 0.0301508 | 0.00502513 / 0.00502513 / 0.00502513 / 0.0301508 | 0.00690955 / 0.00717875 / 0.00690955 / 0.0452261 |

| Lead | Known-F obs-S case accuracy / lower95 | Matched main | First known-F |
|---|---:|---:|---:|
| 0 | 1 / 0.983 | 1 / 0.983 | 1 / 0.983 |
| 1 | 1 / 0.983 | 0.999282 / 0.982 | 0.998277 / 0.981 |
| 1.5 | 0.996705 / 0.979 | 0.996705 / 0.979 | 0.99798 / 0.98 |
| 2 | 0.995685 / 0.977 | 0.996701 / 0.979 | 0.99638 / 0.978 |
| 2.5 | 0.996237 / 0.978 | 0.996652 / 0.978 | 0.995474 / 0.977 |
| 3 | 0.991811 / 0.971 | 0.992131 / 0.972 | 0.985768 / 0.955 |
| 4 | 0.992424 / 0.957 | 0.992674 / 0.954 | 0.972194 / 0.92 |
| 6 | 1 / 0.088 | 1 / 0.088 | 0.888889 / 0.402 |

| Lead | Known-F pooled obs-S accuracy / Fc pooled accuracy / Fc CP95 | Matched main | First known-F |
|---|---:|---:|---:|
| 0 | 1 / 1 / [0.9849839218112391, 1.0] | 1 / 1 / [0.9841915402609456, 1.0] | 1 / 1 / [0.9849082761460857, 1.0] |
| 1 | 1 / 1 / [0.984597915386921, 1.0] | 0.999216 / 0.994565 / [0.9744789408840627, 0.9997212709478818] | 0.998413 / 1 / [0.98443789845606, 1.0] |
| 1.5 | 0.9965 / 1 / [0.9842745217608315, 1.0] | 0.99647 / 0.994681 / [0.9750165410259732, 0.9997272005442659] | 0.998267 / 1 / [0.9842745217608315, 1.0] |
| 2 | 0.995807 / 1 / [0.9818991640129494, 1.0] | 0.996822 / 1 / [0.9817891332557824, 1.0] | 0.995859 / 1 / [0.9828326951663476, 1.0] |
| 2.5 | 0.996674 / 0.993506 / [0.969567601950211, 0.9996669821225882] | 0.996652 / 1 / [0.9803562170473483, 1.0] | 0.995671 / 0.986755 / [0.9588951352875715, 0.9976415648629795] |
| 3 | 0.988976 / 0.992366 / [0.9643006639009576, 0.9996085247808739] | 0.989147 / 0.992 / [0.9626127058803827, 0.9995897378254504] | 0.993902 / 0.992701 / [0.9658428027696241, 0.9996256664716164] |
| 4 | 0.986842 / 1 / [0.9608441125278288, 1.0] | 0.986111 / 0.985507 / [0.933085671104667, 0.9992568951611785] | 0.970339 / 0.986486 / [0.9374927734145206, 0.9993070875479275] |
| 6 | 1 / 1 / [0.6069622310029172, 1.0] | 1 / 1 / [0.6069622310029172, 1.0] | 0.909091 / 1 / [0.7168711644368865, 1.0] |

| Lead | Known-F rho / c / zD / zF medians | Matched main medians | First known-F medians |
|---|---:|---:|---:|
| 0 | 0.999908 / 0.000104729 / 67.9559 / 52.7361 | 0.999992 / 1.09531e-05 / 64.5247 / 15.6947 | 0.999909 / 0.00010385 / 65.1069 / 56.5284 |
| 1 | 0.997823 / 0.00282726 / 14.9647 / 20.4047 | 0.999355 / 0.000744282 / 14.534 / 11.2958 | 0.997419 / 0.00337715 / 13.9338 / 19.546 |
| 1.5 | 0.989603 / 0.0139181 / 7.17482 / 12.3302 | 0.995078 / 0.00579971 / 6.98885 / 8.34566 | 0.990551 / 0.0133669 / 7.47422 / 13.4776 |
| 2 | 0.960772 / 0.0530445 / 3.44516 / 6.47445 | 0.974855 / 0.0308323 / 3.42972 / 5.12875 | 0.96416 / 0.047993 / 3.68719 / 7.52029 |
| 2.5 | 0.877447 / 0.152208 / 2.05321 / 4.58212 | 0.899258 / 0.115485 / 2.01018 / 4.00132 | 0.896015 / 0.128649 / 2.14673 / 4.28578 |
| 3 | 0.708133 / 0.322502 / 1.26511 / 2.68189 | 0.736686 / 0.288825 / 1.23623 / 2.28453 | 0.743479 / 0.286843 / 1.24056 / 2.40936 |
| 4 | 0.307963 / 0.707279 / 0.62078 / 1.11096 | 0.332213 / 0.681252 / 0.59869 / 1.0691 | 0.335824 / 0.677016 / 0.607542 / 1.24971 |
| 6 | 0.0706917 / 0.93024 / 0.253377 / 0.392056 | 0.0723856 / 0.928151 / 0.259309 / 0.411445 | 0.0629009 / 0.937436 / 0.262531 / 0.376042 |

First-panel matched-main accuracy, confidence-share and mechanism-summary rows were not recorded on the exact retained known-forcing cohort; those exact first-panel counterparts are unavailable.

Known-F minus matched main confidence-share differences (two-sided99% case betting; first-panel paired-share intervals were not reported and are unavailable):
- seven_S, 2 LT: 0.00717875 [-0.054, 0.068].
- Fc, 2 LT: 0.00502513 [-0.064, 0.074].
- seven_S, 3 LT: -0.00502513 [-0.068, 0.056].
- Fc, 3 LT: 0.0301508 [-0.042, 0.106].

Main forcing SD, matched cohort: {"min": 0.026175663476999428, "q25": 0.028677406590638416, "median": 0.029298970215336208, "q75": 0.03002132085125176, "max": 0.03249165256768422, "mean": 0.02935476455135902}. First panel: {"min": 0.026489593760281167, "q25": 0.028404265196804772, "median": 0.02908031649215305, "q75": 0.029767902535608327, "max": 0.03288643657959866, "mean": 0.029140887819048274}.
Main forcing correlations, all cases: [{"lead": 2.0, "J8": {"min": 0.024269416975177, "q25": 0.376368031673773, "median": 0.5724135321578196, "q75": 0.7353962561197889, "max": 0.9448985599469729, "mean": 0.5496389339486227}, "D": {"min": -0.653724394299195, "q25": -0.15409274583769828, "median": -0.015188942944643128, "q75": 0.1166931110988882, "max": 0.7673756041874251, "mean": -0.01667946873901411}}, {"lead": 3.0, "J8": {"min": -0.15286678477523302, "q25": 0.11608879038540033, "median": 0.26177634035247205, "q75": 0.4400570825743083, "max": 0.7731472772807816, "mean": 0.2708999893025928}, "D": {"min": -0.571992625213161, "q25": -0.09772845213478562, "median": 0.007528770283753098, "q75": 0.09802457679468052, "max": 0.5554136455225646, "mean": -3.6437509016801207e-06}}]. Matched-cohort correlations: [{"lead": 2.0, "J8": {"min": 0.024269416975177, "q25": 0.3758309191628083, "median": 0.5698288569278763, "q75": 0.7383280888476298, "max": 0.9448985599469729, "mean": 0.5490877127738876}, "D": {"min": -0.653724394299195, "q25": -0.15409274583769828, "median": -0.015310362228048926, "q75": 0.11754684812552041, "max": 0.7673756041874251, "mean": -0.016658825073672084}}, {"lead": 3.0, "J8": {"min": -0.15286678477523302, "q25": 0.11528051277511348, "median": 0.2592837753465723, "q75": 0.4391593967987143, "max": 0.7731472772807816, "mean": 0.26946946554257534}, "D": {"min": -0.571992625213161, "q25": -0.09787726137444563, "median": 0.0065955825596289794, "q75": 0.09745850527923507, "max": 0.5554136455225646, "mean": -0.0005359159698472563}}].

First-panel forcing SD and correlations use the original main panel; fresh descriptive forcing summaries use the matched known-forcing cohort.

Main forcing correlation medians, first panel / fresh matched cohort (different panel populations):
- 2 LT: F with J8 0.543141 / 0.569829; F with D -0.00411491 / -0.0153104.
- 3 LT: F with J8 0.253866 / 0.259284; F with D 0.000118045 / 0.00659558.

| Model | Lead | Patterns | Coverage | Fresh pooled error / case error / upper95 | First-panel pooled / case / upper95 |
|---|---:|---|---:|---:|---:|
| posterior | 2 | all_eight | 0.5 | 0 / 0 / 0.018 | 0 / 0 / 0.018 |
| posterior | 2 | all_eight | 0.7 | 0.000892857 / 0.001 / 0.018 | 0.00357143 / 0.00337302 / 0.021 |
| posterior | 2 | seven_zero_mean | 0.5 | 0 / 0 / 0.018 | 0 / 0 / 0.019 |
| posterior | 2 | seven_zero_mean | 0.7 | 0.00408163 / 0.0040404 / 0.022 | 0.00612245 / 0.0056044 / 0.024 |
| posterior | 3 | all_eight | 0.5 | 0.0225 / 0.0208396 / 0.042 | 0.02125 / 0.0280373 / 0.06 |
| posterior | 3 | all_eight | 0.7 | 0.0651786 / 0.0731131 / 0.11 | 0.0723214 / 0.0795525 / 0.116 |
| posterior | 3 | seven_zero_mean | 0.5 | 0.0271429 / 0.0237967 / 0.045 | 0.03 / 0.0305314 / 0.052 |
| posterior | 3 | seven_zero_mean | 0.7 | 0.0734694 / 0.0832143 / 0.125 | 0.0836735 / 0.0951663 / 0.131 |
| CNN-20k | 2 | all_eight | 0.5 | 0.0175 / 0.0122768 / 0.031 | 0.0225 / 0.0208145 / 0.042 |
| CNN-20k | 2 | all_eight | 0.7 | 0.0375 / 0.0325595 / 0.051 | 0.05 / 0.0544345 / 0.085 |
| CNN-20k | 2 | seven_zero_mean | 0.5 | 0.0257143 / 0.0189716 / 0.039 | 0.0314286 / 0.0320713 / 0.065 |
| CNN-20k | 2 | seven_zero_mean | 0.7 | 0.0540816 / 0.0478608 / 0.069 | 0.0642857 / 0.0629683 / 0.092 |
| CNN-20k | 3 | all_eight | 0.5 | 0.06125 / 0.0573822 / 0.088 | 0.07875 / 0.0766781 / 0.104 |
| CNN-20k | 3 | all_eight | 0.7 | 0.105357 / 0.112102 / 0.148 | 0.125893 / 0.137569 / 0.161 |
| CNN-20k | 3 | seven_zero_mean | 0.5 | 0.0771429 / 0.075448 / 0.117 | 0.0957143 / 0.0990375 / 0.128 |
| CNN-20k | 3 | seven_zero_mean | 0.7 | 0.117347 / 0.123202 / 0.165 | 0.141837 / 0.151723 / 0.174 |
| CNN-F | 2 | all_eight | 0.5 | 0 / 0 / 0.018 | 0.00125 / 0.000868056 / 0.019 |
| CNN-F | 2 | all_eight | 0.7 | 0.000892857 / 0.001 / 0.018 | 0.00625 / 0.00556758 / 0.023 |
| CNN-F | 2 | seven_zero_mean | 0.5 | 0 / 0 / 0.018 | 0.00142857 / 0.00108696 / 0.02 |
| CNN-F | 2 | seven_zero_mean | 0.7 | 0.00612245 / 0.00580808 / 0.024 | 0.0112245 / 0.00932945 / 0.028 |
| CNN-F | 3 | all_eight | 0.5 | 0.025 / 0.0235261 / 0.045 | 0.02 / 0.0257873 / 0.057 |
| CNN-F | 3 | all_eight | 0.7 | 0.0669643 / 0.0720893 / 0.104 | 0.075 / 0.0868509 / 0.125 |
| CNN-F | 3 | seven_zero_mean | 0.5 | 0.0385714 / 0.0369111 / 0.063 | 0.0228571 / 0.0271083 / 0.046 |
| CNN-F | 3 | seven_zero_mean | 0.7 | 0.0744898 / 0.0817857 / 0.121 | 0.0897959 / 0.105611 / 0.129 |
| CNN-noF | 2 | all_eight | 0.5 | 0.04 / 0.0461881 / 0.072 | 0.0375 / 0.0389971 / 0.066 |
| CNN-noF | 2 | all_eight | 0.7 | 0.05625 / 0.0585536 / 0.083 | 0.0598214 / 0.0562381 / 0.079 |
| CNN-noF | 2 | seven_zero_mean | 0.5 | 0.0471429 / 0.0536842 / 0.085 | 0.0442857 / 0.0451094 / 0.072 |
| CNN-noF | 2 | seven_zero_mean | 0.7 | 0.0693878 / 0.0767262 / 0.115 | 0.0734694 / 0.0709814 / 0.096 |
| CNN-noF | 3 | all_eight | 0.5 | 0.08625 / 0.106863 / 0.154 | 0.07875 / 0.10272 / 0.142 |
| CNN-noF | 3 | all_eight | 0.7 | 0.126786 / 0.135315 / 0.175 | 0.121429 / 0.128911 / 0.164 |
| CNN-noF | 3 | seven_zero_mean | 0.5 | 0.0842857 / 0.0811996 / 0.131 | 0.0728571 / 0.0705167 / 0.103 |
| CNN-noF | 3 | seven_zero_mean | 0.7 | 0.133673 / 0.144131 / 0.194 | 0.128571 / 0.129076 / 0.167 |

Matched-coverage case error bounds are one-sided95% v2.3 bounds; population is the full panel and case bounds omit cases with no contributing selected answers.

| Model | Lead | Policy | Fresh expected / realized harms | First expected / realized harms | Fresh actions |
|---|---:|---|---:|---:|---:|
| posterior | 2 | E | 0.639844 / 0 | 1.27683 / 1 | 200 |
| posterior | 2 | C_delta_0 | 0.23275 / 0 | 0.116719 / 0 | 196 |
| posterior | 3 | E | 10.3358 / 11 | 11.4082 / 9 | 200 |
| posterior | 3 | C_delta_0 | 0.911469 / 0 | 0.938516 / 0 | 143 |
| CNN-20k | 2 | E | 0.776734 / 1 | 1.75636 / 3 | 200 |
| CNN-20k | 2 | C_delta_0 | 0.230875 / 0 | 0.138656 / 1 | 196 |
| CNN-20k | 3 | E | 12.0682 / 12 | 12.5455 / 21 | 200 |
| CNN-20k | 3 | C_delta_0 | 0.750047 / 1 | 0.714859 / 3 | 137 |
| CNN-F | 2 | E | 0.503359 / 0 | 0.98275 / 1 | 200 |
| CNN-F | 2 | C_delta_0 | 0.172859 / 0 | 0.215812 / 1 | 197 |
| CNN-F | 3 | E | 9.82958 / 13 | 11.7696 / 11 | 200 |
| CNN-F | 3 | C_delta_0 | 0.790031 / 0 | 0.858312 / 1 | 144 |
| CNN-noF | 2 | E | 0.0078125 / 2 | 0.117188 / 6 | 200 |
| CNN-noF | 2 | C_delta_0 | 0.0078125 / 2 | 0 / 5 | 200 |
| CNN-noF | 3 | E | 0.0234375 / 27 | 0.148516 / 30 | 200 |
| CNN-noF | 3 | C_delta_0 | 0.0234375 / 27 | 0.0585156 / 29 | 200 |

Stage17C counts non-lowering effects as harm; Part2 strict-positive harm counts and zero-effect ties are recorded separately.

| Model, 2 LT | Fresh median bound / share below0.05 / vacuous share | First-panel values |
|---|---:|---:|
| CNN-F | 0.0630595 / 0.475625 / 0.01375 | 0.0576382 / 0.4825 / 0.016875 |
| CNN-noF | 0.721513 / 0.1025 / 0.396875 | 0.641866 / 0.108125 / 0.39125 |

R-other resolutions: [].

## L3 training-seed replication

All eight new selected checkpoints are committed and all fresh inference manifests were verified before scoring. L3a and L3b use the unchanged frozen aggregation, case contribution rule and failed-run rule. Training-run variation is separate from case-level bounds.

L3a: {'lower': 0.0040000000000000036, 'upper': 0.1299999999999999, 'empty': False, 'point': 0.06708841828188562, 'offset': False, 'fallback': False}. L3b positive new pair count: 4. Confirmed: True.

| Seed | L1 estimate | 99% interval | CNN-F pooled S error | CNN-noF pooled S error |
|---|---:|---|---:|---:|
| 0 | 0.06874699374699375 | [0.0040000000000000036, 0.1319999999999999] | 0.0017391304347825765 | 0.06073211314475868 |
| 1 | 0.07231990231990232 | [0.006000000000000005, 0.1359999999999999] | 0.0017559262510974394 | 0.062342038753159246 |
| 2 | 0.06481481481481483 | [0.0, 0.1279999999999999] | 0.0034995625546806464 | 0.05901911886949296 |
| 3 | 0.06550640560792845 | [0.0020000000000000018, 0.1299999999999999] | 0.0017528483786152238 | 0.061499578770008445 |
| 4 | 0.06563771237138072 | [0.0020000000000000018, 0.1279999999999999] | 0.0026109660574412663 | 0.06120760959470639 |

Full per-seed state skill, confident errors and bounds, gate harm bounds, uniform-decrease choices and other descriptive metrics are in receipts/acd_stage19_L3.json.
