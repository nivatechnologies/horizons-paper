"""Receipt-only sentence audit renderer; no model, sampler, forecasts or fitting."""
import json,re,hashlib,subprocess,sys
from pathlib import Path
from acd_numbers import ROOT,build,render as numbers_render
from check_acd import match,tokens
BASE='https://github.com/nivatechnologies/horizons-paper/blob/paper/aspen-2026-10-determinacy/aspen/determinacy/'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def escape(s):return str(s).replace('|','&#124;').replace('\n','<br>')
def code(s):return chr(96)+str(s)+chr(96)
def run():
 p=ROOT/'receipts/acd_stage4_abstract_audit.json';data=json.loads(p.read_text());rows=data['rows']
 expected=build();registry=expected['numbers']
 assert json.loads((ROOT/'numbers_acd.json').read_text())==expected
 assert (ROOT/'NUMBERS_ACD.md').read_text()==numbers_render(expected)
 draft=(ROOT/'ACD_ABSTRACT_DRAFT.md').read_text()
 abstract=draft.split('## Abstract\n\n')[1].split('\n\n## Optional')[0]
 sentences=re.split(r'(?<=[.!?])\s+(?=[A-Z])',abstract)
 assert len(sentences)==8
 assert [r['sentence'] for r in rows if r['id'].startswith('S')]==sentences
 title=re.search(r'\*\*Title:\*\* (.+)',draft)[1]
 alt=re.search(r'\*\*Alternative title:\*\* (.+)',draft)[1]
 assert next(r['sentence'] for r in rows if r['id']=='T')==title
 assert next(r['sentence'] for r in rows if r['id']=='T-alt')==alt
 for letter in ['M','A']:
  optional=re.search(r'\*\*'+letter+r' \([^\n]+?\):\*\* (.+)',draft)[1]
  assert next(r['sentence'] for r in rows if r['id']==letter)==optional
 semantic_items=0
 for row in rows:
  row['source_values']={key:registry[key] for key in dict.fromkeys([n['key'] for n in row['numbers']]+row['context_keys'])}
  for item in row['numbers']:
   literal={'half':'0.5','sixteenfold':'16'}.get(item['literal'],item['literal'])
   if item['key'].endswith('_PERCENT') and literal.endswith('%'):literal=literal[:-1]
   good=bool(match(literal,{item['key']:registry[item['key']]}))
   item['rounding_OK']=good
   assert good,(row['id'],item)
   semantic_items+=1
  row['rounding']='OK' if row['numbers'] else 'N/A — no explicit number'
 result=subprocess.run([sys.executable,str(ROOT/'check_acd.py'),'--text',str(ROOT/'ACD_ABSTRACT_DRAFT.md')],capture_output=True,text=True)
 (ROOT/'receipts/acd_stage4_abstract_check.txt').write_text(result.stdout+result.stderr)
 assert result.returncode==0,result.stdout+result.stderr
 stage2=json.loads((ROOT/'receipts/acd_stage2.json').read_text())
 assert stage2['R2b']['status']=='PRECEDES' and stage2['R2b']['prerequisite']
 for li in [3,5]:
  assert stage2['R0'][li]['R0']['status']=='PASS' and stage2['R0'][li]['R0_F']['status']=='PASS'
 assert all(r['status']=='DIFFERS' for r in stage2['R2a'])
 assert stage2['R6']['status']=='COMPLETE'
 counts={v:sum(r['verdict']==v for r in rows) for v in ['OK','FIX']}
 data.update(draft_sha256=sha(ROOT/'ACD_ABSTRACT_DRAFT.md'),base='91462d02c7c3ce96bae54ebfd9ccd2ea5b228ee1',counts=counts,numeric_check=dict(exit_code=result.returncode,extracted=len(list(tokens(draft))),semantic_items=semantic_items,unmatched=0),source_hashes={s:sha(ROOT/s) for s in ['numbers_acd.json','receipts/acd_stage2.json','receipts/acd_stage4_amplitude.json','sources/WO_v2.3.md','acd_abstract_audit.py']},hard_stops=[],resolutions=[dict(rule='R-other',trigger='Fc shorthand and broader forecast-horizon referents',resolution='Flag each affected row; propose the full Fc name and measured scope; preserve the draft, no assumed naming waiver.'),dict(rule='R-other',trigger='Ambiguous contrast, lead, averaging and CNN subset',resolution='Use the frozen estimands and denominators explicitly; rounding PASS is insufficient for semantic correctness.'),dict(rule='R-other',trigger='Broad world-model/practice framing outside Setup and licensed sentences',resolution='Replace with the measured question; retain only the S8 world-model reporting desideratum.'),dict(rule='R-other',trigger='Optional M/A outside L1–L10',resolution='No current abstract license. Propose descriptive wording and record the explicit scope/license amendment needed; do not infer comparison gates or run new experiments.')])
 p.write_text(json.dumps(data,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
 lines=['# Aspen abstract audit — supplied draft; audit complete, FIX rows open','',
 f"Base {data['base']}; receipt-only review on sulaco CPU. Draft preserved verbatim, SHA-256 {data['draft_sha256']}. No new runs, posterior samples, forecasts, training, inference or cloud computation. No Qwen service changes.",
 '',
 f"**{counts['OK']} OK / {counts['FIX']} FIX across 12 rows**: eight abstract sentences, title, alternative title, M and A. The audit is performed; the release audit is not closed until FIX rows are resolved. The prior missing-draft intake FIX is resolved.",
 '',
 f"Numeric checker: PASS, {data['numeric_check']['extracted']} visible literals, zero unmatched; output saved to receipts/acd_stage4_abstract_check.txt. All {semantic_items} sentence-level numeric/word-number mappings also pass at the stated rounding against their specific semantic key. Generic checker matches are only rounding candidates; the table pins quantities, units, panel and license. Header L# and §# tokens are structural, not empirical claims. 96 is the Lorenz-96 model identifier, not N. All full-precision values below are registry values (proportions unless named percent/ratio/count); rounding percentages applies ×100, except the already-percent CI constant. 'Half' is 0.5 and 'sixteenfold' is 16.",
 '',
 '## Sentence-level factual and licensing audit','',
 '| ID / claim | Sentence, verbatim | Number(s) | NUMBERS key(s) | Full-precision value(s) | Rounding OK? | Licensing L# / condition | Wording / §11 scope rules | Comparison and ordering route trace | Verdict | Proposed fix (draft unchanged) |',
 '|---|---|---|---|---|---|---|---|---|---|---|']
 for r in rows:
  literals='; '.join(x['literal'] for x in r['numbers']) or 'None'
  keys=list(r['source_values'])
  keytext='<br>'.join(code(k) for k in keys) or 'None'
  full='<br>'.join(code(k)+' = '+repr(r['source_values'][k]['value'])+(' (context)' if k in r['context_keys'] and k not in [n['key'] for n in r['numbers']] else '') for k in keys) or 'Not applicable'
  columns=[r['id']+' — '+r['kind'],r['sentence'],literals,keytext,full,r['rounding'],r['license'],r['finding'],r['comparison'],r['verdict'],r['fix']]
  lines.append('| '+' | '.join(escape(v) for v in columns)+' |')
 lines+=['','## Exact sources for the keyed values','', '| Row | Key | Receipt | Actual path / derivation |','|---|---|---|---|']
 for r in rows:
  for k,v in r['source_values'].items():
   path=json.dumps(v['receipt_path'],ensure_ascii=False) if isinstance(v['receipt_path'],list) else v['receipt_path']
   extra=('; '+v['derivation']) if 'derivation' in v else ''
   if 'additional_sources' in v:extra+='; additional sources '+json.dumps(v['additional_sources'],ensure_ascii=False)
   lines.append('| '+' | '.join(escape(x) for x in [r['id'],code(k),v['receipt'],path+extra])+' |')
 lines+=['','## Optional sentences: what would license them','']
 for r in rows[-2:]:lines+=['**'+r['id']+' — FIX.** '+r['needs'],'']
 lines+=['## Scope and route controls','',
 'Fc is always “the sign of the unforced window-energy anomaly” under §11. Defining “forecast sign” at first use does not create an exception. The phrase appears in S4, S7, M, A and the deliberate-deviation note; equivalent shorthand appears in S2 and S6 and broader forecast language appears in the two titles. The note acknowledges the conflict but is not approval to waive it. Todd can change the scope rule explicitly; no waiver is assumed here.',
 '',
 'None of the eight abstract sentences or two titles uses the frozen banned terms fixed, determined by the observations, every consistent instance, settled, certified, guaranteed or proven. M/A also contain none. S8 supplies the permitted world-model reporting desideratum; S1 instead asserts general evaluation practice outside the receipts. The CNN phrase “a deterministic CNN emulator” is correct. “Overconfident” is neither written nor licensed: the saved CNN R0 case accuracy is 0.9386483886483887 with one-sided upper 0.962.',
 '',
 'The R2b comparison is first loss of confidence on the tested lead grid, averaged over eligible cases after averaging their eligible-action shares; 194 cases and 1332 actions. It is not a universal per-instance or per-action ordering. All R0 and R0-F lead prerequisites are PASS or NOT EVALUABLE and the saved prerequisite is true. R2a at 2/3 LT is DIFFERS with both calibration prerequisites PASS. L4 medians at 2 LT are descriptive. R1m intervals stored as bootstrap intervals are approximate and descriptive; quartile bands are dispersion, and no interval for the ratio of medians is asserted.',
 '',
 'L9 uses a 3 LT horizon: answered leads 0, 1, 1.5, 2, 2.5, 3 and refused leads 4, 6. Its 26% and 7% fractions have separate within-range denominators. L8 uses 442 posterior-open intervention-sign questions at 2 LT, of which 97 are CNN-confident and 64 correct. These are distinct populations. The broad forecast horizon and learned-world-model capability are not measured by any of these routes.',
 '',
 'A compares all-confident development shares only; it does not use the changed-amplitude observation-confidence/null proxies. The five existing posterior re-forecast settings do not establish a continuous-range result or calibrated correctness for changed actions. No optional sentence is inserted into the draft or receives an invented L#.',
 '',
 'The only new resolution rule is R-other, as recorded in receipts/acd_stage4_abstract_audit.json. No H1–H3 stop. Draft wording remains unchanged; fixes are proposals, not silent amendments.',
 '']
 (ROOT/'ACD_ABSTRACT_AUDIT.md').write_text('\n'.join(lines).rstrip()+'\n')
 marker='\n## Stage4 abstract-to-license ledger — 2026-10-05\n'
 ledger=ROOT/'CLAIM_LEDGER.md';old=ledger.read_text().split(marker)[0]
 ledgerlines=[marker.strip(),'','Supplied abstract audited; prior missing-input FIX resolved. Publication route remains PUBLISH under frozen §11; release wording fixes remain open. Counts: 2 OK / 10 FIX. Draft unchanged. M/A have no current abstract license.','', '| Row | Abstract sentence / title / optional sentence | L# | NUMBERS keys | Verdict |','|---|---|---|---|---|']
 for r in rows:ledgerlines.append('| '+' | '.join(escape(v) for v in [r['id'],r['sentence'],r['license'],'; '.join(r['source_values']) or 'None',r['verdict']])+' |')
 ledgerlines+=['','Full precision, receipt paths, route trace and proposed fixes: ACD_ABSTRACT_AUDIT.md. Follow-up used only existing receipts, with arithmetic conversions for actual snapshot span, confidence levels and tested-amplitude normalization; no scientific reruns. Stage4 R-other scope and wording resolutions are recorded in receipts/acd_stage4_abstract_audit.json.','']
 ledger.write_text(old+'\n'+'\n'.join(ledgerlines).rstrip()+'\n')
 # Update current overview, preserving original compute/figure reporting.
 report=ROOT/'ACD_STAGE4_REPORT.md';s=report.read_text()
 s=s.replace('# Aspen Stage4 report — receipt work complete; abstract audit OPEN','# Aspen Stage4 report — receipt work and abstract audit complete; release FIX rows open')
 s=s.replace('NUMBERS: 4696 full-precision keys.',f"NUMBERS: {len(registry)} full-precision keys (eight source-labelled arithmetic/contract additions in the abstract follow-up).")
 start=s.index('**Abstract audit:');end=s.index('\n## Resolution rules',start)
 s=s[:start]+f"**Abstract audit: {counts['OK']} OK / {counts['FIX']} FIX across 12 rows.** The actual title, alternative title, eight sentences and optional M/A have been audited. Draft preserved verbatim; numeric PASS with 49 extracted literals and zero unmatched. Prior missing-draft FIX resolved. All remaining FIX rows and proposed fixes appear in ACD_ABSTRACT_AUDIT.md; release fixes remain open. No paper was released or submitted.\n"+s[end:]
 s=s.replace('| R-other | Abstract/title payload is a paste placeholder | Preserve exact supplied payload and record input FIX. No scientific claims assessed, no fabricated abstract, no sign-off; remaining receipt work complete. |','| R-other | Abstract follow-up: Fc naming, ambiguous estimands and outside-license M/A | Preserve supplied draft, flag affected rows, propose precise licensed wording; no implicit waiver or new license. Historical missing-input FIX is resolved. |')
 s=s.split('\n## Abstract follow-up at 91462d0\n')[0]
 s+='\n## Abstract follow-up at 91462d0\n\nThe only new rule is R-other for naming, measured scope, exact estimands and outside-license optional material. Audit complete: 2 OK / 10 FIX; numerical values and ratios round correctly. Metadata alone was added to NUMBERS so semantic mappings use actual quantities rather than coincidental rounding matches. No model runs, plotting, calibration, thresholds or decision routes changed. New audit input/receipt: receipts/acd_stage4_abstract_audit.json; renderer: acd_abstract_audit.py. Proposed fixes await editorial disposition, not further computation.\n'
 report.write_text(s)
 # Existing vault note retains figure and artifact links; refresh draft and verdict sections.
 target=ROOT/'vault/04-Results/R_Aspen-Counterfactual-Determinacy-Stage4-2026-10.md'
 s=target.read_text();s=s.replace('**Receipt work complete; abstract audit OPEN.**','**Receipt work and abstract audit complete; release FIX rows open.**')
 draft_heading='## Supplied draft payload, verbatim' if '## Supplied draft payload, verbatim' in s else '## Supplied draft, verbatim'
 start=s.index(draft_heading);end=s.index('## Rules fired',start)
 new='## Supplied draft, verbatim\n\n'+chr(96)*3+'\n'+draft+chr(96)*3+'\n\n## Audit verdicts\n\n**2 OK / 10 FIX**, across the title, alternative title, eight abstract sentences and optional M/A. Numeric checker: PASS, 49 visible literals, zero unmatched. The prior missing-input FIX is resolved. Audit performed; proposed wording/license fixes remain open. Draft unchanged.\n\n| Row | Kind | L# | Verdict |\n|---|---|---|---|\n'
 for r in rows:new+='| '+' | '.join(escape(x) for x in [r['id'],r['kind'],r['license'],r['verdict']])+' |\n'
 new+='\n## Every FIX row and proposed fix\n\n| Row | Sentence / title, verbatim | Finding | Proposed fix |\n|---|---|---|---|\n'
 for r in rows:
  if r['verdict']=='FIX':new+='| '+' | '.join(escape(x) for x in [r['id'],r['sentence'],r['finding'],r['fix']])+' |\n'
 new+='\n## M and A licensing requirements\n\n'
 for r in rows[-2:]:new+='**'+r['id']+'**. '+r['needs']+'\n\n'
 s=s[:start]+new+s[end:]
 s=s.replace('- **R-other**: Abstract/title payload is a paste placeholder. Preserve exact supplied payload and record input FIX. No scientific claims assessed, no fabricated abstract, no sign-off; remaining receipt work complete.','- **R-other**: The previous missing-title/draft input FIX is resolved. This follow-up flags Fc shorthand, broader forecast referents, ambiguous leads/contrasts/denominators, unsupported general practice framing, and M/A outside L1–L10; proposes precise wording and licensing requirements; changes no route, threshold or draft text.')
 s=s.split('\nFollow-up audit receipt:')[0]
 s+='\nFollow-up audit receipt: [receipts/acd_stage4_abstract_audit.json]('+BASE+'receipts/acd_stage4_abstract_audit.json). The claim ledger maps all twelve rows to their keys and verdicts. No new scientific runs or figure rendering occurred.\n'
 target.write_text(s)
 manifestpath=ROOT/'ACD_STAGE4_ARTIFACTS.json';m=json.loads(manifestpath.read_text())
 m.update(abstract_status='AUDIT COMPLETE: 2 OK / 10 FIX; RELEASE WORDING/LICENSE FIXES OPEN',audit_counts=dict(OK=2,FIX=10,abstract_sentences=8,title_rows=2,optional_rows=2),abstract_followup_base=data['base'],draft_sha256=data['draft_sha256'],abstract_numeric_check=data['numeric_check'])
 for r in m['resolutions']:
  if r['finding']=='Abstract/title payload is a paste placeholder':
   r.update(finding='Supplied title/draft follow-up; prior missing-input FIX resolved',resolution='Audit performed: 2 OK / 10 FIX. Preserve exact draft, propose scope/estimand/naming fixes; M/A remain unlicensed.')
 m['abstract_followup_resolutions']=data['resolutions']
 for pth in list(m['outputs']):m['outputs'][pth]=sha(ROOT/pth)
 for pth in ['NUMBERS_ACD.md','numbers_acd.json','CLAIM_LEDGER.md','receipts/acd_stage4_abstract_check.txt','receipts/acd_stage4_abstract_audit.json','acd_abstract_audit.py',str(target.relative_to(ROOT))]:
  m['outputs'][pth]=sha(ROOT/pth)
 manifestpath.write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps(dict(counts=counts,semantic_numbers=semantic_items,draft_sha256=data['draft_sha256'],literal_numbers=data['numeric_check']['extracted'],hard_stops=[])))
if __name__=='__main__':run()
