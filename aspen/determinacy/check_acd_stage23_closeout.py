"""Verify the new supplement and unchanged prior registry file hashes."""
import json
from pathlib import Path
from acd_stage23_closeout_registry import ROOT,RECEIPT,rows,render,sha
expected=rows(json.loads((ROOT/RECEIPT).read_text()));actual=json.loads((ROOT/'numbers_acd_stage23_closeout.json').read_text());assert expected==actual
assert (ROOT/'NUMBERS_ACD_STAGE23_CLOSEOUT.md').read_text()==render(expected)
record=json.loads((ROOT/RECEIPT).read_text())
assert all(sha(ROOT/p)==h for p,h in record['registry_verification']['prior_registry_files_sha256'].items())
assert all(record['checks'][k]['passed'] for k in ['A1','A2','A3','A4','A5'])
assert not record['realized_outcome_accesses'] and record['training_updates']==record['optimizer_runs']==0
print('PASS: closeout supplement; all prior registry files byte-identical')
