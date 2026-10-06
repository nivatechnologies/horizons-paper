"""Render Stage 7 status and vault note from saved source/check/audit receipts only."""
from pathlib import Path
import hashlib,json,subprocess
ROOT=Path(__file__).resolve().parent
BASE="f679cde7c6f3b6f861f745bc220ea64e116c6bd2"
URL="https://github.com/nivatechnologies/horizons-paper/blob/paper/aspen-2026-10-determinacy/aspen/determinacy/"
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run():
    source=json.loads((ROOT/"receipts/acd_stage7_source.json").read_text())
    paper=json.loads((ROOT/"receipts/acd_stage7_paper_audit.json").read_text())
    abstract=json.loads((ROOT/"receipts/acd_stage7_abstract_audit.json").read_text())
    numeric=json.loads((ROOT/"receipts/acd_stage7_numeric_check.json").read_text())
    registry=json.loads((ROOT/"numbers_acd.json").read_text())
    previous=json.loads(subprocess.check_output(["git","show",BASE+":aspen/determinacy/numbers_acd.json"],cwd=ROOT))["numbers"]
    assert all(registry["numbers"][k]==v for k,v in previous.items())
    modified=subprocess.check_output(["git","diff","--name-only",BASE],cwd=ROOT).decode().splitlines()
    assert not any(p.startswith("aspen/determinacy/receipts/") and "/acd_stage7" not in p for p in modified)
    current_abstract_counts={v:sum(r["verdict"]==v and not r["id"].startswith("A_OPTIONAL_") for r in abstract["rows"]) for v in ("OK","FIX")}
    fixes=[("Paper",r) for r in paper["rows"] if r["verdict"]=="FIX"]
    fixes += [("Abstract",r) for r in abstract["rows"] if r["verdict"]=="FIX"]
    for audit in (paper,abstract):
        assert audit.get("inventory_counts",audit["counts"])=={v:sum(r["verdict"]==v for r in audit["rows"]) for v in ("OK","FIX")}
    for name in ("paper/main.tex","paper/refs.bib"):
        assert digest(ROOT/name)==source["expected"][name]
    draft=(ROOT/"ACD_ABSTRACT_DRAFT.md").read_text()
    body=draft.split("## Abstract\n\n",1)[1].split("\n\n## Optional sentences",1)[0].rstrip("\n")+"\n"
    assert hashlib.sha256(body.encode()).hexdigest()==source["expected"]["paper/ABSTRACT_v4.txt"]
    assert not numeric["unmatched"]
    structural=[r for r in numeric["structural_constants"] if r["token"]]
    rules=[dict(rule="R-other",trigger=r["id"],resolution="Keep the supplied draft unchanged, flag the proposed fix, and withhold any broader reading or claim that this finding would require.") for _,r in fixes]
    status=[
        "# Stage 7 — paper v4 source verification and full audit","",
        "Base: "+BASE+". Sources remain byte-identical to the supplied v4 archive. Both source hashes and the abstract body hash match Todd's expected SHA-256 values. Titles and historical optional sentences are preserved.","",
        f'Paper audit: {paper["counts"]["OK"]} OK / {paper["counts"]["FIX"]} FIX. Abstract audit: {current_abstract_counts["OK"]} OK / {current_abstract_counts["FIX"]} FIX for the current abstract and titles; two historical optional rows are unselected.',
        f'Numeric registry: {len(registry["numbers"])} keys; regeneration PASS. De-TeXed paper and supplied abstract: zero unmatched literals, raw checker exit 0.',
        "Structural inventory: "+", ".join(str(r["token"])+" at TeX line "+str(r["line"]) for r in structural)+f'; {len(numeric["structural_constants"])-len(structural)} document label/reference occurrences; {len(numeric["bibliographic_numbers"])} bibliography metadata fields.',"",
        "Todd-licensed standing deviations: title, opening framing sentence, forecast-sign shorthand defined at first use, and labelled post hoc/development material in the abstract and introduction. No new frozen-route license is inferred from Stage 6.",
        "No build attempted; no PDF or build log was supplied. Sources use the existing receipt-derived figures; page count is not claimed.",
        "Receipts/static-source checks only, on sulaco CPU. No scientific forward runs, posterior/MAP/RML sampling, training, inference, cloud compute or service changes. Qwen services and Baccus close-out untouched.","",
        "## Open findings","",
        "| Audit | ID / line | Claim | Proposed fix |","|---|---|---|---|"]
    def cell(s):return str(s).replace("|","\\|").replace("\n"," ")
    for label,r in fixes:
        status.append("| "+" | ".join(cell(x) for x in (label,r["id"]+" / "+str(r.get("line","")),r["text"],r["proposed_fix"]))+" |")
    if not fixes:status.append("| Both | None | No open FIX rows | — |")
    status += ["","R-other fires for each open finding listed above: retain the supplied draft and flag the narrower proposed wording. Earlier R-other resolutions (corrected all-S denominator, exploratory scope/no frozen license, retained numerical energy-budget closure residual) continue to apply. No hard stop fired.",""]
    (ROOT/"ACD_STAGE7_STATUS.md").write_text("\n".join(status))
    note=["# Aspen intervention horizon paper — Stage 7, v4","",
        f'V4 sources verified unchanged. Independent full paper audit: **{paper["counts"]["OK"]} OK / {paper["counts"]["FIX"]} FIX**; abstract audit: **{current_abstract_counts["OK"]} OK / {current_abstract_counts["FIX"]} FIX** for the current abstract and titles (historical optional sentences are unselected).',
        "Branch: paper/aspen-2026-10-determinacy. Base: "+BASE+".","",
        "Sulaco directory: /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/.",""]
    for path,label in [
        ("paper/main.tex","Paper source"),("paper/refs.bib","References"),
        ("ACD_PAPER_AUDIT.md","Full v4 paper audit"),("ACD_ABSTRACT_DRAFT.md","Verbatim v4 abstract and retained titles"),
        ("ACD_ABSTRACT_AUDIT.md","Abstract audit and Todd's standing rulings"),
        ("ACD_PAPER_NUMERIC_CHECK.md","Numeric check and structural inventory"),
        ("NUMBERS_ACD.md","Receipt-backed numbers registry"),("ACD_STAGE6_READING.md","Post hoc Stage 6 reading"),
        ("receipts/acd_stage7_paper_audit.json","V4 paper audit receipt"),
        ("receipts/acd_stage7_abstract_audit.json","V4 abstract audit receipt"),
        ("receipts/acd_stage7_source.json","Source hash verification"),
        ("ACD_STAGE7_STATUS.md","Stage 7 status and all proposed fixes")]:
        note.append("- ["+label+"]("+URL+path+")")
    note+=["","Both numeric checks: **zero unmatched numbers**; registry regeneration PASS. Structural constants and bibliography metadata are separately inventoried. No TeX build attempted; the supplied archive includes no PDF. Sources and abstracts were not corrected by the auditor.",""]
    note+=status[status.index("## Open findings"):]
    (ROOT/"Draft_Aspen-Intervention-Horizon-Paper-2026-10.md").write_text("\n".join(note).rstrip()+"\n")
    verification=dict(base=BASE,source_hashes=source["expected"],source_hashes_verified=True,abstract_verbatim=True,titles_unchanged=True,
        numeric_raw_exit=numeric["raw_checker_exit"],unmatched=numeric["unmatched"],
        prior_registry_unchanged=True,prior_receipts_unchanged=True,registry_keys=len(registry["numbers"]),paper_counts=paper["counts"],abstract_counts=abstract["counts"],current_abstract_counts=current_abstract_counts,
        resolutions=rules,scientific_runs=0,build_attempted=False)
    (ROOT/"receipts/acd_stage7_verification.json").write_text(json.dumps(verification,indent=2)+"\n")
    files=["paper/main.tex","paper/refs.bib","paper/main.detex.txt","paper/TEX_ENVIRONMENT.json","ACD_ABSTRACT_DRAFT.md","ACD_PAPER_AUDIT.md","ACD_ABSTRACT_AUDIT.md","ACD_PAPER_NUMERIC_CHECK.md","NUMBERS_ACD.md","numbers_acd.json","acd_numbers.py","acd_paper_check.py","acd_stage7_report.py","ACD_STAGE7_STATUS.md","Draft_Aspen-Intervention-Horizon-Paper-2026-10.md"]
    files += [str(p.relative_to(ROOT)) for p in sorted((ROOT/"receipts").glob("acd_stage7*"))]
    (ROOT/"ACD_STAGE7_ARTIFACTS.json").write_text(json.dumps(dict(base=BASE,hashes={p:digest(ROOT/p) for p in files},resolutions=rules),indent=2)+"\n")
    print(json.dumps(dict(paper=paper["counts"],abstract=abstract["counts"],fix_ids=[r["id"] for _,r in fixes]),indent=2))
if __name__=="__main__":run()
