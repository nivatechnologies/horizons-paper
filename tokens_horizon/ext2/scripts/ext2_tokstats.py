"""EXT2 tokenizer report on held-out data (ext2_freeze.yaml `report`): the calibration held-out split
(runs/cache/ext_kolmo/calib_heldout.npy, 51,200 states from 64 trajectories; never trained on or used for selection).

Per configuration: parameters (encoder, decoder, quantizer = 0: FSQ has no learned parameters), training time and
steps, selected checkpoint, held-out reconstruction ||x - D(E(x))|| / sigma_A (RMS, mean, median, share within
eps), code utilization (distinct codes used on held-out tokens / codebook size), per-dimension level usage
(levels used / levels and normalized entropy), and the reconstruction null (calibration mean, zero field).
Writes results/ext2/k3_tokenizers.csv.

Usage: python ext2/scripts/ext2_tokstats.py <device> [config ...]
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from ext2_measure import Coder, TRAIN  # noqa: E402
from fsq_ae import CONFIGS  # noqa: E402
from th import config  # noqa: E402
from th import kolmo_eval as E  # noqa: E402

RES = config.RESULTS / "ext2"


def main(device, names):
    sA = E.sigma_A()
    X = np.load(E.CACHE / "calib_heldout.npy", mmap_mode="r").reshape(-1, 64, 64)
    mu = np.load(E.CACHE / "calib_fit.npy", mmap_mode="r").reshape(-1, 4096)
    mean = np.zeros(4096)
    for i in range(0, len(mu), 20000):
        mean += mu[i:i + 20000].sum(0)
    mean = (mean / len(mu)).reshape(64, 64)
    rows = []
    for name in names:
        side, levels = CONFIGS[name]
        tag = ""
        info = json.loads((TRAIN / name / "info.json").read_text())
        if info["diverged"]:
            tag = "_lr1e-4"
            info = json.loads((TRAIN / f"{name}{tag}" / "info.json").read_text())
        coder = Coder(name, device, tag)
        errs, codes, null_mean, null_zero = [], [], [], []
        for i in range(0, len(X), 5000):
            x = np.asarray(X[i:i + 5000], np.float64)
            dec, c = coder(x)
            errs.append(np.sqrt(((dec - x) ** 2).sum((-2, -1))) / sA)
            codes.append(c)
            null_mean.append(np.sqrt(((x - mean) ** 2).sum((-2, -1))) / sA)
            null_zero.append(np.sqrt((x ** 2).sum((-2, -1))) / sA)
        e = np.concatenate(errs)
        codes = np.concatenate(codes).ravel()
        n_codes = int(np.prod(levels))
        used = np.unique(codes)
        basis = np.concatenate([[1], np.cumprod(levels[:-1])])
        lv_use, lv_ent = [], []
        for k, L in enumerate(levels):
            lvl = (codes // basis[k]) % L
            p = np.bincount(lvl, minlength=L) / len(lvl)
            lv_use.append(f"{int((p > 0).sum())}/{L}")
            q = p[p > 0]
            lv_ent.append(round(float(-(q * np.log(q)).sum() / np.log(L)), 4))
        pc = np.bincount(codes, minlength=n_codes) / len(codes)
        q = pc[pc > 0]
        rows.append(dict(config=name, latent=f"{side}x{side}", tokens=side * side, levels=str(levels), codes_per_token=n_codes,
                         bits_per_frame=side * side * float(np.log2(n_codes)), params_encoder=info["params"]["encoder"],
                         params_decoder=info["params"]["decoder"], params_quantizer=0, params_total=info["params"]["total"],
                         train_steps=info["steps"], lr=info["lr"], train_seconds=info["train_seconds"],
                         best_step=info["best_step"], best_val_rel_rms=info["best_val_rel_rms"], diverged_first_run=bool(tag),
                         heldout_states=len(e), heldout_traj=64, heldout_rel_rms=float(np.sqrt(np.mean(e ** 2))),
                         heldout_rel_mean=float(e.mean()), heldout_rel_median=float(np.median(e)),
                         **{f"heldout_share_within_eps{x}": float(np.mean(e <= x)) for x in E.EPS},
                         code_utilization=len(used) / n_codes, codes_used=len(used),
                         code_perplexity=float(np.exp(-(q * np.log(q)).sum())),
                         level_usage=" ".join(lv_use), level_entropy_norm=str(lv_ent),
                         null_mean_rel_rms=float(np.sqrt(np.mean(np.concatenate(null_mean) ** 2))),
                         null_zero_rel_rms=float(np.sqrt(np.mean(np.concatenate(null_zero) ** 2))),
                         label="learned"))
        print(name, "held-out rel RMS", round(rows[-1]["heldout_rel_rms"], 4), "util", round(rows[-1]["code_utilization"], 4),
              rows[-1]["level_usage"], flush=True)
    RES.mkdir(parents=True, exist_ok=True)
    with open(RES / "k3_tokenizers.csv", "w", newline="") as fh:
        fh.write(f"# git_sha={config.git_sha()}; EXT2 learned-tokenizer kill test; held-out = calibration held-out split\n")
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    torch.set_num_threads(8)
    main(sys.argv[1], sys.argv[2:] or list(CONFIGS))
