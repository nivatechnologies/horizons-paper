# Stage 18 learned controls and response derivatives

## Part A

Every arm uses the original confirmation instances and retained draws. These readings are post hoc and license no frozen route. Outcome arrays are opened only by the Sulaco scorer. Training-run variation remains distinct from case-level uncertainty.

Own forcing, posterior-mean forcing and fixed climatological forcing are information diagnostics. The seeded within-case forcing permutation deliberately breaks the joint posterior; it is reported as an intervention on model input, without a posterior interpretation.

| Arm | LT | State RMSE/sigma | State ACC | Confident S share | Pooled confident S error | Case confident S error | Case error bounds |
|---|---:|---:|---:|---:|---:|---:|---:|
| CNN-F-ownF | 2 | 0.122231 | 0.982641 | 0.72125 | 0.00866551 | 0.00757358 | [0, 0.025] |
| CNN-F-ownF | 3 | 0.269676 | 0.927257 | 0.4075 | 0.00766871 | 0.011134 | [0, 0.04] |
| CNN-F-meanF | 2 | 0.122206 | 0.982628 | 0.720625 | 0.00780572 | 0.00685571 | [0, 0.025] |
| CNN-F-meanF | 3 | 0.269514 | 0.927218 | 0.40875 | 0.00917431 | 0.0164354 | [0, 0.046] |
| CNN-F-constantF | 2 | 0.120761 | 0.982873 | 0.72 | 0.0078125 | 0.00694544 | [0, 0.025] |
| CNN-F-constantF | 3 | 0.267716 | 0.928003 | 0.413125 | 0.00907716 | 0.0124832 | [0, 0.041] |
| CNN-F-permutedF | 2 | 0.12229 | 0.982626 | 0.71875 | 0.00782609 | 0.00685571 | [0, 0.025] |
| CNN-F-permutedF | 3 | 0.26972 | 0.927227 | 0.4025 | 0.00776398 | 0.010845 | [0, 0.039] |

Each direction of the case-error bounds uses the v2.3 one-sided 95% instance betting construction; pooled error is descriptive.

| Arm | LT | Quantity | Equal-case RMSE | Equal-case bias |
|---|---:|---|---:|---:|
| CNN-F-ownF | 2 | J8 | 0.0160508 | -0.00231997 |
| CNN-F-ownF | 2 | Jk | 0.0219492 | -0.00425283 |
| CNN-F-ownF | 2 | Dk | 0.0177908 | -0.00193286 |
| CNN-F-ownF | 3 | J8 | 0.0594487 | -0.00163846 |
| CNN-F-ownF | 3 | Jk | 0.0733581 | -0.00457246 |
| CNN-F-ownF | 3 | Dk | 0.0816559 | -0.002934 |
| CNN-F-meanF | 2 | J8 | 0.0548869 | -0.00243568 |
| CNN-F-meanF | 2 | Jk | 0.0571976 | -0.00423526 |
| CNN-F-meanF | 2 | Dk | 0.021749 | -0.00179958 |
| CNN-F-meanF | 3 | J8 | 0.10226 | -0.00197167 |
| CNN-F-meanF | 3 | Jk | 0.111841 | -0.00464375 |
| CNN-F-meanF | 3 | Dk | 0.106228 | -0.00267208 |
| CNN-F-constantF | 2 | J8 | 0.0723139 | -0.00304145 |
| CNN-F-constantF | 2 | Jk | 0.0741555 | -0.00499027 |
| CNN-F-constantF | 2 | Dk | 0.0238489 | -0.00194882 |
| CNN-F-constantF | 3 | J8 | 0.121692 | -0.00379306 |
| CNN-F-constantF | 3 | Jk | 0.130543 | -0.00643575 |
| CNN-F-constantF | 3 | Dk | 0.116643 | -0.00264269 |
| CNN-F-permutedF | 2 | J8 | 0.0746684 | -0.00241137 |
| CNN-F-permutedF | 2 | Jk | 0.0768586 | -0.00426986 |
| CNN-F-permutedF | 2 | Dk | 0.0247663 | -0.00185849 |
| CNN-F-permutedF | 3 | J8 | 0.127207 | -0.00164203 |
| CNN-F-permutedF | 3 | Jk | 0.13617 | -0.00467125 |
| CNN-F-permutedF | 3 | Dk | 0.12173 | -0.00302922 |

Errors compare each emulator draw with the same draw’s physics forecast.

| Arm | LT | Policy | Regret | Capture | Actions taken | Harms | Conditional harm CP95 | Uniform decrease in every instance |
|---|---:|---|---:|---:|---:|---:|---:|---|
| CNN-F-ownF | 2 | E | 0.00894941 | 0.971474 | 200 | 1 | [0.000256434, 0.0234985] | False |
| CNN-F-ownF | 2 | C_delta_0 | 0.0184245 | 0.941272 | 195 | 1 | [0.000263008, 0.0240952] | False |
| CNN-F-ownF | 3 | E | 0.0850397 | 0.842769 | 200 | 11 | [0.0311469, 0.0893961] | False |
| CNN-F-ownF | 3 | C_delta_0 | 0.182672 | 0.662256 | 142 | 1 | [0.000361155, 0.0329703] | False |
| CNN-F-meanF | 2 | E | 0.00894941 | 0.971474 | 200 | 1 | [0.000256434, 0.0234985] | False |
| CNN-F-meanF | 2 | C_delta_0 | 0.0184245 | 0.941272 | 195 | 1 | [0.000263008, 0.0240952] | False |
| CNN-F-meanF | 3 | E | 0.0810157 | 0.850209 | 200 | 11 | [0.0311469, 0.0893961] | False |
| CNN-F-meanF | 3 | C_delta_0 | 0.178114 | 0.670684 | 141 | 1 | [0.000363716, 0.033201] | False |
| CNN-F-constantF | 2 | E | 0.00878264 | 0.972005 | 200 | 1 | [0.000256434, 0.0234985] | False |
| CNN-F-constantF | 2 | C_delta_0 | 0.0182762 | 0.941744 | 196 | 1 | [0.000261666, 0.0239735] | False |
| CNN-F-constantF | 3 | E | 0.0838205 | 0.845023 | 198 | 11 | [0.0314646, 0.0902824] | False |
| CNN-F-constantF | 3 | C_delta_0 | 0.187504 | 0.653321 | 140 | 1 | [0.000366314, 0.033435] | False |
| CNN-F-permutedF | 2 | E | 0.00894941 | 0.971474 | 200 | 1 | [0.000256434, 0.0234985] | False |
| CNN-F-permutedF | 2 | C_delta_0 | 0.0184245 | 0.941272 | 195 | 1 | [0.000263008, 0.0240952] | False |
| CNN-F-permutedF | 3 | E | 0.0810157 | 0.850209 | 200 | 11 | [0.0311469, 0.0893961] | False |
| CNN-F-permutedF | 3 | C_delta_0 | 0.182724 | 0.662159 | 139 | 1 | [0.000368948, 0.0336723] | False |

Conditional harm bounds are exact one-sided 95% Clopper–Pearson bounds. Action histograms and the full calibration, coverage, paired-endpoint and confidence readings are in the receipt.

CNN-F-ownF reproduction: maximum absolute predicted-cost difference 0.137897; changed confidence classifications 0.

## Part B

Every arm uses the original confirmation instances and retained draws. These readings are post hoc and license no frozen route. Outcome arrays are opened only by the Sulaco scorer. Training-run variation remains distinct from case-level uncertainty.

