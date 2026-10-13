# Stage 23 — corrected response-training recipe

Frozen Q1 and Q2 results on the Stage 22 panel. Other readings are descriptive; the original-panel derivative and restricted-menu readings are POST HOC and license no frozen route. All tables below are generated from receipts/acd_stage23.json by acd_stage23_report.py.

Weight 0.03 was selected by the frozen validation rule. Q1 did not confirm, so no further training seeds are triggered.

| Reading | Point | Interval / bound | Bound type | Contributing n | Outcome |
|---|---:|---|---|---:|---|
| Q1: retained CNN-noF minus selected model, seven patterns, 2 LT | -0.00586383 | [-0.02, 0.008] | two-sided 99% v2.3 instance betting | 968 | FAIL |
| Q2: strict-positive harm conditional on C(delta=0) acting, 3 LT | 0.126904 | upper 0.145689 | exact one-sided 95% Clopper–Pearson upper | 985 actions; 997 retained instances | FAIL |

Descriptive selected-minus-E0-fixed, seven patterns at 2 LT: {"lower": 0.04800000000000004, "upper": 0.08400000000000007, "empty": false, "point": 0.06451397087760724, "offset": false, "fallback": false, "bound_type": "two-sided99% v2.3 instance betting"}.

## Validation, both recipes

| Weight | Original state MSE / weight zero | Original effect RMSE | Corrected state MSE / weight zero | Corrected effect RMSE | Corrected checkpoint step |
|---:|---:|---:|---:|---:|---:|
| 0 | 1 | 0.36155 | 1 | 0.36155 | 20000 |
| 0.01 | 21.1188 | 0.202513 | 0.967738 | 0.359296 | 20000 |
| 0.03 | 291.457 | 0.239271 | 0.972668 | 0.353708 | 20000 |
| 0.1 | 45.1801 | 0.211962 | 1.40157 | 0.317145 | 15000 |
| 0.3 | 81.0224 | 0.240397 | 2.20637 | 0.349912 | 20000 |
| 1 | 649.285 | 0.240561 | 342.271 | 0.637563 | 19000 |

Original-recipe guard-aborted weights are retained descriptively at their last validation-eligible checkpoint. The exact guard-abort details and checkpoint steps are listed below. The corrected weight 0.1 run reached its authorized time cap; the other corrected runs completed their schedules. The cap continuation replayed updates from the last optimizer checkpoint and charged that replay time. Full execution records remain in the receipt.

## Training execution

| Weight | Scheduled updates | Skips | Selected step | Charged GPU seconds | Cap seconds | Abort |
|---:|---:|---:|---:|---:|---:|---|
| 0.01 | 20000 | 0 | 20000 | 28593.4 | 36000 | none |
| 0.03 | 20000 | 0 | 20000 | 24499.5 | 36000 | none |
| 0.1 | 15649 | 0 | 15000 | 43078.8 | 43200 | none |
| 0.3 | 20000 | 0 | 20000 | 24468.1 | 36000 | none |
| 1 | 20000 | 0 | 19000 | 28726.5 | 36000 | none |

No corrected-model update was skipped. Every saved hundred-update loss and gradient record, the initial loss-value diagnostic ratio, applied gradient scale and combined preclip norm are in the JSON receipt. The loss-value ratio was diagnostic only; the update used separate gradient norms. Figure: figures/F_stage23_training_losses.pdf. Base loss uses solid circles; raw paired loss dashed squares; base gradient norm dash-dot triangles; paired gradient norm dotted crosses. Both loss and norm axes are logarithmic.

## Descriptive model readings

