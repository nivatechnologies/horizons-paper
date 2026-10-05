# Two-scale decision timestep check

PASS at dt 0.001, independently checked against raw paired costs. All 336 comparisons pass; argmin-change counts are [0, 0, 0] at leads 1, 1.5 and 2 LT_ref.

Measured values are registered in `NUMBERS_TWOSCALE_PREP_FRAGMENT.md`. Checker and altered-record rejection both pass.
No refinement propagates. The two-scale solver keeps dt 0.001; N2 and its variants keep dt 0.01.
The sampler report still requires Todd’s explicit go before two-scale panels.
