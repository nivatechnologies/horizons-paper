# Stage 11 status

Post hoc; licenses no frozen route. Sulaco CPU only. Spark and Stage 10 working files, data, checkpoints, receipts and reports were not modified. No truth was opened. Paper sources remain verbatim; no build.

## Payload verification

- /tmp/aspen_stage11_payload.tgz: 32e5d9c0c3621c0a40f013d113cdd3ec1468d33d9224447190342ab535ad6390 — MATCH
- paper/main.tex: 7f31270b365b6b6559760b4c1c6b6d4bc8db423eb4f221132d75903ae920009c — MATCH
- paper/ABSTRACT_v6.txt: e682ff6a5d0d82e50a1e445f832f39164b3be11d6d7f44df5bc6d50461d2ef1f — MATCH
- paper/refs.bib: ab16d40f680e689faa0fc3346c0f6109f184b87d9176e8ff00f27ee403b89c6f — MATCH

## Number checks

Registry regeneration PASS. Keys before: 16583; after: 17042. Every prior key value is unchanged.
De-TeXed paper raw text checker: exit 1. Every unmatched token follows:
- TeX line 359: 13.5
The percent bracket token corresponds to receipts/acd_stage9.json $.C.CNN-F-resp.confidence_readings[0].error_upper = 0.135. R-other: preserve the supplied text and record the representation exception; do not invent an unscaled registry value.
Abstract text checker PASS; no unmatched tokens. Thousands separators and scientific exponents are normalized by de-TeX.

### Structural inventory

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

Bibliography fields are document metadata, not empirical results; refs.bib unchanged.

## Derived quantities

| Quantity | Full precision | Source | Derivation |
|---|---|---|---|
| CNN-F_GPU_HOURS | 1.6623143853188869 | receipts/acd_stage9.json:$.F.CNN-F.charged_gpu_seconds | charged seconds / seconds per hour; discarded duration already included |
| CNN-F-resp_GPU_HOURS | 4.109466532578049 | receipts/acd_stage9.json:$.F.CNN-F-resp.charged_gpu_seconds | charged seconds / seconds per hour; discarded duration already included |
| CNN20K_TRAIN_TRAJECTORIES | 2048 | receipts/acd_stage9.json:$.CNN_provenance.CNN20k.training_distribution | parse retained training trajectory count; generating source recorded in provenance.source |
| CNNF_TRAIN_TRAJECTORIES | 4096 | acd_stage9_training_data.py:line 10, run trajectory loop | literal_eval trajectory counts in generating code; training and validation use distinct roles |
| CNNF_VAL_TRAJECTORIES | 512 | acd_stage9_training_data.py:line 10, run trajectory loop | literal_eval trajectory counts in generating code; training and validation use distinct roles |
| E_LARGEST_HARM_OVER_MEAN_IMPROVEMENT_2LT | 5.5055263063868844 | receipts/acd_stage9.json:$.D[0].max_harm / $.D[0].mean_improvement | largest realized harm / mean realized improvement, E at 2 LT |
| POSTERIOR_S_WRONG_SHARE_0_TO_3LT | 0.0026700393479482856 | receipts/acd_stage2.json:$.all_confident_calibration, S rows at leads 0 through 3 | sum wrong / sum confident answers; pooled descriptive |
| POSTERIOR_S_ANSWERS_PER_ERROR_0_TO_3LT | 374.5263157894737 | receipts/acd_stage2.json:$.all_confident_calibration, S rows at leads 0 through 3 | sum confident answers / sum wrong |

## Climatological tangent table

Saved frozen null states; float64; exact frozen windows and Stage 9 forward-mode RK4 tangent. No realized truth. Pattern zero is uniform decrease. These finite-ensemble estimates are descriptive; they do not prove invariant-measure shift symmetry.