| Panel / population | Lead | State RMSE / sigma | State ACC | Confident S share (all eight) | Pooled confident S error | Case confident S error | Case error interval, one-sided 95% bounds |
|---|---:|---:|---:|---:|---:|---:|---|
| Stage22 / pooled | 2 | 0.135127 | 0.978121 | 0.738089 | 0.0638695 | 0.0684542 | [0.057, 0.075] |
| Stage22 / pooled | 3 | 0.291538 | 0.913912 | 0.479062 | 0.0811306 | 0.121332 | [0.105, 0.157] |
| Stage22 / F7 | 2 | 0.0717984 | 0.99234 | 0.841114 | 0.0692331 | 0.0703576 | [0.058, 0.085] |
| Stage22 / F7 | 3 | 0.156904 | 0.966905 | 0.635793 | 0.058034 | 0.0642857 | [0.054, 0.091] |
| Stage22 / F9 | 2 | 0.198329 | 0.96393 | 0.635271 | 0.0567823 | 0.0665545 | [0.049, 0.088] |
| Stage22 / F9 | 3 | 0.425903 | 0.861026 | 0.322645 | 0.126553 | 0.179547 | [0.148, 0.237] |
| Part3b / all retained | 2 | 0.114432 | 0.985767 | 0.75125 | 0.0665557 | 0.0673869 | [0.045, 0.09] |
| Part3b / all retained | 3 | 0.264298 | 0.933892 | 0.47 | 0.081117 | 0.104494 | [0.074, 0.154] |

The JSON also reports pooled and equal-case J8/Jk/Dk RMSE and bias, seven-pattern reliability and coverage, calibration tests, same-lead differences, own/fixed-cohort paired endpoints, and per-pattern-group effect errors. Stage22 populations are reported pooled and separately by forcing; Part3b retains its existing population.

## Descriptive cost errors

| Panel / population | Lead | Quantity | Pooled RMSE | Pooled bias | Equal-case RMSE | Equal-case bias |
|---|---:|---|---:|---:|---:|---:|
| Stage22 / pooled | 2 | J8 | 0.0705478 | 0.000576928 | 0.043344 | -0.000205191 |
| Stage22 / pooled | 2 | Jk | 0.354277 | -0.114006 | 0.349539 | -0.115378 |
| Stage22 / pooled | 2 | Dk | 0.352118 | -0.114583 | 0.347853 | -0.115172 |
| Stage22 / pooled | 3 | J8 | 0.216913 | -0.000670971 | 0.134991 | 0.000646912 |
| Stage22 / pooled | 3 | Jk | 0.618142 | -0.181376 | 0.603405 | -0.181118 |
| Stage22 / pooled | 3 | Dk | 0.635981 | -0.180705 | 0.617884 | -0.181765 |
| Stage22 / F7 | 2 | J8 | 0.0192535 | 0.00267482 | 0.0145043 | 0.00296623 |
| Stage22 / F7 | 2 | Jk | 0.32144 | -0.104803 | 0.31909 | -0.104302 |
| Stage22 / F7 | 2 | Dk | 0.321819 | -0.107478 | 0.319575 | -0.107269 |
| Stage22 / F7 | 3 | J8 | 0.0386943 | 0.00426123 | 0.0290389 | 0.00458015 |
| Stage22 / F7 | 3 | Jk | 0.517921 | -0.16136 | 0.513578 | -0.161535 |
| Stage22 / F7 | 3 | Dk | 0.519175 | -0.165621 | 0.514945 | -0.166115 |
| Stage22 / F9 | 2 | J8 | 0.0975877 | -0.00149368 | 0.0721259 | -0.00337025 |
| Stage22 / F9 | 2 | Jk | 0.383942 | -0.123089 | 0.379927 | -0.126431 |
| Stage22 / F9 | 2 | Dk | 0.379659 | -0.121596 | 0.376074 | -0.123061 |
| Stage22 / F9 | 3 | J8 | 0.303336 | -0.00553901 | 0.240731 | -0.00327845 |
| Stage22 / F9 | 3 | Jk | 0.703191 | -0.201132 | 0.693053 | -0.200661 |
| Stage22 / F9 | 3 | Dk | 0.733244 | -0.195593 | 0.720616 | -0.197383 |
| Part3b / all retained | 2 | J8 | 0.043247 | 0.0158432 | 0.0326153 | 0.0144171 |
| Part3b / all retained | 2 | Jk | 0.347308 | -0.102562 | 0.347144 | -0.10492 |
| Part3b / all retained | 2 | Dk | 0.350775 | -0.118405 | 0.350313 | -0.119337 |
| Part3b / all retained | 3 | J8 | 0.135086 | 0.0280543 | 0.0911907 | 0.0252895 |
| Part3b / all retained | 3 | Jk | 0.587175 | -0.162148 | 0.58271 | -0.163297 |
| Part3b / all retained | 3 | Dk | 0.602071 | -0.190202 | 0.595361 | -0.188587 |

