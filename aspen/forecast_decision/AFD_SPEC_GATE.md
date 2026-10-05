# AFD spec integrity gate

Current governing version: WO v5.2 (go-v5.2). Amendment 1, approved 2026-10-04, resolves the implementation halt documented below. Checks 1–9 including 5a remain PASS: the amendment pins the inherited unrounded window predicate without changing truth, selection independence, thresholds, nulls, comparator sets or licensed-sentence rules. A window containing a tick inside the unrounded interval passes the amended rule; a rounded endpoint admitting a tick outside that interval fails it. These are constructed hypotheses under test, not observations. Historical pre-amendment statements below are retained as the original pre-data report; current execution status is in EXECUTION_STATUS.md.

Governing sources read in full through vault MCP: WO v5.1 (go-v5.1), T_Spec-Integrity-Gate, T_Research-Paper-Guideline, and the Aspen handoff. The WO governs conflicts with the handoff/guideline. This report precedes any AFD data.

**Design gate: PASS for checks 1–9 including 5a, with the explicit examples and selector accounting below. Implementation preflight: HALT under WO §3; see AFD_STEP0.md. A design PASS does not authorize bypassing that halt.**

| Check | Result | Written answer |
|---|---|---|
| 1. Two-sided feasibility | PASS | WO §8 supplies hypothetical passing/failing inputs for every headline gate. Additional rule boundaries below cover selectors, reliability, undefined quantities and state numerics. |
| 2. Independence | PASS | New trajectory-disjoint test panels and disjoint namespace leaves supply information not consumed by AAH hypothesis selection. Validation supplies selection information; it is not used for outcomes. No old AAH cell is counted as confirmatory evidence. |
| 3. Referents | PASS (design) | Truth selection winner b uses first half; confirmation uses the second half; full truth means define regret. Operational choices use paired member means. Forecast comparability refers to eligible cases/all actions in the decision window. Repairs refer to named trained models, not recipes. LT_ref is explicitly one-scale. Unavailable metrics satisfy no criterion. The code-window conflict is a separate implementation halt. |
| 4. Source class | PASS | WO is a protocol and authorization, not evidence. §8 is constructed hypotheses, not measurements. AAH freeze/calibration are retained measurements; code establishes implementation. Prior results only motivate selection. Reviewer dispositions establish design changes, not implementation correctness. Literature listed in §12 is intended prior work, not a verified claim of equivalence to this intervention target. |
| 5. No example as definition | PASS | Equations, thresholds, endpoints, population rules, ties and sentence conditions in §§4–7 govern; §8 does not override them. |
| 5a. Example provenance | PASS | Every constructed example in WO §8 is explicitly labelled a hypothesis under test. All additional examples below carry the same label. No physical magnitude is inferred from them. |
| 6. Surprise | PASS | Comparable CNN noninferiority can KILL; validation-selected or direct-cost models can close; physics can lose to nulls in two-scale. None is prevented by the scoring geometry. |
| 7. Null baseline | PASS | Random, identified-physics myopic, validation-chosen fixed action. One-scale sufficiency thresholds against the stronger of myopic/fixed; two-scale sufficiency and physics floor prevent a trivial fixed-action result supporting S8. |
| 8. Comparator separability | PASS | L* is a frozen deployment selector based on validation regret, not proof it is statistically superior to runners-up. Report the other arms; do not call a noisy validation ordering established superiority. H1d/S7 force competing reliable repairs into the report; H1e is mandatory; headline energy language additionally requires REG. N-oracle/N2-offline expose reference and attribution differences. |
| 9. Selector separation | PASS | Provenance, competing-selector overlap and limitation accounting below. No multiplied independent-negatives claim is permitted. |

## Passing and failing inputs

**Every input in this section is a constructed hypothesis under test, not a measurement, a calibration or an anchor.** WO §8's entire table is incorporated by reference and retained verbatim in WO_v5.1.md. It includes eligibility, sufficiency, H1a PASS/KILL, witness reliability, H1b, H1d, CLOSES, NARROWS, REG, S4/S4b, two-scale sufficiency and sentence gates, H1e, repeats, B, timestep check, H1c, H2 and H3.

