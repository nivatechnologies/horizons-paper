# Stage 19 Freeze D — inferred-context repair

This freeze is written after Stage18 A/B were pushed and before any Stage18 diagnostic arm, estimator or pipeline runs on the fresh panel. It licenses no frozen route. Stage18 D/C are outside its scope and require a later Part3c freeze.

## Timing inventory

The inventory below was obtained before writing this document. No Stage18 arm, E0/E1 estimator, fixed pipeline or rolling pipeline has run on any fresh draw; no fresh output or score exists for them. The retained CNN-F and CNN-noF Part2 outputs and L3 seed inference are existing references, not new repair outputs. No realized array was opened for inventory.

## Pipelines and unchanged paths

P0(j) uses the retained CNN-F, stored index zero, with E0 seed j estimating forcing once from each draw's own noise-free eleven-frame pre-action history at the cutoff; that estimate remains fixed. P1f(j) uses E1 once and held fixed; P1r(j) re-estimates E1 from the current rolling window at every learned step. Every estimator seed is reported. All pipelines use amplitude 0.16, nine options, eight leads and the frozen windows. The Stage18 B rollout functions execute unchanged: acd_stage18_inference.run, acd_stage18_estimators.Estimator and acd_stage9_cnn.run. Only input/output destinations and the checkpoint/name allowlist are adapted to Stage19; no Stage18 file is modified. Existing Stage19 noise-free histories are reused by hash. Stage19 Part2 CNN-F and CNN-noF outputs remain unchanged by hash.

B1, primary: for each E0 seed and fresh instance at 2 LT, take CNN-noF seven-pattern confident wrong share minus P0's. Use exactly L1's own-confident-denominator rule, implemented by acd_stage19_l3_statistic.pair_statistic. Both models must give at least one confident answer for that instance-pair. Average over defined seed differences within each instance; keep an instance if any seed defines it. In ascending instance order, acd_stats.difference_interval(alpha=0.01) gives the two-sided 99% v2.3 betting interval. Confirm only if the lower endpoint exceeds zero; empty or offset intervals cannot confirm.

B2: for every E0 seed, at 3 LT the P0 C(delta=0) policy's exact one-sided 95% Clopper–Pearson upper bound on strictly positive harm among acted instances must be below 0.05. The policy uses unchanged acd_stage13_analysis.choices and decision_rows. Harm means realized D strictly greater than zero, as in L2; exact zero-effect ties are reported separately. acd_stats.cp_bounds supplies the one-sided limits. All seeds must satisfy the criterion.

B3: at 3 LT, within each E1 seed and instance take P1r seven-pattern confident wrong share minus P1f, using the same contributing rule. Average defined seeds within instances. Map each difference to (d+1)/2 and apply acd_stats.one_sided(alpha=0.05, direction=1), then map back by 2*lower-1. Confirm only if this one-sided 95% lower bound exceeds zero. This uses the same v2.3 instance betting construction, without a two-tail allocation.

An invalid draw invalidates its instance for that pipeline; never condition on surviving draws. Such an instance gives no confident answer and E/C takes no action. Failed or unavailable seed pipelines make the affected confirmatory reading not evaluable, with all available seeds still reported descriptively; never select or substitute a seed.

## Descriptive readings

For every pipeline/seed at 2 and 3 LT report forcing-estimate RMSE, bias and correlation against each draw's forcing; state anomaly correlation and RMSE/sigma; pooled and equal-case per-draw J8/Jk/Dk errors against that same draw's physics; confidence shares; pooled and case-averaged confident errors and v2.3 bounds; mean calibration; own-fresh-cohort paired endpoint; E and C(delta=0) regret, capture, actions, strictly positive harms, exact conditional-harm bounds, ties and action histograms; and whether uniform decrease is chosen in every instance. Reuse acd_stage19_learned.model_inputs and metrics, preserving their scientific functions by hash. The forcing-estimate reading is at the cutoff, draw/action pooled, as in Stage18 B; rolling-estimator trajectory errors are not inferred from the cutoff record.