| Arm | LT | State RMSE/sigma | State ACC | Confident S share | Pooled confident S error | Case confident S error | Case error bounds |
|---|---:|---:|---:|---:|---:|---:|---:|
| CNN-F-E0-fixed-seed1 | 2 | 0.12322 | 0.982375 | 0.723125 | 0.00864304 | 0.00757358 | [0, 0.025] |
| CNN-F-E0-fixed-seed1 | 3 | 0.270995 | 0.92658 | 0.410625 | 0.00913242 | 0.0166261 | [0, 0.046] |
| CNN-F-E1-fixed-seed1 | 2 | 0.123143 | 0.982389 | 0.724375 | 0.0163934 | 0.0139971 | [0, 0.032] |
| CNN-F-E1-fixed-seed1 | 3 | 0.271039 | 0.926573 | 0.40125 | 0.0140187 | 0.023098 | [0, 0.058] |
| CNN-F-E1-rolling-seed1 | 2 | 0.123504 | 0.982225 | 0.731875 | 0.0273271 | 0.025256 | [0.006, 0.041] |
| CNN-F-E1-rolling-seed1 | 3 | 0.27091 | 0.926404 | 0.44375 | 0.0422535 | 0.0792607 | [0.038, 0.088] |
| CNN-F-E0-fixed-seed2 | 2 | 0.12331 | 0.982475 | 0.719375 | 0.0086881 | 0.00757358 | [0, 0.025] |
| CNN-F-E0-fixed-seed2 | 3 | 0.271373 | 0.926401 | 0.405 | 0.00771605 | 0.010845 | [0, 0.039] |
| CNN-F-E1-fixed-seed2 | 2 | 0.123547 | 0.982282 | 0.728125 | 0.0197425 | 0.0179654 | [0, 0.036] |
| CNN-F-E1-fixed-seed2 | 3 | 0.270993 | 0.926433 | 0.4 | 0.0125 | 0.016722 | [0, 0.047] |
| CNN-F-E1-rolling-seed2 | 2 | 0.123373 | 0.982333 | 0.729375 | 0.0265638 | 0.0250476 | [0.006, 0.041] |
| CNN-F-E1-rolling-seed2 | 3 | 0.270366 | 0.926857 | 0.435 | 0.0416667 | 0.0735072 | [0.035, 0.088] |
| CNN-F-E0-fixed-seed3 | 2 | 0.123827 | 0.982215 | 0.723125 | 0.00864304 | 0.00749581 | [0, 0.025] |
| CNN-F-E0-fixed-seed3 | 3 | 0.271903 | 0.925966 | 0.4075 | 0.00920245 | 0.0164354 | [0, 0.046] |
| CNN-F-E1-fixed-seed3 | 2 | 0.123201 | 0.982382 | 0.7225 | 0.016436 | 0.0151696 | [0, 0.032] |
| CNN-F-E1-fixed-seed3 | 3 | 0.270727 | 0.926549 | 0.405625 | 0.0123267 | 0.0164878 | [0, 0.047] |
| CNN-F-E1-rolling-seed3 | 2 | 0.122758 | 0.982448 | 0.735 | 0.0280612 | 0.0261012 | [0.007, 0.042] |
| CNN-F-E1-rolling-seed3 | 3 | 0.269437 | 0.927181 | 0.436875 | 0.0414878 | 0.0746662 | [0.036, 0.09] |
| CNN-F-E0-fixed-seed4 | 2 | 0.12313 | 0.982382 | 0.720625 | 0.00867303 | 0.00757358 | [0, 0.025] |
| CNN-F-E0-fixed-seed4 | 3 | 0.271134 | 0.926321 | 0.4075 | 0.00766871 | 0.0107827 | [0, 0.039] |
| CNN-F-E1-fixed-seed4 | 2 | 0.122061 | 0.982623 | 0.72625 | 0.0180723 | 0.0156085 | [0, 0.032] |
| CNN-F-E1-fixed-seed4 | 3 | 0.270054 | 0.926919 | 0.404375 | 0.0108192 | 0.0147841 | [0, 0.045] |
| CNN-F-E1-rolling-seed4 | 2 | 0.122846 | 0.982378 | 0.7325 | 0.0255973 | 0.0240893 | [0.005, 0.039] |
| CNN-F-E1-rolling-seed4 | 3 | 0.270227 | 0.92657 | 0.436875 | 0.0400572 | 0.0719862 | [0.035, 0.088] |
| CNN-F-E0-fixed-seed5 | 2 | 0.123594 | 0.982371 | 0.72 | 0.00954861 | 0.00829146 | [0, 0.026] |
| CNN-F-E0-fixed-seed5 | 3 | 0.271403 | 0.926429 | 0.41125 | 0.00911854 | 0.0120011 | [0, 0.041] |
| CNN-F-E1-fixed-seed5 | 2 | 0.123069 | 0.982382 | 0.725 | 0.0181034 | 0.0155604 | [0, 0.033] |
| CNN-F-E1-fixed-seed5 | 3 | 0.270816 | 0.926543 | 0.40125 | 0.0124611 | 0.0157635 | [0, 0.047] |
| CNN-F-E1-rolling-seed5 | 2 | 0.123121 | 0.982344 | 0.734375 | 0.026383 | 0.0243036 | [0.006, 0.04] |
| CNN-F-E1-rolling-seed5 | 3 | 0.270332 | 0.926835 | 0.440625 | 0.0397163 | 0.0727318 | [0.035, 0.085] |

Each direction of the case-error bounds uses the v2.3 one-sided 95% instance betting construction; pooled error is descriptive.

