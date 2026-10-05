# Aspen counterfactual determinacy — confirmation (v2.3)

**§11 status: PUBLISH.** Independent confirmation panel: 200 cases, acd-observation-conf, indices 0–199.

All posterior/crude/CNN outputs were written and hashed before realized outcomes for each case; blind-order verification is in `ACD_STAGE2_ARTIFACTS.json`.

Truth coverage: 189/200 (94.50%); Wilson 95% [90.42%, 96.90%]. Diagnostic exclusions: 0/200. Goodness-of-fit flags: 1/200.

Frozen computation: sulaco CPU, dt .01, float64, four NUTS chains, 1000 warmup and 500 draws/chain; required all-draw and 2000-warmup retries retained. R5: first60 qualifying cases at2LT, Q/F/V/R only. CNN-20k: sulaco GPU inference only.

Cuts: R7, R5-A, R6-3LT, RML-conf, P/B-other-leads, R5-3LT. RML-conf and all-site ceiling not run; no R5/CNN at3LT. P/B are reported only at2/3LT.

| Lead (LT) | R0 | Case accuracy [95% one-sided L,U] | Answer accuracy / answers / cases | Included-excluded R0 | R0-F accuracy [L,U] / status |
|---|---|---|---|---|---|
| 0 | PASS | 1.000000 [0.983000, 1.000000] | 1.000000 / 1373 / 200 | PASS; 1.000000 [0.983000, 1.000000] | 1.000000 [0.984677, 1.000000] / PASS |
| 1 | PASS | 0.998277 [0.981000, 1.000000] | 0.998415 / 1262 / 199 | PASS; 0.998277 [0.981000, 1.000000] | 1.000000 [0.983851, 1.000000] / PASS |
| 1.5 | PASS | 0.998995 [0.982000, 1.000000] | 0.999133 / 1153 / 199 | PASS; 0.998995 [0.982000, 1.000000] | 0.994624 [0.974751, 0.999724] / PASS |
| 2 | PASS | 0.995250 [0.977000, 1.000000] | 0.994851 / 971 / 195 | PASS; 0.995250 [0.977000, 1.000000] | 1.000000 [0.982532, 1.000000] / PASS |
| 2.5 | PASS | 0.994324 [0.976000, 1.000000] | 0.994606 / 927 / 194 | PASS; 0.994324 [0.976000, 1.000000] | 0.986577 [0.958351, 0.997610] / PASS |
| 3 | PASS | 0.983049 [0.954000, 1.000000] | 0.990712 / 646 / 176 | PASS; 0.983049 [0.954000, 1.000000] | 0.992537 [0.965089, 0.999617] / PASS |
| 4 | PASS | 0.989507 [0.952000, 1.000000] | 0.978070 / 228 / 97 | PASS; 0.989507 [0.952000, 1.000000] | 0.974359 [0.921479, 0.995425] / PASS |
| 6 | NOT EVALUABLE | 0.750000 [0.173000, 1.000000] | 0.818182 / 11 / 8 | NOT EVALUABLE; 0.750000 [0.173000, 1.000000] | 1.000000 [0.741134, 1.000000] / NOT EVALUABLE |

R0 uses the worse primary/included-excluded status. Bounds use the frozen v2.3 betting procedure; R0-F uses exact Clopper–Pearson. Case-index ordering and all count floors remain fixed.

| Lead (LT) | All-confident S | Observation-confident S | Confident Fc | Median correlation | Median cancellation |
|---|---|---|---|---|---|
| 2 | 72.38% | 60.69% | 85.00% | 0.974953 | 0.031334 |
| 3 | 40.38% | 40.38% | 67.00% | 0.778394 | 0.244137 |

## Publish routes

R2a 2 LT: **DIFFERS**; Δ -0.243125, 99% interval [-0.352000, -0.136000]; prerequisites met: True.
R2a 3 LT: **DIFFERS**; Δ -0.266250, 99% interval [-0.388000, -0.152000]; prerequisites met: True.

