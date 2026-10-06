# Counterfactual determinacy claim ledger

| Date | Headline / stage | Effect at operating point | Breadth | Headline value | Change type | Reason | Trigger hit? |
|---|---|---|---|---|---|---|---|
| 2026-10-05 | v2.1 hypothesis: instance intervention-sign confidence, covariance and question-targeted measurement | Unmeasured | One-scale L96, N40, declared noise/actions | Unmeasured | None | Synthetic .888 answer-accuracy counterexample invalidates bootstrap gate | Pre-data spec halt at91e77a6 |
| 2026-10-05 | v2.2 uses case-averaged calibration, with answer-level point alongside | Unmeasured | Same scientific setting | Unmeasured | Explicit estimand/status amendment | Grid inversion omitted unrejected .9629/.0371 | Pre-data spec halt atdd82355 |
| 2026-10-05 | v2.3 Stage1: question-targeted four-site probes resolve more open decision questions than forecast/spread/random targeting | Q 0.450 vs best alternative 0.217; margin 0.233; max paired p 0.00025939941 | Development only: 200 cases; first60 qualifying measurement cases; known one-scale law, N40, Ftrue8; unknown inferred F in[6,10] | Meets STRONG margin .15 and publish margin .10; confirmation unmeasured | Data update and prescribed compute reductions | Calibration PASS; 192/200 truth coverage. Intervention-sign confidence precedes factual-anomaly confidence | Stage1 STRONG; Todd decides separately on freeze/confirmation |

At2LT, observation-confident S share 0.6238; confident Fc share 0.8450. R0 case accuracy 0.9942, lower 0.976; answer-level accuracy 0.9940. R2b PRECEDES, paired loss difference -0.2097. The proposed “outlives” direction is not supported on development.

Resolution rules: R-other, R-rml, R-time. R-time cuts optional arms/leads, caps R5 at60 and uses500 draws/chain. R-rml retains the independent approximate cross-check and reports signed-event diagnostics; its Stage1a rerun rule did not trigger. R-other retains the literal climate classification, names only tested targeting arms, and treats Wilks coverage as approximate.

Largest remaining risk: independent confirmation is unmeasured; leads, thresholds and operating point were chosen after AFD exploratory results. Only confirmation can supply evidence for publication. This result does not authorize a freeze or inference.

