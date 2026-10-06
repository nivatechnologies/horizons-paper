# Aspen amplitude exploration with matched climatology — DEVELOPMENT / EXPLORATORY

This licenses nothing in the abstract and changes no frozen confirmation reading. New authorization is limited to forward integration of the climatological null. No posterior, MAP, RML, realized-action forecast, training, inference or cloud computation. Executed on sulaco CPU with 16 integration threads; Qwen services untouched.

Frozen null: 4096 states at F=8, acd-climatology ID 1200007, sub 0, case index 0–4095, PCG64/SeedSequence, initial 8+N(0,1), spin-up 50 LT (2964 RK4 steps at dt 0.01). Identical spun-up states for all five amplitudes, the frozen patterns, output ticks and one-LT windows. Regenerated states are saved for future receipt reuse.

**Baseline reproduction:** probabilities bitwise equal = True; maximum absolute probability difference 0.0; tolerance np.float64(1.7763568394002505e-15). No-action mean saved/regenerated = 9.361002090527514/9.361002090527514; J bitwise equal = True. Regenerated matched nulls are used at every amplitude, including 0.16. Saved frozen mean is retained when matched; otherwise the regenerated mean governs all amplitudes.

**Definitions:** confident S uses at least ceil(0.95·draws) votes for a unique modal answer. Climate-confident S means at least 95% of the matched null gives that posterior modal answer, whether or not the posterior is confident. Observation-confident S is confident and not climate-confident. Thus confident S = observation-confident S + the confident-and-climate overlap; the raw climate-confident share need not equal confident minus observation. Tied posterior modes use answer 0 under the frozen code and are not confident. Fc means the sign of the unforced window-energy anomaly.

**R-other / route prerequisites:** changed-amplitude realized calibration is absent. No new realized-action integration is authorized. R2a/R2b points and v2.3 betting 99% intervals are computed, but formal routes are PREREQUISITE NOT MET at changed amplitudes. The separate numerical-pattern column applies only the frozen margin/bounds classification; it is not a route, abstract license or confirmation result. At 0.16, baseline calibration is reused only when the question origin and posterior/modal/confidence/observation classifications match exactly. No new threshold is selected.

## All tested leads

