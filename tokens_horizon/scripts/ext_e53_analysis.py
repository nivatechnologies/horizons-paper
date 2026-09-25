"""POST-FREEZE EXTENSION E5.3: larger and longer model (width 256, 6 layers, 40,000 steps) against the frozen-size cells.

Cells: A and B at 4 and 10 bits, C (sigma = 0); lorenz28, Delta = 0.05; seeds 0-2; 1,000 confirmation states.
Paired differences (large minus frozen size) on the same states, seeds resampled per arm; frozen margins.
Also: parameters and training compute per arm, and the larger A against the output-support bound.
Labels: cells learned; differences estimate.
"""
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np  # noqa: E402

from th import config, score  # noqa: E402

P = "eps0.3_future"
L = config.RUNS / "learned"
OUT = config.RESULTS / "ext"


def load(sub, tag_prefix, suffix):
    runs = []
    for s in (0, 1, 2):
        d = L / sub / f"{tag_prefix}_s{s}{suffix}"
        if not (d / "done").exists():
            raise FileNotFoundError(d)
        runs.append((np.load(d / "eval.npz"), json.loads((d / "info.json").read_text())))
    return runs


def main():
    rows = []
    bound = {b: np.load(config.RUNS / "headline" / f"lorenz28_b{b}_D0.05_dt0.01_M1500.npz")[f"H_bound_{P}"]
             for b in (4, 10)}
    cells = [("A", 4), ("B", 4), ("A", 10), ("B", 10), ("C", 0)]
    for arm, b in cells:
        pre = f"lorenz28_{arm}_b{b}_D0.05"
        nz = "_n0.0" if arm == "C" else ""
        small = load("main", pre, nz)
        large = load("ext_large", pre, nz + "_steps40000_w256L6")
        Hs = np.stack([z[f"H_{P}"] for z, _ in small])
        Hl = np.stack([z[f"H_{P}"] for z, _ in large])
        ms, los, his = score.bootstrap_mean(Hs)
        ml, lol, hil = score.bootstrap_mean(Hl)
        pd = score.paired_diff(Hl, Hs)
        row = dict(arm=arm, bits=b, delta=0.05, H_frozen_size=ms, H_frozen_ci95=f"[{los:.4f}, {his:.4f}]",
                   H_large=ml, H_large_ci95=f"[{lol:.4f}, {hil:.4f}]", diff_large_minus_frozen=pd["diff"],
                   diff_ci90_lo=pd["ci90"][0], diff_ci90_hi=pd["ci90"][1], diff_ci95_lo=pd["ci95"][0],
                   diff_ci95_hi=pd["ci95"][1], reading="; ".join(score.reading(pd)),
                   params_frozen=small[0][1]["params"]["total"], params_large=large[0][1]["params"]["total"],
                   train_flops_frozen=small[0][1]["train_flops"], train_flops_large=large[0][1]["train_flops"],
                   best_val_frozen=float(np.mean([i["best_val"] for _, i in small])),
                   best_val_large=float(np.mean([i["best_val"] for _, i in large])), label="learned / estimate")
        if arm == "A":
            o = score.outlast(Hl, bound[b])
            rb = Hl.mean() / bound[b].mean()
            row.update(large_outlast_bound=o["outlast"], large_fraction_of_bound=float(rb),
                       large_gap_to_bound=float(bound[b].mean() - Hl.mean()))
            if o["outlast"] > 0:
                raise RuntimeError(f"A outlasts the output-support bound ({arm} b{b}): impossible, find the bug")
        rows.append(row)
    OUT.mkdir(parents=True, exist_ok=True)
    keys = []
    for r in rows:
        keys += [k for k in r if k not in keys]
    with open(OUT / "e53_larger_model.csv", "w", newline="") as fh:
        fh.write(f"# git_sha={config.git_sha()}; POST-FREEZE EXTENSION E5.3\n")
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(f"{r['arm']} b{r['bits']}: frozen {r['H_frozen_size']:.3f} large {r['H_large']:.3f} diff "
              f"{r['diff_large_minus_frozen']:+.3f} [{r['diff_ci95_lo']:+.3f}, {r['diff_ci95_hi']:+.3f}] | {r['reading']} "
              f"| params {r['params_frozen']} -> {r['params_large']}")


if __name__ == "__main__":
    main()
