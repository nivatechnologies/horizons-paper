# Aspen evidence-alignment kill test — October 2026

Status: stopped at the specification gate for affected experimental work. No empirical PASS or KILL has been measured.

Branch: `paper/aspen-2026-10-evidence`. Assigned compute: GB10 Spark `192.168.88.4`, reachable by passwordless SSH and idle at inspection.

The complete work order and Amendment 1 were audited before execution. Independent blinded Step 0 is complete; exact prompt and verbatim answer are committed in `aspen/evidence/CODEX_QUERIES.md`.

# Query selector provenance and overlap

Final selector: one blinded Codex CLI invocation of the exact WO prompt, followed by the single permitted forcing-convention clarification. The empty-directory invocation received no work-order criteria, competing query list or experimental data. All prompts and verbatim answers are in CODEX_QUERIES.md and step0/. No second selection run was made.

| Final query | Exact scalar at t*=t_last+0.5/λ(θ) | Claude overlap |
|---|---|---|
| Forcing power | A mean(u_x sin(4y)) = -A/4 mean(ω cos(4y)) | Exact: forcing power input |
| Viscous energy dissipation | mean(ω²)/Re | Not identical; proportional to Claude's enstrophy at fixed Re |
| Drag energy dissipation | α mean(\|u\|²) | Exact: α·2E |
| Viscous enstrophy dissipation | mean(\|∇ω\|²)/Re | Distinct gradient diagnostic |

Claude's WO set is kinetic energy E=mean(|u|²)/2, enstrophy Z=mean(ω²)/2, drag dissipation 2αE and forcing power input. Exact quantity overlap is 2 of 4. Two additional state-statistic relationships exist: the viscous-energy query is 2Z/Re; the drag query is 2αE. Those relationships do not make the selectors identical across varying parameters.

The final formulas are executable for the inherited zero-mean velocity reconstruction and velocity body force. The original answer's vorticity-source power formula A/16 mean(ω sin(4y)) is not substituted into the World D solver. The single clarification retains all four quantity choices and supplies the matching formula, without changing the query family.

Authorship: blinded query author and explicitly WO-attributed Claude comparison set; angle, displacement, arm, box and outcome selectors by amended WO author, as accounted in AEA_GATE.md. Four queries in one prompt represent one independent framing for negative findings. Actual sensitivity proportions remain hypotheses to be measured; no test-point or learned-error data exist.


# Evidence alignment: spec integrity gate — 2026-10-04

Status after Step 0: **BLOCKED for learned training and final scientific verdict by the history-recipe conflict. Sensitivity time is resolved by the final clarified query formulas.** Independent blinded Step 0 is complete. This is a specification result, not an empirical KILL. No experimental runs were started while the full gate remains failed.

## Authority and boundary

Read the complete WO, including Amendment 1, through the niva-obsidian MCP. Source modification timestamp: 2026-10-04T05:44:22.063Z. Snapshot: WO_SOURCE.md. Standing gate: SPEC_INTEGRITY_TEMPLATE.md. Read 00-Foundations/T_Research-Paper-Guideline.md in full. The user authorizes execution, assigns GB10 Spark 192.168.88.4 and overrides the WO branch with paper/aspen-2026-10-evidence. Isolated worktree is based on fetched origin/paper/adapt-physics-2026-09 at 8147f8262dd5c9659bbc2cd83c70990d8b517584; concurrent horizon worktree is untouched.

Amendment 1 overrides earlier scope, coordinates, directions, substitution, arms, outcomes and cuts. Stage 1 is K only. Insufficient evaluable queries gives otherwise; for sufficient panels KILL precedes PASS. No experimental data, sensitivity run or learned training is authorized by a failed gate. Step 0's blinded selector is independently executable and is expressly required before data.

Read-only Spark inspection succeeded: hostname spark-89d8; NVIDIA GB10, driver 580.178.04, CUDA reported 13.0; GPU utilization 0%; GPU process table lists desktop processes only; 115 GiB available RAM. No inference/training process found by the inspection. Device clock returned Oct 3 while this execution environment date is Oct 4; retain actual timestamps in machine logs. No services changed.

## Checks 1–9 including 5a

