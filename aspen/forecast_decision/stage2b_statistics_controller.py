"""Durable approved two-scale statistics coordinator; no training or selection."""
import argparse,datetime,json,time,subprocess,sys
from pathlib import Path
from protocol import ROOT,ORDER2,write_json,digest
from stage2_statistics_controller import reject_nonfinite


def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()


def readiness(root):
    approval=root/'runs/twoscale/sampler_go.json'
    if not approval.exists():return None,'waiting for Todd two-scale sampler go'
    go=json.loads(approval.read_text());reject_nonfinite(go)
    if go.get('approved') is not True or go.get('approved_by')!='Todd':return None,'Todd sampler approval absent'
    if go['sampler_check_sha256']!=digest(root/'runs/twoscale/sampler_check.json'):raise ValueError('sampler approval source mismatch')
    selection_path=root/'runs/training/final_selection_stage2b.json'
    if not selection_path.exists():return None,'waiting for FINAL validation-selected two-scale manifest'
    selection=json.loads(selection_path.read_text());reject_nonfinite(selection)
    if selection.get('status')!='FINAL':return None,'two-scale selection is not FINAL'
    if selection.get('system')!='two-scale' or not selection.get('selection_completed_at'):raise ValueError('invalid two-scale selection')
    S=selection['S'];names=list(selection['models'])
    if selection['selected_L'] not in S or set(S)!=set(n for n in names if n in ORDER2):raise ValueError('two-scale frozen S mismatch')
    if not {'CNN2-20k','CNN2-R2','CNN2-roll','CNN2-cost'}.issubset(names):raise ValueError('mandatory two-scale arm missing')
    if selection.get('best_fixed_action') not in range(8):raise ValueError('validation-selected fixed action missing')
    for c in range(200):
        if not (root/f'runs/twoscale_test/cpu_{c:03d}.npz').exists():return None,'waiting for complete approved two-scale truth'
        for name in names:
            path=root/f'runs/twoscale_test/{name}_{c:03d}.npz';meta=path.with_suffix('.json')
            if not path.exists() or not meta.exists():return None,'waiting for two-scale raw inference '+name
            record=json.loads(meta.read_text())
            if record.get('checkpoint_sha256')!=selection['models'][name]['sha256']:raise ValueError('two-scale checkpoint mismatch '+str(meta))
    compute_path=root/'runs/statistics_compute_metadata.json'
    if not compute_path.exists():return None,'waiting for public two-scale compute receipts'
    compute=json.loads(compute_path.read_text())
    if any(n not in compute['training'] for n in names):return None,'waiting for all public two-scale terminal phase receipts'
    return dict(selection=selection,path=selection_path,approval=approval,names=['N2','N2-offline','N2-noclosure']+names),'ready'


def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--authorization',required=True);p.add_argument('--watch',action='store_true');a=p.parse_args()
    status=a.root/'runs/stage2b_statistics_status.json'
    while True:
        scope=a.root/'runs/final_scope_status.json'
        if scope.exists() and json.loads(scope.read_text()).get('two_scale')=='not_run':
            write_json(status,dict(status='NOT_RUN_AT_AUTHORIZED_CUTOFF',at=now(),role='statistics only'));return
        ready,reason=readiness(a.root)
        write_json(status,dict(status='READY' if ready else 'WAITING',at=now(),reason=reason,role='statistics only',test_access_authorization=a.authorization))
        if ready:break
        if not a.watch:return
        time.sleep(30)
    from assemble_metrics import assemble
    rows,result=assemble(a.root,a.root/'runs/2b_case_rows.json',ready['names'],a.authorization,stage='2b',selected=ready['selection']['selected_L'],two_scale=True,intervals=True,fixed_action=ready['selection']['best_fixed_action'])
    result['selection_completed_at']=ready['selection']['selection_completed_at'];result['selection_manifest']=str(ready['path'].relative_to(a.root));result['cuts']=ready['selection'].get('cuts',[]);result['not_run']=ready['selection'].get('not_run',[])
    for path in [ready['path'],ready['approval']]:result['source_hashes'][str(path.relative_to(a.root))]=digest(path)
    write_json(a.root/'runs/2b_metrics_cases.json',dict(cases=rows));write_json(a.root/'runs/2b_metrics.json',result)
    subprocess.run([sys.executable,str(a.root/'full_report.py'),'--root',str(a.root),'--stage','2b'],check=True)
    write_json(status,dict(status='REGISTERED',at=now(),role='statistics only',NUMBERS_fragment='NUMBERS_FULL_METRICS_STAGE2B.md',reading='AFD_STAGE2B_READING.md',factual_audit='OPEN'))
if __name__=='__main__':main()