| Pattern | Lead LT | Mean G | Standard error | Mean / SD | P(G < 0) |
|---|---|---|---|---|---|
| 0 | 0.0 | -0.6633717846528909 | 0.000997025575638599 | -10.396106567840526 | 1.0 |
| 0 | 1.0 | -1.4826328052721904 | 0.0034533264877144457 | -6.708354296876888 | 1.0 |
| 0 | 1.5 | -1.582189709412925 | 0.0064364722315500495 | -3.8408794942665976 | 0.996826171875 |
| 0 | 2.0 | -1.645146726330069 | 0.01222810353011291 | -2.1021589762963 | 0.980224609375 |
| 0 | 2.5 | -1.7150689195456694 | 0.02651471460281966 | -1.0106822671608655 | 0.945068359375 |
| 0 | 3.0 | -1.7660307075907464 | 0.05183100995649102 | -0.5323884259494285 | 0.87451171875 |
| 0 | 4.0 | -1.770077905816953 | 0.18385889911974024 | -0.15042767802268653 | 0.708740234375 |
| 0 | 6.0 | -0.7584103164404352 | 2.897934340932164 | -0.004089175184890497 | 0.5283203125 |
| 1 | 0.0 | 0.0006097659220730996 | 0.0009997302377607279 | 0.009530163410614457 | 0.49658203125 |
| 1 | 1.0 | 0.005679504835826486 | 0.003625770975195237 | 0.024475418791450373 | 0.494140625 |
| 1 | 1.5 | 0.009774777317205935 | 0.007102713032659151 | 0.021503177008428645 | 0.497314453125 |
| 1 | 2.0 | 0.0071124163411853715 | 0.014351824367943343 | 0.007743371329100712 | 0.4970703125 |
| 1 | 2.5 | 0.00950443784561405 | 0.03364348259971183 | 0.004414134027224386 | 0.500244140625 |
| 1 | 3.0 | 0.02896005533859702 | 0.06451435615461203 | 0.007013956143050339 | 0.503173828125 |
| 1 | 4.0 | 0.18142480810208553 | 0.22491834059453425 | 0.012603519211025043 | 0.49560546875 |
| 1 | 6.0 | 4.319260046597528 | 3.453763002634654 | 0.01954055277579955 | 0.499267578125 |
| 2 | 0.0 | -0.0003323771366961015 | 0.0009984590694907588 | -0.005201407768798532 | 0.50830078125 |
| 2 | 1.0 | -0.001267030939071244 | 0.004133563552652387 | -0.004789416727434806 | 0.502685546875 |
| 2 | 1.5 | -0.00951296518423093 | 0.008501839882576039 | -0.017483283978122943 | 0.50634765625 |
| 2 | 2.0 | -0.025601992892848962 | 0.01692068231917622 | -0.023641548928402815 | 0.50732421875 |
| 2 | 2.5 | -0.025030596854383552 | 0.038175071916140196 | -0.010244985961228456 | 0.499267578125 |
| 2 | 3.0 | -0.04383129445220134 | 0.08074218117720608 | -0.008482108927829985 | 0.497314453125 |
| 2 | 4.0 | -0.1634673015521816 | 0.28174812947922045 | -0.009065460670400701 | 0.50048828125 |
| 2 | 6.0 | -0.8508807670865011 | 4.399498381705448 | -0.003021938146633167 | 0.509521484375 |
| 3 | 0.0 | 3.9230551581805094e-06 | 0.0010689654272963965 | 5.7343048971755175e-05 | 0.502197265625 |
| 3 | 1.0 | -5.0443018235243886e-05 | 0.005602971013404793 | -0.0001406703975515897 | 0.494873046875 |
| 3 | 1.5 | -0.006257926297174047 | 0.012071047423547407 | -0.008100382258676367 | 0.507568359375 |
| 3 | 2.0 | -0.010096893237820663 | 0.02556746443723302 | -0.006170496774455337 | 0.50732421875 |
| 3 | 2.5 | 0.027308012824986624 | 0.05733758375645312 | 0.007441675641631724 | 0.500732421875 |
| 3 | 3.0 | 0.0692454117202532 | 0.11454855186013027 | 0.009445423277372245 | 0.49658203125 |
| 3 | 4.0 | -0.04838568140562559 | 0.42449915343883815 | -0.001780984168845529 | 0.499267578125 |
| 3 | 6.0 | 3.270689574563782 | 6.674433481953635 | 0.007656758396159876 | 0.505859375 |
| 4 | 0.0 | -0.00031097135256212094 | 0.0016558811744513465 | -0.0029343454462504403 | 0.5048828125 |
| 4 | 1.0 | -0.004330614389755138 | 0.0062115729474327645 | -0.010893512869053601 | 0.500244140625 |
| 4 | 1.5 | -0.0007596656994723547 | 0.014106995626257569 | -0.0008414106638100988 | 0.50830078125 |
| 4 | 2.0 | 0.016336769871791154 | 0.029848316986289907 | 0.008551973947609346 | 0.500244140625 |
| 4 | 2.5 | 0.015391573101671854 | 0.06444378691827837 | 0.0037318311231243134 | 0.491455078125 |
| 4 | 3.0 | 0.00838036526634734 | 0.12996124132376857 | 0.0010075558370550054 | 0.487060546875 |
| 4 | 4.0 | 0.01619179832527938 | 0.5343677810900318 | 0.0004734507913564959 | 0.500244140625 |
| 4 | 6.0 | 4.7647024424829825 | 8.076585137462168 | 0.009217815994841339 | 0.492919921875 |
| 5 | 0.0 | 0.001921848668324499 | 0.0015641029890089248 | 0.019198790395252515 | 0.4892578125 |
| 5 | 1.0 | -0.007471715194556977 | 0.005048073709250251 | -0.023126752230464565 | 0.50927734375 |
| 5 | 1.5 | -0.017240492315610846 | 0.012100134895254064 | -0.022262784238634994 | 0.5068359375 |
| 5 | 2.0 | -0.021263373138935115 | 0.02700217331010391 | -0.012304202386981223 | 0.4873046875 |
| 5 | 2.5 | -0.007483632258839287 | 0.06093280422118875 | -0.001919027944617426 | 0.495849609375 |
| 5 | 3.0 | 0.0671996920924792 | 0.12763157665112934 | 0.008226766576856328 | 0.49853515625 |
| 5 | 4.0 | 0.7812473998075246 | 0.5099635627069212 | 0.023936985923458994 | 0.489501953125 |
| 5 | 6.0 | -9.802838451955036 | 6.860634329905535 | -0.022325829281431248 | 0.49609375 |
| 6 | 0.0 | 0.0005225766997827117 | 0.0012432824844327629 | 0.006567502587982007 | 0.50048828125 |
| 6 | 1.0 | 0.0032261887959129268 | 0.0031248117978874826 | 0.016131915518950112 | 0.4892578125 |
| 6 | 1.5 | 0.009160921987781288 | 0.005980472386388746 | 0.023934464840078638 | 0.482666015625 |
| 6 | 2.0 | 0.02448611387502329 | 0.013749528065895512 | 0.027826084463672122 | 0.48291015625 |
| 6 | 2.5 | 0.07591669909309176 | 0.03466944859932526 | 0.03421451656293849 | 0.485595703125 |
| 6 | 3.0 | 0.13047553800244632 | 0.0645846885057341 | 0.03156600006063699 | 0.506103515625 |
| 6 | 4.0 | 0.15016335980609719 | 0.2266767716968682 | 0.010350873093022284 | 0.491943359375 |
| 6 | 6.0 | 4.937299404348558 | 3.3102224897467796 | 0.023305171610639247 | 0.49462890625 |
| 7 | 0.0 | -0.00234989941369315 | 0.0013927828787439983 | -0.02636245670399593 | 0.45361328125 |
| 7 | 1.0 | 0.006945979762058505 | 0.004934239893301521 | 0.02199547166920286 | 0.474365234375 |
| 7 | 1.5 | 0.020546284432721166 | 0.010477197431870209 | 0.03064137106786986 | 0.47607421875 |
| 7 | 2.0 | 0.024971293492345125 | 0.022860515301800985 | 0.017067701916026096 | 0.48681640625 |
| 7 | 2.5 | -0.01421361008415508 | 0.056879208621025586 | -0.003904549007435165 | 0.49755859375 |
| 7 | 3.0 | -0.056904899484968005 | 0.10417847838670304 | -0.008534767144056422 | 0.501220703125 |
| 7 | 4.0 | 0.14415529412024453 | 0.46035018452651966 | 0.0048928544971595725 | 0.503662109375 |
| 7 | 6.0 | 6.6528710005191805 | 4.9067821652739285 | 0.02118518937294396 | 0.5078125 |

