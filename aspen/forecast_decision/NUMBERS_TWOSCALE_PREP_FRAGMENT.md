## AFD_TWOSCALE_DECISION_DTCHECK

Source: `runs/twoscale/decision_dtcheck.json`; independently replayed from sixteen raw dt-check artifacts.
Checker: `check_twoscale_prep.py`; evidence: `runs/twoscale/dtcheck_checked.json`.

Status: PASS; tamper rejection: True.

| dt | comparisons | failed | elapsed CPU wall seconds | argmin changes (1, 1.5, 2 LT_ref) | S_J |
|---|---|---|---|---|---|
| 0.001 | 336 | 0 | 23.93954798899358 | [0, 0, 0] | [0.32858822303093493, 0.37932914875779034, 0.45728253700369015] |

Chosen dt: 0.001. N2 solver dt remains 0.01 under WO §4 propagation.

Every comparison requires a strictly smaller absolute mean gap change than max(0.05*S_J, two paired standard errors).
State check, sampler approval and decision-cost check remain separate gates. No two-scale panel was launched by this checker.
