# Aspen amplitude exploration — DEVELOPMENT / EXPLORATORY

This licenses nothing in the abstract. Saved development posterior draws and terminal states are re-forecast under the same patterns, leads, windows and questions; no new posterior, MAP, RML or training. Amplitude 0.16 reuses saved J exactly. Other amplitudes use the inherited float64 RK4 integrator at frozen dt 0.01. Existing factual predictions are unchanged.

**R-other:** the saved climatological receipt contains costs and probabilities, not initial states. A matched climatological null at other amplitudes cannot be obtained solely by re-forecasting saved states. No new climatology run is authorized here. The table explicitly reports observation-confidence relative to the frozen 0.16 null as an exploratory proxy. Amplitude-matched observation-confidence and R2b are unavailable outside 0.16. The displayed loss point and 99% betting interval likewise use that frozen-null eligibility proxy; they carry no R2b route status, calibration claim or abstract license. The 0.16 row is the matched development reading.

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

Fc denotes the sign of the unforced window-energy anomaly. Loss is first nonconfident tested lead, or beyond-grid; differences are averaged within eligible cases then over cases, using the v2.3 continuous betting inversion. No realized trajectory is opened by the exploration. Posterior diagnostic exclusions follow existing receipts. Details and source/output hashes: receipts/acd_stage4_amplitude.json.
