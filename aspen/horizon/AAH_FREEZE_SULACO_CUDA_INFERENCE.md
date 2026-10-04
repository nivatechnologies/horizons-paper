# Sulaco CNN inference execution amendment

The machine assignment remains sulaco for Lorenz-96. After31 preliminary CPU cases, a read-only hardware check found an idle RTX2000 Ada with about8GB free alongside existing services. Those services remain running.

A synthetic architecture-only benchmark, without observations, test costs or accuracy, measured the full2048-action/member batch at0.0374333 seconds on CUDA versus0.564231 seconds in the prior CPU benchmark. Peak tensor allocation0.253542GiB. One-step synthetic CPU/GPU maximum absolute difference2.384185791015625e-7. These are execution diagnostics, not scientific performance or proof of long-rollout equality. No test accuracy or response scores were examined to choose the backend.

Run **all200 learned cases afresh on this one GPU backend**. Preserve preliminary CPU arrays/logs in runs/l96/neural_cpu_preliminary; do not pool CPU and GPU outputs or choose a backend by its scientific results. Keep the exact completed20000-step training checkpoint selected by the original validation rule, original windows/seeds/actions, all256 nested members, output times, cost formula, all-action21LT stability drops and thresholds.

Inference remains float32; TF32 is explicitly disabled for CUDA matmul and CuDNN, and deterministic CuDNN is enabled. CPU host threads1. Report actual device, threads, checkpoint and source per case. The earlier CPU64-thread inference layout is superseded solely to reduce measured runtime on the assigned machine. Primary physical-arm data, Tf/Td/M95 readings and every criterion remain unchanged. Unstable members and unavailable statistics retain their existing failures; no refit or rescue.
