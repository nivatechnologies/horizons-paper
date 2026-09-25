"""Regenerate every table, figure and NUMBERS.md from the raw runs in runs/.

    python reproduce.py            # from raw runs (per-state arrays committed under runs/): tables, figures, NUMBERS.md
    python reproduce.py --full     # also (re)compute raw runs that are missing: caches, references, learned grid (GPU, hours)

Every step is a script under scripts/ and is also runnable alone. Compute steps skip settings whose raw output
already exists, so --full on a clone with runs/ removed recomputes everything from the frozen protocol.
Caches (calibration blocks, codebooks, panels) are rebuilt deterministically on first use under runs/cache/.
"""
import argparse
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PY = sys.executable

COMPUTE = [
    ["scripts/prep_cache.py"],
    ["scripts/t0_lyapunov.py"],
    ["scripts/t2_headline.py", "all"],
    ["scripts/t2_headline.py", "run", "--bits", "10", "--dts", "0.01"],
    ["scripts/t2_headline.py", "all", "--system", "lorenz45", "--bits", "6", "10", "--deltas", "0.05", "--dts", "0.01",
     "--res", "results/headline_subsets/lorenz45"],
    ["scripts/t2_headline.py", "all", "--system", "l96_5", "--bits", "6", "10", "--deltas", "0.05", "--dts", "0.01",
     "--res", "results/headline_subsets/l96_5"],
    ["scripts/t2_history.py"],
    ["scripts/t2_decomposition.py"],
    ["scripts/t3_learned.py", "run", "--grid", "stall"],
    ["scripts/t3_learned.py", "run", "--grid", "main"],
    ["scripts/t3_learned.py", "run", "--grid", "postfreeze_dataB"],
    ["scripts/t3_learned.py", "run", "--grid", "postfreeze_dataC"],
    ["scripts/t3_learned.py", "run", "--grid", "ext_large"],
]
# Post-freeze extension pipelines (KS, Kolmogorov, E5 controls) are multi-stage and GPU/CPU heavy; their scripts and
# stage order are documented in README.md ("Post-freeze extension") and are not run by this driver.

TABLES = [
    ["scripts/t2_system_table.py"],
    ["scripts/t2_headline.py", "summarize"],
    ["scripts/t2_headline.py", "summarize", "--system", "lorenz45", "--res", "results/headline_subsets/lorenz45"],
    ["scripts/t2_headline.py", "summarize", "--system", "l96_5", "--res", "results/headline_subsets/l96_5"],
    ["scripts/t2_exchange_law.py"],
    ["scripts/t2_dimension.py"],
    ["scripts/t2_history.py", "--aggregate-only"],
    ["scripts/t2_decomposition.py"],
    ["scripts/postfreeze_codebook_seeds.py"],
    ["scripts/postfreeze_exchange_extra.py"],
    ["scripts/postfreeze_data_axis_B.py"],
    ["scripts/t3_analysis.py"],
    ["scripts/ext_a8_same_panel.py"],
    ["scripts/ext_e53_analysis.py"],
    ["scripts/fig_F1.py"],
    ["scripts/fig_F2_F4_F5.py"],
    ["scripts/fig_F3.py"],
    ["scripts/fig_F6.py"],
    ["scripts/fig_F7.py"],
    ["scripts/fig_F8.py"],
    ["scripts/make_numbers.py"],
]


def run(cmd):
    t0 = time.time()
    print(">>", " ".join(cmd), flush=True)
    r = subprocess.run([PY] + cmd, cwd=HERE, env={**__import__("os").environ, "PYTHONDONTWRITEBYTECODE": "1"})
    print(f"   exit {r.returncode} in {time.time() - t0:.0f}s", flush=True)
    return r.returncode


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--full", action="store_true")
    a = ap.parse_args()
    steps = (COMPUTE if a.full else []) + TABLES
    failed = [" ".join(c) for c in steps if run(c) != 0]
    print("failed steps:", failed if failed else "none")
    sys.exit(1 if failed else 0)