R2b: **PRECEDES**; Δ_loss -0.308787, 99% interval [-0.494000, -0.128000], 194 eligible cases and 1332 eligible actions; prerequisites met: True. Case-averaged loss shares: earlier 59.09%, later 28.22%, same_lead 12.69%, both_beyond 0.00%.

R5 2 LT: **DOES NOT BEAT**; common population 60, margin 0.083333.

| Arm | Confident-correct / population | Confident-wrong | Accuracy lower95 | Truth coverage | Failed refits |
|---|---|---|---|---|---|
| Q | 15 / 60 | 0 | 0.818964 | 91.67% | 0 |
| F | 10 / 60 | 0 | 0.741134 | 93.33% | 1 |
| V | 7 / 60 | 0 | 0.651836 | 93.33% | 0 |
| R | 4 / 60 | 0 | 0.472871 | 88.33% | 0 |

Exact one-sided McNemar: Q vs V: 9 vs 1 discordant; p=0.0107421875; Q vs F: 6 vs 1 discordant; p=0.0625; Q vs R: 13 vs 2 discordant; p=0.003692626953.

## Comparators and horizon rule

| Comparator | Lead (LT) | Confident S | Observation-confident S | Case accuracy [L,U] | R0 | Cohen kappa S |
|---|---|---|---|---|---|---|
| Crude | 2 | 38.81% | 27.62% | 0.985456 [0.953000, 1.000000] | PASS | 0.476205 |
| Crude | 3 | 10.75% | 10.75% | 0.975694 [0.934000, 1.000000] | PASS | 0.294595 |
| CNN-20k | 2 | 66.19% | 54.44% | 0.938648 [0.902000, 0.962000] | PASS | 0.708656 |

R6 among posterior-not-confident S: 97/442 CNN-confident (21.95%); 64 correct (65.98%). Surviving paired members: min 128, max 128; zero-member cases 0.

R2c forecast-horizon rule: 3.0 LT.

| Lead (LT) | Rule answers? | Answered not confident | Refused confident | Exception accuracy |
|---|---|---|---|---|
| 0 | True | 1.69% | 0.00% | 77.78% |
| 1 | True | 8.62% | 0.00% | 80.43% |
| 1.5 | True | 15.62% | 0.00% | 76.00% |
| 2 | True | 27.62% | 0.00% | 77.60% |
| 2.5 | True | 42.06% | 0.00% | 74.44% |
| 3 | True | 59.62% | 0.00% | 73.58% |
| 4 | False | 0.00% | 14.25% | 97.81% |
| 6 | False | 0.00% | 0.69% | 81.82% |

## Licensed sentences (§11)

Setup: known one-scale Lorenz-96 law, N=40; inferred F uniform on [6,10], initial-state prior N(0,(10·SIGMA)²); true F=8; 11 noisy full-state snapshots over .84 LT, Gaussian noise .02·SIGMA; eight persistent forcing patterns of amplitude .16; energy averaged over the inherited [T,T+1] LT windows. Confidence means modal posterior probability at least .95 under that model and prior.

**L1 (2 LT).** With 11 noisy snapshots spanning 0.84 Lyapunov times, the posterior under the known law answers the sign of a small intervention’s effect on window energy with at least 95% probability for 72.38% of case–action questions at 2 LT (60.69% beyond what climatology alone gives), against 85.00% for the sign of the unforced window-energy anomaly.

**L2 (2 LT).** Averaged over cases, confident intervention-sign answers that climatology alone does not give are right 99.53% of the time at 2 LT (one-sided 95% lower bound 0.977000); over all such answers, 99.49%. Including excluded cases: case accuracy 99.53%, lower bound 0.977000, answer accuracy 99.49%.

**L3a (2 LT).** At 2 LT the observation-confident S share and the confident share for the sign of the unforced window-energy anomaly differ by -0.243125 (99% interval [-0.352000, -0.136000]).

