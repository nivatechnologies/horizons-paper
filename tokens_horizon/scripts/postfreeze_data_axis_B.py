"""POST-FREEZE (requested by Todd, 2026-09-25; not pre-registered). NUMBERS.md section P.

B trained on the 20,000 tu data axis (1,000 training trajectories) at 6 and 10 bits, Delta 0.05, seeds 0-2
(runs/learned/postfreeze/), reported next to A's frozen data-axis cells and the 2,000 tu B and A cells, on the same
1,000 confirmation states, primary score. Paired differences use the frozen margins, for information.
Labels: cells are learned; differences are estimates.
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
OUT = config.RESULTS / "postfreeze"


def stack(sub, arm, bits, traj):
    tag = f"lorenz28_{arm}_b{bits}_D0.05_s*" + ("_traj1000" if traj else "")
    runs = [d for d in sorted((L / sub).glob(tag)) if (d / "done").exists() and (("_traj1000" in d.name) == traj)]
    return np.stack([np.load(d / "eval.npz")[f"H_{P}"] for d in runs]), [d.name for d in runs]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    cells, comps = [], []
    for bits in (6, 10):
        H = {}
        for key, sub, arm, traj in (("B 20k", "postfreeze", "B", True), ("A 20k", "main", "A", True),
                                    ("B 2k", "main", "B", False), ("A 2k", "main", "A", False)):
            H[key], names = stack(sub, arm, bits, traj)
            m, lo, hi = score.bootstrap_mean(H[key])
            cells.append(dict(bits=bits, delta=0.05, cell=key, n_seeds=len(names), H=m, ci95_lo=lo, ci95_hi=hi,
                              runs=" ".join(names),
                              label="learned" + (" (post-freeze)" if key == "B 20k" else " (frozen grid)")))
        for a, b in (("B 20k", "B 2k"), ("A 20k", "A 2k"), ("A 20k", "B 20k"), ("A 2k", "B 2k")):
            pd = score.paired_diff(H[a], H[b])
            comps.append(dict(bits=bits, delta=0.05, a=a, b=b, diff_a_minus_b=pd["diff"], ci90_lo=pd["ci90"][0],
                              ci90_hi=pd["ci90"][1], ci95_lo=pd["ci95"][0], ci95_hi=pd["ci95"][1],
                              reading="; ".join(score.reading(pd)), label="post-freeze estimate"))
    sha = config.git_sha()
    for name, rows in (("data_axis_B_cells", cells), ("data_axis_B_comparisons", comps)):
        with open(OUT / f"{name}.csv", "w", newline="") as fh:
            fh.write(f"# git_sha={sha}; POST-FREEZE (Todd 2026-09-25), not pre-registered\n")
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
    (OUT / "data_axis_B.json").write_text(json.dumps(dict(git_sha=sha, note=__doc__, cells=cells, comparisons=comps),
                                                     indent=1, default=float))
    for c in cells:
        print(f"b{c['bits']} {c['cell']:6s} n={c['n_seeds']} H={c['H']:.3f} [{c['ci95_lo']:.3f}, {c['ci95_hi']:.3f}]")
    for c in comps:
        print(f"b{c['bits']} {c['a']} - {c['b']}: {c['diff_a_minus_b']:+.3f} 95[{c['ci95_lo']:+.3f}, {c['ci95_hi']:+.3f}] "
              f"| {c['reading']}")


if __name__ == "__main__":
    main()