| Arm | LT | Quantity | Equal-case RMSE | Equal-case bias |
|---|---:|---|---:|---:|
| CNN-F-E0-fixed-seed1 | 2 | J8 | 0.0277807 | 0.000291805 |
| CNN-F-E0-fixed-seed1 | 2 | Jk | 0.0321473 | -0.00142887 |
| CNN-F-E0-fixed-seed1 | 2 | Dk | 0.0186791 | -0.00172067 |
| CNN-F-E0-fixed-seed1 | 3 | J8 | 0.0686862 | 0.00278474 |
| CNN-F-E0-fixed-seed1 | 3 | Jk | 0.0818995 | -0.00048484 |
| CNN-F-E0-fixed-seed1 | 3 | Dk | 0.0868269 | -0.00326958 |
| CNN-F-E1-fixed-seed1 | 2 | J8 | 0.0254029 | -0.001272 |
| CNN-F-E1-fixed-seed1 | 2 | Jk | 0.0842374 | 0.0246242 |
| CNN-F-E1-fixed-seed1 | 2 | Dk | 0.0806112 | 0.0258962 |
| CNN-F-E1-fixed-seed1 | 3 | J8 | 0.0664676 | -0.000388499 |
| CNN-F-E1-fixed-seed1 | 3 | Jk | 0.139917 | 0.0258448 |
| CNN-F-E1-fixed-seed1 | 3 | Dk | 0.145169 | 0.0262333 |
| CNN-F-E1-rolling-seed1 | 2 | J8 | 0.0385267 | 0.00152294 |
| CNN-F-E1-rolling-seed1 | 2 | Jk | 0.0543001 | 0.00625017 |
| CNN-F-E1-rolling-seed1 | 2 | Dk | 0.0365514 | 0.00472723 |
| CNN-F-E1-rolling-seed1 | 3 | J8 | 0.0812859 | 0.00410547 |
| CNN-F-E1-rolling-seed1 | 3 | Jk | 0.128473 | -0.00456303 |
| CNN-F-E1-rolling-seed1 | 3 | Dk | 0.126032 | -0.00866851 |
| CNN-F-E0-fixed-seed2 | 2 | J8 | 0.0252288 | -0.00271941 |
| CNN-F-E0-fixed-seed2 | 2 | Jk | 0.0296445 | -0.00484908 |
| CNN-F-E0-fixed-seed2 | 2 | Dk | 0.0182606 | -0.00212967 |
| CNN-F-E0-fixed-seed2 | 3 | J8 | 0.0674625 | -0.000540002 |
| CNN-F-E0-fixed-seed2 | 3 | Jk | 0.0801862 | -0.00390357 |
| CNN-F-E0-fixed-seed2 | 3 | Dk | 0.0849673 | -0.00336356 |
| CNN-F-E1-fixed-seed2 | 2 | J8 | 0.0256006 | -0.00449652 |
| CNN-F-E1-fixed-seed2 | 2 | Jk | 0.0827892 | 0.0212798 |
| CNN-F-E1-fixed-seed2 | 2 | Dk | 0.080383 | 0.0257763 |
| CNN-F-E1-fixed-seed2 | 3 | J8 | 0.069828 | -0.00265878 |
| CNN-F-E1-fixed-seed2 | 3 | Jk | 0.140059 | 0.0230624 |
| CNN-F-E1-fixed-seed2 | 3 | Dk | 0.14795 | 0.0257212 |
| CNN-F-E1-rolling-seed2 | 2 | J8 | 0.0365363 | -0.00806674 |
| CNN-F-E1-rolling-seed2 | 2 | Jk | 0.0519755 | -0.00271485 |
| CNN-F-E1-rolling-seed2 | 2 | Dk | 0.0365593 | 0.00535189 |
| CNN-F-E1-rolling-seed2 | 3 | J8 | 0.0795933 | -0.00701763 |
| CNN-F-E1-rolling-seed2 | 3 | Jk | 0.128062 | -0.0148169 |
| CNN-F-E1-rolling-seed2 | 3 | Dk | 0.127149 | -0.00779932 |
| CNN-F-E0-fixed-seed3 | 2 | J8 | 0.0258789 | -0.000831465 |
| CNN-F-E0-fixed-seed3 | 2 | Jk | 0.0307106 | -0.00307409 |
| CNN-F-E0-fixed-seed3 | 2 | Dk | 0.0173124 | -0.00224262 |
| CNN-F-E0-fixed-seed3 | 3 | J8 | 0.064527 | 0.000657845 |
| CNN-F-E0-fixed-seed3 | 3 | Jk | 0.0787458 | -0.00345481 |
| CNN-F-E0-fixed-seed3 | 3 | Dk | 0.0827209 | -0.00411266 |
| CNN-F-E1-fixed-seed3 | 2 | J8 | 0.0243195 | -0.00403933 |
| CNN-F-E1-fixed-seed3 | 2 | Jk | 0.0823878 | 0.0216701 |
| CNN-F-E1-fixed-seed3 | 2 | Dk | 0.0803639 | 0.0257094 |
| CNN-F-E1-fixed-seed3 | 3 | J8 | 0.0677639 | -0.00245684 |
| CNN-F-E1-fixed-seed3 | 3 | Jk | 0.139039 | 0.0231373 |
| CNN-F-E1-fixed-seed3 | 3 | Dk | 0.146653 | 0.0255942 |
| CNN-F-E1-rolling-seed3 | 2 | J8 | 0.0382902 | -0.0102751 |
| CNN-F-E1-rolling-seed3 | 2 | Jk | 0.0528582 | -0.00513218 |
| CNN-F-E1-rolling-seed3 | 2 | Dk | 0.0365811 | 0.00514287 |
| CNN-F-E1-rolling-seed3 | 3 | J8 | 0.0810409 | -0.0105982 |
| CNN-F-E1-rolling-seed3 | 3 | Jk | 0.12679 | -0.0189783 |
| CNN-F-E1-rolling-seed3 | 3 | Dk | 0.126211 | -0.00838014 |
| CNN-F-E0-fixed-seed4 | 2 | J8 | 0.0283812 | -0.0016049 |
| CNN-F-E0-fixed-seed4 | 2 | Jk | 0.0324121 | -0.0034581 |
| CNN-F-E0-fixed-seed4 | 2 | Dk | 0.018577 | -0.0018532 |
| CNN-F-E0-fixed-seed4 | 3 | J8 | 0.0697775 | 2.39601e-05 |
| CNN-F-E0-fixed-seed4 | 3 | Jk | 0.0828416 | -0.00356418 |
| CNN-F-E0-fixed-seed4 | 3 | Dk | 0.0870316 | -0.00358814 |
| CNN-F-E1-fixed-seed4 | 2 | J8 | 0.0234292 | -0.00238541 |
| CNN-F-E1-fixed-seed4 | 2 | Jk | 0.0818839 | 0.0234625 |
| CNN-F-E1-fixed-seed4 | 2 | Dk | 0.0793749 | 0.0258479 |
| CNN-F-E1-fixed-seed4 | 3 | J8 | 0.0639965 | -0.000875427 |
| CNN-F-E1-fixed-seed4 | 3 | Jk | 0.137478 | 0.0251695 |
| CNN-F-E1-fixed-seed4 | 3 | Dk | 0.143433 | 0.0260449 |
| CNN-F-E1-rolling-seed4 | 2 | J8 | 0.0363223 | -0.00700421 |
| CNN-F-E1-rolling-seed4 | 2 | Jk | 0.0511106 | -0.00170377 |
| CNN-F-E1-rolling-seed4 | 2 | Dk | 0.0356892 | 0.00530044 |
| CNN-F-E1-rolling-seed4 | 3 | J8 | 0.0800898 | -0.00721742 |
| CNN-F-E1-rolling-seed4 | 3 | Jk | 0.12671 | -0.0150282 |
| CNN-F-E1-rolling-seed4 | 3 | Dk | 0.125947 | -0.00781077 |
| CNN-F-E0-fixed-seed5 | 2 | J8 | 0.0291987 | -0.00201967 |
| CNN-F-E0-fixed-seed5 | 2 | Jk | 0.0329479 | -0.00388591 |
| CNN-F-E0-fixed-seed5 | 2 | Dk | 0.0191144 | -0.00186624 |
| CNN-F-E0-fixed-seed5 | 3 | J8 | 0.0711401 | -0.000650131 |
| CNN-F-E0-fixed-seed5 | 3 | Jk | 0.0836048 | -0.00400012 |
| CNN-F-E0-fixed-seed5 | 3 | Dk | 0.0879002 | -0.00334999 |
| CNN-F-E1-fixed-seed5 | 2 | J8 | 0.0258999 | -0.00254593 |
| CNN-F-E1-fixed-seed5 | 2 | Jk | 0.0834971 | 0.0233927 |
| CNN-F-E1-fixed-seed5 | 2 | Dk | 0.0804713 | 0.0259386 |
| CNN-F-E1-fixed-seed5 | 3 | J8 | 0.0685637 | -0.000115673 |
| CNN-F-E1-fixed-seed5 | 3 | Jk | 0.140824 | 0.0258188 |
| CNN-F-E1-fixed-seed5 | 3 | Dk | 0.147616 | 0.0259345 |
| CNN-F-E1-rolling-seed5 | 2 | J8 | 0.0356668 | -0.00608008 |
| CNN-F-E1-rolling-seed5 | 2 | Jk | 0.0512178 | 5.24621e-05 |
| CNN-F-E1-rolling-seed5 | 2 | Dk | 0.0368865 | 0.00613254 |
| CNN-F-E1-rolling-seed5 | 3 | J8 | 0.0784952 | -0.00475593 |
| CNN-F-E1-rolling-seed5 | 3 | Jk | 0.126078 | -0.0118066 |
| CNN-F-E1-rolling-seed5 | 3 | Dk | 0.127378 | -0.00705065 |

Errors compare each emulator draw with the same draw’s physics forecast.

