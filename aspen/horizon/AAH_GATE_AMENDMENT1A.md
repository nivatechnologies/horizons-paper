## Amendment 1a: A5 and affected readings — 2026-10-04

**Gate PASS for execution.** Step 0 is complete and not rerun.

Source accounting: reread the WO twice through the niva-obsidian MCP, including raw content, and searched 02-Projects for Amendment 1a. The returned copy still has Amendment 1 A5's 512 bound (modified 2026-10-04T05:43:28.282Z); search found no Amendment 1a. Todd's direct message supplies the controlling correction: M_95 is defined only on {8,16,32,64,128,256}, and a censored unpaired arm uses 256 as a conservative bound. Direct user instructions supersede the stale returned copy. No revision is invented by the executor. This source discrepancy is recorded, not an execution blocker.

A5 implementation: smallest successful tested grid budget at >=0.95 eligible-case accuracy; otherwise censored. The comparison uses unpaired measured value or conservative 256, divided by paired measured grid value. A censored paired arm fails. No continuous-member optimum, extrapolated success at 512, or strict statistical guarantee is asserted. Commitment retains its amended six-look nominal bootstrap design and reports empirical errors.

### Checks 1–9 including 5a, limited to touched parts

| Check | Result |
|---|---|
| 1 two-sided feasibility | PASS: censored unpaired/paired64 gives 256/64=4; paired128 gives 256/128=2 and fails |
| 2 independence | PASS: disjoint truth/arm streams and calibration/test panels unchanged |
| 3 referent | PASS: M_95 is explicitly a tested-grid budget, censoring is a separate status |
| 4 source class | PASS: 256 is a conservative rule-supported bound; no missing-budget measurement invented |
| 5 no example as definition | PASS: formulas and correction define readings; examples illustrate |
| 5a example provenance | PASS: every constructed input below is a hypothesis under test |
| 6 surprise | PASS: small paired benefit or censored paired arm can still defeat PASS |
| 7 null baseline | PASS: random/myopic nulls unchanged |
| 8 comparator separability | PASS: same-physics paired/unpaired comparison and explicit conservative censoring |
| 9 selector separation | PASS under existing Step 0 mechanism; final run-1 actions unchanged; budget/censor selector supplied by Todd's correction |

### Concrete inputs: all hypotheses under test

- Fixed-M >=95%: 190/200 correct at M=64 passes; 189/200 fails.
- Grid minimum: accuracy 0.90 at8, 0.95 at16, 0.93 at32 gives M_95=16; all six grid values below0.95 gives censored. No monotonicity assumption.
- Censored numerator: paired64 plus censored unpaired gives4 and passes3x; paired128 gives2 and fails.
- Censored denominator: paired censored with unpaired128 fails; paired32 with unpaired128 passes4.
- Measured numerator: unpaired128/paired32=4 passes; unpaired128/paired64=2 fails.
- Combined PASS: both systems defined T_f=1, sufficient sustained T_d=3, paired64/unpaired censored passes. Same horizons with paired128/unpaired censored fails.
- KILL precedence remains: both systems sufficient at G(1.5 T_f) with accuracy0.4 triggers KILL; either accuracy0.5 does not.
- Commitment: all amended nominal bounds >0 commits; any bound <=0 through256 remains uncommitted.

Differential correction prediction verified: the previous censored/paired128 example changes from the erroneous bound-based4 to conservative2 and stays failed. Censored/paired64 retains a provable conservative4 and passes; censored paired remains failed; the earlier overlapping accuracy example remains not PASS. Calibration failure, absent forecast crossing, near-ties and removed uncentered variate retain their previous dispositions.

Authorship: correction to A5 supplied directly by Todd, referencing Amendment 1a; action sets by blinded Codex run1 with run2/Claude overlap; horizons/windows/objectives by amended WO author (role-based Claude attribution as previously recorded). No new selector is selected from data.

Disposition: write AAH_FREEZE.md before experimental test data/training. Run calibration first, then every-action chaos gate, and obey the calibration/chaos stop rules before any confirmation panel or learned training. Branch paper/aspen-2026-10-horizon; Baccus Kolmogorov, sulaco Lorenz-96 and truth ensembles. Freeze numeric calibration outcomes by a committed addendum before test-panel generation/training.
