"""Durable CPU statistics coordinator. Never trains or selects a checkpoint.

Consumes FINAL validation-selected manifest and complete inference registry.
No Stage-1 gate reading/report is opened. Wait status is resumable on disk.
"""
import argparse,datetime,json,time,subprocess,sys
from pathlib import Path
from protocol import ROOT,write_json,digest,ORDER
import math
def reject_nonfinite(value):
    if isinstance(value,dict):
        for v in value.values():reject_nonfinite(v)
    elif isinstance(value,list):
        for v in value:reject_nonfinite(v)
    elif isinstance(value,float) and not math.isfinite(value):raise ValueError('nonfinite manifest')


def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()


def readiness(root,selection_path,inference_path):
    from evaluation_hold import hold_active
    if hold_active(root):return None,'Stage2 test reading held pending Todd decision'
    if not selection_path.exists():return None,'waiting for FINAL validation-selection consumer manifest'
    selection=json.loads(selection_path.read_text());reject_nonfinite(selection)
    if selection.get('status')!='FINAL':return None,'selection consumer manifest is not FINAL'
    if selection.get('system')!='one-scale':raise ValueError('wrong selection system')
    if not selection.get('selection_completed_at'):raise ValueError('selection timestamp missing')
    selected=selection['selected_L'];S=selection['S']
    if selected not in S or any(n not in ORDER for n in S):raise ValueError('invalid frozen selection candidate set')
    if not inference_path.exists():return None,'waiting for inference registry'
    inference=json.loads(inference_path.read_text());reject_nonfinite(inference)
    if inference.get('stage')!=2 or not inference.get('complete'):return None,'Stage-2 inference registry incomplete'
    model_names=list(dict.fromkeys(['CNN-20k']+list(selection['models'])))
    required={'CNN-20k','CNN-roll','CNN-R2','CNN-cost','CNN-resp'}
    if not required.issubset(model_names):raise ValueError('mandatory model missing; no full Stage-2 gate')
    if set(S)!=set(n for n in model_names if n in ORDER):raise ValueError('FINAL S differs from available frozen candidate set')
    for name in model_names:
        if name!='CNN-20k':
            record=inference['arms'].get(name)
            if not record or not record.get('complete') or record.get('test')!='complete':return None,'inference incomplete for '+name
            if record['checkpoint_sha256']!=selection['models'][name]['sha256']:raise ValueError('selection/inference checkpoint mismatch '+name)
        expected=selection['models'].get(name,{}).get('sha256')
        if expected is None and name=='CNN-20k':expected=digest(root/'inputs/CNN-20k.pt')
        for c in range(200):
            path=root/f'runs/test/{name}_{c:03d}.npz';meta=root/f'runs/test/{name}_{c:03d}.json'
            if not path.exists() or not meta.exists():return None,'waiting for raw output '+name+' case '+str(c)
            record=json.loads(meta.read_text())
            if record.get('checkpoint_sha256')!=expected:raise ValueError('raw output checkpoint mismatch '+str(meta))
    compute_path=root/'runs/statistics_compute_metadata.json'
    if not compute_path.exists():return None,'waiting for public recorded-phase compute receipts'
    compute=json.loads(compute_path.read_text())
    for name in model_names:
        if name!='CNN-20k' and name not in compute['training']:return None,'waiting for public terminal GPU phase receipt '+name
    names=['N-last','N-oracle']+model_names
    for name in ['N-mis','N-win']:
        if all((root/f'runs/test/{name}_{c:03d}.npz').exists() for c in range(200)):names.append(name)
    return dict(selection=selection,inference=inference,names=names),'ready'


