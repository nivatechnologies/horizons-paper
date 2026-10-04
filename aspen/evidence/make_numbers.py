"""Extend inherited NUMBERS tables with AEA sections and a source/tamper checker."""
import argparse
import hashlib
import sys

from common import ROOT,RESULTS,REPO
sys.path.insert(0,str(REPO/"tokens_horizon/scripts"))
sys.path.insert(0,str(REPO/"tokens_horizon"))
import make_numbers as inherited

SECTIONS=[("AEA-C","chaos.csv","Every-point chaos gate"),
          ("AEA-G","sensitivity.csv","Fixed-lead centre sensitivity"),
          ("AEA-GP","reported_sensitivity.csv","Reported local gradients, not direction selectors"),
          ("AEA-E","errors.csv","Query errors and state bootstrap intervals"),
          ("AEA-R","ratios.csv","Endpoint ratios"),
          ("AEA-I","correlations.csv","Index against baseline predictors"),
          ("AEA-O","outcome.csv","Frozen outcome"),
          ("AEA-T","training.csv","Learned recipe and cost")]


def render():
    inherited.PKG=ROOT;inherited.SECTIONS.clear()
    out=["# NUMBERS — Aspen evidence alignment", "",
         "Generated from source tables; AEA sections use the inherited column/section checker. "
         "Unavailable values remain blank and satisfy no criterion. Source files and hashes are checked."]
    for sec,filename,title in SECTIONS:
        p=RESULTS/filename
        if not p.exists():continue
        rows,sha=inherited.read_csv(p)
        if not sha:raise inherited.NumbersError(f"{sec}: empty source SHA")
        if any(not r.get("label") for r in rows):raise inherited.NumbersError(f"{sec}: unlabelled row")
        cols=[c for c in rows[0] if c!="label"]
        inherited.table(out,sec,title,p,cols,rows,sha)
        out.append("\nSource SHA256: `"+hashlib.sha256(p.read_bytes()).hexdigest()+"`")
    if not inherited.SECTIONS:raise inherited.NumbersError("No AEA data sections")
    return "\n".join(out)+"\n"


if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--check",action="store_true");a=p.parse_args()
    expected=render();target=ROOT/"NUMBERS.md"
    if a.check:
        if not target.exists() or target.read_text()!=expected:
            raise inherited.NumbersError("AEA NUMBERS mismatch with source tables")
        print("AEA NUMBERS checker: zero mismatches")
    else:target.write_text(expected)
