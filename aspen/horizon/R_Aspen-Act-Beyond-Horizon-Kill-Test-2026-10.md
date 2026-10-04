# Aspen act beyond the horizon: results and execution status (2026-10)

Execution complete with the prescribed Kolmogorov calibration stop; no two-system empirical PASS/KILL.

Work order: [[WO_Aspen-Act-Beyond-Horizon-Kill-Test-2026-10-03]]. Gate: [[R_Aspen-Act-Beyond-Horizon-Spec-Gate-2026-10-04]].

Repository: nivatechnologies/horizons-paper, branch `paper/aspen-2026-10-horizon`. Protocol: `aspen/horizon/AAH_FREEZE.md`; measured calibration addenda precede each system's test/training. Step 0 complete and not rerun.

M_95 is only a tested-grid budget in {8,16,32,64,128,256}. Censored unpaired numerator is conservatively 256; censored paired fails. Bootstrap confidence/commitment levels are nominal; empirical errors are reported.

Machines: Baccus for Kolmogorov and FNO; sulaco for Lorenz and brute-force truth ensembles. No Qwen service stopped.

## Lorenz-96

Calibration status: READY_FOR_CALIBRATION_FREEZE_ADDENDUM; selected delta: 0.02.

| delta | Determinable | Panel | Fraction |
|---|---|---|---|
| 0.01 | 2 | 40 | 0.050 |
| 0.02 | 36 | 40 | 0.900 |

Niva forecast horizon T_f=10.0 LT; sustained decision horizon T_d=12.0 LT.

| T (LT) | Eligible / panel | Niva top-1 (M64) | Forecast ACC | Myopic top-1 | Paired / unpaired M95 |
|---|---|---|---|---|---|
| 0.25 | 200 / 200 | 1.0000 | 0.9996 | 1.0000 | 8 / 8 |
| 0.5 | 200 / 200 | 1.0000 | 0.9990 | 1.0000 | 8 / 8 |
| 0.75 | 200 / 200 | 1.0000 | 0.9980 | 1.0000 | 8 / 8 |
| 1.0 | 200 / 200 | 1.0000 | 0.9963 | 1.0000 | 8 / 8 |
| 1.5 | 195 / 200 | 0.9949 | 0.9868 | 0.9590 | 8 / 64 |
| 2.0 | 193 / 200 | 0.9637 | 0.9625 | 0.8394 | 64 / 128 |
| 2.5 | 180 / 200 | 0.9389 | 0.9232 | 0.7000 | 128 / 256 |
| 3.0 | 161 / 200 | 0.9317 | 0.8623 | 0.6335 | 128 / >256 |
| 4.0 | 125 / 200 | 0.9200 | 0.7115 | 0.5360 | 256 / 256 |
| 5.0 | 109 / 200 | 0.8532 | 0.5492 | 0.7523 | 256 / >256 |
| 6.0 | 126 / 200 | 0.8492 | 0.4086 | 0.8889 | 256 / 256 |
| 8.0 | 184 / 200 | 0.8207 | 0.2175 | 0.9946 | 256 / 128 |
| 10.0 | 199 / 200 | 0.8191 | 0.1140 | 1.0000 | 128 / 128 |
| 12.0 | 200 / 200 | 0.8450 | 0.0601 | 1.0000 | 128 / 128 |
| 16.0 | 200 / 200 | 0.7900 | 0.0226 | 1.0000 | 128 / 128 |
| 20.0 | 200 / 200 | 0.8500 | 0.0094 | 1.0000 | 128 / 128 |

Lorenz reading misses PASS: sustained horizon 12 is below the required G(30), which is outside the frozen grid; paired/unpaired M95 ratio at T_f is 1 (128 members each). At G(1.5 T_f)=16, accuracy 0.79 does not meet the <0.5 KILL rule.

Learned-arm evaluation included.

Learned stability: 0 dropped of 51200 attempted members under the all-action 21-LT rule.