def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--selection',type=Path);p.add_argument('--inference',type=Path);p.add_argument('--authorization',required=True);p.add_argument('--watch',action='store_true');a=p.parse_args()
    selection_path=a.selection or a.root/'runs/training/final_selection_stage2.json';inference_path=a.inference or a.root/'runs/stage2_inference/manifest.json'
    status=a.root/'runs/stage2_statistics_status.json'
    while True:
        ready,reason=readiness(a.root,selection_path,inference_path)
        write_json(status,dict(status='READY' if ready else 'WAITING',at=now(),reason=reason,role='statistics only',selection=str(selection_path),inference=str(inference_path),test_access_authorization=a.authorization))
        if ready:break
        print(reason,flush=True)
        if not a.watch:return
        time.sleep(30)
    from evaluation_hold import require_test_release
    require_test_release(a.root)
    from assemble_metrics import assemble
    rows,result=assemble(a.root,a.root/'runs/stage1_cases.json',ready['names'],a.authorization,stage='2',selected=ready['selection']['selected_L'],intervals=True,fixed_action=ready['selection'].get('best_fixed_action'))
    require_test_release(a.root)
    result['selection_completed_at']=ready['selection']['selection_completed_at'];result['selection_manifest']=str(selection_path.relative_to(a.root));result['inference_manifest']=str(inference_path.relative_to(a.root));result['cuts']=ready['selection'].get('cuts',[]);result['not_run']=ready['selection'].get('not_run',[])
    result['source_hashes'][str(selection_path.relative_to(a.root))]=digest(selection_path);result['source_hashes'][str(inference_path.relative_to(a.root))]=digest(inference_path)
    write_json(a.root/'runs/2_metrics_cases.json',dict(cases=rows));write_json(a.root/'runs/2_metrics.json',result)
    # Report registration runs only after independent arithmetic/source checks.
    from full_report import check
    checker=check(dict(cases=rows),result,a.root);write_json(status,dict(status='CHECKED',at=now(),checker=checker,full_report_command='python full_report.py --stage 2',role='statistics only'))
    subprocess.run([sys.executable,str(a.root/'full_report.py'),'--root',str(a.root),'--stage','2'],check=True)
    write_json(status,dict(status='REGISTERED',at=now(),role='statistics only',NUMBERS_fragment='NUMBERS_FULL_METRICS_STAGE2.md',reading='AFD_STAGE2_READING.md',checker=checker,remaining='Root merges NUMBERS fragment, renders checked figures locally, and obtains independent factual audit. Stage2b requires its separate approved sampler go.'))
    gate=result['primary']['gate']
    if gate['sufficiency'] and gate['H1a']=='KILL':
        write_json(a.root/'runs/campaign_control.json',dict(execution='stop',recorded_at=now(),authority='WO v5.2 §7.6',reason='Stage2 H1a KILL; stop campaign and write findings harvest',checked_evidence='runs/2_metrics_checker.json',evidence_sha256=digest(a.root/'runs/2_metrics_checker.json')))
        write_json(status,dict(status='KILL_REGISTERED',at=now(),role='statistics only',findings_harvest='Required; root coordinator writes vault findings from checked records'))
        return
    print('Stage-2 reading registered; full campaign is not declared complete',flush=True)
    # Descriptive secondary results cannot license a sentence or influence L*.
    secondary_names=[name for name in ready['names'] if not name.endswith('-cost') and
        (name in ['N-last','N-oracle'] or all((a.root/f'runs/test2/{name}_{c:03d}.npz').exists() for c in range(100)))]
    fixed=ready['selection'].get('best_fixed_action')
    if fixed is not None and all((a.root/f'runs/test2/cpu_{c:03d}.npz').exists() for c in range(100)):
        secondary_rows,secondary_result=assemble(a.root,a.root/'runs/secondary_case_rows.json',secondary_names,a.authorization,stage='secondary',intervals=True,panel='test2',fixed_action=fixed)
        secondary_result['selection_completed_at']=ready['selection']['selection_completed_at']
        secondary_result['selection_manifest']=str(selection_path.relative_to(a.root))
        secondary_result['source_hashes'][str(selection_path.relative_to(a.root))]=digest(selection_path)
        secondary_result['not_run']=[name for name in ready['names'] if not name.endswith('-cost') and name not in secondary_names]
        write_json(a.root/'runs/secondary_metrics_cases.json',dict(cases=secondary_rows));write_json(a.root/'runs/secondary_metrics.json',secondary_result)
        subprocess.run([sys.executable,str(a.root/'full_report.py'),'--root',str(a.root),'--stage','secondary'],check=True)
        write_json(a.root/'runs/secondary_statistics_status.json',dict(status='REGISTERED',at=now(),role='statistics only',gate=None,licensed_sentences=[]))
if __name__=='__main__':
    try:main()
    except Exception as exc:
        write_json(ROOT/'runs/stage2_statistics_status.json',dict(status='FAILED',at=now(),error=repr(exc),role='statistics only'))
        raise
