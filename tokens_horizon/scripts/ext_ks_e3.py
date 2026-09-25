"""Post-freeze extension E3 on KS (ext_freeze.yaml ks.e3, ks_fix_1): per tokenizer, on the 1,000-state confirmation
panel, at every frame interval, eps 0.1/0.3/0.5, future frames (primary) and from t = 0:
  bound (whole-state and patch k-means only; exact, certified), p_0, no-cross fraction, S_out(1, 3, 10);
  decode-and-integrate (reference; integrator projects its initial condition onto modes 1..M, reference only);
  persistence (reference; hold the decoded current state).
Whole-state ks22 rates 7, 9, 11: decode-and-integrate is NOT computed (Amendment 2 B1.1) until the A9 prediction
commit exists; pass --allow-odd-di only after that commit.

Per-state arrays -> runs/ext/ks/e3/<tokenizer>.npz; summary rows -> runs/ext/ks/e3/<tokenizer>.json
(assembled into results/ext/ks/e3_rows.csv by `assemble`).

Usage: python scripts/ext_ks_e3.py run <device> <nproc> <tokenizer ...>  |  assemble
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import csv    # noqa: E402
import json   # noqa: E402
import sys    # noqa: E402
import time   # noqa: E402
from concurrent.futures import ProcessPoolExecutor   # noqa: E402
from pathlib import Path   # noqa: E402

import numpy as np   # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from th import config   # noqa: E402
from th import ks as K   # noqa: E402
from th import ks_eval as E   # noqa: E402
from th.score import bootstrap_mean, err_rel   # noqa: E402

OUT = config.RUNS / "ext" / "ks" / "e3"
ODD = {7, 9, 11}


def summarize(kind, H, crossed, extra=None):
    m, lo, hi = bootstrap_mean(H)
    r = dict(kind=kind, restricted_mean=m, ci95_lo=lo, ci95_hi=hi, frac_no_cross=float(1 - crossed.mean()),
             median=float(np.median(H)), n=int(len(H)))
    r.update(E.survival(H, crossed))
    if extra:
        r.update(extra)
    return r


def run(tok_name, device, nproc, allow_odd_di=False):
    tok = E.Tok(tok_name)
    system = tok.system
    s = K.ks_spec(system)
    sA = E.sigma_A(system)
    lam = E.lam(system)
    deltas = [float(d) for d in s["frame_intervals"]]
    skip_di = tok.family == "whole" and tok.b in ODD and not allow_odd_di
    rows, arrays = [], {}
    t0 = time.time()
    base = dict(system=system, tokenizer=tok_name, family=tok.family, P=tok.P, b=tok.b, total_bits=tok.bits)
    arr0, pre0 = E.panel(system, "confirmation", deltas[0])
    x0 = np.asarray(arr0[:, pre0])
    dec0, dC0_exact = tok.decode_nearest(x0, device)
    arrays["decoded_x0_err"] = np.linalg.norm(dec0 - x0, axis=1) / sA
    timing = {}
    if tok.has_bound:
        for d in deltas:
            t1 = time.time()
            out, dC0, cnt = E.bound(tok, system, "confirmation", d, sA, device)
            assert np.allclose(dC0, dC0_exact, rtol=1e-12, atol=1e-12)
            for e, r in out.items():
                for start in ("future", "from_t0"):
                    H, c = r[start]
                    arrays[f"bound_d{d:g}_eps{e}_{start}_H"] = H
                    arrays[f"bound_d{d:g}_eps{e}_{start}_crossed"] = c
                    rows.append(dict(base, delta=d, eps=e, start=start, label="bound",
                                     **summarize("bound", H, c, dict(p0=float(r["p0"].mean())))))
            timing[f"bound_d{d:g}"] = time.time() - t1
            timing[f"bound_d{d:g}_counters"] = cnt
        arrays["dC0_over_sigmaA"] = dC0_exact / sA
    # persistence
    for d in deltas:
        arr, pre = E.panel(system, "confirmation", d)
        F = E.n_future(system, d)
        fut = np.asarray(arr[:, pre: pre + F + 1])
        err = err_rel(dec0[None], fut.transpose(1, 0, 2), sA)                       # (F+1, n)
        for e, r in E.horizons_from_err(err, lam, d).items():
            for start in ("future", "from_t0"):
                H, c = r[start]
                arrays[f"persistence_d{d:g}_eps{e}_{start}_H"] = H
                rows.append(dict(base, delta=d, eps=e, start=start, label="reference", **summarize("persistence", H, c)))
    # decode-and-integrate
    if skip_di:
        di_note = "not computed (Amendment 2 B1.1: whole-state odd rate before the A9 prediction commit)"
    else:
        t1 = time.time()
        with ProcessPoolExecutor(nproc) as pool:
            tr = E.di_trajectories(system, dec0, pool, nproc)
        timing["di_integration"] = time.time() - t1
        for d in deltas:
            arr, pre = E.panel(system, "confirmation", d)
            F = E.n_future(system, d)
            fut = np.asarray(arr[:, pre: pre + F + 1])
            err = err_rel(tr[f"{d:g}"].transpose(1, 0, 2), fut.transpose(1, 0, 2), sA)
            for e, r in E.horizons_from_err(err, lam, d).items():
                for start in ("future", "from_t0"):
                    H, c = r[start]
                    arrays[f"di_d{d:g}_eps{e}_{start}_H"] = H
                    arrays[f"di_d{d:g}_eps{e}_{start}_crossed"] = c
                    rows.append(dict(base, delta=d, eps=e, start=start, label="reference",
                                     **summarize("decode_and_integrate", H, c)))
        di_note = "computed; the integrator projects the decoded initial condition onto modes 1..M (reference trajectory only)"
    OUT.mkdir(parents=True, exist_ok=True)
    np.savez(OUT / f"{tok_name}.npz", **arrays)
    rec = dict(tokenizer=tok_name, rows=rows, di=di_note, timing=timing, seconds=time.time() - t0,
               git_sha=config.git_sha(), sigma_A=sA, codebook_meta=getattr(tok, "meta", {}))
    (OUT / f"{tok_name}.json").write_text(json.dumps(rec, indent=1, default=float))
    print(tok_name, "done", round(time.time() - t0), "s", di_note[:20], flush=True)


def assemble():
    rows = []
    for f in sorted(OUT.glob("*.json")):
        rows += json.loads(f.read_text())["rows"]
    keys = ["system", "family", "tokenizer", "P", "b", "total_bits", "delta", "eps", "start", "kind", "label",
            "restricted_mean", "ci95_lo", "ci95_hi", "frac_no_cross", "median", "p0", "S1", "S3", "S10", "n"]
    fn = config.RESULTS / "ext" / "ks" / "e3_rows.csv"
    with open(fn, "w", newline="") as fh:
        fh.write(f"# git_sha={config.git_sha()}; POST-FREEZE EXTENSION\n")
        w = csv.DictWriter(fh, keys, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print("rows", len(rows))


if __name__ == "__main__":
    if sys.argv[1] == "assemble":
        assemble()
    else:
        device, nproc = sys.argv[2], int(sys.argv[3])
        for name in sys.argv[4:]:
            if (OUT / f"{name}.json").exists():
                continue
            run(name, device, nproc)
