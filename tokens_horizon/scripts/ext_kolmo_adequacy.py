"""Post-freeze extension, Kolmogorov calibration adequacy (Amendment 1 A5; kolmogorov.tokenizers.calibration_adequacy).

Per codebook: samples per code (fit patches / K; patches, whole states and independent trajectories separately), k-means
diagnostics (iterations, converged, empty and duplicate fractions, re-seeded clusters; stop rule > 1% or not converged
-> flagged, used and labelled), fit and held-out distortion delta = RMS over states of ||x - decode(x)|| (the scored
norm; also / sigma_A), held-out occupancy, unused-code rate (fit), held-out unused rate. Halved refits (suffix _half):
the same plus the change in the confirmation bound (restricted mean, primary Delta 0.35, eps 0.3, future frames).
Exact decoding by th/patchvq.exact_nn (patch-wise; stage-wise for residual VQ).

Usage: python scripts/ext_kolmo_adequacy.py table <device>  |  halfbound <device>
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from th import config   # noqa: E402
from th import kolmo_eval as E   # noqa: E402
from th.patchvq import exact_nn, to_patches_2d   # noqa: E402

HALF = E.RUNS / "e3_half"


def ct(C, device):
    Ct = torch.as_tensor(C, dtype=torch.float32, device=device)
    return dict(C64=np.asarray(C, float), C32=Ct, cn=(Ct * Ct).sum(1))


def patch_err(C, X, side, device, chunk_states=4096):
    e2, labs = [], []
    c = ct(C, device)
    for s in range(0, len(X), chunk_states):
        Xp = to_patches_2d(np.asarray(X[s:s + chunk_states]), side, side)
        n, P, d = Xp.shape
        idx, d2, _ = exact_nn(Xp.reshape(-1, d), c, device)
        e2.append(d2.reshape(n, P).sum(1))
        labs.append(idx)
    return np.concatenate(e2), np.concatenate(labs)


def rvq_err(Cs, X, device, chunk_states=8192):
    out = []
    cs = [ct(C, device) for C in Cs]
    for s in range(0, len(X), chunk_states):
        R = np.asarray(X[s:s + chunk_states]).reshape(-1, 4096).copy()
        for C, c in zip(Cs, cs):
            idx, _, _ = exact_nn(R, c, device)
            R -= C[idx]
        out.append((R ** 2).sum(1))
    return np.concatenate(out)


def halfbound(device, only=None):
    HALF.mkdir(parents=True, exist_ok=True)
    pnl = E.Panel()
    sA = E.sigma_A()
    d = float(E.spec()["primary_delta"])
    for f in sorted(E.CB.glob("*_half.npz")):
        name = f.stem
        if (HALF / f"{name}.json").exists() or (only and name not in only):
            continue
        tok = E.Tok(name)
        out, dC0, cnt = E.bound(tok, pnl, d, sA, device)
        H, c = out[0.3]["future"]
        rec = dict(tokenizer=name, delta=d, eps=0.3, start="future", restricted_mean=float(H.mean()),
                   frac_no_cross=float(1 - c.mean()), p0=float(out[0.3]["p0"].mean()), **E.survival(H, c),
                   git_sha=config.git_sha(), label="post-freeze extension")
        np.savez(HALF / f"{name}.npz", H=H, crossed=c, dC0=dC0)
        (HALF / f"{name}.json").write_text(json.dumps(rec, indent=1))
        print(name, rec, flush=True)


def table(device):
    Xf = np.load(E.CACHE / "calib_fit.npy", mmap_mode="r").reshape(-1, 64, 64)
    Xh = np.load(E.CACHE / "calib_heldout.npy", mmap_mode="r").reshape(-1, 64, 64)
    trh = np.load(E.CACHE / "calib_heldout_traj.npy")
    sA = E.sigma_A()
    rows = []
    for f in sorted(E.CB.glob("*.npz")):
        name = f.stem
        z = np.load(f)
        meta = json.loads(str(z["meta"]))
        family = name.split("_")[1]
        r = dict(system="kolmo40", family=family, codebook=name, half=name.endswith("_half"), K=meta["K"],
                 n_train=meta["n_train"], samples_per_code=meta["n_train"] / meta["K"], iterations=meta["iterations"],
                 converged=meta["converged"], empty_frac=meta["empty_frac"], duplicate_frac=meta["duplicate_frac"],
                 reseeded_during_fit=meta["reseeded_during_fit"], fit_seconds=meta["seconds"],
                 method=meta.get("method", ""))
        r["stop_rule_flag"] = bool((not meta["converged"]) or meta["empty_frac"] > 0.01 or meta["duplicate_frac"] > 0.01)
        if family == "rvq":
            s = int(name.split("_")[2][1:])
            Cs = [np.load(E.CB / f"kolmo_rvq_s{i}.npz")["C"] for i in range(1, s + 1)]
            e2h = rvq_err(Cs, Xh, device)
            e2f = rvq_err(Cs, Xf, device)
            r.update(layout="whole", P=None, b=8, stage=s, total_bits=8 * s, states_used=meta.get("states_used"),
                     independent_trajectories=meta.get("independent_trajectories"),
                     delta_fit=float(np.sqrt(e2f.mean())), delta_heldout=float(np.sqrt(e2h.mean())),
                     fit_delta_note="RMS over all calibration fit states")
        else:
            side = int(name.split("_")[2][1:])
            b = int(name.split("_")[3][1:])
            e2h, lab = patch_err(z["C"], Xh, side, device)
            occ = np.bincount(lab, minlength=meta["K"])
            r.update(layout=f"{side}x{side}", P=side * side, b=b, total_bits=side * side * b,
                     patches=meta.get("patches"), states_used=meta.get("states_used"),
                     independent_trajectories=meta.get("independent_trajectories"),
                     delta_fit=float(np.sqrt(meta["mse"] * side * side)), delta_heldout=float(np.sqrt(e2h.mean())),
                     heldout_occupancy=float((occ > 0).mean()), unused_code_rate=float(meta["empty_frac"]),
                     heldout_unused_rate=float((occ == 0).mean()),
                     fit_delta_note="sqrt(P * fit mse per patch) on the patches the codebook was fitted on")
        np.save(E.RUNS / f"heldout_err2_{name}.npy", np.bincount(trh, weights=e2h) / np.bincount(trh))
        r["delta_fit_over_sigmaA"] = r["delta_fit"] / sA
        r["delta_heldout_over_sigmaA"] = r["delta_heldout"] / sA
        if r["half"]:
            hb = HALF / f"{name}.json"
            fb = E.RUNS / "e3" / f"{name.replace('_half', '')}.json"
            if hb.exists() and fb.exists():
                h = json.loads(hb.read_text())
                full = [x for x in json.loads(fb.read_text())["rows"] if x["kind"] == "bound" and x["eps"] == 0.3
                        and x["start"] == "future" and x["delta"] == h["delta"]][0]
                r.update(bound_half=h["restricted_mean"], bound_full=full["restricted_mean"],
                         bound_change=h["restricted_mean"] - full["restricted_mean"])
            full_cb = E.CB / f"{name.replace('_half', '')}.npz"
            if full_cb.exists():
                r["delta_heldout_full"] = next((x["delta_heldout"] for x in rows if x["codebook"] == full_cb.stem), None)
        rows.append(r)
        print(name, round(r["delta_heldout_over_sigmaA"], 5), flush=True)
    keys = ["system", "family", "layout", "codebook", "half", "P", "b", "total_bits", "K", "n_train", "samples_per_code",
            "patches", "states_used", "independent_trajectories", "iterations", "converged", "empty_frac",
            "duplicate_frac", "reseeded_during_fit", "stop_rule_flag", "delta_fit", "delta_heldout",
            "delta_fit_over_sigmaA", "delta_heldout_over_sigmaA", "heldout_occupancy", "unused_code_rate",
            "heldout_unused_rate", "delta_heldout_full", "bound_full", "bound_half", "bound_change", "fit_seconds",
            "method"]
    E.RES.mkdir(parents=True, exist_ok=True)
    with open(E.RES / "calibration_adequacy.csv", "w", newline="") as fh:
        fh.write(f"# git_sha={config.git_sha()}; POST-FREEZE EXTENSION\n")
        w = csv.DictWriter(fh, keys, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


if __name__ == "__main__":
    torch.set_num_threads(8)
    if sys.argv[1] == "halfbound":
        halfbound(sys.argv[2], sys.argv[3:] or None)
    else:
        table(sys.argv[2])
