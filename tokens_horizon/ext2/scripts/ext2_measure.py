"""EXT2 measurements M1-M4 for one trained FSQ configuration (ext2_freeze.yaml `measurements`).

On the 1,000-state confirmation panel (the KKE3 states), every frame interval (0.14, 0.35, 0.70), eps 0.1/0.3/0.5,
future frames (primary) and from t = 0 (secondary):
  M1 reconstruction at t = 0: e_0 = ||x_0 - D(E(x_0))|| / sigma_A per state.
  M2 perfect next-token prediction (reference; NOT a bound): e_j = ||x_j - D(E(x_j))|| / sigma_A on the true frames,
     horizon = first scored frame with e_j > eps (th.score.horizon, same convention as E3).
  M3 decode-and-integrate (reference): th.kolmo_eval.di_errors on D(E(x_0)) (the integrator's Galerkin projection acts
     on the decoded initial state of the reference trajectory only; frame 0 scored on the decoded state as is).
  M4 persistence (reference): hold D(E(x_0)).
The selected checkpoint (runs/ext2/train/<config>[tag]/best.pt), float32 inference; decoded grids scored in float64.
Writes runs/ext2/measure/<config>.npz (per-state arrays) and .json (rows).

Usage: python ext2/scripts/ext2_measure.py <config> <device> [train_tag]
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from fsq_ae import build  # noqa: E402
from th import config  # noqa: E402
from th import kolmo_eval as E  # noqa: E402
from ext_kolmo_e3 import summarize  # noqa: E402

OUT = config.RUNS / "ext2" / "measure"
TRAIN = config.RUNS / "ext2" / "train"


class Coder:
    def __init__(self, name, device, tag=""):
        self.model = build(name).to(device).eval()
        self.model.load_state_dict(torch.load(TRAIN / f"{name}{tag}" / "best.pt", map_location=device))
        self.device = device
        self.scale = 64.0 / E.sigma_A()

    @torch.no_grad()
    def __call__(self, Wg, bs=250):
        out = np.empty_like(Wg, dtype=np.float64)
        codes = []
        for i in range(0, len(Wg), bs):
            x = torch.from_numpy((Wg[i:i + bs] * self.scale).astype(np.float32)).to(self.device)
            zq = self.model.encode(x)
            out[i:i + bs] = self.model.decode(zq).double().cpu().numpy() / self.scale
            codes.append(self.model.quant.code_index(zq).flatten(1).cpu().numpy())
        return out, np.concatenate(codes)


def main(name, device, tag=""):
    sA = E.sigma_A()
    deltas = [float(d) for d in E.spec()["frame_intervals"]]
    pnl = E.Panel()
    coder = Coder(name, device, tag)
    t0 = time.time()
    x0 = pnl.unit(0)
    dec0, codes0 = coder(x0)
    e0 = np.sqrt(((dec0 - x0) ** 2).sum((-2, -1))) / sA
    arrays = dict(recon_x0_err=e0, codes_x0=codes0)
    # M2: reconstruction error on every frame of every grid
    need = {}
    for d in deltas:
        u = E.units(d)
        for j in range(E.n_future(d) + 1):
            need.setdefault(j * u, []).append((d, j))
    err_pt = {d: np.empty((E.n_future(d) + 1, len(x0))) for d in deltas}
    for k in sorted(need):
        tr = pnl.unit(k)
        dec, _ = coder(tr)
        e = np.sqrt(((dec - tr) ** 2).sum((-2, -1))) / sA
        for d, j in need[k]:
            err_pt[d][j] = e
    t_pt = time.time() - t0
    base = dict(system="kolmo40", tokenizer=f"fsq_{name}", config=name)
    rows = []

    def add(kind, label, err, d):
        for e, r in E.horizons_from_err(err, d).items():
            for start in ("future", "from_t0"):
                H, c = r[start]
                arrays[f"{kind}_d{d:g}_eps{e}_{start}_H"] = H
                arrays[f"{kind}_d{d:g}_eps{e}_{start}_crossed"] = c
                rows.append(dict(base, delta=d, eps=e, start=start, label=label, **summarize(kind, H, c)))

    for d in deltas:
        arrays[f"pt_err_d{d:g}"] = err_pt[d].astype(np.float32)
        add("perfect_token", "reference (perfect next-token prediction)", err_pt[d], d)
    t1 = time.time()
    for d in deltas:
        add("persistence", "reference", E.persistence_err(dec0, pnl, d, sA), d)
    t_pers = time.time() - t1
    t1 = time.time()
    errs, k_stop = E.di_errors([dec0], pnl, sA, device, deltas)
    t_di = time.time() - t1
    for d in deltas:
        add("decode_and_integrate", "reference", errs[0][d], d)
    m1 = dict(recon_rms=float(np.sqrt(np.mean(e0 ** 2))), recon_mean=float(e0.mean()),
              recon_median=float(np.median(e0)), **{f"share_within_eps{e}": float(np.mean(e0 <= e)) for e in E.EPS},
              null_zero_rms=float(np.sqrt(np.mean((np.linalg.norm(x0.reshape(len(x0), -1), axis=1) / sA) ** 2))))
    OUT.mkdir(parents=True, exist_ok=True)
    np.savez(OUT / f"{name}{tag}.npz", **arrays)
    out = dict(config=name, train_tag=tag, rows=rows, m1=m1, sigma_A=sA,
               timing=dict(perfect_token=t_pt, persistence=t_pers, di=t_di, di_stop_unit=k_stop),
               di_note="the integrator's Galerkin projection (2/3 dealias mask, mean removal) acts on the decoded "
                       "initial state of the reference trajectory only; frame 0 scored on the decoded state as is",
               git_sha=config.git_sha(), label="EXT2 learned-tokenizer kill test")
    (OUT / f"{name}{tag}.json").write_text(json.dumps(out, indent=1, default=float))
    print(name, "measured", round(time.time() - t0), "s; M1 rms", round(m1["recon_rms"], 4), flush=True)


if __name__ == "__main__":
    torch.set_num_threads(8)
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "")
