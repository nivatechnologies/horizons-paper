# Aspen abstract draft (Claude, from confirmation L1–L4, L8, L9)

**Title:** The forecast horizon is not the intervention horizon

**Alternative title:** An intervention's effect loses confidence before the forecast does

## Abstract

Forecasting systems, from data assimilation to learned world models, are judged by how far ahead they forecast, and interventions on chaotic systems are chosen from those forecasts. We show that, for a single observed instance, confidence in the sign of an intervention's effect is more often lost before confidence in the forecast sign, the sign of the unforced window-energy anomaly, than after. In Lorenz-96 (N = 40, known law, inferred forcing), observed at every site in 11 noisy snapshots spanning 0.84 Lyapunov times (LT), we sample the posterior for 200 independent instances and score it against the truth. At 2 LT, 966 of 971 observation-dependent confident intervention-sign answers are right. Paired by instance, intervention-sign confidence is lost before forecast-sign confidence for 59% of eligible actions and after it for 28%, averaged over instances (99% interval for later minus earlier [−0.49, −0.13]), although factual and counterfactual window energies have median posterior correlation 0.975 at 2 LT. In post hoc analyses: at 3 LT, while the posterior-mean forecast still has anomaly correlation 0.93 with the truth, the sign of a small intervention's effect is confident for 37% of questions about the seven patterns climatology never answers, against 67% for the forecast sign (99% interval for the difference [−0.42, −0.18]); the loss tracks the draws' disagreement about the intervention's effect on the mean flow, not its direct energy injection; the ordering holds for the energy of a 10-site block; and a deterministic CNN emulator given the posterior's own histories is confident about as often as the posterior, but at 2 LT its observation-dependent confident answers are right 93.7% of the time against 99.5% (case-averaged). An intervention's confidence horizon is its own quantity, which a world model used to choose actions would need to report per question.


## Optional sentences (outside L1–L10; Todd decides; audit each separately)

**M (mechanism, confirmation R1m, descriptive; would replace the CNN clause):** The intervention's median z, its effect over its posterior spread, starts at 3.6 times the forecast sign's just after the observation window and falls to 0.61 times it by 2 LT.

**A (amplitude, development and exploratory):** In development runs, varying the intervention's amplitude sixteenfold, from 0.5% to 8% of the forcing, keeps the confident intervention-sign share at 2 LT between 73.5% and 79.6%, against 84.5% for the forecast sign.

## Deliberate deviation for the audit

"The forecast sign" is used as a shorthand for the sign of the unforced window-energy anomaly, defined at first use. §11 says Fc is always written in full; the audit should flag it and Todd decides.