## Descriptive confidence, same-lead and paired readings

| Panel / population | Lead | Seven-pattern S share | Observation-confident S share | F_c share | Seven S minus F_c, two-sided 99% interval |
|---|---:|---:|---:|---:|---|
| Stage22 / pooled | 2 | 0.70096 | 0.61334 | 0.841525 | -0.140565 [-0.178, -0.078] |
| Stage22 / pooled | 3 | 0.406362 | 0.416625 | 0.634905 | -0.228543 [-0.276, -0.158] |
| Stage22 / F7 | 2 | 0.818417 | 0.716114 | 0.881526 | -0.0631096 [-0.122, 0.008] |
| Stage22 / F7 | 3 | 0.583764 | 0.510793 | 0.773092 | -0.189329 [-0.256, -0.108] |
| Stage22 / F9 | 2 | 0.583739 | 0.510772 | 0.801603 | -0.217864 [-0.28, -0.14] |
| Stage22 / F9 | 3 | 0.229316 | 0.322645 | 0.496994 | -0.267678 [-0.346, -0.186] |
| Part3b / all retained | 2 | 0.715714 | 0.62625 | 0.82 | -0.104286 [-0.216, -0.006] |
| Part3b / all retained | 3 | 0.394286 | 0.47 | 0.645 | -0.250714 [-0.39, -0.142] |

| Panel / population | Eligibility | Pairs | Instances | Later minus earlier, two-sided 99% interval | Case earlier / later / same |
|---|---|---:|---:|---|---|
| Stage22 / pooled | paired_endpoint | 6456 | 941 | -0.243505 [-0.302, -0.116] | {'earlier': 0.5438844188047164, 'later': 0.3003795354486109, 'same': 0.15573604574667269} |
| Stage22 / pooled | paired_endpoint_fixed_posterior_cohort | 6484 | 942 | -0.252785 [-0.31, -0.128] | {'earlier': 0.5507835405924577, 'later': 0.29799818016378526, 'same': 0.15121827924375691} |
| Stage22 / F7 | paired_endpoint | 3217 | 468 | -0.162607 [-0.26, -0.01] | {'earlier': 0.50489417989418, 'later': 0.3422873422873423, 'same': 0.15281847781847777} |
| Stage22 / F7 | paired_endpoint_fixed_posterior_cohort | 3217 | 467 | -0.175844 [-0.272, -0.024] | {'earlier': 0.5131538696849189, 'later': 0.3373100846334251, 'same': 0.14953604568165593} |
| Stage22 / F9 | paired_endpoint | 3239 | 473 | -0.323548 [-0.418, -0.184] | {'earlier': 0.5824624987415684, 'later': 0.2589147286821705, 'same': 0.15862277257626092} |
| Stage22 / F9 | paired_endpoint_fixed_posterior_cohort | 3267 | 475 | -0.328431 [-0.424, -0.192] | {'earlier': 0.5877794486215538, 'later': 0.25934837092731833, 'same': 0.1528721804511278} |
| Part3b / all retained | paired_endpoint | 1302 | 189 | -0.237087 [-0.414, -0.054] | {'earlier': 0.5415721844293272, 'later': 0.3044847568657092, 'same': 0.15394305870496341} |
| Part3b / all retained | paired_endpoint_fixed_posterior_cohort | 1299 | 189 | -0.243462 [-0.42, -0.062] | {'earlier': 0.5469639707734945, 'later': 0.3035021415973797, 'same': 0.1495338876291257} |

