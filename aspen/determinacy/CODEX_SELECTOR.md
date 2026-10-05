# Blinded selector — Step 0b

Run date: 2026-10-05. OpenAI Codex CLI v0.160.0, default model gpt-6.1-sol, fresh ephemeral session, empty working directory `/tmp/acd-selector-blind`, user config and rules disabled, read-only sandbox. The sole user input was the exact §3 prompt below. No work order, development observations, results, or selected question taxonomy was supplied. The CLI uses its standard system instructions; “nothing else” applies to the supplied task prompt. Exit status 0.

## Exact prompt

A chaotic system (the Lorenz-96 model, 40 variables, forcing F) is observed at all sites with noise for a short window. An operator can apply one of eight small persistent forcing patterns, or none, and cares about one scalar outcome: the mean energy over a later time window. Using only the observations and the known equations, list the questions about this particular observed instance that a physicist would most want answered before acting, and for each say how one would judge whether the available observations are sufficient to answer it. Then propose three rules for choosing four additional precise point measurements, taken at the decision time, that would best help answer such questions.

## Verbatim answer

The central question is **whether the observations distinguish states that imply different good actions**. Reconstructing every detail of the state is useful only insofar as it answers that question.

Write the decision-time state as \(x_d\), the available actions as \(a=0,\ldots,8\), and the outcome as
\[
J_a(x_d)=\frac{1}{T_2-T_1}\int_{T_1}^{T_2}
\frac{1}{2(40)}\sum_{i=1}^{40}x_i(t;a)^2\,dt.
\]
Here action \(0\) applies no additional forcing. Assume the aim is to reduce \(J\); reverse the comparisons if higher energy is preferred.

Use the observed short trajectory, the observation-noise model, and the Lorenz–96 equations to construct an ensemble or confidence set of plausible \(x_d\). For each plausible state, simulate **all nine actions from that same state**. These paired simulations distinguish intervention effects from differences in initial conditions. The conclusions remain conditional on the assumed noise model and accuracy of the equations.

| Question about this observed instance | How to judge whether the observations suffice |
|---|---|
| **What would happen without intervention?** What is the plausible range of later mean energy? | Propagate observation-compatible states under action \(0\). The observations suffice if the resulting uncertainty in \(J_0\) is small relative to the operator’s relevant energy tolerance. Accurate reconstruction during the observed window alone does not establish this. |
| **Which patterns help, and by how much?** For each pattern, what is \(J_a-J_0\)? | Examine paired outcome differences across plausible states. Sufficiency means their uncertainty resolves the sign and a practically meaningful magnitude of the effect. Individual outcomes can be uncertain while their differences are well determined. |
| **Which action is best, and does the choice matter?** | Compare all actions jointly. Ask whether plausible states agree on the winner, or whether one action has acceptably small regret—its energy excess over the best action for each state. A precise ranking is unnecessary when several actions are practically tied. |
| **Could the chosen action backfire?** Could it increase energy substantially even if its average effect is favorable? | Evaluate the adverse part of the paired-effect distribution, or its worst case over a justified confidence set. Observations suffice only if they constrain this risk to the operator’s tolerance. A favorable ensemble mean is insufficient; a small ensemble may also miss important alternatives. |
| **Which unresolved features of the present state determine the action response?** For example, is the system’s spatial configuration important even when total energy is similar? | Find observation-compatible states with different action responses, and identify the state directions separating them. Test whether the observations constrain those directions. Large uncertainty in dynamically irrelevant directions need not prevent action. |
| **Is the response approximately linear for these small persistent forcings, or does it involve trajectory changes that alter the ranking?** | Compare tangent or sensitivity predictions with full simulations at the actual forcing amplitudes across plausible states. Observations suffice if they constrain which response regimes are possible and the action comparison survives the nonlinear check. “Small forcing” alone does not guarantee a small accumulated response. |
| **Are these answers stable under reasonable uncertainty assumptions?** | Repeat the inference with defensible noise assumptions, initial-state priors or confidence sets, and numerical accuracy checks. Check fit to the observed trajectory. If reasonable alternatives change the decision materially, the evidence does not yet support a robust choice. |

“Sufficient” therefore needs a specified energy tolerance, acceptable risk or regret, and confidence level. There is no universal threshold based just on observing all 40 sites or on window length.

