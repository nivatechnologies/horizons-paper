"""Durable single-phase runner on Spark, with explicit completion and failure records."""
import os
from pathlib import Path
import subprocess
import sys
import time

from common import ROOT,RUNS,write_json

PHASES={"reported":["prepare.py","reported-sensitivity"],"data":["data.py","all"],
        "nulls":["evaluate.py","nulls"],"law":["evaluate.py","law"],
        "train_L":["train.py","L_range-3"],"train_F":["train.py","FNO-theta"],
        "learned":["evaluate.py","learned"]}


if __name__=="__main__":
    phase=sys.argv[1]
    if phase not in PHASES:raise ValueError("unknown phase")
    out=RUNS/"phase_status"/f"{phase}.json"
    if out.exists():
        import json
        previous=json.loads(out.read_text())
        if previous["returncode"]==0:raise SystemExit(0)
    t=time.monotonic()
    write_json(RUNS/"phase_status"/f"{phase}_running.json",dict(phase=phase,pid=os.getpid()))
    argv=[sys.executable,"-u",str(ROOT/PHASES[phase][0]),*PHASES[phase][1:]]
    result=subprocess.run(argv,cwd=ROOT.parents[1])
    write_json(out,dict(phase=phase,pid=os.getpid(),returncode=result.returncode,seconds=time.monotonic()-t))
    raise SystemExit(result.returncode)
