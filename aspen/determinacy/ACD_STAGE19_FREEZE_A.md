# Stage 19 Freeze A — fresh reference confirmation panel

Part 1 is blind reference sampling. The fresh reference family is confirmatory; mechanism and learned-model readings will be frozen separately in Part 2. This stage licenses no frozen route. No emulator may read these draws, and no realized outcome may be computed or opened in Part 1.

## Generation and access

Generate 200 instances using `acd-r3-observation`. Use the inherited generation exactly: independent 8 + N(0,1) at every site, spin up 50 LT at F=8, eleven noise-free frames spaced 0.05 apart, and independent Gaussian observation noise of standard deviation 0.02 sigma. The hidden history is written only by generation into runs/stage19/hidden; neither posterior nor forecasting code opens it. Observations are atomically saved and hashed before inference. Every sampler, initializer, diagnostic and forecast file is saved and hashed before dependent consumers read it. Large arrays remain untracked. Per-case outputs and sampler attempts permit restart after a reboot; completed cases are verified and skipped.

## Main posterior

Use the frozen prior and likelihood from acd_posterior.py: x_first has independent Normal(0,(10 sigma)^2) components, F is Uniform(6,10), and the Gaussian likelihood uses the identical float64 RK4 observation map. Four vectorized dense-mass NUTS chains use target acceptance 0.9, 1000 warm-up iterations and 500 retained draws per chain. Initialization uses the frozen acd_fits.case_fits implementation: 128 independent noise-perturbed fits, original-observation misfit and path checks, and the first four valid members. New RNG leaves are supplied by the Stage19 adapter, without changing the inherited module's source. Fewer than four valid members stops the case for R-other instead of relaxing its initialization requirement.

Retain 128 evenly spaced draws per chain (512 total). Split rank R-hat <=1.01 and bulk ESS >=400 are required for every parameter and the log likelihood, with divergent fraction <=0.01. Test all eight D_k and J_8 at both 2 and 3 LT. A failed functional gate triggers forecasts and diagnostics on all 2000 draws, with an integer confidence threshold of 1900 votes. If gates still fail, including any parameter failure, rerun once with 2000 warm-up iterations and 500 draws per chain. Exclude only after that retry fails. Preserve both attempts and every gate vector. The frozen forward forecast map is used for the diagnostics.

## Known-forcing contract (Todd's instruction)

Target p(x_first | Y,F=8), with 40 sampled dimensions. The prior, likelihood, RK4 map, NUTS settings, thinning, diagnostic thresholds, full-draw rescoring and retry rule are identical to the main posterior, except that F is fixed at 8 and is absent from the sampled coordinates and parameter diagnostics. Each chain starts from a maximum-likelihood fit at F=8 to an independently noise-perturbed observation copy. The original misfit and path checks remain unchanged; select the first four valid members among 128 fits. `acd_stage19_knownF.py` implements this contract; its hash is recorded below. Namespace acd-r3-knownF-sampler is disjoint from all other streams. When Stage15C commits, compare its implementation and record any difference as R-other. Keep this Stage19 contract unchanged.

## Forecasts and frozen null

Forecast every retained draw of both posteriors under all nine options at amplitude 0.16, using each main draw's F or fixed F=8 for knownF. Use all eight inherited leads and inclusive output windows, global energy and the energy of sites 0 through 9. Main-posterior draws additionally use the unchanged Stage9 forward-mode RK4 tangent recursion and Stage9 B1 energy-budget code path (the Stage6 forward kernel), saving all per-draw G_k and budget terms. Record closure against the inherited cost calculation. No truth is needed for any of these computations. Reuse the saved 4096-state null, global J-bar and block J-bar unchanged; their source-file hashes are recorded below. MCMC output is not expected to be bitwise identical across hosts.

## Confirmatory reference family

All following readings belong to one declared family, each tested at the original 1% level, and all will be reported without selection:

- C1: original R0 accuracy at every lead, using the original criterion; PASS required at 2 LT.
- C2: original eligible paired first-loss endpoint and censoring. PRECEDES requires estimate at most -0.20 and the two-sided 99% interval's upper bound below zero. Report the direction criterion (upper bound below zero) separately.
- C3: at both 2 and 3 LT, observation-confident S share over all eight patterns minus confident F_c share, magnitude at least 0.15 and two-sided 99% interval excluding zero.
- C4: at both 2 and 3 LT, confident S share over seven zero-mean patterns minus confident F_c share, with the two-sided 99% interval wholly below zero.

All other Part1 quantities are descriptive. Realized-answer scoring waits for the pushed Part2 freeze; no mechanism or learned-model confirmatory reading is set here.

## Timing and continuation

First run five complete instances, including both posterior gate workflows and all prescribed forecasts, tangents, budget terms and block energies. Project the full panel on the recorded available CPU groups, adding conservative allowances for the original confirmation rescore and retry rates. Continue only if projected wall time is at most 24 hours. Otherwise save the timing receipt and stop. Each worker is pinned to four distinct physical cores; four physical cores remain outside all worker affinity groups for Stage18. Every step uses CPU-only JAX and float64, with exact NumPyro 0.22.0 and JAX 0.11.2. No GPU, Qwen service or AFD close-out file is touched.

## Machine-readable freeze

The following values are generated from existing source files, saved receipts and the namespace algorithm.