| Arm | LT | Policy | Regret | Capture | Actions taken | Harms | Conditional harm CP95 | Uniform decrease in every instance |
|---|---:|---|---:|---:|---:|---:|---:|---|
| CNN-F-E0-fixed-seed1 | 2 | E | 0.00888296 | 0.971685 | 200 | 1 | [0.000256434, 0.0234985] | False |
| CNN-F-E0-fixed-seed1 | 2 | C_delta_0 | 0.0213278 | 0.932017 | 194 | 1 | [0.000264363, 0.0242182] | False |
| CNN-F-E0-fixed-seed1 | 3 | E | 0.0837543 | 0.845146 | 200 | 11 | [0.0311469, 0.0893961] | False |
| CNN-F-E0-fixed-seed1 | 3 | C_delta_0 | 0.177819 | 0.671229 | 142 | 1 | [0.000361155, 0.0329703] | False |
| CNN-F-E1-fixed-seed1 | 2 | E | 0.0771545 | 0.754069 | 200 | 1 | [0.000256434, 0.0234985] | False |
| CNN-F-E1-fixed-seed1 | 2 | C_delta_0 | 0.0974921 | 0.689242 | 186 | 1 | [0.000275732, 0.0252494] | False |
| CNN-F-E1-fixed-seed1 | 3 | E | 0.148591 | 0.725269 | 200 | 17 | [0.0548833, 0.124771] | False |
| CNN-F-E1-fixed-seed1 | 3 | C_delta_0 | 0.254706 | 0.529071 | 122 | 2 | [0.00292054, 0.0507038] | False |
| CNN-F-E1-rolling-seed1 | 2 | E | 0.0142466 | 0.954589 | 200 | 2 | [0.00177968, 0.0311426] | False |
| CNN-F-E1-rolling-seed1 | 2 | C_delta_0 | 0.0252401 | 0.919547 | 197 | 2 | [0.00180683, 0.0316117] | False |
| CNN-F-E1-rolling-seed1 | 3 | E | 0.121554 | 0.775258 | 200 | 19 | [0.0631055, 0.136278] | False |
| CNN-F-E1-rolling-seed1 | 3 | C_delta_0 | 0.169734 | 0.686177 | 163 | 9 | [0.0291035, 0.0943715] | False |
| CNN-F-E0-fixed-seed2 | 2 | E | 0.0170608 | 0.945618 | 200 | 1 | [0.000256434, 0.0234985] | False |
| CNN-F-E0-fixed-seed2 | 2 | C_delta_0 | 0.0182187 | 0.941928 | 195 | 0 | [0, 0.0152453] | False |
| CNN-F-E0-fixed-seed2 | 3 | E | 0.0824304 | 0.847593 | 199 | 10 | [0.0275131, 0.0837465] | False |
| CNN-F-E0-fixed-seed2 | 3 | C_delta_0 | 0.178161 | 0.670597 | 141 | 1 | [0.000363716, 0.033201] | False |
| CNN-F-E1-fixed-seed2 | 2 | E | 0.0854282 | 0.727696 | 200 | 2 | [0.00177968, 0.0311426] | False |
| CNN-F-E1-fixed-seed2 | 2 | C_delta_0 | 0.0942364 | 0.69962 | 185 | 0 | [0, 0.0160627] | False |
| CNN-F-E1-fixed-seed2 | 3 | E | 0.14343 | 0.734811 | 200 | 14 | [0.0428126, 0.107268] | False |
| CNN-F-E1-fixed-seed2 | 3 | C_delta_0 | 0.253208 | 0.531841 | 121 | 1 | [0.000423822, 0.0386042] | False |
| CNN-F-E1-rolling-seed2 | 2 | E | 0.0157783 | 0.949707 | 200 | 2 | [0.00177968, 0.0311426] | False |
| CNN-F-E1-rolling-seed2 | 2 | C_delta_0 | 0.0238118 | 0.924099 | 197 | 2 | [0.00180683, 0.0316117] | False |
| CNN-F-E1-rolling-seed2 | 3 | E | 0.118236 | 0.781392 | 200 | 18 | [0.0589787, 0.130539] | False |
| CNN-F-E1-rolling-seed2 | 3 | C_delta_0 | 0.169002 | 0.687529 | 164 | 9 | [0.0289242, 0.093808] | False |
| CNN-F-E0-fixed-seed3 | 2 | E | 0.016894 | 0.94615 | 200 | 1 | [0.000256434, 0.0234985] | False |
| CNN-F-E0-fixed-seed3 | 2 | C_delta_0 | 0.0182187 | 0.941928 | 195 | 0 | [0, 0.0152453] | False |
| CNN-F-E0-fixed-seed3 | 3 | E | 0.0793638 | 0.853263 | 200 | 10 | [0.0273743, 0.0833352] | False |
| CNN-F-E0-fixed-seed3 | 3 | C_delta_0 | 0.180796 | 0.665725 | 142 | 1 | [0.000361155, 0.0329703] | False |
| CNN-F-E1-fixed-seed3 | 2 | E | 0.0864899 | 0.724312 | 200 | 2 | [0.00177968, 0.0311426] | False |
| CNN-F-E1-fixed-seed3 | 2 | C_delta_0 | 0.0982678 | 0.68677 | 184 | 0 | [0, 0.0161493] | False |
| CNN-F-E1-fixed-seed3 | 3 | E | 0.146556 | 0.729032 | 200 | 16 | [0.0508217, 0.118972] | False |
| CNN-F-E1-fixed-seed3 | 3 | C_delta_0 | 0.252573 | 0.533015 | 123 | 2 | [0.00289673, 0.0502988] | False |
| CNN-F-E1-rolling-seed3 | 2 | E | 0.0242778 | 0.922614 | 200 | 2 | [0.00177968, 0.0311426] | False |
| CNN-F-E1-rolling-seed3 | 2 | C_delta_0 | 0.0239942 | 0.923518 | 197 | 1 | [0.000260338, 0.0238529] | False |
| CNN-F-E1-rolling-seed3 | 3 | E | 0.110894 | 0.794968 | 200 | 16 | [0.0508217, 0.118972] | False |
| CNN-F-E1-rolling-seed3 | 3 | C_delta_0 | 0.166462 | 0.692227 | 162 | 7 | [0.0204526, 0.0796256] | False |
| CNN-F-E0-fixed-seed4 | 2 | E | 0.0186622 | 0.940514 | 200 | 2 | [0.00177968, 0.0311426] | False |
| CNN-F-E0-fixed-seed4 | 2 | C_delta_0 | 0.0191648 | 0.938912 | 193 | 0 | [0, 0.0154021] | False |
| CNN-F-E0-fixed-seed4 | 3 | E | 0.0747236 | 0.861843 | 199 | 10 | [0.0275131, 0.0837465] | False |
| CNN-F-E0-fixed-seed4 | 3 | C_delta_0 | 0.173835 | 0.678594 | 144 | 1 | [0.00035614, 0.0325183] | False |
| CNN-F-E1-fixed-seed4 | 2 | E | 0.0841981 | 0.731617 | 200 | 1 | [0.000256434, 0.0234985] | False |
| CNN-F-E1-fixed-seed4 | 2 | C_delta_0 | 0.0970791 | 0.690559 | 184 | 0 | [0, 0.0161493] | False |
| CNN-F-E1-fixed-seed4 | 3 | E | 0.149087 | 0.724351 | 200 | 16 | [0.0508217, 0.118972] | False |
| CNN-F-E1-fixed-seed4 | 3 | C_delta_0 | 0.256536 | 0.525687 | 121 | 1 | [0.000423822, 0.0386042] | False |
| CNN-F-E1-rolling-seed4 | 2 | E | 0.0229338 | 0.926898 | 200 | 2 | [0.00177968, 0.0311426] | False |
| CNN-F-E1-rolling-seed4 | 2 | C_delta_0 | 0.0257585 | 0.917894 | 196 | 1 | [0.000261666, 0.0239735] | False |
| CNN-F-E1-rolling-seed4 | 3 | E | 0.117373 | 0.782989 | 200 | 18 | [0.0589787, 0.130539] | False |
| CNN-F-E1-rolling-seed4 | 3 | C_delta_0 | 0.166003 | 0.693076 | 164 | 9 | [0.0289242, 0.093808] | False |
| CNN-F-E0-fixed-seed5 | 2 | E | 0.0187625 | 0.940194 | 200 | 2 | [0.00177968, 0.0311426] | False |
| CNN-F-E0-fixed-seed5 | 2 | C_delta_0 | 0.0190983 | 0.939124 | 193 | 0 | [0, 0.0154021] | False |
| CNN-F-E0-fixed-seed5 | 3 | E | 0.0858633 | 0.841246 | 200 | 11 | [0.0311469, 0.0893961] | False |
| CNN-F-E0-fixed-seed5 | 3 | C_delta_0 | 0.182672 | 0.662256 | 142 | 1 | [0.000361155, 0.0329703] | False |
| CNN-F-E1-fixed-seed5 | 2 | E | 0.0761388 | 0.757306 | 200 | 1 | [0.000256434, 0.0234985] | False |
| CNN-F-E1-fixed-seed5 | 2 | C_delta_0 | 0.0971887 | 0.69021 | 185 | 1 | [0.000277223, 0.0253845] | False |
| CNN-F-E1-fixed-seed5 | 3 | E | 0.149944 | 0.722768 | 200 | 16 | [0.0508217, 0.118972] | False |
| CNN-F-E1-fixed-seed5 | 3 | C_delta_0 | 0.255669 | 0.52729 | 120 | 1 | [0.000427353, 0.0389208] | False |
| CNN-F-E1-rolling-seed5 | 2 | E | 0.0141932 | 0.954759 | 200 | 2 | [0.00177968, 0.0311426] | False |
| CNN-F-E1-rolling-seed5 | 2 | C_delta_0 | 0.0220785 | 0.929625 | 198 | 2 | [0.00179769, 0.0314538] | False |
| CNN-F-E1-rolling-seed5 | 3 | E | 0.119563 | 0.778939 | 200 | 17 | [0.0548833, 0.124771] | False |
| CNN-F-E1-rolling-seed5 | 3 | C_delta_0 | 0.158649 | 0.706672 | 164 | 7 | [0.0202011, 0.078673] | False |