| Amplitude | Lead LT | Confident S | Climate-confident S | Observation-confident S | Confident Fc | Confident + climate overlap |
|---|---|---|---|---|---|---|
| 0.04 | 0.0 | 0.9875 | 0.125 | 0.8625 | 0.96 | 0.125 |
| 0.04 | 1.0 | 0.921875 | 0.125 | 0.796875 | 0.94 | 0.125 |
| 0.04 | 1.5 | 0.861875 | 0.125 | 0.7375 | 0.87 | 0.124375 |
| 0.04 | 2.0 | 0.738125 | 0.123125 | 0.61875 | 0.845 | 0.119375 |
| 0.04 | 2.5 | 0.561875 | 0.0 | 0.561875 | 0.755 | 0.0 |
| 0.04 | 3.0 | 0.395 | 0.0 | 0.395 | 0.605 | 0.0 |
| 0.04 | 4.0 | 0.099375 | 0.0 | 0.099375 | 0.42 | 0.0 |
| 0.04 | 6.0 | 0.000625 | 0.0 | 0.000625 | 0.02 | 0.0 |
| 0.08 | 0.0 | 0.985625 | 0.125 | 0.860625 | 0.96 | 0.125 |
| 0.08 | 1.0 | 0.921875 | 0.125 | 0.796875 | 0.94 | 0.125 |
| 0.08 | 1.5 | 0.86375 | 0.125 | 0.739375 | 0.87 | 0.124375 |
| 0.08 | 2.0 | 0.735 | 0.123125 | 0.615625 | 0.845 | 0.119375 |
| 0.08 | 2.5 | 0.564375 | 0.0 | 0.564375 | 0.755 | 0.0 |
| 0.08 | 3.0 | 0.403125 | 0.0 | 0.403125 | 0.605 | 0.0 |
| 0.08 | 4.0 | 0.120625 | 0.0 | 0.120625 | 0.42 | 0.0 |
| 0.08 | 6.0 | 0.00125 | 0.0 | 0.00125 | 0.02 | 0.0 |
| 0.16 | 0.0 | 0.98375 | 0.125 | 0.85875 | 0.96 | 0.125 |
| 0.16 | 1.0 | 0.92375 | 0.125 | 0.79875 | 0.94 | 0.125 |
| 0.16 | 1.5 | 0.866875 | 0.125 | 0.7425 | 0.87 | 0.124375 |
| 0.16 | 2.0 | 0.744375 | 0.123125 | 0.62375 | 0.845 | 0.120625 |
| 0.16 | 2.5 | 0.589375 | 0.0 | 0.589375 | 0.755 | 0.0 |
| 0.16 | 3.0 | 0.423125 | 0.0 | 0.423125 | 0.605 | 0.0 |
| 0.16 | 4.0 | 0.18 | 0.0 | 0.18 | 0.42 | 0.0 |
| 0.16 | 6.0 | 0.003125 | 0.0 | 0.003125 | 0.02 | 0.0 |
| 0.32 | 0.0 | 0.9825 | 0.125 | 0.8575 | 0.96 | 0.125 |
| 0.32 | 1.0 | 0.925 | 0.125 | 0.8 | 0.94 | 0.125 |
| 0.32 | 1.5 | 0.87375 | 0.125 | 0.74875 | 0.87 | 0.125 |
| 0.32 | 2.0 | 0.766875 | 0.124375 | 0.645 | 0.845 | 0.121875 |
| 0.32 | 2.5 | 0.625 | 0.12125 | 0.5175 | 0.755 | 0.1075 |
| 0.32 | 3.0 | 0.483125 | 0.0 | 0.483125 | 0.605 | 0.0 |
| 0.32 | 4.0 | 0.259375 | 0.0 | 0.259375 | 0.42 | 0.0 |
| 0.32 | 6.0 | 0.02 | 0.0 | 0.02 | 0.02 | 0.0 |
| 0.64 | 0.0 | 0.9925 | 0.125 | 0.8675 | 0.96 | 0.125 |
| 0.64 | 1.0 | 0.93 | 0.125 | 0.805 | 0.94 | 0.125 |
| 0.64 | 1.5 | 0.879375 | 0.125 | 0.754375 | 0.87 | 0.125 |
| 0.64 | 2.0 | 0.79625 | 0.124375 | 0.6725 | 0.845 | 0.12375 |
| 0.64 | 2.5 | 0.6875 | 0.124375 | 0.570625 | 0.755 | 0.116875 |
| 0.64 | 3.0 | 0.563125 | 0.120625 | 0.45875 | 0.605 | 0.104375 |
| 0.64 | 4.0 | 0.32625 | 0.0 | 0.32625 | 0.42 | 0.0 |
| 0.64 | 6.0 | 0.041875 | 0.0 | 0.041875 | 0.02 | 0.0 |

All shares are proportions. Their approximate descriptive 95% case-bootstrap intervals (B=10000, frozen acd-bootstrap sub 1) are in the JSON receipt; they do not gate or license comparison words.

## R2a: observation-confident S minus confident Fc

| Amplitude | Lead LT | Point | Betting 99% interval | Formal route status | Numerical pattern only |
|---|---|---|---|---|---|
| 0.04 | 2.0 | -0.22625 | [-0.32999999999999996, -0.10999999999999999] | PREREQUISITE NOT MET | DIFFERS |
| 0.04 | 3.0 | -0.21 | [-0.344, -0.09599999999999997] | PREREQUISITE NOT MET | DIFFERS |
| 0.08 | 2.0 | -0.229375 | [-0.32999999999999996, -0.10999999999999999] | PREREQUISITE NOT MET | DIFFERS |
| 0.08 | 3.0 | -0.201875 | [-0.33199999999999996, -0.08599999999999997] | PREREQUISITE NOT MET | DIFFERS |
| 0.16 | 2.0 | -0.22125 | [-0.32199999999999995, -0.10599999999999998] | DIFFERS | DIFFERS |
| 0.16 | 3.0 | -0.181875 | [-0.31000000000000005, -0.07199999999999995] | DIFFERS | DIFFERS |
| 0.32 | 2.0 | -0.2 | [-0.29600000000000004, -0.09199999999999997] | PREREQUISITE NOT MET | DIFFERS |
| 0.32 | 3.0 | -0.121875 | [-0.236, -0.008000000000000007] | PREREQUISITE NOT MET | INCONCLUSIVE |
| 0.64 | 2.0 | -0.1725 | [-0.268, -0.06799999999999995] | PREREQUISITE NOT MET | DIFFERS |
| 0.64 | 3.0 | -0.14625 | [-0.252, -0.03200000000000003] | PREREQUISITE NOT MET | INCONCLUSIVE |

