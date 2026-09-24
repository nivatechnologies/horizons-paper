"""Frozen configuration and paths. Every script reads the freeze through here."""
from __future__ import annotations

import subprocess
from pathlib import Path

import yaml

PKG = Path(__file__).resolve().parents[1]          # tokens_horizon/
FREEZE = PKG / "freeze.yaml"
RUNS = PKG / "runs"
CACHE = RUNS / "cache"
RESULTS = PKG / "results"
FIGS = PKG / "figures"


def freeze() -> dict:
    return yaml.safe_load(FREEZE.read_text())


def lam(system: str) -> float:
    return float(freeze()["lyapunov"][system]["lam_max"])


def window_time(system: str) -> float:
    fz = freeze()
    return fz["scoring"]["window_lyapunov_times"] / lam(system)


def seed(block: str, system: str, stream: int = 0) -> int:
    s = freeze()["seeds"]
    return int(s["block_base"][block] + 100 * s["system_index"][system] + stream)


def git_sha() -> str:
    try:
        out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=PKG, capture_output=True, text=True)
        sha = out.stdout.strip()
        dirty = subprocess.run(["git", "status", "--porcelain", "--", "th", "scripts"], cwd=PKG,
                               capture_output=True, text=True).stdout.strip()
        return sha + ("-dirty" if dirty else "")
    except Exception:
        return "unknown"


def ensure_dirs():
    for p in (RUNS, CACHE, RESULTS, FIGS):
        p.mkdir(parents=True, exist_ok=True)
