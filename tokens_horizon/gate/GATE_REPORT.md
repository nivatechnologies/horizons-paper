# Spec integrity gate: WO "How Much Horizon Does a Bit Buy?" (2026-09-23)

Run by the executing agent (Claude Code on Baccus), 2026-09-24, before the freeze commit, against
`00-Foundations/T_Spec-Integrity-Gate.md` (checks 1–9 and 5a). Evidence files are under `tokens_horizon/`.
Every constructed input below is labelled **[measured: file]** (taken from a run that uses no confirmation data),
**[cited: source]**, or **[hypothesis under test]**. Preliminary numbers from the vault note are exploratory,
unratified input and appear only as hypotheses or reproduction targets, never as anchors.

## Summary

| Check | Result |
|---|---|
| 1 two-sided feasibility | Passes for every rule except the **known-zero test**. It fails on the WO's own tokenizer at 4 bits, so that part (the single-frame decomposition, Task 2.3 and F3) **does not run**. There is also a power caveat on "approximately equal". |
| 2 independence | Passes. Held-out rates interleave the fit rates, so the exchange law is tested by interpolation, not extrapolation. |
| 3 referent | 14 referents were unpinned in the WO. All are now pinned in `freeze.yaml: pins`. One is ambiguous and material: plug-in O versus bias-corrected O in the known-zero test. |
| 4 source class | Passes. The prelim is exploratory, the design doc was not available (the WO governs), and the reviews revise rather than select. |
| 5 / 5a no example as definition | Passes. No threshold is keyed to a prelim example. All examples are labelled. |
| 6 surprise | Passes. Surprises are named below, and the blinded second author names the WO's headline claim as its own surprise. |
| 7 null baseline | Persistence was present. A climatological-mean null is **added** (cheap, and it was proposed by the second author). |
| 8 comparator separability | Passes a priori. It is re-checked on the confirmation results. |
| 9 selector separation | **Not satisfied by "three external reviews" alone.** It is now satisfied in part by a blinded second model (Codex). Overlap is high for rates, intervals, margins and core arms, and the systems diverge. Details below. |

## Check 1 and 5a: every rule, threshold and classification

| Rule | Passing input | Failing input | Verdict |
|---|---|---|---|
| Spectrum sum within 1e-3 of −(σ+1+β) or −d | lorenz28 error 1.0e-4; all six systems ≤ 1.2e-4 **[measured: results/lyapunov.json]** | a wrong diagonal Jacobian term, e.g. J[2,2] = −β/2, shifts the sum by 1.33 **[constructed; Liouville ⟨tr J⟩ identity, Eckmann & Ruelle 1985]** | Two-sided. **Caveat:** blind to off-diagonal Jacobian errors, which move λ but not the sum. Cross-check: λ(ρ=28) = 0.9053 ± 0.0015 against 0.9056 **[cited: Sprott, Chaos and Time-Series Analysis, 2003]** |
| **Known-zero test** O(0) < 1e-10·I(0) | 6, 8, 10 bits: 2.6e-28, 3.0e-28, 3.2e-28 **[measured: frozen calibration codebooks]** | **4 bits: 8.6e-10 [measured: frozen calibration codebooks]**; prelim 1.8e-9 **[measured: prelim reproduction]** | **FAIL, and the outcome is fixed before any data arrives.** k-means stops on `tol = 1e-8` at 102 < 300 iterations, so the 4-bit centres differ from the cell means by ~1e-9 relative. The test detects the tolerance of k-means convergence, not an estimator error. The bias-corrected O_bc(0) is exactly 0 at every rate, because d_C(m_k)² ≪ tr Σ_k / n_k. The WO does not say which O the test uses. **The decomposition is not executed** (WO §5 and the gate rule). The proposed correction is in the session review. |
| Output-support bound "outlast" (strict >) | prelim 4 bits: reference outlasts on 99.3% of states **[hypothesis under test]** | prelim 8 bits: 0% (bound 25.8 > reference 4.25) **[hypothesis under test]** | Two-sided |
| Exchange-law criterion per rate | predicted 2.00, measured 2.20: \|0.20\| ≤ 0.33 → pass. Predicted 0.40, measured 0.45: 0.05 ≤ 0.075 → pass **[hypothesis]** | predicted 2.00, measured 2.50: 0.50 > 0.375 → fail. Predicted 0.30, measured 0.45: 0.15 > 0.075 → fail **[hypothesis]** | Two-sided. The criterion is continuous at 0.5 (0.15 × 0.5 = 0.075) |
| Calibration saturation ≤ 5% non-crossing | at δ = 0.3σ_A everything crosses within about 1 Lyapunov time **[hypothesis]** | only if H at δ = 1e-4σ_A approaches 27. The prelim staircase suggests ≈ 9–10 Lyapunov times **[hypothesis]** | Feasible in principle, but expected to pass on every system: a safety check, not a measurement |
| Filter fallback ≤ 5% of steps | prelim 0.19–1.27% **[measured: prelim reproduction]** | plausible under observation noise, or at 8 bits with Δ = 0.1 **[hypothesis]** | Two-sided |
| Approximately equal (90% CI within ±0.10) | diff 0.02, CI (−0.05, 0.08) **[hypothesis]** | diff 0.02, CI (−0.15, 0.19) **[hypothesis]** | Two-sided, but see the **power caveat** below |
| Well below (diff ≥ 0.25, 95% CI excludes 0) | diff 0.40, CI (0.21, 0.60) | diff 0.30, CI (−0.05, 0.62) | Two-sided. **Degenerate at 4 bits against the bound**: the bound is ≈ 0.12, so no arm can be 0.25 below it. The WO avoids this by reporting the gap and the fraction |
| Near (upper 95% limit of ref − model ≤ 0.15) | ref − model 0.05, upper limit 0.12 | ref − model 0.10, upper limit 0.21 | Two-sided in general. **Degenerate at 4 bits against the bound** (always true). The WO already forbids that reading |
| Stall > 90% repeated tokens | A emitting one token forever: 100% | a generic rollout: repeats ≈ the dwell fraction of the token process at Δ | Two-sided. At Δ = 0.02 and 4 bits the true process repeats its token on most steps (cells are large relative to the motion per frame), so a high repeat fraction is partly structural. The true-process repeat fraction is reported next to it |

