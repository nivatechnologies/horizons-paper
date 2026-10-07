"""Frozen C3 validation-only response-weight selection; no panel files allowed."""
import argparse
import json
from pathlib import Path
import numpy as np
import torch
from acd_stage9_cnn import Emulator
from acd_stage18_inference import guarded, OUT, digest


def select(data, training, settings, micro):
    guarded()
    manifest = json.loads((data/'manifest.json').read_text())
    for name, expected in manifest['data_sha256'].items():
        if digest(data/name) != expected:
            raise RuntimeError('Generated validation/training data hash mismatch')
    if digest(data/'validation_reference.npz') != manifest['validation_reference_sha256']:
        raise RuntimeError('Validation reference hash mismatch')
    cfg = json.loads(settings.read_text())
    sigma = cfg['sigma']
    patterns = np.asarray(cfg['patterns'])
    window = cfg['windows'][3]
    with np.load(data/'val.npz') as source:
        history = source['H'].copy()
    with np.load(data/'validation_reference.npz') as source:
        reference = source['J'][:, :, 3].copy()
    torch.set_num_threads(4)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    rows = []
    for weight in [0., .01, .03, .1, .3, 1.]:
        directory = training/f'CNN-noF-response-{weight:g}-seed1'
        meta = json.loads((directory/'complete.json').read_text())
        checkpoint = directory/'selected.pt'
        model = Emulator().cuda().eval()
        model.load_state_dict(torch.load(checkpoint, map_location='cpu', weights_only=True)['state_dict'])
        result = np.zeros((len(history), 9))
        with torch.no_grad():
            for b in range(0, len(history)*9, micro):
                ids = np.arange(b, min(b+micro, len(history)*9))
                draw, action = ids//9, ids%9
                ctx = torch.tensor(history[draw], device='cuda', dtype=torch.float32)
                a = torch.tensor(.16*patterns[action]/sigma, device='cuda', dtype=torch.float32)
                for tick in range(max(window)+1):
                    state = ctx[:, -1].to(torch.float64)*sigma
                    if tick in window:
                        result[draw, action] += (.5*state.square().mean(-1)/len(window)).cpu().numpy()
                    if tick < max(window):
                        ctx = torch.cat([ctx[:, 1:], model(ctx, a)[:, None]], 1)
        error = (result[:, :8]-result[:, 8, None])-(reference[:, :8]-reference[:, 8, None])
        rows.append(dict(weight=weight, model=directory.name, validation_state_MSE=meta['validation_MSE'],
                         validation_effect_RMSE=float(np.sqrt(np.mean(error**2))),
                         checkpoint_sha256=digest(checkpoint)))
    baseline = rows[0]['validation_state_MSE']
    eligible = [row for row in rows if row['validation_state_MSE'] <= 1.1*baseline and np.isfinite(row['validation_effect_RMSE'])]
    chosen = min(eligible, key=lambda row: (row['validation_effect_RMSE'], row['weight']))
    result = dict(rows=rows, selected=chosen, validation_amplitude=.16, lead=2.,
                  validation_cases=len(history), patterns='all eight',
                  rule='minimum effect RMSE among state MSE at most 1.1 times w=0; smallest weight on ties')
    (OUT/'C_selection.json').write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--data', type=Path, required=True)
    p.add_argument('--training', type=Path, required=True)
    p.add_argument('--settings', type=Path, required=True)
    p.add_argument('--micro', type=int, default=256)
    a = p.parse_args()
    select(a.data, a.training, a.settings, a.micro)
