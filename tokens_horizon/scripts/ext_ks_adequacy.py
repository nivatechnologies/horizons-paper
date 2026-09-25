"""Post-freeze extension, KS calibration adequacy (Amendment 1 A5; ext_freeze.yaml ks.tokenizers.calibration_adequacy).

Per codebook: samples per code (fit vectors / K; patches and independent trajectories separately), k-means
diagnostics (iterations, converged, empty and duplicate fractions, re-seeded clusters; stop rule > 1% or not converged
-> flagged), fit and held-out distortion delta = RMS over states of ||x - decode(x)|| (the scored norm; also / sigma_A),
held-out occupancy (fraction of codes hit by held-out vectors), unused-code rate (codes with no fit assignment) and
held-out-unused rate. Halved refits (suffix _half): the same, plus the change in the confirmation-panel bound
(restricted mean, primary Delta, eps 0.3, future frames), read from runs/ext/ks/e3/ and runs/ext/ks/e3_half/.
Exact decoding: float64 cKDTree nearest code (patch-wise; stage-wise for residual VQ).

Usage: python scripts/ext_ks_adequacy.py [halfbound <device>]
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import csv    # noqa: E402
import json   # noqa: E402
import sys    # noqa: E402
from pathlib import Path   # noqa: E402

import numpy as np   # noqa: E402
from scipy.spatial import cKDTree   # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from th import config   # noqa: E402
from th import ks as K   # noqa: E402
from th import ks_eval as E   # noqa: E402
from th.patchvq import to_patches_1d   # noqa: E402

CACHE = config.CACHE / "ext_ks"
CB = config.RUNS / "ext" / "ks" / "codebooks"
HALF = config.RUNS / "ext" / "ks" / "e3_half"
WORKERS = 32


def decode_err(C, X, P):
    """Per-state squared error of exact patch-wise nearest decoding, and the code labels (n*P,)."""
    Xp = to_patches_1d(X, P).reshape(-1, X.shape[1] // P)
    d, lab = cKDTree(C).query(Xp, workers=WORKERS)
    return (d ** 2).reshape(len(X), P).sum(1), lab


def rvq_err(Cs, X):
    R = X.copy()
    for C in Cs:
        _, lab = cKDTree(C).query(R, workers=WORKERS)
        R -= C[lab]
    return (R ** 2).sum(1)


def halfbound(device):
    """Bound of the halved codebooks at the primary Delta (all eps, both starts) on the confirmation panel."""
    HALF.mkdir(parents=True, exist_ok=True)
    for f in sorted(CB.glob("*_half.npz")):
        name = f.stem
        if (HALF / f"{name}.json").exists():
            continue
        tok = E.Tok(name.replace("_half", ""))
        z = np.load(f)
        tok.C = z["C"]
        tok.name = name
        system = tok.system
        d = float(K.ks_spec(system)["primary_delta"])
        out, dC0, cnt = E.bound(tok, system, "confirmation", d, E.sigma_A(system), device)
        H, c = out[0.3]["future"]
        rec = dict(tokenizer=name, delta=d, eps=0.3, start="future", restricted_mean=float(H.mean()),
                   frac_no_cross=float(1 - c.mean()), p0=float(out[0.3]["p0"].mean()), **E.survival(H, c))
        np.savez(HALF / f"{name}.npz", H=H, crossed=c, dC0=dC0)
        (HALF / f"{name}.json").write_text(json.dumps(rec, indent=1))
        print(name, rec, flush=True)


def main():
    rows = []
    cache = {}
    for f in sorted(CB.glob("*.npz")):
        name = f.stem
        z = np.load(f)
        meta = json.loads(str(z["meta"]))
        parts = name.split("_")
        system, family = parts[0], parts[1]
        if system not in cache:
            Xf = np.load(CACHE / f"calib_{system}_fit.npy", mmap_mode="r")
            Xh = np.load(CACHE / f"calib_{system}_heldout.npy")
            trh = np.load(CACHE / f"calib_{system}_heldout_traj.npy")
            cache[system] = (Xf, Xh, trh)
        Xf, Xh, trh = cache[system]
        sA = E.sigma_A(system)
        r = dict(system=system, family=family, codebook=name, half=name.endswith("_half"), K=meta["K"],
                 n_train=meta["n_train"], samples_per_code=meta["n_train"] / meta["K"],
                 iterations=meta["iterations"], converged=meta["converged"], empty_frac=meta["empty_frac"],
                 duplicate_frac=meta["duplicate_frac"], reseeded_during_fit=meta["reseeded_during_fit"],
                 fit_seconds=meta["seconds"], method=meta.get("method", ""))
        r["stop_rule_flag"] = bool((not meta["converged"]) or meta["empty_frac"] > 0.01 or meta["duplicate_frac"] > 0.01)
        if family == "rvq":
            s = int(parts[2][1:])
            Cs = [np.load(CB / f"{system}_rvq_s{i}.npz")["C"] for i in range(1, s + 1)]
            r.update(P=None, b=8, stage=s, total_bits=8 * s, states_used=meta.get("states_used"),
                     independent_trajectories=meta.get("independent_trajectories"))
            e2h = rvq_err(Cs, Xh)
            rng = np.random.default_rng(0)
            sub = np.sort(rng.choice(len(Xf), min(len(Xf), 500_000), replace=False))
            e2f = rvq_err(Cs, np.asarray(Xf[sub]))
            r.update(delta_fit=float(np.sqrt(e2f.mean())), delta_heldout=float(np.sqrt(e2h.mean())),
                     fit_delta_note="RMS on a fixed 500,000-state subset of the fit block (seed 0)")
        else:
            C = z["C"]
            P = 1 if family == "whole" else int(parts[2][1:])
            b = int(parts[2][1:]) if family == "whole" else int(parts[3][1:])
            r.update(P=P, b=b, total_bits=P * b if family == "patch" else b,
                     patches=meta.get("patches", meta["n_train"]), states_used=meta.get("states_used", meta["n_train"]),
                     independent_trajectories=meta.get("independent_trajectories", meta.get("n_traj_fit")))
            e2h, lab = decode_err(C, Xh, P)
            occ = np.bincount(lab, minlength=len(C))
            r.update(delta_fit=float(np.sqrt(meta["mse"] * P)), delta_heldout=float(np.sqrt(e2h.mean())),
                     heldout_occupancy=float((occ > 0).mean()), unused_code_rate=float(meta["empty_frac"]),
                     heldout_unused_rate=float((occ == 0).mean()),
                     fit_delta_note="sqrt(P * fit mse per vector) on the vectors the codebook was fitted on")
            # per held-out trajectory mean squared error, for D_eff bootstrap over held-out trajectories
            np.save(config.RUNS / "ext" / "ks" / f"heldout_err2_{name}.npy",
                    np.bincount(trh, weights=e2h) / np.bincount(trh))
        if family == "rvq":
            np.save(config.RUNS / "ext" / "ks" / f"heldout_err2_{name}.npy",
                    np.bincount(trh, weights=e2h) / np.bincount(trh))
        r["delta_fit_over_sigmaA"] = r["delta_fit"] / sA
        r["delta_heldout_over_sigmaA"] = r["delta_heldout"] / sA
        if r["half"]:
            hb = HALF / f"{name}.json"
            fb = config.RUNS / "ext" / "ks" / "e3" / f"{name.replace('_half', '')}.json"
            if hb.exists() and fb.exists():
                h = json.loads(hb.read_text())
                full = [x for x in json.loads(fb.read_text())["rows"] if x["kind"] == "bound" and x["eps"] == 0.3
                        and x["start"] == "future" and x["delta"] == h["delta"]][0]
                r.update(bound_half=h["restricted_mean"], bound_full=full["restricted_mean"],
                         bound_change=h["restricted_mean"] - full["restricted_mean"])
        rows.append(r)
        print(name, round(r["delta_heldout_over_sigmaA"], 5), flush=True)
    keys = ["system", "family", "codebook", "half", "P", "b", "total_bits", "K", "n_train", "samples_per_code", "patches",
            "states_used", "independent_trajectories", "iterations", "converged", "empty_frac", "duplicate_frac",
            "reseeded_during_fit", "stop_rule_flag", "delta_fit", "delta_heldout", "delta_fit_over_sigmaA",
            "delta_heldout_over_sigmaA", "heldout_occupancy", "unused_code_rate", "heldout_unused_rate",
            "bound_full", "bound_half", "bound_change", "fit_seconds", "method"]
    fn = config.RESULTS / "ext" / "ks" / "calibration_adequacy.csv"
    with open(fn, "w", newline="") as fh:
        fh.write(f"# git_sha={config.git_sha()}; POST-FREEZE EXTENSION\n")
        w = csv.DictWriter(fh, keys, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "halfbound":
        halfbound(sys.argv[2])
    else:
        main()