**L4 (2 LT).** At 2 LT, the posterior correlation between factual and counterfactual window energies is 0.974953 (median), so the difference carries 0.031334 of their summed uncertainty.

**L5 (2 LT).** Of the confident sign answers at 2 LT, 16.15% are given by climatology at the true forcing; the rest depend on the observations.

**L1 (3 LT).** With 11 noisy snapshots spanning 0.84 Lyapunov times, the posterior under the known law answers the sign of a small intervention’s effect on window energy with at least 95% probability for 40.38% of case–action questions at 3 LT (40.38% beyond what climatology alone gives), against 67.00% for the sign of the unforced window-energy anomaly.

**L2 (3 LT).** Averaged over cases, confident intervention-sign answers that climatology alone does not give are right 98.30% of the time at 3 LT (one-sided 95% lower bound 0.954000); over all such answers, 99.07%. Including excluded cases: case accuracy 98.30%, lower bound 0.954000, answer accuracy 99.07%.

**L3a (3 LT).** At 3 LT the observation-confident S share and the confident share for the sign of the unforced window-energy anomaly differ by -0.266250 (99% interval [-0.388000, -0.152000]).

**L4 (3 LT).** At 3 LT, the posterior correlation between factual and counterfactual window energies is 0.778394 (median), so the difference carries 0.244137 of their summed uncertainty.

**L5 (3 LT).** Of the confident sign answers at 3 LT, 0.00% are given by climatology at the true forcing; the rest depend on the observations.

**L3b.** Paired by case, confidence in an intervention’s sign is lost before confidence in the sign of the unforced window-energy anomaly: it is lost later in 28.22% and earlier in 59.09% of a case’s eligible actions, averaged over cases (99% interval for the difference [-0.494000, -0.128000]).

**L6 (2 LT).** Question-, forecast-, spread-targeted and random measurements turned 25.00%, 16.67%, 11.67% and 6.67% of open decision questions at 2 LT into confident, correct answers; question targeting did not reliably beat the best alternative.

The all-40-site clause is omitted because R5-A was cut before confirmation; no ceiling is inferred.

**L7 (crude).** An ensemble built from perturbed last frames gives observation-confident intervention-sign answers with case-averaged accuracy 98.55% and answer-level accuracy 98.87% at 2 LT (one-sided 95% upper bound 1.000000).

**L7 (RML).** Condition not met; no sentence licensed.

**L8 (2 LT).** On sign questions where the posterior is not confident at 2 LT, a deterministic CNN emulator’s ensemble is confident on 21.95% and right on 65.98% of those.

**L9.** Answering every question up to the lead at which the sign of the unforced window-energy anomaly is confident for half the cases, and none beyond, would answer 25.87% of sign questions the posterior is not confident on (right 75.20%) and refuse 7.47% that it is confident on. Fractions are within the answered and refused lead ranges respectively.

**L10.** Condition not met; no sentence licensed.

## Resolutions and scope

Rules fired: R-diag, R-other, R-rml, R-time.

