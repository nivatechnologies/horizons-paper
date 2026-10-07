"""JVP through actual learned rollouts; FP32 networks and float64 energies, no truth."""
import argparse
import json
from pathlib import Path
import numpy as np
import torch
from acd_stage9_cnn import Emulator, ForcingModel
from acd_stage18_estimators import Estimator
from acd_stage18_inference import OUT, guarded, digest


def run(name, checkpoint, inputs, micro, conditioned=False, estimator=None):
    guarded()
    torch.set_num_threads(4)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    settings = json.loads((inputs/'settings.json').read_text())
    sigma = settings['sigma']
    patterns = torch.tensor(settings['patterns'][:8], device='cuda', dtype=torch.float32)
    windows = settings['windows']
    last = max(max(w) for w in windows)
    model = ForcingModel() if conditioned or estimator else Emulator()
    model.load_state_dict(torch.load(checkpoint, map_location='cpu', weights_only=True)['state_dict'])
    model.cuda().eval()
    if estimator:
        est = Estimator().cuda().eval()
        est.load_state_dict(torch.load(estimator, map_location='cpu', weights_only=True)['state_dict'])
    output = OUT/'derivatives'/name
    output.mkdir(parents=True, exist_ok=True)
    hashes = json.loads((output/'hashes.json').read_text()) if (output/'hashes.json').exists() else {}
    for case in range(200):
        target = output/f'{case:03d}.npz'
        if target.exists() and hashes.get(target.name) == digest(target):
            continue
        with np.load(inputs/f'{case:03d}.npz') as data:
            history, forcing = data['H'].copy(), data['F'].copy()
        result = np.empty((len(history), 8, len(windows)))
        batch = micro
        b = 0
        while b < len(history)*8:
            ids = np.arange(b, min(b+batch, len(history)*8))
            draw, action = ids//8, ids%8
            h = torch.tensor(history[draw]/sigma, device='cuda', dtype=torch.float32)
            f = torch.tensor((forcing[draw]-8)/2, device='cuda', dtype=torch.float32)
            if estimator:
                with torch.no_grad():
                    f = est(h)
            p = patterns[action]

            def rollout(amplitude):
                ctx = h
                cost = torch.zeros((len(ids), len(windows)), device='cuda', dtype=torch.float64)
                a = amplitude*p/sigma
                for tick in range(last+1):
                    state = ctx[:, -1].to(torch.float64)*sigma
                    energy = .5*state.square().mean(-1)
                    for lead, window in enumerate(windows):
                        if tick in window:
                            addition = torch.zeros_like(cost)
                            addition[:, lead] = energy/len(window)
                            cost = cost+addition
                    if tick < last:
                        pred = model(ctx, a, f) if conditioned or estimator else model(ctx, a)
                        ctx = torch.cat([ctx[:, 1:], pred[:, None]], 1)
                return cost
            try:
                with torch.no_grad():
                    zero = torch.zeros((), device='cuda', dtype=torch.float32)
                    _, tangent = torch.func.jvp(rollout, (zero,), (torch.ones_like(zero),))
                result[draw, action] = tangent.cpu().numpy()
                b += len(ids)
            except torch.cuda.OutOfMemoryError:
                torch.cuda.empty_cache()
                batch //= 2
                if batch < 1:
                    raise
        pending = target.with_suffix('.tmp.npz')
        np.savez_compressed(pending, G=result)
        pending.replace(target)
        hashes[target.name] = digest(target)
        (output/'hashes.json').write_text(json.dumps(hashes, indent=2)+'\n')
        print(name, 'JVP', case, len(history), batch, flush=True)
    (output/'complete.json').write_text(json.dumps(dict(model=name, checkpoint_sha256=digest(checkpoint),
                     estimator_sha256=digest(estimator) if estimator else None, output_hashes=hashes,
                     gpu=torch.cuda.get_device_name(), network_dtype='float32', energy_dtype='float64'), indent=2)+'\n')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--name', required=True)
    p.add_argument('--checkpoint', type=Path, required=True)
    p.add_argument('--inputs', type=Path, required=True)
    p.add_argument('--micro', type=int, default=256)
    p.add_argument('--conditioned', action='store_true')
    p.add_argument('--estimator', type=Path)
    a = p.parse_args()
    run(a.name, a.checkpoint, a.inputs, a.micro, a.conditioned, a.estimator)