**Power caveat (approximately equal).** For a paired difference whose per-state standard deviation is s, with n = 300 states, the 90% half-width is about 1.645 s/√300 = 0.095 s. The ±0.10 reading is attainable only if s ≲ 1 and the true difference is near 0. Between learned arms, seed variance widens the interval further. An "approximately equal" reading will be rare. The absence of that reading is not evidence of a difference (WO §2.8).

## Check 2: independence
- Confirmation panels come from a disjoint seed block (40000+). Codebooks, D_eff and h use the calibration block only (10000+). Model selection uses the validation block only (30000+).
- The exchange-law prediction h(δ̂(R)) uses the 1,024-code error *directions* and calibration δ̂(R). The measured quantity uses the rate-R codebook's actual per-state errors on confirmation states. New information: the held-out codebooks, their per-state error-norm spread (the Jensen gap between h at the RMS error and the mean of h), and confirmation states. **Limit:** held-out rates {5, 7, 9, 11} sit between fit rates {6, 8, 10, 12}, so this tests interpolation.

## Check 3: referents pinned before execution
The WO left these open. Each is fixed in `freeze.yaml: pins`: δ̂(R) data; the "measured" H at held-out rates; the states and scoring grid for h; units of C's noise (per coordinate, ×σ_A); whether C's noise applies at evaluation (no); what C and E output at t = 0; E's projection form; head parameterization (residual on the decoded current frame, for B, C, D and E alike); probe training; which arms get seeds 3 and 4; the meaning of "after the pilot budget" for the stall check (1,000 steps, validation panel); Δ = 0.035 against dt = 0.01 (see WO errors); the timing-jitter mechanics; the history-sweep grid.
**Material ambiguity:** "O must be below 1e-10·I" does not say whether O is the plug-in or the bias-corrected term. The conservative reading (plug-in) is applied, and the decomposition stops.

## Check 4: source class
Prelim vault note `R_AIConf-Tokens-Horizon-Prelim-Code-2026-09-23` (status unratified-input): exploratory. It is used as a reproduction target (Task 0.3) and never to set a threshold. The note had not reached the vault MCP index, so it was read from its Drive copy. The design document v4 was not available to the executor, and the WO governs. The "three independent external reviews" revised the selector. A review is not a competing selector (see check 9).

## Check 5: no example as definition
The §0 prelim figures (0.12, 2.93, 99.3%) are motivation. No criterion references them. The readings in §4 are structural (a bound caps, a margin applies). Passes.

## Check 6: results that would surprise the author
(a) Any learned codebook-valued arm (A) outlasting the output-support bound on any state. This is impossible, so it would mean a scoring bug. (b) B or D exceeding the history reference by more than the near margin, which triggers the leakage investigation. (c) The exchange law failing at held-out rates. (d) The confirmation history reference at 4 bits falling far from the prelim 2.93. (e) D_eff far from D_KY on Lorenz-96. The blinded second author's stated surprise is that token histories substantially beat the single-token information limit, which is this WO's headline claim.

## Check 7: null baseline
Persistence (hold the current prototype) is in the WO. **Added:** a climatological-mean forecast (the calibration mean), scored identically. It is cheap and is reported next to persistence in the headline table.

