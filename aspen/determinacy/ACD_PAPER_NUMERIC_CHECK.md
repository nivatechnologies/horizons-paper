# V4 numeric check — Stage 7

Both supplied-text checks have zero unmatched literals. NUMBERS regeneration passes with 12016 keys. Matching alone verifies rounding; the independent audits verify meaning, denominator and source.

Checked paper/main.detex.txt (original TeX line numbers retained); raw output: receipts/acd_stage7_paper_check.txt. Checked the supplied ABSTRACT_v4.txt verbatim before moving the temporary file out of the repository; raw output: receipts/acd_stage7_abstract_check.txt. The abstract source hash is in receipts/acd_stage7_source.json.

Structural constants are separately inventoried even when an unrelated registry value matches them:

| Line | Constant | Meaning |
|---|---|---|
| 66 | 38 | Declared structural question/pair count or thin-draw count; explicitly exempted by Todd |
| 69 | 28 | Declared structural question/pair count or thin-draw count; explicitly exempted by Todd |
| 95 | 512 | Declared structural question/pair count or thin-draw count; explicitly exempted by Todd |
| 312 | 38 | Declared structural question/pair count or thin-draw count; explicitly exempted by Todd |

Document label/reference occurrences: 36. Bibliographic metadata fields: 143; years, volumes, pages and identifiers are inventoried in receipts/acd_stage7_numeric_check.json and have no empirical receipt requirement.

Derived keys: ACD_R0_CORRECT_2LT (971 × answer accuracy = 966); ACD_R0_CASE_ERROR_RATE_2LT (1 − case accuracy); ACD_POSTHOC_STAGE6_C_CASE_ERROR_RATE_2LT (1 − post hoc CNN case accuracy). The pattern-table maximum forcing changes and fractions also have explicit closed-form contract derivations.

No TeX build, scientific integration, sampling, fitting, training or inference. Prior Stage 5 check receipts remain unchanged.