- **R-time** — Stages1–3 full projection exceeds12h: {"initial_seconds": 104977.9093867197, "after_population_seconds": 56050.68403900741, "settings": {"dt": 0.01, "warmup": 1000, "draws": 500, "r5_population": 60, "cuts": ["R7", "R5-A", "R6-3LT", "RML-conf", "P/B-other-leads", "R5-3LT"]}}
- **R-other** — Spec gate scope findings: "True-F climate advantage is literal rather than proven monotone; untested selector targeting arms cannot support L6; Wilks coverage remains approximate."
- **R-rml** — Full-panel signed-event cross-check flags: {"question_lead_flags": 163, "total_question_leads": 59200, "per_lead": [1, 7, 11, 11, 37, 34, 35, 27], "resolution": "Report coupled diagnostic events; retain RML as an approximate cross-check. Stage1a S at2LT had0/160 substantive flags, so its rerun rule did not trigger."}
- **R-other** — RML-conf cut removes prescribed fourth MAP and chain initializers: "No RML fits on confirmation. Four MAP starts at (y0,Fhat),(y0,6.5),(y0,9.5),(y0,8.0); 8.0 is the prior midpoint. The four fitted states initialize the four chains. Lowest MAP likelihood cost is provisional; final minimum includes every full posterior draw. Same prior, likelihood, optimizer, diagnostics, seeds and thresholds."
- **R-other** — Frozen R5-A cut removes all-site licensed-sentence clause: "Report Q/F/V/R only; omit the all40 ceiling clause and RML sentence. No value is imputed for a cut arm."
- **R-diag** — conf 129 R5 F refit fails after retry: {"parameters": {"max_rhat": 1.0101014940121888, "min_ess": 920.6332452896124, "rhat": [1.0101014940121888, 1.0005885020976695, 1.0006232010510832, 1.0025072874682068, 1.0006423278341379, 0.9994872238418999, 1.0010513929805962, 1.0006991465449275, 1.0006870720587615, 1.0004279897780466, 1.0036280939013988, 1.0009457978654277, 1.0026856753288422, 0.9993838961981276, 1.002346529628168, 1.0002180454897518, 0.9997771159895088, 1.0044577423940646, 1.0016272629348517, 1.003638610074947, 1.0027381698163904, 1.0065650363244951, 1.0018026039859194, 1.0026790059438897, 1.0000702333593072, 1.004137266383759, 1.0028703395949823, 1.0015648666493953, 1.0005936378673679, 1.0011785787038794, 1.002702244962179, 1.0004625802256262, 1.0000139106545205, 1.0048249221614778, 1.001057381739742, 1.0001899973498574, 1.0068592706707085, 0.9990362253943804, 1.001649734045085, 1.0020134233288376, 0.9992667402142813, 1.00593008229638], "ess": [2434.2286426083224, 2301.276645861343, 2198.5132351727507, 2199.2584436583297, 2405.8619511151646, 2530.779626696419, 2451.9190514448846, 2355.682796477284, 2593.003254464499, 2381.318511412974, 2385.886233822753, 2537.407993789659, 2274.4168460254905, 2425.173183538417, 2472.7807473837324, 2195.1993611528137, 2103.703351999036, 2622.1432539728607, 2594.7156671578327, 2580.066402764634, 2543.3436235477866, 2546.8081887647254, 2465.9488982628386, 2533.347379172572, 2317.0619178400893, 2525.3551096684196, 2413.603534070178, 2315.6082701588152, 2475.632302640378, 2439.3322736635005, 2720.109345928977, 2485.75935187576, 2305.10018908481, 2754.3871441172455, 2179.0851333788823, 1877.2372014989658, 2386.1082723695463, 2164.906847582478, 2238.310354299022, 2581.209739381629, 2142.216594496582, 920.6332452896124], "passed": false}, "function": {"max_rhat": 1.0019426445709783, "min_ess": 427.92950544430306, "passed": true}}

All bootstrap share/mechanism/comparator intervals are approximate and descriptive; they do not gate publication or license comparison words. Betting, exact Clopper–Pearson and exact McNemar determine the route statuses. Null probabilities are reused unchanged; climate classification uses the sampler’s modal answer. Wilks coverage is measured and approximate.

The full receipt contains R1 maps, R1m covariance/divergence, R2c per-lead errors/refusals, R3/R6 calibration and reliability, R5 site/refit records, rank histograms, fit flags and diagnostic uncertainty: `receipts/acd_stage2.json`. Omitted readings supply no claim. This is a confirmation reading, not an abstract submission.

Related: [[WO_Aspen-Counterfactual-Determinacy-2026-10-04]], [[L_Aspen-Counterfactual-Determinacy-Claim-Ledger-2026-10]].
