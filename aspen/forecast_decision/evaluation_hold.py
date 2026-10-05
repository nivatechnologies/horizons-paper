"""Persistent Todd-controlled hold on Stage 2/2b test readings."""
import json


def hold_active(root):
    # Closure supersedes the earlier resumable hold for this work order.
    if (root/'runs/closure/control.json').exists():return True
    training=root/'runs/training/closure_control.json'
    if training.exists() and json.loads(training.read_text()).get('campaign_closed') is True:return True
    path=root/'runs/stage2_test_hold.json'
    if not path.exists():return False
    record=json.loads(path.read_text())
    # Absence of elapsed time, a finished model, or a stopped service releases nothing.
    return not (record.get('status')=='RELEASED' and record.get('released_by')=='Todd')


def require_test_release(root):
    if hold_active(root):raise PermissionError('Stage 2/2b test reading prohibited by closure or held until Todd explicitly releases the active work order')
