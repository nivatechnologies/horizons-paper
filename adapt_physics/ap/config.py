"""Paths, seeds and the freeze for Adapt the Physics (stage 1)."""
from __future__ import annotations

import subprocess
from pathlib import Path

import yaml

PKG = Path(__file__).resolve().parents[1]          # adapt_physics/
FREEZE = PKG / "ap_freeze.yaml"
RUNS = PKG / "runs"
CACHE = RUNS / "cache"
RESULTS = PKG / "results"
FIGS = PKG / "figures"
SYSTEM_INDEX = 9                                   # Kolmogorov with drag (tokens_horizon uses 0-8)
BLOCK_BASE = {"calibration": 10000, "training": 20000, "validation": 30000, "test": 40000, "lyapunov": 50000,
              "noise": 60000}


def seed(block: str, stream: int = 0) -> int:
    """block base + 100 * 9 + stream (the tokens_horizon freeze.yaml scheme, a new system index)."""
    return int(BLOCK_BASE[block] + 100 * SYSTEM_INDEX + stream)


def freeze() -> dict:
    return yaml.safe_load(FREEZE.read_text())


def git_sha() -> str:
    try:
        sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=PKG, capture_output=True, text=True).stdout.strip()
        dirty = subprocess.run(["git", "status", "--porcelain", "--", "."], cwd=PKG, capture_output=True,
                               text=True).stdout.strip()
        return sha + ("-dirty" if dirty else "")
    except Exception:
        return "unknown"
