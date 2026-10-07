"""Saved physics/learned JVP comparison, with no realized-outcome access."""
import argparse
import json
from pathlib import Path
import numpy as np
from acd_protocol import LEADS
from acd_stage18_inference import ROOT, OUT, digest, guarded


def run(name):
    guarded()
    meta = json.loads((OUT/'derivatives'/name/'complete.json').read_text())
    climatology = json.loads((ROOT/'receipts/acd_stage11_clim_tangent.json').read_text())
    sd = np.array([[next(r['standard_deviation'] for r in climatology['rows']
                         if r['pattern'] == k and r['lead'] == lead) for lead in LEADS] for k in range(8)])
    all_g, all_h, pair = [], [], []
    for case in range(200):
        path = OUT/'derivatives'/name/f'{case:03d}.npz'
        if digest(path) != meta['output_hashes'][path.name]:
            raise RuntimeError('Derivative output hash mismatch')
        with np.load(ROOT/'runs/stage9'/f'forward_{case:03d}.npz') as d:
            g = d['G'].copy()
        with np.load(path) as d:
            h = d['G'].copy()
        if g.shape != h.shape or not np.isfinite(h).all():
            raise RuntimeError('Derivative shape or finiteness failure')
        pg, ph = (g < 0).mean(0), (h < 0).mean(0)
        classes = lambda p: np.where(np.maximum(p, 1-p) >= .95, np.where(p > .5, -1, 1), 0)
        near = np.stack([(np.abs(g) <= gamma*sd).mean(0) for gamma in [.05, .1, .2, .5]])
        pair.append(dict(g=classes(pg), h=classes(ph), z=np.abs(h.mean(0))/h.std(0, ddof=1),
                         near=near, mse=((h-g)**2).mean(0), probability_error=np.abs(ph-pg)))
        all_g.append(g)
        all_h.append(h)
    g, h = np.concatenate(all_g), np.concatenate(all_h)
    rows = []
    for t, lead in enumerate(LEADS):
        cg = np.array([p['g'][:, t] for p in pair]).ravel()
        ch = np.array([p['h'][:, t] for p in pair]).ravel()
        agreement = float((cg == ch).mean())
        chance = sum(float((cg == k).mean()*(ch == k).mean()) for k in [-1, 0, 1])
        mse = float(np.mean((h[:, :, t]-g[:, :, t])**2))
        near = np.array([p['near'][:, :, t] for p in pair])
        rows.append(dict(lead=float(lead), per_draw_sign_agreement=float((np.sign(g[:, :, t]) == np.sign(h[:, :, t])).mean()),
                         normalized_RMS_error=float(np.sqrt(mse/np.mean(g[:, :, t]**2))),
                         normalization='physics tangent pooled RMS at this lead',
                         three_class_agreement=agreement,
                         three_class_kappa=(agreement-chance)/(1-chance) if chance < 1 else None,
                         median_z=float(np.median([p['z'][:, t] for p in pair])),
                         pooled_MSE=mse,
                         pair_MSE_quartiles=np.quantile([p['mse'][:, t] for p in pair], [.25, .5, .75]).tolist(),
                         probability_error_quartiles=np.quantile([p['probability_error'][:, t] for p in pair], [.25, .5, .75]).tolist(),
                         near_zero=[dict(gamma=gamma, pair_mass_quartiles=np.quantile(near[:, i], [.25, .5, .75]).tolist())
                                    for i, gamma in enumerate([.05, .1, .2, .5])]))
    result = dict(model=name, rows=rows, output_hashes=meta['output_hashes'], code_sha256=digest(__file__),
                  post_hoc=True, licenses_frozen_route=False)
    (ROOT/'receipts'/f'acd_stage18_derivatives_{name}.json').write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--name', required=True)
    run(p.parse_args().name)
