# Aspen full descriptive metrics

Statistics stage: secondary. Source: NUMBERS_FULL_METRICS_SECONDARY.md checked JSON record.

| Lead (LT) | Arm | Eligible P | All-case P | wACC | wRMSE | MSRE | VRE | All-case regret | B |
|---|---|---|---|---|---|---|---|---|---|
| 1 | N-last | 0.99 | 0.99 | 0.982855 | 0.130483 | 0.144827 | 0.30535 | 0.00116904 | 0.998574 |
| 1 | N-oracle | 1 | 1 | 0.984396 | 0.12354 | 0.0652706 | 0.208832 | 0 | 1 |
| 1 | CNN-20k | 0.99 | 0.99 | 0.992559 | 0.0764329 | 0.556552 | 0.95329 | 0.0001849 | 0.999774 |
| 1.5 | N-last | 1 | 1 | 0.955485 | 0.213359 | 0.209756 | 0.31294 | 0 | 1 |
| 1.5 | N-oracle | 1 | 1 | 0.958835 | 0.204168 | 0.0992612 | 0.197275 | 0 | 1 |
| 1.5 | CNN-20k | 0.94898 | 0.94 | 0.979745 | 0.130207 | 0.726054 | 0.889649 | 0.00493179 | 0.993272 |
| 2 | N-last | 0.947368 | 0.92 | 0.911012 | 0.309135 | 0.223493 | 0.28181 | 0.0070448 | 0.989367 |
| 2 | N-oracle | 0.978947 | 0.98 | 0.915708 | 0.299541 | 0.125235 | 0.205551 | 0.00112273 | 0.998305 |
| 2 | CNN-20k | 0.747368 | 0.72 | 0.956477 | 0.2016 | 0.850787 | 0.913815 | 0.0555474 | 0.916156 |
| 2.5 | N-last | 0.957447 | 0.94 | 0.848703 | 0.40896 | 0.246168 | 0.253851 | 0.00351405 | 0.994323 |
| 2.5 | N-oracle | 0.957447 | 0.95 | 0.852815 | 0.402263 | 0.15219 | 0.199993 | 0.00305876 | 0.995059 |
| 2.5 | CNN-20k | 0.585106 | 0.58 | 0.914319 | 0.29403 | 0.934148 | 0.895406 | 0.137297 | 0.778205 |
| 3 | N-last | 0.944444 | 0.9 | 0.767618 | 0.504697 | 0.279898 | 0.247758 | 0.00548964 | 0.990311 |
| 3 | N-oracle | 0.966667 | 0.93 | 0.773151 | 0.498964 | 0.187957 | 0.191709 | 0.00279507 | 0.995067 |
| 3 | CNN-20k | 0.555556 | 0.52 | 0.852346 | 0.394203 | 1.06782 | 0.901028 | 0.147052 | 0.740462 |
| 4 | N-last | 0.927711 | 0.84 | 0.610633 | 0.642448 | 0.355329 | 0.249588 | 0.0150344 | 0.976052 |
| 4 | N-oracle | 0.939759 | 0.84 | 0.617849 | 0.637334 | 0.278201 | 0.210033 | 0.01075 | 0.982876 |
| 4 | CNN-20k | 0.481928 | 0.45 | 0.705909 | 0.563418 | 1.27319 | 1.00299 | 0.182545 | 0.709227 |
| 6 | N-last | 0.976744 | 0.94 | 0.346493 | 0.777438 | 0.609665 | 0.261666 | 0.010095 | 0.98585 |
| 6 | N-oracle | 0.976744 | 0.95 | 0.349086 | 0.776617 | 0.564181 | 0.243427 | 0.00877212 | 0.987704 |
| 6 | CNN-20k | 0.651163 | 0.59 | 0.403882 | 0.755697 | 1.59085 | 0.889823 | 0.19267 | 0.72993 |

Failed cases have wrong top-1, worst regret and ACC zero; excluded metrics carry counts in the checked record. Response metrics are ratios of sums, with paired case bootstrap.

Realized regret is reported in raw energy, as the panel median range counterpart, and as the historical per-case range descriptive ratio. No new threshold uses these descriptive ratios.

Complete cost mean/spread decomposition, all-case counterparts, action use, work and bootstrap intervals are in the named NUMBERS fragment.

This descriptive baseline report licenses no headline sentence.