| T (LT) | Learned top-1 (M64) | Learned ACC | Response correlation | Response relative error |
|---|---|---|---|---|
| 0.25 | 1.0000 | 0.9999 | 0.9934 | 0.2016 |
| 0.5 | 1.0000 | 0.9998 | 0.9890 | 0.1677 |
| 0.75 | 1.0000 | 0.9995 | 0.9793 | 0.2024 |
| 1.0 | 0.9900 | 0.9991 | 0.9637 | 0.2653 |
| 1.5 | 0.8667 | 0.9964 | 0.9157 | 0.4407 |
| 2.0 | 0.7358 | 0.9874 | 0.8471 | 0.6714 |
| 2.5 | 0.6667 | 0.9701 | 0.7675 | 0.9186 |
| 3.0 | 0.6211 | 0.9383 | 0.6974 | 1.1200 |
| 4.0 | 0.4160 | 0.8387 | 0.6089 | 1.3134 |
| 5.0 | 0.4954 | 0.6807 | 0.5468 | 1.5323 |
| 6.0 | 0.4603 | 0.5229 | 0.5430 | 1.6365 |
| 8.0 | 0.5815 | 0.2809 | 0.5980 | 1.1899 |
| 10.0 | 0.7990 | 0.1477 | 0.7447 | 0.7335 |
| 12.0 | 0.8300 | 0.0749 | 0.7868 | 0.6326 |
| 16.0 | 0.8350 | 0.0228 | 0.7901 | 0.6184 |
| 20.0 | 0.8250 | 0.0056 | 0.7948 | 0.6167 |

## Kolmogorov

Calibration status: CALIBRATION_FAIL; selected delta: None.

| delta | Determinable | Panel | Fraction |
|---|---|---|---|
| 0.01 | 6 | 20 | 0.300 |
| 0.02 | 6 | 20 | 0.300 |
| 0.05 | 13 | 20 | 0.650 |
| 0.1 | 13 | 20 | 0.650 |

No amplitude meets 16/20. Kolmogorov stopped under A8: no escalation, replacement panel, chaos gate, test ensemble or FNO data/training. Prepared code was not executed. This is a calibration failure, not the empirical KILL criterion.

## Descriptive response/forecast correlations

Unit: (arm,T), pooling learned/misidentified/jitter within each system. Full-rank QR residuals; unavailable coefficients stay unavailable; no inferential or strongest-practice claim. Pending learned evidence means an incomplete panel.

| System | Available / attempted units | Learned Tf / status | Accuracy–response controlling ACC | Accuracy–ACC controlling response |
|---|---|---|---|---|
| l96 | 48 / 48 | 10.0 / defined | 0.9454 | -0.4762 |

## Evidence and completion

Every measured number is generated from JSON sources into `aspen/horizon/NUMBERS.md` (AAH sections). `make_numbers.py check` replays source values and reports zero mismatches; a deliberate numeric mutation was rejected.

Raw arrays/logs are retained under each compute checkout’s `aspen/horizon/runs/`; source SHAs accompany summaries. Lorenz calibration launch-tag correction is explicitly recorded in its source JSON and calibration freeze addendum; numerical data unchanged.

Commitment wall times measure nested forecast cohorts plus bootstrap interval analysis, sharing all 16 horizons. They exclude parameter identification, observation preparation and sampler setup; no end-to-end planner latency claim is made.

Optional cuts fixed before data, in the WO order: latent emulator, W=2 sensitivity, impulsive timing. All mandatory Lorenz arms were retained. The planned 30-case Kolmogorov panel and FNO were not executed because its calibration failed.

No two-system PASS/KILL finding is inferred from a stopped system. Calibration/chaos failures stop the affected part. Results and session review are published through the niva-obsidian MCP.

Greyscale PNG/PDF figures: repository `aspen/horizon/figures/decision_and_forecast`, `members_paired_unpaired`, and `learned_response_and_forecast`. A stopped system is explicitly marked unavailable. Checked NUMBERS sections AAH* replay source measurements with zero mismatches.

Generated by `aspen/horizon/results_note.py` into `04-Results/R_Aspen-Act-Beyond-Horizon-Kill-Test-2026-10.md`.

Lorenz CNN training complete: 20000 updates, 999681 parameters; best normalized 1-LT validation MSE 0.00052633801. Training score is not test performance. The final 200-case test evaluation uses the same full-FP32 sulaco CUDA backend with TF32 disabled; preliminary CPU outputs retained and excluded.

## Post-hoc action-frequency diagnostic

Diagnostic only; no selector or criterion changed. Uniform negative-forcing action 0 is the truth-best action in every eligible Lorenz case at 10, 12, 16, 20 LT. The myopic null selects action 0 for all 200 cases. This is a boundary of the selected action panel, not a universal claim about planning. Selector: final blinded Codex run1 action set; one framing.

Source: `results/l96_posthoc_action_frequency.json`; checked section AAHLPOSTHOC.

## Artifact audit

All 200 learned cases pass the retained-artifact check: one CUDA backend/source/checkpoint, frozen output times and consistent finite-survivor/drop records. The ACC norm-floor correction affects 0 saved physical values and 0 learned values. Calibration replay exactly reproduces all 80 Kolmogorov panel records from 20,480 finite member files. Sources: `results/l96_neural_artifact_audit.json`, `results/kolmo_calibration_audit.json`; checked AAHLNAUDIT/AAHKCAUDIT sections.
