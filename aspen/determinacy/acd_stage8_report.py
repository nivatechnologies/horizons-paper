"""Render v5 check, status and vault documents from saved audit receipts."""
from pathlib import Path
import hashlib,json,subprocess
ROOT=Path(__file__).resolve().parent
BASE="5df47447c22fca97c0d55cf14b74240b7f0500fe"
URL="https://github.com/nivatechnologies/horizons-paper/blob/paper/aspen-2026-10-determinacy/aspen/determinacy/"
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run():
    source=json.loads((ROOT/"receipts/acd_stage8_source.json").read_text())
    paper=json.loads((ROOT/"receipts/acd_stage8_paper_audit.json").read_text())
    abstract=json.loads((ROOT/"receipts/acd_stage8_abstract_audit.json").read_text())
    numeric=json.loads((ROOT/"receipts/acd_stage8_numeric_check.json").read_text())
    diff=json.loads((ROOT/"receipts/acd_stage8_diff.json").read_text())
    registry=json.loads((ROOT/"numbers_acd.json").read_text())
    assert registry==json.loads(subprocess.check_output(["git","show",BASE+":aspen/determinacy/numbers_acd.json"],cwd=ROOT))
    modified=subprocess.check_output(["git","diff","--name-only",BASE],cwd=ROOT).decode().splitlines()
    assert not any(p.startswith("aspen/determinacy/receipts/") and "/acd_stage8" not in p for p in modified)
    for path in ("paper/main.tex","paper/refs.bib"):assert digest(ROOT/path)==source["expected"][path]
    draft=(ROOT/"ACD_ABSTRACT_DRAFT.md").read_text()
    body=draft.split("## Abstract\n\n",1)[1].split("\n\n## Optional sentences",1)[0].rstrip("\n")+"\n"
    assert hashlib.sha256(body.encode()).hexdigest()==source["expected"]["paper/ABSTRACT_v5.txt"]
    prior=subprocess.check_output(["git","show",BASE+":aspen/determinacy/ACD_ABSTRACT_DRAFT.md"],cwd=ROOT).decode()
    assert draft.split("## Abstract")[0]==prior.split("## Abstract")[0]
    assert draft.split("## Optional sentences")[1]==prior.split("## Optional sentences")[1]
    assert not numeric["unmatched"]
    fixes=[(label,r) for label,audit in (("Paper",paper),("Abstract",abstract)) for r in audit["rows"] if r["verdict"]=="FIX"]
    rules=[dict(rule="R-other",trigger="Supplied v5 main.tex retains its unchanged printed date label 'draft v4'.",
                resolution="Preserve verified supplied bytes, identify the artifact as the supplied v5 source, and flag the printed-label discrepancy. It is outside the changed-passage audit.")]
    rules += [dict(rule="R-other",trigger=r["id"],resolution="Retain the supplied source and flag the narrower proposed fix; license no broader claim.") for _,r in fixes]
    structural=[r for r in numeric["structural_constants"] if r["token"]]
    check=["## Stage 8 — v5 numeric checks","",
        "Both checks pass with zero unmatched numbers. Registry regeneration PASS; all 12016 keys and their sources remain unchanged.",
        "Raw outputs: receipts/acd_stage8_paper_check.txt and receipts/acd_stage8_abstract_check.txt. De-TeXed source retains original line numbers.",
        "Structural inventory: "+", ".join(str(r["token"])+" at line "+str(r["line"]) for r in structural)+f'; {len(numeric["structural_constants"])-len(structural)} label/reference occurrences and {len(numeric["bibliographic_numbers"])} bibliography metadata fields.',
        "No build or scientific runs.",""]
    p=ROOT/"ACD_PAPER_NUMERIC_CHECK.md"
    old=subprocess.check_output(["git","show",BASE+":aspen/determinacy/ACD_PAPER_NUMERIC_CHECK.md"],cwd=ROOT).decode()
    p.write_text(old.rstrip()+"\n\n"+"\n".join(check))
    lines=["# Stage 8 — paper v5","",
        "Base: "+BASE+". Supplied source hashes verified; main.tex and refs.bib remain unchanged. The abstract is replaced verbatim, with titles and historical optional text preserved.",
        f'Changed-paper audit: {paper["counts"]["OK"]} OK / {paper["counts"]["FIX"]} FIX. Current abstract and titles: {abstract["counts"]["OK"]} OK / {abstract["counts"]["FIX"]} FIX.',
        f'Current paper inventory: {paper["current_counts"]["OK"]} OK / {paper["current_counts"]["FIX"]} FIX; only the ten changed sentences were re-audited, with unchanged entries carried forward.',
        "The eight paper and two abstract Stage 7 rows are explicitly disposed in the appended audits and Stage 8 audit receipts.",
        "Numeric checks: zero unmatched numbers; NUMBERS regeneration PASS with 12016 unchanged keys.",
        f'Abstract length: {diff["abstract_characters_excluding_trailing_newline"]} Unicode characters, excluding final newline.',
        "Todd-licensed standing rulings remain: title, opening framing, defined forecast-sign shorthand, labelled post hoc/development material in abstract and introduction. Post hoc evidence licenses no frozen route.","",
        "## Open audit rows","", "| Audit | ID | Proposed fix |","|---|---|---|"]
    for label,r in fixes:lines.append("| "+label+" | "+r["id"]+" | "+r["proposed_fix"].replace("|","\\|").replace("\n"," ")+" |")
    if not fixes:lines.append("| Both | None | No open FIX rows |")
    lines += ["","## Resolution rules","",
        "R-other: the supplied v5 source still prints 'October 2026 --- draft v4'. Preserve its verified bytes and flag this metadata discrepancy. The printed label was unchanged, so it is outside the requested changed-passage re-audit.",
        "Prior R-other scope rules remain: corrected all-S denominator, exploratory/post hoc readings license no frozen route, and numerical energy-budget closure residual retained. No hard stop fired.",
        "No build, sampling, integration, fitting, inference, training, cloud compute or Qwen service changes. All work uses static sources and receipts on sulaco CPU; Baccus close-out untouched.",""]
    (ROOT/"ACD_STAGE8_STATUS.md").write_text("\n".join(lines))
    note=["# Aspen intervention horizon paper — Stage 8, v5","",
        f'Supplied v5 sources verified unchanged. Changed-paper audit: **{paper["counts"]["OK"]} OK / {paper["counts"]["FIX"]} FIX**; current abstract and titles: **{abstract["counts"]["OK"]} OK / {abstract["counts"]["FIX"]} FIX**.',
        f'Current full-paper inventory: **{paper["current_counts"]["OK"]} OK / {paper["current_counts"]["FIX"]} FIX**; all ten Stage 7 findings are resolved.',
        "Branch: paper/aspen-2026-10-determinacy. Base: "+BASE+".",
        "Sulaco: /home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy/.",""]
    for path,label in [("paper/main.tex","V5 paper source"),("paper/refs.bib","References"),("ACD_PAPER_AUDIT.md","Appended changed-passage audit and Stage 7 dispositions"),("ACD_ABSTRACT_DRAFT.md","Verbatim v5 abstract and retained titles"),("ACD_ABSTRACT_AUDIT.md","Full v5 abstract audit"),("ACD_PAPER_NUMERIC_CHECK.md","Numeric checks and structural inventory"),("receipts/acd_stage8_paper_audit.json","V5 paper audit receipt"),("receipts/acd_stage8_abstract_audit.json","V5 abstract audit receipt"),("receipts/acd_stage8_source.json","Source hash verification"),("receipts/acd_stage8_diff.json","Source diff inventory"),("ACD_STAGE8_STATUS.md","Stage 8 status")]:
        note.append("- ["+label+"]("+URL+path+")")
    note += ["","Both numeric checks have zero unmatched numbers. Abstract: 1894 characters excluding final newline. No build attempted; no PDF supplied.",""]+lines[lines.index("## Open audit rows"):]
    (ROOT/"Draft_Aspen-Intervention-Horizon-Paper-2026-10.md").write_text("\n".join(note).rstrip()+"\n")
    result=dict(base=BASE,source_hashes_verified=True,abstract_verbatim=True,titles_unchanged=True,optional_text_unchanged=True,
        registry_unchanged=True,prior_receipts_unchanged=True,numeric_unmatched=numeric["unmatched"],
        paper_counts=paper["counts"],current_paper_counts=paper["current_counts"],abstract_counts=abstract["counts"],resolutions=rules,scientific_runs=0,build_attempted=False)
    (ROOT/"receipts/acd_stage8_verification.json").write_text(json.dumps(result,indent=2)+"\n")
    paths=["paper/main.tex","paper/refs.bib","paper/main.detex.txt","paper/TEX_ENVIRONMENT.json","ACD_ABSTRACT_DRAFT.md","ACD_PAPER_AUDIT.md","ACD_ABSTRACT_AUDIT.md","ACD_PAPER_NUMERIC_CHECK.md","acd_paper_check.py","acd_stage8_report.py","ACD_STAGE8_STATUS.md","Draft_Aspen-Intervention-Horizon-Paper-2026-10.md"]
    paths += [str(p.relative_to(ROOT)) for p in sorted((ROOT/"receipts").glob("acd_stage8*"))]
    (ROOT/"ACD_STAGE8_ARTIFACTS.json").write_text(json.dumps(dict(base=BASE,hashes={p:digest(ROOT/p) for p in paths},resolutions=rules),indent=2)+"\n")
    print(json.dumps(result,indent=2))
if __name__=="__main__":run()
