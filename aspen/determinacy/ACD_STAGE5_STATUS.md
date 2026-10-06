# Stage 5b — sources and draft audit complete

Base: 77026bc25841c1b0b73899c1c6c493b137bcaca3. Todd's embedded archive was decoded on sulaco; paper/main.tex and paper/refs.bib were verified against the supplied SHA-256 values before use and remain unchanged.

Completed:
- Independent ACD_PAPER_AUDIT.md: 332 OK / 15 FIX across 347 rows. All methods are checked against frozen WO and code. Proposed fixes are recorded; main.tex is not edited.
- Paper de-TeX extraction and numeric check: zero empirical unmatched numbers. Authorized structural unmatched values are 38, 28 and 512 at lines 63, 66 and 75. Bibliographic metadata and document labels are inventoried separately.
- NUMBERS registry: 6146 keys; regeneration passes.
- ACD_ABSTRACT_DRAFT.md: only the abstract's amplitude sentence changes from “In development runs” to “In exploratory development runs”. Titles and optional text are unchanged.
- ACD_ABSTRACT_AUDIT.md: 13 OK / 0 FIX for current abstract plus retained titles under Todd's four standing rulings. Prior independent findings remain historical artifacts.
- Vault note: 02-Projects/Draft_Aspen-Intervention-Horizon-Paper-2026-10.md, with source/audit/abstract links and every proposed paper fix.

R-other keeps R2c U's corrected ALL-S-question denominator and withholds formal changed-amplitude ordering licenses when realized calibration is unavailable. Standing deviations do not change any numerical threshold.

No TeX build attempted, as instructed. The user reports an off-sulaco pdflatex + bibtex build; no PDF was included in the supplied archive. The current environment is paper/TEX_ENVIRONMENT.json. Page count is not claimed.

No new scientific runs, integrations, sampling, MAP/RML, training or inference. CPU-only receipt/static-source checks on sulaco; no cloud compute; Qwen services and Baccus close-out untouched. Scientific receipts and frozen execution code remain byte-identical to the base commit.

Source receipt: receipts/acd_stage5b_source.json.
Numeric check: ACD_PAPER_NUMERIC_CHECK.md, paper/main.detex.txt and receipts/acd_stage5b_numeric_check.json.
Independent audit receipt: receipts/acd_stage5b_paper_audit.json.
Stage artifact hashes: ACD_STAGE5B_ARTIFACTS.json.

## Stage 5c — v3 targeted audit

Base: 780a74724f9db61d3a63f0782b0e48b296ce361b. V3 main.tex and unchanged refs.bib match the supplied hashes and are committed without source edits. Numeric registry regeneration passes. Empirical unmatched numbers: zero; authorized structural unmatched occurrences are 38 at lines 63/205, 28 at line 66, and 512 at line 75. No build attempted.

The targeted independent audit appends to ACD_PAPER_AUDIT.md. All thirteen revised prior FIX rows resolve. P033_05 and P043_01 remain “declined, pending Todd”. Current paper inventory: 347 OK / 2 FIX across 349 rows; 17 changed/new sentences reviewed, 332 rows carried (330 OK / 2 FIX). No unchanged sentence or number moved lines. Stage 5b audit/check receipts remain historical and unchanged; current receipts use acd_stage5c_* names. Abstract artifacts remain unchanged from Stage 5b, with 13 OK / zero open FIX under standing rulings.

R-other: retain corrected L9 all-S denominator and withhold formal changed-amplitude ordering where calibration prerequisites were not evaluated. Two declined editorial findings remain pending; no additional license inferred. No hard stop or new scientific run. V3 source/diff receipts: receipts/acd_stage5c_source.json and receipts/acd_stage5c_diff.json.
