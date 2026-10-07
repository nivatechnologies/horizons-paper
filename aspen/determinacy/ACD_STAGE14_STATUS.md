# Stage 14 status

Post hoc; licenses no frozen route. CPU work on sulaco in an isolated checkout. Payload sources retained verbatim; no paper build. Spark, GPU, Stage 10/10b artifacts, Qwen and AFD close-out were not accessed or modified. Existing registry/checker dependency reads were used for mandated registry regeneration; no Stage 10/10b analysis or artifact mutation.

## Payload hashes

| Path | SHA-256 | Check |
|---|---|---|
| /tmp/paper_v8.tgz | 6cfc2900e8a7f07da26b2132648ac875443a21cdb0d0d30f220cbffc566319e0 | PASS |
| paper/main.tex | af9c36b87b7bbd9ed121ab84608d10aa84dadae012d7e6a6ae4926c9b026e086 | PASS |
| paper/ABSTRACT_v8.txt | dc95939bf64d62a5153d208f25343480581bb4907018fc45171bbf333ac4e7af | PASS |
| paper/refs.bib | c520bba342e7e13519ea946b8344885fe6532641eb0cf510dc283ea74bf30bd3 | PASS |

Abstract characters excluding final newline: 1858; whitespace-separated words: 294.

## Registry and text checks

Registry keys: 37738 → 37739. Every previous key retains its entire record, including its value. New key: ACD_POSTHOC_PAPER_V8_CNN_F_RESP_ERROR_UPPER_PERCENT_2LT, calculated from the retained Stage 9 upper bound by percentage scaling.

Paper: PASS; unmatched tokens: none; numeric tokens checked: 1403.
Abstract: PASS; unmatched tokens: none; numeric tokens checked: 25.
Registry: PASS; unmatched tokens: none.

Initial paper unmatched token: line 526, `13.5`. Resolved by computed percentage-unit derivation; no source edit. The de-TeX routine collapses the thousands separator in `15,202`, so its split tokens do not remain unmatched. Structural counts (questions, pairs, draws), section/table/equation labels and bibliography metadata are non-empirical; they are separate from claim licensing.

## Audit counts

Paper: OK 843; FIX 6.
Abstract: OK 8; FIX 0.

Every new/changed sentence, all table cells and all captions are included; unchanged/moved sentences also appear to make the content comparison reviewable. Exact receipt-column identities were additionally asserted for the main emulator table, appendix response-model table and cross-model decision table. All moved reference targets are defined once and all figure paths exist. Independent covariance algebra confirms the inequality in Section 4.2.

## FIX rows verbatim

- V8_122_02 (line 122): The seven-pattern curve is post hoc, but the caption labels only the pre-registered right-hand reading. Proposed replacement: Left: confident shares on the confirmation panel; the seven-pattern comparison is post hoc. Forecast sign: solid circles; all eight intervention signs: dashed squares; seven patterns: dash-dot triangles; observation-confident signs: dotted diamonds.
- V8_224_05 (line 224): The rounded maximum is smaller than the actual maximum; a strict upper bound cannot be stated at that rounded value. Proposed replacement: The largest share of draw-level intervention-sign answers that change is 0.0011 (rounded), at 6 LT.
- V8_288_04 (line 288): Mean divided by standard deviation does not determine sign probability for a general posterior; the next sentence correctly invokes the full tangent distribution. Proposed replacement: It does not establish how much posterior probability lies on either side of zero; the mean relative to its own spread is a descriptive summary, not a determination of sign confidence.
- V8_366_07 (line 366): The direct cost-head emulator was evaluated only at one lead and has no paired endpoint in the Stage 9 receipt; the universal statement includes an untested model. Proposed replacement: Every rollout emulator with a paired endpoint reproduces the paired ordering; the direct cost head has no paired endpoint in this evaluation.
- V8_513_01 (line 513): Moving this material into the appendix leaves the training/result paragraph without a local post hoc label; the later table and figure captions do not label the paragraph itself. Proposed replacement: Post hoc on the confirmation panel, CNN-F-resp adds to CNN-F's loss a paired loss on the difference between rollouts from one start under two actions, weighted so that the two losses start equal.
- V8_534_02 (line 534): The requested F13 re-render uses dash-dot triangles for CNN-F and long-dash crosses for CNN-F-resp, unlike this caption. Proposed replacement: Posterior (solid, circles), CNN-20k (dashed, squares), CNN-F (dash-dot, triangles), CNN-F-resp (long-dash, crosses), and the direct cost head (spaced dotted line, plus markers; not interpretable, see text). The thin dotted diagonal has no markers and marks perfect reliability.

## F13 presentation hashes

| Figure file | Before SHA-256 | After SHA-256 |
|---|---|---|
| F13_main_paper.pdf | 13db03c3fcd9adb1e094629ac3039e6f768c239a359434811903f8a05abb57c8 | 6d7f7958816f1d5535ec7aa96046b4b66ec24341d9cc55ecd50bb908877e5963 |
| F13_main_paper.png | 96d8fb0e9d3fa49c36fe93a70f0041efb4634ad1892ca529fc3b76f74597c4f8 | 45974ac4fed4a58a5a5599369ede43ee5a59a6d59c7370a3e59b7e218374e5bb |

| F13_reliability_paper.pdf | 353f2f1b82c0a376f14a77f03fc3f40a67b046e8b51190abda3fe7847733e0af | 48c7f1aa38c8bc8c091a53cacf0dd3ba48be7c94ee5a1385d24142c4216d9ac8 |
| F13_reliability_paper.png | fa7e3773ae0d89625a1b3d11f2e13b506606ac8c352924ad6ebab723a5669155 | 9210c31fc3450d22a5b10e1744d3c69e4112139a46de41ac9ce9d688c2a87a63 |

Both PDFs: measured MediaBox 720 × 288 points. Greyscale; posterior solid/circles, CNN-20k dashed/squares, CNN-F dash-dot/triangles, CNN-F-resp long-dash/crosses, cost head spaced dotted/plus. Reliability diagonal thin dotted without a marker. Receipt series reused without recomputation; PNG visually inspected.

## R-other resolutions

Citation descriptions remain outside receipt scope and author-verified, as instructed. Caption/appendix post hoc labels and the universal-emulator statement take the narrower supported scope in the proposed wording. No new experiment, inference or route is licensed. Training continues independently; no Spark access was needed.
