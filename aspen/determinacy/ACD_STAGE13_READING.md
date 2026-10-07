# Stage 13 — review-3 analyses

Post hoc on confirmation; licenses no frozen route. CPU forward integration and scoring on sulaco. Paper and abstract unchanged. No Spark, GPU, Stage 10/10b, Qwen or AFD close-out work. All reported values below are rendered from the receipts by acd_stage13_render.py.

## A — cross-model decisions

Improvement and regret use realized costs. Capture = mean improvement / mean no-action regret. Any invalid draw/option forces no action for E/C, with no survivor conditioning. Histograms list options in index order, no action last. Zero-harm upper bounds are one-sided exact Clopper–Pearson.

### posterior

Invalid case indices: []

| lead | policy | mean_improvement | mean_regret | capture_fraction | acting_share | harms | median_harm | max_harm | zero_harm_CP_upper | chosen_actions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | E | 0.296751 | 0.0169731 | 0.945898 | 1 | 1 | 1.63377 | 1.63377 | — | [140, 3, 3, 11, 16, 18, 4, 5, 0] |
| 2 | no_action | 0 | 0.313724 | 0 | 0 | 0 | — | — | 0.014867 | [0, 0, 0, 0, 0, 0, 0, 0, 200] |
| 2 | always_uniform_decrease | 0.260132 | 0.0535915 | 0.829176 | 1 | 6 | 0.0945245 | 0.817617 | — | [200, 0, 0, 0, 0, 0, 0, 0, 0] |
| 2 | C_delta_0 | 0.292769 | 0.0209553 | 0.933205 | 0.96 | 0 | — | — | 0.014867 | [137, 2, 3, 9, 16, 17, 3, 5, 8] |
| 2 | C_delta_0.1 | 0.292769 | 0.0209553 | 0.933205 | 0.96 | 0 | — | — | 0.014867 | [137, 2, 3, 9, 16, 17, 3, 5, 8] |
| 3 | E | 0.462429 | 0.07843 | 0.85499 | 0.995 | 9 | 0.205919 | 1.43848 | — | [84, 8, 10, 21, 20, 30, 12, 14, 1] |
| 3 | no_action | 0 | 0.540859 | 0 | 0 | 0 | — | — | 0.014867 | [0, 0, 0, 0, 0, 0, 0, 0, 200] |
| 3 | always_uniform_decrease | 0.275226 | 0.265633 | 0.508869 | 1 | 30 | 0.199771 | 1.42088 | — | [200, 0, 0, 0, 0, 0, 0, 0, 0] |
| 3 | C_delta_0 | 0.369414 | 0.171445 | 0.683013 | 0.705 | 0 | — | — | 0.014867 | [69, 5, 6, 9, 16, 23, 2, 11, 59] |
| 3 | C_delta_0.1 | 0.353325 | 0.187534 | 0.653266 | 0.665 | 0 | — | — | 0.014867 | [68, 5, 6, 8, 13, 22, 2, 9, 67] |

### CNN-20k

Invalid case indices: []

| lead | policy | mean_improvement | mean_regret | capture_fraction | acting_share | harms | median_harm | max_harm | zero_harm_CP_upper | chosen_actions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | E | 0.286588 | 0.0271355 | 0.913505 | 1 | 3 | 0.19408 | 1.63377 | — | [119, 3, 3, 15, 22, 29, 4, 5, 0] |
| 2 | no_action | 0 | 0.313724 | 0 | 0 | 0 | — | — | 0.014867 | [0, 0, 0, 0, 0, 0, 0, 0, 200] |
| 2 | always_uniform_decrease | 0.260132 | 0.0535915 | 0.829176 | 1 | 6 | 0.0945245 | 0.817617 | — | [200, 0, 0, 0, 0, 0, 0, 0, 0] |
| 2 | C_delta_0 | 0.286353 | 0.0273705 | 0.912756 | 0.96 | 1 | 0.123794 | 0.123794 | — | [117, 2, 3, 12, 22, 28, 3, 5, 8] |
| 2 | C_delta_0.1 | 0.286205 | 0.0275188 | 0.912283 | 0.955 | 1 | 0.123794 | 0.123794 | — | [117, 2, 3, 12, 22, 27, 3, 5, 9] |
| 3 | E | 0.414578 | 0.126281 | 0.766518 | 0.99 | 21 | 0.169531 | 1.43848 | — | [69, 7, 11, 17, 24, 39, 9, 22, 2] |
| 3 | no_action | 0 | 0.540859 | 0 | 0 | 0 | — | — | 0.014867 | [0, 0, 0, 0, 0, 0, 0, 0, 200] |
| 3 | always_uniform_decrease | 0.275226 | 0.265633 | 0.508869 | 1 | 30 | 0.199771 | 1.42088 | — | [200, 0, 0, 0, 0, 0, 0, 0, 0] |
| 3 | C_delta_0 | 0.31452 | 0.226339 | 0.581519 | 0.67 | 3 | 0.0516709 | 0.0797564 | — | [56, 4, 6, 9, 17, 26, 3, 13, 66] |
| 3 | C_delta_0.1 | 0.304461 | 0.236398 | 0.562921 | 0.625 | 1 | 0.0516709 | 0.0516709 | — | [52, 4, 6, 8, 15, 25, 3, 12, 75] |

