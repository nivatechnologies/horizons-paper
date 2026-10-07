"""Stage18 information interventions and persistent-context pipelines; no truth access."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent
OUT = ROOT/'runs/stage18'


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def guarded():
    freeze = json.loads((ROOT/'receipts/acd_stage18_freeze.json').read_text())
    marker = json.loads((OUT/'freeze_pushed.json').read_text())
    if digest(ROOT/'ACD_STAGE18_FREEZE.md') != marker['sha256']:
        raise RuntimeError('Stage18 freeze changed')
    for name, expected in freeze['code_hashes'].items():
        if digest(ROOT/name) != expected:
            raise RuntimeError('Stage18 implementation hash differs: '+name)
    return freeze


def prepare_A():
    freeze = guarded()
    source = OUT/'confirmation_inputs'
    for arm in ['ownF', 'meanF', 'constantF', 'permutedF']:
        target = OUT/'A_inputs'/arm
        target.mkdir(parents=True, exist_ok=True)
        (target/'settings.json').write_bytes((source/'settings.json').read_bytes())
        for case in range(200):
            path = target/f'{case:03d}.npz'
            if path.exists():
                continue
            with np.load(source/f'{case:03d}.npz') as data:
                history, forcing = data['H'].copy(), data['F'].copy()
            if arm == 'meanF':
                forcing.fill(forcing.mean())
            elif arm == 'constantF':
                forcing.fill(8.)
            elif arm == 'permutedF':
                rng = np.random.default_rng(np.random.SeedSequence([freeze['namespace_id'], 2, case]))
                forcing = rng.permutation(forcing)
            pending = path.with_suffix('.tmp.npz')
            np.savez_compressed(pending, H=history, F=forcing)
            pending.replace(path)


def run(name, data, checkpoint, micro, estimator=None, estimator_kind=None, rolling=False):
    freeze = guarded()
    import acd_stage9_cnn as original
    from acd_stage18_estimators import Estimator
    import torch
    settings = json.loads((data/'settings.json').read_text())
    horizon = max(max(w) for w in settings['windows'])
    estimates = []
    baseclass = original.ForcingModel
    if estimator is not None:
        est = Estimator(estimator_kind == 'E1').cuda().eval()
        ck = torch.load(estimator, map_location='cpu', weights_only=True)
        est.load_state_dict(ck['state_dict'])

        class Pipeline(baseclass):
            def __init__(self):
                super().__init__()
                self.calls = 0
                self.fixed = None

            def forward(self, H, A, F):
                if self.calls % horizon == 0:
                    self.fixed = est(H, A)
                    estimates.append(self.fixed.detach().cpu().numpy())
                forcing = est(H, A) if rolling else self.fixed
                self.calls += 1
                return super().forward(H, A, forcing)

        original.ForcingModel = Pipeline
    output = OUT/'inference'/name
    output.mkdir(parents=True, exist_ok=True)
    manifest = output/'hashes.json'
    hashes = json.loads(manifest.read_text()) if manifest.exists() else {}
    for path in output.glob('[0-9][0-9][0-9].npz'):
        if hashes.get(path.name) != digest(path):
            path.unlink()
    save = original.np.savez_compressed

    def saved(path, **arrays):
        path = Path(path)
        pending = path.with_suffix('.tmp.npz')
        if estimator is not None:
            arrays['estimated_F_at_cutoff'] = np.concatenate(estimates)*2+8
            estimates.clear()
        save(pending, **arrays)
        pending.replace(path)
        hashes[path.name] = digest(path)
        tmp = manifest.with_suffix('.tmp.json')
        tmp.write_text(json.dumps(hashes, indent=2)+'\n')
        tmp.replace(manifest)

    original.np.savez_compressed = saved
    empty_cache = torch.cuda.empty_cache
    if estimator is not None:
        original_init = Pipeline.__init__
        instances = []
        def initialized(self):
            original_init(self)
            instances.append(self)
        Pipeline.__init__ = initialized
        def reset_after_oom():
            for instance in instances:
                instance.calls, instance.fixed = 0, None
            estimates.clear()
            empty_cache()
        torch.cuda.empty_cache = reset_after_oom
    try:
        original.run(name, checkpoint, data, output, micro)
    finally:
        original.ForcingModel = baseclass
        original.np.savez_compressed = save
        torch.cuda.empty_cache = empty_cache
    result = json.loads((output/'complete.json').read_text())
    result.update(output_hashes=hashes, cases=len(hashes), gpu_visible_devices=os.environ.get('CUDA_VISIBLE_DEVICES'),
                  estimator_sha256=digest(estimator) if estimator else None,
                  estimator_kind=estimator_kind, reestimate_every_step=rolling,
                  post_hoc=True, licenses_frozen_route=False)
    (output/'complete.json').write_text(json.dumps(result, indent=2)+'\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['prepare_A', 'run'])
    parser.add_argument('--name')
    parser.add_argument('--data', type=Path)
    parser.add_argument('--checkpoint', type=Path)
    parser.add_argument('--micro', type=int, default=256)
    parser.add_argument('--estimator', type=Path)
    parser.add_argument('--estimator-kind', choices=['E0', 'E1'])
    parser.add_argument('--rolling', action='store_true')
    args = parser.parse_args()
    if args.mode == 'prepare_A':
        prepare_A()
    else:
        run(args.name, args.data, args.checkpoint, args.micro, args.estimator, args.estimator_kind, args.rolling)
