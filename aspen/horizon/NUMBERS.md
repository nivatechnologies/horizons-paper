# NUMBERS: act beyond the horizon

AAH sections use the existing NUMBERS checker. Every measurement is replayed from its JSON source; missing inputs are pending, never zero. Labels: estimate (finite panels/bootstrap/Monte Carlo), reference (specified chance baseline). Bootstrap confidence is nominal.


## AAHLCAL. Amplitude calibration

Source `results/l96_calibration.json` · SHA `bd46f7d27417cbc01938a07cdcdea986c60f982d`

Calibration cases only. First passing amplitude selected; later amplitudes not tested.

| id | system | delta | eligible | n | fraction | label |
|---|---|---|---|---|---|---|
| AAHLCAL-1 | l96 | 0.0100 | 2 | 40 | 0.0500 | estimate |
| AAHLCAL-2 | l96 | 0.0200 | 36 | 40 | 0.9000 | estimate |

## AAHLARMS. Per-horizon arm readings

Source `results/l96_solver_statistics.json` · SHA `4d3a404a8399b82d36c9fc8efc0b63ffccb99676`

| id | T | arm | eligible | total | sufficient | top1 | ACC | M95 | regret | realized_regret | response_correlation | response_relative_error | label |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AAHLARMS-1 | 0.2500 | paired | 200 | 200 | 1 | 1.0000 | 0.9996 | 8 | 0.0000 | 0.0000 | 0.9999 | 0.0105 | estimate |
| AAHLARMS-2 | 0.2500 | unpaired | 200 | 200 | 1 | 1.0000 | 0.9996 | 8 | 0.0000 | 0.0000 | 0.9987 | 0.0456 | estimate |
| AAHLARMS-3 | 0.2500 | jitter | 200 | 200 | 1 | 1.0000 | 0.9996 | 8 | 0.0000 | 0.0000 | 0.9999 | 0.0105 | estimate |
| AAHLARMS-4 | 0.2500 | misidentified | 200 | 200 | 1 | 1.0000 | 0.9991 | 8 | 0.0000 | 0.0000 | 0.9991 | 0.0665 | estimate |
| AAHLARMS-5 | 0.5000 | paired | 200 | 200 | 1 | 1.0000 | 0.9990 | 8 | 0.0000 | 0.0000 | 0.9999 | 0.0131 | estimate |
| AAHLARMS-6 | 0.5000 | unpaired | 200 | 200 | 1 | 1.0000 | 0.9990 | 8 | 0.0000 | 0.0000 | 0.9987 | 0.0446 | estimate |
| AAHLARMS-7 | 0.5000 | jitter | 200 | 200 | 1 | 1.0000 | 0.9990 | 8 | 0.0000 | 0.0000 | 0.9999 | 0.0131 | estimate |
| AAHLARMS-8 | 0.5000 | misidentified | 200 | 200 | 1 | 1.0000 | 0.9970 | 8 | 0.0000 | 0.0000 | 0.9972 | 0.0864 | estimate |
| AAHLARMS-9 | 0.7500 | paired | 200 | 200 | 1 | 1.0000 | 0.9980 | 8 | 0.0000 | 0.0000 | 0.9998 | 0.0192 | estimate |
| AAHLARMS-10 | 0.7500 | unpaired | 200 | 200 | 1 | 1.0000 | 0.9980 | 8 | 0.0000 | 0.0000 | 0.9982 | 0.0528 | estimate |
| AAHLARMS-11 | 0.7500 | jitter | 200 | 200 | 1 | 1.0000 | 0.9980 | 8 | 0.0000 | 0.0000 | 0.9998 | 0.0192 | estimate |
| AAHLARMS-12 | 0.7500 | misidentified | 200 | 200 | 1 | 1.0000 | 0.9919 | 8 | 0.0000 | 0.0000 | 0.9904 | 0.1359 | estimate |
| AAHLARMS-13 | 1.0000 | paired | 200 | 200 | 1 | 1.0000 | 0.9963 | 8 | 0.0000 | 8.767e-04 | 0.9994 | 0.0307 | estimate |
| AAHLARMS-14 | 1.0000 | unpaired | 200 | 200 | 1 | 1.0000 | 0.9964 | 8 | 0.0000 | 8.767e-04 | 0.9972 | 0.0670 | estimate |
| AAHLARMS-15 | 1.0000 | jitter | 200 | 200 | 1 | 1.0000 | 0.9963 | 8 | 0.0000 | 8.767e-04 | 0.9994 | 0.0307 | estimate |
| AAHLARMS-16 | 1.0000 | misidentified | 200 | 200 | 1 | 1.0000 | 0.9813 | 8 | 0.0000 | 8.767e-04 | 0.9752 | 0.2151 | estimate |
| AAHLARMS-17 | 1.5000 | paired | 195 | 200 | 1 | 0.9949 | 0.9868 | 8 | 3.785e-04 | 0.0071 | 0.9974 | 0.0661 | estimate |
| AAHLARMS-18 | 1.5000 | unpaired | 195 | 200 | 1 | 0.9795 | 0.9869 | 64 | 0.0017 | 0.0081 | 0.9932 | 0.1086 | estimate |
| AAHLARMS-19 | 1.5000 | jitter | 195 | 200 | 1 | 0.9949 | 0.9868 | 8 | 3.785e-04 | 0.0071 | 0.9974 | 0.0661 | estimate |
| AAHLARMS-20 | 1.5000 | misidentified | 195 | 200 | 1 | 0.9179 | 0.9388 | >256 | 0.0167 | 0.0187 | 0.9037 | 0.4437 | estimate |
| AAHLARMS-21 | 2.0000 | paired | 193 | 200 | 1 | 0.9637 | 0.9625 | 64 | 0.0047 | 0.0418 | 0.9936 | 0.1083 | estimate |
| AAHLARMS-22 | 2.0000 | unpaired | 193 | 200 | 1 | 0.9378 | 0.9625 | 128 | 0.0054 | 0.0381 | 0.9887 | 0.1443 | estimate |
| AAHLARMS-23 | 2.0000 | jitter | 193 | 200 | 1 | 0.9637 | 0.9625 | 64 | 0.0047 | 0.0418 | 0.9936 | 0.1083 | estimate |
| AAHLARMS-24 | 2.0000 | misidentified | 193 | 200 | 1 | 0.7979 | 0.8684 | >256 | 0.0523 | 0.0756 | 0.7610 | 0.7232 | estimate |
| AAHLARMS-25 | 2.5000 | paired | 180 | 200 | 1 | 0.9389 | 0.9232 | 128 | 0.0122 | 0.1086 | 0.9855 | 0.1670 | estimate |
| AAHLARMS-26 | 2.5000 | unpaired | 180 | 200 | 1 | 0.9111 | 0.9236 | 256 | 0.0146 | 0.1135 | 0.9813 | 0.1890 | estimate |
| AAHLARMS-27 | 2.5000 | jitter | 180 | 200 | 1 | 0.9389 | 0.9232 | 128 | 0.0122 | 0.1086 | 0.9855 | 0.1670 | estimate |
| AAHLARMS-28 | 2.5000 | misidentified | 180 | 200 | 1 | 0.5944 | 0.7837 | >256 | 0.1533 | 0.2186 | 0.6248 | 0.9237 | estimate |
| AAHLARMS-29 | 3.0000 | paired | 161 | 200 | 1 | 0.9317 | 0.8623 | 128 | 0.0104 | 0.1400 | 0.9783 | 0.2045 | estimate |
| AAHLARMS-30 | 3.0000 | unpaired | 161 | 200 | 1 | 0.8447 | 0.8627 | >256 | 0.0277 | 0.1538 | 0.9732 | 0.2269 | estimate |
| AAHLARMS-31 | 3.0000 | jitter | 161 | 200 | 1 | 0.9317 | 0.8623 | 128 | 0.0104 | 0.1400 | 0.9783 | 0.2045 | estimate |
| AAHLARMS-32 | 3.0000 | misidentified | 161 | 200 | 1 | 0.4845 | 0.6880 | >256 | 0.2008 | 0.2793 | 0.5694 | 0.9931 | estimate |
| AAHLARMS-33 | 4.0000 | paired | 125 | 200 | 1 | 0.9200 | 0.7115 | 256 | 0.0216 | 0.2766 | 0.9708 | 0.2357 | estimate |
| AAHLARMS-34 | 4.0000 | unpaired | 125 | 200 | 1 | 0.8560 | 0.7128 | 256 | 0.0341 | 0.2829 | 0.9644 | 0.2606 | estimate |
| AAHLARMS-35 | 4.0000 | jitter | 125 | 200 | 1 | 0.9200 | 0.7115 | 256 | 0.0216 | 0.2766 | 0.9708 | 0.2357 | estimate |
| AAHLARMS-36 | 4.0000 | misidentified | 125 | 200 | 1 | 0.4720 | 0.4955 | >256 | 0.2621 | 0.3460 | 0.5143 | 1.0068 | estimate |
| AAHLARMS-37 | 5.0000 | paired | 109 | 200 | 1 | 0.8532 | 0.5492 | 256 | 0.0448 | 0.3144 | 0.9483 | 0.3141 | estimate |
| AAHLARMS-38 | 5.0000 | unpaired | 109 | 200 | 1 | 0.8899 | 0.5474 | >256 | 0.0336 | 0.3298 | 0.9424 | 0.3329 | estimate |
| AAHLARMS-39 | 5.0000 | jitter | 109 | 200 | 1 | 0.8532 | 0.5492 | 256 | 0.0448 | 0.3144 | 0.9483 | 0.3141 | estimate |
| AAHLARMS-40 | 5.0000 | misidentified | 109 | 200 | 1 | 0.5505 | 0.3519 | >256 | 0.2982 | 0.3894 | 0.4485 | 1.0232 | estimate |
| AAHLARMS-41 | 6.0000 | paired | 126 | 200 | 1 | 0.8492 | 0.4086 | 256 | 0.0686 | 0.3927 | 0.9167 | 0.4008 | estimate |
| AAHLARMS-42 | 6.0000 | unpaired | 126 | 200 | 1 | 0.7937 | 0.4060 | 256 | 0.0838 | 0.3593 | 0.9189 | 0.3935 | estimate |
| AAHLARMS-43 | 6.0000 | jitter | 126 | 200 | 1 | 0.8492 | 0.4086 | 256 | 0.0686 | 0.3927 | 0.9167 | 0.4008 | estimate |
| AAHLARMS-44 | 6.0000 | misidentified | 126 | 200 | 1 | 0.6349 | 0.2461 | >256 | 0.2228 | 0.3630 | 0.4850 | 0.9623 | estimate |
| AAHLARMS-45 | 8.0000 | paired | 184 | 200 | 1 | 0.8207 | 0.2175 | 256 | 0.1259 | 0.3796 | 0.8287 | 0.5668 | estimate |
| AAHLARMS-46 | 8.0000 | unpaired | 184 | 200 | 1 | 0.8424 | 0.2166 | 128 | 0.1199 | 0.3828 | 0.8283 | 0.5590 | estimate |
| AAHLARMS-47 | 8.0000 | jitter | 184 | 200 | 1 | 0.8207 | 0.2175 | 256 | 0.1259 | 0.3796 | 0.8287 | 0.5668 | estimate |
| AAHLARMS-48 | 8.0000 | misidentified | 184 | 200 | 1 | 0.7554 | 0.1093 | 256 | 0.1935 | 0.3718 | 0.6671 | 0.8032 | estimate |
| AAHLARMS-49 | 10.0000 | paired | 199 | 200 | 1 | 0.8191 | 0.1140 | 128 | 0.1562 | 0.4066 | 0.7842 | 0.6335 | estimate |
| AAHLARMS-50 | 10.0000 | unpaired | 199 | 200 | 1 | 0.8744 | 0.1123 | 128 | 0.1101 | 0.3838 | 0.7917 | 0.6237 | estimate |
| AAHLARMS-51 | 10.0000 | jitter | 199 | 200 | 1 | 0.8191 | 0.1140 | 128 | 0.1562 | 0.4066 | 0.7842 | 0.6335 | estimate |
| AAHLARMS-52 | 10.0000 | misidentified | 199 | 200 | 1 | 0.7487 | 0.0525 | 256 | 0.2125 | 0.4179 | 0.7530 | 0.7121 | estimate |
| AAHLARMS-53 | 12.0000 | paired | 200 | 200 | 1 | 0.8450 | 0.0601 | 128 | 0.1417 | 0.4225 | 0.7980 | 0.6009 | estimate |
| AAHLARMS-54 | 12.0000 | unpaired | 200 | 200 | 1 | 0.8100 | 0.0544 | 128 | 0.1590 | 0.4202 | 0.7941 | 0.6175 | estimate |
| AAHLARMS-55 | 12.0000 | jitter | 200 | 200 | 1 | 0.8450 | 0.0601 | 128 | 0.1417 | 0.4225 | 0.7981 | 0.6009 | estimate |
| AAHLARMS-56 | 12.0000 | misidentified | 200 | 200 | 1 | 0.8100 | 0.0216 | 128 | 0.1622 | 0.4015 | 0.7623 | 0.7214 | estimate |
| AAHLARMS-57 | 16.0000 | paired | 200 | 200 | 1 | 0.7900 | 0.0226 | 128 | 0.1858 | 0.4249 | 0.7937 | 0.6102 | estimate |
| AAHLARMS-58 | 16.0000 | unpaired | 200 | 200 | 1 | 0.7900 | 0.0204 | 128 | 0.1903 | 0.4266 | 0.7942 | 0.6069 | estimate |
| AAHLARMS-59 | 16.0000 | jitter | 200 | 200 | 1 | 0.7900 | 0.0227 | 128 | 0.1858 | 0.4249 | 0.7936 | 0.6103 | estimate |
| AAHLARMS-60 | 16.0000 | misidentified | 200 | 200 | 1 | 0.8200 | 0.0040 | 256 | 0.1573 | 0.4151 | 0.7599 | 0.7084 | estimate |
| AAHLARMS-61 | 20.0000 | paired | 200 | 200 | 1 | 0.8500 | 0.0094 | 128 | 0.1362 | 0.4491 | 0.7802 | 0.6391 | estimate |
| AAHLARMS-62 | 20.0000 | unpaired | 200 | 200 | 1 | 0.8100 | 0.0148 | 128 | 0.1720 | 0.4509 | 0.7808 | 0.6364 | estimate |
| AAHLARMS-63 | 20.0000 | jitter | 200 | 200 | 1 | 0.8400 | 0.0098 | 128 | 0.1445 | 0.4512 | 0.7785 | 0.6438 | estimate |
| AAHLARMS-64 | 20.0000 | misidentified | 200 | 200 | 1 | 0.7550 | 0.0092 | 256 | 0.2164 | 0.4395 | 0.7383 | 0.7178 | estimate |