### CNN-F

Invalid case indices: []

| lead | policy | mean_improvement | mean_regret | capture_fraction | acting_share | harms | median_harm | max_harm | zero_harm_CP_upper | chosen_actions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | E | 0.304774 | 0.00894941 | 0.971474 | 1 | 1 | 0.0114894 | 0.0114894 | — | [150, 1, 2, 10, 14, 15, 3, 5, 0] |
| 2 | no_action | 0 | 0.313724 | 0 | 0 | 0 | — | — | 0.014867 | [0, 0, 0, 0, 0, 0, 0, 0, 200] |
| 2 | always_uniform_decrease | 0.260132 | 0.0535915 | 0.829176 | 1 | 6 | 0.0945245 | 0.817617 | — | [200, 0, 0, 0, 0, 0, 0, 0, 0] |
| 2 | C_delta_0 | 0.295299 | 0.0184245 | 0.941272 | 0.975 | 1 | 0.0114894 | 0.0114894 | — | [147, 1, 2, 10, 14, 14, 3, 4, 5] |
| 2 | C_delta_0.1 | 0.292282 | 0.0214418 | 0.931654 | 0.965 | 1 | 0.0114894 | 0.0114894 | — | [147, 1, 2, 9, 14, 14, 2, 4, 7] |
| 3 | E | 0.455819 | 0.0850397 | 0.842769 | 1 | 11 | 0.252403 | 1.43848 | — | [94, 5, 7, 20, 19, 32, 8, 15, 0] |
| 3 | no_action | 0 | 0.540859 | 0 | 0 | 0 | — | — | 0.014867 | [0, 0, 0, 0, 0, 0, 0, 0, 200] |
| 3 | always_uniform_decrease | 0.275226 | 0.265633 | 0.508869 | 1 | 30 | 0.199771 | 1.42088 | — | [200, 0, 0, 0, 0, 0, 0, 0, 0] |
| 3 | C_delta_0 | 0.358187 | 0.182672 | 0.662256 | 0.71 | 1 | 0.0346814 | 0.0346814 | — | [76, 4, 4, 9, 15, 22, 3, 9, 58] |
| 3 | C_delta_0.1 | 0.338872 | 0.201986 | 0.626545 | 0.66 | 1 | 0.0346814 | 0.0346814 | — | [72, 4, 4, 8, 12, 22, 3, 7, 68] |

### CNN-F-resp

Invalid case indices: []