For four additional precise measurements \(x_i(t_d)\), choose the sites **jointly**, accounting for what the existing observations already tell you. Three useful rules are:

1. **Choose the four sites with the greatest expected reduction in decision regret.**  
   For each candidate set of sites, consider its possible measurement values, condition the state ensemble on each result, and recompute the best action. Select the set that most improves the expected outcome of the resulting decision. This directly targets uncertainty that can change what the operator should do. It requires an explicit probabilistic uncertainty model and decision objective.

2. **Choose the four sites that most reduce uncertainty in the important energy contrasts.**  
   Target \(J_a-J_b\), especially comparisons among competitive actions and against no intervention. Use state covariances and sensitivities of these contrasts to screen candidate sets, then validate promising sets with nonlinear ensemble simulations. Measure coordinates that reveal uncertain, outcome-sensitive state directions; selecting the four largest sensitivities separately can waste measurements on redundant information.

3. **Choose the four sites that best distinguish plausible scenarios requiring different actions.**  
   Group observation-compatible states by their preferred action or by whether a candidate action causes unacceptable harm. Select sites whose joint values most clearly separate those groups, giving priority to consequential disagreements. A robust version maximizes separation of the hardest-to-distinguish conflicting scenarios, subject to the actual measurement precision. This is particularly useful when the state uncertainty has several distinct possibilities or probability weights are unreliable.

The first rule targets the decision itself, the second targets quantitative intervention effects, and the third targets unresolved competing explanations. None requires the four most uncertain state variables to be the four most useful measurements.
## Overlap report (executor; separate from the verbatim answer)

Selector provenance: competing selector generated by the blinded CLI session above; primary S/P/B/Fc taxonomy and targeting implementation authored as disclosed in WO §2 (GPT framing, Claude specification, inherited action/observable selectors). One independent competing framing, not seven independent negative tests.

| WO element | Independent overlap |
|---|---|
| S: action versus no-action sign | Direct: “Which patterns help, and by how much?” and backfire risk. |
| P: pairwise action ordering | Direct: energy contrasts J_a−J_b and quantitative rankings. |
| B: best of eight interventions | Substantial: best action, but the answer considers all nine including no action. Preserve the WO's eight-action gate; nine-action winner is an additional reading. |
| Fc: unforced window-energy anomaly sign | Partial: unforced outcome range appears; a climatological-mean threshold does not. The specific Fc threshold remains authored by the primary selector. |
| Q targeting | Direct family overlap: covariance/sensitivity of important contrasts; exact greedy linear-Gaussian rule and four-site update are not independently specified. |
| F targeting | No separate unforced-forecast targeting arm proposed. Forecast uncertainty is a question, not one of the three targeting rules. |
| V targeting | Discussed but not endorsed: largest state uncertainties need not be the most useful sites. |
| R targeting | No random targeting rule proposed. It remains a null control. |

Two of four question families have direct overlap, B has substantial overlap with a wider action set, Fc only partial overlap. One of four WO targeting families is independently proposed. All three independent targeting rules concern the decision, with expected regret and conflicting-scenario separation beyond WO Q. This supports the broader intervention-decision framing; it does not independently validate the Fc framing, thresholds, or exact targeting algorithm. Check 9's different-author implementation is satisfied by the competing blinded selector and this disclosed divergence; no missing selector is treated as an experimental negative.

## Required additional descriptive readings

If amended execution proceeds, add these from saved J_s(k,T), including action 8 (no action), at each available lead. They cannot affect gates, thresholds, case selection, or publish routes.

- Unforced energy distribution: mean, standard deviation, and empirical 5/50/95% quantiles of J_8.
- Paired effect magnitude and backfire: mean and 5/50/95% quantiles of D_k=J_k−J_8, P(D_k>0), and E[max(D_k,0)] for each action. Existing S supplies P(D_k<0); exact-zero counts remain separate.
- Nine-action winner probabilities, ties to lowest existing index, alongside the prescribed eight-intervention B.
- Regret: R_s(k)=J_s(k)−min_{j=0..8}J_s(j); mean and 5/50/95% quantiles by action. Report for the minimum-posterior-mean-cost action as well. No practical tolerance or “acceptable” label is invented.

State-response directions, nonlinear sensitivity checks, prior/noise robustness, and new targeting algorithms require more than saved costs; record them as selector suggestions, not added required gates or new experiments. No data reading was performed at this halt.
