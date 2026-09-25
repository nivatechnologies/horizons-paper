"""Post-freeze extension E3 on Kolmogorov flow (ext_freeze.yaml kolmogorov.e3 = ks.e3; Amendments 1-2; ks_fix_1).

Per tokenizer, on the 1,000-state confirmation panel, at every frame interval (0.14, 0.35, 0.70), eps 0.1/0.3/0.5,
future frames (primary) and from t = 0:
  bound (patch k-means only; exact, certified; none for residual VQ, A1), p_0, no-cross fraction, S_out(1, 3, 10);
  decode-and-integrate (reference; the integrator's Galerkin projection acts on the decoded initial state of the
  reference trajectory only); persistence (reference; hold the decoded current state).
Several tokenizers given in one call share one batched decode-and-integrate run (identical per-state results).

Per-state arrays -> runs/ext/kolmo/e3/<tokenizer>.npz; rows -> runs/ext/kolmo/e3/<tokenizer>.json;
`assemble` writes results/ext/kolmo/e3_rows.csv.

Usage: python scripts/ext_kolmo_e3.py run <device> <tokenizer ...>  |  assemble
"""
import csv
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from th import config   # noqa: E402
from th import kolmo_eval as E   # noqa: E402
from th.score import bootstrap_mean   # noqa: E402

OUT = E.RUNS / "e3"


def summarize(kind, H, crossed, extra=None):
    m, lo, hi = bootstrap_mean(H)
    r = dict(kind=kind, restricted_mean=m, ci95_lo=lo, ci95_hi=hi, frac_no_cross=float(1 - crossed.mean()),
             median=float(np.median(H)), n=int(len(H)))
    r.update(E.survival(H, crossed))
    if extra:
        r.update(extra)
    return r


def log_to(name):
    (E.RUNS / "logs").mkdir(parents=True, exist_ok=True)
    f = open(E.RUNS / "logs" / f"e3_{name}.log", "a")

    def log(s):
        f.write(time.strftime("%H:%M:%S ") + s + "\n")
        f.flush()
    return log


def run(names, device):
    sA = E.sigma_A()
    s = E.spec()
    deltas = [float(d) for d in s["frame_intervals"]]
    pnl = E.Panel()
    x0 = pnl.unit(0)
    toks = [E.Tok(n) for n in names]
    log = log_to("_".join(names) if len(names) == 1 else f"batch_{names[0]}_x{len(names)}")
    t0 = time.time()
    decs = []
    rec = {}
    for tok in toks:
        dec0, dC0, _ = tok.decode_nearest(x0, device)
        decs.append(dec0)
        base = dict(system="kolmo40", tokenizer=tok.name, family=tok.family, layout=tok.layout, P=tok.P, b=tok.b,
                    total_bits=tok.bits)
        arrays = dict(decoded_x0_err=np.sqrt(((dec0 - x0) ** 2).sum((-2, -1))) / sA)
        rows, timing = [], {}
        if tok.has_bound:
            assert np.allclose(dC0 / sA, arrays["decoded_x0_err"], rtol=1e-9, atol=1e-12)
            for d in deltas:
                t1 = time.time()
                out, dCb, cnt = E.bound(tok, pnl, d, sA, device, log=log)
                assert np.allclose(dCb, dC0, rtol=1e-12, atol=1e-12)
                for e, r in out.items():
                    for start in ("future", "from_t0"):
                        H, c = r[start]
                        arrays[f"bound_d{d:g}_eps{e}_{start}_H"] = H
                        arrays[f"bound_d{d:g}_eps{e}_{start}_crossed"] = c
                        rows.append(dict(base, delta=d, eps=e, start=start, label="bound",
                                         **summarize("bound", H, c, dict(p0=float(r["p0"].mean())))))
                timing[f"bound_d{d:g}"] = time.time() - t1
                timing[f"bound_d{d:g}_counters"] = cnt
                log(f"{tok.name} bound d{d:g} {time.time() - t1:.0f}s")
            arrays["dC0_over_sigmaA"] = dC0 / sA
        t1 = time.time()
        for d in deltas:
            err = E.persistence_err(dec0, pnl, d, sA)
            for e, r in E.horizons_from_err(err, d).items():
                for start in ("future", "from_t0"):
                    H, c = r[start]
                    arrays[f"persistence_d{d:g}_eps{e}_{start}_H"] = H
                    arrays[f"persistence_d{d:g}_eps{e}_{start}_crossed"] = c
                    rows.append(dict(base, delta=d, eps=e, start=start, label="reference",
                                     **summarize("persistence", H, c)))
        timing["persistence"] = time.time() - t1
        rec[tok.name] = dict(base=base, rows=rows, arrays=arrays, timing=timing)
    t1 = time.time()
    errs, k_stop = E.di_errors(decs, pnl, sA, device, deltas, log=log)
    t_di = time.time() - t1
    log(f"DI {len(toks)} tokenizers {t_di:.0f}s, stop unit {k_stop}")
    OUT.mkdir(parents=True, exist_ok=True)
    for tok, er in zip(toks, errs):
        r0 = rec[tok.name]
        for d in deltas:
            for e, r in E.horizons_from_err(er[d], d).items():
                for start in ("future", "from_t0"):
                    H, c = r[start]
                    r0["arrays"][f"di_d{d:g}_eps{e}_{start}_H"] = H
                    r0["arrays"][f"di_d{d:g}_eps{e}_{start}_crossed"] = c
                    r0["rows"].append(dict(r0["base"], delta=d, eps=e, start=start, label="reference",
                                           **summarize("decode_and_integrate", H, c)))
        r0["timing"]["di_integration_shared"] = t_di
        r0["timing"]["di_batch_size"] = len(toks)
        np.savez(OUT / f"{tok.name}.npz", **r0["arrays"])
        out = dict(tokenizer=tok.name, rows=r0["rows"], timing=r0["timing"], sigma_A=sA,
                   di_note="the integrator's Galerkin projection (2/3 dealias mask, mean removal) acts on the decoded "
                           "initial state of the reference trajectory only; frame 0 scored on the decoded state as is",
                   git_sha=config.git_sha(), label="post-freeze extension", codebook_meta=tok.meta)
        (OUT / f"{tok.name}.json").write_text(json.dumps(out, indent=1, default=float))
        print(tok.name, "done", round(time.time() - t0), "s", flush=True)


def assemble():
    rows = []
    for f in sorted(OUT.glob("*.json")):
        rows += json.loads(f.read_text())["rows"]
    keys = ["system", "family", "tokenizer", "P", "b", "total_bits", "delta", "eps", "start", "kind", "label",
            "restricted_mean", "ci95_lo", "ci95_hi", "frac_no_cross", "median", "p0", "S1", "S3", "S10", "n", "layout"]
    E.RES.mkdir(parents=True, exist_ok=True)
    with open(E.RES / "e3_rows.csv", "w", newline="") as fh:
        fh.write(f"# git_sha={config.git_sha()}; POST-FREEZE EXTENSION\n")
        w = csv.DictWriter(fh, keys, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print("rows", len(rows))


if __name__ == "__main__":
    torch.set_num_threads(8)
    if sys.argv[1] == "assemble":
        assemble()
    else:
        names = [n for n in sys.argv[3:] if not (OUT / f"{n}.json").exists()]
        if names:
            run(names, sys.argv[2])
