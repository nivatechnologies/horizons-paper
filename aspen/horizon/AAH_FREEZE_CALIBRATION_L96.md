# Lorenz-96 calibration freeze addendum — 2026-10-04

Committed before Lorenz test-panel generation and learned training. Kolmogorov remains in calibration.

- Selected delta: 0.02
- Eligibility: 2/40 at delta0.01; 36/40 (90%) at delta0.02. First passing amplitude, no later amplitudes tested.
- Unperturbed lambda: 1.6868253700458604; LT: 0.5928295944308761
- Unperturbed lambda 95% interval: [1.680066743336494, 1.6935839967552269]
- Unperturbed spatial RMS sigma: 4.312600593723798
- Every action chaos gate passed: 8/8.

| Action | lambda | Lower95% | Upper95% |
|---|---|---|---|
| 0 | 1.6364291789001146 | 1.6297623536434618 | 1.6430960041567675 |
| 1 | 1.6855192112272581 | 1.6789455435127993 | 1.692092878941717 |
| 2 | 1.6912857564297765 | 1.685184355279371 | 1.697387157580182 |
| 3 | 1.6847953958958575 | 1.6794077938414649 | 1.69018299795025 |
| 4 | 1.690507746422347 | 1.6837560353165857 | 1.6972594575281084 |
| 5 | 1.6852556201904547 | 1.6787739633984382 | 1.6917372769824712 |
| 6 | 1.6891507544230129 | 1.6836589830075248 | 1.694642525838501 |
| 7 | 1.6903392822114496 | 1.6848715888366226 | 1.6958069755862766 |

Sources: results/l96_calibration.json and results/l96_action_chaos.json; source commit bd46f7d27417cbc01938a07cdcdea986c60f982d. Raw runtime metadata mistakenly carried launch tag7fe5631; artifact metadata records this correction explicitly after SHA256 verification of the executed source files. No numerical data changed.

The main AAH_FREEZE.md and Amendment1a member criterion remain unchanged. No test cases or trained checkpoints were used to choose amplitude or protocol.
