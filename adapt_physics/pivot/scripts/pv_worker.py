"""Tiny GPU job queue for the pivot runs. Each worker (one per GPU) repeatedly claims, under a file lock, the first
unclaimed job whose dependency files all exist, runs it with CUDA device substituted for {dev}, and records the exit
code. Jobs file lines: `name | dep1 dep2 ... | command with {dev}`. Stops when every job is claimed; gives up after a
timeout (8 h) if the remaining jobs' dependencies never appear. State: <jobs>.state.json (claims and exit codes).

Usage: python pivot/scripts/pv_worker.py <jobs file> <device> [lifetime hours, default 8]
"""
import fcntl
import json
import subprocess
import sys
import time
from pathlib import Path


def main(jobs_file, dev, hours=8.0):
    jobs_file = Path(jobs_file)
    state_file = jobs_file.with_suffix(".state.json")
    lock = jobs_file.with_suffix(".lock")
    t_end = time.time() + float(hours) * 3600
    while time.time() < t_end:
        job = None
        with open(lock, "w") as lk:
            fcntl.flock(lk, fcntl.LOCK_EX)
            state = json.loads(state_file.read_text()) if state_file.exists() else {}
            lines = [l.strip() for l in jobs_file.read_text().splitlines() if l.strip() and not l.startswith("#")]
            pending = 0
            for l in lines:
                name, deps, cmd = [x.strip() for x in l.split("|", 2)]
                if name in state:
                    continue
                pending += 1
                if all(Path(d).exists() for d in deps.split()):
                    job = (name, cmd.replace("{dev}", dev))
                    state[name] = dict(device=dev, start=time.time())
                    state_file.write_text(json.dumps(state, indent=1))
                    break
        if job is None:
            if pending == 0:
                print(dev, "no jobs left", flush=True)
                return
            time.sleep(30)
            continue
        name, cmd = job
        print(time.strftime("%H:%M:%S"), dev, "start", name, flush=True)
        rc = subprocess.run(cmd, shell=True, env={**__import__("os").environ, "PYTHONDONTWRITEBYTECODE": "1"}).returncode
        with open(lock, "w") as lk:
            fcntl.flock(lk, fcntl.LOCK_EX)
            state = json.loads(state_file.read_text())
            state[name].update(end=time.time(), rc=rc)
            state_file.write_text(json.dumps(state, indent=1))
        print(time.strftime("%H:%M:%S"), dev, "done", name, "rc", rc, flush=True)
    print(dev, "timeout", flush=True)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else 8.0)
