# Aspen abstract draft (Claude, from confirmation L1–L4, L8, L9)

**Title:** The forecast horizon is not the intervention horizon

**Alternative title:** An intervention's effect loses confidence before the forecast does

## Abstract

Forecasting systems, from data assimilation to learned world models, are judged by how far ahead they forecast, and interventions on chaotic systems are chosen from those forecasts. We show that, for a single observed instance, confidence in the sign of an intervention's effect is more often lost before confidence in the forecast sign, the sign of the unforced window-energy anomaly, than after. In one-scale Lorenz-96 (N = 40, known law, inferred forcing), observed at every site in 11 noisy snapshots spanning 0.84 Lyapunov times (LT), we sample the full posterior for 200 independent instances and score it against each realized trajectory. At 2 LT the posterior answers the sign of a small intervention's effect on window energy with at least 95% probability for 72% of case–action questions and for 61% beyond what climatology at the true forcing gives, against 85% for the forecast sign; the 61% share minus the 85% share is −0.24 (99% interval [−0.35, −0.14]). At 3 LT, 40% against 67%. At 2 LT, averaged over instances, confident intervention-sign answers that climatology alone does not give are right 99.5% of the time (one-sided 95% lower bound 97.7%). Paired by instance, intervention-sign confidence is lost before forecast-sign confidence for 59% of an instance's eligible actions and after it for 28%, averaged over instances (99% interval for later minus earlier [−0.49, −0.13]), although at 2 LT the median posterior correlation between factual and counterfactual window energies is 0.975, so their difference carries 3% of the summed uncertainty. In development runs at five amplitudes from 0.5% to 8% of the forcing, the confident intervention-sign share at 2 LT ranges from 73.5% to 79.6%, against 84.5% for the forecast sign. A rule that answers every intervention-sign question through the last lead at which the forecast sign is confident for at least half the instances (3 LT), and none beyond, answers without posterior confidence 26% of the intervention-sign questions in that range, and those answers are right 75% of the time. At 2 LT, a deterministic CNN emulator's ensemble is confident on 22% of the intervention-sign questions the posterior is not confident on, and right on 66% of those. An intervention's confidence horizon is its own quantity, which a world model used to choose actions would need to report per question.

## Optional sentences (outside L1–L10; Todd decides; audit each separately)

**M (mechanism, confirmation R1m, descriptive; would replace the CNN clause):** The intervention's median z, its effect over its posterior spread, starts at 3.6 times the forecast sign's just after the observation window and falls to 0.61 times it by 2 LT.

**A (amplitude, development and exploratory):** In development runs, varying the intervention's amplitude sixteenfold, from 0.5% to 8% of the forcing, keeps the confident intervention-sign share at 2 LT between 73.5% and 79.6%, against 84.5% for the forecast sign.

## Deliberate deviation for the audit

"The forecast sign" is used as a shorthand for the sign of the unforced window-energy anomaly, defined at first use. §11 says Fc is always written in full; the audit should flag it and Todd decides.