| lead | policy | mean_improvement | mean_regret | capture_fraction | acting_share | harms | median_harm | max_harm | zero_harm_CP_upper | chosen_actions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | E | 0.287171 | 0.0265528 | 0.915362 | 1 | 2 | 0.0302531 | 0.039613 | — | [154, 1, 4, 12, 12, 13, 1, 3, 0] |
| 2 | no_action | 0 | 0.313724 | 0 | 0 | 0 | — | — | 0.014867 | [0, 0, 0, 0, 0, 0, 0, 0, 200] |
| 2 | always_uniform_decrease | 0.260132 | 0.0535915 | 0.829176 | 1 | 6 | 0.0945245 | 0.817617 | — | [200, 0, 0, 0, 0, 0, 0, 0, 0] |
| 2 | C_delta_0 | 0.282634 | 0.0310902 | 0.9009 | 0.98 | 2 | 0.0302531 | 0.039613 | — | [152, 0, 4, 12, 12, 12, 1, 3, 4] |
| 2 | C_delta_0.1 | 0.280544 | 0.0331803 | 0.894237 | 0.975 | 2 | 0.0302531 | 0.039613 | — | [152, 0, 4, 12, 12, 11, 1, 3, 5] |
| 3 | E | 0.329239 | 0.21162 | 0.608733 | 1 | 30 | 0.304827 | 1.99557 | — | [99, 6, 9, 19, 19, 31, 8, 9, 0] |
| 3 | no_action | 0 | 0.540859 | 0 | 0 | 0 | — | — | 0.014867 | [0, 0, 0, 0, 0, 0, 0, 0, 200] |
| 3 | always_uniform_decrease | 0.275226 | 0.265633 | 0.508869 | 1 | 30 | 0.199771 | 1.42088 | — | [200, 0, 0, 0, 0, 0, 0, 0, 0] |
| 3 | C_delta_0 | 0.306 | 0.234859 | 0.565766 | 0.725 | 9 | 0.218045 | 0.376873 | — | [83, 2, 6, 9, 12, 19, 6, 8, 55] |
| 3 | C_delta_0.1 | 0.280127 | 0.260732 | 0.517929 | 0.69 | 9 | 0.218045 | 0.376873 | — | [83, 1, 6, 8, 11, 18, 4, 7, 62] |

### Paired comparisons against posterior

Sign tests are exact two-sided on nonzero case regret differences. Bootstrap intervals are descriptive paired case intervals. McNemar is exact on case harm indicators. No multiplicity-adjusted or frozen-route claim.

