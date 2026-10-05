# Session review — ACD v2.3 specification findings (2026-10-05)

Todd authorized Stage 0 through the Stage 1 gate and replaced specification halts with §14 resolutions. The synthetic audit passes. The following findings are retained under R-other; none changes a threshold or accesses confirmation data.

| Finding | Source | Resolution | Stage 1 implication |
|---|---|---|---|
| The null's exact knowledge of F=8 is an information advantage, but it does not prove a pointwise ordering of posterior confidence for every case/action/lead | WO §6 | Use the literal same-modal-answer climate classification and report null shares | “Beyond climatology” means the declared classification, without a general monotonicity claim |
| The blinded selector proposes expected-regret and scenario-separation targeting outside the tested Q/F/V/R arms | CODEX_SELECTOR.md at eb87279; WO §3 | Record them as untested comparators; L6 names the tested arms | No claim of optimal targeting across algorithms |
| The 56.94 Wilks likelihood radius is approximate in the nonlinear finite-noise problem | WO §5 | Report realized Δχ² coverage and fit diagnostics | Coverage is measured performance, not validation of posterior probabilities or identification |

Reports and code: `horizons-paper`, branch `paper/aspen-2026-10-determinacy`, `aspen/determinacy/ACD_SPEC_GATE.md`. The Stage 1 gate retains these scope findings alongside numerical resolution rules. No freeze or confirmation is authorized in this run.

Related: [[WO_Aspen-Counterfactual-Determinacy-2026-10-04]], [[T_Spec-Integrity-Gate]], [[T_Research-Paper-Guideline]].
