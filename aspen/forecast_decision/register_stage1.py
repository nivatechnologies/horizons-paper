"""Register coordinator-checked Stage1 numbers and mandatory gate-summary."""
import copy,json
from pathlib import Path
from protocol import ROOT,write_json,digest
from check_campaign import verify
from result_note import stage1_note
def main():
    cases=json.loads((ROOT/"runs/stage1_cases.json").read_text())
    reading=json.loads((ROOT/"runs/stage1_reading.json").read_text())
    checked=verify(cases,reading)
    bad=copy.deepcopy(reading);bad["primary"]["gap"]+=.01
    # primary aliases are not shared after JSON load; tamper must fail primary/lead consistency.
    try:verify(cases,bad)
    except (AssertionError,ValueError):pass
    else:raise AssertionError("tampered gate number was not rejected")
    bad=copy.deepcopy(reading);bad["primary"]["arms"]["CNN-20k"]["wACC"]=float("nan")
    try:verify(cases,bad)
    except (AssertionError,ValueError):pass
    else:raise AssertionError("NaN was not rejected")
    checked.update(tamper_rejected=True,NaN_rejected=True)
    write_json(ROOT/"runs/stage1_checker_registered.json",checked)
    prefix=(ROOT/"NUMBERS.md").read_text().split("\n## AFD_STAGE1_READING")[0]
    section="\n## AFD_STAGE1_READING\n\nMeasured case/panel reading; no licensed sentence. Source: runs/stage1_reading.json, checked from runs/stage1_cases.json.\n\n"
    section+="\u0060\u0060\u0060json\n"+json.dumps(reading,indent=2,allow_nan=False)+"\n\u0060\u0060\u0060\n"
    section+="\n## AFD_STAGE1_CHECKER\n\n"+json.dumps(checked,sort_keys=True)+"\n"
    section+="\n| Artifact | SHA256 |\n|---|---|\n"
    for name in ["stage1_reading.json","stage1_cases.json","stage1_checker_registered.json"]:
        section+=f"| runs/{name} | {digest(ROOT/'runs'/name)} |\n"
    (ROOT/"NUMBERS.md").write_text(prefix+section)
    assert json.loads((ROOT/"NUMBERS.md").read_text().split("\u0060\u0060\u0060json\n")[-1].split("\n\u0060\u0060\u0060")[0])==reading
    note=stage1_note(reading,checked)
    r=reading["primary"]
    note+="\nHeadline value now, against the threshold: gap "+str(r["gap"])+" versus required0.15; lower bound "+str(r["lower95"])+" versus required0.10. Neither PASS condition clears. Upper bound exceeds0.05, so this is not KILL.\n"
    note+="\nWhat changed since the last gate: Amendment1 resolved the window halt; fresh truth and baseline evaluation now exist.\n"
    note+="\nLargest remaining risk to the so-what test: the fresh baseline gap is below the precommitted counterexample threshold; repair/strongest-incumbent outcomes are not known.\n"
    note+="\nCoordinator would: go to Stage2 under WO§9, because an otherwise reading explicitly authorizes continuation. No headline sentence is licensed. Stage2b truth still requires the sampler go.\n"
    note+="\nNUMBERS checker PASS; tampered finite number and NaN both rejected. Raw truth eligibility was also checked on sulaco (runs/stage1_checker.json).\n"
    (ROOT/"AFD_STAGE1_READING.md").write_text(note)
    print(note)
if __name__=="__main__":main()