| model | lead | policy | chosen_option_different_share | mean_regret_difference | exact_two_sided_sign_p | descriptive_paired_bootstrap_95_interval | posterior_only_harm | model_only_harm | exact_McNemar_p |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CNN-20k | 2 | E | 0.15 | 0.0101624 | 0.00522288 | [0.003994828550094985, 0.017760918471309454] | 0 | 2 | 0.5 |
| CNN-20k | 2 | no_action | 0 | 0 | 1 | [0.0, 0.0] | 0 | 0 | 1 |
| CNN-20k | 2 | always_uniform_decrease | 0 | 0 | 1 | [0.0, 0.0] | 0 | 0 | 1 |
| CNN-20k | 2 | C_delta_0 | 0.165 | 0.0064152 | 0.00455138 | [-0.001952131881475108, 0.013931547067891603] | 0 | 1 | 1 |
| CNN-20k | 2 | C_delta_0.1 | 0.16 | 0.0065635 | 0.0021024 | [-0.0016437304829293323, 0.013836380185731436] | 0 | 1 | 1 |
| CNN-20k | 3 | E | 0.29 | 0.0478506 | 0.000100497 | [0.020262249759056897, 0.0761796904967676] | 1 | 13 | 0.00183105 |
| CNN-20k | 3 | no_action | 0 | 0 | 1 | [0.0, 0.0] | 0 | 0 | 1 |
| CNN-20k | 3 | always_uniform_decrease | 0 | 0 | 1 | [0.0, 0.0] | 0 | 0 | 1 |
| CNN-20k | 3 | C_delta_0 | 0.25 | 0.0548938 | 0.000305864 | [0.02514740033110984, 0.08860551345751067] | 0 | 3 | 0.25 |
| CNN-20k | 3 | C_delta_0.1 | 0.255 | 0.0488641 | 0.0017692 | [0.020550641191001178, 0.08048289738292373] | 0 | 1 | 1 |
| CNN-F | 2 | E | 0.06 | -0.00802371 | 0.774414 | [-0.02521334404608477, 0.0013084001222163817] | 0 | 0 | 1 |
| CNN-F | 2 | no_action | 0 | 0 | 1 | [0.0, 0.0] | 0 | 0 | 1 |
| CNN-F | 2 | always_uniform_decrease | 0 | 0 | 1 | [0.0, 0.0] | 0 | 0 | 1 |
| CNN-F | 2 | C_delta_0 | 0.065 | -0.00253081 | 1 | [-0.00908539659483313, 0.001424100785977174] | 0 | 1 | 1 |
| CNN-F | 2 | C_delta_0.1 | 0.055 | 0.000486535 | 1 | [-0.0008794397976298149, 0.0019344964221562838] | 0 | 1 | 1 |
| CNN-F | 3 | E | 0.08 | 0.00660967 | 1 | [-0.005777139356841712, 0.02110904473675141] | 0 | 2 | 0.5 |
| CNN-F | 3 | no_action | 0 | 0 | 1 | [0.0, 0.0] | 0 | 0 | 1 |
| CNN-F | 3 | always_uniform_decrease | 0 | 0 | 1 | [0.0, 0.0] | 0 | 0 | 1 |
| CNN-F | 3 | C_delta_0 | 0.08 | 0.0112268 | 0.803619 | [-0.011280695520377278, 0.03752993855433789] | 0 | 1 | 1 |
| CNN-F | 3 | C_delta_0.1 | 0.065 | 0.0144525 | 0.581055 | [-0.001604883998561347, 0.03489778324970443] | 0 | 1 | 1 |
| CNN-F-resp | 2 | E | 0.185 | 0.0095797 | 0.00256321 | [-0.011455087627054198, 0.025065181069386662] | 0 | 1 | 1 |
| CNN-F-resp | 2 | no_action | 0 | 0 | 1 | [0.0, 0.0] | 0 | 0 | 1 |
| CNN-F-resp | 2 | always_uniform_decrease | 0 | 0 | 1 | [0.0, 0.0] | 0 | 0 | 1 |
| CNN-F-resp | 2 | C_delta_0 | 0.2 | 0.0101349 | 0.00222143 | [-0.006010952908975902, 0.02430804199723716] | 0 | 2 | 0.5 |
| CNN-F-resp | 2 | C_delta_0.1 | 0.195 | 0.012225 | 0.00106502 | [-0.0033750261985781484, 0.02559765579452658] | 0 | 2 | 0.5 |
| CNN-F-resp | 3 | E | 0.405 | 0.13319 | 5.65621e-06 | [0.08574509874288805, 0.18509616716384744] | 0 | 21 | 9.53674e-07 |
| CNN-F-resp | 3 | no_action | 0 | 0 | 1 | [0.0, 0.0] | 0 | 0 | 1 |
| CNN-F-resp | 3 | always_uniform_decrease | 0 | 0 | 1 | [0.0, 0.0] | 0 | 0 | 1 |
| CNN-F-resp | 3 | C_delta_0 | 0.38 | 0.0634141 | 0.0154403 | [0.01789352083842215, 0.11054046675032915] | 0 | 9 | 0.00390625 |
| CNN-F-resp | 3 | C_delta_0.1 | 0.37 | 0.0731982 | 0.0265168 | [0.028719797604850536, 0.1226091166971045] | 0 | 9 | 0.00390625 |

## B — full-grid step halving

First-frame restart includes the observation window. Every saved posterior draw, every option, every lead window, truth and the saved null are reintegrated with float64 RK4. The climatological anomaly reference Jbar is frozen; null probabilities are recomputed.

Draws: 273520; null states: 4096; dt: 0.01 → 0.005.