## AAHLCONTROL. Members, commitment and null readings

Source `results/l96_solver_statistics.json` · SHA `e7604b3e83523a6dbdb84929921982b27c52978b`

M95 restricted to budget grid. Censored unpaired conservative numerator256; paired censoring fails. Wall seconds measure nested cohorts sharing all scoring horizons plus interval analysis, on a shared host.

| id | T | ratio | member_pass | myopic | random | committed | uncommitted | mean_members | commitment_errors | wall_seconds | random_regret | myopic_regret | random_realized | myopic_realized | label |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AAHLCONTROL-1 | 0.2500 | 1.0000 | 0 | 1.0000 | 0.1250 | 200 | 0 | 8.0000 | 0.0000 | 0.0397 | 0.7598 | 0.0000 | 0.7594 | 0.0000 | estimate |
| AAHLCONTROL-2 | 0.5000 | 1.0000 | 0 | 1.0000 | 0.1250 | 200 | 0 | 8.0000 | 0.0000 | 0.0397 | 0.7548 | 0.0000 | 0.7545 | 0.0000 | estimate |
| AAHLCONTROL-3 | 0.7500 | 1.0000 | 0 | 1.0000 | 0.1250 | 200 | 0 | 8.0000 | 0.0000 | 0.0397 | 0.7286 | 0.0000 | 0.7276 | 0.0000 | estimate |
| AAHLCONTROL-4 | 1.0000 | 1.0000 | 0 | 1.0000 | 0.1250 | 200 | 0 | 8.0000 | 0.0000 | 0.0397 | 0.6961 | 0.0000 | 0.6903 | 8.767e-04 | estimate |
| AAHLCONTROL-5 | 1.5000 | 8.0000 | 1 | 0.9590 | 0.1250 | 196 | 4 | 16.5306 | 0.0000 | 0.0419 | 0.6152 | 0.0050 | 0.5963 | 0.0106 | estimate |
| AAHLCONTROL-6 | 2.0000 | 2.0000 | 0 | 0.8394 | 0.1250 | 178 | 22 | 28.4494 | 0.0000 | 0.0479 | 0.5646 | 0.0331 | 0.5371 | 0.0542 | estimate |
| AAHLCONTROL-7 | 2.5000 | 2.0000 | 0 | 0.7000 | 0.1250 | 163 | 37 | 57.2761 | 0.0063 | 0.0562 | 0.5509 | 0.0775 | 0.5106 | 0.1409 | estimate |
| AAHLCONTROL-8 | 3.0000 | 2.0000 | 0 | 0.6335 | 0.1250 | 138 | 62 | 85.1014 | 0.0231 | 0.0688 | 0.5337 | 0.1016 | 0.4873 | 0.2127 | estimate |
| AAHLCONTROL-9 | 4.0000 | 1.0000 | 0 | 0.5360 | 0.1250 | 94 | 106 | 128.6809 | 0.0000 | 0.0209 | 0.5386 | 0.1408 | 0.4685 | 0.3116 | estimate |
| AAHLCONTROL-10 | 5.0000 | 1.0000 | 0 | 0.7523 | 0.1250 | 66 | 134 | 156.7273 | 0.0000 | 0.0246 | 0.5760 | 0.0955 | 0.4779 | 0.3694 | estimate |
| AAHLCONTROL-11 | 6.0000 | 1.0000 | 0 | 0.8889 | 0.1250 | 50 | 150 | 186.2400 | 0.0000 | 0.0286 | 0.6155 | 0.0393 | 0.4881 | 0.3911 | estimate |
| AAHLCONTROL-12 | 8.0000 | 0.5000 | 0 | 0.9946 | 0.1250 | 54 | 146 | 246.5185 | 0.0000 | 0.0362 | 0.7140 | 0.0021 | 0.4669 | 0.3690 | estimate |
| AAHLCONTROL-13 | 10.0000 | 1.0000 | 0 | 1.0000 | 0.1250 | 61 | 139 | 219.4098 | 0.0000 | 0.0325 | 0.7581 | 0.0000 | 0.4809 | 0.3848 | estimate |
| AAHLCONTROL-14 | 12.0000 | 1.0000 | 0 | 1.0000 | 0.1250 | 68 | 132 | 235.7647 | 0.0000 | 0.1446 | 0.7669 | 0.0000 | 0.4968 | 0.4195 | estimate |
| AAHLCONTROL-15 | 16.0000 | 1.0000 | 0 | 1.0000 | 0.1250 | 70 | 130 | 229.9429 | 0.0000 | 0.0341 | 0.7737 | 0.0000 | 0.4980 | 0.3940 | estimate |
| AAHLCONTROL-16 | 20.0000 | 1.0000 | 0 | 1.0000 | 0.1250 | 70 | 130 | 236.8000 | 0.0000 | 0.0351 | 0.7696 | 0.0000 | 0.4857 | 0.4123 | estimate |

