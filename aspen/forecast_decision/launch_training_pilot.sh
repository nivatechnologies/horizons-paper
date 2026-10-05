#!/usr/bin/env bash
set -euo pipefail
task_root=/mnt/niva-array/work/aspen-forecast-decision-20261005/aspen/forecast_decision
/usr/bin/python3 - "$task_root/runs/training/closure_control.json" <<'PY'
import json,sys
from pathlib import Path
p=Path(sys.argv[1])
if p.exists() and not json.loads(p.read_text()).get('pilot_allowed',True):
    raise SystemExit('WO Section19 closure: pilot launch prohibited')
PY
exec /home/todd/.local/bin/bwrap \
  --ro-bind / / --proc /proc --dev-bind /dev /dev \
  --tmpfs /mnt --tmpfs /home --tmpfs /tmp --dir /tmp/worker \
  --ro-bind "$task_root/runs/training_pilot/source" /tmp/worker/source \
  --ro-bind "$task_root/runs/training_data2" /tmp/worker/data \
  --bind "$task_root/runs/training_pilot" /tmp/worker/out \
  --ro-bind /mnt/niva-array/horizons-paper/.venv /tmp/venv \
  --unsetenv PYTHONPATH --setenv CUDA_VISIBLE_DEVICES 1 \
  --chdir /tmp/worker/source \
  -- /tmp/venv/bin/python train.py --name CNN2-roll \
     --data /tmp/worker/data --out /tmp/worker/out --microbatch 64 --pilot-updates 100