| Check | Result | Written accounting |
|---|---|---|
| 1 Two-sided feasibility | PASS for numeric predicates; full implementation conditional | Concrete inputs below show both sides; precedence resolves overlapping PASS/KILL. |
| 2 Independence | PASS at design level | Centre sensitivity and held-out query errors consume different information. Amendment requires disjoint training, validation, sensitivity, attractor, test, identification streams; freeze exact seeds before data. Noise and resampling substreams must be separated too. |
| 3 Referents | FAIL for learned recipe; sensitivity time resolved after Step 0 | History conflict below remains. Final clarified query time resolves the initial sensitivity issue. Ratios and correlations additionally require missing-value conventions before final readings. Most referents are repaired by Amendment 1. |
| 4 Source class | PASS for audit | WO is a hypothesis/protocol; source code is implementation, not performance evidence; inherited chaos measurements apply at their recorded parameters only. No novelty or strongest-current-practice claim is inferred from an unverified citation. |
| 5 No example as definition | PASS | Rules, not illustrative errors in the WO, define outcomes. |
| 5a Example provenance | PASS | Every constructed numerical example in this report is explicitly a hypothesis under test, not a measured or physically validated flow. |
| 6 Surprise | PASS | Both learned arms showing equal error across directions triggers KILL; a law arm with strong direction dependence can prevent PASS. |
| 7 Null baseline | PASS | Persistence and centre-parameter solver are mandatory and reported alongside arms. |
| 8 Comparator separability | CONDITIONAL / affected training blocked | Two different learned configurations are specified and neither is presumed best-in-class. FNO-θ information advantage is explicit. History ambiguity prevents a uniquely reproducible learned comparison. Bootstrap intervals are reported, not superiority gates; overlapping intervals cannot establish strongest-practice ordering. |
| 9 Selector separation | PASS for Step 0 mechanism | Blinded Codex CLI received only the specified prompt and completed before any data. Final formulas are clarified once for the inherited forcing convention; prompt, verbatim answers and Claude overlap are retained. Other selectors attributed below; one prompt is one framing, not four independent negative findings. |

## Blocking defects and differential correction requests

1. **Sensitivity forecast horizon (check 3).** Amendment fixes g at u=0, step 0.1, and paired centre-attractor initial states. Query horizon is defined as 0.5 LT of test-point θ. It does not state whether ±0.1 solver runs hold h=0.5/λ(centre) fixed (partial parameter derivative at fixed forecast time) or each recomputes h=0.5/λ(perturbed θ) (derivative along a parameter-dependent time). These are distinct observables: for a trajectory query Q(θ,h(θ)), the derivative contains an extra ∂Q/∂h · dh/dθ. Hypothetical under test: ∂Q/∂u=1 at fixed h, ∂Q/∂h=2 and dh/du=0.5 gives total derivative 2, not 1. Even its direction may change when parameter components differ. Pin one convention before deriving directions or test points. A correction must leave |g|<1e-8 queries unusable and failed-chaos points excluded.

2. **Inherited L_range history (checks 3, 8).** Amendment says architecture and 11-frame history are unchanged, and only the 1,024 training conditions change. At commit 8147f8262dd5c9659bbc2cd83c70990d8b517584, adapt_physics/AP_FREEZE.md:44 calls L_range an 8-frame FNO; adapt_physics/ap/fno.py:71 sets L_range n_in=8; adapt_physics/scripts/ap_train.py reads that n_in directly. Eleven is the identification observation window, not the inherited FNO input. Explicitly select an 11-input-frame adaptation retaining the remaining L_range settings, or an unchanged 8-input-frame network supplied the last 8 observations of the 11-frame window. Do not call a changed input architecture unchanged. FNO-θ inherits L_param/FNO-Re's 4-frame input (adapt_physics/ap/fno.py:72) unless explicitly extended. A correction must keep the prescribed budgets and true-parameter comparator; no choice based on panel performance.

Additional final-reading conventions to pin in the freeze or correction: σ_q=0 makes normalized query error undefined; e90=0 makes R undefined (0/0 or positive/0); constant vectors make Spearman undefined. The WO supplies no zero-denominator or undefined-correlation rule. Do not silently use epsilon denominators or turn unavailable statistics into satisfying criteria. This is conditional until the actual blinded formulas are known.

The amended ray directions and realized displacement are distinct by definition. Projection onto a cube can rotate the displacement. Therefore d0/d90 label generating rays, while D_g and D_perp use actual projected displacement as amended. This is not a reason to change the construction or substitute a failed point.

### Rerun after the single Step 0 clarification

The permitted clarification was asked because the initial answer supplied two forcing conventions, while the mandated World D solver fixes the velocity-body-force convention. The final verbatim answer fixes all four formulas and explicitly writes t*=t_last+0.5/λ(θ). Under Amendment 1's exact-formula rule, the query is now Q(θ,h(θ)); its central differences must use the parameter-dependent query horizon, including the λ dependence. The first defect is therefore resolved by the authorized final query definition, not by a replacement from this executor. A user correction selecting a fixed centre horizon would override this reading and must be recorded before execution.

