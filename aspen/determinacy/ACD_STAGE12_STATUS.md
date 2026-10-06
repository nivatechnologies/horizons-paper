# Stage 12 status

Post hoc; no frozen-route license. Sulaco CPU only, receipts/code review. No truth access or scientific runs. Spark, GPU, Stage 10 working files and AFD close-out untouched. Qwen services untouched. Paper and abstract remain byte-for-byte as supplied. No build.

## Hash verification

- /tmp/aspen_stage12_payload.tgz: 43ed68af3284114ad2cb7b8c92e87eecfa1aea9c1efcc47be7faaf712c9d1c4f — MATCH
- paper/main.tex: 101347824f089d6a73788a5b951c684972a3985cebfd668d2a24b571b993b4a3 — MATCH
- paper/ABSTRACT_v7.txt: a43391e36e7d0d0925a54680df3ead3c281ba2388f8cae77a7fd44f1af7f08f8 — MATCH
- paper/refs.bib: ab16d40f680e689faa0fc3346c0f6109f184b87d9176e8ff00f27ee403b89c6f — MATCH
Prior abstract retained unchanged.

## Registry and checks

Prior registry keys: 17042. Current keys: 17054. Every prior value unchanged. Registry regeneration: PASS.
Paper raw text check exit: 1. Every unmatched token:
- TeX line 359: 13.5; expected percent bracket encoding of receipt bound.
Abstract text check: PASS; no unmatched tokens. The de-TeX helper was called through its run function with the stage identifier, without changing its tracked source.

Structural literals and document references, separated from empirical claims:
- Line 69: 38; Declared structural question/pair count or thin-draw count; explicitly exempted by Todd
- Line 72: 28; Declared structural question/pair count or thin-draw count; explicitly exempted by Todd
- Line 98: 512; Declared structural question/pair count or thin-draw count; explicitly exempted by Todd
- Line 46: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 54: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 60: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 65: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 73: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 76: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 82: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 106: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 109: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 113: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 119: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 125: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 143: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 146: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 154: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 169: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 170: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 172: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 180: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 201: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 208: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 212: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 213: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 219: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 240: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 246: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 262: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 268: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 275: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 279: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 285: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 292: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 296: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 297: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 303: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 307: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 308: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 314: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 334: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 338: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 341: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 343: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 349: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 368: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 372: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 373: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 381: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 409: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 415: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 428: None; Section/equation/table reference label; resolved numbers belong to document structure
- Line 430: None; Section/equation/table reference label; resolved numbers belong to document structure
Bibliography metadata remains unchanged and outside empirical receipt matching.

## Derived receipt

| Key | Full precision | Evidence |
|---|---|---|
| posterior_POOLED_S_ERROR_2LT | 0.0043177892918825345 | receipts/acd_stage9.json:$.C.posterior.confidence_readings[0].all_confident_accuracy.answer_accuracy; one minus pooled answer accuracy; all confident intervention-sign answers, main amplitude |
| posterior_S_WRONG_2LT | 5 | receipts/acd_stage9.json:$.C.posterior.confidence_readings[0].all_confident_accuracy; rounded integer reconstructed from (1 - answer_accuracy) * answers; integer identity checked within float round-off |
| posterior_S_ANSWERS_2LT | 1158 | receipts/acd_stage9.json:$.C.posterior.confidence_readings[0].all_confident_accuracy.answers; retained pooled all-confident intervention-sign answer count |
| CNN-20k_POOLED_S_ERROR_2LT | 0.05460750853242324 | receipts/acd_stage9.json:$.C.CNN-20k.confidence_readings[0].all_confident_accuracy.answer_accuracy; one minus pooled answer accuracy; all confident intervention-sign answers, main amplitude |
| CNN-20k_S_WRONG_2LT | 64 | receipts/acd_stage9.json:$.C.CNN-20k.confidence_readings[0].all_confident_accuracy; rounded integer reconstructed from (1 - answer_accuracy) * answers; integer identity checked within float round-off |
| CNN-20k_S_ANSWERS_2LT | 1172 | receipts/acd_stage9.json:$.C.CNN-20k.confidence_readings[0].all_confident_accuracy.answers; retained pooled all-confident intervention-sign answer count |
| CNN-F_POOLED_S_ERROR_2LT | 0.008665511265164683 | receipts/acd_stage9.json:$.C.CNN-F.confidence_readings[0].all_confident_accuracy.answer_accuracy; one minus pooled answer accuracy; all confident intervention-sign answers, main amplitude |
| CNN-F_S_WRONG_2LT | 10 | receipts/acd_stage9.json:$.C.CNN-F.confidence_readings[0].all_confident_accuracy; rounded integer reconstructed from (1 - answer_accuracy) * answers; integer identity checked within float round-off |
| CNN-F_S_ANSWERS_2LT | 1154 | receipts/acd_stage9.json:$.C.CNN-F.confidence_readings[0].all_confident_accuracy.answers; retained pooled all-confident intervention-sign answer count |
| ZERO_MEAN_MAX_ABS_MEAN_OVER_SD | 0.03421451656293849 | receipts/acd_stage11_clim_tangent.json:$.rows[52].mean_over_sd; maxabs over patterns one through seven and all retained leads; extremizing source row recorded |
| ZERO_MEAN_MIN_NEGATIVE_SHARE | 0.45361328125 | receipts/acd_stage11_clim_tangent.json:$.rows[56].negative_share; min over patterns one through seven and all retained leads; extremizing source row recorded |
| ZERO_MEAN_MAX_NEGATIVE_SHARE | 0.509521484375 | receipts/acd_stage11_clim_tangent.json:$.rows[23].negative_share; max over patterns one through seven and all retained leads; extremizing source row recorded |

## Delta audit

Changed or added source lines: 22, 28, 38, 48, 98, 260, 266, 290, 291, 332, 333, 341, 343, 366, 367, 434, 447. Tangent caption also audited despite unchanged caption text.
paper: 17 OK; 1 FIX.

V7_260 (line 260): The maximum absolute mean/SD is 0.03421451656293849. It rounds to 0.034, but “within 0.034 standard deviations” states a strict upper bound that the exact value exceeds.
Proposed wording: Replace “within 0.034 standard deviations of zero at every lead” with “approximately 0.034 standard deviations from zero at most over the tested leads”.
abstract: 8 OK; 0 FIX.

Stage 11 external-source rows specified by Todd are recorded as outside receipt scope; author-verified against source. This is an author-provenance ruling, not an independent examination of those source texts.
Existing figure captions were checked against the actual PNGs and the retained PDF counterparts: solid/circle and dashed/square tangent curves; variance panels with hatched IQR; reliability model markers and dashes; amplitude lead-specific circles/squares, crosses/plus signs, diamonds/triangles.

## Resolutions

R-other: retain the expected percent-bracket representation exception. Strict upper-bound language receives FIX; preserve paper text pending Todd. No arbitrary unscaled number was added to silence the checker.
Only explicit Stage 12 paths are committed; fast-forward-only publication on the canonical paper branch.