Also report P0 minus retained CNN-F under B1's construction, with a two-sided 99% interval, descriptively. No equivalence claim is made: near this panel size the construction cannot provide a narrow equivalence interval even when all differences vanish.

Repeat the Stage18 A posterior-mean forcing, constant forcing eight and seeded within-instance permutation diagnostics using unchanged Stage18 seeds and preparation path. Permutation deliberately breaks the joint posterior. Pair E0 seed j with CNN-F stored index j-1 for every committed Stage16 CNN-F checkpoint, as in Stage18's freeze; report these pairings descriptively. First-panel readings use only committed Stage18 receipts; a first-panel pairing not yet reported is shown as pending, never fabricated.

## Execution and scoring gate

After this freeze is committed and pushed, Baccus 170HX inference queues behind all L3 seed inference and any active Stage16/18 jobs. No job is preempted. P0 seeds run first, then P1f/P1r, then A diagnostics, followed by matched-seed descriptive pipelines. Jobs resume per case; outputs and manifests are written atomically and hashed before scoring. Temporary Baccus vLLM leases follow Todd's existing stop-and-restore authorization. No realized outcome is opened during inference. Scoring runs only in Stage19 scoring code on Baccus CPU from the existing realized cache, with at most four threads. It does not create new realized outcomes. Store Part3b receipt and append the reading; retain every prior registry value and push fast-forward.

## Inventory, checkpoints and code hashes

