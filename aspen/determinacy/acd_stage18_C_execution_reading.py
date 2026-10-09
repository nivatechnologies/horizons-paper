"""Descriptive C validation and shared-label reporting from saved receipts; no outcomes."""
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
OUT = ROOT/'runs/stage18'
HEADING = '\n## Part C execution reading\n'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run():
    selection = json.loads((OUT/'C_selection.json').read_text())
    baseline = next(r for r in selection['rows'] if r['weight'] == 0.)
    assert selection['selected']['model'] == baseline['model']
    controller = ROOT/'acd_stage18_response_controller.py'
    source = controller.read_text()
    assert 'weights = list(dict.fromkeys([0., chosen[\'weight\']]))' in source
    assert 'for model in dict.fromkeys(models):' in source
    rows = []
    for row in selection['rows']:
        directory = OUT/'training'/row['model']
        meta = json.loads((directory/'complete.json').read_text())
        assert sha(directory/'selected.pt') == row['checkpoint_sha256'] == meta['selected_sha256']
        record = dict(row, validation_state_MSE_ratio_to_weight_zero=row['validation_state_MSE']/baseline['validation_state_MSE'],
                      selected_step=meta['selected_step'], guard_abort=meta['abort'], scope='descriptive validation only',
                      training_receipt_path=str((directory/'complete.json').relative_to(ROOT)))
        if meta['abort']:
            last = max(directory.glob('checkpoint_*.pt'))
            check = json.loads((OUT/'C_last_saved_identity.json').read_text())[row['model']]
            assert check['state_equal'] and check['validation_equal']
            assert check['selected_sha256'] == sha(directory/'selected.pt') and check['last_saved_sha256'] == sha(last)
            record['last_saved_identity'] = check
            record.update(checkpoint_scope='last saved checkpoint; also validation-selected', last_saved_checkpoint_path=str(last.relative_to(ROOT)))
        else:
            record['checkpoint_scope'] = 'validation-selected checkpoint'
        rows.append(record)
    ready = OUT/'C_reading_ready.json'
    status = json.loads(ready.read_text()) if ready.exists() else None
    names = status['completed_models'] if status else [baseline['model']]
    shared = [n for n in names if n.startswith('CNN-noF-response-0-seed')]
    receipt = dict(post_hoc=True, licenses_frozen_route=False, criteria_unchanged=True,
        R_other='Selected weight is zero. Selected and weight-zero labels refer to the same model. If the frozen extra-seed trigger fires, train each further seed once and report that run under both labels; no duplicate training, inference, scoring or GPU charge.',
        code_hashes={controller.name:sha(controller), Path(__file__).name:sha(Path(__file__))},
        selection_source='runs/stage18/C_selection.json', selection_source_sha256=sha(OUT/'C_selection.json'),
        validation_rows=rows, extra_seed_trigger=status['extra_seed_trigger'] if status else None,
        extra_seed_trigger_status='scored' if status else 'pending confirmation scoring',
        reporting_labels={'weight zero':shared, 'selected':shared})
    path = ROOT/'receipts/acd_stage18_C_execution_reading.json'
    path.write_text(json.dumps(receipt, indent=2, allow_nan=False)+'\n')
    body = HEADING+'\nR-other execution reading: '+receipt['R_other']+' Criteria unchanged. Frozen training, validation selection, extra-seed trigger, populations and scoring are unchanged. Shared labels do not represent independent runs.\n\n'
    body += '| Weight | Checkpoint step | Guard abort | Validation state MSE / weight zero | Validation effect RMSE |\n|---:|---:|---|---:|---:|\n'
    for r in rows:
        body += f"| {r['weight']:g} | {r['selected_step']} | {r['guard_abort'] or 'none'} | {r['validation_state_MSE_ratio_to_weight_zero']:.8g} | {r['validation_effect_RMSE']:.8g} |\n"
    body += '\nAll validation rows are descriptive only. Guard-aborted rows use the last saved checkpoint, verified tensor-for-tensor to equal the validation-selected model, with identical step and validation MSE; container SHA-256s differ because the trainer serializes the two files separately. Other rows use the validation-selected checkpoint. These additions do not rerun selection. Source values, checkpoint identities and reporting-label aliases are in receipts/acd_stage18_C_execution_reading.json.\n\n'
    body += 'Extra-seed trigger: '+('pending confirmation scoring' if status is None else str(status['extra_seed_trigger']))+'.\n\n'
    body += '| Reporting label | Shared run identities |\n|---|---|\n'
    for label, runs in receipt['reporting_labels'].items():
        body += '| '+label+' | '+', '.join(runs)+' |\n'
    reading = ROOT/'ACD_STAGE18_READING.md'
    text = reading.read_text()
    if HEADING in text:
        start = text.index(HEADING)
        end = text.find('\n## ',start+len(HEADING))
        text = text[:start]+(text[end:] if end != -1 else '')
    reading.write_text(text.rstrip()+'\n'+body)
    return receipt

def verify_last_saved():
    import torch
    rows = {}
    selection = json.loads((OUT/'C_selection.json').read_text())
    for row in selection['rows']:
        directory = OUT/'training'/row['model']
        meta = json.loads((directory/'complete.json').read_text())
        if not meta['abort']:
            continue
        p, q = directory/'selected.pt', max(directory.glob('checkpoint_*.pt'))
        a, b = [torch.load(f,map_location='cpu',weights_only=True) for f in (p,q)]
        check = dict(selected_step=a['step'],last_saved_step=b['step'],
                     state_equal=a['state_dict'].keys()==b['state_dict'].keys() and all(torch.equal(a['state_dict'][k],b['state_dict'][k]) for k in a['state_dict']),
                     validation_equal=a['validation_MSE']==b['validation_MSE'],
                     selected_sha256=sha(p),last_saved_sha256=sha(q))
        assert check['state_equal'] and check['validation_equal'] and check['selected_step']==check['last_saved_step']
        rows[row['model']] = check
    (OUT/'C_last_saved_identity.json').write_text(json.dumps(rows,indent=2)+'\n')

if __name__ == '__main__':
    import sys
    if '--verify-last-saved' in sys.argv:
        verify_last_saved()
    else:
        print(json.dumps(run(),indent=2))