## Check 8: comparator separability
A priori, the references are well separated (prelim reference 2.93 against decode-and-integrate 0.28 at 4 bits). Separability of the learned arms is decided by the paired intervals on confirmation data. A single most favourable cell is never quoted alone. Every rate, Δ and seed cell appears in tables.

## Check 9: selector separation

**Provenance line.** Systems, rates, frame intervals, arms, margins and readings were authored by Claude (chat), then revised through three external reviews. The executing agent is Claude Code, the same model family.

**Is that sufficient?** No. The rule requires either a *competing* selector from a second author (or a blinded agent) starting elsewhere, with the overlap reported, or three independent framings. Reviews that revise the author's selector do not produce a competing selector. The reviewers' identity, model family and independence are also not documented in the WO.

**Missing items.** (1) A competing selector. (2) Documentation of who the three reviewers were.

**Remedy executed.** A blinded second model (OpenAI Codex, via the codex-rescue agent) received only the research question and proposed its own selector. Its answer is verbatim in `gate/check9_blinded_selector_codex.md`. Overlap:

| Selector | WO | Codex (blinded) | Overlap |
|---|---|---|---|
| Systems | Lorenz-63 ρ = 28, 45; L96 d = 5, 6, 10, 20 | Lorenz-63 ρ = 28; Rössler; Kuramoto–Sivashinsky L = 22 | **1 of 3 (Lorenz-63 ρ = 28 only)**: divergent |
| Rates | 4–12 bits; fit {6, 8, 10, 12}, held out {5, 7, 9, 11} | 2–10 bits; fit even, hold out odd | High (same even/odd design) |
| Frame intervals | 0.02, 0.05, 0.1 tu (0.018–0.09 Tλ on L63) | 0.02, 0.05, 0.1 Tλ | High |
| Horizon | normalized error > 0.3 (0.1, 0.5), Lyapunov times, restricted mean, W = 27 | normalized error 0.2 / 0.4, sustained 3 frames, censor 5 Tλ, survival median | Medium (same construct, different threshold and censoring) |
| Arms | decode-and-integrate, PF history reference, persistence, A/B/C/D/E, A-probe | decode-and-integrate, analogue history reference, categorical versus continuous heads, persistence, climatology, true-state ceiling | High on the core (categorical versus continuous on one backbone, decode-and-integrate, history reference, persistence) |
| Margins | approx equal 90% CI in ±0.10; well below ≥ 0.25 at 95%; near ≤ 0.15 upper 95% | approx equal 90% CI in ±0.10; clearly below 95% CI below −0.25; near 90% CI in ±0.25 | Approx equal identical; well below close; near divergent |
| Exchange law | calibration map h from codebook-direction errors | fixed slope ln 2 / D₁ per bit, intercept fit on even rates | Divergent construct |

**Consequences.** Findings on Lorenz-63 ρ = 28 are covered by both selectors. Claims resting on the choice of other systems (ρ = 45, L96), on the "near" margin, or on the h-map form of the exchange law are labelled **selector-dependent** in `NUMBERS.md` and the results note. As a second-author comparator (no criterion change), the fixed-slope law is also evaluated on the same held-out rates and reported next to the WO criterion.

## Errors found in the WO
1. **Hardware.** Baccus has 3 × NVIDIA CMP 170HX (sm_80, 64/64/40 GB), not an RTX 5080. The 128-core machine is Baccus itself (192.168.88.236). The WO names 192.168.88.228. With Todd's permission the GPUs were freed by stopping three idle Qwen vLLM user services. They are restarted at the end.
2. **Repo.** The WO names the shared private build repo. Todd created a dedicated private repo for this paper (empty) and directed the work there. It has no `main` yet. Only the paper branch is pushed.
3. **Prelim note** absent from the vault MCP at the stated path. It was read from Drive (`R_AIConf-Tokens-Horizon-Prelim-Code-2026-09-23.md`, 46,025 bytes).
4. **Known-zero threshold** is incompatible with the frozen k-means stopping rule at 4 bits (see check 1).
5. **Δ = 0.035** (history sweep) is not a multiple of dt = 0.01, and interpolation is forbidden. The sweep is integrated at dt = 0.005.
6. **Grid count.** "About 175" counts 174 base models. Seeds 3 and 4 at the headline add 16 (A, B and D at 4 and 6 bits, C at both noise levels, Δ = 0.02), for 190 trained backbones plus probes.
7. **Context mismatch.** The PF uses 3.2 tu and the learned arms 3.3 tu. Both are kept as specified, and the mismatch is flagged in comparisons.
8. **Near and well-below readings are degenerate** against the 4-bit bound (≈ 0.12 < 0.15 < 0.25). The WO handles this for "near" but should say so for "well below" too.