```json
{
  "panel_instances": 200,
  "seeds": {
    "ids": {
      "acd-r3-observation": 7420358367672037684,
      "acd-r3-sampler": 15952455394814718883,
      "acd-r3-knownF-sampler": 18290979991765005169
    },
    "id_rule": "first eight bytes of SHA-256(namespace), little endian; SeedSequence [ID,0,sub,case,member,action]",
    "new_leaf_count": 54800,
    "prior_acd_leaf_count": 147564,
    "earlier_namespace_literals": [
      "acd-bootstrap",
      "acd-climatology",
      "acd-crude-",
      "acd-crude-conf",
      "acd-crude-dev",
      "acd-dtcheck",
      "acd-measure-",
      "acd-measure-conf",
      "acd-measure-dev",
      "acd-observation-conf",
      "acd-posterior-",
      "acd-posterior-conf",
      "acd-posterior-dev",
      "acd-sampler-",
      "acd-sampler-conf",
      "acd-sampler-dev",
      "acd-stage4-test-",
      "acd-train-F",
      "acd-twoscale"
    ],
    "earlier_root_count": 74,
    "root_disjoint": true,
    "leaves_unique": true
  },
  "code_hashes": {
    "/mnt/niva-array/work/aspen-determinacy-stage19-20261007/aspen/determinacy/acd_protocol.py": "160eabe8ccee07d0de17576a441b6fef1a93e1d5dbb68f2df9eb118a1eaad000",
    "/mnt/niva-array/work/aspen-determinacy-stage19-20261007/aspen/determinacy/acd_fits.py": "17e62ac36a1ff18bc93721dc828a77e079932f320423d3aa9e367432df9d13cd",
    "/mnt/niva-array/work/aspen-determinacy-stage19-20261007/aspen/determinacy/acd_posterior.py": "0b80c61b2e7530dabec4f9c3f0e7fee51f2cfc1ad15745b729d3ddc227c6a60a",
    "/mnt/niva-array/work/aspen-determinacy-stage19-20261007/aspen/determinacy/acd_mechanism.py": "886fea5d67b217e72829c4e07b469473e391cfb17b84d18f6bc0307606e40e9f",
    "/mnt/niva-array/work/aspen-determinacy-stage19-20261007/aspen/determinacy/acd_stage6_forward.py": "0a19fd6241604464a1d4aca8baaff6d4c60d47dc20eba64497963a942998612d",
    "/mnt/niva-array/work/aspen-determinacy-stage19-20261007/aspen/determinacy/acd_stage9_forward.py": "74241c217a34299094d4052df02debbda5ef79df28a1f348021b15f83b50a235",
    "/mnt/niva-array/work/aspen-determinacy-stage19-20261007/aspen/determinacy/acd_stage19_part1.py": "0c2ada83246e7827ce772e4c7e21d22bd9eca1c055d9228303df8ca8a43b5b1e",
    "/mnt/niva-array/work/aspen-determinacy-stage19-20261007/aspen/determinacy/acd_stage19_knownF.py": "3436c492cc71fba647822d5e37e363ae135e75742227dc4ddaf38fb99f4882c3",
    "/mnt/niva-array/work/aspen-determinacy-stage19-20261007/aspen/determinacy/acd_stage19_step0.py": "3d9ab76d89d7069105dfb8e23b4b3840923507614bfc70c3947b38b8ad411bd5",
    "/mnt/niva-array/work/aspen-determinacy-stage19-20261007/aspen/determinacy/acd_stage19_freeze.py": "5d51069e6ca6b7599b3bae827bb55650389351dda2510591f3feba93cb6958b0",
    "/mnt/niva-array/work/aspen-forecast-decision-20261005/aspen/forecast_decision/protocol.py": "e6d002264a8000ac88d15db41b76cd69bf17c5472de04b29f51b56408841412d",
    "/mnt/niva-array/work/aspen-forecast-decision-20261005/aspen/forecast_decision/physics.py": "13ef98834e47bd667f53cce50af3e7d573a1bc4eb9c38987f389a05b1f2fc5d7"
  },
  "null_hashes": {
    "runs/stage19/reused/runs/null/null.npz": "ba96dcafedf5a12585cc0f28418fd01b6a264360d2b10c72044e4ccbc0693b28",
    "runs/stage19/reused/runs/stage4b_null/states.npz": "0d7db6b75fc1f1a279e884a1c63205ba278a58726d676e41cb58d2aba5160b4d",
    "runs/stage19/reused/runs/stage6/null_block.npz": "ea3d16198e7b31ccfa8b06507d35785b3ba5a3eb0c3e4f3c295413bbf6a69bc8"
  },
  "jbar": 9.361002090527514,
  "jbar_block": 9.336460869223554,
  "environment": {
    "host": "baccus",
    "python": "3.13.11",
    "jax": "0.11.2",
    "numpyro": "0.22.0",
    "numpy": "2.5.3",
    "jax_x64": true,
    "devices": [
      "cpu:0"
    ]
  },
  "cpu_groups": [
    [
      0,
      1,
      2,
      3
    ],
    [
      4,
      5,
      6,
      7
    ],
    [
      8,
      9,
      10,
      11
    ],
    [
      12,
      13,
      14,
      15
    ],
    [
      16,
      17,
      18,
      19
    ],
    [
      20,
      21,
      22,
      23
    ],
    [
      24,
      25,
      26,
      27
    ],
    [
      28,
      29,
      30,
      31
    ],
    [
      32,
      33,
      34,
      35
    ],
    [
      36,
      37,
      38,
      39
    ],
    [
      40,
      41,
      42,
      43
    ],
    [
      44,
      45,
      46,
      47
    ],
    [
      48,
      49,
      50,
      51
    ],
    [
      52,
      53,
      54,
      55
    ],
    [
      56,
      57,
      58,
      59
    ]
  ],
  "reserved_cpus": [
    60,
    61,
    62,
    63
  ],
  "step0_receipt_sha256": "1e2d281bb4d72b25c3fbff4f7ade68f3a69d2b3a6a686416107a14bcff902bbb",
  "knownF_stage15C_comparison": "pending its commit; this contract will not change"
}
```