## AAHKCAL. Amplitude calibration

Source `results/kolmo_calibration_progress.json` · SHA `41730cd159d0a98a9e4d32be7feb9729d62f9653`

Calibration cases only. First passing amplitude selected; later amplitudes not tested.

| id | system | delta | eligible | n | fraction | label |
|---|---|---|---|---|---|---|
| AAHKCAL-1 | kolmo | 0.0100 | 6 | 20 | 0.3000 | estimate |
| AAHKCAL-2 | kolmo | 0.0200 | 6 | 20 | 0.3000 | estimate |

## AAHLPOSTHOC. Post-hoc action frequency, no changed selectors

Source `results/l96_posthoc_action_frequency.json` · SHA `1297ee00e5de5155124796572e93f230a1f48d17`

Final blinded Codex run1 action panel; one framing. All200 myopic choices were action0. Diagnostic only, not a criterion.

| id | T | eligible | action0_best | label |
|---|---|---|---|---|
| AAHLPOSTHOC-1 | 0.2500 | 200 | 200 | estimate |
| AAHLPOSTHOC-2 | 0.5000 | 200 | 200 | estimate |
| AAHLPOSTHOC-3 | 0.7500 | 200 | 200 | estimate |
| AAHLPOSTHOC-4 | 1.0000 | 200 | 200 | estimate |
| AAHLPOSTHOC-5 | 1.5000 | 195 | 187 | estimate |
| AAHLPOSTHOC-6 | 2.0000 | 193 | 162 | estimate |
| AAHLPOSTHOC-7 | 2.5000 | 180 | 126 | estimate |
| AAHLPOSTHOC-8 | 3.0000 | 161 | 102 | estimate |
| AAHLPOSTHOC-9 | 4.0000 | 125 | 67 | estimate |
| AAHLPOSTHOC-10 | 5.0000 | 109 | 82 | estimate |
| AAHLPOSTHOC-11 | 6.0000 | 126 | 112 | estimate |
| AAHLPOSTHOC-12 | 8.0000 | 184 | 183 | estimate |
| AAHLPOSTHOC-13 | 10.0000 | 199 | 199 | estimate |
| AAHLPOSTHOC-14 | 12.0000 | 200 | 200 | estimate |
| AAHLPOSTHOC-15 | 16.0000 | 200 | 200 | estimate |
| AAHLPOSTHOC-16 | 20.0000 | 200 | 200 | estimate |

