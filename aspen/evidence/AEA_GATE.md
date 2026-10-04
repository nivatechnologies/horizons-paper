# Evidence alignment: spec integrity gate — 2026-10-04

Status: **BLOCKED for sensitivity, angle-panel construction, learned training and final scientific verdict. Independent blinded Step 0 may proceed.** This is a specification result, not an empirical KILL.

## Authority and boundary

Read the complete WO, including Amendment 1, through the niva-obsidian MCP. Source modification timestamp: 2026-10-04T05:44:22.063Z. Snapshot: WO_SOURCE.md. Standing gate: SPEC_INTEGRITY_TEMPLATE.md. Read 00-Foundations/T_Research-Paper-Guideline.md in full. The user authorizes execution, assigns GB10 Spark 192.168.88.4 and overrides the WO branch with paper/aspen-2026-10-evidence. Isolated worktree is based on fetched origin/paper/adapt-physics-2026-09 at 8147f8262dd5c9659bbc2cd83c70990d8b517584; concurrent horizon worktree is untouched.

Amendment 1 overrides earlier scope, coordinates, directions, substitution, arms, outcomes and cuts. Stage 1 is K only. Insufficient evaluable queries gives otherwise; for sufficient panels KILL precedes PASS. No experimental data, sensitivity run or learned training is authorized by a failed gate. Step 0's blinded selector is independently executable and is expressly required before data.

Read-only Spark inspection succeeded: hostname spark-89d8; NVIDIA GB10, driver 580.178.04, CUDA reported 13.0; GPU utilization 0%; GPU process table lists desktop processes only; 115 GiB available RAM. No inference/training process found by the inspection. Device clock returned Oct 3 while this execution environment date is Oct 4; retain actual timestamps in machine logs. No services changed.

## Checks 1–9 including 5a

| Check | Result | Written accounting |
|---|---|---|
| 1 Two-sided feasibility | PASS for numeric predicates; full implementation conditional | Concrete inputs below show both sides; precedence resolves overlapping PASS/KILL. |
| 2 Independence | PASS at design level | Centre sensitivity and held-out query errors consume different information. Amendment requires disjoint training, validation, sensitivity, attractor, test, identification streams; freeze exact seeds before data. Noise and resampling substreams must be separated too. |
| 3 Referents | FAIL for affected sensitivity and learned recipes | Two blocking defects below. Ratios and correlations additionally require missing-value conventions before final readings. Most referents are repaired by Amendment 1. |
| 4 Source class | PASS for audit | WO is a hypothesis/protocol; source code is implementation, not performance evidence; inherited chaos measurements apply at their recorded parameters only. No novelty or strongest-current-practice claim is inferred from an unverified citation. |
| 5 No example as definition | PASS | Rules, not illustrative errors in the WO, define outcomes. |
| 5a Example provenance | PASS | Every constructed numerical example in this report is explicitly a hypothesis under test, not a measured or physically validated flow. |
| 6 Surprise | PASS | Both learned arms showing equal error across directions triggers KILL; a law arm with strong direction dependence can prevent PASS. |
| 7 Null baseline | PASS | Persistence and centre-parameter solver are mandatory and reported alongside arms. |
| 8 Comparator separability | CONDITIONAL / affected training blocked | Two different learned configurations are specified and neither is presumed best-in-class. FNO-θ information advantage is explicit. History ambiguity prevents a uniquely reproducible learned comparison. Bootstrap intervals are reported, not superiority gates; overlapping intervals cannot establish strongest-practice ordering. |
| 9 Selector separation | Step 0 mechanism admissible; completion pending | Blinded Codex CLI gets only the specified prompt. Record its final queries verbatim plus Claude overlap. Other selectors attributed below; one prompt is one framing, not four independent negative findings. |

## Blocking defects and differential correction requests

1. **Sensitivity forecast horizon (check 3).** Amendment fixes g at u=0, step 0.1, and paired centre-attractor initial states. Query horizon is defined as 0.5 LT of test-point θ. It does not state whether ±0.1 solver runs hold h=0.5/λ(centre) fixed (partial parameter derivative at fixed forecast time) or each recomputes h=0.5/λ(perturbed θ) (derivative along a parameter-dependent time). These are distinct observables: for a trajectory query Q(θ,h(θ)), the derivative contains an extra ∂Q/∂h · dh/dθ. Hypothetical under test: ∂Q/∂u=1 at fixed h, ∂Q/∂h=2 and dh/du=0.5 gives total derivative 2, not 1. Even its direction may change when parameter components differ. Pin one convention before deriving directions or test points. A correction must leave |g|<1e-8 queries unusable and failed-chaos points excluded.

2. **Inherited L_range history (checks 3, 8).** Amendment says architecture and 11-frame history are unchanged, and only the 1,024 training conditions change. Actual AP_FREEZE.md line 44 calls L_range an 8-frame FNO; ap/fno.py ARMS sets L_range n_in=8; ap_train.py reads that n_in directly. Eleven is the identification observation window, not the inherited FNO input. Explicitly select an 11-input-frame adaptation retaining the remaining L_range settings, or an unchanged 8-input-frame network supplied the last 8 observations of the 11-frame window. Do not call a changed input architecture unchanged. FNO-θ inherits L_param/FNO-Re's 4-frame input unless explicitly extended. A correction must keep the prescribed budgets and true-parameter comparator; no choice based on panel performance.

Additional final-reading conventions to pin in the freeze or correction: σ_q=0 makes normalized query error undefined; e90=0 makes R undefined (0/0 or positive/0); constant vectors make Spearman undefined. The WO supplies no zero-denominator or undefined-correlation rule. Do not silently use epsilon denominators or turn unavailable statistics into satisfying criteria. This is conditional until the actual blinded formulas are known.

The amended ray directions and realized displacement are distinct by definition. Projection onto a cube can rotate the displacement. Therefore d0/d90 label generating rays, while D_g and D_perp use actual projected displacement as amended. This is not a reason to change the construction or substitute a failed point.

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
| KILL precedence over PASS | arm1 R=[3,3,3,3], ρ=(.65,.20); arm2 R=[1,1,1,1], ρ=(.2,.1): does not trigger common KILL clause | no KILL; qualifying arm1/law can PASS |
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
