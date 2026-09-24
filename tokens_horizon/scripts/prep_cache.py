"""Build shared caches once (calibration blocks, k-means codebooks, training/validation blocks, panels).

Run before any parallel task so no two processes write the same cache file.
"""
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from th import data  # noqa: E402
from th.tokenize import kmeans_codebook  # noqa: E402

SYSTEMS = ["lorenz28", "lorenz45", "l96_5", "l96_6", "l96_10", "l96_20"]
RATES = [4, 5, 6, 7, 8, 9, 10, 11, 12]


def prep_system(s):
    data.calibration(s)
    data.panel(s, "confirmation")
    if s in ("lorenz28", "lorenz45", "l96_5"):
        data.train_trajectories(s, "training")
        data.train_trajectories(s, "validation")
    if s == "lorenz28":
        data.panel(s, "validation")
        data.panel(s, "confirmation", dt=0.005)
    return s


def prep_cb(args):
    s, b = args
    cb = kmeans_codebook(s, b)
    return s, b, cb.meta["n_iter"]


if __name__ == "__main__":
    with ProcessPoolExecutor(6) as ex:
        for s in ex.map(prep_system, SYSTEMS):
            print("data", s, flush=True)
    jobs = [(s, b) for s in SYSTEMS for b in RATES]
    jobs.sort(key=lambda j: -j[1])
    with ProcessPoolExecutor(27) as ex:
        for s, b, it in ex.map(prep_cb, jobs):
            print("kmeans", s, b, it, flush=True)