| lead | type | draw_answer_changed_share | confidence_changed_count | confidence_changed_share | realized_answer_changed_count | realized_answer_changed_share |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | S | 4.57005e-07 | 0 | 0 | 0 | 0 |
| 0 | P | 5.22291e-07 | 0 | 0 | 0 | 0 |
| 0 | B | 0 | 0 | 0 | 0 | 0 |
| 0 | Fc | 0 | 0 | 0 | 0 | 0 |
| 1 | S | 5.48406e-06 | 0 | 0 | 0 | 0 |
| 1 | P | 2.61146e-06 | 0 | 0 | 1 | 0.000178571 |
| 1 | B | 0 | 0 | 0 | 0 | 0 |
| 1 | Fc | 0 | 0 | 0 | 0 | 0 |
| 1.5 | S | 9.1401e-06 | 0 | 0 | 0 | 0 |
| 1.5 | P | 5.48406e-06 | 0 | 0 | 0 | 0 |
| 1.5 | B | 3.65604e-06 | 0 | 0 | 0 | 0 |
| 1.5 | Fc | 0 | 0 | 0 | 0 | 0 |
| 2 | S | 2.05652e-05 | 0 | 0 | 0 | 0 |
| 2 | P | 1.44936e-05 | 0 | 0 | 0 | 0 |
| 2 | B | 2.92483e-05 | 0 | 0 | 0 | 0 |
| 2 | Fc | 3.65604e-06 | 0 | 0 | 0 | 0 |
| 2.5 | S | 2.74203e-05 | 0 | 0 | 0 | 0 |
| 2.5 | P | 2.71592e-05 | 0 | 0 | 1 | 0.000178571 |
| 2.5 | B | 6.58087e-05 | 0 | 0 | 0 | 0 |
| 2.5 | Fc | 1.09681e-05 | 0 | 0 | 0 | 0 |
| 3 | S | 5.48406e-05 | 0 | 0 | 0 | 0 |
| 3 | P | 4.62228e-05 | 1 | 0.000178571 | 0 | 0 |
| 3 | B | 0.000116993 | 0 | 0 | 0 | 0 |
| 3 | Fc | 1.46242e-05 | 0 | 0 | 0 | 0 |
| 4 | S | 0.000137558 | 0 | 0 | 0 | 0 |
| 4 | P | 0.00011856 | 3 | 0.000535714 | 1 | 0.000178571 |
| 4 | B | 0.000266891 | 0 | 0 | 0 | 0 |
| 4 | Fc | 8.7745e-05 | 0 | 0 | 0 | 0 |
| 6 | S | 0.00111738 | 0 | 0 | 3 | 0.001875 |
| 6 | P | 0.00104223 | 0 | 0 | 8 | 0.00142857 |
| 6 | B | 0.00223018 | 0 | 0 | 1 | 0.005 |
| 6 | Fc | 0.000873794 | 0 | 0 | 0 | 0 |

Recomputed eligibility: {"pairs": 1332, "cases": 194, "case_averaged": {"earlier": 0.5909425625920471, "later": 0.28215513009327436, "same": 0.12690230731467844}, "interval": {"lower": -0.494, "upper": -0.128, "empty": false, "point": -0.3087874324987727, "offset": false, "fallback": false, "scope": "POST HOC; no frozen route license"}}

Original eligible cohort sensitivity: {"pairs": 1332, "cases": 194, "case_averaged": {"earlier": 0.5909425625920471, "later": 0.28215513009327436, "same": 0.12690230731467844}, "interval": {"lower": -0.494, "upper": -0.128, "empty": false, "point": -0.3087874324987727, "offset": false, "fallback": false, "scope": "POST HOC; no frozen route license"}}

Original baseline: {"pairs": 1332, "cases": 194, "case_averaged": {"earlier": 0.5909425625920471, "later": 0.28215513009327436, "same": 0.12690230731467844}, "interval": {"lower": -0.494, "upper": -0.128, "empty": false, "point": -0.3087874324987727, "offset": false, "fallback": false, "scope": "POST HOC; no frozen route license"}}

Paired point change: 0

Table 2, observation-confident S accuracy and confident Fc accuracy:

| lead | S_case_accuracy | S_one_sided95_lower | S_answers | S_cases | Fc_accuracy | Fc_one_sided95_lower | Fc_answers |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0.983 | 1373 | 200 | 1 | 0.984677 | 194 |
| 1 | 0.998277 | 0.981 | 1262 | 199 | 1 | 0.983851 | 184 |
| 1.5 | 0.998995 | 0.982 | 1153 | 199 | 0.994624 | 0.974751 | 186 |
| 2 | 0.99525 | 0.977 | 971 | 195 | 1 | 0.982532 | 170 |
| 2.5 | 0.994324 | 0.976 | 927 | 194 | 0.986577 | 0.958351 | 149 |
| 3 | 0.983049 | 0.954 | 646 | 176 | 0.992537 | 0.965089 | 134 |
| 4 | 0.989507 | 0.952 | 228 | 97 | 0.974359 | 0.921479 | 78 |
| 6 | 0.75 | 0.173 | 11 | 8 | 1 | 0.741134 | 10 |

Other question accuracy and seven-pattern comparisons: full-precision receipt tables in receipts/acd_stage13_dt.json.

