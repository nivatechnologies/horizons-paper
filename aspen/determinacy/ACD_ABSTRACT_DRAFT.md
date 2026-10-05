# Aspen abstract draft (Claude, from confirmation L1–L4, L8, L9)

**Title:** The forecast horizon is not the intervention horizon

**Alternative title:** An intervention's effect loses confidence before the forecast does

## Abstract

Forecasting systems, from data assimilation to learned world models, are judged by how far ahead they forecast, and interventions on chaotic systems are chosen from those forecasts. We show that, for a single observed instance, confidence in the sign of an intervention's effect is more often lost before confidence in the sign of the forecast it acts on than after. In one-scale Lorenz-96 (N = 40, known law, inferred forcing), observed at every site in 11 noisy snapshots spanning 0.84 Lyapunov times (LT), we compute the full posterior for 200 independent instances and score it against each realized trajectory. At 2 LT the posterior answers the sign of a small intervention's effect on window energy with at least 95% probability for 72% of case–action questions (61% beyond what climatology alone gives), against 85% for the sign of the unforced window-energy anomaly, the forecast sign (difference −0.24, 99% interval [−0.35, −0.14]); at 3 LT, 40% against 67%. Averaged over instances, confident answers that climatology alone does not give are right 99.5% of the time (one-sided 95% lower bound 97.7%). Paired by instance, intervention-sign confidence is lost before forecast-sign confidence for 59% of actions and after it for 28% (99% interval for the difference [−0.49, −0.13]), although the posterior correlation between factual and counterfactual window energies is 0.97, so their difference carries 3% of the summed uncertainty. Answering every question up to the lead at which the forecast sign is confident for half the instances, and none beyond, would answer 26% of the intervention questions the posterior is not confident on (right 75%) and refuse 7% it is confident on; a deterministic CNN emulator's ensemble is confident on 22% of those open questions and right on 66%. An intervention's confidence horizon is its own quantity, which a world model used to choose actions would need to report per question.

## Optional sentences (outside L1–L10; Todd decides; audit each separately)

**M (mechanism, confirmation R1m, descriptive; would replace the CNN clause):** The intervention's median z, its effect over its posterior spread, starts at 3.6 times the forecast sign's just after the observation window and falls to 0.61 times it by 2 LT.

**A (amplitude, development and exploratory):** In development runs, varying the intervention's amplitude sixteenfold, from 0.5% to 8% of the forcing, keeps the confident intervention-sign share at 2 LT between 73.5% and 79.6%, against 84.5% for the forecast sign.

## Deliberate deviation for the audit

"The forecast sign" is used as a shorthand for the sign of the unforced window-energy anomaly, defined at first use. §11 says Fc is always written in full; the audit should flag it and Todd decides.