| Panel / population | Lead | Threshold | Cases | Calibration point | Two-sided 99% v2.3 interval | Reject mean calibration |
|---|---:|---:|---:|---:|---|---|
| Stage22 / pooled | 2 | 0.5 | 997 | 0.064101 | [0.05, 0.084] | True |
| Stage22 / pooled | 2 | 0.95 | 975 | 0.0653623 | [0.05, 0.086] | True |
| Stage22 / pooled | 3 | 0.5 | 997 | 0.0442888 | [0.024, 0.064] | True |
| Stage22 / pooled | 3 | 0.95 | 801 | 0.0543236 | [0.032, 0.08] | True |
| Stage22 / F7 | 2 | 0.5 | 498 | 0.081016 | [0.054, 0.11] | True |
| Stage22 / F7 | 2 | 0.95 | 498 | 0.0812295 | [0.054, 0.11] | True |
| Stage22 / F7 | 3 | 0.5 | 498 | 0.0566895 | [0.03, 0.086] | True |
| Stage22 / F7 | 3 | 0.95 | 473 | 0.0547522 | [0.026, 0.086] | True |
| Stage22 / F9 | 2 | 0.5 | 499 | 0.0472198 | [0.022, 0.076] | True |
| Stage22 / F9 | 2 | 0.95 | 477 | 0.0487964 | [0.02, 0.078] | True |
| Stage22 / F9 | 3 | 0.5 | 499 | 0.031913 | [0, 0.062] | False |
| Stage22 / F9 | 3 | 0.95 | 328 | 0.0537057 | [0.01, 0.104] | True |
| Part3b / all retained | 2 | 0.5 | 200 | 0.064575 | [0, 0.128] | False |
| Part3b / all retained | 2 | 0.95 | 200 | 0.075224 | [0.01, 0.14] | True |
| Part3b / all retained | 3 | 0.5 | 200 | 0.0445409 | [-0.02, 0.11] | False |
| Part3b / all retained | 3 | 0.95 | 169 | 0.0496951 | [-0.028, 0.128] | False |

## POST HOC full and restricted menus

Restricted menu: seven zero-mean patterns plus no action; E keeps the existing argmin tie order, and C gates only that E choice. Harms are strictly positive effects; zero-effect ties are recorded separately. Expected harms sum the chosen actions’ predicted probabilities of not lowering energy.