[
  {
    "lead": 2.0,
    "seven_S_share": 0.6935714285714286,
    "all_S_share": 0.72375,
    "observation_S_share": 0.606875,
    "Fc_share": 0.85,
    "seven_minus_Fc": {
      "lower": -0.27,
      "upper": -0.04600000000000004,
      "empty": false,
      "point": -0.15642857142857142,
      "offset": false,
      "fallback": false,
      "scope": "POST HOC; no frozen route license"
    },
    "all_minus_Fc": {
      "lower": -0.23399999999999999,
      "upper": -0.018000000000000016,
      "empty": false,
      "point": -0.12625,
      "offset": false,
      "fallback": false,
      "scope": "POST HOC; no frozen route license"
    },
    "observation_minus_Fc": {
      "lower": -0.352,
      "upper": -0.136,
      "empty": false,
      "point": -0.243125,
      "offset": false,
      "fallback": false,
      "scope": "POST HOC; no frozen route license"
    }
  },
  {
    "lead": 3.0,
    "seven_S_share": 0.37214285714285716,
    "all_S_share": 0.40375,
    "observation_S_share": 0.40375,
    "Fc_share": 0.67,
    "seven_minus_Fc": {
      "lower": -0.42000000000000004,
      "upper": -0.18200000000000005,
      "empty": false,
      "point": -0.2978571428571428,
      "offset": false,
      "fallback": false,
      "scope": "POST HOC; no frozen route license"
    },
    "all_minus_Fc": {
      "lower": -0.388,
      "upper": -0.15200000000000002,
      "empty": false,
      "point": -0.26625,
      "offset": false,
      "fallback": false,
      "scope": "POST HOC; no frozen route license"
    },
    "observation_minus_Fc": {
      "lower": -0.388,
      "upper": -0.15200000000000002,
      "empty": false,
      "point": -0.26625,
      "offset": false,
      "fallback": false,
      "scope": "POST HOC; no frozen route license"
    }
  }
]

## C — worked instance (illustrative)

Among earlier pairs, most frequent (S first loss, Fc first loss); lexicographic combination on a frequency tie; lowest case, then lowest action.

| case | action | eligible_pairs | earlier_pairs | combination_count | S_first_loss_lead | Fc_first_loss_lead |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | 2 | 1332 | 788 | 80 | 2 | 4 |

## D — withheld effect sizes (descriptive)

| lead | patterns | status | questions | realized_absolute_effect | posterior_mean_absolute_effect | realized_absolute_effect_over_climate_sd | withheld_exceeds_confident_median | withheld_beneficial |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | all_eight | confident | 1158 | {'q25': 0.0642874089943879, 'median': 0.12879805755226048, 'q75': 0.23731569552453458} | {'q25': 0.07133699133555173, 'median': 0.13442127184270786, 'q75': 0.24081927577386175} | {'q25': 0.36268699575240926, 'median': 0.7259710116540332, 'q75': 1.4110449332437016} | — | — |
| 2 | all_eight | not_confident | 442 | {'q25': 0.013321540374752416, 'median': 0.042939964154182775, 'q75': 0.10825900838611835} | {'q25': 0.011921098020088578, 'median': 0.03527268651721821, 'q75': 0.07932823212856197} | {'q25': 0.07259840985775234, 'median': 0.2331140209022613, 'q75': 0.6487360060955283} | 0.217195 | 0.524887 |
| 2 | seven_zero_mean | confident | 971 | {'q25': 0.05562970495951047, 'median': 0.10527836294879833, 'q75': 0.18627382406253767} | {'q25': 0.06188514726889031, 'median': 0.11173700506054064, 'q75': 0.18727550753537364} | {'q25': 0.3179543666151311, 'median': 0.586757096756719, 'q75': 1.0114356904044421} | — | — |
| 2 | seven_zero_mean | not_confident | 429 | {'q25': 0.012835476108218558, 'median': 0.041340340086724936, 'q75': 0.0995935180026386} | {'q25': 0.01187089781959549, 'median': 0.034496839050494874, 'q75': 0.07550487037859949} | {'q25': 0.06918462022270973, 'median': 0.2276908339403976, 'q75': 0.6210220816447922} | 0.240093 | 0.524476 |
| 3 | all_eight | confident | 646 | {'q25': 0.14427861717823287, 'median': 0.2800876996796182, 'q75': 0.46829180657952607} | {'q25': 0.16073536148557377, 'median': 0.3003470282990141, 'q75': 0.46371382652119914} | {'q25': 0.37068213300585523, 'median': 0.6918221253273251, 'q75': 1.2230527421851065} | — | — |
| 3 | all_eight | not_confident | 954 | {'q25': 0.07276076439426049, 'median': 0.1851883158110903, 'q75': 0.40825984084992584} | {'q25': 0.050361771978303216, 'median': 0.11550320172287498, 'q75': 0.22620560142856666} | {'q25': 0.1776403308352223, 'median': 0.44471466680730676, 'q75': 0.9580981437185813} | 0.352201 | 0.502096 |
| 3 | seven_zero_mean | confident | 521 | {'q25': 0.1292714684583096, 'median': 0.24996179294535636, 'q75': 0.49128364782867884} | {'q25': 0.14096689690950134, 'median': 0.27820591661502425, 'q75': 0.48682954217559} | {'q25': 0.32375470497860775, 'median': 0.5872981770816572, 'q75': 1.0870719324261826} | — | — |
| 3 | seven_zero_mean | not_confident | 879 | {'q25': 0.07017983046802367, 'median': 0.17721385362559516, 'q75': 0.39771072639057703} | {'q25': 0.049546095745251234, 'median': 0.11202853542555723, 'q75': 0.21949279505977093} | {'q25': 0.16796000148365142, 'median': 0.42318718930853266, 'q75': 0.9046562824683211} | 0.387941 | 0.492605 |

