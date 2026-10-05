"""Read-only Step 0 measurements; no panel, model rollout, or training."""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import numpy as np
import torch

HERE = Path(__file__).resolve().parent
BASE = Path("/mnt/niva-array/horizons-paper")
SOURCE = BASE / "aspen/horizon"
SHA = "1cd0ab701b5e663eb7e0304b1d705ddeabe80617"

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def measure():
    # Source checkout remains untouched; avoid import bytecode and model initialization.
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(SOURCE))
    from common import patterns, NAMESPACES
    cal = json.loads((SOURCE / "results/l96_calibration.json").read_text())
    training = json.loads((SOURCE / "runs/l96/learned/training.json").read_text())
    checkpoint = torch.load(SOURCE / "runs/l96/learned/checkpoint.pt",
                            map_location="cpu", weights_only=True)
    lt = 1 / cal["system"]["lambda_mean"]
    windows = []
    for lead in [0, 1, 1.5, 2, 2.5, 3, 4, 6]:
        ticks = np.arange(0, 200, dtype=np.int64)
        # Execute the exact predicates in l96.rollout and neural cost accumulation.
        t = ticks * .05
        old = ticks[(t >= lead*lt - 1e-12) & (t <= (lead+1)*lt + 1e-12)]
        new = list(range(int(np.rint(lead*lt/.05)),
                         int(np.rint((lead+1)*lt/.05))+1))
        windows.append(dict(lead_LT=lead, code_indices=old.tolist(),
                            wo_indices=new, same=old.tolist()==new))
    files = ["runs/l96/learned/checkpoint.pt", "runs/l96/test/climatology.npy",
             "runs/l96/test/climatology.json", "runs/l96/learned/training.json",
             "results/l96_calibration.json", "common.py", "l96.py",
             "train_l96.py", "evaluate_l96.py", "evaluate_l96_neural.py",
             "analyze_l96.py", "enrich_l96.py", "profile_l96.py",
             "climatology_l96.py", "learned_l96_data.py",
             "AAH_FREEZE.md", "AAH_FREEZE_CALIBRATION_L96.md"]
    return dict(source_sha=SHA, status="HALT_SCIENTIFIC_MISMATCH",
                LT=lt, sigma=cal["system"]["sigma"],
                parameter_count=sum(x.numel() for x in checkpoint["state_dict"].values()),
                checkpoint_step=checkpoint["step"], training_updates=training["steps_done"],
                training_seconds_recorded=training["seconds"],
                gpu_time_recorded=False,
                pattern_rms=np.sqrt(np.mean(patterns(0)**2, axis=1)).tolist(),
                namespaces=NAMESPACES, windows=windows,
                hashes={name:digest(SOURCE/name) for name in files},
                wo_sha256=digest(HERE/"WO_v5.1.md"))

def validate(actual, expected):
    assert actual == expected, "preflight evidence mismatch"
    assert actual["parameter_count"] == 999681
    assert actual["checkpoint_step"] == 20000
    assert np.allclose(actual["pattern_rms"], 1., rtol=0, atol=1e-14)
    assert not next(w for w in actual["windows"] if w["lead_LT"]==2)["same"]
    # NaN cannot silently survive the record/comparison.
    json.dumps(actual, allow_nan=False)

def render_numbers(data):
    lines = ["# NUMBERS", "", "## AFD_STEP0", "",
             "Read-only measurements of retained AAH artifacts and exact code predicates.",
             "No AFD scientific outcomes exist. Source SHA: "+data["source_sha"], "",
             "| Key | Value |", "|---|---|"]
    for key in ["status", "LT", "sigma", "parameter_count", "checkpoint_step",
                "training_updates", "training_seconds_recorded", "gpu_time_recorded"]:
        lines.append(f"| {key} | {data[key]} |")
    lines += ["", "## AFD_WINDOWS", "", "Derived from measured LT; indices are zero-based output ticks.",
              "", "| Lead (LT) | Existing code indices | WO indices | Equal |", "|---|---|---|---|"]
    for w in data["windows"]:
        lines.append(f"| {w['lead_LT']} | {w['code_indices'][0]}–{w['code_indices'][-1]} | {w['wo_indices'][0]}–{w['wo_indices'][-1]} | {w['same']} |")
    lines += ["", "## AFD_HASHES", "", "| Artifact | SHA256 |", "|---|---|"]
    lines += [f"| {k} | {v} |" for k,v in data["hashes"].items()]
    lines += [f"| WO_v5.1.md | {data['wo_sha256']} |",
              "", "## AFD_ACTIONS", "",
              "Measured RMS values: "+json.dumps(data["pattern_rms"]),
              "", "## AFD_SEEDS", "", "Retained namespace IDs: "+json.dumps(data["namespaces"],sort_keys=True), ""]
    return "\n".join(lines)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args=parser.parse_args()
    measured=measure()
    if args.write:
        (HERE/"step0_evidence.json").write_text(json.dumps(measured,indent=2,allow_nan=False)+"\n")
        (HERE/"NUMBERS.md").write_text(render_numbers(measured))
    stored=json.loads((HERE/"step0_evidence.json").read_text())
    validate(stored, measured)
    assert (HERE/"NUMBERS.md").read_text().startswith(render_numbers(measured)), "preflight NUMBERS mismatch"
    bad=copy.deepcopy(stored)
    bad["parameter_count"]+=1
    try:
        validate(bad, measured)
    except AssertionError:
        pass
    else:
        raise AssertionError("tampered record was not rejected")
    print("AFD preflight checker PASS; NUMBERS matches; tamper rejected. No data generated.")

if __name__=="__main__":
    main()
