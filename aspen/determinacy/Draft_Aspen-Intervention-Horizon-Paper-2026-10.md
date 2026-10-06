# Aspen intervention horizon paper — Stage 5b

Stage 5b source intake, numeric check and independent paper audit are complete. The draft remains unchanged; proposed paper corrections remain open.

Branch: paper/aspen-2026-10-determinacy. Base: 77026bc25841c1b0b73899c1c6c493b137bcaca3.

- [main.tex](https://github.com/nivatechnologies/horizons-paper/blob/paper/aspen-2026-10-determinacy/aspen/determinacy/paper/main.tex)
- [refs.bib](https://github.com/nivatechnologies/horizons-paper/blob/paper/aspen-2026-10-determinacy/aspen/determinacy/paper/refs.bib)
- [Independent paper audit](https://github.com/nivatechnologies/horizons-paper/blob/paper/aspen-2026-10-determinacy/aspen/determinacy/ACD_PAPER_AUDIT.md)
- [Abstract](https://github.com/nivatechnologies/horizons-paper/blob/paper/aspen-2026-10-determinacy/aspen/determinacy/ACD_ABSTRACT_DRAFT.md)
- [Abstract standing-ruling disposition](https://github.com/nivatechnologies/horizons-paper/blob/paper/aspen-2026-10-determinacy/aspen/determinacy/ACD_ABSTRACT_AUDIT.md)
- [Paper numeric check](https://github.com/nivatechnologies/horizons-paper/blob/paper/aspen-2026-10-determinacy/aspen/determinacy/ACD_PAPER_NUMERIC_CHECK.md)
- [Number registry](https://github.com/nivatechnologies/horizons-paper/blob/paper/aspen-2026-10-determinacy/aspen/determinacy/NUMBERS_ACD.md)
- [TeX environment](https://github.com/nivatechnologies/horizons-paper/blob/paper/aspen-2026-10-determinacy/aspen/determinacy/paper/TEX_ENVIRONMENT.json)

Working directory on sulaco: `/home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/`.

Both source SHA-256 hashes match Todd's supplied values:
- main.tex: `8dc6f207a0b8fc8abe4b12849e335d583df34231b8f4e9e66dd8f8ec8a78eb5e`
- refs.bib: `dbd312eced6c7ee98e29e916d68651bbbfeac92cb58fd80bdb22fbb296375d84`

No TeX build was attempted, as instructed. Todd reports an off-sulaco pdflatex + bibtex build; the supplied archive contains only the two sources, not a PDF.

Numeric registry: 6146 keys, regeneration PASS. Paper empirical unmatched numbers: **0**. Raw unmatched structural constants: **38 questions (line 63), 28 pairs (line 66), 512 draws (line 75)**. Section/equation/table/figure labels and 134 bibliographic metadata fields are separately inventoried; they are not scientific failures.

Independent paper audit: **332 OK / 15 FIX**, 347 rows, including methods checked against the frozen WO and code. Current abstract and retained titles: **13 OK / 0 FIX** under Todd's standing rulings. The only abstract text change is “In exploratory development runs”.

Todd-licensed deviations: title; opening framing sentence; forecast-sign shorthand defined at first use; labelled exploratory development amplitude sentence. These do not change route thresholds or turn development readings into confirmation evidence.

R-other: keep the corrected all-S denominator for R2c U; at changed amplitudes, report exploratory estimates and intervals without a formal ordering license when calibration prerequisites are unmet. No H1–H3 stop.

## Paper FIX rows

| ID / main.tex line | Proposed fix |
|---|---|
| P033_05 / 33 | Present this as the paper’s question: “We ask whether an intervention-sign confidence horizon matches the confidence horizon of the sign of the unforced window-energy anomaly.” |
| P037_05 / 37 | “The protocol and development reading were frozen before confirmation observations and outcomes were generated.” |
| P043_01 / 43 | Move this descriptive z-ratio interpretation to Results or Discussion. In the introduction retain the L4 median correlation and cancellation values. |
| P043_02 / 43 | Replace the ordering claim with exploratory loss-difference point estimates −0.228, −0.220 and −0.210 at amplitudes 0.04, 0.08 and 0.16. State that calibration at changed amplitudes was not recomputed and their formal R2b prerequisites are unmet. At 0.32 and 0.64 the numerical intervals span zero. Move the linear-response hypothesis to Discussion. |
| P094_03 / 94 | “Confident forecast-sign answers pass the separate R0-F criterion at every evaluable lead: at least 30 confident cases and an exact one-sided 95% lower bound of at least 0.90.” |
| P118_02 / 118 | Give the observed shares without equivalence wording: “At 0 LT the shares are 98.3% and 97.0%; at 1 LT they are 91.4% and 92.0%.” |
| P118_03 / 118 | Label the per-lead all-confidence shares descriptive. State the formal DIFFERS result using observation-confident S and confident Fc at 2 and 3 LT only. |
| P118_06 / 118 | “For the other seven patterns the climatological modal sign has probability 0.50–0.56 at every lead, so neither sign is climate-confident.” |
| P166_06 / 166 | “The exploratory loss-difference intervals span zero at amplitudes 0.32 and 0.64; their formal R2b status is PREREQUISITE NOT MET.” |
| P196_01 / 196 | “We use a 128-member ensemble formed by perturbing the last observed frame with observation noise and using the forcing estimated from the observations.” |
| P205_01 / 205 | Add: “Posterior, crude and development RML aggregate all 38 saved question types at all eight leads, including P/B at leads omitted from the confidence maps; CNN uses 2 LT only. Curves are descriptive and do not establish an ordering.” |
| P210_09 / 210 | Add the frozen requirements: Q must settle at least 20 answers, its exact one-sided 95% accuracy lower bound must be at least 0.80, and its post-probe truth coverage must be at least 0.85. State that confirmation Q settled 15 of 60, below the 20-answer floor, as well as failing the margin and paired-test requirements. |
| P231_03 / 231 | “The observed displacement-to-spread ratio is roughly stable after 1 LT, consistent with shared growth of displacement and spread; the mechanism was not identified.” |
| P233_04 / 233 | “Under the linear-response approximation a positive amplitude scales mean and spread together. The three smallest tested development amplitudes have similar confident shares; realized calibration at changed amplitudes was not recomputed.” |
| P247_02 / 247 | “At 0 LT the observed confidence shares are 98.3% and 97.0%. The calibrated observation-confident S/Fc comparison differs at 2 and 3 LT, and the paired loss reading is PRECEDES.” |

No new scientific runs, integration, sampling, MAP/RML, training or inference. Work used saved receipts and static code on sulaco CPU. No cloud compute, Qwen service changes or Baccus close-out changes.