Checks 1, 2, 4, 5, 5a, 6, 7 and 9 remain passing at the design level. Check 3 still fails for the inherited 8-input-frame recipe versus the amended 11-input-frame, unchanged-architecture statement. Check 8 remains conditional on that correction. Since no experiment has started, no data-informed rescue or selector change has occurred. Differential failures remain: |g|<1e-8 unusable; failed chaos points excluded; fewer than three evaluable queries otherwise; equal-direction learned behavior KILL.

## Concrete passing and failing inputs

**All numeric inputs below are constructed hypotheses under test. They show logical feasibility only, and are not physical observations.** Passing a KILL predicate means triggering KILL.

| Predicate / filter | Passing input | Failing input |
|---|---|---|
| Sensitivity usability | |g|=1e-8: usable | |g|=0.9e-8: unusable |
| Inherited chaos gate: lower 95% λ bound >0 | λ interval [0.01,0.03] | [0,0.03] or [-0.01,0.03] |
| Query evaluability | both 0° and 90° chaos lower bounds +0.01 | either bound 0; passing 45° does not rescue |
| Sufficiency | |Q_e|=3 | |Q_e|=2: otherwise, even large ratios |
| PASS learned ratio R≥2 | e0=.24, e90=.12, R=2 | e0=.239, e90=.12, R<2 |
| PASS query count ≥3 | R=[2,2,2,1] | R=[2,2,1,1] |
| PASS Spearman ρ_g≥.6 | ρ_g=.6 | .599 |
| PASS Spearman ρ_perp≤.3 | ρ_perp=.3 | .301 |
| PASS law ratio R≤1.3 | e0=.13, e90=.10 | e0=.1301, e90=.10 |
| PASS law count ≥3 | R_law=[1.3,1.3,1.3,2] | [1.3,1.3,2,2] |
| One same learned arm meets all PASS requirements | arm1 ratios qualify with ρ_g=.7, ρ_perp=.2 | arm1 has ratios only; arm2 has correlations only |
| KILL symmetric ratio max(R,1/R)≤1.3 | e0=.13,e90=.10, or .10,.13 | .1301,.10, or .10,.1301 |
| KILL ratio count for both learned arms | each has 3 qualifying queries | either has only 2; absent correlation KILL |
| KILL |ρ_g−ρ_perp|<.15 | both gaps .149 | either gap .15; absent ratio KILL |
| Complete PASS | Q_e=4; arm1 R=[3,3,3,3], correlations (.8,.1); arm2 R=[2,2,2,2], correlations (.7,.2); law R=[1,1,1,1] | either mandatory learned requirement fails and neither KILL clause holds |
| Complete KILL | Q_e=4; both arms R=[1,1,1,1], finite correlations gaps .4 | both R=[3,3,3,3], both gaps .4 |
| Insufficient before outcome predicates | Q_e=2, both correlation gaps .1: otherwise, not KILL | Q_e=3, both gaps .1: KILL |
| Otherwise | Q_e=4; both R=[1.5,1.5,1.5,1.5], both correlation gaps .3 | a complete PASS or KILL input above |
| Query scalar-state/trajectory eligibility | q=.5 mean(|v(h)|²), an executable state scalar | an unspecified qualitative “stability” label with no formula |
| Normalized error | |qhat−q|=.2, σ_q=.1 gives 2 | σ_q=0 is unavailable, not finite normalized error |

Primary correlations are over (query,point) units as amended, not individual states. State bootstrap B=2000 is descriptive. Query error is the mean of 100 normalized absolute errors. Attractor normalization uses 1,000 samples. Geometry distance 1, FD step .1, 64 paired sensitivity states, training conditions 1,024, optimizer steps 30,000, law sweeps 3 and 30 evaluations per parameter, seed separation, window 11, Δ=.35, noise .02, horizon .5 LT and bounds are protocol settings, not empirically justified success thresholds. No threshold tuning follows data.

## Selector provenance

- Query selector: required blinded Codex CLI; competing four-query set explicitly attributed to Claude in WO. Exact overlap follows Step 0.
- Kolmogorov framing; box; angles {0,45,90,centre}; displacement magnitude 1; direction construction; arms; baselines; thresholds; sample sizes; cut order: WO/Amendment author, role-based Claude attribution from guideline and WO; individual author metadata not independently verified. Executing reader is distinct from that author. These choices limit the inference to this panel.
- Runtime identification search: Amendment author; inherited P1x objective from repository implementation.
- Branch and GB10 routing: Todd's direct instruction.
- No data-driven selector authored by this executor. Four queries from one prompt count as one framing for negative findings.

## Disposition

Report gate before execution. Complete only independent Step 0, its overlap and audit records. No freeze claiming a fully pinned execution protocol; no test-panel data, learned training, empirical AEA NUMBERS, figures or scientific PASS/KILL. On correction rerun affected gate checks and preserve differential failures (unusable queries, excluded chaos points, insufficient panels, equal-direction KILL).