## Audit outcomes

paper: 433 OK; 12 FIX.

V6_034_04 (line 34): External-paper content is not present in retained receipts; bibliography metadata identifies the reference but does not independently substantiate this description.
Proposed replacement: Remove the detailed external-study description pending verification against the cited source text; retain the statement of the present study’s question.

V6_034_05 (line 34): External-paper content is not present in retained receipts; bibliography metadata identifies the reference but does not independently substantiate this description.
Proposed replacement: Remove the detailed external-study description pending verification against the cited source text; retain the statement of the present study’s question.

V6_038_01 (line 38): A superlative ranking of the literature is not established by retained experiment receipts.
Proposed replacement: A related prior result is that of the cited Lorenz-63 and Rössler study.

V6_038_04 (line 38): The negative assertion about both external papers cannot be verified from bibliography metadata in this receipt-only audit.
Proposed replacement: Here we score effect-prediction confidence against realized outcomes; retain any contrast with those papers only with a cited source passage.

V6_098_02 (line 98): Chain starts are valid randomized observation-perturbed fits, not the multi-start likelihood minima: acd_fits.py returns starts=theta[lowest].
Proposed replacement: Each instance runs four chains initialized from valid fits to independently perturbed observation windows; separate multi-start likelihood fits supply the reference minimum.

