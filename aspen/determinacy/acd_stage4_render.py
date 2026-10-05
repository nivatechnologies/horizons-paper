"""Assemble Stage4 audit intake, ledger, report and vault note without drafting."""
import json,hashlib,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
BASE='https://github.com/nivatechnologies/horizons-paper/blob/paper/aspen-2026-10-determinacy/aspen/determinacy/'
PLACEHOLDER='[paste the abstract above, plus title]'
def link(p):return f'[{p}]({BASE+p})'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run():
 draft=ROOT/'ACD_ABSTRACT_DRAFT.md'
 if not draft.exists():draft.write_text(PLACEHOLDER)
 if draft.read_text()!=PLACEHOLDER:raise RuntimeError('Real draft now present: preserve it and complete sentence-level factual audit before rendering.')
 result=subprocess.run([sys.executable,str(ROOT/'check_acd.py'),'--text',str(draft)],capture_output=True,text=True)
 (ROOT/'receipts/acd_stage4_abstract_check.txt').write_text(result.stdout+result.stderr)
 fix='Supply the exact title and abstract; preserve it verbatim, then audit each sentence against confirmation NUMBERS and its route status.'
 auditrow='| 1 | '+PLACEHOLDER+' | None supplied | None | Not applicable | Not applicable | None | No title, setup or scientific sentence was supplied; L1–L10 and scope/comparison wording cannot be assessed | FIX | '+fix+' |'
 audit="""# Aspen abstract audit — input FIX, scientific audit OPEN

The supplied payload contains only the paste placeholder below. A title and actual abstract were requested during execution and have not arrived. The payload is preserved verbatim in ACD_ABSTRACT_DRAFT.md; it is not treated as an abstract and no abstract was invented.

**Counts: 0 OK, 1 FIX (input row); 0 scientific claims assessed.** Release audit is not closed. The number checker extracts zero numbers and mechanically reports PASS; that empty result establishes no factual correctness or license. See receipts/acd_stage4_abstract_check.txt.

| Row | Sentence / supplied payload | Number(s) | NUMBERS key | Full-precision value | Rounding OK? | Licensing L# | Wording / §11 scope review | Verdict | Proposed fix |
|---|---|---|---|---|---|---|---|---|---|
"""+auditrow+"""

The pending substantive pass must check every number, each L# condition, all banned wording, the exact Fc name “the sign of the unforced window-energy anomaly”, declared model/prior/noise/actions, and world-model framing. Every comparison and ordering word must trace to the actual frozen confirmation route. R1m bootstrap intervals are approximate and descriptive; they cannot license comparison words. Development and amplitude-exploratory values license no abstract sentence.

Confirmation guardrails: R0/R0-F PASS at 2 and 3 LT; R2a DIFFERS at both; R2b PRECEDES; R5 DOES NOT BEAT. RML confirmation, R7 and arm A were cut. CNN may use L8’s conditional subset sentence, but “overconfident” is not licensed by its calibration bounds. R5 cannot claim superior targeting. Mechanism medians are descriptive L4 quantities, not causal proof. No actual draft wording has yet been assessed.

**R-other:** missing source text licenses no invented sentence, no substitution of the Stage2 reading for Todd’s draft, and no audit sign-off. All independent Stage4 work continues.
"""
 (ROOT/'ACD_ABSTRACT_AUDIT.md').write_text(audit)
 marker='\n## Stage4 abstract-to-license ledger — 2026-10-05\n'
 ledger=ROOT/'CLAIM_LEDGER.md';text=ledger.read_text().split(marker)[0]
 ledger.write_text(text+marker+"""
The scientific abstract is absent from the request; this is an intake FIX, not an audited scientific sentence. Existing confirmation licenses remain unchanged. Publication route is PUBLISH under §11, but the factual release audit remains OPEN.

| Abstract sentence / supplied payload | L# | NUMBERS keys | Audit verdict |
|---|---|---|---|
| [paste the abstract above, plus title] | None — missing title and abstract | None | FIX: supply verbatim draft; 0 scientific sentences assessed |

Receipt-backed numbers, mechanism and greyscale figures are complete. Optional amplitude results are development/exploratory and license nothing in the abstract. Changed-amplitude null proxies do not extend the frozen scientific claim. Stage4 R-other findings and resolutions: ACD_STAGE4_REPORT.md.
""")
 resolutions=[
  dict(rule='R-other',finding='Protocol and structural literals have no numeric Stage2 JSON field',resolution='Identify contract/source constants separately; empirical values point to actual Stage2 paths. Derived values carry actual input paths and operations; no fabricated receipt path.'),
  dict(rule='R-other',finding='Per-question z_D/z_F distribution and window-level divergence quartiles are not saved',resolution='Report ratio of saved medians explicitly; window divergence point only. Preserve saved tick-level divergence median/IQR separately; no invented quartiles or new statistic.'),
  dict(rule='R-other',finding='Individual physical-state trajectories are not saved for qualifying F1 case 6',resolution='Show existing opposing-draw window-energy curves and saved Q probe, labelled illustrative. Do not reconstruct state trajectories.'),
  dict(rule='R-other',finding='Amplitude-matched climatological states are not on disk',resolution='No new climatological run. Matched observation confidence and R2b unavailable away from 0.16; display frozen-null-relative exploratory proxies explicitly, with no route status or abstract license.'),
  dict(rule='R-other',finding='Abstract/title payload is a paste placeholder',resolution='Preserve exact supplied payload and record input FIX. No scientific claims assessed, no fabricated abstract, no sign-off; remaining receipt work complete.')
 ]
 numbers=json.loads((ROOT/'numbers_acd.json').read_text())
 report=f"""# Aspen Stage4 report — receipt work complete; abstract audit OPEN

Base: c1d692a06483dd57e4d6159f43333d53fa0ab8ca, branch paper/aspen-2026-10-determinacy. Work and numerical computation ran on sulaco CPU in /home/todd/work/aspen-determinacy-stage4-20261005. Original Stage2 and development receipts and scientific code remain unchanged. No new posterior, fits, training, inference or cloud computation; Qwen services are untouched. Baccus checkout and AFD close-out were not changed. The optional exploration integrates saved development posterior terminal states, as expressly authorized.

NUMBERS: {len(numbers['numbers'])} full-precision keys. check_acd.py regenerates both artifacts and rejects differences; --text handles decimals, scientific notation, percentages, k-units and visible identifiers. Digests and Markdown link destinations are provenance, excluded from prose numbers. Rounding uses round-to-nearest/even at the stated last digit, preserving Stage2 float unit conversions. Literal matching checks rounding only; scientific quantity, panel, unit and license require semantic audit. Every visible number in ACD_STAGE2_READING.md matches (544 extracted). Development keys use ACD_DEV_.

Verification passed: registry and Markdown tampering rejected, unmatched number printed with nonzero exit, lexer/unit/scientific cases, exact development baseline shares and R2b, 1000 bitwise unforced-forecast checks, 200 bitwise baseline whole forecasts, F1 designated pair and opposite answers, reproducible PDF/PNG/caption bytes, original checker archived and scientific modules unchanged. Full receipt: receipts/acd_stage4_verification.json. PDF creation/modification dates are omitted for reproducibility; requirements-stage4.lock records the environment.

Figures are receipt-only, PDF and PNG, greyscale, with second cues. F1 is illustrative confirmation case 6; F2 is frozen confidence by question type; F3 is saved mechanism plus z_D/z_F medians and IQR; F4 marks RML development and other arms confirmation; F5 Q/F/V/R is at frozen settings and notes A was cut. Sources, captions and hashes: receipts/acd_stage4_figures.json and figures/CAPTIONS.md. Figures were visually checked for readable axes and distinct cues.

Optional amplitude exploration completed all 200 development cases at 0.04, 0.08, 0.16, 0.32 and 0.64 on eight workers with two integration threads each (16 CPU threads total). Saved individual draw costs live under runs/stage4_amplitude on sulaco; hashes are in receipts/acd_stage4_amplitude.json. The 0.16 forecast is reused exactly; factual forecasts agree bitwise at every amplitude. The report is labelled development and exploratory, licenses no abstract claim, and distinguishes matched quantities from frozen-null proxies.

**Abstract audit: 0 OK / 1 FIX intake row; 0 scientific claims assessed.** Actual title and abstract have not been supplied. ACD_ABSTRACT_DRAFT.md preserves the exact placeholder; its vacuous numeric PASS is not an audit sign-off. ACD_ABSTRACT_AUDIT.md and CLAIM_LEDGER.md record the missing-input FIX. No paper was released or submitted.

## Resolution rules

New Stage4 rule: R-other, with the following applications. No H1–H3 hard stop occurred. Earlier R-time, R-rml, R-other and R-diag findings remain carried in the immutable confirmation receipt; Stage4 introduces no new calibration, cutoff or route status.

| Rule | Finding | Resolution |
|---|---|---|
"""
 for r in resolutions:report+='| '+r['rule']+' | '+r['finding']+' | '+r['resolution']+' |\n'
 report+='\n## Artifact pointers\n\n'
 pointers=['NUMBERS_ACD.md','numbers_acd.json','check_acd.py','ACD_MECHANISM.md','acd_figures.py','figures/CAPTIONS.md','ACD_ABSTRACT_DRAFT.md','ACD_ABSTRACT_AUDIT.md','CLAIM_LEDGER.md','ACD_AMPLITUDE_EXPLORATORY.md','receipts/acd_stage4_verification.json','receipts/acd_stage4_amplitude.json']
 for p in pointers:report+='- '+link(p)+'\n'
 (ROOT/'ACD_STAGE4_REPORT.md').write_text(report)
 vault='# Aspen counterfactual determinacy — Stage4 (2026-10)\n\n**Receipt work complete; abstract audit OPEN.** Confirmation publication route remains PUBLISH under frozen v2.3 §11. Stage4 adds no new confirmation data or posterior. Branch starts at c1d692a; execution was sulaco CPU only.\n\n'+link('ACD_STAGE4_REPORT.md')+'\n\n## Documents and figures\n\n'
 for p in pointers:vault+='- '+link(p)+'\n'
 for name in ['F1_illustrative','F2_confidence','F3_mechanism','F4_reliability','F5_measurements']:
  vault+='- '+link('figures/'+name+'.pdf')+' · '+link('figures/'+name+'.png')+'\n'
 vault+='\n## Supplied draft payload, verbatim\n\n'+chr(96)*3+'\n'+draft.read_text()+'\n'+chr(96)*3+'\n\nThe title and actual abstract are absent. No substitute abstract was written.\n\n## Audit FIX rows\n\nCounts: **0 OK / 1 FIX (intake), 0 scientific claims assessed.** The empty numeric check is not factual audit approval.\n\n| Row | Supplied sentence / payload | Verdict | Proposed fix |\n|---|---|---|---|\n| 1 | '+PLACEHOLDER+' | FIX | '+fix+' |\n\n## Rules fired\n\n'
 for r in resolutions:vault+='- **'+r['rule']+'**: '+r['finding']+'. '+r['resolution']+'\n'
 vault+='\nInherited confirmation rules: R-time, R-rml, R-other, R-diag. No new H1–H3 stop. Optional amplitude forecasts are development/exploratory, license nothing in the abstract, and changed-amplitude observation-confidence/loss proxies explicitly use the frozen 0.16 null.\n\nRelated: [[WO_Aspen-Counterfactual-Determinacy-2026-10-04]], [[R_Aspen-Counterfactual-Determinacy-Confirmation-2026-10]], [[L_Aspen-Counterfactual-Determinacy-Claim-Ledger-2026-10]].\n'
 target=ROOT/'vault/04-Results/R_Aspen-Counterfactual-Determinacy-Stage4-2026-10.md';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(vault)
 manifest=dict(base='c1d692a06483dd57e4d6159f43333d53fa0ab8ca',panel='existing receipts',hard_stops=[],resolutions=resolutions,abstract_status='MISSING DRAFT: INPUT FIX; SCIENTIFIC AUDIT OPEN',audit_counts=dict(OK=0,FIX=1,scientific_claims=0),verification='PASS',outputs={str(p.relative_to(ROOT)):sha(p) for p in sorted(ROOT.glob('ACD_*')) if p.is_file() and p.name not in ['ACD_ARTIFACTS.json','ACD_STAGE2_ARTIFACTS.json','ACD_STAGE4_ARTIFACTS.json']})
 (ROOT/'ACD_STAGE4_ARTIFACTS.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print('Rendered Stage4 report, intake audit, ledger and vault note; 0 OK / 1 input FIX.')
if __name__=='__main__':run()
