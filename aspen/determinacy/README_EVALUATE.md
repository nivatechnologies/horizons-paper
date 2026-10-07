# Evaluate supplied window costs

acd_evaluate.py scores supplied costs post hoc on confirmation. It performs no training, checkpoint selection, posterior sampling or forward integration. Outcomes are read only inside scoring functions.

Supply case-indexed NPZ files with the original zero-padded filenames. Each contains J[draw, option, lead] in the same draw order as the supplied noise-free histories H and own forcings F. Use the frozen patterns, no-action index and lead/window ordering in acd_protocol.py. Optional valid marks invalid predictions. Any invalid draw or option forces no action for E/C and removes confidence for the entire model case; no survivor conditioning.

Run in the recorded CPU environment from this directory:

    python acd_evaluate.py --cost-directory MODEL_COSTS --model-name MODEL --output readings.json

Outputs include confident shares, case-averaged and pooled confident-answer accuracies with v2.3 bounds, seven-pattern reliability, error-versus-coverage, the case-level betting calibration test, same-lead comparisons, paired first-loss endpoints (model-specific and fixed posterior cohort), and decisions. Saved model reproduction fields use the Stage 9 evaluation leads; paired endpoints use the full grid. Costs do not define state skill.

The calibration test is the existing two-sided betting interval for case-mean modal probability minus correctness. Reliability-bin Clopper–Pearson intervals are descriptive because questions cluster within cases.

Required archive dependencies: supplied histories/forcings, posterior draw counts/order and exclusion metadata, the fixed climatological null, scoring-only case outcomes, fixed cohort, evaluator modules and the frozen contract. RELEASE_MANIFEST.md inventories them. The current research checkout uses inherited machine-specific data roots: replace those roots with the archive layout and package the listed dependencies before public release. No archive is published here.

Exact reproduction command:

    python acd_evaluate.py --cost-directory runs/stage9/inference/CNN-F --model-name CNN-F --output runs/stage13/evaluator_CNN-F.json --reproduce-stage9-CNN-F

The exact comparison of floating-point readings, counts and bounds is in receipts/acd_stage13_evaluator_check.json.