## E–G — figures, registry and release preparation

| figure | page_size_points |
| --- | --- |
| F15_overview_paper | [720.0, 288.0] |
| F16_instance_paper | [720.0, 288.0] |
| F13_main_paper | [720.0, 288.0] |
| F17_decisions_paper | [720.0, 288.0] |

Evaluator exact reproduction: True; differences: []. See README_EVALUATE.md and RELEASE_MANIFEST.md. No public archive is published.

## Resolution rules

None fired.

Registry before: 17054; after: 37738. Prior values unchanged. Registry check: PASS.

Release inventory summary:

| role | files | size_bytes |
| --- | --- | --- |
| CNN-20k checkpoint | 1 | 4003061 |
| CNN-F selected checkpoint | 1 | 4008277 |
| CPU environment | 1 | 397 |
| Tables 2–4 and primary comparison aggregate receipts | 1 | 4264042 |
| case provenance and draw policy | 1 | 2928 |
| case-level paired endpoint scoring | 1 | 7693 |
| confidence / calibration scoring | 1 | 8220 |
| cross-model decision records | 1 | 47614 |
| decision scoring and CPU step check | 1 | 13981 |
| embedded ACD_IDS seed role contract | 1 | 26669 |
| external-cost evaluator entry point | 1 | 3982 |
| frozen climatological null states | 1 | 2621952 |
| frozen scientific protocol | 1 | 26669 |
| full precision registry | 1 | 8040096 |
| full-grid step-check receipt | 1 | 329785 |
| hashed realized case-level outcomes | 200 | 170400 |
| inherited evaluator dependency; extract standalone contract/kernel for release | 2 | 6427 |
| learned per-case costs; reproduction records | 400 | 298759677 |
| null probabilities and decision margin sd | 1 | 2379496 |
| observation contract and intervention patterns | 1 | 4557 |
| observation/intervention/statistics contract | 1 | 83496 |
| observed input panel, outcomes stored separately | 200 | 758000 |
| per-case blind-order and hash receipt | 200 | 230773 |
| per-case forecast / fit receipt | 200 | 850082 |
| post hoc learned-model provenance and readings | 1 | 2594526 |
| posterior per-case costs, draws and retained draw ordering | 200 | 390587080 |
| pre-confirmation code hash addendum | 1 | 6313 |
| question definitions | 1 | 3183 |
| question summaries / same-lead scoring | 1 | 15240 |
| registry and numeric checker | 1 | 2459 |
| registry presentation | 1 | 5533409 |
| registry regeneration | 1 | 26287 |
| supplied noise-free draw histories H and own forcing F | 200 | 932480022 |
| v2.3 betting bounds: frozen grid and settings | 1 | 6102 |

Flagged items and checkpoint hashes: RELEASE_MANIFEST.md and receipts/acd_stage13_release.json.
