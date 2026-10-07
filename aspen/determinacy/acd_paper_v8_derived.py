"""Receipt-only percentage-unit derivation for paper v8."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def build():
    source='receipts/acd_stage9.json'
    d=json.loads((ROOT/source).read_text())
    rows=d['C']['CNN-F-resp']['confidence_readings']
    i=next(i for i,r in enumerate(rows) if r['lead']==2.0)
    return dict(scope='Post hoc; no frozen-route license',source_hashes={source:hashlib.sha256((ROOT/source).read_bytes()).hexdigest()},quantities={'CNN_F_RESP_ERROR_UPPER_PERCENT_2LT':dict(value=rows[i]['error_upper']*100,source=source,source_path=f'$.C.CNN-F-resp.confidence_readings[{i}].error_upper',derivation='one-sided betting upper bound multiplied by 100 for the percent-unit bracket in Table tab:resp')})
if __name__=='__main__':
    (ROOT/'receipts/acd_paper_v8_derived.json').write_text(json.dumps(build(),indent=2,allow_nan=False)+'\n')
