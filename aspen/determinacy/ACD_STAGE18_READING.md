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
