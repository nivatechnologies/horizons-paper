"""Prepare a release inventory from local files; never publish or open hidden truth."""
import hashlib,json,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent
RAW=Path('/home/todd/work/aspen-determinacy-20261005/aspen/determinacy/runs')
ART=Path('/home/todd/work/aspen-determinacy-stage4-20261005/aspen/determinacy')
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for chunk in iter(lambda:f.read(1048576),b''):h.update(chunk)
 return h.hexdigest()
def run():
 freeze=subprocess.check_output(['git','log','--format=%H','--reverse','--','ACD_FREEZE.md'],cwd=ROOT,text=True).splitlines()[0]
 items=[]
 def add(p,role,afd=False,hidden=False):
  if not p.exists():items.append(dict(path=str(p),role=role,available=False,flags=['MISSING']));return
  flags=[]
  if afd:flags.append('AFD-derived: permission/provenance review before release')
  if p.stat().st_size>100000000:flags.append('over 100 MB: archive storage required')
  if hidden:flags.append('scoring-only outcomes: release separately from model inputs')
  if p.suffix in ['.py','.md','.json','.jsonl','.lock']:
   text=p.read_text(errors='replace')
   if re.search(r'/home/|/mnt/|192\.168\.|/checkpoint|/data:',text):flags.append('machine paths: sanitize before release')
   if re.search(r'(?i)(?:password|api[_-]?key|access[_-]?token)\s*[:=]\s*[\x22\x27][^\x22\x27]+',text):flags.append('possible credential literal: inspect and redact before release')
  items.append(dict(path=str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p),role=role,available=True,size_bytes=p.stat().st_size,sha256=digest(p),flags=flags))
 for name,role in [('ACD_FREEZE.md','frozen scientific protocol'),('ACD_FREEZE_CODE.md','pre-confirmation code hash addendum'),('sources/WO_v2.3.md','observation/intervention/statistics contract'),('ACD_FREEZE.md','embedded ACD_IDS seed role contract'),('acd_protocol.py','observation contract and intervention patterns'),('acd_questions.py','question definitions'),('acd_stats.py','v2.3 betting bounds: frozen grid and settings'),('acd_evaluate.py','external-cost evaluator entry point'),('acd_stage13_analysis.py','decision scoring and CPU step check'),('acd_stage6_analysis.py','question summaries / same-lead scoring'),('acd_stage9_cnn_metrics.py','confidence / calibration scoring'),('acd_stage9_receipts.py','case-level paired endpoint scoring'),('requirements-cpu.lock','CPU environment'),('numbers_acd.json','full precision registry'),('NUMBERS_ACD.md','registry presentation'),('acd_numbers.py','registry regeneration'),('check_acd.py','registry and numeric checker'),('receipts/acd_stage2.json','Tables 2–4 and primary comparison aggregate receipts'),('receipts/acd_stage2_closeout.json','case provenance and draw policy'),('receipts/acd_stage9.json','post hoc learned-model provenance and readings'),('receipts/acd_stage13_decisions.json','cross-model decision records'),('receipts/acd_stage13_dt.json','full-grid step-check receipt')]:
  add(ROOT/name,role)
 for c in range(200):
  add(RAW/f'conf/case_{c:03d}.json','per-case forecast / fit receipt')
  add(RAW/f'conf/order_{c:03d}.jsonl','per-case blind-order and hash receipt')
  add(RAW/f'conf/input_{c:03d}.npz','observed input panel, outcomes stored separately')
  add(RAW/f'conf/case_{c:03d}.npz','posterior per-case costs, draws and retained draw ordering')
  add(RAW/f'conf/score_{c:03d}.npz','hashed realized case-level outcomes',hidden=True)
  add(ART/f'runs/stage9/evaluation_inputs/{c:03d}.npz','supplied noise-free draw histories H and own forcing F')
  for name in ['CNN-20k','CNN-F']:
   add(ART/f'runs/stage9/inference/{name}/{c:03d}.npz','learned per-case costs; reproduction records',afd=name=='CNN-20k')
 add(ROOT/'runs/stage4b_null/states.npz','frozen climatological null states')
 add(ROOT/'runs/stage4b_null/null_0.16.npz','null probabilities and decision margin sd')
 add(Path('/home/todd/work/aspen-forecast-decision-20261005/aspen/forecast_decision/inputs/CNN-20k.pt'),'CNN-20k checkpoint',afd=True)
 add(ART/'runs/stage9_training/CNN-F/selected.pt','CNN-F selected checkpoint')
 for name in ['physics.py','protocol.py']:
  add(Path('/home/todd/work/aspen-forecast-decision-20261005/aspen/forecast_decision')/name,'inherited evaluator dependency; extract standalone contract/kernel for release',afd=True)
 # Aggregate size flags matter even if each case file is small.
 groups={}
 for role in sorted({i['role'] for i in items}):
  group=[i for i in items if i['role']==role and i['available']]
  groups[role]=dict(files=len(group),size_bytes=sum(i['size_bytes'] for i in group))
 record=dict(preparation_only=True,published=False,freeze_commit=freeze,items=items,groups=groups,settings_source='ACD_FREEZE.md §compute settings; acd_stats.py betting grid/alpha; do not infer settings from rounded paper prose')
 (ROOT/'receipts/acd_stage13_release.json').write_text(json.dumps(record,indent=2)+'\n')
 lines=['# Release manifest — preparation only','','No public archive has been published. Release requires the listed records and a portable copy of the evaluator dependencies. Scoring-only realized outcomes must remain separate from model input histories/forcings. Hidden true states are not inventoried or opened.','','Scientific freeze commit: '+freeze+'. Code addendum: ACD_FREEZE_CODE.md.','','Betting settings and implementation: ACD_FREEZE.md, sources/WO_v2.3.md §10, acd_stats.py. The receipt retains file hashes and byte sizes. The independent unit is the case; reliability-bin CP intervals and paired bootstraps are descriptive.','','AFD-derived files cannot be released as part of this preparation without separate permission/provenance review. Machine paths require sanitization; possible credential literals require inspection/redaction; files or grouped datasets over the archive size threshold need a suitable storage plan. No checkpoint is copied or uploaded.','','| Role | Files | Bytes | Group over 100 MB |','|---|---|---|---|']
 lines += [f"| {role} | {r['files']} | {r['size_bytes']} | {r['size_bytes']>100000000} |" for role,r in groups.items()]
 lines += ['','| Item | Bytes | SHA-256 | Release flags |','|---|---|---|---|']
 lines += [f"| {i['path']} | {i.get('size_bytes','missing')} | {i.get('sha256','missing')} | {'; '.join(i['flags']) or 'none detected'} |" for i in items]
 (ROOT/'RELEASE_MANIFEST.md').write_text('\n'.join(lines)+'\n')
 print('manifest items',len(items),'flagged',sum(bool(i['flags']) for i in items))
if __name__=='__main__':run()
