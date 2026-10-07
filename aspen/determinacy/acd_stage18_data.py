"""Panel-disjoint response-control generation; refuse generation on Baccus."""
import os
os.environ.update(NUMBA_NUM_THREADS='4', OPENBLAS_NUM_THREADS='1', JAX_PLATFORMS='cpu')
import hashlib
import json
import socket
from pathlib import Path
import numpy as np
from acd_protocol import ROOT, LT, SIGMA, PATTERNS, physics


def generate():
    from acd_stage18_inference import guarded
    guarded()
    if socket.gethostname() == 'baccus':
        raise RuntimeError('Stage18 C generation must leave Baccus CPU resources free')
    out = ROOT/'runs/stage18/response_data'
    out.mkdir(parents=True, exist_ok=True)
    namespace = int.from_bytes(hashlib.sha256(b'acd-train-resp').digest()[:8], 'little')
    for role, name, size in [(0, 'train', 4096), (1, 'val', 512)]:
        path = out/f'{name}.npz'
        if path.exists():
            continue
        rng = np.random.default_rng(np.random.SeedSequence([namespace, role]))
        forcing = rng.uniform(6, 10, size)
        initial = forcing[:, None]+rng.standard_normal((size, 40))
        initial = physics.flow(initial, np.repeat(forcing[:, None], 40, 1), round(50*LT/.01), .01)
        history = physics.simulate(initial, np.repeat(forcing[:, None], 40, 1), .01, 11)
        index = rng.integers(8, size=size)
        amplitude = rng.uniform(-.32, .32, size=size)
        action = np.zeros((size, 2, 40))
        action[:, 0] = amplitude[:, None]*PATTERNS[index]
        future = np.empty((size, 2, 36, 40), np.float32)
        for b in range(0, size, 128):
            end = min(size, b+128)
            states = physics.simulate(np.repeat(history[b:end, -1], 2, 0),
                                      (forcing[b:end, None, None]+action[b:end]).reshape(-1, 40), .01, 37)
            future[b:end] = states[:, 1:].reshape(end-b, 2, 36, 40)/SIGMA
        pending = path.with_suffix('.tmp.npz')
        np.savez_compressed(pending, H=(history/SIGMA).astype(np.float32), F=((forcing-8)/2).astype(np.float32),
                            A=(action/SIGMA).astype(np.float32), T=future)
        pending.replace(path)
    manifest = dict(namespace='acd-train-resp', namespace_id=namespace, host=socket.gethostname(),
                    source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                    data_sha256={p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in out.glob('*.npz')},
                    action_pattern='uniformly sampled among eight frozen patterns; second branch no action',
                    noise_free=True, trajectory_disjoint_validation=True)
    (out/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    # Validation references contain no confirmation-panel input or outcome.
    reference = out/'validation_reference.npz'
    if not reference.exists():
        with np.load(out/'val.npz') as validation:
            history, forcing = validation['H'].copy(), validation['F'].copy()*2+8
        costs = []
        for b in range(0, len(history), 32):
            h, f = history[b:b+32], forcing[b:b+32]
            states = physics.simulate(np.repeat(h[:, -1]*SIGMA, 9, 0),
                                      (f[:, None, None]+.16*PATTERNS[None]).reshape(-1, 40), .01)
            costs.append(physics.costs(states).reshape(len(h), 9, -1))
        np.savez_compressed(reference, J=np.concatenate(costs))
    manifest['validation_reference_sha256'] = hashlib.sha256(reference.read_bytes()).hexdigest()
    (out/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    (ROOT/'receipts/acd_stage18_response_data.json').write_text(json.dumps(manifest, indent=2)+'\n')


if __name__ == '__main__':
    generate()