Conditional harm bounds are exact one-sided 95% Clopper–Pearson bounds. Action histograms and the full calibration, coverage, paired-endpoint and confidence readings are in the receipt.

CNN-F-E0-fixed-seed1 forcing estimate: RMSE 0.0138935, bias 0.00203784, correlation 0.948221. Population: each retained draw/action at the cutoff equally.

CNN-F-E1-fixed-seed1 forcing estimate: RMSE 0.0478514, bias 0.015723, correlation 0.670361. Population: each retained draw/action at the cutoff equally.

CNN-F-E1-rolling-seed1 forcing estimate: RMSE 0.0478514, bias 0.015723, correlation 0.670361. Population: each retained draw/action at the cutoff equally.

CNN-F-E0-fixed-seed2 forcing estimate: RMSE 0.0137792, bias -4.73948e-05, correlation 0.947684. Population: each retained draw/action at the cutoff equally.

CNN-F-E1-fixed-seed2 forcing estimate: RMSE 0.047375, bias 0.0138957, correlation 0.670278. Population: each retained draw/action at the cutoff equally.

CNN-F-E1-rolling-seed2 forcing estimate: RMSE 0.047375, bias 0.0138957, correlation 0.670278. Population: each retained draw/action at the cutoff equally.

CNN-F-E0-fixed-seed3 forcing estimate: RMSE 0.0158813, bias 0.000275998, correlation 0.930206. Population: each retained draw/action at the cutoff equally.

CNN-F-E1-fixed-seed3 forcing estimate: RMSE 0.0471515, bias 0.01452, correlation 0.668434. Population: each retained draw/action at the cutoff equally.

CNN-F-E1-rolling-seed3 forcing estimate: RMSE 0.0471515, bias 0.01452, correlation 0.668434. Population: each retained draw/action at the cutoff equally.

CNN-F-E0-fixed-seed4 forcing estimate: RMSE 0.0162087, bias -2.25361e-05, correlation 0.929286. Population: each retained draw/action at the cutoff equally.

CNN-F-E1-fixed-seed4 forcing estimate: RMSE 0.0467715, bias 0.0146902, correlation 0.676775. Population: each retained draw/action at the cutoff equally.

CNN-F-E1-rolling-seed4 forcing estimate: RMSE 0.0467715, bias 0.0146902, correlation 0.676775. Population: each retained draw/action at the cutoff equally.

CNN-F-E0-fixed-seed5 forcing estimate: RMSE 0.0155931, bias -2.94131e-06, correlation 0.935898. Population: each retained draw/action at the cutoff equally.

CNN-F-E1-fixed-seed5 forcing estimate: RMSE 0.047872, bias 0.0153345, correlation 0.673447. Population: each retained draw/action at the cutoff equally.

CNN-F-E1-rolling-seed5 forcing estimate: RMSE 0.047872, bias 0.0153345, correlation 0.673447. Population: each retained draw/action at the cutoff equally.

Training-run variation (means and ranges only; separate from case-level bounds):

