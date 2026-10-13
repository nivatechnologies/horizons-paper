"""Render the closeout receipt, including its independent registry supplement."""
import copy,json
from pathlib import Path
from acd_stage23_closeout_finalize import ROOT,render
record=json.loads((ROOT/'receipts/acd_stage23_closeout.json').read_text())
presentation=copy.deepcopy(record)
presentation['registry_verification']['final_key_count']=record['registry_verification']['combined_key_count']
render(presentation)
print('CLOSEOUT REPORT GENERATED FROM RECEIPT')
