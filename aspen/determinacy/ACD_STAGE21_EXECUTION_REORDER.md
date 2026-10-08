# Stage21 execution reorder

Todd authorized this change to execution order and hardware paths. G1, G2 and R1–R4 retain every frozen definition, population, threshold, bound type and pass criterion. Reference scoring runs immediately on CPU. The existing scoring code creates the realized cache if absent; no emulator is required.

L3 and Part3b keep their existing priority. Stage21 then runs constant-eight CNN-F, P0 seeds and retained CNN-noF first, all on Baccus 170HX, and publishes R1/R2 as soon as their hashed outputs are complete. P1 fixed and rolling for all E1 seeds next run together on one Spark after its current Stage20 queue finishes; R3/R4 are published separately. Descriptive arms run last. Stage18 D/C is released only after every Stage21 inference phase has finished. No existing GPU job is preempted.

The original Freeze E documents remain unchanged. This explicitly supersedes their single-hardware execution arrangement for R3/R4, as authorized by Todd; the two compared arms and all E1 seeds share one Spark hardware path. Frozen rollout/scoring source files stay unchanged. New adapters, phases and hashes:

```json
{
  "utc": "2026-10-08T08:31:09.986157+00:00",
  "authorization": "Todd: reorder under the existing freezes; no criteria change. Score G1/G2 immediately on CPU; R1/R2 first on 170HX, R3/R4 fixed/rolling all seeds together on one Spark when Stage20 frees it; descriptive arms last; Stage18 D/C after Stage21 inference.",
  "criteria_unchanged": true,
  "original_freeze_sha256": "3d4ad539fb02c862b311ebf847cf0878d01c982862e0b1eb71dcf80e2c1c5185",
  "amendment_sha256": "3340d504d053e6ca2f7a5b1ba5cfd02838e361a38cebeace9bac4dd6ce8f637c",
  "reference": "CPU now; no emulator prerequisite; frozen acd_stage6_analysis.calibration/loss and acd_stage21_score.score_actual unchanged",
  "R12": {
    "hardware": "Baccus 170HX",
    "tasks": [
      "CNN-F-constantF",
      "CNN-F-E0-fixed-seed1",
      "CNN-F-E0-fixed-seed2",
      "CNN-F-E0-fixed-seed3",
      "CNN-F-E0-fixed-seed4",
      "CNN-F-E0-fixed-seed5",
      "CNN-noF"
    ]
  },
  "R34": {
    "hardware": "Spark1 GB10, 192.168.88.4; all compared E1 fixed and rolling seeds on the same path",
    "tasks": [
      "CNN-F-E1-fixed-seed1",
      "CNN-F-E1-fixed-seed2",
      "CNN-F-E1-fixed-seed3",
      "CNN-F-E1-fixed-seed4",
      "CNN-F-E1-fixed-seed5",
      "CNN-F-E1-rolling-seed1",
      "CNN-F-E1-rolling-seed2",
      "CNN-F-E1-rolling-seed3",
      "CNN-F-E1-rolling-seed4",
      "CNN-F-E1-rolling-seed5"
    ]
  },
  "descriptive_tasks": [
    "CNN-F-ownF",
    "CNN-F-meanF",
    "CNN-20k",
    "CNN-F-seed1",
    "CNN-F-seed2",
    "CNN-F-seed3",
    "CNN-F-seed4",
    "CNN-noF-seed1",
    "CNN-noF-seed2",
    "CNN-noF-seed3",
    "CNN-noF-seed4"
  ],
  "still_ahead_of_stage21": [
    "L3 inference",
    "Part3b inference"
  ],
  "after_stage21": [
    "Stage18 D",
    "Stage18 C"
  ],
  "code_hashes": {
    "acd_stage21_priority.py": "11011459b020e82cd72c50a8362a05d81a8c0e8cf5fe9bed3ec555d2ca69cca8",
    "acd_stage21_reference.py": "4f9380c037c309f1d1f9700db44232f6b9965550f9bebd77535fcf65ac8da1cb",
    "acd_stage21_spark.py": "58f5143b630b4ae1ed8e18ea0ec22d985bc37208f56e975aee40bcbafef31a5d"
  },
  "publication": "Reference, R1/R2, R3/R4 and descriptive phases each pushed separately; manifests precede scoring; immutable per-phase receipts preserve registry values",
  "realized_outcome_accesses": [],
  "fresh_outputs_before_reorder": []
}
```