| Panel / population | Menu | Lead | Policy | Actions | Harms | Expected harms | Regret | Capture | Conditional harm one-sided 95% CP bounds | Action histogram |
|---|---|---:|---|---:|---:|---:|---:|---:|---|---|
| Stage22 / pooled | full | 2 | E | 997 | 26 | 0.435453 | 0.0709677 | 0.786959 | [0.01833608969320433, 0.03600179690786973] | [994, 0, 0, 1, 0, 0, 0, 2, 0] |
| Stage22 / pooled | full | 2 | C_delta_0 | 995 | 25 | 0.0159531 | 0.0710059 | 0.786844 | [0.01752809025177503, 0.034916226786156135] | [992, 0, 0, 1, 0, 0, 0, 2, 2] |
| Stage22 / pooled | full | 3 | E | 997 | 132 | 2.69516 | 0.301475 | 0.471449 | [0.11506193880254982, 0.1513626725792488] | [993, 0, 0, 0, 2, 1, 0, 1, 0] |
| Stage22 / pooled | full | 3 | C_delta_0 | 985 | 125 | 0.554875 | 0.299839 | 0.474316 | [0.10979465859951704, 0.14568856560301185] | [981, 0, 0, 0, 2, 1, 0, 1, 12] |
| Stage22 / pooled | seven_zero_mean_plus_no_action | 2 | E | 991 | 47 | 20.7163 | 0.0320321 | 0.864601 | [0.03683160227288981, 0.06008227101075199] | [0, 149, 148, 168, 155, 147, 50, 174, 6] |
| Stage22 / pooled | seven_zero_mean_plus_no_action | 2 | C_delta_0 | 888 | 30 | 2.05756 | 0.0592485 | 0.749557 | [0.024420155057120294, 0.04554571624288807] | [0, 141, 132, 148, 133, 130, 37, 167, 109] |
| Stage22 / pooled | seven_zero_mean_plus_no_action | 3 | E | 978 | 126 | 80.4335 | 0.143756 | 0.71943 | [0.1115482489872749, 0.14779965862687908] | [0, 130, 139, 147, 167, 156, 74, 165, 19] |
| Stage22 / pooled | seven_zero_mean_plus_no_action | 3 | C_delta_0 | 612 | 25 | 4.25077 | 0.275941 | 0.461445 | [0.028557988505826425, 0.05658825348864249] | [0, 95, 92, 98, 93, 98, 37, 99, 385] |
| Stage22 / F7 | full | 2 | E | 498 | 1 | 0 | 0.0154598 | 0.940515 | [0.00010299327893557907, 0.009490100551225606] | [498, 0, 0, 0, 0, 0, 0, 0, 0] |
| Stage22 / F7 | full | 2 | C_delta_0 | 498 | 1 | 0 | 0.0154598 | 0.940515 | [0.00010299327893557907, 0.009490100551225606] | [498, 0, 0, 0, 0, 0, 0, 0, 0] |
| Stage22 / F7 | full | 3 | E | 498 | 22 | 0 | 0.11608 | 0.696764 | [0.030093420653999024, 0.06248321593329228] | [498, 0, 0, 0, 0, 0, 0, 0, 0] |
| Stage22 / F7 | full | 3 | C_delta_0 | 498 | 22 | 0 | 0.11608 | 0.696764 | [0.030093420653999024, 0.06248321593329228] | [498, 0, 0, 0, 0, 0, 0, 0, 0] |
| Stage22 / F7 | seven_zero_mean_plus_no_action | 2 | E | 496 | 18 | 2.12639 | 0.0159659 | 0.888018 | [0.023584845136544446, 0.05334130563854821] | [0, 73, 76, 76, 83, 75, 22, 91, 2] |
| Stage22 / F7 | seven_zero_mean_plus_no_action | 2 | C_delta_0 | 484 | 16 | 0.549594 | 0.0179019 | 0.874439 | [0.020843102843710003, 0.04977764372899422] | [0, 73, 74, 73, 81, 73, 19, 91, 14] |
| Stage22 / F7 | seven_zero_mean_plus_no_action | 3 | E | 491 | 37 | 17.981 | 0.0473294 | 0.850289 | [0.056694653479374454, 0.09794459410102042] | [0, 74, 67, 74, 82, 74, 37, 83, 7] |
| Stage22 / F7 | seven_zero_mean_plus_no_action | 3 | C_delta_0 | 402 | 14 | 1.54734 | 0.0873604 | 0.723664 | [0.021174934845232543, 0.05390914702744496] | [0, 66, 55, 63, 62, 62, 26, 68, 96] |
| Stage22 / F9 | full | 2 | E | 499 | 25 | 0.435453 | 0.126364 | 0.688905 | [0.035069094893270605, 0.06927322119705821] | [496, 0, 0, 1, 0, 0, 0, 2, 0] |
| Stage22 / F9 | full | 2 | C_delta_0 | 497 | 24 | 0.0159531 | 0.126441 | 0.688718 | [0.03351775263986233, 0.06724272730508839] | [494, 0, 0, 1, 0, 0, 0, 2, 2] |
| Stage22 / F9 | full | 3 | E | 499 | 110 | 2.69516 | 0.486497 | 0.357825 | [0.19020456682826703, 0.2531645484696889] | [495, 0, 0, 0, 2, 1, 0, 1, 0] |
| Stage22 / F9 | full | 3 | C_delta_0 | 487 | 103 | 0.554875 | 0.48323 | 0.362139 | [0.18139670290981555, 0.24423408642009786] | [483, 0, 0, 0, 2, 1, 0, 1, 12] |
| Stage22 / F9 | seven_zero_mean_plus_no_action | 2 | E | 495 | 29 | 18.5899 | 0.0480661 | 0.854516 | [0.04222459687058751, 0.07902437172183523] | [0, 76, 72, 92, 72, 72, 28, 83, 4] |
| Stage22 / F9 | seven_zero_mean_plus_no_action | 2 | C_delta_0 | 404 | 14 | 1.50797 | 0.100512 | 0.695774 | [0.021069507653357446, 0.05364490884701441] | [0, 68, 58, 75, 52, 57, 18, 76, 95] |
| Stage22 / F9 | seven_zero_mean_plus_no_action | 3 | E | 487 | 89 | 62.4525 | 0.23999 | 0.661134 | [0.1544090985569522, 0.21399574291828172] | [0, 56, 72, 73, 85, 82, 37, 82, 12] |
| Stage22 / F9 | seven_zero_mean_plus_no_action | 3 | C_delta_0 | 210 | 11 | 2.70342 | 0.464145 | 0.344628 | [0.029649702547988873, 0.08521367777370091] | [0, 29, 37, 35, 31, 36, 11, 31, 289] |
| Part3b / all retained | full | 2 | E | 200 | 2 | 0.00195312 | 0.0481995 | 0.849923 | [0.0017796814478925685, 0.031142599414083726] | [200, 0, 0, 0, 0, 0, 0, 0, 0] |
| Part3b / all retained | full | 2 | C_delta_0 | 200 | 2 | 0.00195312 | 0.0481995 | 0.849923 | [0.0017796814478925685, 0.031142599414083726] | [200, 0, 0, 0, 0, 0, 0, 0, 0] |
| Part3b / all retained | full | 3 | E | 200 | 27 | 0.0278437 | 0.257246 | 0.52529 | [0.09702824556141776, 0.1813316880134572] | [200, 0, 0, 0, 0, 0, 0, 0, 0] |
| Part3b / all retained | full | 3 | C_delta_0 | 200 | 27 | 0.0278437 | 0.257246 | 0.52529 | [0.09702824556141776, 0.1813316880134572] | [200, 0, 0, 0, 0, 0, 0, 0, 0] |
| Part3b / all retained | seven_zero_mean_plus_no_action | 2 | E | 199 | 10 | 2.464 | 0.0258656 | 0.883202 | [0.027513086211224915, 0.08374646672212027] | [0, 38, 22, 35, 34, 42, 5, 23, 1] |
| Part3b / all retained | seven_zero_mean_plus_no_action | 2 | C_delta_0 | 186 | 6 | 0.485609 | 0.0302238 | 0.863523 | [0.014139790122403503, 0.06267211980035657] | [0, 36, 22, 32, 33, 35, 5, 23, 14] |
| Part3b / all retained | seven_zero_mean_plus_no_action | 3 | E | 195 | 26 | 15.0086 | 0.118193 | 0.756215 | [0.09513471925948679, 0.18015504310247415] | [0, 27, 25, 29, 28, 35, 15, 36, 5] |
| Part3b / all retained | seven_zero_mean_plus_no_action | 3 | C_delta_0 | 119 | 4 | 1.24627 | 0.219999 | 0.546228 | [0.01156155754031149, 0.07526645610841459] | [0, 18, 17, 17, 16, 17, 7, 27, 81] |