| Arm | LT | Metric | Mean | Range | Runs |
|---|---:|---|---:|---:|---:|
| CNN-F-E0-fixed | 2 | confident_S_share | 0.72125 | [0.719375, 0.723125] | 5 |
| CNN-F-E0-fixed | 2 | pooled_confident_S_error | 0.00883916 | [0.00864304, 0.00954861] | 5 |
| CNN-F-E0-fixed | 2 | case_confident_S_error | 0.0077016 | [0.00749581, 0.00829146] | 5 |
| CNN-F-E0-fixed | 2 | E_regret | 0.0160525 | [0.00888296, 0.0187625] | 5 |
| CNN-F-E0-fixed | 2 | C_regret | 0.0192057 | [0.0182187, 0.0213278] | 5 |
| CNN-F-E0-fixed | 2 | window_mean_RMSE_over_sigma | 0.123416 | [0.12313, 0.123827] | 5 |
| CNN-F-E0-fixed | 2 | window_mean_anomaly_correlation | 0.982364 | [0.982215, 0.982475] | 5 |
| CNN-F-E0-fixed | 2 | J8_RMSE | 0.0272937 | [0.0252288, 0.0291987] | 5 |
| CNN-F-E0-fixed | 2 | J8_bias | -0.00137673 | [-0.00271941, 0.000291805] | 5 |
| CNN-F-E0-fixed | 2 | Dk_RMSE | 0.0183887 | [0.0173124, 0.0191144] | 5 |
| CNN-F-E0-fixed | 2 | Dk_bias | -0.00196248 | [-0.00224262, -0.00172067] | 5 |
| CNN-F-E0-fixed | 2 | seven_pattern_same_lead_difference | -0.155 | [-0.162143, -0.142857] | 5 |
| CNN-F-E0-fixed | 2 | fixed_cohort_paired_endpoint | -0.30408 | [-0.323466, -0.288046] | 5 |
| CNN-F-E0-fixed | 2 | E_capture_fraction | 0.948832 | [0.940194, 0.971685] | 5 |
| CNN-F-E0-fixed | 2 | E_harms | 1.4 | [1, 2] | 5 |
| CNN-F-E0-fixed | 2 | E_actions_taken | 200 | [200, 200] | 5 |
| CNN-F-E0-fixed | 2 | C_delta_0_capture_fraction | 0.938782 | [0.932017, 0.941928] | 5 |
| CNN-F-E0-fixed | 2 | C_delta_0_harms | 0.2 | [0, 1] | 5 |
| CNN-F-E0-fixed | 2 | C_delta_0_actions_taken | 194 | [193, 195] | 5 |
| CNN-F-E0-fixed | 2 | forcing_estimate_RMSE | 0.0150712 | [0.0137792, 0.0162087] | 5 |
| CNN-F-E0-fixed | 2 | forcing_estimate_bias | 0.000448192 | [-4.73948e-05, 0.00203784] | 5 |
| CNN-F-E0-fixed | 2 | forcing_estimate_correlation | 0.938259 | [0.929286, 0.948221] | 5 |
| CNN-F-E0-fixed | 3 | confident_S_share | 0.408375 | [0.405, 0.41125] | 5 |
| CNN-F-E0-fixed | 3 | pooled_confident_S_error | 0.00856764 | [0.00766871, 0.00920245] | 5 |
| CNN-F-E0-fixed | 3 | case_confident_S_error | 0.0133381 | [0.0107827, 0.0166261] | 5 |
| CNN-F-E0-fixed | 3 | E_regret | 0.0812271 | [0.0747236, 0.0858633] | 5 |
| CNN-F-E0-fixed | 3 | C_regret | 0.178656 | [0.173835, 0.182672] | 5 |
| CNN-F-E0-fixed | 3 | window_mean_RMSE_over_sigma | 0.271362 | [0.270995, 0.271903] | 5 |
| CNN-F-E0-fixed | 3 | window_mean_anomaly_correlation | 0.926339 | [0.925966, 0.92658] | 5 |
| CNN-F-E0-fixed | 3 | J8_RMSE | 0.0683187 | [0.064527, 0.0711401] | 5 |
| CNN-F-E0-fixed | 3 | J8_bias | 0.000455283 | [-0.000650131, 0.00278474] | 5 |
| CNN-F-E0-fixed | 3 | Dk_RMSE | 0.0858894 | [0.0827209, 0.0879002] | 5 |
| CNN-F-E0-fixed | 3 | Dk_bias | -0.00353679 | [-0.00411266, -0.00326958] | 5 |
| CNN-F-E0-fixed | 3 | seven_pattern_same_lead_difference | -0.275429 | [-0.288571, -0.264286] | 5 |
| CNN-F-E0-fixed | 3 | fixed_cohort_paired_endpoint | -0.30408 | [-0.323466, -0.288046] | 5 |
| CNN-F-E0-fixed | 3 | E_capture_fraction | 0.849818 | [0.841246, 0.861843] | 5 |
| CNN-F-E0-fixed | 3 | E_harms | 10.4 | [10, 11] | 5 |
| CNN-F-E0-fixed | 3 | E_actions_taken | 199.6 | [199, 200] | 5 |
| CNN-F-E0-fixed | 3 | C_delta_0_capture_fraction | 0.66968 | [0.662256, 0.678594] | 5 |
| CNN-F-E0-fixed | 3 | C_delta_0_harms | 1 | [1, 1] | 5 |
| CNN-F-E0-fixed | 3 | C_delta_0_actions_taken | 142.2 | [141, 144] | 5 |
| CNN-F-E0-fixed | 3 | forcing_estimate_RMSE | 0.0150712 | [0.0137792, 0.0162087] | 5 |
| CNN-F-E0-fixed | 3 | forcing_estimate_bias | 0.000448192 | [-4.73948e-05, 0.00203784] | 5 |
| CNN-F-E0-fixed | 3 | forcing_estimate_correlation | 0.938259 | [0.929286, 0.948221] | 5 |
| CNN-F-E1-fixed | 2 | confident_S_share | 0.72525 | [0.7225, 0.728125] | 5 |
| CNN-F-E1-fixed | 2 | pooled_confident_S_error | 0.0177495 | [0.0163934, 0.0197425] | 5 |
| CNN-F-E1-fixed | 2 | case_confident_S_error | 0.0156602 | [0.0139971, 0.0179654] | 5 |
| CNN-F-E1-fixed | 2 | E_regret | 0.0818819 | [0.0761388, 0.0864899] | 5 |
| CNN-F-E1-fixed | 2 | C_regret | 0.0968528 | [0.0942364, 0.0982678] | 5 |
| CNN-F-E1-fixed | 2 | window_mean_RMSE_over_sigma | 0.123004 | [0.122061, 0.123547] | 5 |
| CNN-F-E1-fixed | 2 | window_mean_anomaly_correlation | 0.982412 | [0.982282, 0.982623] | 5 |
| CNN-F-E1-fixed | 2 | J8_RMSE | 0.0249304 | [0.0234292, 0.0258999] | 5 |
| CNN-F-E1-fixed | 2 | J8_bias | -0.00294784 | [-0.00449652, -0.001272] | 5 |
| CNN-F-E1-fixed | 2 | Dk_RMSE | 0.0802409 | [0.0793749, 0.0806112] | 5 |
| CNN-F-E1-fixed | 2 | Dk_bias | 0.0258337 | [0.0257094, 0.0259386] | 5 |
| CNN-F-E1-fixed | 2 | seven_pattern_same_lead_difference | -0.148 | [-0.15, -0.145714] | 5 |
| CNN-F-E1-fixed | 2 | fixed_cohort_paired_endpoint | -0.298424 | [-0.335739, -0.271183] | 5 |
| CNN-F-E1-fixed | 2 | E_capture_fraction | 0.739 | [0.724312, 0.757306] | 5 |
| CNN-F-E1-fixed | 2 | E_harms | 1.4 | [1, 2] | 5 |
| CNN-F-E1-fixed | 2 | E_actions_taken | 200 | [200, 200] | 5 |
| CNN-F-E1-fixed | 2 | C_delta_0_capture_fraction | 0.69128 | [0.68677, 0.69962] | 5 |
| CNN-F-E1-fixed | 2 | C_delta_0_harms | 0.4 | [0, 1] | 5 |
| CNN-F-E1-fixed | 2 | C_delta_0_actions_taken | 184.8 | [184, 186] | 5 |
| CNN-F-E1-fixed | 2 | forcing_estimate_RMSE | 0.0474043 | [0.0467715, 0.047872] | 5 |
| CNN-F-E1-fixed | 2 | forcing_estimate_bias | 0.0148327 | [0.0138957, 0.015723] | 5 |
| CNN-F-E1-fixed | 2 | forcing_estimate_correlation | 0.671859 | [0.668434, 0.676775] | 5 |
| CNN-F-E1-fixed | 3 | confident_S_share | 0.4025 | [0.4, 0.405625] | 5 |
| CNN-F-E1-fixed | 3 | pooled_confident_S_error | 0.0124251 | [0.0108192, 0.0140187] | 5 |
| CNN-F-E1-fixed | 3 | case_confident_S_error | 0.0173711 | [0.0147841, 0.023098] | 5 |
| CNN-F-E1-fixed | 3 | E_regret | 0.147521 | [0.14343, 0.149944] | 5 |
| CNN-F-E1-fixed | 3 | C_regret | 0.254539 | [0.252573, 0.256536] | 5 |
| CNN-F-E1-fixed | 3 | window_mean_RMSE_over_sigma | 0.270726 | [0.270054, 0.271039] | 5 |
| CNN-F-E1-fixed | 3 | window_mean_anomaly_correlation | 0.926603 | [0.926433, 0.926919] | 5 |
| CNN-F-E1-fixed | 3 | J8_RMSE | 0.0673239 | [0.0639965, 0.069828] | 5 |
| CNN-F-E1-fixed | 3 | J8_bias | -0.00129904 | [-0.00265878, -0.000115673] | 5 |
| CNN-F-E1-fixed | 3 | Dk_RMSE | 0.146164 | [0.143433, 0.14795] | 5 |
| CNN-F-E1-fixed | 3 | Dk_bias | 0.0259056 | [0.0255942, 0.0262333] | 5 |
| CNN-F-E1-fixed | 3 | seven_pattern_same_lead_difference | -0.279 | [-0.295714, -0.265714] | 5 |
| CNN-F-E1-fixed | 3 | fixed_cohort_paired_endpoint | -0.298424 | [-0.335739, -0.271183] | 5 |
| CNN-F-E1-fixed | 3 | E_capture_fraction | 0.727246 | [0.722768, 0.734811] | 5 |
| CNN-F-E1-fixed | 3 | E_harms | 15.8 | [14, 17] | 5 |
| CNN-F-E1-fixed | 3 | E_actions_taken | 200 | [200, 200] | 5 |
| CNN-F-E1-fixed | 3 | C_delta_0_capture_fraction | 0.529381 | [0.525687, 0.533015] | 5 |
| CNN-F-E1-fixed | 3 | C_delta_0_harms | 1.4 | [1, 2] | 5 |
| CNN-F-E1-fixed | 3 | C_delta_0_actions_taken | 121.4 | [120, 123] | 5 |
| CNN-F-E1-fixed | 3 | forcing_estimate_RMSE | 0.0474043 | [0.0467715, 0.047872] | 5 |
| CNN-F-E1-fixed | 3 | forcing_estimate_bias | 0.0148327 | [0.0138957, 0.015723] | 5 |
| CNN-F-E1-fixed | 3 | forcing_estimate_correlation | 0.671859 | [0.668434, 0.676775] | 5 |
| CNN-F-E1-rolling | 2 | confident_S_share | 0.732625 | [0.729375, 0.735] | 5 |
| CNN-F-E1-rolling | 2 | pooled_confident_S_error | 0.0267865 | [0.0255973, 0.0280612] | 5 |
| CNN-F-E1-rolling | 2 | case_confident_S_error | 0.0249595 | [0.0240893, 0.0261012] | 5 |
| CNN-F-E1-rolling | 2 | E_regret | 0.0182859 | [0.0141932, 0.0242778] | 5 |
| CNN-F-E1-rolling | 2 | C_regret | 0.0241766 | [0.0220785, 0.0257585] | 5 |
| CNN-F-E1-rolling | 2 | window_mean_RMSE_over_sigma | 0.12312 | [0.122758, 0.123504] | 5 |
| CNN-F-E1-rolling | 2 | window_mean_anomaly_correlation | 0.982346 | [0.982225, 0.982448] | 5 |
| CNN-F-E1-rolling | 2 | J8_RMSE | 0.0370685 | [0.0356668, 0.0385267] | 5 |
| CNN-F-E1-rolling | 2 | J8_bias | -0.00598063 | [-0.0102751, 0.00152294] | 5 |
| CNN-F-E1-rolling | 2 | Dk_RMSE | 0.0364535 | [0.0356892, 0.0368865] | 5 |
| CNN-F-E1-rolling | 2 | Dk_bias | 0.00533099 | [0.00472723, 0.00613254] | 5 |
| CNN-F-E1-rolling | 2 | seven_pattern_same_lead_difference | -0.150286 | [-0.164286, -0.138571] | 5 |
| CNN-F-E1-rolling | 2 | fixed_cohort_paired_endpoint | -0.303378 | [-0.324939, -0.273932] | 5 |
| CNN-F-E1-rolling | 2 | E_capture_fraction | 0.941713 | [0.922614, 0.954759] | 5 |
| CNN-F-E1-rolling | 2 | E_harms | 2 | [2, 2] | 5 |
| CNN-F-E1-rolling | 2 | E_actions_taken | 200 | [200, 200] | 5 |
| CNN-F-E1-rolling | 2 | C_delta_0_capture_fraction | 0.922937 | [0.917894, 0.929625] | 5 |
| CNN-F-E1-rolling | 2 | C_delta_0_harms | 1.6 | [1, 2] | 5 |
| CNN-F-E1-rolling | 2 | C_delta_0_actions_taken | 197 | [196, 198] | 5 |
| CNN-F-E1-rolling | 2 | forcing_estimate_RMSE | 0.0474043 | [0.0467715, 0.047872] | 5 |
| CNN-F-E1-rolling | 2 | forcing_estimate_bias | 0.0148327 | [0.0138957, 0.015723] | 5 |
| CNN-F-E1-rolling | 2 | forcing_estimate_correlation | 0.671859 | [0.668434, 0.676775] | 5 |
| CNN-F-E1-rolling | 3 | confident_S_share | 0.438625 | [0.435, 0.44375] | 5 |
| CNN-F-E1-rolling | 3 | pooled_confident_S_error | 0.0410363 | [0.0397163, 0.0422535] | 5 |
| CNN-F-E1-rolling | 3 | case_confident_S_error | 0.0744304 | [0.0719862, 0.0792607] | 5 |
| CNN-F-E1-rolling | 3 | E_regret | 0.117524 | [0.110894, 0.121554] | 5 |
| CNN-F-E1-rolling | 3 | C_regret | 0.16597 | [0.158649, 0.169734] | 5 |
| CNN-F-E1-rolling | 3 | window_mean_RMSE_over_sigma | 0.270255 | [0.269437, 0.27091] | 5 |
| CNN-F-E1-rolling | 3 | window_mean_anomaly_correlation | 0.92677 | [0.926404, 0.927181] | 5 |
| CNN-F-E1-rolling | 3 | J8_RMSE | 0.080101 | [0.0784952, 0.0812859] | 5 |
| CNN-F-E1-rolling | 3 | J8_bias | -0.00509673 | [-0.0105982, 0.00410547] | 5 |
| CNN-F-E1-rolling | 3 | Dk_RMSE | 0.126543 | [0.125947, 0.127378] | 5 |
| CNN-F-E1-rolling | 3 | Dk_bias | -0.00794188 | [-0.00866851, -0.00705065] | 5 |
| CNN-F-E1-rolling | 3 | seven_pattern_same_lead_difference | -0.257714 | [-0.266429, -0.242857] | 5 |
| CNN-F-E1-rolling | 3 | fixed_cohort_paired_endpoint | -0.303378 | [-0.324939, -0.273932] | 5 |
| CNN-F-E1-rolling | 3 | E_capture_fraction | 0.782709 | [0.775258, 0.794968] | 5 |
| CNN-F-E1-rolling | 3 | E_harms | 17.6 | [16, 19] | 5 |
| CNN-F-E1-rolling | 3 | E_actions_taken | 200 | [200, 200] | 5 |
| CNN-F-E1-rolling | 3 | C_delta_0_capture_fraction | 0.693136 | [0.686177, 0.706672] | 5 |
| CNN-F-E1-rolling | 3 | C_delta_0_harms | 8.2 | [7, 9] | 5 |
| CNN-F-E1-rolling | 3 | C_delta_0_actions_taken | 163.4 | [162, 164] | 5 |
| CNN-F-E1-rolling | 3 | forcing_estimate_RMSE | 0.0474043 | [0.0467715, 0.047872] | 5 |
| CNN-F-E1-rolling | 3 | forcing_estimate_bias | 0.0148327 | [0.0138957, 0.015723] | 5 |
| CNN-F-E1-rolling | 3 | forcing_estimate_correlation | 0.671859 | [0.668434, 0.676775] | 5 |

