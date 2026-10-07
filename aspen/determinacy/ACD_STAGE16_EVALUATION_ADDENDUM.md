# Stage 16 evaluation addendum

Post hoc on confirmation; licenses no frozen route. Training, seeds, data, optimizer updates, checkpoint selection and inference are unchanged. Matched coverage now uses the committed Stage 15A ranking and its corrected exact-count rule. No outcome participates in ranking. The complete fixed contract is in receipts/acd_stage16_coverage_contract.json.

The coverage adapter passes the full frozen null probability array to the existing summaries function, which performs its own question selection. Passing an already selected array would index it a second time. This coverage-only error was corrected before any new-seed coverage scoring.

Code hashes:

{
  "acd_stage16_metrics.py": {
    "frozen_sha256": "7b86814a7e4dc3b0bf8892f8e319c8b9bff1608ff4bb24363ad563937307b7c6",
    "current_sha256": "86d5885c3ce15715740c241199281f16984a6f4daa17fcb5f828de066c0e3b5e"
  },
  "acd_stage16_coverage.py": {
    "frozen_sha256": null,
    "current_sha256": "ff32f1a24e8d88b2a2849ce9f70bf994605f8956063ce82333b75815c65b4a6f"
  }
}