## POST HOC original-panel derivatives

| Lead | Per-draw sign agreement | Normalized RMS error | Three-class agreement | Kappa | Median z |
|---:|---:|---:|---:|---:|---:|
| 0 | 0.960814 | 0.377573 | 0.944375 | 0.891402 | 61.4221 |
| 1 | 0.90304 | 1.53223 | 0.8575 | 0.748605 | 15.3989 |
| 1.5 | 0.900127 | 1.79244 | 0.8325 | 0.724022 | 7.95225 |
| 2 | 0.896404 | 1.52421 | 0.82875 | 0.738004 | 3.65757 |
| 2.5 | 0.89417 | 1.21144 | 0.851875 | 0.76874 | 1.96719 |
| 3 | 0.867707 | 1.11855 | 0.865 | 0.745077 | 0.979381 |
| 4 | 0.779751 | 1.42254 | 0.9075 | 0.563018 | 0.328441 |
| 6 | 0.580547 | 1.78003 | 0.99 | 0.11006 | 0.0413 |

Normalized RMS error uses the pooled physics-tangent RMS at each lead. The receipt includes transfer-bound ingredients: pooled and case-action squared derivative error, probability error, and near-zero posterior mass at each frozen gamma.

## Execution and provenance

All inference outputs were written and hashed before scoring. Outcomes were opened only inside the unchanged frozen score_actual functions, with access logged. A private CPU dependency copy was incomplete on the first Part3b scoring attempt; its log is retained beside its failure JSON. Copying the unchanged modules repaired that execution failure. No scientific code or criterion changed.

Checkpoint and output arrays remain untracked on niva-array; the publication includes their manifests and task logs. Frozen kernels are identified by hashes in the receipt. Training and inference are complete.
