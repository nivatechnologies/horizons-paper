"""Fresh-panel Stage 9 F5 adapter. No hidden history or outcome is opened."""
import os
os.environ.update(JAX_PLATFORMS='cpu', JAX_ENABLE_X64='true',
                  OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', NUMBA_NUM_THREADS='4')
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from acd_stage19_part2_gate import ROOT, OUT, digest, freeze_ready


def atomic_npz(path, **arrays):
    tmp = path.with_suffix('.tmp.npz')
    np.savez_compressed(tmp, **arrays)
    tmp.replace(path)


def prepare():
    freeze_ready()
    from acd_protocol import SIGMA, PATTERNS, WINDOWS, physics
    from numba import set_num_threads
    set_num_threads(4)
    target = OUT / 'inference_inputs'
    target.mkdir(parents=True, exist_ok=True)
    settings = dict(sigma=float(SIGMA), patterns=np.asarray(PATTERNS).tolist(),
                    windows=[np.asarray(w).tolist() for w in WINDOWS])
    (target / 'settings.json').write_text(json.dumps(settings, indent=2) + '\n')
    for case in range(200):
        source = OUT / f'main_forecast_{case:03d}.npz'
        output = target / f'{case:03d}.npz'
        receipt = output.with_suffix('.json')
        if output.exists() and receipt.exists():
            old = json.loads(receipt.read_text())
            if digest(output) == old['sha256'] and digest(source) == old['source_sha256']:
                continue
            raise RuntimeError(f'History hash mismatch for case {case}')
        with np.load(source) as data:
            theta = data['theta'].copy()
        forcing = theta[:, 40].copy()
        history = physics.simulate(theta[:, :40], np.repeat(forcing[:, None], 40, 1), .01, 11)
        atomic_npz(output, H=history, F=forcing)
        receipt.write_text(json.dumps(dict(case=case, draws=len(theta), sha256=digest(output),
                                          source_sha256=digest(source),
                                          construction='Each retained draw own noise-free history from first frame.'), indent=2) + '\n')
        print('history', case, len(theta), flush=True)


def run(name, checkpoint, micro):
    freeze = freeze_ready()
    contract = json.loads((ROOT / 'receipts/acd_stage19_freeze_b.json').read_text())
    if digest(checkpoint) != contract['checkpoints'][name]:
        raise RuntimeError('Checkpoint differs from Freeze B')
    from acd_stage19_part2_gate import gpu_inventory
    visible = os.environ.get('CUDA_VISIBLE_DEVICES')
    cards = gpu_inventory()
    card = next((c for c in cards if c['uuid'] == visible or str(c['index']) == visible), None)
    if card is None or card['processes']:
        raise RuntimeError('Inference needs one recorded free Baccus GPU')
    data = OUT / 'inference_inputs'
    output = OUT / 'inference' / name
    output.mkdir(parents=True, exist_ok=True)
    manifest = output / 'hashes.json'
    hashes = json.loads(manifest.read_text()) if manifest.exists() else {}
    for existing in output.glob('[0-9][0-9][0-9].npz'):
        if existing.name not in hashes or digest(existing) != hashes[existing.name]:
            # An interrupted write is regenerated, never silently trusted.
            existing.unlink()
    import acd_stage9_cnn as inherited
    original_save = inherited.np.savez_compressed

    def saved(path, **arrays):
        path = Path(path)
        tmp = path.with_suffix('.tmp.npz')
        original_save(tmp, **arrays)
        tmp.replace(path)
        hashes[path.name] = digest(path)
        pending = manifest.with_suffix('.tmp.json')
        pending.write_text(json.dumps(hashes, indent=2) + '\n')
        pending.replace(manifest)

    inherited.np.savez_compressed = saved
    try:
        inherited.run(name, checkpoint, data, output, micro)
    finally:
        inherited.np.savez_compressed = original_save
    complete = json.loads((output / 'complete.json').read_text())
    complete.update(freeze_b_commit=freeze['commit'], gpu_inventory_before=card,
                    output_hashes=hashes, cases=len(hashes), fresh_panel=True)
    (output / 'complete.json').write_text(json.dumps(complete, indent=2) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['prepare', 'run'])
    parser.add_argument('--model', choices=['CNN-F', 'CNN-noF', 'CNN-20k'])
    parser.add_argument('--checkpoint', type=Path)
    parser.add_argument('--micro', type=int, default=256)
    args = parser.parse_args()
    if args.mode == 'prepare':
        prepare()
    else:
        run(args.model, args.checkpoint, args.micro)
