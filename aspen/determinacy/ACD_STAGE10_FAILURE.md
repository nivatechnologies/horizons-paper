# Stage 10 discarded-run failure

The first response-weight sweep run is discarded. Its saved checkpoints are not evaluated. The second model did not start.

Model: CNN-F-resp-0.1. Last logged step: 9200; loss: 0.028024019673466682. Exception: RuntimeError: nonfinite loss.
Last measured GPU duration: 5841.136951338034 seconds. Charged discarded duration: 5847 seconds, deducted from this model’s cap in Stage 10b.

R-other: monotonic final runtime unavailable; charge ceil(last logged monotonic duration + progress-to-exception file-mtime gap + one second filesystem/logging allowance). This is conservative accounting, not an exact measured final GPU duration.

The failure log does not distinguish a diverging rollout from nonfinite gradients poisoning a later update. The previous trainer checked the loss but did not check the gradient norm before clipping and stepping. Finite retained checkpoints do not identify the failure mechanism.

| Checkpoint | SHA-256 |
|---|---|
| checkpoint_008000.pt | d36e59b2f0a80ef31e83e178b6bed70e56fa046b4e9408bd710b45233bef0f1b |
| checkpoint_009000.pt | 22ad0f4669c3f5db1fc1dccfb6868174713f6379b37579571634f4422119bf1a |
| selected.pt | d44335650d55def53206156bdbc4737ac3be1e0469ee0f84db6128436a44bee8 |

Evidence: receipts/acd_stage10_failure.json; Spark training_stage10.log and training/CNN-F-resp-0.1/progress.json.
