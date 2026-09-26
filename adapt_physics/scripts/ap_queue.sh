#!/bin/bash
# Wait (with timeout) for a condition file, then run an eval. Usage: ap_queue.sh <device> <Re> <wait_file|model:NAME> <arms...>
# Never waits on process names (pgrep -f self-matches); waits on files with a 6 h timeout.
dev=$1; re=$2; cond=$3; shift 3
P=../.venv/bin/python
end=$(( $(date +%s) + 21600 ))
if [[ $cond == model:* ]]; then
  m=${cond#model:}
  until [ -f runs/train/$m/info.json ] && [ ! -f runs/train/$m/running ]; do [ $(date +%s) -ge $end ] && exit 2; sleep 30; done
else
  until [ -f "$cond" ]; do [ $(date +%s) -ge $end ] && exit 2; sleep 30; done
fi
PYTHONDONTWRITEBYTECODE=1 $P scripts/ap_eval.py $re $dev "$@"
