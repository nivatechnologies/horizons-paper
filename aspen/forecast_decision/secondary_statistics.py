"""One-scale secondary descriptive coordinator; no policy selection or gate."""
import argparse,json,datetime,subprocess,sys
from pathlib import Path
from protocol import ROOT,write_json


def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--authorization',required=True);a=p.parse_args()
    # Recover the already-selected validation null from registered case flags;
    # do not select an action from this panel or any test cost.
    flags=json.loads((a.root/'runs/stage1_cases.json').read_text())['cases']
    fixed={e['b'] for r in flags for e in r['leads'] if e['fixed_correct']}
    if len(fixed)!=1:raise ValueError('single previously selected fixed action unavailable')
    from assemble_metrics import assemble
    rows,result=assemble(a.root,a.root/'runs/secondary_case_rows.json',['N-last','N-oracle','CNN-20k'],a.authorization,stage='secondary',intervals=True,panel='test2',fixed_action=next(iter(fixed)))
    write_json(a.root/'runs/secondary_metrics_cases.json',dict(cases=rows));write_json(a.root/'runs/secondary_metrics.json',result)
    subprocess.run([sys.executable,str(a.root/'full_report.py'),'--root',str(a.root),'--stage','secondary'],check=True)
    write_json(a.root/'runs/secondary_statistics_status.json',dict(status='REGISTERED',at=datetime.datetime.now(datetime.timezone.utc).isoformat(),role='statistics only',gate=None,licensed_sentences=[]))
if __name__=='__main__':main()