Additional exact boundary cases:

| Axis/filter/classification | Concrete passing input | Concrete failing/nonqualifying input |
|---|---|---|
| Comparable C membership | wACC_N=.95, wACC_L=.94 | wACC_L=.939 |
| Eligible fraction | 160 eligible of 200 | 159 eligible of 200 |
| Physics advantage over nulls | P_N=.95, max(nulls)=.90 | max(nulls)=.91 |
| Witness joint skill | wACC_L=wACC_N=.95; wRMSE_L=wRMSE_N=.30 | wRMSE_L=.301 |
| H1a point gap and bound | gap=.15, lower=.10 | gap=.149 or lower=.099 |
| H1a KILL | nonempty C, every upper=.05 | C empty or any upper=.051 |
| Reliability | 1% failed and 1% dropped | either 1.01% |
| Failed case | 33 dropped of 64 | 32 dropped of 64 is not failed |
| Member stability | finite states with RMS=10 sigma | nonfinite or RMS>10 sigma |
| CNN-cost member stability | every action prediction finite | any action prediction nonfinite |
| H1b PASS | gap=.10, lower=.05, reliable | gap=.099 or lower=.049 |
| Repair RETAINS | lower=.051 | lower=.05 |
| NARROWS | point gain=.05, lower=.001 | gain=.049 or lower=0 |
| REG strictness | regret difference=.01, lower=.001 | difference=0 or lower=0 |
| H1c OPEN | gap=.10, lower=.001, reliable | gap=.099 or lower=0 |
| H2 evaluability | N minus roll=.15, both reliable | gap=.149 or unreliable matched arm |
| H2 WORKS | gain=.10, lower=.001, skill differences=.02 | gain=.099, lower=0 or skill difference=.021 |
| H2 FAILS | upper=.05 and both skill differences=.02 | upper=.051 or skill difference=.021 |
| H2 response mechanism | both response ratios=.7 | either response ratio=.701 |
| H3 response retention | both arms' MSRE/VRE ratios=.8, wACC drops=.005 | any response ratio=.799 (Not supported); only skill fails (inconclusive) |
| Two-scale fixed-action sufficiency | P_fixed=.85 | P_fixed=.851 |
| Two-scale physics floor | physics minus stronger null=.05 | gap=.049 |
| S12 attribution | gain=.05 and lower=.001 | gain=.049 or lower=0 |
| Two-scale state check | max difference=1e-6 sigma_X | difference=1.001e-6 sigma_X |
| Timestep strictness | change=.049 S_J, 2SE=.03 S_J | change=.05 S_J at that SE fails (strict less-than) |
| Available normalized metric | nonzero positive response denominator; S_J>0 | exact zero denominator or S_J=0 |
| Available energy capture | attainable saving denominator=.01 | denominator=0 or negative |
| ACC forecast floor | forecast squared anomaly norm=1e-24 observed norm, observed norm>0 | smaller forecast norm scores zero; zero observed norm is unavailable |
| Paired inputs | same member window/Y for all actions | different member draw for different actions |
| Case independence | distinct independent spin-up per case | shared trajectory across cases |
| Seed integrity | unique leaf tuples and namespace separation | reused tuple or AAH namespace collision |
| Argmin tie | tied actions choose lowest index | higher tied index chosen |
| L* selection | minimum validation regret; remaining ties follow skill and frozen order | test top-1 used to select checkpoint/model |
| Selection isolation | recipes frozen before data, artifacts before own test evaluation | change recipe after any test output or expose test output to training worker |
| Artifact integrity | digest matches file immediately before evaluation | digest differs or missing digest |
| Stage-1 continuation | PASS/otherwise continues under §9 | KILL does not continue |
| Sentence licensing | Stage-2 S1/S2 with all mandatory companions | Stage-1 PASS presented as a licensed sentence |
| Date/budget | training inside frozen cap; required evidence before cutoff | exceeding cap without cuts; unfinished Stage 2b at cutoff is not run |
| Data-freeze ordering | complete rule freeze before generating any data | artifact creation first, rule choice afterward |
| Black/white figure readability | arm discernible from marker/pattern/direct label | arms distinguishable only by hue |

