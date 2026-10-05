"""Persistent Todd-controlled hold on Stage 2/2b test readings."""
import json


def hold_active(root):
    path=root/'runs/stage2_test_hold.json'
    if not path.exists():return False
    record=json.loads(path.read_text())
    # Absence of elapsed time, a finished model, or a stopped service releases nothing.
    return not (record.get('status')=='RELEASED' and record.get('released_by')=='Todd')


def require_test_release(root):
    if hold_active(root):raise PermissionError('Stage 2/2b test reading held until Todd explicitly releases runs/stage2_test_hold.json')
