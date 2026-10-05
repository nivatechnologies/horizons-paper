# ACD Step 0 — v2.3

Read-only verification on sulaco; source base 1b1094a. Completed 200 cases.

| Item | Verification |
|---|---|
| 1 Protocol | Exact LT/SIGMA/leads/OUT; ticks 0–83; unrounded inclusive epsilon window predicate confirmed in protocol.py |
| 2 Observation model | history starts 8+Gaussian, rounds 50 LT/dt spin steps, then 11 frames at 0.05; observation sigma .02·SIGMA; last frame defines time zero |
| 3 Actions/outcome | Eight unit-RMS patterns; persistent F+.16p; index 8 zero pattern; actual cost 9×8 |
| 4 Cost | .5·mean(x²) then arithmetic window mean over inherited WINDOWS |
| 5 dt | Inherited record PASS at 0.01 |
| 6 Fits | extras.objective sums squared residuals/440; exact RK4 reverse; L-BFGS-B maxiter200, F=identify(y,dt); success/finite and all-frame RMS≤10SIGMA checks |
| 7 Data | Manifest matches 200/200; bitwise reproductions 200/200; maximum actual-cost discrepancy 0 |
| 8 CNN | Checkpoint hash below; 11 input frames and SIGMA normalization; action .16p/SIGMA. Base training draws amplitudes continuously through zero, so zero lies in its action support. No inference or model initialization performed |
| 9 Two-scale | rhs2 uses h=1,c=10,b=10; state dt .001 recorded in inherited NUMBERS.md. R7 is optional and not run in this go |

No inherited module was edited. New posterior/readings follow v2.3. Any inherited discrepancy is resolved by R-def, never a pre-gate halt. Full per-case evidence: runs/audit/acd_step0.json.

| Artifact | SHA256 |
|---|---|
| protocol.py | e6d002264a8000ac88d15db41b76cd69bf17c5472de04b29f51b56408841412d |
| physics.py | 13ef98834e47bd667f53cce50af3e7d573a1bc4eb9c38987f389a05b1f2fc5d7 |
| extras.py | a189a8b2a942fb028098e3af686858516b09ad6a896ab6a533808747e3058b52 |
| campaign.py | e44f509bbb5eb102c87d3752de1b7443265e8b0ebe9c6ba1800f2d34a51518dd |
| inputs/CNN-20k.pt | 3c67fc2cfc3a858613160cc81151c09ef45829f08bda67df00b9e78f35f5fe74 |
