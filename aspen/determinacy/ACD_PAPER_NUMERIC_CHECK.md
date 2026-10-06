# Paper numeric check — Stage 5b

The de-TeXed source preserves original main.tex line numbers. Scientific notation, percentages and thousands separators are normalized; citation keys, figure paths and TeX layout dimensions are not scientific numbers.

**Empirical unmatched numbers: 0.** The raw check_acd.py --text exit is 1 because its generic matcher has no structural exemption switch. The three unmatched literals below are explicitly exempted by Todd and are not failures. acd_paper_check.py returns success only when every unmatched literal is an authorized structural occurrence. All semantic claim checks are in ACD_PAPER_AUDIT.md.

| main.tex line | Literal | Structural meaning |
|---|---|---|
| 63 | 38 | Questions per case/lead |
| 66 | 28 | Pairwise comparisons among eight actions |
| 75 | 512 | Thin-draw forecast count |

Section, equation, table and figure reference labels are structural and are retained in the machine-readable inventory. Bibliographic year, volume, issue, page and identifier fields are listed separately in receipts/acd_stage5b_numeric_check.json (134 fields); they are not empirical numbers requiring experiment receipts. No bibliography was compiled or externally verified in this stage.

Commands on sulaco:

```sh
python3 acd_numbers.py
python3 check_acd.py
python3 acd_paper_check.py
```

The raw numeric-check transcript is receipts/acd_stage5b_paper_check.txt; the de-TeXed input is paper/main.detex.txt; sources remain unedited. No TeX build was attempted.