## AAHLTRAIN. CNN training, not test performance

Source `results/l96_training.json` · SHA `b15e94ad8fe894656b27113458b2fdbd03be07a4`

| id | steps_done | params | best_val | seconds | label |
|---|---|---|---|---|---|
| AAHLTRAIN-1 | 20000 | 999681 | 5.263e-04 | 6943.8370 | estimate |

## AAHREAD. Frozen discrete criteria

Source `results/readings.json` · SHA `7e3b01ef968078462adab8013b333468165fc083`

| id | system | Tf | Td | kill_grid_T | pass_grid_T | kill_condition | pass_condition | ratio_at_Tf | accuracy_at_kill_T | label |
|---|---|---|---|---|---|---|---|---|---|---|
| AAHREAD-1 | l96 | 10.0000 | 12.0000 | 16.0000 |  | 0 | 0 | 1.0000 | 0.7900 | estimate |

## AAHPARTIAL. Descriptive correlations

Source `results/readings.json` · SHA `7e3b01ef968078462adab8013b333468165fc083`

Unit (arm,T); learned/misidentified/jitter within each system. No inferential claim. Pending learned evidence means partial panel.

| id | system | units | attempted | learned_Tf | learned_Tf_status | response_partial | forecast_partial | label |
|---|---|---|---|---|---|---|---|---|
| AAHPARTIAL-1 | l96 | 32 | 32 |  | pending | 0.9362 | -0.2058 | estimate |
