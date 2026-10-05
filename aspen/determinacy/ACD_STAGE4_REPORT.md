# Aspen Stage4 report — receipt work and abstract audit complete; release FIX rows open

Base: c1d692a06483dd57e4d6159f43333d53fa0ab8ca, branch paper/aspen-2026-10-determinacy. Work and numerical computation ran on sulaco CPU in /home/todd/work/aspen-determinacy-stage4-20261005. Original Stage2 and development receipts and scientific code remain unchanged. No new posterior, fits, training, inference or cloud computation; Qwen services are untouched. Baccus checkout and AFD close-out were not changed. The optional exploration integrates saved development posterior terminal states, as expressly authorized.

NUMBERS: 4704 full-precision keys (eight source-labelled arithmetic/contract additions in the abstract follow-up). check_acd.py regenerates both artifacts and rejects differences; --text handles decimals, scientific notation, percentages, k-units and visible identifiers. Digests and Markdown link destinations are provenance, excluded from prose numbers. Rounding uses round-to-nearest/even at the stated last digit, preserving Stage2 float unit conversions. Literal matching checks rounding only; scientific quantity, panel, unit and license require semantic audit. Every visible number in ACD_STAGE2_READING.md matches (544 extracted). Development keys use ACD_DEV_.

Verification passed: registry and Markdown tampering rejected, unmatched number printed with nonzero exit, lexer/unit/scientific cases, exact development baseline shares and R2b, 1000 bitwise unforced-forecast checks, 200 bitwise baseline whole forecasts, F1 designated pair and opposite answers, reproducible PDF/PNG/caption bytes, original checker archived and scientific modules unchanged. Full receipt: receipts/acd_stage4_verification.json. PDF creation/modification dates are omitted for reproducibility; requirements-stage4.lock records the environment.

Figures are receipt-only, PDF and PNG, greyscale, with second cues. F1 is illustrative confirmation case 6; F2 is frozen confidence by question type; F3 is saved mechanism plus z_D/z_F medians and IQR; F4 marks RML development and other arms confirmation; F5 Q/F/V/R is at frozen settings and notes A was cut. Sources, captions and hashes: receipts/acd_stage4_figures.json and figures/CAPTIONS.md. Figures were visually checked for readable axes and distinct cues.

Optional amplitude exploration completed all 200 development cases at 0.04, 0.08, 0.16, 0.32 and 0.64 on eight workers with two integration threads each (16 CPU threads total). Saved individual draw costs live under runs/stage4_amplitude on sulaco; hashes are in receipts/acd_stage4_amplitude.json. The 0.16 forecast is reused exactly; factual forecasts agree bitwise at every amplitude. The report is labelled development and exploratory, licenses no abstract claim, and distinguishes matched quantities from frozen-null proxies.

**Abstract audit: 2 OK / 10 FIX across 12 rows.** The actual title, alternative title, eight sentences and optional M/A have been audited. Draft preserved verbatim; numeric PASS with 49 extracted literals and zero unmatched. Prior missing-draft FIX resolved. All remaining FIX rows and proposed fixes appear in ACD_ABSTRACT_AUDIT.md; release fixes remain open. No paper was released or submitted.

## Resolution rules

New Stage4 rule: R-other, with the following applications. No H1–H3 hard stop occurred. Earlier R-time, R-rml, R-other and R-diag findings remain carried in the immutable confirmation receipt; Stage4 introduces no new calibration, cutoff or route status.

| Rule | Finding | Resolution |
|---|---|---|
| R-other | Protocol and structural literals have no numeric Stage2 JSON field | Identify contract/source constants separately; empirical values point to actual Stage2 paths. Derived values carry actual input paths and operations; no fabricated receipt path. |
| R-other | Per-question z_D/z_F distribution and window-level divergence quartiles are not saved | Report ratio of saved medians explicitly; window divergence point only. Preserve saved tick-level divergence median/IQR separately; no invented quartiles or new statistic. |
| R-other | Individual physical-state trajectories are not saved for qualifying F1 case 6 | Show existing opposing-draw window-energy curves and saved Q probe, labelled illustrative. Do not reconstruct state trajectories. |
| R-other | Amplitude-matched climatological states are not on disk | No new climatological run. Matched observation confidence and R2b unavailable away from 0.16; display frozen-null-relative exploratory proxies explicitly, with no route status or abstract license. |
| R-other | Abstract follow-up: Fc naming, ambiguous estimands and outside-license M/A | Preserve supplied draft, flag affected rows, propose precise licensed wording; no implicit waiver or new license. Historical missing-input FIX is resolved. |

## Artifact pointers

- [NUMBERS_ACD.md](https://github.com/nivatechnologies/horizons-paper/blob/paper/aspen-2026-10-determinacy/aspen/determinacy/NUMBERS_ACD.md)
- [numbers_acd.json](https://github.com/nivatechnologies/horizons-paper/blob/paper/aspen-2026-10-determinacy/aspen/determinacy/numbers_acd.json)
- [check_acd.py](https://github.com/nivatechnologies/horizons-paper/blob/paper/aspen-2026-10-determinacy/aspen/determinacy/check_acd.py)
- [ACD_MECHANISM.md](https://github.com/nivatechnologies/horizons-paper/blob/paper/aspen-2026-10-determinacy/aspen/determinacy/ACD_MECHANISM.md)
- [acd_figures.py](https://github.com/nivatechnologies/horizons-paper/blob/paper/aspen-2026-10-determinacy/aspen/determinacy/acd_figures.py)
- [figures/CAPTIONS.md](https://github.com/nivatechnologies/horizons-paper/blob/paper/aspen-2026-10-determinacy/aspen/determinacy/figures/CAPTIONS.md)
- [ACD_ABSTRACT_DRAFT.md](https://github.com/nivatechnologies/horizons-paper/blob/paper/aspen-2026-10-determinacy/aspen/determinacy/ACD_ABSTRACT_DRAFT.md)
- [ACD_ABSTRACT_AUDIT.md](https://github.com/nivatechnologies/horizons-paper/blob/paper/aspen-2026-10-determinacy/aspen/determinacy/ACD_ABSTRACT_AUDIT.md)
- [CLAIM_LEDGER.md](https://github.com/nivatechnologies/horizons-paper/blob/paper/aspen-2026-10-determinacy/aspen/determinacy/CLAIM_LEDGER.md)
- [ACD_AMPLITUDE_EXPLORATORY.md](https://github.com/nivatechnologies/horizons-paper/blob/paper/aspen-2026-10-determinacy/aspen/determinacy/ACD_AMPLITUDE_EXPLORATORY.md)
- [receipts/acd_stage4_verification.json](https://github.com/nivatechnologies/horizons-paper/blob/paper/aspen-2026-10-determinacy/aspen/determinacy/receipts/acd_stage4_verification.json)
- [receipts/acd_stage4_amplitude.json](https://github.com/nivatechnologies/horizons-paper/blob/paper/aspen-2026-10-determinacy/aspen/determinacy/receipts/acd_stage4_amplitude.json)

## Abstract follow-up at 91462d0

The only new rule is R-other for naming, measured scope, exact estimands and outside-license optional material. Audit complete: 2 OK / 10 FIX; numerical values and ratios round correctly. Metadata alone was added to NUMBERS so semantic mappings use actual quantities rather than coincidental rounding matches. No model runs, plotting, calibration, thresholds or decision routes changed. New audit input/receipt: receipts/acd_stage4_abstract_audit.json; renderer: acd_abstract_audit.py. Proposed fixes await editorial disposition, not further computation.