V6_260_09 (line 260): Equivariance alone does not imply that every invariant measure is shift-invariant. The symmetric start law and burn-in preserve shift symmetry in distribution, but do not prove stationarity. A zero tangent mean alone does not imply nearly equiprobable signs.
Proposed replacement: Under a shift-invariant climatological law, equivariance and linearity in the pattern imply zero mean tangent response for zero-mean patterns. The finite-ensemble tangent check is descriptive; the near-half sign probabilities are a separate empirical finding.

V6_341_04 (line 341): Receipts contain a discrete threshold/coverage curve, not a statement at every possible coverage or outside the shared plotted range.
Proposed replacement: Its plotted pooled-error curve lies above the posterior curve over their shared displayed coverage range.

V6_341_05 (line 341): Similar point estimates and overlapping intervals do not establish equivalence on every reading; no equivalence test was specified.
Proposed replacement: CNN-F has similar forecast skill and confident share, a small case-averaged confident error, and the same direction of paired ordering; this comparison does not establish statistical equivalence.

V6_343_06 (line 343): L8 requires both an R0 statistic below its point cutoff and a one-sided betting upper bound below its separate bound cutoff, and refers to the frozen observation-confidence statistic.
Proposed replacement: The frozen protocol permits the word overconfident only when its R0 statistic is below the point cutoff and its one-sided betting upper bound is below the bound cutoff; neither CNN-20k construction meets that rule.

V6_434_06 (line 434): External-paper content is not present in retained receipts; bibliography metadata identifies the reference but does not independently substantiate this description.
Proposed replacement: Remove the detailed external-study description pending verification against the cited source text; retain the statement of the present study’s question.

V6_434_07 (line 434): External-paper content is not present in retained receipts; bibliography metadata identifies the reference but does not independently substantiate this description.
Proposed replacement: Remove the detailed external-study description pending verification against the cited source text; retain the statement of the present study’s question.

V6_447_03 (line 447): The frozen same-lead route compares observation-confident S with confident Fc, while the all-confident S comparison is post hoc.
Proposed replacement: The pre-registered observation-confident S share is lower at the two pre-specified leads; the all-confident comparison and the wider descriptive lead range are post hoc.
abstract: 7 OK; 1 FIX.

AV6_07 (line 1): The emulator percentages are case-averaged confident-error rates, not the pooled fraction of answers implied by “errs on”. Those denominators differ; label the aggregation. B1 descriptive association; same case panel, block and amplitude-specific endpoints; no new frozen-route license.
Proposed replacement: In the emulator clause replace “errs on” with “has a case-averaged error rate of”, and state that the comparison is among confident intervention-sign answers.

All FIX rows remain open; paper and abstract were not edited. R-other: external-source descriptions without retained source text receive FIX rather than a verified verdict; equivalence and unconditional symmetry are not licensed.

## Figure page sizes

| Figure | PDF points | PNG |
|---|---|---|
| figures/F11_tangent_paper.pdf | 360.0 × 288.0 | figures/F11_tangent_paper.png |
| figures/F12_variance_paper.pdf | 720.0 × 288.0 | figures/F12_variance_paper.png |
| figures/F13_reliability_paper.pdf | 720.0 × 288.0 | figures/F13_reliability_paper.png |
| figures/F14_amplitude_paper.pdf | 720.0 × 288.0 | figures/F14_amplitude_paper.png |

Publication uses the canonical paper branch with a fast-forward push. Only the explicit Stage 11 paths are staged.
