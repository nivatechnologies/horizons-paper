---
amends: WO_AIConf-Tokens-Horizon-Extension-2026-09-25
created: '2026-09-25'
follows: WO_AIConf-Tokens-Horizon-Extension-Amendment-1-2026-09-25
status: issued
tags:
  - work-order
  - aiconf-papers
  - tokens-horizon
  - paper
title: 'WO amendment 2: Tokens-horizon extension'
type: work-order-amendment
---
# Amendment 2 to the tokens-horizon extension WO

Apply now, before any further result in the affected items. Commit this amendment into EXT_FREEZE as its own commit. Where Amendment 1 and this amendment differ, this amendment wins. No new experiments and no grid changes: these are execution and wording clarifications plus one release gate.

## B1. A9 ordering, frozen predictor and claim scope
1. **Ordering.** A9 precedes the KS L = 22 whole-state odd-rate (7, 9, 11) decode-and-integrate cells in E3. Bulk E3 evaluation skips those cells until the prediction artifact is committed.
2. **Exposure record.** Before anything else under A9, check whether any odd-rate KS L = 22 whole-state decode-and-integrate horizon was already computed, logged or inspected. Write the answer (yes or no, and what was seen) into the A9 prediction commit. If yes, the test is exposed for those rates: rerunning does not restore held-out status, and the paper reports it as exposed.
3. **Freeze the predictor, not only the slope.** Commit before evaluating any odd rate:
   - form: Ĥ(R) = â + ŝ·R, fitted by ordinary least squares to the per-rate restricted-mean decode-and-integrate horizon (Lyapunov times) at R ∈ {6, 8, 10, 12}, intercept free;
   - Δ, ε = 0.3, window W, panel, and the future-frame primary score, all as frozen for E3;
   - exclusion rule: an even rate is excluded only if more than 5% of its states are censored at W; state any exclusion in the commit, before the fit;
   - the predicted values Ĥ(7), Ĥ(9), Ĥ(11) as numbers;
   - pass criterion per odd rate: the 90% bootstrap CI of (observed − Ĥ(R)) lies within ±0.10 Lyapunov times (the frozen "approximately equal" margin), with Ĥ treated as fixed.
4. **Claim scope.** Replace "This is the only predictive claim the slope form can make" with: "This tests prospective interpolation across held-out rates within the specified system, tokenizer family and rate range; it does not test extrapolation or cross-system transfer." Label the result that way in the results note and NUMBERS.

## B2. A6 negative wording, candidate ordering and the contrast
1. **Negative result wording.** Replace "No tested practical configuration was support-limited at this tolerance" with: "No tested configuration satisfying the E4 size requirements had a validation restricted-mean support horizon below one Lyapunov time." The representability map and survival fractions describe everything else.
2. **Ordering of equal-rate candidates.** Freeze in EXT_FREEZE, before any validation bound is inspected for selection: among eligible candidates with equal total bits per frame, prefer in order (a) L = 22 over the larger domain, (b) the primary frame interval over others, (c) the lower validation mean support horizon, (d) the configuration ID in lexical order. If validation bounds were already inspected, record that in the commit.
3. **Contrast.** Rename "nearby non-binding configuration" to "support-permissive contrast". Criterion: the smallest-bits configuration in the same tokenizer family, domain, patching and Δ as the selected cell, with more total bits per frame, whose validation restricted-mean support horizon is at least 3 Lyapunov times and whose validation S_out(1) (B4) is at least 0.9. Do not call it non-binding; whether its ceiling constrains the learner is read afterwards from the B4 tie statistics and the ratio of learned horizon to cap.
4. **No qualifying contrast.** If no configuration in the evaluated grid meets the criterion, train no contrast, report "no support-permissive contrast within the tested grid", and do not extend the grid to find one.

## B3. A7 frame alignment and masking contract
Add to the frozen E4 model contract:
- All patch predictions for frame t+1 use only frames through t. No ground-truth token from frame t+1, including tokens at other patch positions, enters any prediction for frame t+1.
- Shift targets by one complete frame, not by one flattened token.
- Full attention among the patches of an observed input frame is allowed; attention from any position into frame t+1 or later is not.
- **Required test (commit before training):** for random inputs, change every token in frames t+1 onward and assert that all predictions made from the unchanged prefix (frames through t) are bitwise identical, for A, B and C. The test runs in CI or the pre-training check and its pass is logged.

## B4. Survival units and censored ties (A4 and A8.2)
1. **Survival.** S_out(τ) = P(λ·T_out > τ), where T_out is the physical time of the first scored frame outside tolerance of the decoded support and τ is in Lyapunov times. S_out(τ) is the share of states whose every scored frame at normalized time ≤ τ is covered. A frame exactly at τ counts as "through τ". States with no failure inside the window are right-censored and count as surviving for τ ≤ W; τ > W is not reported. Report τ = 1, 3, 10 (10 only where W ≥ 10).
2. **Ties.** Keep the restricted-horizon comparison. For the failure-frame tie statistic, condition on a support failure that is observed inside the window and after the first scored frame: P(VPT_model = T_out | Δ < T_out ≤ W, failure observed). Report separately:
   - automatic first-frame cases (T_out = Δ);
   - jointly censored cases (both the model and the support survive the window). These are not ties and do not enter the tie statistic.
   Apply to A, persistence and the random-code forecaster (A8.2), and to every E4 learned cell, including the contrast, where censoring may dominate.

## B5. Release gate: bootstrap resampling unit
This is a gate, not documentation. Before the paper is released:
1. Put into NUMBERS (A8.4): number of confirmation trajectories, their lengths, spacing between state start times, the scoring window in time units, and the resampling unit the code actually uses, read from the code rather than the protocol text.
2. Check independence: if states that share a trajectory have overlapping scoring windows (start spacing shorter than the window plus one decorrelation time), resampling individual states understates the intervals.
3. If the check fails, rerun every reported CI with the trajectory (or non-overlapping block) as the resampling unit, resampling the same units for both sides of every paired difference; regenerate NUMBERS; and list every frozen reading whose outcome changes. The paper uses the corrected intervals.
4. Record the gate outcome (pass, or fail plus rerun) in the results note. Release does not proceed until it is recorded.

## Order of work
B3 and B2.2 before any E4 training or selection; B1.1 and B1.2 now; B1.3 before any odd-rate cell; B4 wherever the affected statistics are computed; B5 before release. Cut order is unchanged from A10.
