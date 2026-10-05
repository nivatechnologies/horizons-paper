#!/usr/bin/env bash
set -euo pipefail
task_root=/mnt/niva-array/work/aspen-forecast-decision-20261005/aspen/forecast_decision
/usr/bin/python3 - "$task_root/runs/training/closure_control.json" <<'PY'
import json,sys
from pathlib import Path
p=Path(sys.argv[1])
if p.exists() and not json.loads(p.read_text()).get('new_training_launches',True):
    raise SystemExit('WO Section19 closure: new training launch prohibited')
PY
model_name=$1
gpu_index=$2
microbatch=$3
data_dir=training_data
if [[ "$model_name" == CNN2-* ]]; then data_dir=training_data2; fi
mkdir -p "$task_root/runs/training/$model_name"
mkdir -p "$task_root/runs/training/$model_name/source"
for source_file in models.py protocol.py train.py; do
  cp "$task_root/$source_file" "$task_root/runs/training/$model_name/source/$source_file"
done
sha256sum "$task_root/runs/training/$model_name/source/"*.py > "$task_root/runs/training/$model_name/launch_source_hashes.txt"
date -u +%Y-%m-%dT%H:%M:%SZ > "$task_root/runs/training/$model_name/launched_at.txt"
exec /home/todd/.local/bin/bwrap \
  --ro-bind / / --proc /proc --dev-bind /dev /dev \
  --tmpfs /mnt --tmpfs /home --tmpfs /tmp --dir /tmp/worker \
  --ro-bind "$task_root/runs/training/$model_name/source" /tmp/worker/source \
  --ro-bind "$task_root/runs/$data_dir" /tmp/worker/data \
  --bind "$task_root/runs/training/$model_name" /tmp/worker/out \
  --ro-bind /mnt/niva-array/horizons-paper/.venv /tmp/venv \
  --unsetenv PYTHONPATH --setenv CUDA_VISIBLE_DEVICES "$gpu_index" \
  --chdir /tmp/worker/source \
  -- /tmp/venv/bin/python train.py --name "$model_name" \
     --data /tmp/worker/data --out /tmp/worker/out --microbatch "$microbatch"