| Estimator run | Completed updates | Skipped updates | Selected step | Charged GPU seconds | GPU |
|---|---:|---:|---:|---:|---|
| E0-seed1 | 5000 | 0 | 5000 | 419.846 | NVIDIA CMP 170HX |
| E0-seed2 | 5000 | 0 | 5000 | 419.232 | NVIDIA CMP 170HX |
| E1-seed1 | 5000 | 0 | 5000 | 1609.26 | NVIDIA CMP 170HX |
| E0-seed3 | 5000 | 0 | 5000 | 417.059 | NVIDIA CMP 170HX |
| E1-seed3 | 5000 | 0 | 5000 | 1587.71 | NVIDIA CMP 170HX |
| E1-seed2 | 5000 | 0 | 5000 | 1581.17 | NVIDIA CMP 170HX |
| E0-seed5 | 5000 | 0 | 5000 | 419.683 | NVIDIA CMP 170HX |
| E0-seed4 | 5000 | 0 | 5000 | 418.693 | NVIDIA CMP 170HX |
| E1-seed4 | 5000 | 0 | 5000 | 1617.6 | NVIDIA CMP 170HX |
| E1-seed5 | 5000 | 0 | 5000 | 1579.79 | NVIDIA CMP 170HX |

Alignment record: 10 factual frames before onset and the cutoff state at onset; intervention begins for the next predicted step. The action field accompanies the full factual context, including frames generated before onset. The same action field and trajectory forcing accompany every autoregressive call as predicted frames replace factual frames. Each draw supplies its own noise-free factual history at the cutoff; the selected action field accompanies the initial context and every subsequent rolling context. This matches the onset alignment of training. Random offsets range from the pre-action context through the last complete context in each action branch. The branch action field is supplied even to a window entirely before onset.

