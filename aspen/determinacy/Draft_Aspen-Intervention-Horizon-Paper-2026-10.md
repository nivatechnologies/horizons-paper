# Aspen intervention horizon paper — Stage 5c, v3

V3 sources are verified and unchanged. The independent targeted audit resolves all thirteen revised Stage 5b FIX rows. Two declined rows remain pending Todd.

Branch: `paper/aspen-2026-10-determinacy`. Base: `780a74724f9db61d3a63f0782b0e48b296ce361b`.

- [main.tex](https://github.com/nivatechnologies/horizons-paper/blob/paper/aspen-2026-10-determinacy/aspen/determinacy/paper/main.tex)
- [refs.bib](https://github.com/nivatechnologies/horizons-paper/blob/paper/aspen-2026-10-determinacy/aspen/determinacy/paper/refs.bib)
- [Paper audit, including appended v3 review](https://github.com/nivatechnologies/horizons-paper/blob/paper/aspen-2026-10-determinacy/aspen/determinacy/ACD_PAPER_AUDIT.md)
- [Abstract](https://github.com/nivatechnologies/horizons-paper/blob/paper/aspen-2026-10-determinacy/aspen/determinacy/ACD_ABSTRACT_DRAFT.md)
- [Abstract audit and standing rulings](https://github.com/nivatechnologies/horizons-paper/blob/paper/aspen-2026-10-determinacy/aspen/determinacy/ACD_ABSTRACT_AUDIT.md)
- [Numeric check](https://github.com/nivatechnologies/horizons-paper/blob/paper/aspen-2026-10-determinacy/aspen/determinacy/ACD_PAPER_NUMERIC_CHECK.md)
- [V3 audit receipt](https://github.com/nivatechnologies/horizons-paper/blob/paper/aspen-2026-10-determinacy/aspen/determinacy/receipts/acd_stage5c_paper_audit.json)
- [V3 numeric receipt](https://github.com/nivatechnologies/horizons-paper/blob/paper/aspen-2026-10-determinacy/aspen/determinacy/receipts/acd_stage5c_numeric_check.json)
- [Source diff](https://github.com/nivatechnologies/horizons-paper/blob/paper/aspen-2026-10-determinacy/aspen/determinacy/receipts/acd_stage5c_source.diff)

Sulaco working directory: `/home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/`.

SHA-256 verified:

- `paper/main.tex`: `bf58a6d2e183d77d3f2f99fc4626c389770be12d6b83ef4ae4e6d71a314f3978`
- `paper/refs.bib`: `dbd312eced6c7ee98e29e916d68651bbbfeac92cb58fd80bdb22fbb296375d84`

No build attempted. Todd reports the PDF is built off-sulaco; this archive supplies sources only.

Numeric registry regeneration: PASS (6146 keys). **Zero unmatched empirical numbers**. Raw unmatched structural constants: **38 questions at lines 63 and 205, 28 pairs at line 66, 512 thinned draws at line 75**. Document labels and 134 bibliographic metadata fields are separately inventoried.

Current paper audit: **347 OK / 2 FIX**, 349 rows. Targeted v3 review: **17 OK / 0 new FIX**; inherited inventory: 330 OK / 2 FIX. All 13 revised earlier FIX rows resolve. The diff replaces 12 lines without changing line positions of any unchanged sentence or number. Historical Stage 5b receipts are preserved.

## Open rows — declined, pending Todd

| ID / line | Finding | Proposed fix |
|---|---|---|
| P033_05 / 33 | Introduction attributes an implicit matching-horizon assumption to cited practice. Declined as a framing/register issue, pending Todd. | Present this as the research question: whether intervention-sign confidence and confidence in the sign of the unforced window-energy anomaly have matching horizons. |
| P043_01 / 43 | Descriptive z-ratio interpretation remains in the introductory findings list, outside the frozen headline licenses. Declined, pending Todd. | Move the interpretation to Results/Discussion; retain licensed median correlation and cancellation findings in the introduction. |

The abstract artifacts are unchanged from Stage 5b: 13 OK / zero open FIX under Todd's four standing rulings (title, opening framing, defined forecast-sign shorthand, labelled exploratory development amplitude). These rulings do not grant the two pending paper exceptions.

R-other carried forward: L9 U uses all S questions over answered leads; changed-amplitude formal ordering remains unlicensed where calibration prerequisites were not evaluated. Keep both declined paper findings pending rather than infer approval. No H1–H3 stop.

Receipts and static sources only, on sulaco CPU. No new scientific runs, build, cloud compute, training, inference or service changes. Qwen services and Baccus close-out untouched.
