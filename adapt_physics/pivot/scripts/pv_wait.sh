#!/bin/bash
# pv_wait.sh <file> [<file> ...] -- <command ...>: wait (6 h timeout) until every file exists, then run the command.
# Waits on files only (never pgrep -f, which self-matches).
files=(); while [ "$1" != "--" ]; do files+=("$1"); shift; done; shift
end=$(( $(date +%s) + 21600 ))
for f in "${files[@]}"; do until [ -e "$f" ]; do [ $(date +%s) -ge $end ] && { echo "timeout waiting for $f"; exit 2; }; sleep 30; done; done
PYTHONDONTWRITEBYTECODE=1 "$@"
