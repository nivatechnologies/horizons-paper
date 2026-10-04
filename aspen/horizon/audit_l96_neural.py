"""Audit completed retained neural artifacts without another model rollout."""
import json
import numpy as np
from common import ROOT, GRID, write_json, sha


def main():
    root = ROOT/'runs/l96'
    completion = json.loads((root/'learned/evaluation_complete.json').read_text())
    training = json.loads((root/'learned/training.json').read_text())
    calibration = json.loads((ROOT/'results/l96_calibration.json').read_text())
    assert completion['cases'] == 200
    assert training['steps_done'] == 20000
    expected_times = np.rint(GRID/calibration['system']['lambda_mean']/.05)*.05
    times = []; drops = []; sources = set(); steps = set()
    climate = np.load(root/'test/climatology.npy')[:, None, :]
    physical_floor_changes = 0; learned_floor_changes = 0
    for c in range(200):
        path = root/f'test/neural_{c:03d}'
        record = json.loads(path.with_suffix('.json').read_text())
        with np.load(path.with_suffix('.npz')) as data:
            valid = data['valid']
            assert valid.dtype == np.bool_ and valid.shape == (256,), c
            assert data['cost'].shape == (8, 256, len(GRID)), c
            assert data['mean_snap'].shape == (8, len(GRID), 40), c
            assert np.isfinite(data['cost'][:, valid]).all(), c
            assert np.isnan(data['cost'][:, ~valid]).all(), c
            if valid[:64].any():
                assert np.isfinite(data['mean_snap']).all(), c
                target = np.load(root/f'test/neural_target_{c:03d}.npy')
                ob = np.sum((target-climate)**2, axis=-1)
                fa = np.sum((data['mean_snap']-climate)**2, axis=-1)
                learned_floor_changes += int(((ob>0)&(fa>0)&(fa>=1e-24*ob)&(fa<1e-12*ob)).sum())
            else:
                assert np.isnan(data['mean_snap']).all(), c
            assert np.array_equal(data['actual_snapshot_times'], expected_times), c
            steps.add(int(data['checkpoint_step']))
            drops.append(int((~valid).sum()))
            assert record['dropped'] == drops[-1], c
            assert record['dropped_first64'] == int((~valid[:64]).sum()), c
        assert record['case'] == c and record['device'] == 'cuda:0', c
        assert record['tf32'] is False and record['deterministic_cudnn'] is True, c
        assert record['threads'] == 1 and record['seconds'] > 0, c
        sources.add(record['git_sha']); times.append(record['seconds'])
        with np.load(root/f'test/case_{c:03d}.npz') as physical:
            ob = np.sum((physical['actual_snap']-climate)**2, axis=-1)
            for arm in ['paired', 'unpaired', 'jitter', 'misidentified']:
                fa = np.sum((physical[arm+'_mean_snap']-climate)**2, axis=-1)
                physical_floor_changes += int(((ob>0)&(fa>0)&(fa>=1e-24*ob)&(fa<1e-12*ob)).sum())
    # Physical summaries predate the corrected squared-norm cutoff.
    # Require reaggregation if any retained value would change.
    assert physical_floor_changes == 0, physical_floor_changes
    assert sources == {completion['git_sha']}, sources
    assert steps == {completion['checkpoint_step']}, steps
    assert len(next(iter(sources))) == 40
    write_json(ROOT/'results/l96_neural_artifact_audit.json', dict(
        status='PASS', cases=200, attempted_members=200*256, dropped=sum(drops),
        numerical_source_sha=completion['git_sha'], checkpoint_step=completion['checkpoint_step'],
        device='cuda:0', tf32=False, deterministic_cudnn=True,
        total_case_seconds=sum(times), mean_case_seconds=float(np.mean(times)),
        physical_norm_floor_values_changed=physical_floor_changes,
        learned_values_differing_from_old_norm_floor=learned_floor_changes,
        git_sha=sha(), note='Retained artifact audit; no new evaluation or scientific threshold.'))
    print('L96 neural artifact audit: 200 consistent CUDA cases', flush=True)


if __name__ == '__main__':
    main()