[Stage1 reading](https://github.com/nivatechnologies/horizons-paper/blob/paper/aspen-2026-10-determinacy/aspen/determinacy/ACD_STAGE1_READING.md). Full receipt: `receipts/acd_stage1.json`; numerical checks: `ACD_NUMERICAL_REPORT.md`; complete raw inventory: `ACD_ARTIFACTS.json`.

Historical ledger text is preserved in `sources/Ledger_pre_stage1.md`. Related: [[WO_Aspen-Counterfactual-Determinacy-2026-10-04]], [[R_Aspen-Counterfactual-Determinacy-Stage1-2026-10]], [[T_Research-Paper-Guideline]].

## Confirmation update — 2026-10-05

§11 status **PUBLISH**. Independent 200-case confirmation at the frozen noise, actions, law and compute settings. R0 at2LT PASS, at3LT PASS; truth coverage 189/200. R2a statuses: 2LT DIFFERS, 3LT DIFFERS. R2b PRECEDES, Δ_loss -0.308787. R5 DOES NOT BEAT: Q 25.00%, best alternative 16.67%, margin 0.083333.

The historical development-only risks above describe Stage1. Confirmation numbers now determine publication licensing under §11; every licensed or unavailable sentence is enumerated in the confirmation reading. Scope remains this one-scale perfect-model Lorenz-96 setting; no broader system claim is licensed. Resolution rules: R-diag, R-other, R-rml, R-time.

[Confirmation reading](https://github.com/nivatechnologies/horizons-paper/blob/paper/aspen-2026-10-determinacy/aspen/determinacy/ACD_STAGE2_READING.md). Related: [[R_Aspen-Counterfactual-Determinacy-Confirmation-2026-10]].

## Stage4 abstract-to-license ledger — 2026-10-05

Supplied abstract audited; prior missing-input FIX resolved. Publication route remains PUBLISH under frozen §11; release wording fixes remain open. Counts: 2 OK / 10 FIX. Draft unchanged. M/A have no current abstract license.

| Row | Abstract sentence / title / optional sentence | L# | NUMBERS keys | Verdict |
|---|---|---|---|---|
| T | The forecast horizon is not the intervention horizon | Setup + L3b; R2b PRECEDES | ACD_R2B_POINT | FIX |
| T-alt | An intervention's effect loses confidence before the forecast does | L3b; R2b PRECEDES | ACD_R2B_POINT; ACD_R2B_PAIR_SHARES_EARLIER; ACD_R2B_PAIR_SHARES_LATER | FIX |
| S1 | Forecasting systems, from data assimilation to learned world models, are judged by how far ahead they forecast, and interventions on chaotic systems are chosen from those forecasts. | No L# licenses the broad practice claim | None | FIX |
| S2 | We show that, for a single observed instance, confidence in the sign of an intervention's effect is more often lost before confidence in the sign of the forecast it acts on than after. | L3b; R2b PRECEDES; all lead prerequisites met | ACD_R2B_POINT; ACD_R2B_PAIR_SHARES_EARLIER; ACD_R2B_PAIR_SHARES_LATER | FIX |
| S3 | In one-scale Lorenz-96 (N = 40, known law, inferred forcing), observed at every site in 11 noisy snapshots spanning 0.84 Lyapunov times (LT), we compute the full posterior for 200 independent instances and score it against each realized trajectory. | Setup | ACD_CONTRACT_MODEL_IDENTIFIER; ACD_CONTRACT_STATE_DIMENSION; ACD_CONTRACT_FRAMES; ACD_CONTRACT_OBSERVATION_SPAN_LT; ACD_CASES | OK |
| S4 | At 2 LT the posterior answers the sign of a small intervention's effect on window energy with at least 95% probability for 72% of case–action questions (61% beyond what climatology alone gives), against 85% for the sign of the unforced window-energy anomaly, the forecast sign (difference −0.24, 99% interval [−0.35, −0.14]); at 3 LT, 40% against 67%. | L1 and L3a at 2/3 LT; R0/R0-F PASS, R2a DIFFERS | ACD_R1_S_LEAD_2LT; ACD_CONTRACT_CONFIDENCE; ACD_R1_S_CONFIDENT_POINT_2LT; ACD_R1_S_OBSERVATION_POINT_2LT; ACD_R1_FC_CONFIDENT_POINT_2LT; ACD_R2A_0_POINT; ACD_CONTRACT_ROUTE_CI_PERCENT; ACD_R2A_0_LOWER; ACD_R2A_0_UPPER; ACD_R1_S_LEAD_3LT; ACD_R1_S_CONFIDENT_POINT_3LT; ACD_R1_FC_CONFIDENT_POINT_3LT | FIX |
| S5 | Averaged over instances, confident answers that climatology alone does not give are right 99.5% of the time (one-sided 95% lower bound 97.7%). | L2 at 2 LT; R0 PASS | ACD_R0_CASE_ACCURACY_2LT; ACD_CONTRACT_R0_CI_LEVEL; ACD_R0_CASE_LOWER_2LT; ACD_R0_CASE_ACCURACY_3LT | FIX |
| S6 | Paired by instance, intervention-sign confidence is lost before forecast-sign confidence for 59% of actions and after it for 28% (99% interval for the difference [−0.49, −0.13]), although the posterior correlation between factual and counterfactual window energies is 0.97, so their difference carries 3% of the summed uncertainty. | L3b (PRECEDES) + L4 at 2 LT (R0 PASS) | ACD_R2B_PAIR_SHARES_EARLIER; ACD_R2B_PAIR_SHARES_LATER; ACD_CONTRACT_ROUTE_CI_PERCENT; ACD_R2B_LOWER; ACD_R2B_UPPER; ACD_R1M_RHO_MEDIAN_2LT; ACD_R1M_CANCELLATION_MEDIAN_2LT; ACD_R2B_POINT; ACD_R2B_CASES; ACD_R2B_ACTIONS | FIX |
| S7 | Answering every question up to the lead at which the forecast sign is confident for half the instances, and none beyond, would answer 26% of the intervention questions the posterior is not confident on (right 75%) and refuse 7% it is confident on; a deterministic CNN emulator's ensemble is confident on 22% of those open questions and right on 66%. | L9 (R2c) + L8 at 2 LT (R6 complete, posterior R0 PASS) | ACD_CONTRACT_R2C_HALF_CASES; ACD_L9_ANSWERED_NOT_CONFIDENT; ACD_L9_EXCEPTION_ACCURACY; ACD_L9_REFUSED_CONFIDENT; ACD_R6_POSTERIOR_NOT_CONFIDENT_X; ACD_R6_POSTERIOR_NOT_CONFIDENT_Y; ACD_R2C_HORIZON; ACD_R6_POSTERIOR_NOT_CONFIDENT_QUESTIONS; ACD_R6_POSTERIOR_NOT_CONFIDENT_CNN_CONFIDENT; ACD_R6_POSTERIOR_NOT_CONFIDENT_CORRECT | FIX |
| S8 | An intervention's confidence horizon is its own quantity, which a world model used to choose actions would need to report per question. | Setup/headline framing supported by L3b | ACD_R2B_POINT | OK |
| M | The intervention's median z, its effect over its posterior spread, starts at 3.6 times the forecast sign's just after the observation window and falls to 0.61 times it by 2 LT. | Outside L1–L10; no present abstract license | ACD_R1M_ZD_OVER_ZF_RATIO_OF_MEDIANS_0LT; ACD_R1M_ZD_OVER_ZF_RATIO_OF_MEDIANS_2LT; ACD_R1_S_LEAD_2LT; ACD_R1M_Z_D_MEDIAN_0LT; ACD_R1M_Z_F_MEDIAN_0LT; ACD_R1M_Z_D_MEDIAN_2LT; ACD_R1M_Z_F_MEDIAN_2LT | FIX |
| A | In development runs, varying the intervention's amplitude sixteenfold, from 0.5% to 8% of the forcing, keeps the confident intervention-sign share at 2 LT between 73.5% and 79.6%, against 84.5% for the forecast sign. | Development/exploratory, outside L1–L10; no present abstract license | ACD_DEV_AMPLITUDE_RANGE_FACTOR; ACD_DEV_AMPLITUDE_MIN_FRACTION_TRUE_FORCING; ACD_DEV_AMPLITUDE_MAX_FRACTION_TRUE_FORCING; ACD_DEV_AMPLITUDE_ROWS_0_SHARES_0_LEAD; ACD_DEV_AMPLITUDE_ROWS_1_SHARES_0_CONFIDENT_S; ACD_DEV_AMPLITUDE_ROWS_4_SHARES_0_CONFIDENT_S; ACD_DEV_AMPLITUDE_ROWS_0_SHARES_0_CONFIDENT_FC; ACD_NULL_FORCING; ACD_DEV_AMPLITUDE_ROWS_0_AMPLITUDE; ACD_DEV_AMPLITUDE_ROWS_1_AMPLITUDE; ACD_DEV_AMPLITUDE_ROWS_2_AMPLITUDE; ACD_DEV_AMPLITUDE_ROWS_3_AMPLITUDE; ACD_DEV_AMPLITUDE_ROWS_4_AMPLITUDE; ACD_DEV_AMPLITUDE_ROWS_0_SHARES_0_CONFIDENT_S; ACD_DEV_AMPLITUDE_ROWS_2_SHARES_0_CONFIDENT_S; ACD_DEV_AMPLITUDE_ROWS_3_SHARES_0_CONFIDENT_S; ACD_DEV_AMPLITUDE_ROWS_1_SHARES_0_CONFIDENT_FC; ACD_DEV_AMPLITUDE_ROWS_2_SHARES_0_CONFIDENT_FC; ACD_DEV_AMPLITUDE_ROWS_3_SHARES_0_CONFIDENT_FC; ACD_DEV_AMPLITUDE_ROWS_4_SHARES_0_CONFIDENT_FC | FIX |

Full precision, receipt paths, route trace and proposed fixes: ACD_ABSTRACT_AUDIT.md. Follow-up used only existing receipts, with arithmetic conversions for actual snapshot span, confidence levels and tested-amplitude normalization; no scientific reruns. Stage4 R-other scope and wording resolutions are recorded in receipts/acd_stage4_abstract_audit.json.

## Stage5 abstract audit — supersedes Stage4 wording verdicts

Current revised abstract: 5 OK / 10 FIX. Historical Stage4 verdicts remain historical; current rows supersede them.

| Row | Claim | License | Keys | Verdict |
|---|---|---|---|---|
| T | The forecast horizon is not the intervention horizon | L3b / PRECEDES | ACD_R2B_POINT | FIX |
| T-alt | An intervention's effect loses confidence before the forecast does | L3b / PRECEDES | ACD_R2B_POINT | FIX |
| S1 | Forecasting systems, from data assimilation to learned world models, are judged by how far ahead they forecast, and interventions on chaotic systems are chosen from those forecasts. | No L# |  | FIX |
| S2 | We show that, for a single observed instance, confidence in the sign of an intervention's effect is more often lost before confidence in the forecast sign, the sign of the unforced window-energy anomaly, than after. | L3b / PRECEDES | ACD_R2B_POINT; ACD_R2B_PAIR_SHARES_EARLIER; ACD_R2B_PAIR_SHARES_LATER | FIX |
| S3 | In one-scale Lorenz-96 (N = 40, known law, inferred forcing), observed at every site in 11 noisy snapshots spanning 0.84 Lyapunov times (LT), we sample the full posterior for 200 independent instances and score it against each realized trajectory. | Setup | ACD_CONTRACT_MODEL_IDENTIFIER; ACD_CONTRACT_STATE_DIMENSION; ACD_CONTRACT_FRAMES; ACD_CONTRACT_OBSERVATION_SPAN_LT; ACD_CASES | OK |
| S4 | At 2 LT the posterior answers the sign of a small intervention's effect on window energy with at least 95% probability for 72% of case–action questions and for 61% beyond what climatology at the true forcing gives, against 85% for the forecast sign; the 61% share minus the 85% share is −0.24 (99% interval [−0.35, −0.14]). | L1 + L3a / DIFFERS | ACD_R1_S_CONFIDENT_POINT_2LT; ACD_R1_S_OBSERVATION_POINT_2LT; ACD_R1_FC_CONFIDENT_POINT_2LT; ACD_R2A_0_POINT; ACD_R2A_0_LOWER; ACD_R2A_0_UPPER; ACD_CONTRACT_CONFIDENCE; ACD_CONTRACT_ROUTE_CI_PERCENT; ACD_R1_S_LEAD_2LT | FIX |
| S5 | At 3 LT, 40% against 67%. | L1 | ACD_R1_S_CONFIDENT_POINT_3LT; ACD_R1_FC_CONFIDENT_POINT_3LT; ACD_R1_S_LEAD_3LT | OK |
| S6 | At 2 LT, averaged over instances, confident intervention-sign answers that climatology alone does not give are right 99.5% of the time (one-sided 95% lower bound 97.7%). | L2 / R0 PASS | ACD_R0_CASE_ACCURACY_2LT; ACD_R0_CASE_LOWER_2LT; ACD_CONTRACT_R0_CI_LEVEL; ACD_R1_S_LEAD_2LT | OK |
| S7 | Paired by instance, intervention-sign confidence is lost before forecast-sign confidence for 59% of an instance's eligible actions and after it for 28%, averaged over instances (99% interval for later minus earlier [−0.49, −0.13]), although at 2 LT the median posterior correlation between factual and counterfactual window energies is 0.975, so their difference carries 3% of the summed uncertainty. | L3b / PRECEDES + L4 | ACD_R2B_PAIR_SHARES_EARLIER; ACD_R2B_PAIR_SHARES_LATER; ACD_R2B_POINT; ACD_R2B_LOWER; ACD_R2B_UPPER; ACD_R1M_RHO_MEDIAN_2LT; ACD_R1M_CANCELLATION_MEDIAN_2LT; ACD_CONTRACT_ROUTE_CI_PERCENT; ACD_R1_S_LEAD_2LT | FIX |
| S8 | In development runs at five amplitudes from 0.5% to 8% of the forcing, the confident intervention-sign share at 2 LT ranges from 73.5% to 79.6%, against 84.5% for the forecast sign. | Outside L1-L10 | ACD_DEV_AMPLITUDE_MIN_FRACTION_TRUE_FORCING; ACD_DEV_AMPLITUDE_MAX_FRACTION_TRUE_FORCING; ACD_DEV_AMP_A0P08_R1_CONFIDENT_S_2LT; ACD_DEV_AMP_A0P64_R1_CONFIDENT_S_2LT; ACD_DEV_AMP_A0P08_R1_CONFIDENT_FC_2LT; ACD_DEV_AMP_TESTED_AMPLITUDES_COUNT; ACD_DEV_AMP_A0P08_R1_LEAD_2LT | FIX |
| S9 | A rule that answers every intervention-sign question through the last lead at which the forecast sign is confident for at least half the instances (3 LT), and none beyond, answers without posterior confidence 26% of the intervention-sign questions in that range, and those answers are right 75% of the time. | L9 with mandated R-other denominator correction | ACD_R2C_HORIZON; ACD_L9_ANSWERED_NOT_CONFIDENT; ACD_L9_EXCEPTION_ACCURACY; ACD_CONTRACT_R2C_HALF_CASES | FIX |
| S10 | At 2 LT, a deterministic CNN emulator's ensemble is confident on 22% of the intervention-sign questions the posterior is not confident on, and right on 66% of those. | L8 / posterior R0 PASS | ACD_R6_POSTERIOR_NOT_CONFIDENT_X; ACD_R6_POSTERIOR_NOT_CONFIDENT_Y; ACD_R6_POSTERIOR_NOT_CONFIDENT_QUESTIONS; ACD_R6_POSTERIOR_NOT_CONFIDENT_CNN_CONFIDENT; ACD_R6_POSTERIOR_NOT_CONFIDENT_CORRECT; ACD_R1_S_LEAD_2LT | OK |
| S11 | An intervention's confidence horizon is its own quantity, which a world model used to choose actions would need to report per question. | Permitted world-model reporting desideratum | ACD_R2B_POINT | OK |
| M | The intervention's median z, its effect over its posterior spread, starts at 3.6 times the forecast sign's just after the observation window and falls to 0.61 times it by 2 LT. | Outside L1-L10 | ACD_R1M_ZD_OVER_ZF_RATIO_OF_MEDIANS_0LT; ACD_R1M_ZD_OVER_ZF_RATIO_OF_MEDIANS_2LT; ACD_R1_S_LEAD_2LT; ACD_R1M_Z_D_MEDIAN_0LT; ACD_R1M_Z_F_MEDIAN_0LT; ACD_R1M_Z_D_MEDIAN_2LT; ACD_R1M_Z_F_MEDIAN_2LT | FIX |
| A | In development runs, varying the intervention's amplitude sixteenfold, from 0.5% to 8% of the forcing, keeps the confident intervention-sign share at 2 LT between 73.5% and 79.6%, against 84.5% for the forecast sign. | Outside L1-L10 | ACD_DEV_AMPLITUDE_RANGE_FACTOR; ACD_DEV_AMPLITUDE_MIN_FRACTION_TRUE_FORCING; ACD_DEV_AMPLITUDE_MAX_FRACTION_TRUE_FORCING; ACD_DEV_AMPLITUDE_ROWS_0_SHARES_0_LEAD; ACD_DEV_AMPLITUDE_ROWS_1_SHARES_0_CONFIDENT_S; ACD_DEV_AMPLITUDE_ROWS_4_SHARES_0_CONFIDENT_S; ACD_DEV_AMPLITUDE_ROWS_0_SHARES_0_CONFIDENT_FC; ACD_NULL_FORCING; ACD_DEV_AMPLITUDE_ROWS_0_AMPLITUDE; ACD_DEV_AMPLITUDE_ROWS_1_AMPLITUDE; ACD_DEV_AMPLITUDE_ROWS_2_AMPLITUDE; ACD_DEV_AMPLITUDE_ROWS_3_AMPLITUDE; ACD_DEV_AMPLITUDE_ROWS_4_AMPLITUDE; ACD_DEV_AMPLITUDE_ROWS_0_SHARES_0_CONFIDENT_S; ACD_DEV_AMPLITUDE_ROWS_2_SHARES_0_CONFIDENT_S; ACD_DEV_AMPLITUDE_ROWS_3_SHARES_0_CONFIDENT_S; ACD_DEV_AMPLITUDE_ROWS_1_SHARES_0_CONFIDENT_FC; ACD_DEV_AMPLITUDE_ROWS_2_SHARES_0_CONFIDENT_FC; ACD_DEV_AMPLITUDE_ROWS_3_SHARES_0_CONFIDENT_FC; ACD_DEV_AMPLITUDE_ROWS_4_SHARES_0_CONFIDENT_FC | FIX |

R-other corrects L9 all-S denominator wording; no new abstract license. Full audit: ACD_ABSTRACT_AUDIT.md and receipts/acd_stage5_abstract_review.json. S7 cancellation is a separately measured descriptive median, not a consequence of median correlation alone.


## Stage 5b current abstract disposition (supersedes Stage 5 open rows)

Todd licensed the title, opening framing, defined forecast-sign shorthand and labelled exploratory development amplitude sentence. Current abstract plus titles: 13 OK / 0 FIX. Frozen scientific routes and receipt numbers are unchanged. Optional M/A remain outside the current abstract and carry no new scientific license.

| Row | License / standing deviation | NUMBERS keys | Verdict |
|---|---|---|---|
| T | L3b / PRECEDES; TD-title | ACD_R2B_POINT | OK |
| T-alt | L3b / PRECEDES; TD-title | ACD_R2B_POINT | OK |
| S1 | No L#; TD-opening |  | OK |
| S2 | L3b / PRECEDES; TD-Fc | ACD_R2B_POINT; ACD_R2B_PAIR_SHARES_EARLIER; ACD_R2B_PAIR_SHARES_LATER | OK |
| S3 | Setup;  | ACD_CONTRACT_MODEL_IDENTIFIER; ACD_CONTRACT_STATE_DIMENSION; ACD_CONTRACT_FRAMES; ACD_CONTRACT_OBSERVATION_SPAN_LT; ACD_CASES | OK |
| S4 | L1 + L3a / DIFFERS; TD-Fc | ACD_R1_S_CONFIDENT_POINT_2LT; ACD_R1_S_OBSERVATION_POINT_2LT; ACD_R1_FC_CONFIDENT_POINT_2LT; ACD_R2A_0_POINT; ACD_R2A_0_LOWER; ACD_R2A_0_UPPER; ACD_CONTRACT_CONFIDENCE; ACD_CONTRACT_ROUTE_CI_PERCENT; ACD_R1_S_LEAD_2LT | OK |
| S5 | L1;  | ACD_R1_S_CONFIDENT_POINT_3LT; ACD_R1_FC_CONFIDENT_POINT_3LT; ACD_R1_S_LEAD_3LT | OK |
| S6 | L2 / R0 PASS;  | ACD_R0_CASE_ACCURACY_2LT; ACD_R0_CASE_LOWER_2LT; ACD_CONTRACT_R0_CI_LEVEL; ACD_R1_S_LEAD_2LT | OK |
| S7 | L3b / PRECEDES + L4; TD-Fc | ACD_R2B_PAIR_SHARES_EARLIER; ACD_R2B_PAIR_SHARES_LATER; ACD_R2B_POINT; ACD_R2B_LOWER; ACD_R2B_UPPER; ACD_R1M_RHO_MEDIAN_2LT; ACD_R1M_CANCELLATION_MEDIAN_2LT; ACD_CONTRACT_ROUTE_CI_PERCENT; ACD_R1_S_LEAD_2LT | OK |
| S8 | Outside L1-L10; TD-amplitude, TD-Fc | ACD_DEV_AMPLITUDE_MIN_FRACTION_TRUE_FORCING; ACD_DEV_AMPLITUDE_MAX_FRACTION_TRUE_FORCING; ACD_DEV_AMP_A0P08_R1_CONFIDENT_S_2LT; ACD_DEV_AMP_A0P64_R1_CONFIDENT_S_2LT; ACD_DEV_AMP_A0P08_R1_CONFIDENT_FC_2LT; ACD_DEV_AMP_TESTED_AMPLITUDES_COUNT; ACD_DEV_AMP_A0P08_R1_LEAD_2LT | OK |
| S9 | L9 with mandated R-other denominator correction; TD-Fc | ACD_R2C_HORIZON; ACD_L9_ANSWERED_NOT_CONFIDENT; ACD_L9_EXCEPTION_ACCURACY; ACD_CONTRACT_R2C_HALF_CASES | OK |
| S10 | L8 / posterior R0 PASS;  | ACD_R6_POSTERIOR_NOT_CONFIDENT_X; ACD_R6_POSTERIOR_NOT_CONFIDENT_Y; ACD_R6_POSTERIOR_NOT_CONFIDENT_QUESTIONS; ACD_R6_POSTERIOR_NOT_CONFIDENT_CNN_CONFIDENT; ACD_R6_POSTERIOR_NOT_CONFIDENT_CORRECT; ACD_R1_S_LEAD_2LT | OK |
| S11 | Permitted world-model reporting desideratum;  | ACD_R2B_POINT | OK |

R-other retains the corrected all-S denominator for R2c U. Full disposition: ACD_ABSTRACT_AUDIT.md and receipts/acd_stage5b_abstract_audit.json.

## Stage 5b paper review

Independent paper audit: 332 OK and 15 open FIX rows. Sources remain immutable; proposed fixes are in ACD_PAPER_AUDIT.md and receipts/acd_stage5b_paper_audit.json. Current abstract: 13 OK, zero open FIX rows under Todd’s four standing rulings. These editorial rulings do not expand the frozen scientific licenses.

Open paper rows: P033_05, P037_05, P043_01, P043_02, P094_03, P118_02, P118_03, P118_06, P166_06, P196_01, P205_01, P210_09, P231_03, P233_04, P247_02.

## Stage 5c paper v3 — targeted audit

Main.tex v3 is immutable at SHA-256 bf58a6d2e183d77d3f2f99fc4626c389770be12d6b83ef4ae4e6d71a314f3978. Thirteen revised prior FIX rows resolve; P033_05 and P043_01 remain FIX, declined, pending Todd. Current full-paper inventory: 347 OK / 2 FIX across 349 rows, comprising 17 changed/new OK rows and 332 carried rows (330 OK / 2 FIX). Sources and numerical values do not expand licenses; R-other continues to withhold changed-amplitude formal ordering without calibration prerequisites. Evidence: appended ACD_PAPER_AUDIT.md and receipts/acd_stage5c_paper_audit.json. Abstract artifacts and their prior standing rulings are unchanged.