All factual-context frames have been replaced after 11 output ticks (0.55 model-time units; 0.927754 LT). Source code hashes and line evidence are in receipts/acd_stage18_alignment.json.

## Part D

Forward-mode derivatives pass through the actual FP32 learned rollout; window energies accumulate in float64. Sulaco compares saved derivatives against each draw’s saved physics tangent response. No realized outcome is required.

| Model | LT | Sign agreement | Normalized RMS error | Three-class agreement | Kappa | Median z | Pooled squared error |
|---|---:|---:|---:|---:|---:|---:|---:|
| CNN-20k | 0 | 0.915468 | 0.341359 | 0.89625 | 0.79794 | 64.602 | 0.0071899 |
| CNN-20k | 1 | 0.910923 | 0.194007 | 0.865 | 0.760565 | 13.0794 | 0.014187 |
| CNN-20k | 1.5 | 0.914669 | 0.297712 | 0.855625 | 0.76265 | 7.28691 | 0.0680203 |
| CNN-20k | 2 | 0.897977 | 0.490093 | 0.8475 | 0.766654 | 3.5822 | 0.532937 |
| CNN-20k | 2.5 | 0.877498 | 0.831474 | 0.848125 | 0.759828 | 1.69226 | 5.17608 |
| CNN-20k | 3 | 0.839362 | 1.21105 | 0.881875 | 0.770137 | 0.83687 | 49.7537 |
| CNN-20k | 4 | 0.735944 | 1.5481 | 0.944375 | 0.65833 | 0.247766 | 1691.79 |
| CNN-20k | 6 | 0.555771 | 1.72278 | 0.999375 | 0 | 0.0376747 | 679152 |
| CNN-F-E0-fixed-seed1 | 0 | 0.980779 | 0.0300863 | 0.969375 | 0.94062 | 62.6354 | 5.5852e-05 |
| CNN-F-E0-fixed-seed1 | 1 | 0.983499 | 0.0692732 | 0.9725 | 0.951564 | 13.3557 | 0.00180878 |
| CNN-F-E0-fixed-seed1 | 1.5 | 0.98066 | 0.0916879 | 0.9575 | 0.930375 | 7.4273 | 0.00645162 |
| CNN-F-E0-fixed-seed1 | 2 | 0.974917 | 0.19319 | 0.9675 | 0.950316 | 3.55116 | 0.0828111 |
| CNN-F-E0-fixed-seed1 | 2.5 | 0.960287 | 0.476164 | 0.956875 | 0.931992 | 1.73142 | 1.69753 |
| CNN-F-E0-fixed-seed1 | 3 | 0.930421 | 0.865188 | 0.966875 | 0.936298 | 0.848458 | 25.3936 |
| CNN-F-E0-fixed-seed1 | 4 | 0.835839 | 1.289 | 0.984375 | 0.903954 | 0.257833 | 1172.89 |
| CNN-F-E0-fixed-seed1 | 6 | 0.617502 | 1.52611 | 1 | 1 | 0.0360298 | 532941 |
| CNN-F | 0 | 0.980943 | 0.0299612 | 0.969375 | 0.940583 | 62.6332 | 5.53884e-05 |
| CNN-F | 1 | 0.983795 | 0.068891 | 0.970625 | 0.948279 | 13.3652 | 0.00178888 |
| CNN-F | 1.5 | 0.980725 | 0.0867081 | 0.96375 | 0.940655 | 7.48455 | 0.00576986 |
| CNN-F | 2 | 0.975626 | 0.170396 | 0.963125 | 0.943636 | 3.54171 | 0.0644226 |
| CNN-F | 2.5 | 0.961938 | 0.41603 | 0.959375 | 0.935966 | 1.72295 | 1.29585 |
| CNN-F | 3 | 0.931776 | 0.800746 | 0.965625 | 0.933886 | 0.848413 | 21.7516 |
| CNN-F | 4 | 0.838701 | 1.19011 | 0.986875 | 0.920385 | 0.254589 | 999.825 |
| CNN-F | 6 | 0.617671 | 1.51 | 0.999375 | 0 | 0.0357771 | 521753 |
| CNN-noF | 0 | 0.957526 | 0.373173 | 0.946875 | 0.896777 | 62.0544 | 0.00859254 |
| CNN-noF | 1 | 0.909407 | 1.50547 | 0.86125 | 0.753928 | 15.1655 | 0.854284 |
| CNN-noF | 1.5 | 0.903867 | 1.76247 | 0.85125 | 0.754731 | 7.92792 | 2.38389 |
| CNN-noF | 2 | 0.900697 | 1.52087 | 0.84875 | 0.768633 | 3.68037 | 5.13217 |
| CNN-noF | 2.5 | 0.892087 | 1.26043 | 0.856875 | 0.776166 | 1.91107 | 11.8944 |
| CNN-noF | 3 | 0.86618 | 1.19916 | 0.86625 | 0.745906 | 0.984572 | 48.7818 |
| CNN-noF | 4 | 0.775394 | 1.42855 | 0.906875 | 0.567797 | 0.325503 | 1440.6 |
| CNN-noF | 6 | 0.578171 | 1.7888 | 0.990625 | 0.116608 | 0.0420514 | 732203 |

RMS errors divide by the pooled physics tangent RMS at the same lead. Near-zero posterior masses, per-pair squared-error quartiles and probability-transfer errors are retained in the receipt. The selected response-control derivative is added after its frozen validation selection. All readings are post hoc and license no frozen route.

## Part C execution reading

R-other execution reading: Selected weight is zero. Selected and weight-zero labels refer to the same model. If the frozen extra-seed trigger fires, train each further seed once and report that run under both labels; no duplicate training, inference, scoring or GPU charge. Criteria unchanged. Frozen training, validation selection, extra-seed trigger, populations and scoring are unchanged. Shared labels do not represent independent runs.

| Weight | Checkpoint step | Guard abort | Validation state MSE / weight zero | Validation effect RMSE |
|---:|---:|---|---:|---:|
| 0 | 20000 | none | 1 | 0.36154961 |
| 0.01 | 20000 | none | 21.118794 | 0.20251311 |
| 0.03 | 6000 | skip limit exceeded | 291.45724 | 0.23927088 |
| 0.1 | 20000 | none | 45.180112 | 0.21196242 |
| 0.3 | 20000 | none | 81.022389 | 0.24039685 |
| 1 | 4000 | skip limit exceeded | 649.28469 | 0.24056081 |

All validation rows are descriptive only. Guard-aborted rows use the last saved checkpoint, verified tensor-for-tensor to equal the validation-selected model, with identical step and validation MSE; container SHA-256s differ because the trainer serializes the two files separately. Other rows use the validation-selected checkpoint. These additions do not rerun selection. Source values, checkpoint identities and reporting-label aliases are in receipts/acd_stage18_C_execution_reading.json.

Extra-seed trigger: pending confirmation scoring.

| Reporting label | Shared run identities |
|---|---|
| weight zero | CNN-noF-response-0-seed1 |
| selected | CNN-noF-response-0-seed1 |
