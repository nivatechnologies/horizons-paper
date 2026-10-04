# Aspen evidence-alignment kill test — October 2026

## GB10 execution results — Amendment 1b

Frozen outcome: **otherwise**. Evaluable queries: **4 of 4**. Complete arm panel: **True**. Step 0 was retained without rerunning.

The experiment uses the amended fixed-lead sensitivity and inherited 8-frame L_range / 4-frame FNO-θ inputs, with three parameter channels only for FNO-θ. All arms use the same physical query functional at each test θ; its explicit parameter factors are evaluation constants, not additional inputs to L_range or the identifier. Point errors use each point's 0.5-Lyapunov-time lead and 100 independent states. The law uses all 11 observations and exactly 270 misfit evaluations per state.

45° points, ensemble disagreement and context identifiability were cut in the specified order before data. This is one selector framing with four queries; a negative is not four independent negative findings. Selector provenance and exact query overlap remain in CODEX_QUERIES.md, QUERY_OVERLAP.md and the gate appendix.

### Every-point chaos gate

| point | Re | A | alpha | lam | ci_lo | ci_hi | chaotic |
|---|---|---|---|---|---|---|---|
| centre | 40 | 1 | 0.07733 | 0.1734 | 0.1649 | 0.182 | True |
| q0_0 | 38.7 | 1.2 | 0.08157 | 0.2089 | 0.2011 | 0.2167 | True |
| q0_90 | 52 | 1.021 | 0.07778 | 0.2843 | 0.2809 | 0.2877 | True |
| q1_0 | 34.43 | 1.2 | 0.07467 | 0.1026 | 0.09578 | 0.1093 | True |
| q1_90 | 39.61 | 1.014 | 0.1083 | 0.1547 | 0.1531 | 0.1564 | True |
| q2_0 | 45.96 | 1.142 | 0.1068 | 0.2689 | 0.2666 | 0.2711 | True |
| q2_90 | 52 | 0.9501 | 0.06699 | 0.2477 | 0.2416 | 0.2538 | True |
| q3_0 | 37.48 | 1.2 | 0.07491 | 0.1573 | 0.148 | 0.1665 | True |
| q3_90 | 39.81 | 1.015 | 0.1083 | 0.1553 | 0.1538 | 0.1569 | True |

Source: aspen/evidence/results/chaos.csv; checked in NUMBERS.md.

### Endpoint ratios

| query | arm | error_0 | error_90 | ratio | symmetric_ratio | available |
|---|---|---|---|---|---|---|
| forcing_power | L_range-3 | 0.02692 | 0.04668 | 0.5768 | 1.734 | True |
| forcing_power | FNO-theta | 0.01259 | 0.02888 | 0.436 | 2.294 | True |
| forcing_power | law | 0.01965 | 0.008602 | 2.285 | 2.285 | True |
| forcing_power | persistence | 0.5636 | 0.7439 | 0.7576 | 1.32 | True |
| forcing_power | centre-law | 0.3563 | 0.1 | 3.562 | 3.562 | True |
| viscous_energy | L_range-3 | 0.07385 | 0.06732 | 1.097 | 1.097 | True |
| viscous_energy | FNO-theta | 0.01812 | 0.02065 | 0.8772 | 1.14 | True |
| viscous_energy | law | 0.0908 | 0.02689 | 3.376 | 3.376 | True |
| viscous_energy | persistence | 0.8632 | 0.9235 | 0.9348 | 1.07 | True |
| viscous_energy | centre-law | 0.4806 | 0.1235 | 3.893 | 3.893 | True |
| drag_energy | L_range-3 | 0.08908 | 0.1156 | 0.7705 | 1.298 | True |
| drag_energy | FNO-theta | 0.06325 | 0.04896 | 1.292 | 1.292 | True |
| drag_energy | law | 0.02625 | 0.0113 | 2.323 | 2.323 | True |
| drag_energy | persistence | 0.6264 | 0.3793 | 1.651 | 1.651 | True |
| drag_energy | centre-law | 1.075 | 0.4938 | 2.177 | 2.177 | True |
| viscous_enstrophy | L_range-3 | 0.05851 | 0.1811 | 0.3231 | 3.095 | True |
| viscous_enstrophy | FNO-theta | 0.01725 | 0.02816 | 0.6124 | 1.633 | True |
| viscous_enstrophy | law | 0.08138 | 0.07983 | 1.019 | 1.019 | True |
| viscous_enstrophy | persistence | 0.6785 | 1.129 | 0.6007 | 1.665 | True |
| viscous_enstrophy | centre-law | 0.7633 | 0.0817 | 9.342 | 9.342 | True |

Source: aspen/evidence/results/ratios.csv; checked in NUMBERS.md.

### Index and baselines

| arm | n_units | rho_g | rho_perp | gap | rho_euclidean | rho_mahalanobis |
|---|---|---|---|---|---|---|
| L_range-3 | 12 | 0.3844 | 0.8115 | 0.4271 | 0.7053 | 0.6336 |
| FNO-theta | 12 | -0.1993 | 0.1993 | 0.3986 | 0.3131 | 0.1424 |
| law | 12 | 0.6941 | 0.5873 | 0.1068 | 0.5326 | 0.6798 |
| persistence | 12 | -0.1886 | 0.4449 | 0.6336 | -0.02159 | -0.1602 |
| centre-law | 12 | 0.8685 | 0.4983 | 0.3702 | 0.7809 | 0.9468 |

Source: aspen/evidence/results/correlations.csv; checked in NUMBERS.md.

The partial correlation controlling λ(θ)·h is unavailable because that control equals 0.5 at every point. Unavailable statistics satisfy no outcome clause. No epsilon denominator or excluded-point substitution is used.