## R2b: first confidence loss on the tested lead grid

Eligible actions are observation-confident S at lead 0 with confident Fc at lead 0. The point is the mean over eligible cases of their eligible-action mean [later minus earlier]. Cases with no eligible action are excluded. Beyond-grid losses follow the frozen tie rule. Case-index order is preserved for predictable betting. Detailed pair counts/shares, per-case values and observation-loss variant are saved in the receipt.

| Amplitude | Eligible cases | Eligible actions | Delta_loss | Betting 99% interval | Formal route status | Numerical pattern only |
|---|---|---|---|---|---|
| 0.04 | 192 | 1324 | -0.22817460317460317 | [-0.402, -0.02400000000000002] | PREREQUISITE NOT MET | PRECEDES |
| 0.08 | 192 | 1321 | -0.2201140873015873 | [-0.392, -0.010000000000000009] | PREREQUISITE NOT MET | PRECEDES |
| 0.16 | 192 | 1319 | -0.2096974206349206 | [-0.384, -0.016000000000000014] | PRECEDES | PRECEDES |
| 0.32 | 192 | 1316 | -0.1960565476190476 | [-0.352, 0.006000000000000005] | PREREQUISITE NOT MET | NO ORDER DETECTED |
| 0.64 | 192 | 1332 | -0.1005704365079365 | [-0.252, 0.08800000000000008] | PREREQUISITE NOT MET | NO ORDER DETECTED |

## Prior proxy table — retained for reference

The old frozen-0.16-null proxy report and receipt are unchanged: ACD_AMPLITUDE_EXPLORATORY.md and receipts/acd_stage4_amplitude.json. That table is reproduced below as historical proxy readings; do not confuse it with the matched results above.

| Amplitude | Lead (LT) | Confident S | Observation-confident S (0.16-null proxy) | Confident Fc | Proxy loss difference | Proxy 99% interval | Matched null? |
|---|---|---|---|---|---|---|---|
| 0.04 | 2 | 0.738125 | 0.61875 | 0.845 | -0.22817460317460317 | [-0.402, -0.02400000000000002] | False |
| 0.04 | 3 | 0.395 | 0.395 | 0.605 | -0.22817460317460317 | [-0.402, -0.02400000000000002] | False |
| 0.08 | 2 | 0.735 | 0.615625 | 0.845 | -0.2201140873015873 | [-0.392, -0.010000000000000009] | False |
| 0.08 | 3 | 0.403125 | 0.403125 | 0.605 | -0.2201140873015873 | [-0.392, -0.010000000000000009] | False |
| 0.16 | 2 | 0.744375 | 0.62375 | 0.845 | -0.2096974206349206 | [-0.384, -0.016000000000000014] | True |
| 0.16 | 3 | 0.423125 | 0.423125 | 0.605 | -0.2096974206349206 | [-0.384, -0.016000000000000014] | True |
| 0.32 | 2 | 0.766875 | 0.645 | 0.845 | -0.1960565476190476 | [-0.352, 0.006000000000000005] | False |
| 0.32 | 3 | 0.483125 | 0.483125 | 0.605 | -0.1960565476190476 | [-0.352, 0.006000000000000005] | False |
| 0.64 | 2 | 0.79625 | 0.6725 | 0.845 | -0.1005704365079365 | [-0.252, 0.08800000000000008] | False |
| 0.64 | 3 | 0.563125 | 0.563125 | 0.605 | -0.1005704365079365 | [-0.252, 0.08800000000000008] | False |

## Resolution rules

| Rule | Trigger | Resolution |
|---|---|---|
| R-other | Changed-amplitude R0 calibration is unavailable and only null forward integrations are newly authorized | Compute case-ordered R2a/R2b estimates and betting intervals, but formal route status is PREREQUISITE NOT MET for changed amplitudes. Report numerical margin/interval classification separately without a route license. Reuse baseline calibration only if the baseline question origin and classifications match. No realized-action forecast or posterior fit is run. |

No H1–H3 stop. Numerical baseline checks, source/output hashes, null probabilities, all-lead shares and intervals: receipts/acd_stage4b_null.json and receipts/acd_stage4b_amplitude_matched.json. Figure: figures/F6_amplitude.pdf and figures/F6_amplitude.png; caption: figures/F6_amplitude_CAPTION.md. Original proxy forecasts, calibration receipts, confirmation readings, draft and abstract audit are unchanged.