Scoring axes without their own thresholds are descriptive: cost forecast error, MSRE/VRE outside H2/H3, ranking, cost-pair correlation/RE, energy saved, action usage, injected work and per-decision cost. Their passing inputs are finite defined outputs with the correct case/action/time population; failing inputs are zero denominators, nonfinite values, wrong population, excluded-case counts omitted, or invented timings. They have no hidden “good performance” threshold.

## Selector provenance and competing starting point

The executing GPT author provides a competing selector from the **control decision operation**: compare whether history-and-action models can rank persistent interventions by expected energy, separating state prediction, long-window state training, direct objective prediction and paired-action response training; include an identified solver, fixed-parameter solver, history-assimilated solver, myopic/fixed/random policies, and an unresolved-process boundary. Report at a short window, the decision window and longer leads, with energy regret as the practical check.

This starts from the decision operation rather than the AAH cell. It competes with Claude's proposed forecast-mismatch narrative. It names no model as the expected winner.

| Selector | Author/source | Competing overlap / consequence |
|---|---|---|
| Action candidate list/order | Blinded Codex run 1; independent run 2 retained in AAH CODEX_ACTIONS.md | 7 of 8 exact L96 patterns overlap; mode 10 versus half-domain sectors differs. Fixed run-1 list remains the tested action vocabulary. One shared prompt framing; no independence multiplier. |
| Domain, energy objective, persistent forcing | Claude WO; blinded action authors independently chose energy-reduction controls in the earlier action task | Competing operation framing retains energy and persistence but does not assert weather-scale generality. L96 remains a domain-limited finding. |
| Primary lead/thresholds | Claude after AAH; fresh test data; reviewed WO | Competing operation framing retains a decision window and shorter/longer curves; it supplies no independent empirical justification for the numerical thresholds. Those are operational hypothesis thresholds, not measured universal limits. |
| Comparator ladder, rollout and response arms | Claude; GPT review named decision-window repair | Competing operation framing independently includes state, long-window, direct-cost and paired-response training, fixed/identified/history-assimilated physics. All are present in WO; there is no competing arm exclusion favoring the thesis. |
| CNN-R2 and CNN2-R2 | GPT reviewer, details to be frozen by executor | Decision-window state training overlaps the operation selector; validation-only regret selection is deterministic. |
| Direct-cost models, N2-offline, repeats, conditioned truth, X-only closure | GPT reviewer named them; Claude specified them | All overlap the operation framing or its unresolved-process/attribution checks. These can overturn the headline. |
| Two-scale equations/parameters, closure polynomial/search interval | Claude before any two-scale data | Competing framing agrees on unresolved-process boundary and X-only training parity, not uniquely on this polynomial/system. Conclusions stay specific to the tested system/closure; sampler execution report and Todd go still required. |
| Comparable set, repair subsets, L*/L*2 | Claude rules; reviewer repairs; deterministic validation selection | Operation framing includes every tested repair and separate direct-cost result; no test-selected “strongest model” is allowed. Reliability exclusions are reported as unstable, never erased. |
| Published sentence vocabulary | Claude §§7.6–7.7 after GPT reviews | Mandatory companions report contrary/unresolved results. No claim that only physics or counterfactual supervision can work. |
| Execution recipe selectors not yet instantiated | Executor under §9 | Must be fixed in AFD_FREEZE before any data; presently not frozen because Step 0 halted. |

Independence accounting: both action runs share one framing; the new competing control-operation framing is a second-author comparator/domain check, not another empirical panel. Repeated leads/actions/seeds are not independent domain framings. Report outcomes as model/panel readings, never as a count of independent hypotheses disproved.

## Overall status

The work order can return materially different outcomes and permits scope narrowing. Its approved toy-setting deviation is explicit. Design checks pass; the reused implementation does not yet meet the scientific cost-window convention. Step 0's §3 halt controls all subsequent scientific work. No headline sentence, Stage-1 result or two-scale sampler result exists.
