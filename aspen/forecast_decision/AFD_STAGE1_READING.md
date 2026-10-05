# Aspen forecast-versus-decision: Stage 1 reading

Stage and gate: Stage 1, sufficiency then H1a, T*=2 LT. SUFFICIENT; H1a otherwise.

Sufficiency: 188/200 eligible (0.94); P_N − max(P_myopic,P_fixed)=0.170213; myopic=0.765957; fixed=0.765957.

H1a: P_N=0.93617; P_CNN-20k=0.81383; gap=0.12234; one-sided 95% lower=0.0740546, upper=0.173684.

wACC: N-last=0.924167, CNN-20k=0.973884. wRMSE: N-last=0.288165, CNN-20k=0.155256.

Failed cases: N-last=0, CNN-20k=0; dropped members: N-last=0/12800, CNN-20k=0/12800.

Stage 1 licenses no sentence. Source: NUMBERS Stage-1 reading and checker PASS.

Headline value now, against the threshold: gap 0.12234042553191493 versus required0.15; lower bound 0.07405458089668615 versus required0.10. Neither PASS condition clears. Upper bound exceeds0.05, so this is not KILL.

What changed since the last gate: Amendment1 resolved the window halt; fresh truth and baseline evaluation now exist.

Largest remaining risk to the so-what test: the fresh baseline gap is below the precommitted counterexample threshold; repair/strongest-incumbent outcomes are not known.

Coordinator would: go to Stage2 under WO§9, because an otherwise reading explicitly authorizes continuation. No headline sentence is licensed. Stage2b truth still requires the sampler go.

NUMBERS checker PASS; tampered finite number and NaN both rejected. Raw truth eligibility was also checked on sulaco (runs/stage1_checker.json).