```json
{
  "inventory": {
    "utc": "2026-10-08T06:09:08.299295+00:00",
    "stage18_models_run_on_fresh_draws": [],
    "fresh_outputs_or_scores": [],
    "fresh_inference_names": [
      "CNN-20k",
      "CNN-F",
      "CNN-F-seed1",
      "CNN-F-seed4",
      "CNN-noF",
      "CNN-noF-seed1",
      "CNN-noF-seed2"
    ],
    "realized_arrays_opened": false
  },
  "tasks": [
    {
      "name": "CNN-F-E0-fixed-seed1",
      "first_panel_name": "CNN-F-E0-fixed-seed1",
      "kind": "E0",
      "rolling": false,
      "seed": 1,
      "checkpoint": "runs/stage18/checkpoints/CNN-F.pt",
      "estimator": "runs/stage18/training/E0-seed1/selected.pt",
      "checkpoint_sha256": "f883730e8df0798c07effbb1d51b05a646bea6f688b2a4bc74b9edf4ca104e8b",
      "estimator_sha256": "05b0c966567209037b87478b238939eeaa23f2202ae7148c06dd34797bdee3da"
    },
    {
      "name": "CNN-F-E0-fixed-seed2",
      "first_panel_name": "CNN-F-E0-fixed-seed2",
      "kind": "E0",
      "rolling": false,
      "seed": 2,
      "checkpoint": "runs/stage18/checkpoints/CNN-F.pt",
      "estimator": "runs/stage18/training/E0-seed2/selected.pt",
      "checkpoint_sha256": "f883730e8df0798c07effbb1d51b05a646bea6f688b2a4bc74b9edf4ca104e8b",
      "estimator_sha256": "d461bae9dfd507b07955eda2342abe717900232af40cd5ac9e0b5981fb1fcd2f"
    },
    {
      "name": "CNN-F-E0-fixed-seed3",
      "first_panel_name": "CNN-F-E0-fixed-seed3",
      "kind": "E0",
      "rolling": false,
      "seed": 3,
      "checkpoint": "runs/stage18/checkpoints/CNN-F.pt",
      "estimator": "runs/stage18/training/E0-seed3/selected.pt",
      "checkpoint_sha256": "f883730e8df0798c07effbb1d51b05a646bea6f688b2a4bc74b9edf4ca104e8b",
      "estimator_sha256": "dc6fe8559093681cece7166443cd1a8d44bdf7f8e794e9f07bed42bf2bb876a3"
    },
    {
      "name": "CNN-F-E0-fixed-seed4",
      "first_panel_name": "CNN-F-E0-fixed-seed4",
      "kind": "E0",
      "rolling": false,
      "seed": 4,
      "checkpoint": "runs/stage18/checkpoints/CNN-F.pt",
      "estimator": "runs/stage18/training/E0-seed4/selected.pt",
      "checkpoint_sha256": "f883730e8df0798c07effbb1d51b05a646bea6f688b2a4bc74b9edf4ca104e8b",
      "estimator_sha256": "fc538e434c04df7ffa91fa9021f9bb64c6006700b95262772b5e139e492a195b"
    },
    {
      "name": "CNN-F-E0-fixed-seed5",
      "first_panel_name": "CNN-F-E0-fixed-seed5",
      "kind": "E0",
      "rolling": false,
      "seed": 5,
      "checkpoint": "runs/stage18/checkpoints/CNN-F.pt",
      "estimator": "runs/stage18/training/E0-seed5/selected.pt",
      "checkpoint_sha256": "f883730e8df0798c07effbb1d51b05a646bea6f688b2a4bc74b9edf4ca104e8b",
      "estimator_sha256": "6a7edd4aee91e81b7a272c6e9b2a7962e9a000ed44ab7378f478ad6657a38e2f"
    },
    {
      "name": "CNN-F-E1-fixed-seed1",
      "first_panel_name": "CNN-F-E1-fixed-seed1",
      "kind": "E1",
      "rolling": false,
      "seed": 1,
      "checkpoint": "runs/stage18/checkpoints/CNN-F.pt",
      "estimator": "runs/stage18/training/E1-seed1/selected.pt",
      "checkpoint_sha256": "f883730e8df0798c07effbb1d51b05a646bea6f688b2a4bc74b9edf4ca104e8b",
      "estimator_sha256": "68dd5417b6682455c260669fd1d027a9c88b9b79e977a633b05eefe21db7cbbf"
    },
    {
      "name": "CNN-F-E1-fixed-seed2",
      "first_panel_name": "CNN-F-E1-fixed-seed2",
      "kind": "E1",
      "rolling": false,
      "seed": 2,
      "checkpoint": "runs/stage18/checkpoints/CNN-F.pt",
      "estimator": "runs/stage18/training/E1-seed2/selected.pt",
      "checkpoint_sha256": "f883730e8df0798c07effbb1d51b05a646bea6f688b2a4bc74b9edf4ca104e8b",
      "estimator_sha256": "f00b0e61f4711838771260d491561b98c13ece23a59013b42e02dc35d5c35af0"
    },
    {
      "name": "CNN-F-E1-fixed-seed3",
      "first_panel_name": "CNN-F-E1-fixed-seed3",
      "kind": "E1",
      "rolling": false,
      "seed": 3,
      "checkpoint": "runs/stage18/checkpoints/CNN-F.pt",
      "estimator": "runs/stage18/training/E1-seed3/selected.pt",
      "checkpoint_sha256": "f883730e8df0798c07effbb1d51b05a646bea6f688b2a4bc74b9edf4ca104e8b",
      "estimator_sha256": "2cb897095bd0947f93f437e57dd139d2aa9786da2047459ed3325326aa3307d6"
    },
    {
      "name": "CNN-F-E1-fixed-seed4",
      "first_panel_name": "CNN-F-E1-fixed-seed4",
      "kind": "E1",
      "rolling": false,
      "seed": 4,
      "checkpoint": "runs/stage18/checkpoints/CNN-F.pt",
      "estimator": "runs/stage18/training/E1-seed4/selected.pt",
      "checkpoint_sha256": "f883730e8df0798c07effbb1d51b05a646bea6f688b2a4bc74b9edf4ca104e8b",
      "estimator_sha256": "4019cf5fa1fdcdb46c308c15ac120820df8e4fe1bab6c3cb67818ac429fb177b"
    },
    {
      "name": "CNN-F-E1-fixed-seed5",
      "first_panel_name": "CNN-F-E1-fixed-seed5",
      "kind": "E1",
      "rolling": false,
      "seed": 5,
      "checkpoint": "runs/stage18/checkpoints/CNN-F.pt",
      "estimator": "runs/stage18/training/E1-seed5/selected.pt",
      "checkpoint_sha256": "f883730e8df0798c07effbb1d51b05a646bea6f688b2a4bc74b9edf4ca104e8b",
      "estimator_sha256": "296e1b28883aa63fd58eb89ea619e0586a97537e1c576b25d01d9266670cf972"
    },
    {
      "name": "CNN-F-E1-rolling-seed1",
      "first_panel_name": "CNN-F-E1-rolling-seed1",
      "kind": "E1",
      "rolling": true,
      "seed": 1,
      "checkpoint": "runs/stage18/checkpoints/CNN-F.pt",
      "estimator": "runs/stage18/training/E1-seed1/selected.pt",
      "checkpoint_sha256": "f883730e8df0798c07effbb1d51b05a646bea6f688b2a4bc74b9edf4ca104e8b",
      "estimator_sha256": "68dd5417b6682455c260669fd1d027a9c88b9b79e977a633b05eefe21db7cbbf"
    },
    {
      "name": "CNN-F-E1-rolling-seed2",
      "first_panel_name": "CNN-F-E1-rolling-seed2",
      "kind": "E1",
      "rolling": true,
      "seed": 2,
      "checkpoint": "runs/stage18/checkpoints/CNN-F.pt",
      "estimator": "runs/stage18/training/E1-seed2/selected.pt",
      "checkpoint_sha256": "f883730e8df0798c07effbb1d51b05a646bea6f688b2a4bc74b9edf4ca104e8b",
      "estimator_sha256": "f00b0e61f4711838771260d491561b98c13ece23a59013b42e02dc35d5c35af0"
    },
    {
      "name": "CNN-F-E1-rolling-seed3",
      "first_panel_name": "CNN-F-E1-rolling-seed3",
      "kind": "E1",
      "rolling": true,
      "seed": 3,
      "checkpoint": "runs/stage18/checkpoints/CNN-F.pt",
      "estimator": "runs/stage18/training/E1-seed3/selected.pt",
      "checkpoint_sha256": "f883730e8df0798c07effbb1d51b05a646bea6f688b2a4bc74b9edf4ca104e8b",
      "estimator_sha256": "2cb897095bd0947f93f437e57dd139d2aa9786da2047459ed3325326aa3307d6"
    },
    {
      "name": "CNN-F-E1-rolling-seed4",
      "first_panel_name": "CNN-F-E1-rolling-seed4",
      "kind": "E1",
      "rolling": true,
      "seed": 4,
      "checkpoint": "runs/stage18/checkpoints/CNN-F.pt",
      "estimator": "runs/stage18/training/E1-seed4/selected.pt",
      "checkpoint_sha256": "f883730e8df0798c07effbb1d51b05a646bea6f688b2a4bc74b9edf4ca104e8b",
      "estimator_sha256": "4019cf5fa1fdcdb46c308c15ac120820df8e4fe1bab6c3cb67818ac429fb177b"
    },
    {
      "name": "CNN-F-E1-rolling-seed5",
      "first_panel_name": "CNN-F-E1-rolling-seed5",
      "kind": "E1",
      "rolling": true,
      "seed": 5,
      "checkpoint": "runs/stage18/checkpoints/CNN-F.pt",
      "estimator": "runs/stage18/training/E1-seed5/selected.pt",
      "checkpoint_sha256": "f883730e8df0798c07effbb1d51b05a646bea6f688b2a4bc74b9edf4ca104e8b",
      "estimator_sha256": "296e1b28883aa63fd58eb89ea619e0586a97537e1c576b25d01d9266670cf972"
    },
    {
      "name": "CNN-F-meanF",
      "first_panel_name": "CNN-F-meanF",
      "arm": "meanF",
      "checkpoint": "runs/stage18/checkpoints/CNN-F.pt",
      "estimator": null,
      "checkpoint_sha256": "f883730e8df0798c07effbb1d51b05a646bea6f688b2a4bc74b9edf4ca104e8b",
      "estimator_sha256": null
    },
    {
      "name": "CNN-F-constantF",
      "first_panel_name": "CNN-F-constantF",
      "arm": "constantF",
      "checkpoint": "runs/stage18/checkpoints/CNN-F.pt",
      "estimator": null,
      "checkpoint_sha256": "f883730e8df0798c07effbb1d51b05a646bea6f688b2a4bc74b9edf4ca104e8b",
      "estimator_sha256": null
    },
    {
      "name": "CNN-F-permutedF",
      "first_panel_name": "CNN-F-permutedF",
      "arm": "permutedF",
      "checkpoint": "runs/stage18/checkpoints/CNN-F.pt",
      "estimator": null,
      "checkpoint_sha256": "f883730e8df0798c07effbb1d51b05a646bea6f688b2a4bc74b9edf4ca104e8b",
      "estimator_sha256": null
    },
    {
      "name": "CNN-F-E0-matched-seed2",
      "first_panel_name": null,
      "kind": "E0",
      "rolling": false,
      "seed": 2,
      "stored_index": 1,
      "checkpoint": "runs/stage19/L3_checkpoints/CNN-F-seed1/selected.pt",
      "estimator": "runs/stage18/training/E0-seed2/selected.pt",
      "checkpoint_sha256": "1c1e3a8c169cb1394fd01eb5237e49a198a82759f5be4f030ccfe57426e61e25",
      "estimator_sha256": "d461bae9dfd507b07955eda2342abe717900232af40cd5ac9e0b5981fb1fcd2f"
    },
    {
      "name": "CNN-F-E0-matched-seed3",
      "first_panel_name": null,
      "kind": "E0",
      "rolling": false,
      "seed": 3,
      "stored_index": 2,
      "checkpoint": "runs/stage19/L3_checkpoints/CNN-F-seed2/selected.pt",
      "estimator": "runs/stage18/training/E0-seed3/selected.pt",
      "checkpoint_sha256": "e22c5e78c6508eea9916e93b55e1494cca31fbc2c17349610cf340fdab4ab8b2",
      "estimator_sha256": "dc6fe8559093681cece7166443cd1a8d44bdf7f8e794e9f07bed42bf2bb876a3"
    },
    {
      "name": "CNN-F-E0-matched-seed4",
      "first_panel_name": null,
      "kind": "E0",
      "rolling": false,
      "seed": 4,
      "stored_index": 3,
      "checkpoint": "runs/stage19/L3_checkpoints/CNN-F-seed3/selected.pt",
      "estimator": "runs/stage18/training/E0-seed4/selected.pt",
      "checkpoint_sha256": "df39ee98a5e350f770eb684192fc819af985055eb6bf7c8d1c3b7d428cc87b78",
      "estimator_sha256": "fc538e434c04df7ffa91fa9021f9bb64c6006700b95262772b5e139e492a195b"
    },
    {
      "name": "CNN-F-E0-matched-seed5",
      "first_panel_name": null,
      "kind": "E0",
      "rolling": false,
      "seed": 5,
      "stored_index": 4,
      "checkpoint": "runs/stage19/L3_checkpoints/CNN-F-seed4/selected.pt",
      "estimator": "runs/stage18/training/E0-seed5/selected.pt",
      "checkpoint_sha256": "51a15aed19862c0c5d319346dbac5d9dc69de5420b86e24dc1a29b7e3f3a3500",
      "estimator_sha256": "6a7edd4aee91e81b7a272c6e9b2a7962e9a000ed44ab7378f478ad6657a38e2f"
    }
  ],
  "code_hashes": {
    "acd_stage19_part3b_contract.py": "0728290e9db1c4ca65d8dac5f2cb8804fb898c9a831dabe764e32cc57c532142",
    "acd_stage19_part3b_inference.py": "509c68f9705047443df929b3ea29000465c07b9586792e805c1dc501977465a2",
    "acd_stage19_part3b_score.py": "f61a892630f3d7dbec34e20b3ba386fc5913373fe618970ac9675dbbf5df4a4d",
    "acd_stage19_part3b_report.py": "98929e45793ca9dd3a1ea7f5f915f31cd0309200f9ccc9ca5b046ff184208d80",
    "acd_stage18_inference.py": "a6ea2847438a23a3290fa12c91535423413f31e8f3b3bd578d93735fa4a0fcb7",
    "acd_stage18_estimators.py": "3e3d00143ecd874a3680378870683c0ccc875c3badbb098202b222de05eee4bc",
    "acd_stage9_cnn.py": "3ca018b1dc35c5cb9734787e852240e7517d88007515692d27fd882f3c13d434",
    "acd_stage9_train.py": "9c36418c45ab0727d2c4294b96bed1102b85d65d269636f6c9b38e3573605269",
    "acd_stage19_inference.py": "591f6ce4989b19be4bbda36e6ffa39ecf34940bc513a1770e361b00ee1a7ef6d",
    "acd_stage19_learned.py": "9319e768f5d211472d6c52fe0b7c4cef975d878be242b14807a43178e7e85930",
    "acd_stage19_l3_statistic.py": "72da9641cfa8341a50b85514e42f0f15be1e5886e79348c9870c345cee5ce33b",
    "acd_stage19_score.py": "87e0bc98e9352fdc532f842ac2b5f2eb335eb9f8ba8d613045bcc428cef73ecd",
    "acd_stage13_analysis.py": "ffe50e4894aa97eb6de690abc996c1a8589ec8be926af0100f077b2220be289b",
    "acd_stage6_analysis.py": "c9fa8c1f9e211f8e7ea47ec63947bff3693258c738c377ce7874b425bba58cd8",
    "acd_stage9_receipts.py": "966a21bc72ef4b3c8ede354a1246fb5d01c4b3df440ef19902ec032a688b456c",
    "acd_stats.py": "1c97d51262a7546b70320c1207de554eff6f9b6a58b00428a2640f5ead6f685a",
    "acd_protocol.py": "160eabe8ccee07d0de17576a441b6fef1a93e1d5dbb68f2df9eb118a1eaad000",
    "acd_stage19_gpu_lease.py": "5e09e6e6284bfb35df35a9431400caf2936973f3819657f80659360f3f4fcadc",
    "acd_stage19_part2_gate.py": "518e5890d5ac88f210a47a304ae9fd7cb47986ff444b3d078dc13ffc76b1a001"
  },
  "references": {
    "CNN-F": "f883730e8df0798c07effbb1d51b05a646bea6f688b2a4bc74b9edf4ca104e8b",
    "CNN-noF": "4bfef787a80269dada0acd7ca74ef84eb6442a580c706a57333c55dc647b1f67"
  },
  "first_panel_receipt_hashes": {
    "acd_stage18_A.json": "07cc69061dc38ff45dc54164707c4a90cefc87cd97a867776e48e967aecea032",
    "acd_stage18_B.json": "6d958cef5b49fac5dbb0df455edd54635ddc07186dd7607c4d76becc997307c3"
  },
  "criteria": {
    "B1_alpha": 0.01,
    "B1_direction": "lower > 0",
    "B2_alpha": 0.05,
    "B2_upper_strictly_below": 0.05,
    "B2_harm": "realized D > 0",
    "B3_alpha": 0.05,
    "B3_direction": "one-sided lower > 0"
  },
  "inference_order": [
    "E0 fixed",
    "E1 fixed and rolling",
    "A diagnostics",
    "matched E0/CNN-F seeds"
  ],
  "no_preemption": true,
  "fresh_panel": true,
  "licenses_frozen_route": false
}
```