### Learned recipe and cost

| arm | steps | n_in | param_channels | params | best_step | best_val | train_seconds |
|---|---|---|---|---|---|---|---|
| L_range-3 | 3e+04 | 8 | 0 | 1.68e+07 | 3e+04 | 0.0001871 | 6310 |
| FNO-theta | 3e+04 | 4 | 3 | 1.68e+07 | 3e+04 | 9.858e-05 | 6236 |

Source: aspen/evidence/results/training.csv; checked in NUMBERS.md.

### Figures and provenance

Greyscale figures: aspen/evidence/figures/AEA1_error_angle.png, AEA2_error_displacement.png, AEA3_index_baselines.png, with SVG equivalents. Mean normalized query errors and state-bootstrap 95% intervals are in AEA-E. Centre and reported local gradients are in AEA-G and AEA-GP. Tables use inherited NUMBERS column/section validation, producing commit SHAs and source SHA256 hashes.

The frozen PASS/KILL rules return otherwise; Todd decides the next stage.

L_range-3: 0 queries with R ≥ 2; 2 with max(R, 1/R) ≤ 1.3; correlation gap 0.4271.

FNO-theta: 0 queries with R ≥ 2; 2 with max(R, 1/R) ≤ 1.3; correlation gap 0.3986.

The law meets R ≤ 1.3 for 1 queries. Neither PASS nor KILL is satisfied. This selector framing does not establish the proposed directional thesis. No stage-2 experiment was started.


## Protocol and gate record

## Amendment 1b affected-gate rerun — 2026-10-04

**Gate PASS for execution.** Step 0 remains complete and is not rerun. Full WO re-read through niva-obsidian MCP, including Amendment 1b; source modified 2026-10-04T06:42:35.127Z. This entry supersedes the earlier blocked disposition and the earlier total-derivative sensitivity reading.

| Check | Result and affected accounting |
|---|---|
| 1 Two-sided feasibility | PASS: fixed-time derivative and explicit inherited input counts are executable; unavailable-statistic clauses retain both satisfying and failing cases below. |
| 2 Independence | PASS: corrections are pre-data, with disjoint streams retained. Input choices are fixed before panel performance. |
| 3 Referents | PASS: sensitivity uses fixed h_c=0.5/λ(centre) for both perturbations; errors use each test point's 0.5/λ. L_range consumes last 8/11 frames, FNO-θ last 4/11, law all 11. Parameter extension is explicitly one-to-three channels. |
| 4 Source class | PASS: user correction and amended protocol define execution; repository code confirms inherited 8/4 histories. Claimed approximate stationarity cancellation is motivation, not required evidence or a criterion. |
| 5 / 5a | PASS: definitions control; all constructed examples below are hypotheses under test, not physical observations. |
| 6 Surprise | PASS: equal-direction learned errors still KILL; unusable queries or law direction dependence can still prevent PASS. |
| 7 Null baseline | PASS: persistence and centre-parameter solver retained. |
| 8 Comparator separability | PASS for stage-1 design: distinct inherited inputs and privileged parameter channels are explicit; no strongest-current-practice ranking inferred without measurements. |
| 9 Selector separation | PASS under completed Step 0 mechanism; no regenerated queries or selection on evidence. Query set by blinded Codex, comparison set attributed to Claude; angles, displacement, arms and thresholds by amended WO author. Fixed-lead sensitivity correction is explicitly user-supplied. |

All following numerical inputs are **hypotheses under test**:
- Fixed-lead sensitivity: with ∂Q/∂u=1, ∂Q/∂h=2, dh/du=.5, derivative 1 follows the amended rule; derivative 2 would fail that rule.
- L_range inputs: exactly last 8 of 11 passes; changing its lift to 11-frame input fails. FNO-θ last 4 plus three normalized parameter channels passes; 11 frames or a single parameter channel fails.
- σ exclusion: mean q=2, σ=1e-12 is below 2e-12 and excluded; σ=2e-12 is retained (strict <). A mathematically undefined normalized error is unavailable under the overarching unavailable-statistic rule, even if a zero mean makes the relative exclusion test zero; never use an epsilon.
- Ratio: errors (.2,.1) give R=2 and satisfy the inclusive PASS ratio; (0,.1), (.2,0), or (0,0) give unavailable R and satisfy neither ratio clause.
- Spearman: nonconstant vectors with ρ_g=.6, ρ_perp=.3 satisfy PASS; a constant error or index vector makes the relevant coefficient unavailable and blocks that correlation clause. Neither unavailable coefficient triggers KILL.
- Three usable 0°/90° query pairs can support PASS; two cannot. |g|=.9e-8 stays unusable; a zero chaos lower bound stays excluded.
- Learned errors (.3,.3) for at least three queries in each arm still satisfy ratio KILL. (.4,.1) do not satisfy ratio KILL. Gaps .149 in both arms trigger correlation KILL; a gap .15 or unavailable coefficient does not.

Differential correction verified: no sensitivity-norm, chaos or sufficiency exclusion is relaxed. Missing statistics cannot be converted into favorable criteria. The history correction fixes the referent without panel-dependent input selection. Ratios and thresholds, arm budgets and final query formulas are unchanged.

Disposition: commit AEA_FREEZE.md and seed/config freeze before test-panel data or learned training; execute on GB10 Spark 192.168.88.4, branch paper/aspen-2026-10-evidence. Run centre calibration/sensitivity and every-point chaos gate first. Record realized displacement and all excluded points. Existing Step 0 artifacts are immutable.


## Historical pre-correction audit

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
